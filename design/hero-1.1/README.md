# Hero 1.1 — „Die Bibliothek zeigen"

Der Hero der Landingpage für Release 1.1, in drei Breiten.

| Datei | Breite |
|---|---|
| `Main.dc.html` | Desktop, 1440 × 820 |
| `MainTablet.dc.html` | iPad hochkant, 834 × 1112 |
| `MainPhone.dc.html` | iPhone, 390 × 844 |
| `canvas.json` | Anordnung, Titel und Notizen der Canvas |

Herkunft der Werte: Farben, Radien und Schatten aus `assets/tokens.css`;
Systemschrift-Stack und die Größen der Fließtexte aus dem Hero-CSS in
`index.html`. Neu gegenüber der heutigen Seite ist **Saira** als
Display-Schrift — sie steht in `tokens.css` bereits als `--font-display`
und läuft in der App, auf der Website bisher nicht. Sie wird über Google
Fonts geladen.

Ab 834 px stapelt sich der Hero: Text oben, Geräte darunter. Auf dem iPhone
entfällt die Fakten-Zeile, weil der Fließtext dasselbe schon sagt.

Bilder: `shot-*.jpg` und `app-icon.jpg` sind verkleinerte Fassungen aus
`assets/` (Quellbreite 720 px) — für den echten Einbau gehören die Originale
hinein. `badge-de.svg` ist unverändert übernommen.

`booksafe-hero-varianten.html` ist die zusammengesetzte Canvas. Sie wird aus
den Dateien oben neu erzeugt und nicht von Hand bearbeitet.

Die verworfenen Richtungen A und C stehen im vorigen Commit auf diesem Branch.
