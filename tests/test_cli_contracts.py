import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class CliContractTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args],
            capture_output=True,
            text=True,
        )

    def test_text_linters_require_an_explicit_source(self):
        for name in ("register_lint.py", "german_pattern_lint.py", "syntax_lint.py"):
            with self.subTest(name=name):
                proc = self.run_script(name)
                self.assertEqual(proc.returncode, 2)
                self.assertIn("one of the arguments", proc.stderr)

    def test_spell_lint_requires_both_sides(self):
        no_input = self.run_script("spell_lint.py")
        before_only = self.run_script("spell_lint.py", "--before", "Alt")
        after_only = self.run_script("spell_lint.py", "--after", "Neu")

        self.assertEqual(no_input.returncode, 2)
        self.assertEqual(before_only.returncode, 2)
        self.assertEqual(after_only.returncode, 2)
        self.assertIn("--after", before_only.stderr)
        self.assertIn("--before", after_only.stderr)

    def test_fixture_linters_reject_empty_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("register_lint.py", "german_pattern_lint.py"):
                with self.subTest(name=name):
                    proc = self.run_script(name, "--fixture", tmp)
                    self.assertEqual(proc.returncode, 2)
                    self.assertIn("contains no JSON files", proc.stderr)


if __name__ == "__main__":
    unittest.main()
