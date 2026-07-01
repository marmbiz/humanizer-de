# spaCy-Proof-of-Concept

Testet, ob POS-/Dependency-/Lemma-/NER-Information via `spaCy` + `de_core_news_sm` die Präzision der bestehenden Regex-/Wortlisten-Linter messbar verbessert. Reiner Test, nicht eingebaut in den shipped Skill – siehe `docs/todo-naechste-schritte.md` (Schritt 2) und `/Users/mm/.claude/plans/noble-knitting-wadler.md` für den vollständigen Plan.

## Setup

```bash
cd research/spacy-poc
python3.13 -m venv .venv   # Python 3.14 hat noch keine spaCy-Wheels
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m spacy download de_core_news_sm
```

## Ausführen

```bash
.venv/bin/python tagset_probe.py       # Schritt 0: Label-Schema-Regression
.venv/bin/python compare.py            # Fixtures + Korpus-Vergleich, schreibt results/
```

## Ergebnis (Fixture-basiert, siehe `results/fixture_report.md` für Details)

| Messung | Precision | Recall | F1 | Erfolgskriterium erreicht? |
| --- | --- | --- | --- | --- |
| Passiv + subjektlose Fragmente (Muster 39) | 0.952 | 1.000 | 0.976 | Knapp nein – 1 False Positive auf einem geschützten Negativ-Fall (`p39_neg_05`) |
| Nomen-Verb-Verhältnis (Nominalstil) | 1.000 | 1.000 | 1.000 | Ja – trennt alle 20 Fälle korrekt |
| Lemma-Floskeln | 0.917 | 0.786 | 0.846 | Nein – mehrere verpasste Abstrakta/Marker; ein Fall (`lemma_26`) ist der erwartete, im Plan bewusst nicht adressierte Use-Mention-Fall |
| NER-Anker (Regex-Baseline) | 0.733 | 1.000 | 0.846 | Baseline |
| NER-Anker (spaCy) | 0.818 | 0.818 | 0.818 | Nein – höhere Precision als Regex, aber niedrigerer Recall (verpasst u. a. „Dalai Lama“, „Techniker Krankenkasse“ als Ganzes) |

**Bewertung:** Kein glattes "spaCy gewinnt überall". Nominalstil ist ein klarer, neuer, funktionierender Messwert. Passiv/Fragmente ist einen einzigen Fehlklassifikations-Fall von Erfolg entfernt – wahrscheinlich behebbar. Lemma-Floskeln und NER zeigen echte, informative Grenzen des kleinen Modells (`de_core_news_sm`), keine Implementierungsfehler.

## Auffälliger Korpus-Befund (siehe `results/corpus_comparison.md`)

Auf den 21 echten Blogposts liegt die Regex-Namenserkennung (`evidence_lint.py`s `proper_name`-Anker) durchgängig 3–4× höher als spaCys NER-Treffer (z. B. ein Post: 786 vs. 261 Treffer). Da im Deutschen jedes Substantiv großgeschrieben wird, ist naheliegend, dass die Regex-Heuristik auf echtem Fließtext deutlich mehr falsch-positive "Namen" zählt als das kleine, aber präzisere NER-Modell. Nicht abschließend verifiziert (keine Zeit mehr investiert) – offene Frage für eine mögliche Fortsetzung.

## Offene Punkte / nicht Teil dieses PoC

- Use-Mention (Wort in Zitat vs. Gebrauch) wird durch Lemma-Matching nicht gelöst – bestätigt durch `lemma_26`.
- Der eine Passiv/Fragment-Fehlklassifikations-Fall (`p39_neg_05`) ist nicht weiter untersucht.
- Ob die Regex-vs-spaCy-Namensdiskrepanz auf echtem Korpus ein Precision- oder ein Zählmethoden-Artefakt ist, ist offen.

## Entscheidung

Noch nicht getroffen – siehe `docs/todo-naechste-schritte.md` für den finalen Eintrag nach Review.
