# Bild-Pipeline

Erzeugt die WebP-Fassungen der Screenshots und das `apple-touch-icon.png`.

    node towebp.mjs

Das Skript liest `assets/{de,en}-*.jpg` und `assets/app-icon.png`, schreibt
`.webp` daneben und legt zusätzlich `assets/apple-touch-icon.png` (180 × 180,
aus `app-icon-1024.png`) an. Es überschreibt vorhandene Dateien.

## Warum die JPEGs bleiben

Die Seiten binden jedes Bild als `<picture>` ein:

    <picture>
      <source srcset="assets/de-today.webp" type="image/webp">
      <img src="assets/de-today.jpg" alt="…" width="720" height="1564">
    </picture>

Browser ohne WebP nehmen das JPEG. Die Presse-Seiten verlinken zum Download
weiterhin die **JPEGs** — Redaktionen wollen kein WebP.

**`picture { display: contents; }` steht in jeder Seite und muss dort bleiben.**
Ohne die Regel bildet das `<picture>` eine eigene Inline-Box; im Hero sind die
Screenshots absolut positioniert und würden sich dann am `<picture>` statt am
`.hero-shots`-Container ausrichten.

## Qualität

`toDataURL('image/webp', 0.82)`. Bei 0.82 steht der kleinste Text in den
Listenzeilen (11 px im Original) auch bei 2,6-facher Vergrößerung noch sauber;
darunter franst er aus. Ergebnis über alle 15 Bilder: 1722 KB → 582 KB.

Auf der Startseite bedeutet das 919 KB → 309 KB an Bildern.

## Nach neuen Screenshots

1. neue `.jpg` nach `assets/` legen
2. `node towebp.mjs`
3. prüfen, dass für jedes `<img>` eine `.webp` daneben liegt — fehlt eine,
   lädt der Browser still das JPEG und niemand merkt es
