"""Erzeugt neu-in-1-9/, en/whats-new-1-9/, neu-in-1-8/, en/whats-new-1-8/, versionen/ und en/versions/ der Landingpage.

Aufruf: python3 -I build_pages.py <landingpage-repo> <asc_notes.json>
Quelle der Detailseiten 1.2–1.8: deren eigenes <main> (Karten „Neu“/„Verbessert“/„Behoben“).
Quelle 0.4–1.1: die im App Store veröffentlichten Versionshinweise (ASC-API).
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
NOTES = json.loads(Path(sys.argv[2]).read_text())

DE_MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
             "September", "Oktober", "November", "Dezember"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]
# Store-live-Daten (Produktstatus.md §3)
RELEASES = {
    "1.9": (28, 10), "1.8": (17, 10), "1.7": (12, 10), "1.6": (7, 10), "1.5": (27, 9), "1.4": (25, 9), "1.3": (23, 9),
    "1.2": (14, 9), "1.1": (15, 8), "1.0": (6, 8), "0.9": (28, 7), "0.8": (24, 7),
    "0.7": (16, 7), "0.6": (12, 7), "0.5": (7, 7), "0.4": (1, 7),
}
DETAIL_PAGES = ["1.8", "1.7", "1.6", "1.5", "1.4", "1.3", "1.2"]
NOTE_ONLY = ["1.1", "1.0", "0.9", "0.8", "0.7", "0.6", "0.5", "0.4"]


def date(v, lang):
    d, m = RELEASES[v]
    return f"{d}. {DE_MONTHS[m - 1]} 2026" if lang == "de" else f"{d} {EN_MONTHS[m - 1]} 2026"


L = {
    "de": dict(
        detail=lambda v: f"neu-in-{v.replace('.', '-')}/",
        locale="de_DE", og="og-de.jpg", og_alt="BookSafe — Deine Bibliothek gehört dir.",
        badge="badge-de.svg", badge_alt="Laden im App Store", store="https://apps.apple.com/de/app/booksafe/id6779730178",
        home="Startseite", support="Support", contact="Kontakt", contact_href="support/#kontakt",
        other_name="English", other_lang="en",
        copyright="© 2026 Sisofa. Apple, das Apple-Logo und App Store sind Marken von Apple Inc.",
        back="← Zur Startseite", back2="← Zurück zur Startseite",
    ),
    "en": dict(
        detail=lambda v: f"whats-new-{v.replace('.', '-')}/",
        locale="en_US", og="og-en.jpg", og_alt="BookSafe — Your library belongs to you.",
        badge="badge-en.svg", badge_alt="Download on the App Store", store="https://apps.apple.com/app/booksafe/id6779730178",
        home="Home", support="Support", contact="Contact", contact_href="support/#contact",
        other_name="Deutsch", other_lang="de",
        copyright="© 2026 Sisofa. Apple, the Apple logo and App Store are trademarks of Apple Inc.",
        back="← Back to the home page", back2="← Back to the home page",
    ),
}

TEMPLATE = {"de": (ROOT / "neu-in-1-7/index.html").read_text(),
            "en": (ROOT / "en/whats-new-1-7/index.html").read_text()}


def style_block(lang):
    t = TEMPLATE[lang]
    return t[t.index("<style>"):t.index("</style>") + len("</style>")]


EXTRA_CSS = """
  /* Archiv (versionen/): Sprungleiste zu den Versionen und die tieferen Ebenen,
     die durch das Einbetten der Detailseiten entstehen (h3 -> h4). */
  .version-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
  .version-nav a {
    font-size: 14px; font-weight: 600; text-decoration: none;
    border: 1px solid var(--hairline); border-radius: 999px; padding: 4px 12px;
  }
  .version-nav a:hover { background: var(--hairline); }
  section.version { scroll-margin-top: 16px; }
  section.version > h2 { font-size: 24px; }
  section.version h3 { font-size: 18px; margin: 24px 0 4px; }
  section.version h4 { font-size: 16px; margin: 18px 0 4px; }
  section.version h4 .num { font-family: var(--font-display); color: var(--gold-deep); margin-right: 8px; }
  .more { margin-top: 18px; font-weight: 600; }
  .archive-link { display: inline-block; margin-top: 12px; font-weight: 600; }
  .film-figure.four { grid-template-columns: repeat(4, minmax(0, 1fr)); max-width: 720px; }
