import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fp_corpus_report.py"
BASELINE = ROOT / "tests" / "fp_corpus" / "baseline.json"

spec = importlib.util.spec_from_file_location("fp_corpus_report", SCRIPT)
fp_corpus_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fp_corpus_report)


class FalsePositiveCorpusTests(unittest.TestCase):
    def test_current_run_does_not_exceed_baseline(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        current = fp_corpus_report.build_report()

        self.assertEqual(set(baseline), set(current))

        for path, findings in baseline.items():
            self.assertGreater(sum(findings.values()), 0, f"{path} has no baseline findings")

        regressions = []
        for path, current_findings in current.items():
            baseline_findings = baseline[path]
            for kind, current_count in current_findings.items():
                baseline_count = baseline_findings.get(kind, 0)
                if current_count > baseline_count:
                    regressions.append(f"{path}: {kind} {current_count} > {baseline_count}")

            for kind, baseline_count in baseline_findings.items():
                current_count = current_findings.get(kind, 0)
                if current_count < baseline_count:
                    print(f"FP corpus improved: {path}: {kind} {current_count} < {baseline_count}")

        self.assertEqual(regressions, [])


if __name__ == "__main__":
    unittest.main()
