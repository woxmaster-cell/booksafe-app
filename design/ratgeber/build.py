#!/usr/bin/env python3
"""Erzeugt die Ratgeber-Seiten unter /ratgeber/ (Übersicht + Artikel).

Die Inhalte stehen in articles.py; diese Datei hält nur das gemeinsame Gerüst,
damit Kopf, Stil und Fuß auf allen Seiten gleich bleiben.

    python3 design/ratgeber/build.py

Regeln für die Texte (Marketing-Konzept): jede Zahl aus einer Quelle (Code oder
Store-Angabe), keine fremden App-Namen, kein Klarname — Label Sisofa.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from articles import ARTICLES, PUBLISHED  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://booksafe.app/ratgeber/"
STORE = "https://apps.apple.com/de/app/booksafe/id6779730178"

CSS = """
  :root {
    --navy: var(--brand-navy);
    --navy-2: var(--brand-navy-light);
    --gold: var(--brand-gold);
    --gold-deep: var(--brand-gold-deep);
    --bg: var(--web-light-bg);
    --panel: var(--web-light-panel);
    --text: var(--web-light-text);
    --muted: var(--web-light-muted);
    --hairline: var(--web-light-hairline);
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: var(--web-dark-bg);
      --panel: var(--web-dark-panel);
      --text: var(--web-dark-text);
      --muted: var(--web-dark-muted);
      --gold-deep: var(--brand-gold);
      --hairline: var(--web-dark-hairline);
    }
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }
  a { color: var(--gold-deep); }
  header {
    background: linear-gradient(180deg, var(--navy-2) 0%, var(--navy) 100%);
    color: var(--web-hero-text);
    text-align: center;
    padding: 44px 24px 48px;
  }
  header .icon { width: 64px; height: 64px; border-radius: 15px; margin: 0 auto 16px; display: block; box-shadow: 0 8px 22px var(--web-hero-icon-shadow); }
  header .kicker { color: var(--gold); font-weight: 700; font-size: 13px; letter-spacing: 0.12em; text-transform: uppercase; }
  header h1 { font-size: 28px; letter-spacing: -0.02em; max-width: 720px; margin: 6px auto 0; line-height: 1.25; }
  header .sub { color: var(--web-hero-text-faint); margin: 8px auto 0; max-width: 620px; }
  header nav { margin-top: 14px; font-size: 14px; }
  header nav a { color: var(--gold); text-decoration: none; font-weight: 600; margin: 0 8px; }
  header nav a:hover { text-decoration: underline; }
  main { max-width: 720px; margin: 0 auto; padding: 36px 20px 24px; }
  section.card {
    background: var(--panel);
    border: 1px solid var(--hairline);
    border-radius: 16px;
    padding: 24px 26px;
    margin-bottom: 24px;
  }
  h1, h2 { font-family: var(--font-display); letter-spacing: -0.02em; }
  h2 { font-size: 21px; margin-bottom: 6px; }
  h3 { font-size: 17px; margin: 22px 0 4px; }
  p + p, ul + p, p + ul { margin-top: 10px; }
  ul { padding-left: 1.2em; }
  li + li { margin-top: 6px; }
  .lead { font-size: 17.5px; }
  .note { color: var(--muted); font-size: 14.5px; margin-top: 12px; }
  .meta { color: var(--muted); font-size: 13.5px; margin-top: 14px; }
  figure.shot { margin: 18px auto 4px; max-width: 220px; }
  figure.shot img { display: block; width: 100%; height: auto; border-radius: 14px; border: 1px solid var(--hairline); }
  figure.shot figcaption { margin-top: 8px; font-size: 13.5px; color: var(--muted); text-align: center; }
  picture { display: contents; }
  .list a.item { display: block; text-decoration: none; color: inherit; padding: 16px 0; border-top: 1px solid var(--hairline); }
  .list a.item:first-of-type { border-top: 0; padding-top: 4px; }
  .list a.item strong { display: block; font-family: var(--font-display); font-size: 18px; color: var(--gold-deep); letter-spacing: -0.01em; }
  .list a.item span { color: var(--muted); font-size: 15px; }
  .list a.item:hover strong { text-decoration: underline; }
  .cta p { margin-bottom: 4px; }
  .store { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin-top: 14px; }
  .store img { height: 48px; width: auto; display: block; }
  .more a { display: block; margin-top: 6px; }
  footer {
    border-top: 1px solid var(--hairline);
    padding: 36px 24px 48px;
    text-align: center;
    font-size: 14px;
    color: var(--muted);
  }
  footer nav { margin-bottom: 12px; }
  footer nav a { margin: 0 12px; text-decoration: none; font-weight: 600; }
  footer nav a:hover { text-decoration: underline; }
  :focus-visible { outline: 3px solid var(--navy); outline-offset: 3px; }
  header :focus-visible { outline-color: var(--gold); }
  @media (prefers-color-scheme: dark) {
    :focus-visible { outline-color: var(--gold); }
  }
  @media (max-width: 520px) {
    header { padding: 38px 20px 42px; }
    header h1 { font-size: 24px; }
    section.card { padding: 20px 18px; }
  }
