import importlib.util
import random
import time
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

    def test_range_checker_matches_naive_in_ranges(self):
        rng = random.Random(20260705)
        fragments = [
            "Prosa mit ein paar Wörtern. ",
            chr(0x201E) + "Zitat" + chr(0x201C) + " ",
            "`inline code` ",
            "```\nblock\n``` ",
            "https://example.org/pfad?x=1 ",
            "mail@example.org ",
            '"gerade Anführung" ',
        ]
        for _ in range(200):
            text = "".join(rng.choice(fragments) for _ in range(rng.randint(1, 12)))
            ranges = unicode_lint.protected_ranges(text)
            contains = unicode_lint.range_checker(ranges)
            for index in range(len(text) + 1):
                self.assertEqual(
                    contains(index),
                    unicode_lint.in_ranges(index, ranges),
                    f"Abweichung bei Index {index} in: {text!r}",
                )

    def test_large_file_lint_is_fast(self):
        parts = []
        for i in range(1000):
            parts.append(f"Absatz {i} mit https://example.org/seite/{i} und `code_{i}` im Fließtext. ")
            if i % 5 == 0:
                parts.append(chr(0x201E) + f"Zitat {i}" + chr(0x201C) + " ")
        text = "".join(parts)
        start = time.process_time()
        unicode_lint.lint(text)
        elapsed = time.process_time() - start
        self.assertLess(elapsed, 1.0, f"lint() brauchte {elapsed:.2f} s CPU-Zeit")


if __name__ == "__main__":
    unittest.main()
