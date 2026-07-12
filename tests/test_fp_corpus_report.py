import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fp_corpus_report.py"
CORPUS_DIR = ROOT / "tests" / "fp_corpus"


class FalsePositiveCorpusReportTests(unittest.TestCase):
    def run_report(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_default_corpus_runs(self):
        proc = self.run_report()

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(json.loads(proc.stdout))

    def test_relative_repository_corpus_runs(self):
        proc = self.run_report("--corpus-dir", "tests/fp_corpus")

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("tests/fp_corpus/a_anaphoric_sie.md", json.loads(proc.stdout))

    def test_external_absolute_corpus_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus_dir = Path(tmp)
            (corpus_dir / "mini.md").write_text("Ein kurzer Text.\n", encoding="utf-8")
            proc = self.run_report("--corpus-dir", str(corpus_dir))

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), {"mini.md": {}})

    def test_empty_or_missing_corpus_fails_visibly(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus_dirs = (Path(tmp), Path(tmp) / "missing")
            for corpus_dir in corpus_dirs:
                with self.subTest(corpus_dir=corpus_dir):
                    proc = self.run_report("--corpus-dir", str(corpus_dir))

                    self.assertNotEqual(proc.returncode, 0)
                    self.assertIn("corpus directory", proc.stderr)


if __name__ == "__main__":
    unittest.main()
