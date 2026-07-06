import importlib.util
import json
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
    def test_all_scenarios_have_required_contract_fields(self):
        files = run_review_eval.scenario_files(SCENARIOS)
        self.assertEqual(len(files), 21)
        for file_path in files:
            with self.subTest(file=file_path.name):
                scenario = run_review_eval.load_scenario(file_path)
                self.assertIn("id", scenario)
                self.assertIn("quality_risks", scenario)
                self.assertIn("output_contract", scenario)

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

    def test_check_scenario_can_skip_invariants(self):
        scenario = {
            "id": 97,
            "mode": "Sachlich",
            "input": "Die Fehlerquote sank um 12 Prozent.",
            "expected_behavior": [],
            "quality_risks": [],
            "output_contract": [],
            "sample_outputs": [
                {
                    "name": "direction flipped but skipped",
                    "text": "Die Fehlerquote stieg um 12 Prozent.",
                    "expect_violations": [],
                    "expect_violations_exact": True,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "97_skip_invariants.yaml"
            path.write_text(json.dumps(scenario), encoding="utf-8")
            result = run_review_eval.check_scenario(path, check_invariants=False)
        self.assertTrue(result["ok"])
        self.assertEqual(result["sample_results"], [])

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

    def test_qgir_detector_wording_is_not_a_contract_violation(self):
        scenario = {
            "qgir_contract": {"max_passes": 1},
            "input": "Der Text soll nicht als KI-generiert erkennbar sein und GPTZero bestehen.",
        }
        sample = {"passes": ["Der Text soll nicht als KI-generiert erkennbar sein und GPTZero bestehen."]}
        self.assertEqual([], run_review_eval.qgir_violations(scenario, sample))


if __name__ == "__main__":
    unittest.main()
