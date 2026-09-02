# WARP - Humanizer (Deutsch) Entwicklerleitfaden (v5.26.0)

WARP = Workflow, Architecture, References, Principles.

## Architektur

`SKILL.md` ist nicht mehr die Musterquelle. Seit v3.5 ist es ein schlanker Runtime-Router.
Der folgende Baum zeigt die zentralen Dateien, nicht den vollständigen Repository-Inhalt:

```text
humanizer-de/
├── SKILL.md                         # SOP, Trigger, Ablauf, Toolroutine
├── references/
│   ├── patterns.md                  # vollständiger 72-Musterkatalog
│   ├── decision-tables.md           # Overlap- und Moduslogik
│   ├── qgir.md                      # Quality-Guided Iterative Revision
│   ├── evidence-ledger.md           # Claim-Delta und Faktenanker
│   ├── register-profiles.md         # Zielprofil und Registerlogik
│   └── de-naturalness.md            # deutsche Rule Cards für späte Muster
├── scripts/
│   ├── unicode_lint.py              # Muster 43/46, JSON-Report, optional --fix
│   ├── rhythm_lint.py               # Muster 4/54/55/61, JSON-Report
│   ├── evidence_lint.py             # Faktenanker vor/nach Rewrite
│   ├── humanizer_two_pass.py        # getrenntes Audit und begrenzter Rewrite
│   ├── detection_snapshot.py        # report-only Stand der Fixture- und FP-Befunde
│   ├── register_lint.py             # Register-/Profil-Drift
│   ├── german_pattern_lint.py       # deutsche Marker-Cluster
│   ├── run_review_eval.py           # Scenario-Contract-Invarianten
│   ├── bench.py                     # deterministische CPU-Benchmarks der Linter
│   ├── build_skill_bundle.py        # uploadbares Skill-Bundle als ZIP bauen
│   ├── cli_output.py                # Modul: Datei-Leser, JSON-Ausgabe, Exit-Code-Policy (kein CLI)
│   ├── doctor.py                    # lokale Humanizer-Installation diagnostizieren
│   ├── fp_corpus_report.py          # False-Positive-Korpus nach Datei und Fundart auswerten
│   ├── humanizer_audit.py           # kompakten Humanizer-Lint-Audit ausführen
│   ├── spell_lint.py                # neue unbekannte Hunspell-Wörter vor/nach Rewrite prüfen
│   ├── style_profile.py             # rohe Stilmetriken ohne Interpretation ausgeben
│   ├── syntax_lint.py               # optionale spaCy-Syntaxmetriken ausgeben
│   ├── text_scope.py                # Modul für offsettreue Markdown-Textbereiche (kein CLI)
│   └── verify_changes.py            # Änderungsnachweis zwischen Original und gelieferter Fassung
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
└── README.md                        # Nutzer-Dokumentation
```

## Wartungsregeln

