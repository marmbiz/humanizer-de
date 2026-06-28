# Evidence Ledger

Nutze diese Ledger-Regeln, bevor ein Text menschlicher umformuliert wird. Ziel ist nicht mehr Kontrolle ueber Stil, sondern Schutz vor semantischer Drift.

## Geschuetzte Anker

Diese Elemente duerfen durch Humanisierung nicht verschwinden, wandern oder ihre Bedeutung aendern:

- Zahlen, Prozentwerte, Geldbetraege, Zeitraeume und Datumsangaben
- Eigennamen von Personen, Organisationen, Orten, Produkten und Quellen
- direkte Zitate und zitierte Satzteile
- URLs, DOI/ISBN/ISSN, Aktenzeichen, Paragraphen und Normverweise
- Code, Statuscodes, technische Feldnamen, Dateinamen und API-Bezeichner
- Autoritaetsgrad: "belegt", "vermutlich", "laut", "kann", "muss"

## Operationstypen

| Typ | Erlaubt? | Bedingung |
|---|---|---|
| `STYLE_ONLY` | ja | Keine geschuetzten Anker neu, weg oder anders bewertet |
| `SPLIT_SENTENCE` | ja | Anker bleiben wortgleich erhalten |
| `MERGE_SENTENCE` | ja | Logische Beziehungen bleiben gleich |
| `DROP_FLUFF` | ja | Nur Artefakt ohne Informationsgehalt entfernen |
| `CLARIFY_WITH_EXISTING_EVIDENCE` | ja | Konkretion steht bereits im Input oder Kontext |
| `MARK_GAP` | ja | Fehlende Quelle/Substanz sichtbar markieren |
| `BLOCK_SOURCE_MISMATCH` | nein | Quelle belegt die neue oder alte Aussage nicht |
| `BLOCK_FAKE_REFERENCE` | nein | Quelle, DOI, ISBN, Aktenzeichen, Urteil, Link oder Zitat wirkt fabriziert oder traegt die Aussage nicht |
| `BLOCK_UNGROUNDED_DETAIL` | nein | Neues Detail, Beispiel, Motiv, Zahl oder Ich-Erlebnis ohne Anker |

## Factual-Reliability-Gate

Konkrete Quellen sind nicht Dekoration. Eine Referenz muss existieren, formal plausibel sein und die konkrete Aussage tragen. Wenn das im aktuellen Material nicht pruefbar ist, markiere den Pruefstatus statt den Text glatter zu schreiben.

Pruefe besonders:

- DOI, ISBN, ISSN, URL, Aktenzeichen, Paragraph und Gerichtsentscheidung
- Autor-Jahr-Kombinationen und Publikationstitel
- direkte Zitate, Seitenzahlen und Zahlenangaben
- Quellen, die nur thematisch passen, aber nicht die konkrete Aussage belegen
- Tracking- oder KI-Artefakte in Links

Kein Ersatzbeleg ohne Input- oder Quellenanker. Wenn die Quelle falsch wirkt, ist die richtige Operation Markierung, Kuerzung oder Rueckfrage.

## Claim-Delta-Regel

Jede geaenderte Passage muss intern diese Frage bestehen:

1. Welche Anker standen vorher im Text?
2. Welche Anker stehen nachher im Text?
3. Ist jeder neue Anker durch Input, Quelle oder Schreibprobe gedeckt?
4. Hat sich der Autoritaetsgrad veraendert?
5. Wurde eine Luecke markiert statt gefuellt?

Wenn eine Antwort unklar ist, nicht glatter schreiben. Markieren oder Rueckfrage stellen.

## QGIR-Invarianten

Bei iterativer Revision gilt die Claim-Delta-Regel nach jedem Pass, nicht nur am Ende.

- Jeder Pass muss die vorher geschuetzten Anker erneut erhalten.
- Neue Faktenanker, Beispiele, Ursachen, Personen, Orte oder Erfahrungsdetails blocken den Loop.
- "kann", "laut", "vermutlich" und andere Qualifier duerfen nicht zu "zeigt", "beweist" oder "muss" werden.
- Eine spaetere Runde darf keine Luecke fuellen, die eine fruehere Runde korrekt markiert hat.
- Wenn Claim-Erhalt und Stilgewinn kollidieren, stoppt QGIR.
