# Plan: Ratgeber ausbauen, inklusive englischer Fassung

Dieses Dokument ist eine Planung. Es liegt unter `design/` und geht nicht live. Es ändert keine Seite, keinen Preis und keinen Store-Link.

Stand der Website, an dem der Plan hängt: BookSafe 1.12, deutsch und englisch, iPhone, iPad, Apple Watch und Android. Der Ratgeber selbst ist nur deutsch und beschreibt den Stand vom 19. Oktober 2026. Die Belege in `design/ratgeber/articles.py` nennen noch die App 1.8.

## Was heute online ist

Fünf Artikel plus eine Übersicht, erzeugt von `design/ratgeber/build.py` aus `articles.py`. Jede Seite ist eine eigene `index.html`.

Umfang des Artikeltexts (Wörter in der ersten Karte, ohne den Store-Kasten und ohne „Weitere Ratgeber“):

| Artikel | Wörter | Überschriften im Text |
| --- | ---: | --- |
| Neuerscheinungen nicht verpassen | 259 | vier `h3` |
| SuB abbauen | 257 | fünf `h3` |
| Buchreihe, richtige Reihenfolge | 230 | drei `h3` |
| Bücher erfassen | 221 | vier `h3` |
| Bücherei-Leihfristen | 195 | drei `h3` |

Das `h1` steht im Seitenkopf. Im Artikel gibt es kein `h2`. Die beiden `h2` der Seite gehören zum Store-Kasten und zur Linkliste darunter. Es gibt kein Inhaltsverzeichnis.

Was die Artikel schon können: Du-Form, ein konkreter BookSafe-Abschnitt, ein Screenshot, ein ehrlicher Satz zu Android in „Neuerscheinungen“ (keine Widgets) und in „Bücher erfassen“ (kein iCloud, Backup als Datei). Store-Buttons für App Store und Google Play stehen unter jedem Artikel. Fremde App-Namen kommen nicht vor. Das soll so bleiben.

## Schwächen

- Die Texte beantworten die Frage, brechen aber nach dem ersten praktischen Tipp ab. Für eine Suche, die eine Anleitung erwartet, ist das dünn. Ein Ausbau auf etwa 800 bis 1400 Wörter ist der eigentliche Hebel, nicht noch eine Meta-Zeile.
- Android ist nicht durchgehalten. Leihfristen, Reihen und der SuB-Artikel beschreiben Mitteilungen, Widgets oder den Heute-Bildschirm, ohne zu sagen, was davon auf Android fehlt.
- Der Stand ist 1.8. Danach kamen unter anderem ein eigenes Bild je Reihe, der Eindruck mit Stimmungen, weitere Leseupdate-Designs und BookSafe bei Google Play. Die Artikel erwähnen das nicht.
- Es gibt keine englische Fassung und deshalb keine `hreflang`-Paare. Die englische Website verlinkt den Ratgeber nicht, weil es nichts zu verlinken gibt.
- Im Fließtext verweisen die Artikel nicht aufeinander. Nur der Block „Weitere Ratgeber“ und die Store-Buttons tun das.
- Die strukturierten Daten sind `Article` plus Breadcrumb. `dateModified` ist gleich `datePublished`. Eine FAQ lohnt sich erst, wenn der Text echte Frage-Antwort-Blöcke hat, nicht vorher.
- Die Screenshots sind deutsch: Wunschliste, Buchdetail, Heute, Bibliothek. Englische Pendants liegen für Heute, Bibliothek, Buchdetail und Statistik in `assets/`. Eine englische Wunschliste (`en-wishlist`) liegt nicht.
- Die Übersicht ist eine Linkliste. Sie sagt nicht, für wen welcher Text ist.
- „SuB“ ist im Deutschen die richtige Zielgruppen-Sprache. Im Englischen trägt die Abkürzung nicht. Dort gehören „unread pile“ und „TBR“ in den Text, nicht „SuB“.

## Themen

