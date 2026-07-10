import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MAKE = shutil.which("make")


@unittest.skipUnless(MAKE, "make is not available")
class LanguageToolTargetTests(unittest.TestCase):
    def run_lt(self, path: str, filename: str = "README.md") -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PATH"] = path
        return subprocess.run(
            [MAKE, "-s", "lt", f"FILE={filename}"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def install_fake(self, directory: str, body: str) -> Path:
        executable = Path(directory) / "languagetool"
        executable.write_text("#!/bin/sh\n" + body, encoding="utf-8")
        executable.chmod(0o755)
        return executable

    def test_lt_skips_cleanly_only_when_languagetool_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_lt(directory)

        self.assertEqual(result.returncode, 0)
        self.assertIn("nicht installiert", result.stdout)

    def test_lt_propagates_languagetool_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            self.install_fake(directory, "exit 23\n")
            result = self.run_lt(directory)

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("nicht installiert", result.stdout)

    def test_lt_passes_a_spaced_filename_as_one_argument(self):
        with tempfile.TemporaryDirectory() as directory:
            self.install_fake(directory, "printf '<%s>\\n' \"$@\"\n")
            result = self.run_lt(directory, "drafts/my text.md")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.splitlines(),
            ["<-l>", "<de-DE>", "<--json>", "<drafts/my text.md>"],
        )


if __name__ == "__main__":
    unittest.main()
