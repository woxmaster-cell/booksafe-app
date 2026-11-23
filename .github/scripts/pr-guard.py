#!/usr/bin/env python3
# pr-guard: mechanischer Check fuer PRs in den BookSafe-Repos.
# Gibt nie Werte aus der Sperrliste, keine Namen oder Mails und keine Diff-Ausschnitte aus,
# nur Ort, Feld und Art eines Treffers. Exit 0 = gruen, Exit 1 = rot.
# Lokal: PR_GUARD_REPO, BASE_SHA, HEAD_SHA, PR_TITLE_FILE, PR_BODY_FILE und
# PR_GUARD_DENYLIST aus der Umgebung; in GitHub Actions kommen Titel und Body aus GITHUB_EVENT_PATH.
import json
import os
import re
import subprocess
import sys

IDS = {("woxmaster-cell", "woxmaster@googlemail.com"),  # je Commit genau ein Paar,
       ("Claude", "noreply@anthropic.com")}  # fuer Autor und Committer gleich
REPOS = {
    "woxmaster-cell/BookSafe": "ios",
    "woxmaster-cell/BookSafe-Android": "android",
    "woxmaster-cell/booksafe-ops": "ops",
    "woxmaster-cell/booksafe-app": "app",
}
# Literale so zusammengesetzt, dass dieses Skript seinen eigenen Check nicht ausloest.
HOME_PATH = "/" + "Users" + "/"
TRAILER_RE = re.compile(
    r"^\s*(co-authored-by|signed-off-by|reviewed-by|acked-by|tested-by|reported-by|"
    r"suggested-by|helped-by|generated-by|made-with|claude-session|cursor-session)\s*:",
    re.I | re.M)
FOOTER_RE = re.compile(
    r"generated with \[?(claude|cursor)|claude\.ai/(code|chat|share)|cursor\.com/(agents|share)|"
    r"\U0001F916 generated|made with (claude|cursor)", re.I)