Suchvolumen-Zahlen liegen nicht vor. Die Keywords sind eine redaktionelle Einschätzung der Formulierung, die eine suchende Person tippen würde, plus die Suchintention. Keine erfundenen Volumen.

„Ausbauen“ heißt: den bestehenden Artikel auf den Stand der Website bringen, Android ungeschönt ergänzen, intern verlinken, `dateModified` setzen. Den Slug nicht ändern.

| Prio | Thema | Art | Keyword DE (Einschätzung) | Intention | Keyword EN (Einschätzung) | Intention | Ziel Wörter | Aufwand |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| 1 | Neuerscheinungen nicht verpassen | ausbauen | neuerscheinungen nicht verpassen | informational | don't miss new book releases | informational | 1000–1200 | M |
| 1 | Buchreihe in der richtigen Reihenfolge | ausbauen | buchreihe richtige reihenfolge | informational | book series reading order | informational | 1100–1400 | M |
| 1 | Stapel ungelesener Bücher abbauen | ausbauen | stapel ungelesener bücher abbauen | informational | unread book pile | informational | 1100–1400 | M |
| 1 | Bücher erfassen | ausbauen | bücher per isbn scannen | informational, mit App-Suche | scan isbn to catalog books | informational, mit App-Suche | 1000–1300 | M |
| 2 | Leihfristen der Bücherei | ausbauen | bücherei leihfrist erinnerung | informational | library book due date reminder | informational | 900–1200 | M |
| 2 | Android und iPhone, die Unterschiede | neu | buch app android ohne konto | informational, Vergleich | book app for android no account | informational, Vergleich | 900–1100 | M |
| 2 | Bibliothek organisieren | neu | eigene bibliothek organisieren | informational | organize your home library | informational | 1200–1500 | L |
| 2 | Lesen tracken | neu | lesefortschritt tracken | informational, mit App-Suche | reading session tracker | informational, mit App-Suche | 1000–1200 | M |
| 2 | Leseziel | neu | leseziel setzen | informational | set a reading goal | informational | 800–1000 | S |
| 3 | Umzug ohne Konto | neu | bücherliste importieren csv | informational | import a book list from csv | informational | 800–1000 | M |
| 3 | Lesejahr | neu | lesejahr rückblick | informational | reading year in review | informational | 900–1100 | M |
| 3 | Wunschliste teilen | neu, nur falls nötig | wunschliste bücher teilen | informational | share a book wishlist | informational | 700–900 | S |
| 4 | Buch-App ohne Konto | neu, kurz | buch app ohne konto | informational, mit App-Suche | book tracking app no account | informational, mit App-Suche | 700–900 | S |

Nebenkeywords, ebenfalls Einschätzung, nicht als eigene Artikel: „sub abbauen“ für den SuB-Text, „tbr pile“ für die englische Fassung, „isbn scanner bibliothek“, „erscheinungstermin erinnerung“.

Was in die ausgebauten Artikel gehört, und nur das, was die Website heute beschreibt:

- Neuerscheinungen: Wunschliste, Countdown, Erscheinungskalender, Mitteilung am Erscheinungstag nur bei genauem Datum, Feuerwerk. Widget nur auf iPhone und iPad. Auf Android Countdown und Kalender in der App, keine Widgets.
- Reihen: Reihe und Band aus den Katalogen, sonst von Hand. „Weitere Bände der Reihe“, Bündeln als ein Eintrag, Sonderbände wie „Band 8,5“, seit 1.9 ein eigenes Bild je Reihe.
- SuB: Status „Ungelesen“, Filter, eigene Listen, Lese-Challenge, Status „Abgebrochen“. Die Uhr und die Live-Aktivität gibt es nur zum iPhone. Auf Android steht die laufende Sitzung in der Benachrichtigungsleiste.
- Erfassen: Barcode und gedruckte ISBN, Titelsuche, Standort im Regal, CSV-Import mit Bewertungen, Lesedaten und Notizen, reine ISBN-Liste. Keine Namen anderer Apps. iCloud nur auf iPhone und iPad. Auf Android bleibt die Bibliothek auf dem Gerät, ein Backup vom iPhone kommt als Datei im Tab „Optionen“. Export als CSV oder PDF auf beiden.
- Leihfristen: Besitz „Ausgeliehen“, Rückgabedatum, Hinweis in der Bibliothek, Mitteilung zwei Tage vorher und am Tag, Scan des Ausleihbelegs. Im englischen Text dazu sagen, dass der Beleg-Scan auf gedruckte deutsche Ausleihbelege zielt und kein Ersatz für jedes Bibliothekssystem der Welt ist.

