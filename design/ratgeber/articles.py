"""Inhalte der Ratgeber-Seiten. Erzeugt werden sie von build.py.

Jeder Artikel: slug, title (Browser-Tab/Suche), description (Suchergebnis),
h1, sub, teaser (Übersicht), body (HTML, mit {SHOT:name|alt|Bildunterschrift}).

Belege für die App-Aussagen (Stand 19.10.2026, App 1.8):
- Mitteilung um 9 Uhr nur bei tagesgenauem Datum: ReleaseNotificationPlan (OPT-316/317)
- Feuerwerk am Erscheinungstag: FEAT-224; Countdown-Widget: 0.3
- „Weitere Bände der Reihe“, Tipp öffnet „Buch hinzufügen“: FEAT-222/223, SeriesView
- Reihen bündeln: FEAT-245; Status „Abgebrochen“: FEAT-242; eigene Listen: FEAT-247/249
- Leih-Erinnerung 2 Tage vorher und am Tag: LoanNotifications.warnLeadDays
- Ausleihbeleg scannen: FEAT-202; Standort: FEAT-246
- ISBN-Scanner liest Barcode und gedruckte Nummer: FEAT-235
- Import aus anderen Apps: OPT-323; Export CSV/PDF; Backup-Datei: FEAT-237
- Preis: kostenlos bis 50 Bücher, Pro 3,99 € einmalig (Store, Presse-One-Pager)
"""
import datetime

PUBLISHED = datetime.date(2026, 10, 19)

