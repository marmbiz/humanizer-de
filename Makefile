FILE ?= README.md
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
LANGUAGETOOL ?= languagetool

.PHONY: test help lint eval-contracts verify bench detection-snapshot doctor doctor-full lt skill-bundle

test:
	$(PYTHON) -m unittest discover -s tests -v

help:
	@echo 'test                Alle Unit-Tests ausführen'
	@echo 'help                Diese Target-Übersicht anzeigen'
	@echo 'lint                Linter-Smoke-Tests ausführen'
	@echo 'eval-contracts      Review-Szenarien prüfen'
	@echo 'verify              Tests, Linter, Szenarien und Diff prüfen'
	@echo 'skill-bundle        Uploadbares Skill-Bundle bauen'
	@echo 'bench               CPU-Benchmarks gegen die Baseline prüfen'
	@echo 'detection-snapshot  Erkennungsstand der Fixtures und FP-Befunde ausgeben'
	@echo 'doctor              Lokale Humanizer-Installation prüfen'
	@echo 'doctor-full         Installation samt optionalen Werkzeugen prüfen'
	@echo 'lt                  Datei optional mit LanguageTool prüfen'

lint:
	$(PYTHON) scripts/unicode_lint.py --text "AB" > /dev/null
	$(PYTHON) scripts/unicode_lint.py --file SKILL.md > /dev/null
	$(PYTHON) scripts/rhythm_lint.py --text "Kurzer Test. Noch ein Satz." --scope user_text --mode sachlich > /dev/null
	$(PYTHON) scripts/evidence_lint.py --fixture tests/corpus/evidence > /dev/null
	$(PYTHON) scripts/register_lint.py --fixture tests/corpus/register > /dev/null
	$(PYTHON) scripts/german_pattern_lint.py --fixture tests/corpus/de-naturalness > /dev/null

eval-contracts:
	$(PYTHON) scripts/run_review_eval.py tests/scenarios > /dev/null

verify: test lint eval-contracts
	git diff --check

skill-bundle:
	$(PYTHON) scripts/build_skill_bundle.py

bench:
	$(PYTHON) scripts/bench.py --check

detection-snapshot:
	$(PYTHON) scripts/detection_snapshot.py

doctor:
	$(PYTHON) scripts/doctor.py

doctor-full:
	$(PYTHON) scripts/doctor.py --require-full

lt:
	@if ! command -v "$(LANGUAGETOOL)" >/dev/null; then \
		echo "languagetool nicht installiert — optional; siehe README — übersprungen"; \
		exit 0; \
	fi; \
	"$(LANGUAGETOOL)" -l de-DE --json "$(FILE)"