"""


def page(lang, *, path, depth, title, description, og_title, og_desc, alternates,
         h1, sub, header_links, body, extra_css="", css_patch=None):
    c = L[lang]
    up = "../" * depth
    css = style_block(lang)
    if css_patch:
        css = css_patch(css)
    css = css.replace("</style>", extra_css + "</style>")
    other_path = alternates[c["other_lang"]]
    alt_links = "\n".join(
        f'<link rel="alternate" hreflang="{k}" href="https://booksafe.app/{v}">' for k, v in
        [("en", alternates["en"]), ("de", alternates["de"]), ("x-default", alternates["de"])])
    rel_other = up + other_path
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2C4B6B">
<title>{title}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<meta property="og:title" content="{html.escape(og_title, quote=True)}">
<meta property="og:description" content="{html.escape(og_desc, quote=True)}">
<meta property="og:image" content="https://booksafe.app/assets/{c['og']}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{c['og_alt']}">
<meta property="og:url" content="https://booksafe.app/{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{c['locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{up}assets/app-icon.png">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="canonical" href="https://booksafe.app/{path}">
{alt_links}
<link rel="stylesheet" href="{up}assets/tokens.css">
<link rel="stylesheet" href="{up}assets/fonts.css">
{css}
</head>
<body>

<header>
  <a class="lang-switch" href="{rel_other}" hreflang="{c['other_lang']}" lang="{c['other_lang']}">{c['other_name']}</a>
  <picture><source srcset="{up}assets/app-icon.webp" type="image/webp"><img class="icon" src="{up}assets/app-icon.png" alt="{'BookSafe App-Icon' if lang == 'de' else 'BookSafe app icon'}" width="72" height="72"></picture>
  <h1>{h1}</h1>
  <p class="sub">{sub}</p>
{header_links}
</header>

<main>
{body}
</main>

<footer>
  <nav>
    <a href="{'../' * (depth - (1 if lang == 'en' else 0))}">{c['home']}</a>
    <a href="{'../' * (depth - (1 if lang == 'en' else 0))}support/">{c['support']}</a>
    <a href="{'../' * (depth - (1 if lang == 'en' else 0))}{c['contact_href']}">{c['contact']}</a>
    <a href="{rel_other}" hreflang="{c['other_lang']}" lang="{c['other_lang']}">{c['other_name']}</a>
  </nav>
  <p>BookSafe · Sisofa · <a href="mailto:kontakt@sisofa.de">kontakt@sisofa.de</a></p>
  <p>{c['copyright']}</p>
</footer>

</body>
</html>
"""


def good_to_know(lang, depth):
    """Die Karte „Gut zu wissen“ wörtlich aus der 1.7-Seite."""
    t = TEMPLATE[lang]
    key = "<h2>Gut zu wissen</h2>" if lang == "de" else "<h2>Good to know</h2>"
    i = t.rindex('<section class="card">', 0, t.index(key))
    j = t.index("</section>", i) + len("</section>")
    return "  " + t[i:j].strip()


# ---------------------------------------------------------------- Neu in 1.8
def film_figure(lang, up):
    names = {"de": [("gilded", "Glanz", "goldene Ziffern auf blau-violettem Verlauf"),
                    ("clothbound", "Einband", "Karteikarte „Lesekatalog“ mit Stempel auf grünem Leinen"),
                    ("almanac", "Almanach", "Titelseite der Zeitung „The BookSafe Almanac“"),
                    ("passport", "Lesepass", "Titelseite „Ein Jahr in Büchern“ mit Ticket „42 Bücher“ und Stempel")],
             "en": [("gilded", "Gilded", "golden numbers on a blue-violet gradient"),
                    ("clothbound", "Clothbound", "“Reading catalogue” index card with a stamp on green cloth"),
                    ("almanac", "Almanac", "front page of “The BookSafe Almanac”"),
                    ("passport", "Passport", "title page “A Year in Books” with a “42 books” ticket and a stamp")]}[lang]
    pre = "Filmdesign" if lang == "de" else "film design"
    figs = []
    for key, name, alt in names:
        a = f"{pre} {name}: {alt}" if lang == "de" else f"{name} {pre}: {alt}"
        figs.append(f"""      <figure>
        <picture><source srcset="{up}assets/{lang}-film-{key}.webp" type="image/webp"><img src="{up}assets/{lang}-film-{key}.jpg" alt="{html.escape(a, quote=True)}" loading="lazy" width="720" height="1561"></picture>
        <figcaption>{name}</figcaption>
      </figure>""")
    return '    <div class="film-figure">\n' + "\n".join(figs) + "\n    </div>"


