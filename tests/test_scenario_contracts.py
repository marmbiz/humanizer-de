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
        self.assertEqual(len(files), 13)
        for file_path in files:
            with self.subTest(file=file_path.name):
                scenario = run_review_eval.load_scenario(file_path)
                self.assertIn("id", scenario)
                self.assertIn("forbidden_changes", scenario)
                self.assertIn("output_contract", scenario)

    def test_sample_outputs_trigger_expected_violations(self):
        for file_path in run_review_eval.scenario_files(SCENARIOS):
            with self.subTest(file=file_path.name):
                result = run_review_eval.check_scenario(file_path)
                self.assertTrue(result["ok"], result)


if __name__ == "__main__":
    unittest.main()
