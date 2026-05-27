import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "unicode_lint.py"

spec = importlib.util.spec_from_file_location("unicode_lint", SCRIPT)
unicode_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unicode_lint)


class UnicodeLintTests(unittest.TestCase):
    def test_hidden_unicode_is_found_and_removed(self):
        hidden = chr(0x200B)
        text = f"Alpha{hidden}Beta"
        findings = unicode_lint.lint(text)
        self.assertEqual(ord(hidden), 0x200B)
        self.assertTrue(any(item["pattern"] == 43 for item in findings))
        self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_non_breaking_space_is_not_flagged(self):
        text = f"5{chr(0x00A0)}km"
        self.assertEqual(unicode_lint.lint(text), [])
        self.assertEqual(unicode_lint.fix(text), text)

    def test_correct_german_quotes_are_clean(self):
        text = chr(0x201E) + "Text" + chr(0x201C)
        self.assertEqual(ord(text[0]), 0x201E)
        self.assertEqual(ord(text[-1]), 0x201C)
        self.assertEqual(unicode_lint.lint(text), [])

    def test_wrong_german_closing_quote_is_fixed(self):
        text = chr(0x201E) + "Text" + chr(0x201D)
        fixed = unicode_lint.fix(text)
        self.assertTrue(any(item["kind"] == "wrong_german_closing_quote" for item in unicode_lint.lint(text)))
        self.assertEqual(ord(fixed[-1]), 0x201C)

    def test_nested_single_german_quotes_are_valid(self):
        text = chr(0x201E) + "Er sagte: " + chr(0x201A) + "Hallo" + chr(0x2018) + chr(0x201C)
        self.assertEqual(unicode_lint.lint(text), [])

    def test_wrong_single_german_closing_quote_is_fixed(self):
        text = chr(0x201A) + "Hallo" + chr(0x2019)
        fixed = unicode_lint.fix(text)
        self.assertTrue(any(item["kind"] == "wrong_single_german_closing_quote" for item in unicode_lint.lint(text)))
        self.assertEqual(ord(fixed[-1]), 0x2018)

    def test_english_curly_quote_pair_is_reported(self):
        text = chr(0x201C) + "Text" + chr(0x201D)
        self.assertTrue(any(item["kind"] == "english_curly_quotes" for item in unicode_lint.lint(text)))

    def test_valid_german_closing_quote_is_not_english_opener(self):
        text = chr(0x201E) + "A" + chr(0x201C) + " und " + chr(0x201E) + "B" + chr(0x201D)
        findings = unicode_lint.lint(text)
        self.assertTrue(any(item["kind"] == "wrong_german_closing_quote" for item in findings))
        self.assertFalse(any(item["kind"] == "english_curly_quotes" for item in findings))

    def test_stray_wrong_double_closing_quote_is_reported(self):
        text = "Text" + chr(0x201D)
        self.assertTrue(any(item["kind"] == "stray_wrong_german_closing_quote" for item in unicode_lint.lint(text)))

    def test_stray_wrong_single_closing_quote_is_reported(self):
        text = "Text" + chr(0x2019)
        self.assertTrue(any(item["kind"] == "stray_wrong_single_german_closing_quote" for item in unicode_lint.lint(text)))

    def test_typographic_german_apostrophe_is_not_quote_finding(self):
        text = "Hans" + chr(0x2019) + " Auto"
        self.assertEqual(unicode_lint.lint(text), [])

    def test_ascii_quotes_are_reported_not_normalized(self):
        text = '"Text"'
        self.assertTrue(any(item["kind"] == "straight_quote" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), text)

    def test_inline_code_is_protected_from_quote_findings(self):
        text = '`"code"`'
        self.assertEqual(unicode_lint.lint(text), [])


if __name__ == "__main__":
    unittest.main()