def four_films(css):
    css = css.replace("/* Filmdesigns (1.7): drei gerenderte Filmszenen nebeneinander, gleiche Groesse (720 x 1561). */",
                      "/* Filmdesigns (1.8): vier gerenderte Filmszenen nebeneinander, gleiche Groesse (720 x 1561). */")
    i = css.index(".film-figure {")
    j = css.index("}", i)
    blk = css[i:j].replace("repeat(3, minmax(0, 1fr))", "repeat(4, minmax(0, 1fr))").replace("max-width: 560px", "max-width: 720px")
    return css[:i] + blk + css[j:]


def build_18(lang):
    up = "../" if lang == "de" else "../../"
    if lang == "de":
        body = f"""
  <section class="card lead">
    <h2>Worum es in diesem Update geht</h2>
    <p>BookSafe 1.8 ist das Update für alle, die Comics und Reihen sammeln: Comics wie Asterix werden richtig erkannt, Cover, Band und „Bände gesamt“ trägst du schon beim Anlegen ein, und der Jahresrückblick bekommt sein viertes Filmdesign — den „Lesepass“.</p>
    <p>Diese Seite beschreibt die Änderungen ausführlicher, als es in die Versionshinweise im App Store passt.</p>
    <p class="updated">Version 1.8 · veröffentlicht am 17. Oktober 2026</p>
  </section>

  <section class="card">
    <h2>Neu</h2>

    <h3><span class="num">1</span>Ein viertes Filmdesign: der Lesepass</h3>
    <p>Neben „Glanz“, „Einband“ und „Almanach“ gibt es im Jahresrückblick jetzt den <strong>Lesepass</strong>. Er erzählt dein Lesejahr als Comic-Ausweis: zehn Seiten zum Umblättern, mit Stempeln, Ticket und eigenem Song. Der Film dauert 80 Sekunden. Du wählst ihn wie die anderen Designs über den Paletten-Knopf.</p>
{film_figure(lang, up)}

    <h3><span class="num">2</span>Den Jahresrückblick als Bild oder als Video teilen</h3>
    <p>Der Teilen-Knopf im Jahresrückblick fragt jetzt, was du teilen möchtest: <strong>„Bild teilen“</strong> für die Übersicht deines Jahres oder <strong>„Video teilen“</strong> für den Film im gewählten Design. Das Video lässt sich teilen, ohne den Film vorher anzusehen.</p>

    <h3><span class="num">3</span>Das Cover schon beim Anlegen</h3>
    <p>In „Buch hinzufügen“ wählst du das Cover gleich mit — aus der Fotobibliothek oder direkt abfotografiert. Beim Abfotografieren schneidet BookSafe das Cover automatisch zu. Im Buchdetail geht beides unter „Cover ändern“.</p>

    <h3><span class="num">4</span>Band und „Bände gesamt“ von Hand</h3>
    <p>Beim Anlegen trägst du unter „Reihe“ jetzt auch den Band und die Zahl der Bände ein. „Bände gesamt“ lässt sich außerdem im Reihen-Blatt des Buchdetails ändern. Was du selbst einträgst, überschreibt die Automatik nicht.</p>

    <h3><span class="num">5</span>Kontakt &amp; Feedback in den Einstellungen</h3>
    <p>In den Einstellungen gibt es jetzt <strong>„Kontakt &amp; Feedback“</strong>. Es öffnet eine Mail an uns, in der App-Version und Gerät schon stehen. Daten aus deiner Bibliothek gehen nicht mit.</p>
  </section>

  <section class="card">
    <h2>Verbessert</h2>
    <ul>
      <li>Comics werden richtig erkannt: der Albumtitel statt eines Reihennamens mit Nummer — etwa „Asterix und Kleopatra“ statt „Asterix 02“ —, die richtige Reihe statt eines Verlagstitels und das Genre „Comic“ statt „Roman“</li>
      <li>eine ISBN, die zu einer Sammelbox gehört, wird als Box angelegt statt als Band 1</li>
      <li>„Daten bereinigen“ in den Einstellungen korrigiert die Reihe bereits gespeicherter Bücher</li>
      <li>sauberere Reihennamen und Untertitel: ohne Katalog-Klammern und Bindestrich-Ketten, ohne Werbetext im Untertitel</li>
      <li>Spin-offs landen in ihrer eigenen Reihe</li>
    </ul>
    <p class="note">Dazu viele weitere Detailverbesserungen.</p>
  </section>

  <section class="card">
    <h2>Ältere Versionen</h2>
    <p>Was BookSafe seit Version 0.4 dazugelernt hat — vom Ausleih-Tracker über iCloud-Sync und die Apple Watch bis zu den Filmen im Jahresrückblick —, steht gesammelt im Archiv. Zusammen zeigen die Versionen, was die App heute alles kann.</p>
    <a class="archive-link" href="../versionen/">Zum Archiv der älteren Versionen →</a>
  </section>

{good_to_know(lang, 1)}
"""
        return page(lang, path="neu-in-1-8/", depth=1,
                    title="BookSafe — Neu in Version 1.8",
                    description="Was BookSafe 1.8 neu bringt: das vierte Filmdesign „Lesepass“ für den Jahresrückblick, Teilen als Bild oder Video, Cover und Band schon beim Anlegen, Kontakt & Feedback in den Einstellungen und Comics wie Asterix richtig erkannt.",
                    og_title="BookSafe — Neu in Version 1.8",
                    og_desc="Das Update für Comic- und Reihensammler: Comics richtig erkannt, Cover und Band schon beim Anlegen, dazu der Lesepass als viertes Filmdesign — im Detail.",
                    alternates={"de": "neu-in-1-8/", "en": "en/whats-new-1-8/"},
                    h1="Neu in Version 1.8", sub="Im App Store seit 17. Oktober 2026",
                    header_links='  <a class="home" href="../">← Zur Startseite</a>',
                    body=body, css_patch=four_films)
    body = f"""
  <section class="card lead">
    <h2>What this update is about</h2>
    <p>BookSafe 1.8 is the update for everyone who collects comics and series: comics like Asterix are recognised correctly, you enter the cover, the volume and “Total volumes” right when adding a book, and Year in Review gets its fourth film design — the “Passport”.</p>
    <p>This page describes the changes in more detail than fits into the App Store release notes.</p>
    <p class="updated">Version 1.8 · released 17 October 2026</p>
  </section>

  <section class="card">
    <h2>New</h2>

    <h3><span class="num">1</span>A fourth film design: the Passport</h3>
    <p>Alongside “Gilded”, “Clothbound” and “Almanac”, Year in Review now offers the <strong>Passport</strong>. It tells your reading year as a comic-style ID: ten pages to flip through, with stamps, a ticket and its own song. The film runs 80 seconds. Pick it like the other designs with the palette button.</p>
{film_figure(lang, up)}

    <h3><span class="num">2</span>Share Year in Review as an image or as a video</h3>
    <p>The share button in Year in Review now asks what you want to share: <strong>“Share image”</strong> for the overview of your year, or <strong>“Share video”</strong> for the film in the design you picked. You can share the video without watching the film first.</p>

    <h3><span class="num">3</span>The cover right when adding a book</h3>
    <p>In “Add Book” you pick the cover straight away — from your photo library or photographed on the spot. When you take a photo, BookSafe crops the cover automatically. In the book details, both work under “Change cover”.</p>

    <h3><span class="num">4</span>Volume and “Total volumes” by hand</h3>
    <p>When adding a book you can now enter the volume and the number of volumes under “Series”. “Total volumes” can also be changed in the series sheet of the book details. Automatic updates never overwrite what you entered yourself.</p>

    <h3><span class="num">5</span>Contact &amp; Feedback in Settings</h3>
    <p>Settings now have <strong>“Contact &amp; Feedback”</strong>. It opens an email to us with the app version and device already filled in. No data from your library is included.</p>
  </section>

  <section class="card">
    <h2>Improved</h2>
    <ul>
      <li>comics are recognised correctly: the album title instead of a series name with a number such as “Asterix 02”, the right series instead of a publisher’s title, and the genre “Comic” instead of “Novel”</li>
      <li>an ISBN that belongs to a box set is added as the box instead of as volume 1</li>
      <li>“Clean Up Data” in Settings fixes the series of books you have already saved</li>
      <li>cleaner series names and subtitles: no catalogue brackets or hyphen chains, no marketing copy in the subtitle</li>
      <li>spin-offs land in their own series</li>
    </ul>
    <p class="note">Plus many further refinements.</p>
  </section>

  <section class="card">
    <h2>Earlier versions</h2>
    <p>Everything BookSafe has learned since version 0.4 — from the loan tracker to iCloud sync and the Apple Watch to the Year in Review films — is collected in the archive. Together, the versions show everything the app can do today.</p>
    <a class="archive-link" href="../versions/">Go to the archive of earlier versions →</a>
  </section>

{good_to_know(lang, 2)}
"""
    return page(lang, path="en/whats-new-1-8/", depth=2,
                title="BookSafe — What’s new in version 1.8",
                description="What BookSafe 1.8 adds: the fourth Year in Review film design “Passport”, sharing as an image or video, cover and volume right when adding a book, Contact & Feedback in Settings, and comics like Asterix recognised correctly.",
                og_title="BookSafe — What’s new in version 1.8",
                og_desc="The update for comic and series collectors: comics recognised correctly, cover and volume right when adding a book, plus the Passport as a fourth film design — in detail.",
                alternates={"de": "neu-in-1-8/", "en": "en/whats-new-1-8/"},
                h1="What’s new in version 1.8", sub="On the App Store since 17 October 2026",
                header_links='  <a class="home" href="../">← Back to the home page</a>',
                body=body, css_patch=four_films)


