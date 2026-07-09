# Humanizer-de Coverage Matrix

Status: P0 source-of-truth matrix for v5.5.0.

This matrix prevents one common documentation error: treating the 66-pattern catalog as if every pattern were deterministically detected, automatically rewritten, and fully regression-tested. The project has several coverage layers with different guarantees.

## Coverage Layers

| Layer | Files | What it covers | Guarantee | What it does not cover |
|---|---|---|---|---|
| Pattern catalog | `references/patterns.md` | 66 named German AI-writing and text-quality patterns with severity, indicators, examples, and rewrite guidance | Complete catalog of the current rule vocabulary | Deterministic detection, safe auto-fix, or empirical validation for every pattern |
| Decision tables | `references/decision-tables.md` | Overlap logic, mode matrix, evidence cases, structure cases, phrase/template cases, profile conflicts | Binding short logic for common ambiguous cases | Exhaustive handling of every text genre or edge case |
| Naturalness cards | `references/de-naturalness.md` | Operational cards for patterns 54, 55, 58, 60, 63, 64, 65 plus DACH and QGIR stop notes | Practical guardrails for late-stage German naturalness work | Full readability model or complete German stylistics |
| Register profiles | `references/register-profiles.md` | Address form, distance, sentence/paragraph shape, terms, particles, punctuation, profile conflicts | Guardrails against generic looseness and profile drift | Automatic inference of every target audience |
| Evidence ledger | `references/evidence-ledger.md` | Protected factual anchors, claim-delta operations, QGIR invariants | Strong safeguard against obvious factual drift | Full semantic equivalence or source verification |
| QGIR | `references/qgir.md`, `SKILL.md` | Bounded second revision loop, pass limits, edit budget, stop rules | Process gate for proportional revision | Default full rewrite workflow |
| Unicode linter | `scripts/unicode_lint.py` | Hidden Unicode and German quote issues | Deterministic findings and conservative fixes for its scope | Style, evidence, rhythm, register |
| Rhythm linter | `scripts/rhythm_lint.py` | Suspicion metrics for patterns 4, 54, 55, 61 | Deterministic measurements and scoped suspicions | Final KI-Tell judgment; pattern 51 is deliberately not emitted |
| German pattern linter | `scripts/german_pattern_lint.py` | Cluster checks for patterns 54, 58, 63, 64, 65 | Deterministic cluster findings for selected naturalness signals | Most of the 66-pattern catalog |
| Register linter | `scripts/register_lint.py` | Mixed address, expected address blockers, modal particles, formal voice intrusion | Deterministic profile-drift warnings/blockers for its features | Full register modeling |
| Evidence linter | `scripts/evidence_lint.py` | Before/after anchor drift: numbers, dates, URLs, DOI, paragraphs, code, quotes, proper names, authority, direction | Conservative drift warnings/blockers | Full factual checking or semantic preservation |
| Scenario contracts | `tests/scenarios/`, `scripts/run_review_eval.py` | LLM-in-loop invariants for output discipline, QGIR traces, edit budget, anchors, register, detector wording | Regression checks for known failure modes | A complete benchmark of German writing quality |
| Human reviewer / LLM judgment | `SKILL.md`, scenario docs | Cluster interpretation, context, register tradeoffs, rewrite choices, subtle structure | Required for judgment-only patterns and proportional edits | Deterministic reproducibility without tests |

## Script Pattern Coverage

| Script | Primary pattern IDs | Notes |
|---|---|---|
| `unicode_lint.py` | 43, 46, 49-adjacent quote/apostrophe safeguards | Focused technical/typographic checks |
| `rhythm_lint.py` | 4, 54, 55, 61 | Returns suspicions; cluster interpretation stays outside the script |
| `german_pattern_lint.py` | 54, 58, 63, 64, 65 | Naturalness cluster checks only |
| `register_lint.py` | 63 plus register/profile drift | Pattern IDs are secondary to profile safeguards |
| `evidence_lint.py` | 11, 26, 42, 53-adjacent claim-delta risks | Detects anchor drift; does not verify external sources |
| `run_review_eval.py` | Cross-pattern scenario contracts | Tests output invariants, not free-form prose quality |

## Axis View: Check Axis x Check Level

Second view on the same coverage: which check axis is enforced at which level. Axes are equal-ranked and individually engageable; the profile axis works without any AI forensics.

| Check axis | Linter | Golden corpus | Scenario contract |
|---|---|---|---|
| Tells | `unicode_lint.py`, `rhythm_lint.py`, `german_pattern_lint.py` (selected patterns) | `unicode_patterns` / `rhythm_patterns` in `tests/corpus/*_expected.json` | `invariant_violations` in `run_review_eval.py`; exact zero-tell samples since strict mode |
| Register | `register_lint.py` | — | `register_shift` / `formal_register_break` invariants; scenario 19 |
| Rhythm | `rhythm_lint.py` (suspicions) | `style_profile_ranges` (cases 06-08) | via profile corridors (`stddev_mean_ratio`) |
| Evidence | `evidence_lint.py` (standalone before/after CLI) | — | anchor/claim invariants, QGIR contracts |
| Profile | `style_profile.py` + `references/style-targets.json` (measurement, no verdict) | `style_profile_ranges` (cases 06-08) | `style_profile_contract` (`profile_out_of_range`, `profile_required_metric_failed`); scenarios 16, 19, 20 |

## Judgment-Only Or Partly Judgment-Only Areas

These areas can be guided by rules and tests, but should not be documented as fully automated:

- Legitimate Fachsprache vs. generic buzzword prose.
- Passiv and Nominalstil in formal, legal, scientific, or technical contexts.
- Whether a transition is mechanical or genuinely improves reader guidance.
- Whether a paragraph adds substance or only sounds good.
- Whether an example, scene, anecdote, or stronger thesis is needed.
- Whether a rewrite preserves meaning beyond protected anchors.
- Whether DACH regional style is authentic for the target context.

## Allowed Coverage Claims

- "The repo contains a 66-pattern catalog."
- "The repo has deterministic linters for selected technical, rhythm, naturalness, register, and evidence risks."
- "The repo uses scenario contracts to catch known LLM-in-loop failure modes."
- "QGIR is a bounded process for proportional revision when clusters remain."

## Disallowed Coverage Claims

- "All 66 patterns are deterministically detected."
- "The tools can prove semantic equivalence."
- "The skill automatically rewrites every pattern safely."
- "Passing `make verify` proves text quality for arbitrary German inputs."
- "Detector scores are an acceptance criterion."

## Audit Priorities Derived From Coverage

1. Evidence and meaning preservation: highest risk because bad rewrites can change facts.
2. Register/profile fidelity: high risk because generic humanization can damage formal, legal, technical, or author-specific text.
3. False-positive control: high risk for Fachsprache, AI-marker vocabulary, passives, nominal style, rhythm, and DACH variants.
4. Over-rewrite prevention: high risk where naturalness work adds voice, anecdotes, examples, or looseness without input support.
5. Honest automation boundaries: required so docs and roadmap do not overstate script coverage.
