import importlib.util
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
        self.assertEqual(len(files), 18)
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

    def test_qgir_detector_wording_is_not_a_contract_violation(self):
        scenario = {
            "qgir_contract": {"max_passes": 1},
            "input": "Der Text soll nicht als KI-generiert erkennbar sein und GPTZero bestehen.",
        }
        sample = {"passes": ["Der Text soll nicht als KI-generiert erkennbar sein und GPTZero bestehen."]}
        self.assertEqual([], run_review_eval.qgir_violations(scenario, sample))


if __name__ == "__main__":
    unittest.main()