SECRET_LINE_RES = [
    ("PEM-Schluessel", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----")),
    ("AuthKey-Datei", re.compile(r"AuthKey_[A-Z0-9]{10}\.p8")),
    ("Key- oder Issuer-ID", re.compile(
        r"(?i:issuer[ _-]?id|key[ _-]?id)[\"'\s:=]+[\"']?"
        r"(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|(?=[A-Z]*[0-9])[A-Z0-9]{10})\b")),
    ("Token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}|\bgithub_pat_[A-Za-z0-9_]{50,}|"
                         r"\bAIza[0-9A-Za-z_-]{35}\b|\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("Token-Zuweisung", re.compile(r"(?i:goatcounter_api_token|telegram_bot_token)\s*[:=]\s*[\"']?[A-Za-z0-9:_-]{16,}")),
]
SECRET_NAME_RE = re.compile(r"(\.p8|\.jks|\.keystore|(^|/)keystore\.properties)$", re.I)
LIMIT_RE = re.compile(r"\b(bookLimit|warnThreshold)\b[^=\n]*=\s*1_?000\b")
LIMIT_FILES_RE = re.compile(r"\.(swift|kt|kts)$")
TEXT_FILES_RE = re.compile(r"\.(md|markdown|txt|html?)$", re.I)
DOC_ONLY_RE = re.compile(r"\.(md|markdown|txt|csv|jsonl)$", re.I)
S2_MIN_RE = re.compile(r"^(\.github/|\.claude/|CLAUDE\.md$|Scripts/|scripts/|fastlane/|Android/fastlane/|Darwin/fastlane/)")
S0_ALLOW = {
    "ops": re.compile(
        r"^data/asc/(downloads/standard/daily/\d{4}-\d{2}-\d{2}\.csv|downloads/detailed/monthly/\d{4}-\d{2}\.csv|"
        r"snapshot/downloads-(standard-daily-\d{4}-\d{2}-\d{2}|detailed-monthly-\d{4}-\d{2})\.csv|"
        r"sales/daily/\d{4}-\d{2}-\d{2}\.csv|manifest\.json)$"),
    "ios": re.compile(
        r"^docs/marketing/AppleAdAgent/(berichte/\d{4}-(KW\d{2}|\d{2}-\d{2})\.(md|telegram\.txt)|"
        r"memory/(MEMORY\.md|kpi-verlauf\.csv|aenderungen\.jsonl))$"),
}
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

findings = []


def bad(msg):
    findings.append(msg)


def git(*args):
    r = subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if r.returncode != 0:
        raise RuntimeError("git " + args[0])
    return r.stdout.decode("utf-8", "replace")


def load_denylist():
    raw = os.environ.get("PR_GUARD_DENYLIST", "")
    plain, code_ok, short, masks = [], [], 0, []
    for line in raw.replace("\r", "\n").split("\n"):
        e = line.strip()
        if not e or e.startswith("#"):
            continue
        target = plain
        if e.lower().startswith("code-ok:"):
            e = e[8:].strip()
            target = code_ok
        if len(e) < 4:
            short += 1
            continue
        target.append(e.lower())
        masks.extend({e, e.lower()})
    if os.environ.get("GITHUB_ACTIONS") == "true":
        # Die Zeile wird vom Runner verarbeitet und erscheint nicht im Log.
        for e in masks:
            sys.stdout.write("::add-mask::" + e + "\n")
        sys.stdout.flush()
    return plain, code_ok, short


def hits(text, entries):
    t = text.lower()
    return any(e in t for e in entries)


def strip_code_ok(text, code_ok):
    t = text.lower()
    for e in code_ok:
        t = t.replace(e, " ")
    return t


def field_value(body, label):
    vals = []
    for line in body.split("\n"):
        s = line.replace("*", "").strip().lstrip("-> ").strip()
        m = re.match(r"(?i)" + re.escape(label) + r"\s*:\s*(.*)$", s)
        if m:
            vals.append(m.group(1).strip())
    return vals


def main():
    repo = os.environ.get("PR_GUARD_REPO", "")
    kind = REPOS.get(repo)
    if not kind:
        bad("Unbekanntes Repo, pr-guard kennt nur die vier BookSafe-Repos.")
        return
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    title = body = ""
    fork = False
    ev = os.environ.get("GITHUB_EVENT_PATH")
    if ev and os.path.isfile(ev):
        with open(ev, encoding="utf-8") as f:
            pr = json.load(f).get("pull_request") or {}
        title = pr.get("title") or ""
        body = pr.get("body") or ""
        hr = ((pr.get("head") or {}).get("repo") or {}).get("full_name")
        br = ((pr.get("base") or {}).get("repo") or {}).get("full_name")
        fork = hr != br
    else:
        if os.environ.get("PR_TITLE_FILE"):
            with open(os.environ["PR_TITLE_FILE"], encoding="utf-8") as f:
                title = f.read()
        if os.environ.get("PR_BODY_FILE"):
            with open(os.environ["PR_BODY_FILE"], encoding="utf-8") as f:
                body = f.read()
    if not re.fullmatch(r"[0-9a-f]{40}", base) or not re.fullmatch(r"[0-9a-f]{40}", head):
        bad("BASE_SHA oder HEAD_SHA fehlt oder ist kein voller SHA.")
        return

    plain, code_ok, short = load_denylist()
    allent = plain + code_ok
    if fork:
        bad("PR aus einem Fork: Sperrliste dort nicht verfuegbar, Check bewusst rot. Pruefung von Hand.")
    elif not allent:
        bad("Secret `PR_GUARD_DENYLIST` ist nicht gesetzt.")
    if short:
        bad("Sperrliste: %d Eintraege kuerzer als 4 Zeichen, bitte im Secret korrigieren." % short)

    # 1. Commits
    commits = [c for c in git("rev-list", "--reverse", base + ".." + head).split() if c]
    if not commits:
        bad("Keine neuen Commits gegenueber der Basis gefunden.")
    for c in commits:
        meta = git("show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce", c).rstrip("\n").split("\x00")
        if len(meta) != 4 or tuple(meta[0:2]) not in IDS:
            bad("Commit %s: Autor ist nicht die erlaubte Identitaet." % c[:12])
        if len(meta) != 4 or tuple(meta[2:4]) not in IDS or meta[2:4] != meta[0:2]:
            bad("Commit %s: Committer ist nicht die erlaubte Identitaet oder nicht gleich dem Autor." % c[:12])
        msg = git("show", "-s", "--format=%B", c)
        if TRAILER_RE.search(msg):
            bad("Commit %s: Nachricht enthaelt einen Trailer." % c[:12])
        if FOOTER_RE.search(msg):
            bad("Commit %s: Nachricht enthaelt einen Footer oder Session-Link." % c[:12])
        if HOME_PATH in msg:
            bad("Commit %s: Nachricht enthaelt einen Klarpfad unter Home." % c[:12])
        if hits(msg, allent):
            bad("Commit %s: Sperrlisten-Treffer in der Nachricht." % c[:12])

    # 2. PR-Titel und -Body
    for label, text in (("PR-Titel", title), ("PR-Body", body)):
        if TRAILER_RE.search(text):
            bad(label + ": enthaelt einen Trailer.")
        if FOOTER_RE.search(text):
            bad(label + ": enthaelt einen Footer oder Session-Link.")
        if HOME_PATH in text:
            bad(label + ": enthaelt einen Klarpfad unter Home.")
        if hits(text, allent):
            bad(label + ": Sperrlisten-Treffer.")

    # 3. Dateien und hinzugefuegte Zeilen
    status = git("diff", "--no-color", "--no-renames", "--name-status", base + "..." + head)
    changed, deleted = [], []
    for line in status.split("\n"):
        if not line.strip():
            continue
        st, _, path = line.partition("\t")
        if st.startswith("D"):
            deleted.append(path)
        else:
            changed.append(path)
    allpaths = changed + deleted
    for p in changed:
        name_hit = hits(p, allent)
        shown = "<Pfad mit Sperrlisten-Treffer>" if name_hit else p
        if name_hit:
            bad("Dateipfad: Sperrlisten-Treffer.")
        if SECRET_NAME_RE.search(p):
            bad("Datei %s: Schluessel- oder Keystore-Datei." % shown)
    diff = git("diff", "--no-color", "--no-ext-diff", "--no-renames", "-U0", base + "..." + head)
    cur = None
    reported = set()
    for line in diff.split("\n"):
        if line.startswith("+++ "):
            cur = line[6:] if line.startswith("+++ b/") else None
            continue
        if line.startswith("Binary files ") and " and b/" in line:
            bp = line.rsplit(" and b/", 1)[1].rsplit(" differ", 1)[0]
            if not hits(bp, allent):
                print("Hinweis: Binaerdatei %s nicht auf Inhalt geprueft." % bp)
            continue
        if cur is None or not line.startswith("+") or line.startswith("+++"):
            continue
        text = line[1:]
        shown = "<Pfad mit Sperrlisten-Treffer>" if hits(cur, allent) else cur
        def once(kind_msg):
            key = (shown, kind_msg)
            if key not in reported:
                reported.add(key)
                bad("Datei %s: %s" % (shown, kind_msg))
        if HOME_PATH in text:
            once("Klarpfad unter Home in hinzugefuegter Zeile.")
        for label, rx in SECRET_LINE_RES:
            if rx.search(text):
                once("Secret-Muster (%s) in hinzugefuegter Zeile." % label)
        if LIMIT_FILES_RE.search(cur) and LIMIT_RE.search(text):
            once("Freibuecher-Limit 1000 gesetzt.")
        if allent:
            probe = text.lower() if TEXT_FILES_RE.search(cur) else strip_code_ok(text, code_ok)
            if hits(probe, allent):
                once("Sperrlisten-Treffer in hinzugefuegter Zeile.")

    # 4. Stufe
    visible = COMMENT_RE.sub("", body)
    stufen = field_value(visible, "Stufe")
    stage = None
    if len(stufen) != 1:
        bad("PR-Body: Feld `Stufe:` fehlt oder steht mehrfach.")
    else:
        m = re.match(r"S([0-3])\b", stufen[0])
        if not m:
            bad("PR-Body: `Stufe:` nennt nicht genau eine von S0, S1, S2, S3.")
        else:
            stage = int(m.group(1))
    if stage is not None:
        if stage == 0:
            allow = S0_ALLOW.get(kind)
            if allow is None:
                bad("Stufe S0 gibt es in diesem Repo nicht.")
            else:
                if deleted:
                    bad("Stufe S0: PR loescht Dateien, in S0 nicht erlaubt.")
                if any(not allow.match(p) for p in changed):
                    bad("Stufe S0: mindestens eine Datei liegt ausserhalb der S0-Allowlist.")
        if stage < 2 and (kind == "app" or any(S2_MIN_RE.match(p) for p in allpaths)):
            bad("Stufe zu niedrig: Dateien unter .github, .claude, CLAUDE.md, Skripten, fastlane oder booksafe-app sind mindestens S2.")

    # 5. Testlog (nur iOS und Android, nur bei Nicht-Doku-PRs)
    if kind in ("ios", "android"):
        doc_only = bool(allpaths) and all(
            DOC_ONLY_RE.search(p) and not p.startswith(".github/") for p in allpaths)
        if not doc_only:
            tl = field_value(visible, "Testlog")
            ok = len(tl) == 1 and "<" not in tl[0] and re.match(
                r"(?i)(kommentar\b.*\b[0-9a-f]{40}\b|offen, weil\s+\S.{4,}|nicht n(oe|ö)tig, weil\s+\S.{4,})", tl[0])
            if not ok:
                bad("PR-Body: Feld `Testlog:` fehlt, ist leer oder nicht ausgefuellt (Code-PR).")

    print("pr-guard: %d Commits, %d Dateien, Stufe %s." % (
        len(commits), len(allpaths), "S%d" % stage if stage is not None else "-"))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # nur der Typ, nie der Inhalt
        bad("Interner Fehler (%s), Check bewusst rot." % type(exc).__name__)
    gha = os.environ.get("GITHUB_ACTIONS") == "true"
    for f in findings:
        print(("::error::" if gha else "ROT: ") + f)
    if findings:
        print("pr-guard: rot, %d Befunde." % len(findings))
        sys.exit(1)
    print("pr-guard: gruen.")
    sys.exit(0)