# ---------------------------------------------------------------- Neu in 1.9
def build_19(lang):
    if lang == "de":
        body = f"""
  <section class="card lead">
    <h2>Worum es in diesem Update geht</h2>
    <p>BookSafe 1.9 nimmt dir Handgriffe ab: Jede gebündelte Reihe bekommt auf Wunsch ihr eigenes Bild, Bücher legst du gleich mit allen Angaben an, und Lesesitzungen trägst du auch ohne Dauer nach. Außerdem sagt BookSafe jetzt Bescheid, wenn der Katalog der Deutschen Nationalbibliothek gestört ist.</p>
    <p>Diese Seite beschreibt die Änderungen ausführlicher, als es in die Versionshinweise im App Store passt.</p>
    <p class="updated">Version 1.9 · veröffentlicht am 28. Oktober 2026</p>
  </section>

  <section class="card">
    <h2>Neu</h2>

    <h3><span class="num">1</span>Ein eigenes Bild für jede Reihe</h3>
    <p>Mit „Reihen bündeln“ steht jede Reihe als eine Kachel in der Bibliothek. Statt des Farbverlaufs kann diese Kachel jetzt ein eigenes <strong>Reihenbild</strong> zeigen: Halte die Reihen-Kachel gedrückt oder öffne das Menü in der Reihe und wähle ein Foto aus deiner Fotobibliothek, fotografiere ein Bild oder nimm das Cover eines Bandes. Der Reihenname steht weiter gut lesbar darüber. Das Reihenbild gilt auf dem jeweiligen Gerät und reist im Bibliotheks-Backup mit.</p>

    <h3><span class="num">2</span>Bücher gleich mit allen Angaben anlegen</h3>
    <p>In „Buch hinzufügen“ klappst du jetzt <strong>„Weitere Angaben“</strong> auf und trägst Verlag, Erscheinungsdatum, Erstveröffentlichung, Originaltitel, Übersetzung, Sprachen und Beschreibung gleich beim Anlegen ein. Du musst das Buch danach nicht mehr heraussuchen, um den Rest zu ergänzen. Was du selbst einträgst, überschreibt die Automatik nicht.</p>

    <h3><span class="num">3</span>Lesesitzungen auch ohne Dauer nachtragen</h3>
    <p>Beim Nachtragen einer Lesesitzung reichen jetzt die gelesenen Seiten — eine Dauer musst du nicht mehr angeben. Die Seiten stellst du per Schiebebalken ein oder tippst „Seiten gelesen“ direkt ein. Die Dauer geht per Schiebebalken, als Zahl oder per Schnellwahl. Dein Lesetempo rechnet BookSafe nur aus Sitzungen mit Seiten und Dauer.</p>
  </section>

  <section class="card">
    <h2>Verbessert</h2>
    <ul>
      <li>Ist der Katalog der Deutschen Nationalbibliothek gestört, sagt BookSafe das: Titel- und Autorensuche zeigen einen Hinweis statt „Keine Treffer“ — auch dann, wenn nur englische Ausgaben gefunden wurden und deutsche fehlen können</li>
      <li>deutsche Ausgaben britischer Verlage werden per ISBN gefunden</li>
      <li>Reihenangaben aus dem Katalog wie „Robert Langdon ; 1“ werden als Reihe mit Band erkannt</li>
      <li>Gesamtausgaben werden auch erkannt, wenn die Reihe in deiner Bibliothek anders geschrieben ist</li>
      <li>Jahresrückblick und Filme zeigen große Zahlen mit Tausenderpunkt, etwa „23.382“ Seiten</li>
      <li>„Bibliothek PDF“ ist auf Englisch durchgehend englisch — Titel, Seitenzahlen und Dateiname</li>
    </ul>
    <p class="note">Dazu viele weitere Detailverbesserungen.</p>
  </section>

  <section class="card">
    <h2>Ältere Versionen</h2>
    <p>Was BookSafe seit Version 0.4 dazugelernt hat — vom Ausleih-Tracker über iCloud-Sync und die Apple Watch bis zu den Filmen im Jahresrückblick —, steht gesammelt im Archiv. Zusammen zeigen die Versionen, was die App heute alles kann.</p>
    <a class="archive-link" href="../versionen/">Zum Archiv der älteren Versionen →</a>
  </section>

{good_to_know(lang, 1)}
"""
        return page(lang, path="neu-in-1-9/", depth=1,
                    title="BookSafe — Neu in Version 1.9",
                    description="Was BookSafe 1.9 neu bringt: ein eigenes Bild für jede Reihe, Bücher gleich mit allen Angaben anlegen, Lesesitzungen ohne Dauer nachtragen und ein Hinweis, wenn der Katalog der Deutschen Nationalbibliothek gestört ist.",
                    og_title="BookSafe — Neu in Version 1.9",
                    og_desc="Ein eigenes Bild für jede Reihe, Bücher gleich mit allen Angaben anlegen und Lesesitzungen auch ohne Dauer nachtragen — im Detail.",
                    alternates={"de": "neu-in-1-9/", "en": "en/whats-new-1-9/"},
                    h1="Neu in Version 1.9", sub="Im App Store seit 28. Oktober 2026",
                    header_links='  <a class="home" href="../">← Zur Startseite</a>',
                    body=body)
    body = f"""
  <section class="card lead">
    <h2>What this update is about</h2>
    <p>BookSafe 1.9 saves you a few steps: every grouped series can have its own image, you add books with all their details right away, and you can log reading sessions even without a duration. BookSafe also tells you when the German National Library catalogue is disrupted.</p>
    <p>This page describes the changes in more detail than fits into the App Store release notes.</p>
    <p class="updated">Version 1.9 · released 28 October 2026</p>
  </section>

  <section class="card">
    <h2>New</h2>

    <h3><span class="num">1</span>Your own image for every series</h3>
    <p>With “Group Series”, each series appears as a single tile in your library. Instead of the colour gradient, that tile can now show its own <strong>series image</strong>: long-press the series tile or open the menu in the series, then pick a photo from your library, take a picture or use the cover of one of its volumes. The series name stays readable on top. The series image applies to that device and travels with your library backup.</p>

    <h3><span class="num">2</span>Add books with all their details right away</h3>
    <p>In “Add Book” you can now expand <strong>“More Details”</strong> and enter publisher, release date, first published, original title, translation, languages and description while adding the book. No need to look the book up again afterwards to fill in the rest. Automatic updates never overwrite what you entered yourself.</p>

    <h3><span class="num">3</span>Log reading sessions even without a duration</h3>
    <p>When you log a reading session after the fact, the pages you read are now enough — a duration is no longer required. Set the pages with a slider or type in “Pages read” directly. The duration works with a slider, as a number or with a quick pick. BookSafe calculates your reading pace only from sessions that have both pages and a duration.</p>
  </section>

  <section class="card">
    <h2>Improved</h2>
    <ul>
      <li>when the German National Library catalogue is disrupted, BookSafe says so: title and author search show a notice instead of “No results” — even when only English editions were found and German ones may be missing</li>
      <li>German editions from British publishers are found by ISBN</li>
      <li>series details from the catalogue such as “Robert Langdon ; 1” are recognised as a series with its volume</li>
      <li>complete editions are detected even when the series is spelled differently in your library</li>
      <li>Year in Review and its films show large numbers with thousands separators, such as “23,382” pages</li>
      <li>“Library PDF” is fully in English when your device is set to English — title, page numbers and file name</li>
    </ul>
    <p class="note">Plus many further refinements.</p>
  </section>

  <section class="card">
    <h2>Earlier versions</h2>
    <p>Everything BookSafe has learned since version 0.4 — from the loan tracker to iCloud sync and the Apple Watch to the Year in Review films — is collected in the archive. Together, the versions show everything the app can do today.</p>
    <a class="archive-link" href="../versions/">Go to the archive of earlier versions →</a>
  </section>

{good_to_know(lang, 2)}
"""
    return page(lang, path="en/whats-new-1-9/", depth=2,
                title="BookSafe — What’s new in version 1.9",
                description="What BookSafe 1.9 adds: your own image for every series, adding books with all their details right away, logging reading sessions without a duration, and a notice when the German National Library catalogue is disrupted.",
                og_title="BookSafe — What’s new in version 1.9",
                og_desc="Your own image for every series, add books with all their details right away and log reading sessions even without a duration — in detail.",
                alternates={"de": "neu-in-1-9/", "en": "en/whats-new-1-9/"},
                h1="What’s new in version 1.9", sub="On the App Store since 28 October 2026",
                header_links='  <a class="home" href="../">← Back to the home page</a>',
                body=body)


