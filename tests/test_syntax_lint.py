import builtins
import io
import importlib.util
import json
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


syntax_lint = load_script("syntax_lint")


def run_cli(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = module.main(argv)
    return exit_code, json.loads(stdout.getvalue())


def spacy_model_available():
    try:
        import spacy

        spacy.load("de_core_news_sm")
    except Exception:
        return False
    return True


SPACY_MODEL_AVAILABLE = spacy_model_available()


class SyntaxLintOptionalDependencyTests(unittest.TestCase):
    def test_module_import_does_not_require_spacy(self):
        self.assertTrue(hasattr(syntax_lint, "main"))

    def test_missing_spacy_reports_unavailable_and_exits_zero(self):
        real_import = builtins.__import__

        def import_without_spacy(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "spacy" or name.startswith("spacy."):
                raise ModuleNotFoundError("No module named 'spacy'")
            return real_import(name, globals, locals, fromlist, level)

        with mock.patch("builtins.__import__", side_effect=import_without_spacy):
            exit_code, report = run_cli(syntax_lint, ["--text", "x"])

        self.assertEqual(exit_code, 0)
        self.assertFalse(report["available"])
        self.assertEqual(report["reason"], "spacy_missing")
        self.assertIsNone(report["metrics"])
        self.assertEqual(report["findings"], [])

    def test_default_cli_exits_zero_in_current_environment(self):
        exit_code, report = run_cli(syntax_lint, ["--text", "x"])

        self.assertEqual(exit_code, 0)
        self.assertIn(report["available"], {True, False})
        if not report["available"]:
            self.assertIn(report["reason"], {"spacy_missing", "model_missing"})


@unittest.skipUnless(SPACY_MODEL_AVAILABLE, "spaCy German model is not available")
class SyntaxLintSpacyTests(unittest.TestCase):
    def test_markdown_structure_does_not_create_subjectless_fragments(self):
        text = """---
title: Sauberer Artikel
description: Struktur darf nicht als Satz gelten.
---

# Eisberg-Heuristik

```text
Quelle --> Prüfung
         |
         v
      Befund
```

Der Artikel erklärt die Methode. Die Auswertung bleibt nachvollziehbar.
"""
        exit_code, report = run_cli(syntax_lint, ["--text", text])

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["available"])
        subjectless = [
            finding
            for finding in report["findings"]
            if finding["kind"] == "subjectless_fragment"
        ]
        self.assertEqual(subjectless, [])

    def test_subjectless_fragment_in_markdown_prose_is_still_reported(self):
        text = """# Kontext

Ohne klares Subjekt. Der zweite Satz ist vollständig.
"""
        exit_code, report = run_cli(syntax_lint, ["--text", text])

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["available"])
        subjectless = [
            finding
            for finding in report["findings"]
            if finding["kind"] == "subjectless_fragment"
        ]
        self.assertEqual(len(subjectless), 1)
        self.assertEqual(subjectless[0]["sentence"], "Ohne klares Subjekt.")

    def test_passive_sentence_reports_agent_phrase(self):
        exit_code, report = run_cli(
            syntax_lint,
            ["--text", "Der Bericht wird von der Behörde geprüft."],
        )

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["available"])
        self.assertEqual(len(report["findings"]), 1)
        finding = report["findings"][0]
        self.assertEqual(finding["pattern"], 39)
        self.assertEqual(finding["kind"], "passive_sentence")
        self.assertEqual(finding["severity"], "info")
        self.assertIn("von", finding["agent_phrase"])

    def test_contract_sentence_has_no_historical_false_alarm(self):
        exit_code, report = run_cli(
            syntax_lint,
            ["--text", "Der Vertrag endet am 31. Dezember 2026."],
        )

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["available"])
        self.assertEqual(report["findings"], [])

    def test_nominal_sentence_has_higher_noun_verb_ratio(self):
        nominal_code, nominal_report = run_cli(
            syntax_lint,
            [
                "--text",
                "Die kontinuierliche Optimierung der behördlichen Prüfprozesse erfordert eine sorgfältige Dokumentation.",
            ],
        )
        verbal_code, verbal_report = run_cli(
            syntax_lint,
            ["--text", "Das Team prüft, dokumentiert und verbessert die Abläufe."],
        )

        self.assertEqual(nominal_code, 0)
        self.assertEqual(verbal_code, 0)
        self.assertTrue(nominal_report["available"])
        self.assertTrue(verbal_report["available"])
        self.assertGreater(
            nominal_report["metrics"]["noun_verb_ratio"],
            verbal_report["metrics"]["noun_verb_ratio"],
        )

    def test_verb_bracket_span_detects_german_bracket(self):
        bracket_code, bracket_report = run_cli(
            syntax_lint,
            [
                "--text",
                "Er hat die Rechnung nach langem Hin und Her gestern endlich bezahlt.",
            ],
        )
        plain_code, plain_report = run_cli(
            syntax_lint,
            ["--text", "Das Team bezahlt die Rechnung."],
        )

        self.assertEqual(bracket_code, 0)
        self.assertEqual(plain_code, 0)
        self.assertTrue(bracket_report["available"])
        self.assertTrue(plain_report["available"])
        self.assertGreaterEqual(
            bracket_report["metrics"]["verb_bracket_span_max"],
            8,
        )
        self.assertEqual(plain_report["metrics"]["verb_bracket_span_max"], 0)
        self.assertGreater(
            bracket_report["metrics"]["verb_bracket_span_max"],
            plain_report["metrics"]["verb_bracket_span_max"],
        )

    def test_embedding_depth_rises_for_nested_clauses(self):
        simple_code, simple_report = run_cli(
            syntax_lint,
            ["--text", "Er sagt, dass sie kommt."],
        )
        nested_code, nested_report = run_cli(
            syntax_lint,
            ["--text", "Er sagt, dass sie kommt, weil er fragt, ob es klappt."],
        )

        self.assertEqual(simple_code, 0)
        self.assertEqual(nested_code, 0)
        self.assertTrue(simple_report["available"])
        self.assertTrue(nested_report["available"])
        self.assertGreater(
            nested_report["metrics"]["max_embedding_depth"],
            simple_report["metrics"]["max_embedding_depth"],
        )

    def test_mean_dependency_distance_is_positive_for_sentence(self):
        exit_code, report = run_cli(
            syntax_lint,
            ["--text", "Das Team prüft die Rechnung sorgfältig."],
        )

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["available"])
        self.assertGreater(report["metrics"]["mean_dependency_distance"], 0)


if __name__ == "__main__":
    unittest.main()
