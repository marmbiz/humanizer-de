FILE ?= README.md
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: test lint eval-contracts verify bench doctor doctor-full lt

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) scripts/unicode_lint.py --text "AB" > /dev/null
	$(PYTHON) scripts/unicode_lint.py --file SKILL.md > /dev/null
	$(PYTHON) scripts/rhythm_lint.py --text "Kurzer Test. Noch ein Satz." --scope user_text --mode sachlich > /dev/null
	$(PYTHON) scripts/evidence_lint.py --fixture tests/corpus/evidence > /dev/null
	$(PYTHON) scripts/register_lint.py --fixture tests/corpus/register > /dev/null
	$(PYTHON) scripts/german_pattern_lint.py --fixture tests/corpus/de-naturalness > /dev/null

eval-contracts:
	$(PYTHON) scripts/run_review_eval.py tests/scenarios --check-invariants > /dev/null

verify: test lint eval-contracts
	git diff --check

bench:
	python3 scripts/bench.py --check

doctor:
	$(PYTHON) scripts/doctor.py

doctor-full:
	$(PYTHON) scripts/doctor.py --require-full

lt:
	@if ! command -v languagetool >/dev/null; then \
		echo "languagetool nicht installiert — optional; siehe README — übersprungen"; \
		exit 0; \
	fi; \
	languagetool -l de-DE --json "$(FILE)"