# ---------------------------------------------------------------- Archiv
def detail_content(lang, v):
    """Lead-Absatz + alle Inhaltskarten außer Lead und „Gut zu wissen“, eine Ebene tiefer."""
    rel = L[lang]["detail"](v)
    src = ROOT / ("" if lang == "de" else "en") / rel / "index.html"
    t = src.read_text()
    main = t[t.index("<main>") + 6:t.index("</main>")]
    cards = re.findall(r'<section class="card( lead)?">(.*?)</section>', main, re.S)
    lead_p, parts = "", []
    stop = "<h2>Gut zu wissen</h2>" if lang == "de" else "<h2>Good to know</h2>"
    for is_lead, inner in cards:
        if is_lead:
            lead_p = re.search(r"<p>(.*?)</p>", inner, re.S).group(1)
            continue
        if stop in inner or 'class="archive-link"' in inner:
            continue
        if inner.count("<figure>") == 4:
            inner = inner.replace('<div class="film-figure">', '<div class="film-figure four">')
        inner = re.sub(r"<(/?)h3>", r"<\1h4>", inner)
        inner = re.sub(r"<(/?)h2>", r"<\1h3>", inner)
        inner = re.sub(r" (Was Version|What version) [0-9.]+ (gebracht hat|brought)[^<]*<a [^>]*>[^<]*</a>\.", "", inner)
        parts.append(inner.strip("\n"))
    sub = re.search(r'<p class="sub">(.*?)</p>', t).group(1)
    return lead_p, sub, "\n".join(parts)


