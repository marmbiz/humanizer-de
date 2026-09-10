import io
import importlib.util
import json
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bench.py"


def load_bench_script():
    spec = importlib.util.spec_from_file_location("bench", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BenchScriptSmokeTests(unittest.TestCase):
    def test_synthetic_markdown_contains_apostrophe_cases(self):
        bench = load_bench_script()
        text = bench.synthetic_markdown(1)
        self.assertIn("Hans’", text)
        self.assertIn("Projekts’", text)
        self.assertIn("Mitarbeiter's", text)

    def test_bench_outputs_parseable_json_for_small_size(self):
        bench = load_bench_script()
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            exit_code = bench.main(["--sizes", "1", "--runs", "1"])

        report = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(set(report), {"unicode_lint", "rhythm_lint", "humanizer_audit"})
        for timings in report.values():
            self.assertEqual(set(timings), {"1kb"})
            self.assertIsInstance(timings["1kb"], float)

    def test_check_passes_with_matching_baseline(self):
        bench = load_bench_script()
        baseline = {name: {"1kb": 1.0} for name in ("unicode_lint", "rhythm_lint", "humanizer_audit")}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            with mock.patch.object(bench, "run_benchmarks", return_value={name: {"1kb": 0.5} for name in baseline}):
                with mock.patch("sys.stdout", io.StringIO()), mock.patch("sys.stderr", io.StringIO()):
                    self.assertEqual(bench.main(["--check", "--baseline", str(path), "--sizes", "1"]), 0)

    def test_check_fails_on_regression(self):
        bench = load_bench_script()
        baseline = {name: {"1kb": 1.0} for name in ("unicode_lint", "rhythm_lint", "humanizer_audit")}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            with mock.patch.object(bench, "run_benchmarks", return_value={name: {"1kb": 1.31} for name in baseline}):
                with mock.patch("sys.stdout", io.StringIO()), mock.patch("sys.stderr", io.StringIO()):
                    self.assertEqual(bench.main(["--check", "--baseline", str(path), "--sizes", "1"]), 1)

    def test_check_reports_missing_baseline_as_exit_two(self):
        bench = load_bench_script()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("sys.stderr", io.StringIO()):
                with self.assertRaisesRegex(SystemExit, "2"):
                    bench.main(["--check", "--baseline", str(Path(tmp) / "missing.json")])


if __name__ == "__main__":
    unittest.main()
