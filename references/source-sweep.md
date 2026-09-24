# Quellen-Sweep

Als optionale externe Belegprüfung öffnet der Quellen-Sweep die zitierten Quellen, also
Webseite, PDF oder Abstract, und hält sie gegen die Aussagen im Text. Er ist kein weiterer
Pass. Er läuft als eigener Schritt ganz am Ende.

## Warum am Ende

Stil und Quellen verlangen zwei verschiedene Arten zu lesen. Rhythmus, Figuren und Struktur
erkennt nur, wer den Text am Stück liest; die Quellenprüfung dagegen wandert durch fremde
Dokumente, sucht Fundstellen und rechnet nach, sodass beim Wechsel zwischen beidem der Blick
aufs Ganze verloren geht und die geladenen Quelltexte den Kontext füllen. Dazu kommt der
Rewrite. Jede Umformulierung kann den Anspruch einer Aussage verschieben. Vor dem Rewrite
geprüft, gilt das Ergebnis für einen Text, den es danach so nicht mehr gibt. Maßgeblich ist
deshalb die Endfassung.

## Aufgabenteilung mit Pass 1

| Schritt | Was | Was nicht |
|---|---|---|
| Pass 1 | Belege im Text prüfen: fehlende Fußnote, vage Autorität (M11), Formfehler und Prüfziffern (M26), Zahlen gegen Zahlen im selben Text nachrechnen, Aussage stärker als die eigene Fußnote (M42, soweit im Text sichtbar), Spekulation (M53). Jeden Fund markieren. | Keine Quelle öffnen, nichts abrufen. |
| Quellen-Sweep | Die markierten und alle übrigen zitierten Quellen öffnen und gegen die Aussage halten. | Keine Stilarbeit, keine Umformulierung. |

## Wann er läuft

- Nur auf ausdrücklichen Wunsch: „Quellen prüfen“, „volle Stärke“, „mit Belegprüfung“ oder gleichwertig.
- Erst nach Pass 5, im Audit-Zweig nach dem vollständigen Musterdurchgang.
- Beim Rewrite auf der geänderten Fassung, nicht auf dem Original.
- Ohne Netz- oder Dateizugriff entfällt er; betroffene Quellen tragen dann `[QUELLE NICHT VERIFIZIERT]`.

## Ablauf

1. Belegliste bauen. Pro Aussage steht darin eine Zeile mit wörtlichem Kurzzitat, Fußnote
   oder Anker, der Quelle samt Link und der Pass-1-Markierung, falls es eine gibt. Auch
   Aussagen ohne Quelle gehören hinein, sobald sie eine Zahl oder Tatsache behaupten.
2. Auslagern, wo der Host es erlaubt. Ein Subagent mit frischem Kontext bekommt nur die
   Belegliste, nicht den Stilbericht. Ohne Subagenten läuft der Sweep im selben Kontext,
   aber erst nach dem abgeschlossenen Stilteil.
3. Selbst lesen. Die Fundstelle wird wörtlich gesucht; bei PDFs erst den Text extrahieren
   und dann nach Zahl oder Schlüsselbegriff durchsuchen, statt einer fremden Zusammenfassung
   zu trauen.
4. Pro Aussage einstufen:
   - `bestätigt`: Zahl, Zeitraum und Reichweite der Aussage stehen so in der Quelle.
   - `abweichend`: Die Quelle existiert, sagt aber etwas anderes oder weniger (M42). Konkret benennen, etwa Erhebungs- statt Erscheinungsjahr, Einleitungssatz statt Ergebnis oder engere Population.
   - `nicht prüfbar`: Quelle nicht erreichbar oder Fundstelle nicht im zugänglichen Teil. Einen Kongruenzvorwurf gibt es dann nicht (operative Schranke aus M42).
   - `fehlt`: Die Aussage braucht eine Quelle und hat keine (M11/M53).
5. Nichts reparieren. Am Text ändert der Sweep nichts. Korrekturen folgen erst auf
   Nutzerauftrag und laufen danach wieder durch Claim-Lock und Pass 5.

## Output

Im Output-Block „Belege“ steht dann je Aussage eine Zeile: Kurzzitat, Status und in einem
Satz die Fundstelle oder die Abweichung. Rechenproben wie Summen oder Quoten stehen gesammelt
in einer Zeile. Was ungeprüft blieb, etwa die Zugehörigkeit von Autoren oder ein fehlender
Messzeitraum, wird ausdrücklich genannt.

## Grenzen

Geprüft wird nur, was die zugängliche Quelle zeigt. Eine fachliche Endabnahme ersetzt der
Sweep nicht, und Vollständigkeit verspricht er auch nicht.