PREFIX = {"neu": ("NEU", "NEW"), "verbessert": ("Verbessert", "Improved", "iPad"), "behoben": ("Behoben", "Fixed")}
GROUP_TITLE = {"de": {"neu": "Neu", "verbessert": "Verbessert", "behoben": "Behoben"},
               "en": {"neu": "New", "verbessert": "Improved", "behoben": "Fixed"}}


def clean_tests(line):
    # Dauerregel (AppStoreConnect.md §2): keine Testanzahlen in Marketing-Texten.
    line = re.sub(r" und (über|mehr als) \d+ neue automatische Tests( für Stabilität im Alltag)?", r" und mehr Stabilität im Alltag", line)
    line = re.sub(r" and (more than|over) \d+ new automated tests( for everyday stability)?", r" and more everyday stability", line)
    return line


def notes_content(lang, v):
    loc = "de-DE" if lang == "de" else "en-US"
    groups = {"neu": [], "verbessert": [], "behoben": []}
    tail = []
    for raw in NOTES[v]["notes"][loc].splitlines():
        line = raw.strip().lstrip("•").strip()
        if not line:
            continue
        line = clean_tests(line)
        m = re.match(r"([A-Za-zäöü]+):\s*(.*)", line)
        key = None
        if m:
            for k, prefixes in PREFIX.items():
                if m.group(1) in prefixes:
                    key = k
        if key:
            text = m.group(2) if m.group(1) != "iPad" else line
            groups[key].append(text[0].upper() + text[1:])
        elif re.match(r"(Viele|Many)\b", line):
            tail.append(line)
        else:
            groups["neu"].append(line)
    out = []
    for k in ("neu", "verbessert", "behoben"):
        if groups[k]:
            items = "\n".join(f"      <li>{html.escape(x, quote=False)}</li>" for x in groups[k])
            out.append(f"    <h3>{GROUP_TITLE[lang][k]}</h3>\n    <ul>\n{items}\n    </ul>")
    for x in tail:
        out.append(f'    <p class="note">{html.escape(x, quote=False)}</p>')
    return "\n".join(out)


