# Sharing-Karte (Open Graph)

Das Vorschaubild, das Mastodon, WhatsApp, Slack & Co. zeigen, wenn jemand
booksafe.app verlinkt. Vorher zeigte `og:image` auf `de-today.jpg` — einen
720 × 1564 großen Hochkant-Screenshot, den Link-Vorschauen beschneiden.

| Datei | Zweck |
|---|---|
| `og-de.jpg` / `og-en.jpg` | die Karten, 1200 × 630, je rund 64 KB |
| `card.tmpl.html` | Quelle mit Platzhaltern |
| `build.py` | setzt Schriften, Icon und Screenshots ein → `card-de.html`, `card-en.html` |
| `render.mjs` | rendert beide Karten als JPEG und prüft die Maße |
| `shrink.mjs` | verkleinert die Screenshots aus `assets/` auf 440 px Breite |

## Neu erzeugen

    node shrink.mjs        # nur nötig, wenn die Screenshots in assets/ neu sind
    python3 build.py && node render.mjs
    cp og-de.jpg og-en.jpg ../../assets/

`render.mjs` prüft, dass die Karte exakt 1200 × 630 misst, Saira geladen ist,
die Schlagzeile zweizeilig bleibt und kein Text aus der Karte läuft — es endet
mit Exit-Code 1, wenn etwas davon nicht stimmt.

**Die Maße dürfen nicht auseinanderlaufen:** `index.html` und `en/index.html`
deklarieren `og:image:width` und `og:image:height` als 1200 × 630. Wird hier mit
einem anderen `deviceScaleFactor` gerendert, rechnen Scraper mit falschen Werten.

## Sprachen

Jede Karte trägt die Screenshots ihrer Sprache — die englische zeigt
`en-today` und `en-watch`, nicht die deutschen Screens. Beim Ändern von
`build.py` darauf achten.
