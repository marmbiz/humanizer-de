# WARP - Humanizer (Deutsch) Entwicklerleitfaden (v4.1.0)

WARP = Workflow, Architecture, References, Principles.

## Architektur

`SKILL.md` ist nicht mehr die Musterquelle. Seit v3.5 ist es ein schlanker Runtime-Router:

```text
humanizer-de/
├── SKILL.md                         # SOP, Trigger, Ablauf, Toolroutine
├── references/
│   ├── patterns.md                  # vollständiger 65-Musterkatalog
│   ├── decision-tables.md           # Overlap- und Moduslogik
│   ├── qgir.md                      # Quality-Guided Iterative Revision
│   ├── evidence-ledger.md           # Claim-Delta und Faktenanker
│   ├── register-profiles.md         # Zielprofil und Registerlogik
│   └── de-naturalness.md            # deutsche Rule Cards fuer spaete Muster
├── scripts/
│   ├── unicode_lint.py              # Muster 43/46, JSON-Report, optional --fix
│   ├── rhythm_lint.py               # Muster 4/51/54/55/61, JSON-Report
│   ├── evidence_lint.py             # Faktenanker vor/nach Rewrite
│   ├── register_lint.py             # Register-/Profil-Drift
│   ├── german_pattern_lint.py       # deutsche Marker-Cluster
│   └── run_review_eval.py           # Scenario-Contract-Invarianten
├── tests/
│   ├── test_skill_structure.py
│   ├── test_patterns_catalog.py
│   ├── test_decision_tables.py
│   ├── test_unicode_lint.py
│   ├── test_rhythm_lint.py
│   ├── test_corpus.py
│   ├── SCENARIOS.md                 # Urteils-Regressionsszenarien (LLM-im-Loop)
│   ├── scenarios/                   # maschinenlesbare Contract- und QGIR-Fixtures
│   └── corpus/
├── README.md                        # Nutzer-Dokumentation
└── tone-of-voice.txt                # optionale Stilreferenz
```

## Wartungsregeln

1. Halte `SKILL.md` unter 2.000 Tokens. Zielbereich: 900-1.400 Tokens.
2. Schreibe `SKILL.md` als SOP: direkte Wenn/Dann-Regeln, keine Muster-Enzyklopädie.
3. Ändere den Slow-Update-Block nur für stabile Ziel-, Sicherheits-, Modus- oder Verifikationsregeln.
4. Lege neue Muster oder ausführliche Beispiele in `references/patterns.md`, nicht in `SKILL.md`.
5. Pflege Overlaps in `references/decision-tables.md`, wenn Muster gegeneinander abgegrenzt werden müssen.
6. Baue deterministische Checks als Script, wenn Prompt-Regeln wiederholt fehleranfällig sind.

## Muster ändern

Wenn ein Muster geändert oder ergänzt wird:

1. `references/patterns.md` aktualisieren.
2. Kurzreferenz und Musterkörper synchron halten.
3. Bei Overlap mit bestehenden Mustern `references/decision-tables.md` aktualisieren.
4. `tests/test_patterns_catalog.py` erweitern, wenn IDs oder Pflichtmarker betroffen sind.
5. Bei neuem False-Positive-Risiko, Carve-out oder Failure-Mode ein Szenario in `tests/SCENARIOS.md` ergänzen; maschinenlesbare Invarianten zusätzlich in `tests/scenarios/` ablegen.
6. README-Version und Changelog-Abschnitt nur bei Release-relevanter Änderung nachziehen.

Keine neuen Muster in Patch-Releases verstecken. Ab v4.0.0 nutzt das Projekt eigenes SemVer ohne Fork-Suffix und trackt keine Upstream-Versionen mehr: neue Muster und neue optionale Workflow-Modi sind Minor-Bumps, Breaking-Änderungen an Ablauf oder Output-Format sind Major-Bumps.

## Unicode und Quotes

Muster 43 und 46 sind scriptgestützt:

```bash
python3 scripts/unicode_lint.py --file path/to/text.md
python3 scripts/unicode_lint.py --file path/to/text.md --fix --write
```

Fuer echten Nutzertext immer `--file` verwenden. `--text` ist nur fuer statische Smoke-Tests wie `AB` gedacht; Rohtext nie direkt in Shell-Kommandos einsetzen.

