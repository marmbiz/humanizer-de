import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "doctor.py"

spec = importlib.util.spec_from_file_location("doctor", SCRIPT)
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)


class DoctorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = doctor.build_report()

    def test_report_checks_base_and_optional_toolchain_without_user_text(self):
        report = self.report

        self.assertTrue(report["ok"])
        self.assertEqual(report["name"], "humanizer-de")
        self.assertEqual(report["version"], "5.6.0")
        self.assertEqual(report["privacy"], "No user text or content files were read.")
        ids = {item["id"] for item in report["checks"]}
        self.assertTrue(
            {
                "base_skill",
                "claude_plugin",
                "codex_plugin",
                "version_sync",
                "python",
                "spacy",
                "german_model",
                "precise",
                "hunspell",
                "hunspell_de",
                "languagetool",
                "java",
            }.issubset(ids)
        )

    def test_json_cli_is_machine_readable(self):
        stdout = io.StringIO()
        with mock.patch.object(doctor, "build_report", return_value=self.report):
            with redirect_stdout(stdout):
                exit_code = doctor.main(["--json"])

        self.assertEqual(exit_code, 0)
        report = json.loads(stdout.getvalue())
        self.assertTrue(report["ok"])

    def test_require_full_exits_one_for_partial_installation(self):
        report = {
            "name": "humanizer-de",
            "version": "5.6.0",
            "ok": True,
            "full": False,
            "summary": "base_only",
            "privacy": "No user text or content files were read.",
            "checks": [],
        }
        with mock.patch.object(doctor, "build_report", return_value=report):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(doctor.main(["--json", "--require-full"]), 1)

    def test_select_python_prefers_project_venv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            python = root / ".venv" / "bin" / "python"
            python.parent.mkdir(parents=True)
            python.touch()

            self.assertEqual(doctor.select_python(root), python)

    def test_select_python_supports_windows_project_venv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            python = root / ".venv" / "Scripts" / "python.exe"
            python.parent.mkdir(parents=True)
            python.touch()

            self.assertEqual(doctor.select_python(root), python)

    def test_human_report_has_clear_summary(self):
        output = doctor.format_report(self.report)

        self.assertIn("Humanizer-DE Doctor", output)
        self.assertIn("Basis-Skill", output)
        self.assertIn("--precise", output)
        self.assertIn("Gesamt:", output)
        self.assertIn("keine Nutzertexte", output)


if __name__ == "__main__":
    unittest.main()
