import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_script(name):
    script = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


unicode_lint = load_script("unicode_lint")
register_lint = load_script("register_lint")
evidence_lint = load_script("evidence_lint")
rhythm_lint = load_script("rhythm_lint")
german_pattern_lint = load_script("german_pattern_lint")
humanizer_audit = load_script("humanizer_audit")


def run_cli(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = module.main(argv)
    return exit_code, json.loads(stdout.getvalue())


def finding_kinds(report):
    return {item["kind"] for item in report["findings"]}


class ExitCodeTests(unittest.TestCase):
    def test_unicode_lint_exits_1_for_any_finding_and_0_for_clean_text(self):
        finding_code, finding_report = run_cli(unicode_lint, ["--text", 'Er sagte "Hallo".'])
        clean_code, clean_report = run_cli(unicode_lint, ["--text", "Das Team prueft die Datei."])

        self.assertEqual(finding_code, 1)
        self.assertIn("straight_quote", finding_kinds(finding_report))
        self.assertEqual(clean_code, 0)
        self.assertEqual(clean_report["findings"], [])

    def test_register_lint_exits_1_only_for_blockers(self):
        blocker_code, blocker_report = run_cli(
            register_lint,
            ["--text", "Klingt spannend?", "--mode", "formal"],
        )
        warning_code, warning_report = run_cli(
            register_lint,
            ["--text", "Du kannst die Datei pruefen. Bitte senden Sie danach die Freigabe."],
        )
        clean_code, clean_report = run_cli(register_lint, ["--text", "Das Team prueft die Datei."])

        self.assertEqual(blocker_code, 1)
        self.assertIn("formal_voice_intrusion", finding_kinds(blocker_report))
        self.assertTrue(any(item["severity"] == "blocker" for item in blocker_report["findings"]))
        self.assertEqual(warning_code, 0)
        self.assertIn("mixed_address", finding_kinds(warning_report))
        self.assertTrue(all(item["severity"] == "warning" for item in warning_report["findings"]))
        self.assertEqual(clean_code, 0)
        self.assertEqual(clean_report["findings"], [])

    def test_evidence_lint_exits_1_only_for_blockers(self):
        blocker_code, blocker_report = run_cli(
            evidence_lint,
            [
                "--before",
                "Die Wartezeit sank laut Bericht.",
                "--after",
                "Die Wartezeit sank laut Bericht um 63 Prozent.",
            ],
        )
        warning_code, warning_report = run_cli(
            evidence_lint,
            [
                "--before",
                "Die Stadt veroeffentlichte den Bericht.",
                "--after",
                "Die Stadt Koeln veroeffentlichte den Bericht.",
            ],
        )
        clean_code, clean_report = run_cli(
            evidence_lint,
            [
                "--before",
                "Das Team prueft den Text.",
                "--after",
                "Das Team prueft den Text genau.",
            ],
        )

        self.assertEqual(blocker_code, 1)
        self.assertIn("added_number", finding_kinds(blocker_report))
        self.assertTrue(any(item["severity"] == "blocker" for item in blocker_report["findings"]))
        self.assertEqual(warning_code, 0)
        self.assertIn("added_proper_name", finding_kinds(warning_report))
        self.assertTrue(all(item["severity"] == "warning" for item in warning_report["findings"]))
        self.assertEqual(clean_code, 0)
        self.assertEqual(clean_report["findings"], [])

    def test_rhythm_lint_always_exits_0(self):
        finding_code, finding_report = run_cli(
            rhythm_lint,
            ["--text", "Zudem prueft das Team die Werte. Zudem speichert es die Notizen."],
        )
        clean_code, clean_report = run_cli(rhythm_lint, ["--text", "Kurz. Noch ein Satz."])

        self.assertEqual(finding_code, 0)
        self.assertIn("connector density", {item["reason"] for item in finding_report["suspicions"]})
        self.assertEqual(clean_code, 0)
        self.assertEqual(clean_report["suspicions"], [])

    def test_german_pattern_lint_always_exits_0(self):
        finding_code, finding_report = run_cli(
            german_pattern_lint,
            [
                "--text",
                "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.",
            ],
        )
        clean_code, clean_report = run_cli(german_pattern_lint, ["--text", "Das Team prueft die Datei."])

        self.assertEqual(finding_code, 0)
        self.assertIn("ai_marker_cluster", finding_kinds(finding_report))
        self.assertEqual(clean_code, 0)
        self.assertEqual(clean_report["findings"], [])

    def test_humanizer_audit_always_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            finding_path = Path(tmp) / "finding.md"
            clean_path = Path(tmp) / "clean.md"
            finding_path.write_text('Er sagte "Hallo".', encoding="utf-8")
            clean_path.write_text("Das Team prueft die Datei. Danach endet der Test.", encoding="utf-8")

            finding_code, finding_report = run_cli(
                humanizer_audit,
                ["--file", str(finding_path), "--no-profile"],
            )
            clean_code, clean_report = run_cli(
                humanizer_audit,
                ["--file", str(clean_path), "--no-profile"],
            )

        self.assertEqual(finding_code, 0)
        self.assertIn("straight_quote", finding_kinds(finding_report))
        self.assertFalse(finding_report["ok"])
        self.assertEqual(clean_code, 0)
        self.assertTrue(clean_report["ok"])
        self.assertEqual(clean_report["findings"], [])


if __name__ == "__main__":
    unittest.main()
