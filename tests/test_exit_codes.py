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


cli_output = load_script("cli_output")
unicode_lint = load_script("unicode_lint")
register_lint = load_script("register_lint")
evidence_lint = load_script("evidence_lint")
rhythm_lint = load_script("rhythm_lint")
german_pattern_lint = load_script("german_pattern_lint")
humanizer_audit = load_script("humanizer_audit")
spell_lint = load_script("spell_lint")


def run_cli(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = module.main(argv)
    return exit_code, json.loads(stdout.getvalue())


class ExitCodeTests(unittest.TestCase):
    def test_policy_matrix(self):
        finding_sets = {
            "clean": [],
            "warning": [{"severity": "warning"}],
            "blocker": [{"severity": "blocker"}],
        }
        expected = {
            ("never", "clean"): 0,
            ("never", "warning"): 0,
            ("never", "blocker"): 0,
            ("blocker", "clean"): 0,
            ("blocker", "warning"): 0,
            ("blocker", "blocker"): 1,
            ("any", "clean"): 0,
            ("any", "warning"): 1,
            ("any", "blocker"): 1,
        }

        for (policy, finding_kind), exit_code in expected.items():
            with self.subTest(policy=policy, findings=finding_kind):
                self.assertEqual(
                    cli_output.resolve_exit_code(policy, finding_sets[finding_kind]),
                    exit_code,
                )

    def test_advisory_findings_are_gate_neutral(self):
        findings = [
            {"severity": "info", "advisory": True},
            {"severity": "blocker", "advisory": True},
        ]

        self.assertEqual(cli_output.resolve_exit_code("any", findings), 0)
        self.assertEqual(cli_output.resolve_exit_code("blocker", findings), 0)

    def test_any_policy_still_gates_non_advisory_findings(self):
        findings = [
            {"severity": "info", "advisory": True},
            {"severity": "warning"},
        ]

        self.assertEqual(cli_output.resolve_exit_code("any", findings), 1)

    def test_blocker_policy_still_gates_non_advisory_blockers(self):
        findings = [
            {"severity": "blocker", "advisory": True},
            {"severity": "blocker"},
        ]

        self.assertEqual(cli_output.resolve_exit_code("blocker", findings), 1)

    def test_cli_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_path = Path(tmp) / "finding.md"
            audit_path.write_text('Er sagte "Hallo".', encoding="utf-8")
            cases = [
                (unicode_lint, ["--text", 'Er sagte "Hallo".'], "any", 1),
                (register_lint, ["--text", "Die Prüfung ist abgeschlossen. ✅", "--mode", "formal"], "blocker", 1),
                (
                    evidence_lint,
                    [
                        "--before",
                        "Die Wartezeit sank laut Bericht.",
                        "--after",
                        "Die Wartezeit sank laut Bericht um 63 Prozent.",
                    ],
                    "blocker",
                    1,
                ),
                (
                    rhythm_lint,
                    ["--text", "Zudem prueft das Team die Werte. Zudem speichert es die Notizen."],
                    "never",
                    0,
                ),
                (
                    german_pattern_lint,
                    [
                        "--text",
                        "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.",
                    ],
                    "never",
                    0,
                ),
                (
                    humanizer_audit,
                    ["--file", str(audit_path), "--no-profile"],
                    "never",
                    0,
                ),
            ]

            for module, argv, expected_policy, expected_code in cases:
                with self.subTest(module=module.__name__), mock.patch.object(
                    module,
                    "resolve_exit_code",
                    wraps=module.resolve_exit_code,
                ) as resolver:
                    code, _ = run_cli(module, argv)
                    self.assertEqual(code, expected_code)
                    self.assertEqual(resolver.call_args.args[0], expected_policy)

        warning_report = {"available": True, "findings": [{"severity": "warning"}]}
        with mock.patch.object(spell_lint, "lint", return_value=warning_report), mock.patch.object(
            spell_lint,
            "resolve_exit_code",
            wraps=spell_lint.resolve_exit_code,
        ) as resolver:
            code, _ = run_cli(
                spell_lint,
                ["--before", "Das Team prüft.", "--after", "Das Team prüft."],
            )
        self.assertEqual(code, 0)
        self.assertEqual(resolver.call_args.args[0], "never")

    def test_cli_fail_on_flag_is_forwarded(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_path = Path(tmp) / "finding.md"
            audit_path.write_text('Er sagte "Hallo".', encoding="utf-8")
            cases = [
                (unicode_lint, ["--text", 'Er sagte "Hallo".']),
                (
                    register_lint,
                    ["--text", "Du prüfst den Text. Bitte senden Sie die Freigabe."],
                ),
                (
                    evidence_lint,
                    [
                        "--before",
                        "Die Wartezeit sank laut Bericht.",
                        "--after",
                        "Die Wartezeit sank laut Bericht um 63 Prozent.",
                    ],
                ),
                (
                    rhythm_lint,
                    ["--text", "Zudem prüft das Team die Werte. Zudem speichert es die Notizen."],
                ),
                (
                    german_pattern_lint,
                    [
                        "--text",
                        "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.",
                    ],
                ),
                (
                    humanizer_audit,
                    ["--file", str(audit_path), "--no-profile"],
                ),
            ]

            for module, argv in cases:
                with self.subTest(module=module.__name__), mock.patch.object(
                    module,
                    "resolve_exit_code",
                    wraps=module.resolve_exit_code,
                ) as resolver:
                    code, _ = run_cli(module, argv + ["--fail-on", "any"])
                    self.assertEqual(code, 1)
                    self.assertEqual(resolver.call_args.args[0], "any")
                    self.assertTrue(resolver.call_args.args[1])

        warning_report = {"available": True, "findings": [{"severity": "warning"}]}
        with mock.patch.object(spell_lint, "lint", return_value=warning_report), mock.patch.object(
            spell_lint,
            "resolve_exit_code",
            wraps=spell_lint.resolve_exit_code,
        ) as resolver:
            code, _ = run_cli(
                spell_lint,
                [
                    "--before",
                    "Das Team prüft.",
                    "--after",
                    "Das Team prüft.",
                    "--fail-on",
                    "any",
                ],
            )
        self.assertEqual(code, 1)
        self.assertEqual(resolver.call_args.args[0], "any")
        self.assertEqual(resolver.call_args.args[1], warning_report["findings"])

    def test_blocker_policy_is_rejected_by_warning_only_scripts(self):
        cases = [
            (unicode_lint, ["--text", 'Er sagte "Hallo".']),
            (rhythm_lint, ["--text", "Zudem prüft das Team die Werte."]),
            (german_pattern_lint, ["--text", "Der Text beleuchtet das Thema."]),
            (spell_lint, ["--before", "Das Team prüft.", "--after", "Das Team prüft."]),
        ]

        for module, argv in cases:
            stderr = io.StringIO()
            with self.subTest(module=module.__name__), redirect_stderr(stderr):
                code = module.main(argv + ["--fail-on", "blocker"])
            self.assertEqual(code, 2)
            self.assertIn("invalid choice: 'blocker'", stderr.getvalue())

    def test_blocker_policy_still_gates_blocker_capable_scripts(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker_path = Path(tmp) / "blocker.md"
            blocker_path.write_text("Die Prüfung ist abgeschlossen. ✅", encoding="utf-8")
            warning_path = Path(tmp) / "warning.md"
            warning_path.write_text("Welche Folgen hat der Effekt?", encoding="utf-8")
            cases = [
                (
                    register_lint,
                    ["--text", "Die Prüfung ist abgeschlossen. ✅", "--mode", "formal"],
                    ["--text", "Welche Folgen hat der Effekt?", "--mode", "formal"],
                ),
                (
                    evidence_lint,
                    [
                        "--before",
                        "Die Wartezeit sank laut Bericht.",
                        "--after",
                        "Die Wartezeit sank laut Bericht um 63 Prozent.",
                    ],
                    [
                        "--before",
                        "Das Team prüft den Text.",
                        "--after",
                        "Das Team von Acme prüft den Text.",
                    ],
                ),
                (
                    humanizer_audit,
                    ["--file", str(blocker_path), "--mode", "formal", "--no-profile"],
                    ["--file", str(warning_path), "--mode", "formal", "--no-profile"],
                ),
            ]

            for module, blocker_argv, warning_argv in cases:
                with self.subTest(module=module.__name__):
                    blocker_code, blocker_report = run_cli(module, blocker_argv + ["--fail-on", "blocker"])
                    warning_code, warning_report = run_cli(module, warning_argv + ["--fail-on", "blocker"])
                    self.assertEqual(blocker_code, 1)
                    self.assertTrue(any(item.get("severity") == "blocker" for item in blocker_report["findings"]))
                    self.assertEqual(warning_code, 0)
                    self.assertTrue(warning_report["findings"])
                    self.assertEqual({item.get("severity") for item in warning_report["findings"]}, {"warning"})


if __name__ == "__main__":
    unittest.main()
