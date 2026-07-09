import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


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
spell_lint = load_script("spell_lint")


def hunspell_de_available():
    return spell_lint.availability_reason() is None


HUNSPELL_DE_AVAILABLE = hunspell_de_available()


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

    def test_unicode_lint_fail_on_never_exits_0_for_finding(self):
        code, report = run_cli(unicode_lint, ["--text", 'Er sagte "Hallo".', "--fail-on", "never"])

        self.assertEqual(code, 0)
        self.assertIn("straight_quote", finding_kinds(report))

    def test_unicode_lint_fail_on_blocker_exits_0_without_blocker_severity(self):
        code, report = run_cli(unicode_lint, ["--text", 'Er sagte "Hallo".', "--fail-on", "blocker"])

        self.assertEqual(code, 0)
        self.assertIn("straight_quote", finding_kinds(report))

    def test_unicode_lint_fail_on_any_exits_1_for_finding(self):
        code, report = run_cli(unicode_lint, ["--text", 'Er sagte "Hallo".', "--fail-on", "any"])

        self.assertEqual(code, 1)
        self.assertIn("straight_quote", finding_kinds(report))

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

    def test_register_lint_fail_on_never_exits_0_for_warning(self):
        code, report = run_cli(
            register_lint,
            [
                "--text",
                "Du kannst die Datei pruefen. Bitte senden Sie danach die Freigabe.",
                "--fail-on",
                "never",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("mixed_address", finding_kinds(report))
        self.assertTrue(all(item["severity"] == "warning" for item in report["findings"]))

    def test_register_lint_fail_on_blocker_exits_0_for_warning(self):
        code, report = run_cli(
            register_lint,
            [
                "--text",
                "Du kannst die Datei pruefen. Bitte senden Sie danach die Freigabe.",
                "--fail-on",
                "blocker",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("mixed_address", finding_kinds(report))
        self.assertTrue(all(item["severity"] == "warning" for item in report["findings"]))

    def test_register_lint_fail_on_any_exits_1_for_warning(self):
        code, report = run_cli(
            register_lint,
            [
                "--text",
                "Du kannst die Datei pruefen. Bitte senden Sie danach die Freigabe.",
                "--fail-on",
                "any",
            ],
        )

        self.assertEqual(code, 1)
        self.assertIn("mixed_address", finding_kinds(report))
        self.assertTrue(all(item["severity"] == "warning" for item in report["findings"]))

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

    def test_evidence_lint_fail_on_never_exits_0_for_blocker(self):
        code, report = run_cli(
            evidence_lint,
            [
                "--before",
                "Die Wartezeit sank laut Bericht.",
                "--after",
                "Die Wartezeit sank laut Bericht um 63 Prozent.",
                "--fail-on",
                "never",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("added_number", finding_kinds(report))
        self.assertTrue(any(item["severity"] == "blocker" for item in report["findings"]))

    def test_evidence_lint_fail_on_blocker_exits_1_for_blocker(self):
        code, report = run_cli(
            evidence_lint,
            [
                "--before",
                "Die Wartezeit sank laut Bericht.",
                "--after",
                "Die Wartezeit sank laut Bericht um 63 Prozent.",
                "--fail-on",
                "blocker",
            ],
        )

        self.assertEqual(code, 1)
        self.assertIn("added_number", finding_kinds(report))
        self.assertTrue(any(item["severity"] == "blocker" for item in report["findings"]))

    def test_evidence_lint_fail_on_any_exits_1_for_blocker(self):
        code, report = run_cli(
            evidence_lint,
            [
                "--before",
                "Die Wartezeit sank laut Bericht.",
                "--after",
                "Die Wartezeit sank laut Bericht um 63 Prozent.",
                "--fail-on",
                "any",
            ],
        )

        self.assertEqual(code, 1)
        self.assertIn("added_number", finding_kinds(report))
        self.assertTrue(any(item["severity"] == "blocker" for item in report["findings"]))

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

    def test_rhythm_lint_fail_on_never_exits_0_for_suspicion(self):
        code, report = run_cli(
            rhythm_lint,
            [
                "--text",
                "Zudem prueft das Team die Werte. Zudem speichert es die Notizen.",
                "--fail-on",
                "never",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("connector density", {item["reason"] for item in report["suspicions"]})
        self.assertTrue(all(item.get("severity") == "warning" for item in report["suspicions"]))

    def test_rhythm_lint_fail_on_blocker_exits_0_for_warning_suspicion(self):
        code, report = run_cli(
            rhythm_lint,
            [
                "--text",
                "Zudem prueft das Team die Werte. Zudem speichert es die Notizen.",
                "--fail-on",
                "blocker",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("connector density", {item["reason"] for item in report["suspicions"]})
        self.assertTrue(all(item.get("severity") == "warning" for item in report["suspicions"]))

    def test_rhythm_lint_fail_on_any_exits_1_for_suspicion(self):
        code, report = run_cli(
            rhythm_lint,
            [
                "--text",
                "Zudem prueft das Team die Werte. Zudem speichert es die Notizen.",
                "--fail-on",
                "any",
            ],
        )

        self.assertEqual(code, 1)
        self.assertIn("connector density", {item["reason"] for item in report["suspicions"]})

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

    def test_german_pattern_lint_fail_on_never_exits_0_for_warning(self):
        code, report = run_cli(
            german_pattern_lint,
            [
                "--text",
                "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.",
                "--fail-on",
                "never",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("ai_marker_cluster", finding_kinds(report))
        self.assertTrue(all(item["severity"] == "warning" for item in report["findings"]))

    def test_german_pattern_lint_fail_on_blocker_exits_0_for_warning(self):
        code, report = run_cli(
            german_pattern_lint,
            [
                "--text",
                "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.",
                "--fail-on",
                "blocker",
            ],
        )

        self.assertEqual(code, 0)
        self.assertIn("ai_marker_cluster", finding_kinds(report))
        self.assertTrue(all(item["severity"] == "warning" for item in report["findings"]))

    def test_german_pattern_lint_fail_on_any_exits_1_for_warning(self):
        code, report = run_cli(
            german_pattern_lint,
            [
                "--text",
                "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.",
                "--fail-on",
                "any",
            ],
        )

        self.assertEqual(code, 1)
        self.assertIn("ai_marker_cluster", finding_kinds(report))
        self.assertTrue(all(item["severity"] == "warning" for item in report["findings"]))

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

    def test_humanizer_audit_fail_on_never_exits_0_for_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            finding_path = Path(tmp) / "finding.md"
            finding_path.write_text('Er sagte "Hallo".', encoding="utf-8")

            code, report = run_cli(
                humanizer_audit,
                ["--file", str(finding_path), "--no-profile", "--fail-on", "never"],
            )

        self.assertEqual(code, 0)
        self.assertIn("straight_quote", finding_kinds(report))
        self.assertGreater(report["summary"]["counts"]["unicode"], 0)

    def test_humanizer_audit_fail_on_blocker_exits_1_for_register_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            finding_path = Path(tmp) / "finding.md"
            finding_path.write_text("Klingt spannend?", encoding="utf-8")

            code, report = run_cli(
                humanizer_audit,
                ["--file", str(finding_path), "--mode", "formal", "--no-profile", "--fail-on", "blocker"],
            )

        self.assertEqual(code, 1)
        self.assertIn("formal_voice_intrusion", finding_kinds(report))
        self.assertTrue(any(item["severity"] == "blocker" for item in report["findings"]))

    def test_humanizer_audit_fail_on_any_exits_1_for_finding_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            finding_path = Path(tmp) / "finding.md"
            finding_path.write_text('Er sagte "Hallo".', encoding="utf-8")

            code, report = run_cli(
                humanizer_audit,
                ["--file", str(finding_path), "--no-profile", "--fail-on", "any"],
            )

        self.assertEqual(code, 1)
        self.assertIn("straight_quote", finding_kinds(report))
        self.assertGreater(sum(report["summary"]["counts"].values()), 0)

    def test_spell_lint_default_exits_0_when_unavailable(self):
        with mock.patch.object(spell_lint.shutil, "which", return_value=None):
            code, report = run_cli(
                spell_lint,
                ["--before", "Das Team prüft.", "--after", "Das Team prüft."],
            )

        self.assertEqual(code, 0)
        self.assertEqual(report, {"available": False, "reason": "hunspell_missing", "findings": []})

    def test_spell_lint_fail_on_never_exits_0_when_unavailable(self):
        with mock.patch.object(spell_lint.shutil, "which", return_value=None):
            code, report = run_cli(
                spell_lint,
                ["--before", "Das Team prüft.", "--after", "Das Team prüft.", "--fail-on", "never"],
            )

        self.assertEqual(code, 0)
        self.assertEqual(report, {"available": False, "reason": "hunspell_missing", "findings": []})

    @unittest.skipUnless(HUNSPELL_DE_AVAILABLE, "hunspell de_DE dictionary is not available")
    def test_spell_lint_fail_on_blocker_exits_0_for_warning_only_finding(self):
        code, report = run_cli(
            spell_lint,
            [
                "--before",
                "Das Team prüft den Bericht.",
                "--after",
                "Das Team prüft den Berihct.",
                "--fail-on",
                "blocker",
            ],
        )

        self.assertEqual(code, 0)
        self.assertTrue(report["available"])
        self.assertEqual(report["findings"][0]["severity"], "warning")

    @unittest.skipUnless(HUNSPELL_DE_AVAILABLE, "hunspell de_DE dictionary is not available")
    def test_spell_lint_fail_on_any_exits_1_for_warning_finding(self):
        code, report = run_cli(
            spell_lint,
            [
                "--before",
                "Das Team prüft den Bericht.",
                "--after",
                "Das Team prüft den Berihct.",
                "--fail-on",
                "any",
            ],
        )

        self.assertEqual(code, 1)
        self.assertTrue(report["available"])
        self.assertEqual(report["findings"][0]["severity"], "warning")


if __name__ == "__main__":
    unittest.main()