def build_archive(lang):
    de = lang == "de"
    up = "../" if de else "../../"
    versions = DETAIL_PAGES + NOTE_ONLY
    nav = "\n".join(f'      <a href="#v{v.replace(".", "-")}">{v}</a>' for v in versions)
    cards = []
    for v in versions:
        vid = "v" + v.replace(".", "-")
        if v in DETAIL_PAGES:
            lead_p, sub, content = detail_content(lang, v)
            more = (f'    <p class="more"><a href="../{L[lang]["detail"](v)}">Ausführliche Seite zu Version {v} →</a></p>' if de
                    else f'    <p class="more"><a href="../{L[lang]["detail"](v)}">Full page for version {v} →</a></p>')
            cards.append(f"""  <section class="card version" id="{vid}">
    <h2>Version {v}</h2>
    <p class="updated">{sub}</p>
    <p>{lead_p}</p>
{content}
{more}
  </section>""")
        else:
            sub = (f"Im App Store seit {date(v, lang)}" if de else f"On the App Store since {date(v, lang)}")
            extra = ""
            if v == "0.4":
                extra = ('\n    <p>Die erste Version im deutschen und englischen App Store, mit den Inhalten von 0.3.</p>' if de
                         else '\n    <p>The first version on the German and English App Store, including what 0.3 brought.</p>')
            cards.append(f"""  <section class="card version" id="{vid}">
    <h2>Version {v}</h2>
    <p class="updated">{sub}</p>{extra}
{notes_content(lang, v)}
  </section>""")
    if de:
        lead = f"""  <section class="card lead">
    <h2>Was BookSafe alles kann</h2>
    <p>Hier stehen die Neuerungen aller früheren Versionen, von der neuesten zur ältesten. Zusammen zeigen sie, was in BookSafe steckt — vom Scannen und den Reihen über Ausleihen, Wunschliste und Statistik bis zu iCloud-Sync, Apple Watch und den Filmen im Jahresrückblick.</p>
    <p>Jede Beschreibung gibt den Stand ihrer Version wieder; manches wurde seither weiter ausgebaut. Was die aktuelle Version bringt, steht auf der <a href="../neu-in-1-9/">Seite zu Version 1.9</a>.</p>
    <nav class="version-nav" aria-label="Versionen">
{nav}
    </nav>
  </section>"""
    else:
        lead = f"""  <section class="card lead">
    <h2>Everything BookSafe can do</h2>
    <p>Here are the new features of every earlier version, newest first. Together they show what BookSafe has to offer — from scanning and series to loans, wishlist and statistics, all the way to iCloud sync, Apple Watch and the Year in Review films.</p>
    <p>Each description reflects the state of its version; some things have been developed further since. What the current version brings is on the <a href="../whats-new-1-9/">version 1.9 page</a>.</p>
    <nav class="version-nav" aria-label="Versions">
{nav}
    </nav>
  </section>"""
    store = (f"""  <section class="card">
    <div class="store">
      <a href="{L[lang]['store']}"><img src="{up}assets/{L[lang]['badge']}" alt="{L[lang]['badge_alt']}" width="144" height="48"></a>
      <a href="../">{L[lang]['back2']}</a>
    </div>
  </section>""")
    body = "\n" + lead + "\n\n" + "\n\n".join(cards) + "\n\n" + store + "\n"
    if de:
        return page(lang, path="versionen/", depth=1, title="BookSafe — Ältere Versionen",
                    description="Archiv aller früheren BookSafe-Versionen von 0.4 bis 1.8: was jede Version neu gebracht hat — und damit alles, was die App kann.",
                    og_title="BookSafe — Ältere Versionen",
                    og_desc="Alle früheren Versionen im Überblick: Neuerungen, Verbesserungen und Fehlerbehebungen von 0.4 bis 1.8.",
                    alternates={"de": "versionen/", "en": "en/versions/"},
                    h1="Ältere Versionen", sub="Alles, was BookSafe von Version 0.4 bis 1.8 dazugelernt hat",
                    header_links='  <a class="home" href="../neu-in-1-9/">← Neu in Version 1.9</a>',
                    body=body, extra_css=EXTRA_CSS)
    return page(lang, path="en/versions/", depth=2, title="BookSafe — Earlier versions",
                description="Archive of every earlier BookSafe version from 0.4 to 1.8: what each version added — and with it, everything the app can do.",
                og_title="BookSafe — Earlier versions",
                og_desc="All earlier versions at a glance: new features, improvements and fixes from 0.4 to 1.8.",
                alternates={"de": "versionen/", "en": "en/versions/"},
                h1="Earlier versions", sub="Everything BookSafe learned from version 0.4 to 1.8",
                header_links='  <a class="home" href="../whats-new-1-9/">← What’s new in version 1.9</a>',
                body=body, extra_css=EXTRA_CSS)


OUT = {
    "neu-in-1-9/index.html": build_19("de"),
    "en/whats-new-1-9/index.html": build_19("en"),
    "neu-in-1-8/index.html": build_18("de"),
    "en/whats-new-1-8/index.html": build_18("en"),
    "versionen/index.html": build_archive("de"),
    "en/versions/index.html": build_archive("en"),
}
for rel, text in OUT.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    print(rel, len(text))
