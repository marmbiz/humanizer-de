# Prüfskripte: Messen, Runner, Stilprofil, Exit-Codes

Alles, was mit Python 3 lokal läuft: der Sammelcheck, die Stilkarte, der Zwei-Aufruf-Runner, das persönliche Stilprofil, die Zusatzwerkzeuge, Einzelchecks und Exit-Codes. Die Kurzfassung steht in der [README](../README.md#messen-und-audit).

## Messen und Audit

Am Anfang jedes Durchgangs steht eine Messung. Im Agenten übernimmt der Skill sie selbst. Als
Kommandozeilen-Werkzeug genügt dafür Python 3 ohne Zusatzpakete. Gemeldet werden
Preflight-Risiko, Rhythmusdaten, eine Stilkarte sowie Befunde mit Muster-Nummer und Severity.
Unten steht eine gekürzte Fassung, vollständig nennt die Ausgabe zusätzlich Modus, Datei und
alle leeren Prüfsektionen:

```text
$ python3 scripts/humanizer_audit.py --file entwurf.md --mode sachlich --format md

Preflight: risk=low, score=0, recommendation=no_rewrite_or_local_edit_only
Calibration: risk=low means no calibrated signal fired, not that the text is clean. Signal coverage is weakest for advertising, social-media and essay/thought-leadership registers, where AI patterns can pass unseen.
Rhythm: sentences=12, mean=13.5, stddev/mean=0.434, subject_initial=0.5, connectors=0
StyleProfile: words=162, nominal_style_ratio=0.0, type_token_ratio=0.772, particles=0
Findings:
unicode:
- warning pattern 43 hidden_unicode x1 spans=245:246: Remove hidden Unicode character.
- warning pattern 46 wrong_german_closing_quote x1 spans=385:386: Use U+201C after U+201E, not U+201D.
```

Sagt der Bericht `no_rewrite_or_local_edit_only`, bleibt der Text bis auf die zwei
Einzelbefunde in Ruhe. Die Calibration-Zeile erscheint bei jedem `low`-Befund und erinnert
daran, dass ein stilles Ergebnis nur „kein geeichtes Signal“ bedeutet. In Registern wie
Werbung, Social Media oder Essayistik kann dahinter auch eine Erkennungslücke stecken. Die
Ausgaben sind Verdacht, kein Urteil, und ausdrücklich keine
Autorenschaftsprüfung – wofür die Zahlen taugen und wofür nicht, steht in der README unter
[Fakten, Grenzen und Datenschutz](../README.md#fakten-grenzen-und-datenschutz).

Im JSON tragen adressierbare Befunde ein optionales Feld
`spans: [{"start": 245, "end": 246}]`. Gezählt wird in Unicode-Codepoints wie in Python,
bezogen auf den unveränderten Originaltext. `offset_unit` nennt diese Konvention
explizit. Dokumentweite Rhythmusmetriken erhalten bewusst keine erfundene Einzelposition.

Die Stilkarte gibt es auch einzeln, wenn dich nur die Messwerte interessieren und nicht der
ganze Bericht:

```bash
python3 scripts/style_profile.py --file entwurf.md --target sachlich
```

Das Ergebnis kommt als JSON und deutet nichts, sondern zählt: Satzlängen und ihre Streuung,
Nominalstil-Anteil, Type-Token-Ratio, Modalpartikeln. Mit `--target` kommt ein Delta zum
Korridor des gewählten Modus dazu, ohne `--target` bleiben es die Rohzahlen. Ein eigenes
Profil unter `.humanizer/profile.json` überschreibt die Korridore, und `--no-profile`
ignoriert es.

## Lokaler Prüfablauf

### Zwei getrennte Modellaufrufe

Der optionale Runner trennt Audit und Rewrite auch technisch. Vor dem Audit sichert er die
unveränderte Eingabe als `original.md` und erzeugt daraus `normalized.md`, das
`unicode_lint --fix --write` konservativ bereinigt. Alle folgenden Schritte einschließlich
Schutzankern und Evidence-Gate arbeiten auf dieser Fassung, und `report.json` hält den Eingriff
unter `unicode_fix` fest. Der erste, read-only Aufruf erstellt ein Ledger aus bestätigten
Kandidaten und wortgleichen Schutzankern. Bleiben bestätigte Kandidaten übrig, liefert ein
frischer zweiter Aufruf nur Ersetzungen dafür. Der Host setzt sie deterministisch ein.
Teilüberschriften, Teilsätze, verschobene Schutzanker und neue Evidence-Blocker werden abgelehnt.
Mehrfach vorkommende identische Sätze oder Überschriften adressiert das Audit-Ledger über das
1-basierte Feld `occurrence`. Lässt das Rewrite-Modell einen bestätigten Kandidaten aus, führt
`report.json` ihn unter `skipped_candidates` mit dem Grund `no_replacement`.

Voraussetzung ist eine angemeldete lokale `claude`-CLI. Das Zielverzeichnis muss leer sein:

```bash
python3 scripts/humanizer_two_pass.py \
  --file entwurf.md \
  --out-dir humanizer-lauf \
  --mode sachlich \
  --max-budget-usd 2
```

Mit installiertem spaCy und deutschem Modell aktiviert `--precise` zusätzlich die bestehenden
Fehlalarmfilter im Sammelcheck und im Evidence-Gate. Das Flag ist optional; ohne spaCy fällt der
Runner auf die unveränderten Standardprüfungen zurück und protokolliert den inaktiven Status.

Alternativ läuft derselbe Vertrag über eine angemeldete lokale Codex-CLI:

```bash
python3 scripts/humanizer_two_pass.py \
  --file entwurf.md \
  --out-dir humanizer-lauf-codex \
  --mode sachlich \
  --provider codex
```

Codex verwendet dabei seinen Standardanbieter. Lokale `config.toml`-Anpassungen werden für den
isolierten Lauf nicht geladen. Eine nicht leere globale `$CODEX_HOME/AGENTS.md` oder
`AGENTS.override.md` führt zum Abbruch, damit keine persönlichen Anweisungen Audit oder Rewrite
verändern.

Ein Modell lässt sich mit `--model` wählen. `--max-budget-usd` ist Claude vorbehalten. Codex
protokolliert seinen Tokenverbrauch stattdessen in den JSONL-Ereignissen der Call-Artefakte.
Der Rewrite-Aufruf erhält keine Schreibrechte: Nur der
Host kann bestätigte Spannen anwenden. Nur ein angenommenes Ergebnis erscheint als `result.md`.
Abgelehnte Vorschläge heißen `rejected.md`, und `report.json` nennt Schutzverletzungen oder Blocker.
`changes.diff` hält die Änderung in beiden Fällen als Unified Diff fest; bei einem Null-Edit bleibt
die Datei leer. Danach vergleicht `verify_changes.py` die ausgelieferte Fassung mit dem echten
Original. Den vollständigen Nachweis enthält `verify.json`. In `report.json` steht unter
`verification` die Kurzfassung aus Identität, Änderungsquote und Typografie-Deltas.
Ein zweiter deterministischer Sammelcheck schreibt `postflight.json`; der Hauptreport trennt
behobene, verbliebene und neu entstandene Befundklassen, ohne daraus ein neues Stil-Gate zu
machen. Evidence-Warnings bleiben ebenfalls sichtbar. `spell-report.json` warnt optional vor
neu eingeführten, Hunspell unbekannten Wörtern und meldet sich ohne Hunspell als inaktiv ab.
`normalized.md`, die Prüfberichte, Audit, Ledger, Modellantworten und Hashes bleiben zur
Nachprüfung im Zielverzeichnis.
Der Text wird an den jeweiligen Modellanbieter übertragen. Die Quellenprüfung bleibt eine
unvollständige Nebenprüfung. Die harten Gates schützen erkennbare Anker, ersetzen aber keine
fachliche Endabnahme.

### Ein Durchlauf in vier Kommandos

So sieht die Arbeit konkret aus, die Ausgaben sind gekürzt. Schritt 4 läuft mit dem geklonten Repo sofort, weil er auf einer mitgelieferten Fixture arbeitet. Die Schritte 1 bis 3 brauchen eigene Dateien an der Stelle von `entwurf.md`, `vorher.md` und `nachher.md`.

**1. Der Audit findet echte Cluster.** Ein typischer KI-Entwurf („In der heutigen digitalen Landschaft ist es entscheidend, Prozesse nahtlos zu gestalten. Unsere maßgeschneiderten Lösungen beleuchten vielschichtige Aspekte …“):

```bash
python3 scripts/humanizer_audit.py --file entwurf.md --mode sachlich
# → german_pattern: ai_marker_cluster (Muster 64), abstraction_cluster (Muster 58)
# → preflight: medium → humanizer_pass
```

**2. Text ohne kalibriertes Signal bleibt unangetastet.** Derselbe Aufruf auf einem lebendigen menschlichen Text:

```bash
# → counts: alles 0 · preflight: low → no_rewrite_or_local_edit_only
```

Das ist der Null-Edit: Die Antwort meldet „kein kalibriertes Signal; kein Rewrite angezeigt“,
nicht die unbelegbare Gesamtaussage, der Text sei sauber.

**3. Das Evidence-Gate blockt erkennbare Faktenanker-Änderungen.** Ändert eine Umformulierung „12 Prozent“ in „13 Prozent“:

```bash
python3 scripts/evidence_lint.py --before-file vorher.md --after-file nachher.md
# → blocker: removed_number ["12 Prozent"], added_number ["13 Prozent"] · Exit 1
```

Ein nicht blockierter Lauf ist keine Sachprüfung: Der Linter vergleicht erkennbare Anker und
Marker, bindet sie aber nicht vollständig an Akteure und Aussagen.

**4. `--precise` räumt dokumentierte Fehlalarme ab** (mit installiertem spaCy) – direkt auf einer mitgelieferten Fixture nachprüfbar:

```bash
python3 scripts/register_lint.py --file tests/fp_corpus/a_anaphoric_sie.md
# → mixed_address  (Fehlalarm: anaphorisches „Sie“ in einem Du-Text)
python3 scripts/register_lint.py --file tests/fp_corpus/a_anaphoric_sie.md --precise
# → keine Findings · "precise": {"requested": true, "active": true}
```

### Lokaler Schnellcheck

Für Datei-Input ist der erste deterministische Schritt ein kompakter Sammelcheck:

```bash
python3 scripts/humanizer_audit.py --file <text.md> --mode sachlich
```

Eindeutig sichere Unicode-Korrekturen lassen sich vor dem Audit atomar anwenden:

```bash
python3 scripts/humanizer_audit.py --file <text.md> --mode sachlich --fix-safe
```

Der Schalter entfernt ausschließlich die bereits von `unicode_lint --fix` abgedeckten verborgenen
Unicode-Zeichen und repariert eindeutige deutsche Schlusszeichen aus Muster 43/46. Gerade
ASCII-Anführungszeichen sowie Zahlen-, Datums- und Apostrophformate werden nicht automatisch
umgeschrieben. Symlink-Eingaben lehnt der schreibende Pfad ab; bestehende Dateirechte bleiben
beim atomaren Ersetzen erhalten.

Für Arbeitsordner mit Markdown-Entwürfen kann der neueste Stand automatisch gewählt werden:

```bash
python3 scripts/humanizer_audit.py --latest <dir> --mode sachlich --format md
```

Der Sammelcheck ruft Unicode-, Rhythmus-, Naturalness- und Register-Prüfung in einem Prozess auf und gibt eine kurze gemeinsame Befundliste aus. Konkrete Fundstellen enthalten optionale Originaltext-Spans. Frontmatter, Code-Fences und andere geschützte Markdown-Bereiche verschieben die Offsets nicht. Mit `--precise` (und installiertem spaCy) fängt der Check die dokumentierten Fehlalarm-Klassen ab und hängt die Syntax-Analyse als eigene Sektion an. Die Einzelskripte bleiben für gezielte Nachprüfung nutzbar. `scripts/rhythm_lint.py` druckt standardmäßig eine kompakte Dokumentansicht und zeigt volle Absatzdaten nur mit `--include-paragraphs`.

Der Report enthält außerdem ein Preflight-Risiko (`low`, `medium`, `high`, `insufficient_text`). Es beschreibt, ob der Text messbar zu gleichförmig wirkt: etwa durch sehr ähnliche Satzlängen, kaum kurze oder lange Sätze, wiederholte Satzanfänge, viele mechanische Übergänge oder Naturalness-Cluster. Das ist eine Qualitätsheuristik, keine Aussage zur Autorenschaft.

Bei hohem Risiko empfiehlt der Skill nach der normalen Überarbeitung einen kontrollierten Nachkamm: das **Combing-Gate**. Dabei dürfen höchstens zwei gezielte Rhythmusänderungen passieren, zum Beispiel ein kürzerer Satz, ein anderer Satzanfang oder ein besser verteilter Absatz. Neue Fakten, künstliche Ich-Signale, Füllwörter oder Satzfragmente bleiben tabu. Der Report weist ausdrücklich darauf hin, dass Textqualität, Präzision oder Lesbarkeit durch solchen Rhythmus-Feinschliff auch schlechter werden können. Auch das Combing-Gate ist kein Detektor-Bypass und garantiert keine Score-Änderung.

Weil der Sammelcheck reines JSON auf stdout liefert, lässt er sich als deterministisches Werkzeug
in eigene Pipelines und Agenten-Frameworks (etwa LangChain, CrewAI oder n8n) einhängen:

```python
import json, subprocess

def humanizer_audit(path, mode="sachlich"):
    report = subprocess.run(
        ["python3", "scripts/humanizer_audit.py", "--file", path, "--mode", mode],
        capture_output=True, text=True, check=True,
    )
    return json.loads(report.stdout)
```

Das deckt den deterministischen Audit-Teil ab. Ohne den optionalen Zwei-Aufruf-Runner laufen
Rewrite, Claim-Lock und Selbst-Audit weiterhin im LLM-Agenten.

### Persönliches Stilprofil

Wiederkehrende Stilvorlieben überleben die Session in einer optionalen Datei `.humanizer/profile.json` im Arbeitsverzeichnis. Die Datei enthält ausschließlich Korridor-Overrides im Schema von [`references/style-targets.json`](../references/style-targets.json) plus datierte Stilnotizen – niemals eigene Texte oder Textauszüge:

```json
{
  "schema_version": 1,
  "overrides": {
    "sachlich": { "particle_count": { "max": 1 } }
  },
  "notes": [
    { "date": "2026-07-06", "note": "Modalpartikel in Einleitungen beibehalten." }
  ]
}
```

`humanizer_audit.py` und `style_profile.py` legen diese Overrides automatisch über die Basis-Korridore (Override ersetzt den Korridor der Metrik komplett). Überschriebene Korridore sind im Delta-Report mit `"override": true` markiert. Mit `--profile <datei.json>` wählen beide Skripte ein anderes Profil ausdrücklich aus. Fehlt der angegebene Pfad, endet der Aufruf mit einem Fehler. Mit `--no-profile` laufen sie reproduzierbar ohne Nutzerprofil. Unbekannte Metriken oder kaputtes JSON erzeugen nur eine Warnung. Die Datei gehört in die `.gitignore` des jeweiligen Projekts, nicht ins Repository.

Gefüllt wird das Profil auf Wunsch im Abschluss-Dialog: Wenn ein Lauf wiederholt in dieselbe Richtung korrigiert wurde, fragt der Skill am Ende einmal, ob er sich die Regel merken soll – bei Zustimmung schreibt er sie ins Profil und weist beim ersten Anlegen auf den `.gitignore`-Eintrag `.humanizer/` hin. Details: [`references/user-profile.md`](../references/user-profile.md).

## Zusatzwerkzeuge installieren

- **Python 3** führt die mitgelieferten deterministischen Prüfskripte aus. Der Basis-Skill braucht
  es nicht.
- **spaCy** schaltet `--precise` frei. Empfohlen ist eine projektlokale Umgebung mit einer von
  spaCy unterstützten Python-Version. CI und die folgenden Befehle verwenden Python 3.12:

  ```bash
  # macOS/Linux
  python3.12 -m venv .venv
  .venv/bin/python -m pip install -r requirements-precise.txt

  # Windows
  py -3.12 -m venv .venv
  .venv\Scripts\python.exe -m pip install -r requirements-precise.txt
  # Alternativ in einer bereits kompatiblen Python-Umgebung:
  py -m pip install -r requirements-precise.txt
  ```

  Der Skill bevorzugt diesen `.venv`-Interpreter und ergänzt den Sammelcheck um `--precise`.
  Das vermeidet Konflikte mit systemverwaltetem Python und mit Python-Versionen, für die der
  gepinnte spaCy-Build nicht verfügbar ist. Ohne `--precise` bleibt jeder Report unverändert. Details:
  [spaCy-Dokumentation](https://spacy.io/usage/models).
- **Hunspell mit `de_DE`** warnt über `spell_lint.py`, wenn ein Rewrite neue unbekannte Wörter
  einführt. macOS: `brew install hunspell`; Debian/Ubuntu:
  `sudo apt install hunspell hunspell-de-de`. Unter Windows ist die CLI-Einrichtung aufwendiger;
  Einsteiger können sie zunächst auslassen. Details: [Hunspell](https://github.com/hunspell/hunspell).
- **LanguageTool** ist eine ausdrückliche Zweitmeinung für Maintainer. Auf macOS stellt
  `brew install languagetool` den von `make lt` erwarteten CLI-Befehl bereit. Unter Windows und
  Linux unterscheidet sich die CLI-/Java-Einrichtung. Desktop- oder Browser-App allein reichen
  dafür nicht zwingend. LanguageTool bleibt außerhalb von `verify` und CI.

Fehlt ein Werkzeug, meldet es sich mit `"available": false` oder einer Skip-Meldung ab. Nichts
davon wird zusammen mit dem Skill installiert oder automatisch aktiviert.

## Einzelchecks

Einzelchecks:

```bash
python3 scripts/doctor.py --json
python3 scripts/humanizer_audit.py --file <text.md> --mode sachlich
python3 scripts/humanizer_audit.py --file <text.md> --mode sachlich --profile <profil.json>
python3 scripts/humanizer_audit.py --latest <dir> --mode sachlich --format md
python3 scripts/unicode_lint.py --file <text.md>
python3 scripts/rhythm_lint.py --file <text.md> --scope user_text --mode sachlich
python3 scripts/rhythm_lint.py --file <text.md> --scope user_text --mode sachlich --include-paragraphs
python3 scripts/evidence_lint.py --before-file before.md --after-file after.md
python3 scripts/spell_lint.py --before-file before.md --after-file after.md
python3 scripts/register_lint.py --file <text.md> --mode formal
python3 scripts/german_pattern_lint.py --file <text.md> --mode locker
python3 scripts/run_review_eval.py tests/scenarios
python3 scripts/detection_snapshot.py
python3 scripts/syntax_lint.py --file <text.md>
```

### Detection-Snapshot und Content-CI

`python3 scripts/detection_snapshot.py` fasst die vorhandenen Golden-, Naturalness- und
Register-Fixtures mit dem tolerierten False-Positive-Korpus zusammen. Der JSON-Bericht enthält
die erwarteten, gefundenen, fehlenden und zusätzlichen Treffer sowie einen Fixture-Hash. Er ist
bewusst report-only: kein globaler Recall-/F1-Score und kein Release-Gate.

Die Workflow-Vorlage [`.github/workflows/content-audit.yml`](../.github/workflows/content-audit.yml)
führt diesen Snapshot bei passenden Pull Requests aus und auditiert geänderte Markdown-Dateien
mit `--fail-on never`. Sie lädt die JSON-Berichte als Artefakt hoch und schreibt nur die Anzahl
geprüfter Dateien in die Job-Zusammenfassung. Es gibt keine PR-Kommentare, keine Modellaufrufe
und keine Schreibberechtigung für Repository-Inhalte.

### Exit-Codes

Alle Scripts folgen der Konvention `0` = ok, `1` = Findings gemäß Fail-Schwelle bzw. Fixture-/Eval-Mismatch, `2` = Aufruffehler (falsche Argumente). Die Fail-Schwelle unterscheidet sich bewusst je Script:
`--fail-on` übersteuert die Fail-Schwelle pro Aufruf. Die Defaults bleiben unverändert. Blocker kennen nur `register_lint.py`, `evidence_lint.py` und `humanizer_audit.py`, deshalb akzeptieren allein sie `{never,blocker,any}`. Für `unicode_lint.py`, `rhythm_lint.py`, `german_pattern_lint.py` und `spell_lint.py` gilt `{never,any}`; ein `blocker` dort wäre eine Schwelle, die nie greift, und wird als Aufruffehler abgewiesen. Ohne das Flag arbeiten `syntax_lint.py` (reine Messstufe), `style_profile.py` und `run_review_eval.py`; `doctor.py` kennt stattdessen `--require-full`.

| Script | Exit `1` bei |
|---|---|
| `doctor.py` | defektem Basis-Skill; mit `--require-full` auch bei fehlendem Zusatzwerkzeug |
| `unicode_lint.py` | jedem Finding |
| `register_lint.py`, `evidence_lint.py` | nur Blockern; Warnings blocken nicht |
| `rhythm_lint.py`, `german_pattern_lint.py`, `humanizer_audit.py`, `syntax_lint.py`, `spell_lint.py` | nie; Messen ist kein Urteil, der JSON-Report ist die Schnittstelle |
| `detection_snapshot.py` | nie; der Snapshot ist ein nicht-gatender Trendbericht |
| `run_review_eval.py` und alle `--fixture`-Modi | Erwartungs-Mismatch |

Wer ein Script in CI als Gate nutzt, muss diese Semantik kennen: `german_pattern_lint.py` und `rhythm_lint.py` liefern auch mit Befunden Exit `0`; dort gehört der JSON-Report ausgewertet, nicht der Exit-Code.

### Evidence-Gate einzeln nutzen

Das ankerbasierte Evidence-Gate prüft ein Textpaar unabhängig vom Humanizing auf erkennbare
Faktenverschiebungen:

```bash
python3 scripts/evidence_lint.py --before-file before.md --after-file after.md
```

Verglichen werden Faktenanker (Zahlen, Daten, URLs, DOIs, Paragraphen, Code, Zitate, Eigennamen)
sowie dokumentweite Marker für Autoritätsgrad und Claim-Richtung. Der JSON-Report listet erkannte
Abweichungen. Ein Blocker, etwa eine neue Zahl oder ein eindeutiger Richtungswechsel, gehört
zurückgewiesen. Exit-Code 1 gilt nur bei Blockern; Warnings wie neue Eigennamen blocken nicht.
Gleichbleibende Marker können vertauschte Beziehungen, Akteure oder Negationen verdecken. Ein
grüner Report ist deshalb keine semantische oder fachliche Freigabe. Details zum Schema stehen in
[`references/evidence-ledger.md`](../references/evidence-ledger.md).

Die YAML-Szenarien in `tests/scenarios/` sind bewusst maschinenlesbare Contracts. QGIR-Szenarien prüfen zusätzlich Pass-Limits, Edit-Budget, geschützte Anker, Registerdrift und Claim-Richtungsdrift. Detector-Bezug bleibt außerhalb der Contract-Checks. Die ausführlichere Datei `tests/SCENARIOS.md` bleibt die manuelle LLM-im-Loop-Referenz.
