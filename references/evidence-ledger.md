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

## Maschinenlesbarer Report

`scripts/evidence_lint.py` prueft ein Before/After-Paar automatisch gegen diese Ledger-Regeln und schreibt einen JSON-Report auf stdout.

Aufrufmodi:

- `--before "<text>" --after "<text>"` — Passagen direkt als Argument
- `--before-file <datei> --after-file <datei>` — Passagen aus Dateien (Datei-Paar-Modus)
- `--write-ledger <datei>` — Original-Anker aus `--before`/`--before-file` als Ledger schreiben
- `--ledger <datei>` — `--after`/`--after-file` gegen ein Original-Ledger pruefen
- `--fixture <datei-oder-verzeichnis>` — JSON-Fixtures mit `before`, `after` und optional `expect_kinds`

## Ledger-Modus

Der Ledger-Modus schuetzt QGIR gegen kumulativen Drift: Vor Pass 1 wird aus dem Original ein
Anker-Ledger geschrieben; nach jedem Pass wird der aktuelle Text gegen dieses Original-Ledger
geprueft, nicht nur gegen den direkten Vorpass.

Schema:

```json
{
  "schema_version": 2,
  "extraction_policy": {
    "mode": "default"
  },
  "anchors": {
    "number": ["12 Prozent"],
    "date": [],
    "url": [],
    "doi": [],
    "paragraph": [],
    "code": [],
    "quote": [],
    "proper_name": []
  }
}
```

Neue Ledger enthalten die tatsaechlich verwendete Extraktions-Policy. Bei aktivem spaCy-Filter
stehen dort zusaetzlich Modellname und Modellversion. Der Diff-Lauf bricht mit Exit 2 ab, wenn
seine Policy nicht zur gespeicherten Policy passt. Ledger mit Schema 1 bleiben lesbar; weil ihnen
diese Metadaten fehlen, wird ihre Policy im Report als `legacy_unknown` ausgewiesen.

Vor Pass 1:

```bash
python3 scripts/evidence_lint.py --before-file /tmp/qgir-original.txt --write-ledger /tmp/qgir-ledger.json
```

Nach jedem Pass:

```bash
python3 scripts/evidence_lint.py --ledger /tmp/qgir-ledger.json --after-file /tmp/qgir-pass.txt
```

Mit `--precise` wirkt der spaCy-Filter im Write-Modus auf die Before-Anker im Ledger und im
Ledger-Diff nur auf die After-Anker. Das Ledger selbst bleibt die Original-Quelle. Deshalb muss
`--precise` fuer beide Laeufe unter derselben Modellversion tatsaechlich aktiv sein; ein lautloser
Fallback auf die Default-Policy wird nicht mit einem spaCy-Ledger verglichen.

Report im Paar-Modus:

```json
{
  "ok": false,
  "findings": [
    {"severity": "blocker", "kind": "added_number", "message": "New number anchor introduced.", "values": ["63 Prozent"]}
  ]
}
```

`ok` ist nur `true`, wenn gar keine Findings vorliegen. Der Exit-Code haengt allein an Blockern.

Finding-Kinds:

- `removed_<anker>` / `added_<anker>` — Anker verschwunden bzw. neu eingefuehrt. Anker-Arten: `number`, `date`, `url`, `doi`, `paragraph`, `code`, `quote` (jeweils Blocker) sowie `proper_name` (Warning).
- `authority_strengthened` (Blocker) — starker Autoritaetsmarker (z. B. "belegt", "muss") neu im After.
- `hedge_removed` (Warning) — Hedge (z. B. "kann", "vermutlich") entfernt, waehrend starke Marker im After stehen.
- `claim_direction_changed` (Blocker) — Aussagerichtung kippt zwischen Zunahme und Abnahme.

Severity und Exit-Codes:

- `blocker` = Verstoss gegen die Ledger-Regeln oben; `warning` = manuell pruefen, blockt nicht automatisch.
- Paar-Modus: Exit 1 nur, wenn mindestens ein Finding `severity = blocker` hat. Nur Warnings → Exit 0.
- Fixture-Modus: Report `{"ok": ..., "results": [{"fixture": ..., "ok": ..., "findings": [...]}]}`; Exit 1, wenn eine Fixture-Erwartung (`expect_kinds`) nicht getroffen wird — unabhaengig von der Severity.

## QGIR-Invarianten

Bei iterativer Revision gilt die Claim-Delta-Regel nach jedem Pass, nicht nur am Ende.

- Jeder Pass muss die vorher geschuetzten Anker erneut erhalten.
- Neue Faktenanker, Beispiele, Ursachen, Personen, Orte oder Erfahrungsdetails blocken den Loop.
- "kann", "laut", "vermutlich" und andere Qualifier duerfen nicht zu "zeigt", "beweist" oder "muss" werden.
- Eine spaetere Runde darf keine Luecke fuellen, die eine fruehere Runde korrekt markiert hat.
- Wenn Claim-Erhalt und Stilgewinn kollidieren, stoppt QGIR.