"""


def page(*, url, rel, title, description, h1, sub, kicker, body, jsonld):
    """Ein vollständiges Dokument. `rel` ist der Pfad zurück zur Wurzel."""
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2C4B6B">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="https://booksafe.app/assets/og-de.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="BookSafe — Deine Bibliothek gehört dir.">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="de_DE">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{rel}assets/app-icon.png">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="{rel}assets/tokens.css">
<link rel="stylesheet" href="{rel}assets/fonts.css">
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
</script>
<style>{CSS}</style>
</head>
<body>

<header>
  <picture><source srcset="{rel}assets/app-icon.webp" type="image/webp"><img class="icon" src="{rel}assets/app-icon.png" alt="BookSafe App-Icon" width="64" height="64"></picture>
  <p class="kicker">{e(kicker)}</p>
  <h1>{e(h1)}</h1>
  <p class="sub">{e(sub)}</p>
  <nav><a href="{rel}">Startseite</a>{'' if rel == '../' else f'<a href="{rel}ratgeber/">Alle Ratgeber</a>'}</nav>
</header>

<main>
{body}
</main>

<footer>
  <nav>
    <a href="{rel}">Startseite</a>
    <a href="{rel}ratgeber/">Ratgeber</a>
    <a href="{rel}support/">Support</a>
  </nav>
  <p>BookSafe · Sisofa · <a href="mailto:kontakt@sisofa.de">kontakt@sisofa.de</a></p>
  <p>© 2026 Sisofa. Apple, das Apple-Logo und App Store sind Marken von Apple Inc.</p>
</footer>

</body>
</html>
"""


def shot(rel, name, alt, caption):
    return (f'<figure class="shot"><picture><source srcset="{rel}assets/{name}.webp" type="image/webp">'
            f'<img src="{rel}assets/{name}.jpg" alt="{html.escape(alt)}" loading="lazy" width="720" height="1564">'
            f'</picture><figcaption>{html.escape(caption)}</figcaption></figure>')


def cta(rel):
    return f"""  <section class="card cta">
    <h2>BookSafe ausprobieren</h2>
    <p>BookSafe ist eine Buchverwaltung für iPhone und iPad, ohne Konto und ohne Tracking. Kostenlos bis 50 Bücher, danach einmalig 3,99 € für BookSafe Pro, kein Abo.</p>
    <div class="store">
      <a href="{STORE}"><img src="{rel}assets/badge-de.svg" alt="Laden im App Store" width="144" height="48"></a>
    </div>
  </section>"""


def breadcrumbs(*trail):
    """Pfad für das Suchergebnis: BookSafe › Ratgeber › Artikel."""
    steps = (("BookSafe", "https://booksafe.app/"),) + trail
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": name, "item": link}
                            for i, (name, link) in enumerate(steps, start=1)],
    }


def build():
    publisher = {"@type": "Organization", "name": "Sisofa", "url": "https://booksafe.app/"}
    written = []

    for a in ARTICLES:
        rel = "../../"
        url = f"{BASE}{a['slug']}/"
        body = a["body"].replace("{SHOT:", "\x00").split("\x00")
        # Platzhalter {SHOT:name|alt|caption} → Bild
        out = [body[0]]
        for part in body[1:]:
            spec, rest = part.split("}", 1)
            out.append(shot(rel, *spec.split("|")) + rest)
        others = [o for o in ARTICLES if o is not a]
        more = "\n".join(f'    <a href="../{o["slug"]}/">{html.escape(o["h1"])}</a>' for o in others)
        content = f"""  <section class="card">
{''.join(out)}
    <p class="meta">Sisofa · {PUBLISHED.strftime('%d.%m.%Y')}</p>
  </section>

{cta(rel)}

  <section class="card more">
    <h2>Weitere Ratgeber</h2>
{more}
  </section>"""
        jsonld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["h1"],
            "description": a["description"],
            "inLanguage": "de",
            "datePublished": PUBLISHED.isoformat(),
            "dateModified": PUBLISHED.isoformat(),
            "author": publisher,
            "publisher": publisher,
            "mainEntityOfPage": url,
            "image": "https://booksafe.app/assets/og-de.jpg",
        }
        jsonld = [jsonld, breadcrumbs(("Ratgeber", BASE), (a["h1"], url))]
        doc = page(url=url, rel=rel, title=a["title"], description=a["description"], h1=a["h1"],
                   sub=a["sub"], kicker="Ratgeber", body=content, jsonld=jsonld)
        target = ROOT / "ratgeber" / a["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc, encoding="utf-8")
        written.append(target)

    items = "\n".join(
        f'    <a class="item" href="{o["slug"]}/"><strong>{html.escape(o["h1"])}</strong>'
        f'<span>{html.escape(o["teaser"])}</span></a>' for o in ARTICLES)
    content = f"""  <section class="card list">
{items}
  </section>

{cta('../')}"""
    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "BookSafe Ratgeber",
        "inLanguage": "de",
        "url": BASE,
        "publisher": publisher,
        "hasPart": [{"@type": "Article", "headline": o["h1"], "url": f"{BASE}{o['slug']}/"} for o in ARTICLES],
    }
    jsonld = [jsonld, breadcrumbs(("Ratgeber", BASE))]
    doc = page(url=BASE, rel="../", title="BookSafe Ratgeber: rund ums Lesen und Sammeln",
               description="Kurze Ratgeber rund um die eigene Bibliothek: Neuerscheinungen im Blick behalten, Buchreihen in der richtigen Reihenfolge lesen, den Stapel ungelesener Bücher abbauen, Leihfristen und Bücher erfassen.",
               h1="Ratgeber rund ums Lesen und Sammeln", sub="Kurze Antworten auf Fragen, die sich jede Leserin und jeder Leser irgendwann stellt.",
               kicker="BookSafe", body=content, jsonld=jsonld)
    target = ROOT / "ratgeber" / "index.html"
    target.write_text(doc, encoding="utf-8")
    written.append(target)

    for t in written:
        print(t.relative_to(ROOT))


if __name__ == "__main__":
    build()