ARTICLES = [
    {
        "slug": "neuerscheinungen-nicht-verpassen",
        "title": "Neuerscheinungen nicht verpassen: Erscheinungstermine | BookSafe",
        "description": "Wie du Erscheinungstermine deiner Lieblingsautorinnen und -autoren im Blick behältst: Wunschliste mit Countdown, Erinnerung am Erscheinungstag und warum der genaue Tag zählt.",
        "h1": "Neuerscheinungen nicht verpassen",
        "sub": "So behältst du Erscheinungstermine im Blick, ohne ständig nachzusehen.",
        "teaser": "Wunschliste, Countdown und eine Erinnerung am Tag selbst, und warum der genaue Tag zählt.",
        "body": """
    <p class="lead">Der nächste Band ist angekündigt, aber bis er erscheint, vergehen Monate. Am Ende entdeckt man ihn zufällig in der Buchhandlung oder gar nicht. Mit ein paar Handgriffen lässt sich das vermeiden.</p>

    <h3>Woher du Termine bekommst</h3>
    <ul>
      <li><strong>Verlag und Buchhandel:</strong> Vorbestellbare Titel stehen dort meist schon Monate vorher, oft mit Datum.</li>
      <li><strong>Die Autorin oder der Autor selbst:</strong> Website, Newsletter und Social Media nennen den Tag oft früher und genauer.</li>
      <li><strong>Bibliothekskataloge:</strong> Angekündigte Bücher erscheinen dort früh, aber häufig nur mit Monat oder Jahr.</li>
    </ul>

    <h3>Eine Liste statt vieler Lesezeichen</h3>
    <p>Wichtig ist, dass alle Termine an einem Ort stehen. In BookSafe setzt du ein angekündigtes Buch auf die <strong>Wunschliste</strong>, per ISBN-Scan oder über die Titelsuche. Die Wunschliste zeigt bei jedem Buch, wie viele Tage es noch dauert, und der Erscheinungskalender zeigt die Cover an ihrem Tag. Ein Widget auf dem Home-Bildschirm zählt ebenfalls herunter.</p>
    {SHOT:de-wishlist|Wunschliste in BookSafe: anstehende Erscheinungen mit Countdown in Tagen|Wunschliste mit Countdown}

    <h3>Der genaue Tag macht den Unterschied</h3>
    <p>Am Erscheinungstag kommt um 9 Uhr eine Mitteilung, und beim Öffnen der App erscheint das Cover groß mit einem kleinen Feuerwerk. Beides klappt nur, wenn der <strong>genaue Tag</strong> bekannt ist. Steht im Katalog nur der Monat oder das Jahr, trägst du den Tag selbst ein: im Buch unter „Weitere Angaben“ beim Datum auf den Stift tippen.</p>

    <h3>Kurz zusammengefasst</h3>
    <ul>
      <li>Angekündigte Bücher sofort auf eine Wunschliste setzen, nicht erst kurz vorher.</li>
      <li>Den genauen Tag eintragen, sobald Verlag oder Autorin ihn nennen.</li>
      <li>Mitteilungen erlauben, sonst fällt die Erinnerung am Tag weg.</li>
    </ul>
""",
    },
    {
        "slug": "buchreihe-reihenfolge",
        "title": "Buchreihen in der richtigen Reihenfolge lesen | BookSafe",
        "description": "Welcher Band kommt als Nächstes? So findest du die Reihenfolge einer Buchreihe heraus, erkennst fehlende Bände und behältst lange Reihen im Überblick.",
        "h1": "Buchreihen in der richtigen Reihenfolge lesen",
        "sub": "Welcher Band kommt als Nächstes, und welcher fehlt noch im Regal?",
        "teaser": "Bandnummern finden, fehlende Bände erkennen und lange Reihen im Überblick behalten.",
        "body": """
    <p class="lead">Bei Reihen entscheidet die Reihenfolge, ob die Geschichte aufgeht. Gleichzeitig steht die Bandnummer oft nur klein auf dem Buchrücken oder gar nicht, und deutsche Ausgaben erscheinen manchmal in anderer Reihenfolge als die Originale.</p>

    <h3>Wo die Bandnummer steht</h3>
    <ul>
      <li><strong>Im Buch:</strong> Titelei oder Klappentext nennen oft „Band 3“ oder „Der dritte Fall“.</li>
      <li><strong>Beim Verlag:</strong> Reihenseiten listen die Bände meist vollständig und in Reihenfolge.</li>
      <li><strong>In Bibliothekskatalogen:</strong> Dort sind Reihe und Bandnummer als eigene Angabe erfasst, auch für ältere Bücher.</li>
    </ul>
    <p>Achtung bei Übersetzungen: Manchmal erscheint ein Band auf Deutsch später oder wird ganz ausgelassen. Im Zweifel gilt die Reihenfolge der deutschen Ausgabe, wenn du auf Deutsch liest.</p>

    <h3>Die Reihe auf einen Blick</h3>
    <p>BookSafe übernimmt Reihe und Band beim Erfassen aus den Bibliothekskatalogen, soweit diese sie kennen; sonst trägst du beides selbst ein. Die Reihenansicht sortiert deine Bände nach Nummer, und unter <strong>„Weitere Bände der Reihe“</strong> siehst du, welche Bände du noch nicht hast. Ein Tipp darauf öffnet „Buch hinzufügen“ mit den Angaben des Bands, dort kannst du ihn gleich auf die Wunschliste setzen.</p>
    <p>Wer viele Reihen besitzt, kann sie in der Bibliothek bündeln: Dann steht jede Reihe als ein Eintrag in der Liste statt als viele einzelne Bücher.</p>
    {SHOT:de-detail|Buchdetail in BookSafe mit Lesestatus, Bewertung und Standort|Buchdetail}

    <h3>Kurz zusammengefasst</h3>
    <ul>
      <li>Die Bandnummer gleich beim Erfassen mitspeichern, nicht später nachsuchen.</li>
      <li>Bei Übersetzungen auf die Reihenfolge der deutschen Ausgabe achten.</li>
      <li>Fehlende Bände auf die Wunschliste setzen, dann verpasst du auch neue.</li>
    </ul>
""",
    },
    {
        "slug": "sub-abbauen",
        "title": "SuB abbauen: Tipps für den Stapel ungelesener Bücher | BookSafe",
        "description": "Der SuB wächst schneller, als du liest? Praktische Tipps, um den Stapel ungelesener Bücher abzubauen: Überblick verschaffen, auswählen, Ziele setzen und auch mal abbrechen.",
        "h1": "SuB abbauen: Tipps für den Stapel ungelesener Bücher",
        "sub": "Wenn der Stapel schneller wächst, als du liest.",
        "teaser": "Überblick verschaffen, bewusst auswählen, ein Jahresziel setzen und auch mal abbrechen.",
        "body": """
    <p class="lead">SuB steht für „Stapel ungelesener Bücher“. Fast jede Leserin und jeder Leser hat einen, und meist wächst er schneller, als er schrumpft. Das ist kein Problem, solange er Freude macht und kein schlechtes Gewissen.</p>

    <h3>1. Erst einmal zählen</h3>
    <p>Wie groß ist der Stapel wirklich? Wer alle Bücher erfasst und als „Ungelesen“ markiert, sieht es schwarz auf weiß. In BookSafe filterst du die Bibliothek nach Status und siehst die Zahl in der Statistik. Oft ist der SuB kleiner als gefühlt, manchmal größer.</p>

    <h3>2. Kleine Stapel statt eines großen</h3>
    <p>Eine Liste mit fünfzig Büchern lähmt eher. Besser sind kleine Auswahlen: „Herbstbücher“, „Für den Urlaub“, „Endlich lesen“. In BookSafe legst du dafür eigene Listen an und ziehst Bücher hinein. Die nächste Lektüre kommt dann aus einer Auswahl von fünf statt aus fünfzig.</p>

    <h3>3. Ein Ziel, das passt</h3>
    <p>Ein Jahresziel hilft, wenn es erreichbar ist. Die Lese-Challenge auf dem Heute-Bildschirm zeigt, wie viele Bücher du dieses Jahr gelesen hast und ob du im Plan liegst. Lesesitzungen mit Timer zeigen dazu, wie viel Zeit du wirklich liest.</p>
    {SHOT:de-today|Heute-Bildschirm in BookSafe mit Spruch des Tages, Lese-Challenge und aktuellem Buch|Heute mit Lese-Challenge}

    <h3>4. Abbrechen ist erlaubt</h3>
    <p>Ein Buch, das nach fünfzig Seiten nicht zündet, muss nicht zu Ende gelesen werden. Markiere es als „Abgebrochen“: Es verschwindet vom Stapel, zählt aber nicht als gelesen. So bleibt die Statistik ehrlich.</p>

    <h3>5. Neue Käufe bewusst</h3>
    <p>Wer vor dem Kauf auf die eigene Liste schaut, kauft seltener doppelt. BookSafe warnt beim Erfassen, wenn ein Buch schon in der Bibliothek steht. Und was nicht sofort sein muss, kommt erst auf die Wunschliste.</p>
""",
    },
    {
        "slug": "buecherei-leihfristen",
        "title": "Bücherei-Bücher rechtzeitig zurückgeben: Leihfristen | BookSafe",
        "description": "Nie wieder Mahngebühren: So behältst du die Leihfristen deiner Bücherei-Bücher im Blick, mit Erinnerung vor dem Rückgabetag und dem Ausleihbeleg als Abkürzung.",
        "h1": "Bücherei-Bücher rechtzeitig zurückgeben",
        "sub": "Leihfristen im Blick, ohne Mahngebühren.",
        "teaser": "Rückgabetage festhalten, rechtzeitig erinnert werden und den Ausleihbeleg als Abkürzung nutzen.",
        "body": """
    <p class="lead">Die Bücherei ist die günstigste Art, viel zu lesen. Nur die Rückgabetage gehen im Alltag leicht unter, besonders wenn mehrere Bücher mit verschiedenen Fristen zu Hause liegen.</p>

    <h3>Was hilft</h3>
    <ul>
      <li><strong>Den Ausleihbeleg aufheben:</strong> Er nennt alle Bücher mit ihren Fristen.</li>
      <li><strong>Das Online-Konto der Bücherei:</strong> Dort lässt sich meist auch verlängern, wenn das Buch nicht vorgemerkt ist.</li>
      <li><strong>Eine Erinnerung vor dem Tag,</strong> nicht erst am Tag selbst. Dann bleibt Zeit zum Verlängern oder Zurückbringen.</li>
    </ul>

    <h3>Leihen in BookSafe</h3>
    <p>In BookSafe stellst du bei einem Buch den Besitz auf „Ausgeliehen“, trägst ein, von wo es kommt, zum Beispiel „Stadtbücherei“, und gibst das Rückgabedatum an. Die Bibliothek zeigt dann bei jedem Buch, wie viele Tage bis zur Rückgabe bleiben, und markiert überfällige Bücher.</p>
    <p>Zwei Tage vor der Rückgabe und am Rückgabetag selbst kommt eine Mitteilung. Sind mehrere Bücher am selben Tag fällig, fasst BookSafe sie in einer Mitteilung zusammen.</p>
    {SHOT:de-library|Bibliothek in BookSafe mit Leih-Hinweisen wie „Rückgabe in 5 Tagen“ und „2 Tage überfällig“|Leihfristen in der Bibliothek}

    <h3>Die Abkürzung: den Beleg scannen</h3>
    <p>Statt jede Frist einzutippen, scannst du den gedruckten Ausleihbeleg. BookSafe liest die Titel und Fristen, ordnet sie deinen Büchern zu und fragt nach, wo es unsicher ist. Nach einer Verlängerung reicht ein neuer Scan des neuen Belegs.</p>
""",
    },
    {
        "slug": "buecher-erfassen",
        "title": "Eigene Bücher erfassen: die Bibliothek per ISBN-Scan | BookSafe",
        "description": "Wie du deine Bücher schnell erfasst: ISBN scannen, Daten aus Bibliothekskatalogen, Standort im Regal festhalten und bestehende Listen aus anderen Apps übernehmen.",
        "h1": "Eigene Bücher erfassen: die Bibliothek per ISBN-Scan",
        "sub": "Vom Regal in die App, ein Buch nach dem anderen oder alle auf einmal.",
        "teaser": "ISBN scannen, Standort festhalten, bestehende Listen übernehmen und die Daten sichern.",
        "body": """
    <p class="lead">Eine eigene Bücherliste lohnt sich: Man kauft nichts doppelt, findet Bücher im Regal wieder und weiß, was man verliehen hat. Der Aufwand ist kleiner, als er aussieht.</p>

    <h3>Die ISBN ist der Schlüssel</h3>
    <p>Fast jedes Buch trägt eine ISBN, meist als Strichcode auf der Rückseite. In BookSafe hältst du die Kamera darauf, und Titel, Autor, Cover, Verlag und Erscheinungsdatum kommen aus Bibliothekskatalogen. Ist der Strichcode beschädigt oder überklebt, liest der Scanner auch die gedruckte Nummer darüber. Ältere Bücher ohne ISBN findest du über die Titelsuche oder trägst sie von Hand ein.</p>
    {SHOT:de-library|Bibliothek in BookSafe mit Covern, Autoren und Lesestatus|Die Bibliothek}

    <h3>Den Standort gleich mitspeichern</h3>
    <p>Wer mehrere Regale hat, trägt beim Erfassen den Ort und das Fach ein, etwa „Wohnzimmer, Fach 2“. Die Suche findet Bücher dann auch über den Standort.</p>

    <h3>Schon eine Liste woanders?</h3>
    <p>Wer seine Bücher bisher in einer anderen Buch-App geführt hat, exportiert dort eine CSV-Datei und importiert sie in BookSafe. Bei den Exporten gängiger Buch-Apps kommen Bewertungen, Lesestatus, Lesedaten und Notizen mit. Eine reine ISBN-Liste funktioniert ebenfalls.</p>

    <h3>Die eigenen Daten sichern</h3>
    <p>BookSafe braucht kein Konto. Die Bibliothek liegt auf dem Gerät und gleicht sich über deine private iCloud zwischen iPhone und iPad ab. Dazu kannst du sie jederzeit als CSV oder PDF exportieren oder als eine Backup-Datei sichern.</p>
""",
    },
]
