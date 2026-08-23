# Presse-Onepager (A4)

Einseitige Presse-Information zu BookSafe 1.1, deutsch und englisch, verdichtet
aus `presse/index.html` bzw. `en/press/index.html`.

| Datei | Zweck |
|---|---|
| `BookSafe-Presse-Onepager.pdf` / `.png` | deutsche Fassung |
| `BookSafe-Press-Onepager.pdf` / `.png` | englische Fassung |
| `onepager.tmpl.html` / `onepager-en.tmpl.html` | Quellen, mit Platzhaltern für die Schriften |
| `build.py` | ersetzt die Platzhalter durch base64 → `onepager.html`, `onepager-en.html` |
| `render.mjs` | rendert beide Fassungen als PDF und PNG |

Die vier Ausgabedateien liegen zusätzlich in `assets/` — von dort verlinken die
beiden Presse-Seiten sie zum Download. Nach jeder Änderung also mitkopieren:

    python3 build.py && node render.mjs
    cp BookSafe-*-Onepager.pdf BookSafe-*-Onepager.png ../../assets/

`render.mjs` prüft dabei, ob der Inhalt noch aufs Blatt passt, ob das PDF
einseitig bleibt und ob beide Schriften geladen sind — es endet mit
Exit-Code 1, wenn eine Fassung durchfällt. Das Blatt schneidet sonst
stillschweigend ab. Reserve über dem Fuß: rund 70 px (DE) bzw. 50 px (EN).

## Schriften

Beide Schriften stecken als base64 im HTML, damit PDF und PNG überall gleich
aussehen und die Datei ohne Netz funktioniert.

- **Saira** (Schnitt 800) für Auszeichnungen — dieselbe Datei wie auf der Website
- **Source Sans 3** für den Fließtext — Ersatz für die Systemschrift der Website:
  Apples SF Pro darf nicht in ein PDF eingebettet werden

Beide unter SIL Open Font License 1.1 (`../../assets/fonts/OFL.txt` bzw.
`SOURCE-SANS-OFL.txt`).

## Abweichungen zur Presse-Seite

Der One-Pager ist eine Verdichtung, keine Kopie:

- Er führt **fünf** Kernfunktionen, die Presse-Seite **sechs**. Auf dem Blatt
  entfällt „Deine Bibliothek gehört dir“, weil das dort der Claim in der
  Kopfzeile ist und die Datenschutz-Spalte direkt daneben steht.
- Reihenfolge auf dem Blatt: Erfassen, Lesejahr, Wunschliste, Apple Watch,
  Reihen. Die Presse-Seite behält ihre gewachsene Reihenfolge.
- Der Pressekontakt nennt nur „Sisofa“, keinen Klarnamen. In
  `support/index.html` steht der Name weiterhin — dort ist er als
  Verantwortlicher für die Datenverarbeitung rechtlich nötig.
