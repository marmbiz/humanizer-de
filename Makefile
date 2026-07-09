FILE ?= README.md

.PHONY: test lint eval-contracts verify bench lt

test:
	python3 -m unittest discover -s tests -v

lint:
	python3 scripts/unicode_lint.py --text "AB" > /dev/null
	python3 scripts/unicode_lint.py --file SKILL.md > /dev/null
	python3 scripts/rhythm_lint.py --text "Kurzer Test. Noch ein Satz." --scope user_text --mode sachlich > /dev/null
	python3 scripts/evidence_lint.py --fixture tests/corpus/evidence > /dev/null
	python3 scripts/register_lint.py --fixture tests/corpus/register > /dev/null
	python3 scripts/german_pattern_lint.py --fixture tests/corpus/de-naturalness > /dev/null

eval-contracts:
	python3 scripts/run_review_eval.py tests/scenarios --check-invariants > /dev/null

verify: test lint eval-contracts
	git diff --check

bench:
	python3 scripts/bench.py --check

lt:
	@command -v languagetool >/dev/null && languagetool -l de-DE --json $(FILE) || echo "languagetool nicht installiert (brew install languagetool) — übersprungen"