Neue Themen, an die echten Funktionen gekoppelt:

- Android und iPhone. Dieser Artikel ist der ehrliche Überblick, die anderen verlinken ihn, statt die Einschränkung jedes Mal neu zu verstecken. Pflichtsätze, sinngemäß und ohne Beschönigung: keine Widgets, keine Uhr, kein laufender Abgleich mit dem iPhone, die Bibliothek bleibt auf dem Gerät, ein iPhone-Backup lässt sich als Datei übernehmen, BookSafe Pro ist ein eigener Kauf über Google Play und gilt nicht im App Store, umgekehrt genauso. Der Scanner nutzt Google ML Kit und sendet Diagnosedaten an Google. Dafür auf `/supportandroid/` bzw. `/en/supportandroid/` verlinken, die Datenschutzerklärung nicht kopieren. Dazu, was auf beiden gilt: kein Konto, keine Werbung, keine BookSafe-Server, Export als CSV oder PDF, kostenlos bis 50 Bücher.
- Bibliothek organisieren: Standort und Fach, Lesestatus, Sortierung, eigene Listen, eine Liste oder die Wunschliste als Bild oder Text teilen.
- Lesen tracken: Sitzung mit Timer, Sitzung ohne Dauer nachtragen, Statistik. Apple Watch, Sperrbildschirm und Live-Aktivität nur zum iPhone. Android wie oben, Benachrichtigungsleiste, keine Uhr.
- Leseziel: die Lese-Challenge auf dem Heute-Bildschirm. Mit dem SuB-Artikel verlinken, nicht denselben Text zweimal schreiben.
- Umzug ohne Konto: CSV und Backup-Datei. Kein laufender Sync zwischen Android und iPhone. Pro-Kauf nicht plattformübergreifend. Keine fremden Produktnamen.
- Lesejahr: Rückblick mit Kennzahlen, Top 3, Film in den Designs der Website, Teilen als Bild oder Video. Vor dem Schreiben an der App prüfen, was davon auf Android wirklich vorhanden ist. Die Website nennt Widgets und die Uhr als nur zum iPhone, den Film nicht. Nichts dazuerfinden. Was nicht geprüft ist, kommt nicht in den Artikel.
- Wunschliste teilen: erst als Abschnitt im Neuerscheinungen-Artikel. Ein eigener Text nur, wenn dieser Abschnitt über etwa 400 Wörter wächst.
- Buch-App ohne Konto: kurzer Text, der auf die Support-Seiten verweist. Kein zweites Exemplar der Datenschutzerklärung. Den ML-Kit-Hinweis für Android nicht weglassen.

Nicht anfassen und nicht versprechen: Preise, Store-URLs, erfundene Nutzerzahlen, Vergleiche mit namentlich genannten anderen Apps.

## Reihenfolge

1. Die fünf bestehenden deutschen Artikel auf 1.12 bringen, inklusive der Android-Sätze und der Links untereinander. Sie sind schon öffentlich. Ein Ausbau ändert den Slug nicht.
2. Dieselbe fünf Artikel übersetzen, sobald der deutsche Text steht. Vorher zu übersetzen hieße, den Stand von 1.8 zu konservieren.
3. Neue Artikel in dieser Reihenfolge: Android-Unterschiede, Bibliothek organisieren, Lesen tracken, Leseziel, Umzug, Lesejahr, danach Wunschliste teilen nur falls nötig, zuletzt der kurze Text zur App ohne Konto.