1. Halte `SKILL.md` bei höchstens 2.300 Wörtern. Neue Zusätze brauchen einen Tausch oder eine bewusst dokumentierte Anhebung.
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
python3 scripts/humanizer_audit.py --file path/to/text.md --fix-safe
```

Für echten Nutzertext immer `--file` verwenden. `--text` ist nur für statische Smoke-Tests wie `AB` gedacht; Rohtext nie direkt in Shell-Kommandos einsetzen.

Der Linter darf versteckte Unicode-Zeichen entfernen, sichere `U+201E ... U+201D`-Paare zu `U+201E ... U+201C` korrigieren und ASCII-Schlusszeichen nach deutschem Öffner (`U+201E`/`U+201A`) zu `U+201C`/`U+2018` umschreiben. Freistehende ASCII-Quotes ohne deutschen Öffner werden nur gemeldet, nicht automatisch umgewandelt.
`humanizer_audit.py --fix-safe` macht ausschließlich diese bestehenden Korrekturen und prüft
anschließend die gespeicherte Fassung. Zahlen-, Datums- und Apostrophformate bleiben manuell.

Tests müssen echte Codepoints mit `chr()`/`ord()` prüfen. Optisch ähnliche Glyphen reichen nicht.

## Rhythmus und Burstiness

Muster 4, 54, 55 und 61 sind messbar unterstützt (Muster 51 liefert seit dem Validitätsbefund keinen Verdacht mehr, nur Messwerte):

```bash
python3 scripts/rhythm_lint.py --file path/to/text.md
python3 scripts/rhythm_lint.py --file path/to/text.md --scope user_text --mode sachlich
python3 scripts/rhythm_lint.py --text "Kurzer Test. Noch ein Satz."
```

Der Rhythmus-Linter ist ein reines Mess-Tool. Er schreibt nichts, korrigiert nichts und meldet nur Verdachtsmomente. `--scope skill_doc` und `--mode formal` unterdrücken Stilverdachte, die für SOP-, Rechts-, Technik- oder Wissenschaftstexte nicht handlungsleitend sind. Bei Nutzertexten `--file` verwenden; `--text` bleibt Smoke-Tests vorbehalten.

## Claim-, Register- und Naturalness-Checks

```bash
python3 scripts/evidence_lint.py --before-file before.md --after-file after.md
python3 scripts/register_lint.py --file text.md --mode sachlich
python3 scripts/german_pattern_lint.py --file text.md --mode locker
python3 scripts/run_review_eval.py tests/scenarios
```

Diese Checks sind konservative Reviewer-Hilfen. Sie sollen Faktenanker, Registerbrüche und Cluster melden, aber keine Rewrite-Automatik ersetzen.

## QGIR

QGIR steht für Quality-Guided Iterative Revision. Es ist ein begrenzter zweiter Revisionsmodus für proportionale, belegtreue Qualitätsverbesserung:

```bash
python3 scripts/run_review_eval.py tests/scenarios
```

QGIR-Contracts liegen in `tests/scenarios/*qgir*.yaml`. Neue QGIR-Regeln zuerst in `references/qgir.md` beschreiben und nur dann in `SKILL.md` aufnehmen, wenn sie für die Runtime zwingend sind.

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
git diff --check
```

Zusätzlich manuell prüfen:

- `SKILL.md`, `README.md`, `WARP.md`, `references/patterns.md`, `references/decision-tables.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` und `agents/openai.yaml` bleiben synchron.
- `references/patterns.md` enthält exakt die Muster 1-72 ohne Lücken.
- `SKILL.md` verlinkt `references/patterns.md`, `references/decision-tables.md`, `references/qgir.md`, `references/evidence-ledger.md`, `references/register-profiles.md`, `references/de-naturalness.md`, `scripts/unicode_lint.py` und `scripts/rhythm_lint.py`.
- Die installierte Kopie unter `~/.agents/skills/humanizer-de` oder dem lokalen Legacy-Pfad `~/.codex/skills/humanizer-de` wird erst nach grünen Tests synchronisiert.

## Release-Prozess

Der README-Abschnitt „Was ist neu?“ trägt nur den Eintrag der aktuellen Version; alle früheren Einträge stehen in `CHANGELOG.md`. GitHub Releases sind die öffentlichen Meilensteine für installierbare oder sichtbare Versionen.

Bei jedem Version-Bump:

1. Version und Changelog synchronisieren: `SKILL.md`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `references/patterns.md`, `references/decision-tables.md`, `docs/coverage-matrix.md`, `README.md`, `WARP.md`, `CITATION.cff`, `tests/test_skill_structure.py` und `tests/test_doctor.py`. Dabei wandert der bisherige README-Eintrag aus „Was ist neu?“ nach oben in `CHANGELOG.md`; der neue Eintrag ersetzt ihn im README. `.claude-plugin/marketplace.json` trägt bewusst kein `version`-Feld; `assets/checkliste-ki-tells.md` synchronisiert die Musterzahl, nicht die Version.
2. `make verify` ausführen.
3. Änderungen auf `main` bringen (direkter Push oder Pull Request) und den CI-Lauf auf `main` mit `gh run list` prüfen.
4. Erst nach grüner CI Tag `vX.Y.Z` auf den neuesten Commit setzen und pushen.
5. `make skill-bundle` ausführen und das GitHub Release aus dem Tag mit `dist/humanizer-de.zip` als Asset erstellen – Releases sind nach dem Anlegen versiegelt, das Asset muss beim `gh release create` dabei sein. Release Notes sollen die Changelog-Zeile konkretisieren, aber keinen breiteren Scope behaupten.

Patch-Releases ohne Nutzerwirkung dürfen nur im Changelog stehen. Minor-/Major-Releases und sichtbare Tool-, Skill- oder Workflow-Änderungen bekommen immer Git-Tag und GitHub Release.

Ausnahme dokumentiert: `v5.22.0` hat bewusst kein eigenes GitHub Release – der Stand ging im `v5.22.1`-Release auf, das auch das Skill-Bundle nachlieferte.

## Optimierung

Verbessere den Skill mit bounded edits:

1. Sammle reale Fehlfälle oder Rollout-Diffs.
2. Formuliere höchstens drei kleine Änderungen pro Runde.
3. Teste auf gehaltenen Proben: locker, sachlich, formal, quellenlastig, Unicode, Quotes.
4. Behalte eine Änderung nur, wenn False Positives, Substanzerhalt und Ausgabeformat nicht regressieren.
5. Dokumentiere verworfene Änderungen als Lessons, nicht als zusätzlichen Skill-Text.
