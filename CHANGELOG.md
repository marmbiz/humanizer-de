# Changelog

Der neueste Eintrag steht im README unter [„Was ist neu?“](README.md#was-ist-neu).
Hier stehen alle früheren Versionen; die GitHub-Releases konservieren die Originalnotizen.

- **5.24.0** - Der Two-Pass-Runner bereinigt die Eingabe jetzt am Eingang. Eine Arbeitskopie
  läuft durch den konservativen Unicode-Fix, und alle Schutzanker frieren auf der reparierten
  Fassung ein. Am Ausgang vergleicht das neue Prüfskript `verify_changes.py` die gelieferte
  Fassung mit dem unveränderten Original und legt den vollen Nachweis als `verify.json` bei.
  Im Report stehen Identität, Änderungsquote und Typografie-Deltas. Damit zählt das Paket 26
  Dateien. Ein fehlerhaft gefülltes Advisory-Feld bricht den Lauf nicht mehr ab, sondern
  wandert aussortiert und begründet in den Report.

- **5.23.0** - Der Sammelcheck ordnet ein unauffälliges Ergebnis jetzt selbst ein. `risk=low`
  heißt nur, dass kein geeichtes Signal angeschlagen hat. Eine neue Calibration-Zeile nennt
  deshalb die Register, in denen die Erkennung am schwächsten ist, darunter Werbung, Social
  Media und Essayistik. Dort kann ein stilles Ergebnis auch eine Lücke sein. Im Formal-Modus
  blockieren Fragezeichen nicht mehr pauschal: Echte Sachfragen erzeugen eine Warnung mit
  Prüfauftrag. Emojis bleiben Blocker. Alle `--fail-on`-Flags erklären in der Hilfe ihre
  Schwelle samt Default, `make help` listet die Make-Ziele auf, und der Entwicklerleitfaden
  führt jetzt alle Skripte.

- **5.22.3** - Wartungslauf. `doctor.py` vergleicht die Version über alle versionstragenden
  Dateien statt nur über die Manifeste. Fehlende Repo-Dateien gelten in der Paketform nicht
  als Fehler. Die Naturalness-Karte zu Muster 7 beschreibt jetzt die konzessive
  „Trotz X … Y“-Schablone statt einer Dublette von Muster 8. In der Modusmatrix des Skills
  sind vier Formulierungen an die verbindlichen Entscheidungstabellen angeglichen.
  Anrede-Befunde von `register_lint` hängen laut korrigierter Doku am gesetzten
  Erwartungswert, nicht am Modus. Aus dem Katalog sind verwaiste Kategorie-Zeilen entfernt,
  aus den Rhythmus-Prüfungen ein totes Muster. WARP beschreibt den Umfang von `--fix` und
  den Release-Ablauf vollständig, und zwei neue Tests sichern die Musterzahl-Angaben und
  die Dateizahl des Pakets.

- **5.22.2** - Das hochladbare Paket trägt jetzt Lizenz und Herkunftsnachweis. Als
  eigenständige Weitergabe braucht es beide. Gebündelt wird nur noch, was der Skill selbst
  aufruft; die Entwicklungswerkzeuge des Repositorys sind draußen, weil sie Testdaten oder
  fremde Programme erwarten und im Paket nicht laufen. `doctor.py` erkennt die Paketform und
  verlangt dort keine Plugin-Manifeste mehr, statt einen vollständigen Stand als Fehler zu
  melden. Weil das Archiv aus einer festen Dateiliste entsteht und seine Metadaten gesetzt
  sind, liefert derselbe Stand auf jedem Betriebssystem dieselbe Prüfsumme. Die
  Installationsanleitung beschreibt den Paketinhalt genauer. Der Präzisionspfad steckt als
  Code im Archiv, es fehlen nur spaCy und das Sprachmodell.
- **5.22.1** - Wer kein Terminal nutzt, installiert den Skill jetzt in der Weboberfläche von
  Claude. `make skill-bundle` packt Skill, Referenzen und Prüfskripte in ein Archiv, das jedem
  Release beiliegt. Die Installationsanleitung beschreibt den Upload und nennt die Einstellung,
  ohne die dort keine Prüfskripte laufen. Derselbe Stand ergibt immer dasselbe Archiv, deshalb
  lässt sich die ausgegebene Prüfsumme gegen die Angabe im Release halten. Am Skill selbst
  ändert sich nichts.
- **5.22.0** - Vier kleine Workflow-Erweiterungen nutzen vorhandene Verträge: Der Sammelcheck
  kann die konservativen Unicode-Korrekturen aus Muster 43/46 mit `--fix-safe` atomar anwenden.
  Der Two-Pass-Runner schreibt für angenommene und abgelehnte Fassungen ein `changes.diff`.
  `normalized.md` hält seine Arbeitsfassung fest, `verify.json` den vollständigen
  Änderungsnachweis gegen das Original.
  Ein report-only Detection-Snapshot hält Treffer und tolerierte Fehlalarme der bestehenden
  Fixtures samt Hash fest. Eine Content-CI-Vorlage veröffentlicht diese Daten und Audits
  geänderter Markdown-Dateien als Artefakt, ohne PR-Kommentare oder Gate. Die Scenario-Contracts
  laufen nun auch über `make verify` in CI. Das Claude-Plugin nutzt die native Skill-Erkennung
  und umgeht damit den fehleranfälligen Root-Pfad älterer Claude-Code-Versionen.
- **5.21.4** - Muster 45 ergänzt drei kontextgebundene Calques aus der Praxis: transitives
  „tragen“ für englisch carries, „Veränderungen umarmen“ für embrace change und „Potenzial
  freischalten“ für unlock potential. Idiomatisches „tragen“ sowie wörtliches Umarmen und
  technisches Freischalten bleiben geschützt. Die Erkennung bleibt urteilsbasiert. Eine neue
  Linter-Regel oder pauschale Wortmarker kommen nicht hinzu.
- **5.21.3** - Der Antithesen-Detektor von Muster 8 erkennt jetzt auch den nachgestellten
  Kontrast-Schwanz: Sätze mit dem Schluss „X, nicht Y.“ zählen in den bestehenden
  Dichtebefund. Abkürzungs-, Dezimal- und Ordinalpunkte gelten dabei nicht als Satzende.
  Wie bisher bleiben beidseitige Wert-Korrekturen nach dem Muster
  „am Dienstag, nicht am Mittwoch.“ ausgenommen, und an den Schwellen ändert sich nichts.
- **5.21.2** - Muster 16 kennt jetzt die Semikolon-Variante: Gehäufte Hauptsatz-Verbindungen per
  Semikolon sind ein Claude-typisches Interpunktionsmuster, und die Ersetzungshierarchie warnt vor
  genau dieser Ausweichroute. Im Katalog sind 66 deutsche Schlusszeichen repariert, die als gerades
  ASCII gesetzt waren. Diese Fehlerklasse behebt `unicode_lint --fix` künftig automatisch. Zehn
  Besser-Beispiele lösten ihr Muster einheitlich per Gedankenstrich oder Semikolon und zeigen nun
  gestreute Ersatzstrategien. Dazu drei Doku-Korrekturen: WARP.md führt Muster 51 nicht mehr als
  linter-gestützt, die SIR-Referenzwerte tragen korrekte Etiketten, und die Modusmatrix beschreibt
  das Linter-Verhalten je Modus.
- **5.21.1** - Pass 4 rotiert Satzanfänge nur noch, wenn wirklich ein Rhythmus-Cluster vorliegt, und
  stoppt am menschlichen Maß von rund 0,8 subjektinitialen Sätzen, statt pauschal jedes dritte
  Vorfeld umzubauen. In gemessenen menschlichen Blog- und Sachtexten beginnen vier von fünf Sätzen
  mit dem Subjekt. Wer tiefer rotiert, erzeugt das nächste Muster. Muster 3 nennt jetzt auch „es ist
  wichtig zu beachten“ und „zu beachten ist, dass“. Bei Muster 64 kennzeichnet der Katalog
  urteilsbasierte Vokabeln maschinenlesbar, ein neuer Test hält Katalog und Linter synchron.
  Erkennungslogik und Schwellen bleiben unverändert.
- **5.21.0** - Der getrennte Two-Pass-Runner unterstützt neben Claude jetzt auch Codex. Codex
  läuft in zwei ephemeren, read-only Prozessen mit strukturierten Ausgaben. Benutzerkonfiguration
  und Exec-Regeln sowie globale oder projektbezogene `AGENTS.md`-Anweisungen werden nicht geladen,
  lokale Skills, Plugin-, App-, Shell- und Werkzeug-Suchfunktionen sind abgeschaltet. Meldet der
  Ereignisstrom trotzdem einen Werkzeugaufruf, verwirft der Host den Lauf. Das Claude-spezifische
  USD-Budget wird bei Codex nicht vorgetäuscht: dort bleiben die Tokenzahlen in den
  Call-Artefakten nachvollziehbar.
- **5.20.0** - Audit und Rewrite können erstmals in zwei wirklich getrennten Modellaufrufen
  laufen. Der optionale lokale Runner friert Kandidaten, Fakten, Zitate, Fachbegriffe und
  Persona-Anker nach dem ersten Aufruf ein. Ein frischer, werkzeugloser Rewrite darf danach
  nur bestätigte Spannen bearbeiten. Eingesetzt werden seine Ersetzungen vom Host, nicht vom
  Modell. Vollständige Überschriften und Sätze gehören dabei jeweils einer Änderung. Unsichere
  Teilstrukturen, überlappende Kandidaten, verschobene Schutzanker und neue Evidence-Blocker
  führen zum Verwerfen statt zu einem scheinbar fertigen Text. Die Quellenprüfung bleibt
  ausdrücklich unvollständig. Der neue Ablauf schützt Stil und Substanz, macht daraus aber
  keinen Belegprüfer. Daneben zählen Fettdruck und Antithesen in Fremdstimmen nicht mehr zur
  Autorenprosa, fünf adverbiale Vorfelder verzerren die SIR-Messung nicht länger, und das
  Evidence-Gate erkennt Beleg-Widerlegungs-Wechsel, ohne `%`/`Prozent` oder `€`/`Euro` als
  Faktenänderung zu behandeln. Muster 64 trennt außerdem ein Cluster abstrakter
  „tragen“-Metaphern von etablierten und konkreten Verwendungen des Verbs.
- **5.19.0** - Unsichtbare Zeichen findet Muster 43 jetzt auch dort, wo sie am gefährlichsten
  sind. Neu geprüft werden der Unicode-Tags-Block und die Variation Selectors. Im Tags-Block
  spiegeln die Zeichen U+E0020 bis U+E007E die druckbaren ASCII-Zeichen, weshalb sich damit
  ein vollständiger Text unsichtbar in einen Absatz einbetten lässt. Von acht getesteten
  Klassen versteckter Zeichen rutschten vorher sieben durch. Zwei Ausnahmen bleiben, sonst
  zerstört die Bereinigung echte Inhalte. Hinter einem Emoji oder einer Keycap-Ziffer darf ein
  Variation Selector stehen, und die Flaggen von Schottland, Wales und England bestehen selbst
  aus Tag-Zeichen. Bei der Ausnahme für Flaggen zählt nicht die Form, sondern die feste Liste
  der drei Kürzel. Sonst ließe sich beliebiger Text als Pseudo-Flagge tarnen. Über 55 Dateien
  aus Testkorpora, Menschentexten und ausgelieferter Dokumentation entstand kein einziger
  neuer Treffer.
- **5.18.1** - Muster 8 nennt jetzt eine weitere Figur: „X hat kein Y-Problem, X hat ein
  Z-Problem“. Statt die Diagnose zu belegen, ersetzt die Umdeutung sie. Geändert hat sich nur
  Dokumentation, keine Erkennungslogik und keine Schwelle.
- **5.18.0** - Gehäufte Gedankenstriche (Muster 16) prüft der Skill jetzt deterministisch.
  Bisher war das Urteilssache. Der neue Detektor `dash_cluster` erkennt zwei Formen: viele
  Striche gedrängt in einem Absatz, und wenige Striche über viele Absätze verstreut, wobei
  gerade die zweite Form die häufigere KI-Gewohnheit ist und bisher übersehen wurde. An 39
  verifizierten Menschentexten sind beide Tore geeicht, ohne einen einzigen Fehlalarm.
  Literatur, Recht und Plenarreden setzen Gedankenstriche schließlich reichlich und völlig
  legitim. Unangetastet bleiben einzelne Striche, Bindestriche in Wörtern, Zahlenbereiche und
  das Schema „nicht X, sondern Y“, das zu Muster 8 gehört. Anlass war eine eigene Messung. Im
  Schnitt setzt Claude 1,56 Gedankenstriche gegen 0,56 bei GPT, fast dreimal so viele, und
  damit ruht das Muster erstmals auf deutschen Daten statt auf einer aus dem Englischen
  entliehenen Vorlage. GPT verrät sich woanders: an gleichförmigeren Satzlängen.
- **5.17.3** - Der Werbeschablonen-Hook ist wieder draußen. Er kam mit 5.17.0 und sollte
  Fundstellen nach jedem Schreibvorgang an das Modell melden, ohne Platz in `SKILL.md` zu
  kosten. In zwölf Vergleichsläufen mit und ohne Hook stand es null zu null. Kaputt war er
  nicht, die Zustellung ist nachgewiesen. Dabei bekam er nie etwas zu melden, weil der Detektor
  auf frisch erzeugter Werbung schweigt und weil bei Text im Prompt gar keine Datei geschrieben
  wird. Seinen eigentlichen Zweck erfüllt ohnehin die Preflight-Kopplung: ein Kanal neben
  Prompt und Anleitung, gemessen wirksam, eine Zeile Code. Der Detektor und diese Kopplung
  bleiben unverändert. Damit fallen 356 Zeilen weg, dazu 14 Tests und eine Datenschutzzeile,
  die eine wirkungslose Funktion erklären musste.
- **5.17.2** - `register_lint` hält jetzt, was SKILL.md verspricht. Zwei dort beschriebene
  Ausnahmen fehlten im Code. Ein `ja` hinter dem Doppelpunkt zählte als Modalpartikel, und in
  einem Rezept stand eben „Vegetarisch: Ja“. Dasselbe traf `mal` in `5-mal` und `schon` in
  zeitlicher Bedeutung. Die zweite Lücke saß bei der Anapher: Das satzinitiale `Sie` sollte
  laut Anleitung ungezählt bleiben, wenn es sich auf ein Bezugswort zurückbezieht, doch die
  Ausnahme kippte, sobald irgendwo im Vorsatz eine Du-Form stand. In einem durchgehend duzenden
  Text ist das der Normalfall. Gemessen an 19 verifizierten Menschentexten aus Recht, Leichter
  Sprache, Rezepten und Behördendeutsch sinken die Warnungen von 10 auf 5 Texte. Echte
  Registerbrüche und echte Partikelhäufungen findet der Linter weiterhin.
- **5.17.1** - Der Hook ist jetzt opt-in. In 5.17.0 lief er ab Installation mit und schickte
  bei jeder geschriebenen Markdown- oder Textdatei Auszüge an das Modell, auch wenn niemand den
  Skill aufgerufen hatte. Das war die falsche Voreinstellung für ein Werkzeug, dessen
  Doctor-Check eigens meldet, dass keine Nutzertexte gelesen wurden. Ohne
  `HUMANIZER_AD_HOOK=on` bleibt er still. Alles andere gilt als aus: ein leerer Wert, `off`,
  `0`, `false` oder irgendetwas Unerwartetes. Wer ihn will, schaltet ihn bewusst ein.
- **5.17.0** - Werbeschablonen erkennt der Skill jetzt deterministisch. Der neue Detektor
  `ad_boilerplate_cluster` sucht Figuren statt Vokabeln: Sozialbeweis wie „über 3.400 Betriebe
  vertrauen bereits“, Standard-Werbeabschnitte wie „Das sagen unsere Kunden“, gestapelte
  Handlungsaufforderungen. Einzeln zählt nichts davon. Erst im Verbund meldet er etwas.
  Wortlisten waren der erste Versuch, und sie fielen im August durch: 19 von 27 geratenen
  Kandidaten kamen in echter KI-Werbung gar nicht vor. Im Sammelcheck wiegt der Befund doppelt,
  denn bisher meldete der bei Werbetexten `preflight: low` — und das Modell nahm die Entwarnung
  als Freibrief, obwohl die Schablonen offen im Text standen. Am Testtext t3 entfernt der alte
  Stand 0 von 7 Schablonen, der neue 6 von 7, bei unveränderten 13 Zahlen, Normen und Namen.
  Dazu kommt ein Hook. Nach jedem Schreibvorgang meldet er dieselben Fundstellen an das Modell,
  ohne Platz in `SKILL.md` zu kosten. Das Muster stammt von Anthropic: Deren offizielles Plugin
  `security-guidance` aus dem `claude-plugins-official`-Marketplace prüft bei `PostToolUse` mit
  Matcher auf die Schreibwerkzeuge und reicht Befunde über
  `hookSpecificOutput.additionalContext` weiter. Bei Text, der direkt im Prompt steht, greift
  er nicht. Die Musterzahl bleibt bei 72. Muster 2 und 44 sind jetzt teilweise linter-gestützt,
  Muster 9 bleibt Urteilssache. Auf frisch erzeugter KI-Werbung feuert der Detektor allerdings
  nicht. In sechs Testläufen entstanden sechs verschiedene Überschriften für dieselbe
  Kundenstimmen-Sektion, und davon kennt er genau eine. Er erkennt also Formulierungen und
  keine Bauformen. Das begrenzt ihn auf Texte, die t3 ähneln.
- **5.16.0** - Die Quellenprüfung hängt nicht mehr am Stil-Ergebnis. Fand der Skill stilistisch
  nichts zu tun, hörte er bisher ganz auf — auch bei den Belegen, obwohl die Null-Edit-Regel
  dort ausdrücklich eine Ausnahme vorsah. Sie stand als Nachsatz einer Stilregel und wurde mit
  ihr abgehakt. In vier Texten des Wirksamkeitspiloten schrieb der Skill deshalb je über hundert
  Wörter zu Anführungszeichen und Passivsätzen, aber kein Wort zu den eingebauten Falschquellen.
  Jetzt läuft der Belegteil unabhängig davon, ein niedriges Preflight-Risiko verkürzt ihn nicht
  mehr, und jede erkannte Quelle wird einzeln eingestuft — auch die Zahlen, die an einer bereits
  geprüften Institution hängen und ihre Glaubwürdigkeit allein von ihr beziehen. Dafür bekommt
  der Output einen Pflichtblock „Belege“, der auch beim Null-Edit erscheint. Auf denselben vier
  Texten steigt die Zahl beanstandeter Quellen von null auf drei von acht. Die Umstellung wirkt
  bei sachfremden Autoritäten. Erfundene Aktenzeichen und erfundene Personen bleiben dagegen
  unmarkiert, denn sie sehen im Text unauffällig aus und fallen nur auf, wenn jemand sie
  nachschlägt.
- **5.15.1** - Drei Reibungspunkte aus dem ersten Gebrauchs-Audit behoben, alle an echten
  Ausführungsspuren gemessen. Eingabedateien löst der Skill jetzt zuerst im Arbeitsverzeichnis
  auf und fragt sonst nach — vorher suchte er im eigenen Installationsordner und systemweit,
  woran ein kompletter Lauf scheiterte. Beim Nachschlagen in Referenzdateien fordert er
  Zeileninhalt statt der Dateiliste an, die zuvor drei Anläufe für ein einzelnes Muster
  kostete. Und den Katalog holt er nun gezielt über die Pass-Anker aus 5.15.0 statt die ganze
  Datei zu lesen. Der Volltext bleibt dem Audit-Zweig vorbehalten. Hintergrund der letzten
  Änderung: Nach der Katalog-Kopplung las jeder Lauf die 14.700 Wörter dreimal, gemessen
  45 Prozent Mehrkosten auf drei Vergleichstexten.
- **5.15.0** - Seit dieser Version hängt der Musterkatalog an der Arbeitsanweisung. Bisher rief
  die Anleitung 20 der 72 Muster beim Namen auf, 19 weitere waren über Prüfskripte erreichbar.
  Der Rest hatte keinen Weg in die Prüfung: Ein Trikolon blieb in einem Autorentext unbemerkt,
  obwohl der Katalog es seit jeher als Muster 9 führt. In jedem Musterblock steht nun, zu welchem
  Durchgang er gehört, und jeder Durchgang arbeitet alle seine Muster ab statt nur der genannten
  Schwerpunkte. Neu ist außerdem ein eigener Zweig für das reine Audit. Wer Befunde will und keine
  Redaktion, bekommt den vollständigen Katalog geprüft — auch dann, wenn die Oberflächenmessung
  zuvor Entwarnung gab, denn sie sieht Wortwahl und Satzrhythmus, nicht rhetorische Figuren.
  Für die Anleitung steigt die Wortgrenze dafür von 2000 auf 2300.
- **5.14.0** - Acht Robustheitsfehler behoben, die das Werkzeug an Stellen blind oder falsch
  machten, an denen niemand nachgesehen hatte. Enthielt ein unveränderter Text sowohl
  Steigerungs- als auch Sinkwörter, blockierte ihn das Evidence-Gate, jetzt blockt nur eine echte
  Richtungsänderung. In einzeiligem HTML wird die Prosa wieder geprüft, was den Parsedown-Weg
  betrifft, ganze fett gesetzte Sätze zählen nun mit, und zwischen benachbarten Fett-Spannen
  entstehen keine Phantom-Treffer mehr. Zitierte Fremdrede zählt nicht mehr zur Autorenstimme.
  An juristischen Abkürzungen wie Abs. oder Art. bricht die Satztrennung
  nicht mehr, und nummerierte Listen bleiben ganz. Im Präzisionspfad unterscheidet der
  Register-Check jetzt das informelle Plural-ihr von der Höflichkeitsform. Dazu kommen kleinere
  Korrekturen bei Abstrakta im Singular und bei Mehrwortmarkern mit ungewöhnlichem Leerzeichen.
  Katalog und Schwellen bleiben unverändert. Die Fehlalarm-Baseline ist byte-identisch geblieben.

- **5.13.0** - Befunde von `syntax_lint` erscheinen jetzt als Hinweise mit Severity `info` im
  kompakten Audit-Report. Bisher war Muster 39 nur in einer internen Sektion sichtbar.
  **Achtung für CI-Nutzer:** Advisory-Befunde sind ab sofort gate-neutral, `--fail-on any`
  schlägt darauf also nicht mehr an. Ohne diese Regel würde jeder deutsche Text mit einer
  Passivkonstruktion das Gate reißen, denn ein Hinweis liefert Kontext und keinen Defekt.
  Betroffen ist auch der Kandidatenhinweis für Muster 72, der bisher für sich genommen Exit-Code
  `1` auslöste. Künftig werden auffällige unbelegte oder erfundene Quellen unabhängig vom
  Stilbefund markiert, selbst wenn der Text sonst unangetastet bleibt. Weil Markieren kein Eingriff
  ist, bleibt der Null-Edit-Vertrag intakt. Klarstellung zur Modussteuerung: Der Muster-Linter meldet modusunabhängig,
  nur die Preflight-Empfehlung wertet den Modus maschinell aus. Katalog und Schwellen bleiben unverändert.

- **5.12.0** - Wartungsrelease mit zwei geschlossenen Detektor-Lücken: Fettdruck-Marker
  schlossen die Prosa zwischen zwei Fett-Spannen als Zitat aus, und der Fakten-Carve-out griff
  nur für „nicht A, sondern B“. Wochentags-, Monats- und Einheitenkorrekturen bleiben jetzt in
  beiden Antithesenformen unbeanstandet. Zeilenenden überleben Lesen und Schreiben, damit
  Positionsangaben zur Datei passen. Unlesbare Dateien und defekte Fixtures enden
  vertragsgemäß mit Exit-Code `2`. **Für CI-Nutzer wichtig:** `--fail-on blocker` entfällt bei
  `unicode_lint.py`, `rhythm_lint.py`, `german_pattern_lint.py` und `spell_lint.py`, weil
  diese Scripts keine Blocker erzeugen und die Option das Gate still abschaltete. Dazu
  kleinere Korrekturen an Scope, Segmentierung und Tokenisierung sowie durchgehend korrekte
  Orthografie in den ausgelieferten Skill-Dateien. Katalog und Schwellen bleiben unverändert.

- **5.11.0** - Der Naturalness-Linter erkennt dichte M8-Cluster aus „nicht A, sondern B“
  und „A und nicht B“ und berücksichtigt sie im Preflight. Gemeinsames Scope-Handling schützt
  Zitate, Code, URLs und HTML; eindeutige Zahlen- und Datumskorrekturen bleiben unbeanstandet.
  Schwellen und Katalogumfang ändern sich nicht.

## Ältere Reihen

| Reihe | Wichtigste Änderungen |
|---|---|
| **5.10.x** | Katalog auf 72 Muster erweitert; adressierbare Findings, Null-Edit-Vertrag, präziseres Zitat-Scoping sowie klarere Mess-, Installations- und Auslieferungsdokumentation. |
| **5.9.x** | Muster 67–69 für Ankündigungs-Spaltsätze, Komparativ-Rahmung und strukturellen Register-Kollaps ergänzt. |
| **5.8.x** | Deterministische Prüfungen für negative Parallelismen und Fettschrift eingeführt; Anbieter-Artefakte und M59-Prüffragen aktualisiert. |
| **5.7.x** | Doctor, Windows-Härtung, Absatz-Konnektoren, Formal-Emoji und Satzmetrik-Kalibrierung ergänzt. |
| **5.6.x** | Plugin portabel paketiert; Evidence-Gate, Markdown-Scoping, QGIR, Fehlerpfade und CI erweitert. |
| **5.5.x** | `--precise`, False-Positive-Korpus, Original-Ledger, Syntaxmetriken und CI-Exit-Codes eingeführt. |
| **5.4.x** | Optionale spaCy-Syntaxanalyse und positive Qualitätsrubrik ergänzt. |
| **5.3.x** | Lokales Stilprofil, gemeinsame Zählregeln und robuste CLI-Verträge eingeführt. |
| **5.0–5.2** | Sammelaudit, Preflight/Combing und klares Skill-Routing aufgebaut. |
| **4.x** | Eigenständiges SemVer, QGIR, Evidence-/Register-Contracts und Katalogausbau auf 66 Muster. |
| **3.x** | Fork zur modularen deutschen Skill-Architektur mit Lintern, Tests und 63 Mustern ausgebaut. |
| **1.x–2.x** | Deutsche Ausgangsfassung und erste Audit-, Severity- und Moduslogik. |
