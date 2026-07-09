import io
import importlib.util
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "spell_lint.py"

spec = importlib.util.spec_from_file_location("spell_lint", SCRIPT)
spell_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spell_lint)


def run_cli(argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = spell_lint.main(argv)
    return exit_code, json.loads(stdout.getvalue())


def hunspell_de_available():
    return spell_lint.availability_reason() is None


HUNSPELL_DE_AVAILABLE = hunspell_de_available()


class SpellLintTests(unittest.TestCase):
    def test_module_import_does_not_require_hunspell(self):
        self.assertTrue(hasattr(spell_lint, "main"))

    def test_missing_hunspell_reports_unavailable_and_exits_zero(self):
        with mock.patch.object(spell_lint.shutil, "which", return_value=None):
            exit_code, report = run_cli(["--before", "Das Team prüft.", "--after", "Das Team prüft."])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report, {"available": False, "reason": "hunspell_missing", "findings": []})

    def test_missing_dictionary_reports_unavailable_and_exits_zero(self):
        failed_probe = mock.Mock(returncode=1, stderr="Can't open affix or dictionary files", stdout="")
        with mock.patch.object(spell_lint.shutil, "which", return_value="/usr/local/bin/hunspell"):
            with mock.patch.object(spell_lint, "run_hunspell", return_value=failed_probe):
                exit_code, report = run_cli(["--before", "Das Team prüft.", "--after", "Das Team prüft."])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report, {"available": False, "reason": "dictionary_missing", "findings": []})

    def test_diff_unknowns_reports_only_new_after_words_sorted(self):
        finding = spell_lint.diff_unknowns({"Fachwort"}, {"Fachwort", "Zulu", "Alpha"})

        self.assertEqual(
            finding,
            {
                "kind": "new_unknown_words",
                "severity": "warning",
                "words": ["Alpha", "Zulu"],
            },
        )

    def test_diff_unknowns_returns_none_without_new_unknowns(self):
        self.assertIsNone(spell_lint.diff_unknowns({"Fachwort"}, {"Fachwort"}))
        self.assertIsNone(spell_lint.diff_unknowns({"Fachwort"}, set()))

    def test_word_unknown_before_and_after_is_filtered(self):
        self.assertIsNone(spell_lint.diff_unknowns({"Projektname"}, {"Projektname"}))


@unittest.skipUnless(HUNSPELL_DE_AVAILABLE, "hunspell de_DE dictionary is not available")
class SpellLintHunspellTests(unittest.TestCase):
    def test_new_typo_is_reported_as_single_unknown_word(self):
        report = spell_lint.lint("Das Team prüft den Bericht.", "Das Team prüft den Berihct.")

        self.assertTrue(report["available"])
        self.assertFalse(report["ok"])
        self.assertEqual(
            report["findings"],
            [
                {
                    "kind": "new_unknown_words",
                    "severity": "warning",
                    "words": ["Berihct"],
                }
            ],
        )

    def test_identical_text_has_no_finding(self):
        report = spell_lint.lint("Das Team prüft den Bericht.", "Das Team prüft den Bericht.")

        self.assertTrue(report["available"])
        self.assertTrue(report["ok"])
        self.assertEqual(report["findings"], [])

    def test_cli_always_exits_zero_for_warning(self):
        exit_code, report = run_cli(
            [
                "--before",
                "Das Team prüft den Bericht.",
                "--after",
                "Das Team prüft den Berihct.",
            ]
        )

        self.assertEqual(exit_code, 0)
        self.assertFalse(report["ok"])
        self.assertEqual(report["findings"][0]["words"], ["Berihct"])

    def test_legitimate_unknown_compound_is_documented_boundary(self):
        # Empirically with local hunspell de_DE, this legitimate domain-style
        # compound is unknown; spell_lint is an invariant, not a correctness
        # judge, so a new after-only compound is still reported as noise.
        word = "Krankenhauszukunftsgesetzumsetzung"
        report = spell_lint.lint("Das Team prüft den Bericht.", f"Das Team prüft die {word}.")

        self.assertEqual(report["findings"][0]["words"], [word])


if __name__ == "__main__":
    unittest.main()
