# WARP - Humanizer (Deutsch) Entwicklerleitfaden (v3.7.0-de.1)

WARP = Workflow, Architecture, References, Principles.

## Architektur

`SKILL.md` ist nicht mehr die Musterquelle. Seit v3.5 ist es ein schlanker Runtime-Router:

```text
humanizer-de/
├── SKILL.md                         # SOP, Trigger, Ablauf, Toolroutine
├── references/
│   ├── patterns.md                  # vollständiger 57-Musterkatalog
│   └── decision-tables.md           # Overlap- und Moduslogik
├── scripts/
│   └── unicode_lint.py              # Muster 43/46, JSON-Report, optional --fix
├── tests/
│   ├── test_skill_structure.py
│   ├── test_patterns_catalog.py
│   ├── test_decision_tables.py
│   └── test_unicode_lint.py
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
5. README-Version und Changelog-Abschnitt nur bei Release-relevanter Änderung nachziehen.

Keine neuen Muster in Patch-Releases verstecken. Wenn aus 57 Mustern 58 werden, ist das eine sichtbare Versionierungs- und Dokumentationsänderung.

## Unicode und Quotes

Muster 43 und 46 sind scriptgestützt:

```bash
python3 scripts/unicode_lint.py --file path/to/text.md
python3 scripts/unicode_lint.py --file path/to/text.md --fix --write
```

Fuer echten Nutzertext immer `--file` verwenden. `--text` ist nur fuer statische Smoke-Tests wie `AB` gedacht; Rohtext nie direkt in Shell-Kommandos einsetzen.

Der Linter darf versteckte Unicode-Zeichen entfernen und sichere `U+201E ... U+201D`-Paare zu `U+201E ... U+201C` korrigieren. ASCII-Quotes werden gemeldet, aber nicht automatisch in deutsche Quotes umgewandelt.

Tests müssen echte Codepoints mit `chr()`/`ord()` prüfen. Optisch ähnliche Glyphen reichen nicht.

## Verification

Vor Release:

```bash
python3 -m unittest discover -s tests
python3 scripts/unicode_lint.py --text "AB"
git diff --check
```

Zusätzlich manuell prüfen:

- `SKILL.md`, `README.md` und `WARP.md` nennen dieselbe Version.
- `references/patterns.md` enthält exakt die Muster 1-57 ohne Lücken.
- `SKILL.md` verlinkt `references/patterns.md`, `references/decision-tables.md` und `scripts/unicode_lint.py`.
- Die installierte Kopie unter `~/.codex/skills/humanizer-de` wird erst nach grünen Tests synchronisiert.

## Optimierung

Verbessere den Skill mit bounded edits:

1. Sammle reale Fehlfälle oder Rollout-Diffs.
2. Formuliere höchstens drei kleine Änderungen pro Runde.
3. Teste auf gehaltenen Proben: locker, sachlich, formal, quellenlastig, Unicode, Quotes.
4. Behalte eine Änderung nur, wenn False Positives, Substanzerhalt und Ausgabeformat nicht regressieren.
5. Dokumentiere verworfene Änderungen als Lessons, nicht als zusätzlichen Skill-Text.