Der Linter darf versteckte Unicode-Zeichen entfernen und sichere `U+201E ... U+201D`-Paare zu `U+201E ... U+201C` korrigieren. ASCII-Quotes werden gemeldet, aber nicht automatisch in deutsche Quotes umgewandelt.

Tests müssen echte Codepoints mit `chr()`/`ord()` prüfen. Optisch ähnliche Glyphen reichen nicht.

## Rhythmus und Burstiness

Muster 4, 51, 54, 55 und 61 sind messbar unterstützt:

```bash
python3 scripts/rhythm_lint.py --file path/to/text.md
python3 scripts/rhythm_lint.py --file path/to/text.md --scope user_text --mode sachlich
python3 scripts/rhythm_lint.py --text "Kurzer Test. Noch ein Satz."
```

Der Rhythmus-Linter ist ein reines Mess-Tool. Er schreibt nichts, korrigiert nichts und meldet nur Verdachtsmomente. `--scope skill_doc` und `--mode formal` unterdruecken Stilverdachte, die fuer SOP-, Rechts-, Technik- oder Wissenschaftstexte nicht handlungsleitend sind. Bei Nutzertexten `--file` verwenden; `--text` bleibt Smoke-Tests vorbehalten.

## Claim-, Register- und Naturalness-Checks

```bash
python3 scripts/evidence_lint.py --before-file before.md --after-file after.md
python3 scripts/register_lint.py --file text.md --mode sachlich
python3 scripts/german_pattern_lint.py --file text.md --mode locker
python3 scripts/run_review_eval.py tests/scenarios --check-invariants
```

Diese Checks sind konservative Reviewer-Hilfen. Sie sollen Faktenanker, Registerbrueche und Cluster melden, aber keine Rewrite-Automatik ersetzen.

## QGIR

QGIR steht fuer Quality-Guided Iterative Revision. Es ist ein begrenzter zweiter Revisionsmodus fuer proportionale, belegtreue Qualitaetsverbesserung:

```bash
python3 scripts/run_review_eval.py tests/scenarios --check-invariants
```

QGIR-Contracts liegen in `tests/scenarios/*qgir*.yaml`. Neue QGIR-Regeln zuerst in `references/qgir.md` beschreiben und nur dann in `SKILL.md` aufnehmen, wenn sie fuer die Runtime zwingend sind.

## Verification

Vor Release:

```bash
python3 -m unittest discover -s tests
python3 scripts/unicode_lint.py --text "AB"
python3 scripts/unicode_lint.py --file SKILL.md
python3 scripts/rhythm_lint.py --text "Kurzer Test. Noch ein Satz." --scope user_text --mode sachlich
python3 scripts/evidence_lint.py --fixture tests/corpus/evidence
python3 scripts/register_lint.py --fixture tests/corpus/register
python3 scripts/german_pattern_lint.py --fixture tests/corpus/de-naturalness
python3 scripts/run_review_eval.py tests/scenarios --check-invariants
git diff --check
```

Zusätzlich manuell prüfen:

- `SKILL.md`, `README.md`, `WARP.md`, `references/patterns.md`, `references/decision-tables.md`, `.claude-plugin/plugin.json` und `.claude-plugin/marketplace.json` nennen dieselbe Version.
- `references/patterns.md` enthält exakt die Muster 1-65 ohne Lücken.
- `SKILL.md` verlinkt `references/patterns.md`, `references/decision-tables.md`, `references/qgir.md`, `references/evidence-ledger.md`, `references/register-profiles.md`, `references/de-naturalness.md`, `scripts/unicode_lint.py` und `scripts/rhythm_lint.py`.
- Die installierte Kopie unter `~/.codex/skills/humanizer-de` wird erst nach grünen Tests synchronisiert.

## Optimierung

Verbessere den Skill mit bounded edits:

1. Sammle reale Fehlfälle oder Rollout-Diffs.
2. Formuliere höchstens drei kleine Änderungen pro Runde.
3. Teste auf gehaltenen Proben: locker, sachlich, formal, quellenlastig, Unicode, Quotes.
4. Behalte eine Änderung nur, wenn False Positives, Substanzerhalt und Ausgabeformat nicht regressieren.
5. Dokumentiere verworfene Änderungen als Lessons, nicht als zusätzlichen Skill-Text.
