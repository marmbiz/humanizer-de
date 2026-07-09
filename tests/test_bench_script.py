import io
import importlib.util
import json
import unittest
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


if __name__ == "__main__":
    unittest.main()