Der Android-Artikel kommt vor den anderen neuen Texten, weil die Startseite Android schon zeigt und der Ratgeber das bisher nicht einordnet. Bibliothek, Tracking und Leseziel sind die Funktionen, die auf der Startseite die Kapitel tragen.

## Englische Fassung, technisch

`build.py` bleibt der einzige Ort, der HTML schreibt. Vorschlag:

- Englische Texte in `design/ratgeber/articles_en.py`, gleiches Schema wie `articles.py` (slug, title, description, h1, sub, teaser, body). Dieselben Slugs, damit die Paare stabil sind.
- `build.py` läuft über beide Sprachen. Deutsch bleibt `/ratgeber/` und `/ratgeber/<slug>/`. Englisch wird `/en/guide/` und `/en/guide/<slug>/`. Die übrige englische Site benutzt englische Pfadwörter (`press`, `versions`, `support`), deshalb `guide` und nicht `ratgeber` unter `/en/`.
- In jedem Paar `link rel="alternate"` für `de`, `en` und `x-default`. `x-default` zeigt auf die deutsche URL, wie auf dem Rest der Site. `canonical` zeigt auf die eigene URL.
- Die Sitemap braucht keine feste Liste. `node design/assets-pipeline/sitemap.mjs` nimmt jede `index.html` außerhalb von `design/` und liest die `hreflang`-Paare aus der Seite. Voraussetzung: canonical stimmt, die Seite ist nicht `noindex`.
- Footer: auf den englischen Ratgeber-Seiten ein Link „Guide“ nach `/en/guide/`, auf den deutschen bleibt „Ratgeber“. Die englische Startseite bekommt den Guide-Link erst, wenn `/en/guide/` existiert. Vorher nicht.
- Store-Kasten wie heute, sprachgerecht: deutsch `badge-de.svg` und `google-play-badge-de.png` mit der deutschen App-Store-URL, englisch `badge-en.svg` und `google-play-badge-en.png` mit der englischen App-Store-URL. Die Google-Play-URL bleibt `https://play.google.com/store/apps/details?id=de.sisofa.booksafe`. Preise nicht anfassen: kostenlos bis 50 Bücher, Pro einmalig 3,99 € je Plattform, kein Abo, ein Kauf gilt nur für diese Plattform.
- Interne Links im Fließtext zeigen auf den Geschwisterartikel derselben Sprache. Der Android-Artikel zeigt auf die Android-Supportseite der jeweiligen Sprache.
- Screenshots: `en-today`, `en-library`, `en-detail`, `en-stats` gibt es. `en-wishlist` gibt es nicht. Den deutschen Wunschliste-Screenshot nicht als englische Oberfläche ausgeben. Entweder das Bild nachliefern oder die Figur im englischen Neuerscheinungen-Artikel weglassen.
- JSON-LD: `inLanguage` je Sprache, `dateModified` beim Ausbau neu setzen, `description` weiter dasselbe kurze Feld wie die Meta-Description (etwa 155 Zeichen, Wichtigstes vorn).
- Kein Analyse-Skript ergänzen.

## Aufwand, als Größe der Änderung

S ist ein Artikel aus Funktionen, die schon auf der Website stehen, ohne neue Screenshots. M ist ein bestehender Artikel, der Android, Querverweise und den Stand 1.12 aufnimmt, oder ein neuer Artikel mit einem Screenshot, der schon vorliegt. L ist „Bibliothek organisieren“, weil dort Standort, Listen, Sortierung und Teilen in einen Text müssen, ohne drei andere Artikel zu wiederholen. Die Generator-Erweiterung um Englisch ist einmalig M, die fünf Übersetzungen danach je S.

Kalenderzeiten stehen hier bewusst nicht.

## Offen, bevor jemand schreibt

- Am Gerät prüfen, welche Teile des Jahresrückblicks auf Android vorhanden sind. Bis dahin kein Satz dazu.
- Navigationswort auf Englisch: Vorschlag „Guide“, kurz wie „Press“ und „Versions“.
- Neue Slugs erst festlegen, wenn die Überschrift steht. Bestehende Slugs bleiben.
