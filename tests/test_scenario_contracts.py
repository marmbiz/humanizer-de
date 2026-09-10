import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_review_eval.py"
SCENARIOS = ROOT / "tests" / "scenarios"

spec = importlib.util.spec_from_file_location("run_review_eval", SCRIPT)
run_review_eval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_review_eval)


class ScenarioContractTests(unittest.TestCase):
    def test_eval_runner_reuses_sibling_module_instances(self):
        code = (
            "import sys; "
            f"sys.path.insert(0, {str(ROOT / 'scripts')!r}); "
            "import run_review_eval as runner; "
            "assert runner.evidence_lint is sys.modules['evidence_lint']; "
            "assert runner.register_lint is sys.modules['register_lint']; "
            "assert runner.rhythm_lint is sys.modules['rhythm_lint']; "
            "assert runner.style_profile.register_lint is runner.register_lint"
        )
        completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def assert_scenario_usage_error(self, scenario: dict, message: str) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "invalid.json"
            path.write_text(json.dumps(scenario), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
            )

        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("error:", proc.stderr)
        self.assertIn(message, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_all_scenarios_have_required_contract_fields(self):
        files = run_review_eval.scenario_files(SCENARIOS)
        self.assertEqual(len(files), 29)
        for file_path in files:
            with self.subTest(file=file_path.name):
                scenario = run_review_eval.load_scenario(file_path)
                self.assertIn("id", scenario)
                self.assertIn("quality_risks", scenario)
                self.assertIn("output_contract", scenario)

    def test_documented_scenario_ids_match_contract_matrix(self):
        docs = (ROOT / "tests" / "SCENARIOS.md").read_text(encoding="utf-8")
        matrix = docs.split("## Coverage-Matrix", 1)[1].split("Die Szenarien 14 bis 18", 1)[0]
        documented_matrix_ids = {int(value) for value in re.findall(r"\|\s*(\d+)\s*\|", matrix)}
        contract_ids = {
            run_review_eval.load_scenario(path)["id"]
            for path in run_review_eval.scenario_files(SCENARIOS)
        } - set(range(14, 19))
        heading_ids = {int(value) for value in re.findall(r"(?m)^## Szenario (\d+):", docs)}
        self.assertEqual(documented_matrix_ids, contract_ids)
        self.assertEqual(heading_ids, contract_ids)

    def test_qgir_scenarios_have_quality_contracts(self):
        qgir_files = [file_path for file_path in run_review_eval.scenario_files(SCENARIOS) if "qgir" in file_path.name]
        self.assertEqual(len(qgir_files), 5)
        for file_path in qgir_files:
            with self.subTest(file=file_path.name):
                scenario = run_review_eval.load_scenario(file_path)
                contract = scenario.get("qgir_contract")
                self.assertIsInstance(contract, dict)
                self.assertIn("max_passes", contract)

    def test_sample_outputs_trigger_expected_violations(self):
        for file_path in run_review_eval.scenario_files(SCENARIOS):
            with self.subTest(file=file_path.name):
                result = run_review_eval.check_scenario(file_path)
                self.assertTrue(result["ok"], result)

    def test_qgir_rejects_missing_or_malformed_pass_trace(self):
        scenario = {
            "qgir_contract": {"max_passes": 2},
            "input": "Die API liefert Status 200.",
        }
        self.assertIn(
            "qgir_missing_pass_trace",
            run_review_eval.qgir_violations(scenario, {"text": "Die API liefert Status 200."}),
        )
        self.assertIn(
            "qgir_missing_pass_trace",
            run_review_eval.qgir_violations(scenario, {"passes": "Die API liefert Status 200."}),
        )

    def test_qgir_edit_budget_counts_additive_expansion(self):
        before = "Die API liefert Status 200. Clients prüfen `items`."
        after = (
            "Die API liefert Status 200. Clients prüfen `items`. "
            "Zusätzlich erklärt der Text ausführlich die Motivation, die Zielgruppe, die Architektur "
            "und mehrere hypothetische Vorteile, die im Ausgangstext nicht belegt sind."
        )
        self.assertGreater(run_review_eval.changed_sentence_ratio(before, after), 0.35)

    def test_qgir_checks_every_pass_against_original(self):
        scenario = {
            "mode": "Sachlich",
            "input": "Die Fehlerquote liegt laut Bericht bei 12 Prozent.",
            "qgir_contract": {
                "max_passes": 2,
                "protected_anchors": ["12 Prozent"],
            },
        }
        sample = {
            "passes": [
                "Die Fehlerquote liegt laut Bericht bei 12 Prozent; zusätzlich werden 30 Prozent genannt.",
                "Laut Bericht liegt die Fehlerquote weiterhin bei 12 Prozent.",
            ]
        }

        violations = run_review_eval.qgir_violations(scenario, sample)

        self.assertIn("new_factual_anchor", violations)
        self.assertNotIn("full_text_output", violations)

    def test_qgir_checks_protected_anchors_and_register_on_intermediate_passes(self):
        scenario = {
            "mode": "Sachlich",
            "input": "Sie erhalten die Freigabe am Freitag.",
            "qgir_contract": {
                "max_passes": 2,
                "protected_anchors": ["Freitag"],
                "required_address": "Sie",
            },
        }
        sample = {
            "passes": [
                "Du erhältst die Freigabe bald.",
                "Sie erhalten die Freigabe am Freitag.",
            ]
        }

        violations = run_review_eval.qgir_violations(scenario, sample)

        self.assertIn("missing_protected_anchor", violations)
        self.assertIn("register_shift", violations)

    def test_qgir_checks_authoritative_text_alongside_pass_trace(self):
        scenario = {
            "mode": "Sachlich",
            "input": "Sie erhalten die Freigabe am Freitag.",
            "qgir_contract": {
                "max_passes": 2,
                "max_changed_sentence_ratio": 0.2,
                "protected_anchors": ["Freitag"],
                "required_address": "Sie",
            },
        }
        sample = {
            "passes": ["Sie erhalten die Freigabe am Freitag."],
            "text": "Du erhältst die Freigabe bald.",
        }

        violations = run_review_eval.qgir_violations(scenario, sample)

        self.assertIn("missing_protected_anchor", violations)
        self.assertIn("register_shift", violations)
        self.assertIn("edit_budget_exceeded", violations)

    def test_strict_mode_fails_on_unexpected_violation(self):
        scenario = {
            "id": 99, "mode": "Sachlich",
            "input": "Die Fehlerquote sank um 12 Prozent.",
            "expected_behavior": [], "quality_risks": [], "output_contract": [],
            "sample_outputs": [],
        }
        sample_output = "Die Fehlerquote stieg um 12 Prozent."
        violations = run_review_eval.invariant_violations(scenario, sample_output)
        self.assertIn("claim_direction_changed", violations)
        self.assertNotEqual(set(), set(violations))

    def test_machine_output_rejects_branding_prelude(self):
        scenario = {
            "id": 99,
            "mode": "Sachlich",
            "machine_output": True,
            "input": "Die API liefert Status 200.",
            "expected_behavior": [],
            "quality_risks": [],
            "output_contract": [],
            "sample_outputs": [],
        }
        output = 'Less machine. More voice.\n{"ok": true, "findings": []}'
        self.assertIn("branding_prelude_in_machine_output", run_review_eval.invariant_violations(scenario, output))

        without_machine_output = dict(scenario)
        without_machine_output.pop("machine_output")
        self.assertNotIn(
            "branding_prelude_in_machine_output",
            run_review_eval.invariant_violations(without_machine_output, output),
        )

    def test_check_scenario_exact_expectation_mismatch_fails(self):
        scenario = {
            "id": 98,
            "mode": "Sachlich",
            "input": "Die Fehlerquote sank um 12 Prozent.",
            "expected_behavior": [],
            "quality_risks": [],
            "output_contract": [],
            "sample_outputs": [
                {
                    "name": "direction flipped but expected clean",
                    "text": "Die Fehlerquote stieg um 12 Prozent.",
                    "expect_violations": [],
                    "expect_violations_exact": True,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "98_exact_mismatch.yaml"
            path.write_text(json.dumps(scenario), encoding="utf-8")
            result = run_review_eval.check_scenario(path)
        self.assertFalse(result["ok"])
        self.assertFalse(result["sample_results"][0]["ok"])
        self.assertIn("claim_direction_changed", result["sample_results"][0]["actual"])

    def test_scenario_without_samples_is_rejected(self):
        scenario = {
            "id": 96,
            "mode": "Sachlich",
            "input": "Ein Satz.",
            "expected_behavior": [],
            "quality_risks": [],
            "output_contract": [],
            "sample_outputs": [],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "96_empty.yaml"
            path.write_text(json.dumps(scenario), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-empty"):
                run_review_eval.check_scenario(path)

    def test_null_edit_contract_accepts_unchanged_and_rejects_polish(self):
        scenario = {
            "input": "Der Dienst speichert die Datei lokal.",
            "null_edit_contract": {"require_unchanged": True},
        }

        self.assertEqual(
            run_review_eval.null_edit_violations(
                scenario,
                "Der Dienst speichert die Datei lokal.",
            ),
            [],
        )
        self.assertEqual(
            run_review_eval.null_edit_violations(
                scenario,
                "Der Dienst speichert die Datei zuverlässig lokal.",
            ),
            ["unnecessary_edit"],
        )
        self.assertEqual(
            run_review_eval.null_edit_violations(
                scenario,
                "Der Dienst speichert die Datei lokal.\n",
            ),
            ["unnecessary_edit"],
        )
        self.assertIn(
            "full_text_output",
            run_review_eval.invariant_violations(
                {"input": scenario["input"], "null_edit_contract": {"require_unchanged": False}},
                scenario["input"],
            ),
        )

    def test_missing_and_empty_scenario_paths_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty = Path(tmp_dir) / "empty"
            empty.mkdir()
            missing = Path(tmp_dir) / "missing"
            with self.assertRaisesRegex(ValueError, "no scenario files"):
                run_review_eval.scenario_files(empty)
            with self.assertRaisesRegex(ValueError, "does not exist"):
                run_review_eval.scenario_files(missing)

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(empty)],
                capture_output=True,
                text=True,
            )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("no scenario files found", proc.stderr)

    def test_style_profile_contract_flags_out_of_range_and_required_metric(self):
        scenario = {
            "style_profile_contract": {
                "target": "sachlich",
                "max_out_of_range": 1,
                "required_in_range": ["particle_count"],
            },
            "input": "Der Bericht liegt vor.",
        }
        sample = {"text": "Das ist ja irgendwie ein Thema. Das ist halt eben doch ein Thema."}
        violations = run_review_eval.style_profile_violations(scenario, sample)
        self.assertIn("profile_out_of_range", violations)
        self.assertIn("profile_required_metric_failed", violations)

    def test_style_profile_contract_respects_out_of_range_budget(self):
        scenario = {
            "style_profile_contract": {"target": "sachlich", "max_out_of_range": 3},
            "input": "Der Bericht liegt vor.",
        }
        sample = {"text": "Das ist ja irgendwie ein Thema. Das ist halt eben doch ein Thema."}
        self.assertEqual([], run_review_eval.style_profile_violations(scenario, sample))

    def test_style_profile_contract_absent_yields_no_violations(self):
        scenario = {"input": "Der Bericht liegt vor."}
        sample = {"text": "Das ist ja halt so."}
        self.assertEqual([], run_review_eval.style_profile_violations(scenario, sample))

    def test_unknown_style_target_is_usage_error(self):
        scenario = {
            "id": 99,
            "mode": "Sachlich",
            "input": "Der Bericht liegt vor.",
            "expected_behavior": [],
            "quality_risks": [],
            "output_contract": [],
            "sample_outputs": [{"text": "Der Bericht liegt vor."}],
            "style_profile_contract": {"target": "unbekannt"},
        }
        self.assert_scenario_usage_error(scenario, "unknown style target")

    def test_contract_metric_without_corridor_is_usage_error(self):
        scenario = {
            "id": 99,
            "mode": "Sachlich",
            "input": "Der Bericht liegt vor.",
            "expected_behavior": [],
            "quality_risks": [],
            "output_contract": [],
            "sample_outputs": [{"text": "Der Bericht liegt vor."}],
            "style_profile_contract": {
                "target": "sachlich",
                "required_in_range": ["connector_density"],
            },
        }
        self.assert_scenario_usage_error(scenario, "has no corridor")

    def test_qgir_detector_wording_is_not_a_contract_violation(self):
        scenario = {
            "qgir_contract": {"max_passes": 1},
            "input": "Der Text soll nicht als KI-generiert erkennbar sein und GPTZero bestehen.",
        }
        sample = {"passes": ["Der Text soll nicht als KI-generiert erkennbar sein und GPTZero bestehen."]}
        self.assertEqual([], run_review_eval.qgir_violations(scenario, sample))


if __name__ == "__main__":
    unittest.main()
