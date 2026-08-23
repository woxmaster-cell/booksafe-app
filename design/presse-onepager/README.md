# Presse-Onepager (A4)

Einseitige Presse-Information zu BookSafe 1.1, verdichtet aus `presse/index.html`
und `support/index.html`.

| Datei | Zweck |
|---|---|
| `BookSafe-Presse-Onepager.pdf` | Auslieferung an Redaktionen — echtes A4, Text auswählbar, Schriften eingebettet |
| `BookSafe-Presse-Onepager.png` | Vorschau / Web-Einbindung, 2382 × 3369 px (288 dpi) |
| `onepager.tmpl.html` | Quelle, mit Platzhaltern für die Schriften |
| `build.py` | ersetzt die Platzhalter durch base64 → `onepager.html` |
| `render.mjs` | rendert PDF und PNG aus `onepager.html` |

## Neu erzeugen

    python3 build.py && node render.mjs

`render.mjs` prüft dabei mit, ob der Inhalt noch aufs Blatt passt
(`ueberlauf` muss 0 sein, `PDF-Seiten` muss 1 sein). Nach Textänderungen
also immer den Ausgabewert lesen — das Blatt schneidet stillschweigend ab,
wenn der Inhalt wächst. Derzeit sind rund 70 px Reserve über dem Fuß.

## Schriften

Beide Schriften stecken als base64 im HTML, damit PDF und PNG überall gleich
aussehen und die Datei ohne Netz funktioniert.

- **Saira** (Schnitt 800) für Auszeichnungen — dieselbe Datei wie auf der Website
- **Source Sans 3** für den Fließtext — Ersatz für die Systemschrift der Website:
  Apples SF Pro darf nicht in ein PDF eingebettet werden

Beide stehen unter der SIL Open Font License 1.1 (`../../assets/fonts/OFL.txt`
bzw. `SOURCE-SANS-OFL.txt`).

## Inhaltlicher Stand

Das Blatt ist auf **Version 1.1** geschrieben (Apple Watch als fünfte
Kernfunktion). `presse/index.html` steht noch auf 1.0 — beides sollte
zusammengeführt werden.
