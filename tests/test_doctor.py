import importlib.util
import io
import json
import os
import subprocess
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
import cli_output


class DoctorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = doctor.build_report()

    def test_report_checks_base_and_optional_toolchain_without_user_text(self):
        report = self.report

        self.assertTrue(report["ok"])
        self.assertEqual(report["name"], "humanizer-de")
        self.assertEqual(report["version"], "5.7.2")
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
            "version": "5.7.2",
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

    def test_java_home_supports_windows_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            java = Path(tmp) / "bin" / "java.exe"
            java.parent.mkdir(parents=True)
            java.touch()

            with mock.patch.dict(os.environ, {"JAVA_HOME": tmp}):
                with mock.patch.object(doctor.shutil, "which", return_value=None):
                    self.assertEqual(doctor.java_binary(), str(java))

    def test_empty_hunspell_version_output_does_not_crash(self):
        version_result = subprocess.CompletedProcess(["hunspell", "--version"], 0, "", "")
        dictionary_result = subprocess.CompletedProcess(["hunspell"], 0, "", "")
        with mock.patch.object(doctor.shutil, "which", return_value="hunspell"):
            with mock.patch.object(
                doctor,
                "run_command",
                side_effect=[(version_result, None), (dictionary_result, None)],
            ):
                checks = doctor.hunspell_checks()

        self.assertEqual(checks[0]["status"], "available")
        self.assertNotIn("version", checks[0])
        self.assertEqual(checks[1]["status"], "available")

    def test_command_decoding_preserves_unrepresentable_bytes(self):
        completed = subprocess.CompletedProcess(["tool"], 0, "", "")
        with mock.patch.object(doctor.subprocess, "run", return_value=completed) as run:
            doctor.run_command(["tool"])

        self.assertEqual(run.call_args.kwargs["errors"], "backslashreplace")

    def test_human_output_escapes_for_legacy_stdout_encoding(self):
        class LegacyStdout:
            encoding = "cp1252"

        with mock.patch.object(cli_output.sys, "stdout", LegacyStdout()):
            self.assertEqual(cli_output.text_for_stdout("A\u200bB"), "A\\u200bB")

    def test_human_report_has_clear_summary(self):
        output = doctor.format_report(self.report)

        self.assertIn("Humanizer-DE Doctor", output)
        self.assertIn("Basis-Skill", output)
        self.assertIn("--precise", output)
        self.assertIn("Gesamt:", output)
        self.assertIn("keine Nutzertexte", output)


if __name__ == "__main__":
    unittest.main()
