import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "unicode_lint.py"

spec = importlib.util.spec_from_file_location("unicode_lint", SCRIPT)
unicode_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unicode_lint)


class UnicodeLintTests(unittest.TestCase):
    def test_delivered_markdown_has_no_hidden_unicode(self):
        paths = (
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "WARP.md",
            ROOT / "skills" / "humanizer-de" / "SKILL.md",
            *sorted((ROOT / "references").glob("*.md")),
            *sorted((ROOT / "assets").glob("*.md")),
            ROOT / "docs" / "coverage-matrix.md",
        )

        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                hidden = [
                    item
                    for item in unicode_lint.lint(path.read_text(encoding="utf-8"))
                    if item["kind"] == "hidden_unicode"
                ]
                self.assertEqual(hidden, [])

    def test_hidden_unicode_is_found_and_removed(self):
        hidden = chr(0x200B)
        text = f"Alpha{hidden}Beta"
        findings = unicode_lint.lint(text)
        self.assertEqual(ord(hidden), 0x200B)
        self.assertTrue(any(item["pattern"] == 43 for item in findings))
        self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_mixed_script_words_are_reported_without_fixing(self):
        cases = (
            ("Die Anаlyse stimmt.", "Anаlyse", "а", "U+0430"),
            ("Das Mοdell passt.", "Mοdell", "ο", "U+03BF"),
            ("https://exаmple.org/pfad", "exаmple", "а", "U+0430"),
        )
        for text, word, foreign, codepoint in cases:
            with self.subTest(word=word):
                findings = [item for item in unicode_lint.lint(text) if item["kind"] == "mixed_script"]
                self.assertEqual(len(findings), 1)
                self.assertEqual(findings[0]["pattern"], 43)
                self.assertEqual(findings[0]["spans"], [{"start": text.index(word), "end": text.index(word) + len(word)}])
                self.assertIn(word, findings[0]["message"])
                self.assertIn(foreign, findings[0]["message"])
                self.assertIn(codepoint, findings[0]["message"])
                self.assertEqual(unicode_lint.fix(text), text)

    def test_single_script_words_are_not_reported(self):
        for text in ("Fußgänger", "Полностью", "Café"):
            with self.subTest(text=text):
                self.assertFalse(any(item["kind"] == "mixed_script" for item in unicode_lint.lint(text)))

    def test_mixed_script_ignored_character_boundaries(self):
        # Ziffern und kombinierende Zeichen tragen kein Schriftsystem.
        for text in ("H2O", "Cafe\u0301"):
            with self.subTest(text=text):
                self.assertFalse(any(item["kind"] == "mixed_script" for item in unicode_lint.lint(text)))

    def test_emoji_zwj_sequence_is_preserved(self):
        for text in ("👨‍👩‍👧‍👦", "👩‍💻", "👩🏽‍💻", "❤️‍🔥"):
            with self.subTest(text=text):
                self.assertEqual(unicode_lint.lint(text), [])
                self.assertEqual(unicode_lint.fix(text), text)

    def test_zwj_between_letters_is_still_removed(self):
        text = "Alpha\u200dBeta"

        self.assertTrue(any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_tag_block_payload_is_reported_and_removed(self):
        # U+E0020-U+E007F mirror printable ASCII and carry invisible payloads.
        payload = "".join(chr(0xE0000 + ord(char)) for char in "hi")
        text = f"Alpha{payload}Beta"

        findings = unicode_lint.lint(text)
        self.assertEqual(len([item for item in findings if item["kind"] == "hidden_unicode"]), 2)
        self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_language_tag_is_reported(self):
        text = f"Alpha{chr(0xE0001)}Beta"

        self.assertTrue(any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_variation_selectors_outside_emoji_are_reported(self):
        for code in (0xFE00, 0xFE0E, 0xFE0F, 0xE0100, 0xE01EF):
            with self.subTest(codepoint=code):
                text = f"Alpha{chr(code)}Beta"
                self.assertTrue(
                    any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text))
                )
                self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_subdivision_flag_tag_sequence_is_preserved(self):
        # Scotland, Wales and England are spelled with tag characters.
        for subdivision in ("gbsct", "gbwls", "gbeng"):
            text = "\U0001f3f4" + "".join(chr(0xE0000 + ord(char)) for char in subdivision) + "\U000e007f"
            with self.subTest(subdivision=subdivision):
                self.assertEqual(unicode_lint.lint(text), [])
                self.assertEqual(unicode_lint.fix(text), text)

    def test_emoji_variation_selector_is_preserved(self):
        for text in ("Ein Herz ❤️ hier.", "Taste 1️⃣ hier.", "Haken ✔︎ hier."):
            with self.subTest(text=text):
                self.assertEqual(unicode_lint.lint(text), [])
                self.assertEqual(unicode_lint.fix(text), text)

    def test_payload_disguised_as_flag_sequence_is_reported(self):
        # Well-formed flag structure, but the payload is not a real subdivision:
        # without the closed list this smuggles arbitrary text past the carve-out.
        for payload in ("secret", "123", "!"):
            text = "\U0001f3f4" + "".join(chr(0xE0000 + ord(char)) for char in payload) + "\U000e007f"
            with self.subTest(payload=payload):
                self.assertTrue(
                    any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text))
                )
                self.assertEqual(unicode_lint.fix(text), "\U0001f3f4")

    def test_tag_sequence_without_flag_base_is_reported(self):
        # Same characters, no flag base: this is payload, not an emoji.
        text = "Alpha" + "".join(chr(0xE0000 + ord(char)) for char in "gb") + chr(0xE007F) + "Beta"

        self.assertTrue(any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), "AlphaBeta")

    def test_tag_sequence_without_cancel_is_reported(self):
        text = "\U0001f3f4" + "".join(chr(0xE0000 + ord(char)) for char in "gbsct")

        self.assertTrue(any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), "\U0001f3f4")

    def test_variation_selector_at_text_start_is_reported(self):
        text = "️Alpha"

        self.assertTrue(any(item["kind"] == "hidden_unicode" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), "Alpha")

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

    def test_one_closer_cannot_close_two_openers(self):
        text = "„a „b“"
        findings = unicode_lint.lint(text)

        unclosed = [item for item in findings if item["kind"] == "unclosed_german_quote"]
        self.assertEqual([item["index"] for item in unclosed], [0])

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

    def test_ascii_closing_after_german_opener_is_fixed(self):
        text = chr(0x201E) + 'Text"'
        self.assertTrue(any(item["kind"] == "ascii_german_closing_quote" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), chr(0x201E) + "Text" + chr(0x201C))

    def test_ascii_closing_after_single_german_opener_is_fixed(self):
        text = chr(0x201A) + 'Text"'
        self.assertTrue(any(item["kind"] == "ascii_single_german_closing_quote" for item in unicode_lint.lint(text)))
        self.assertEqual(unicode_lint.fix(text), chr(0x201A) + "Text" + chr(0x2018))

    def test_ascii_pair_after_closed_german_pair_stays_untouched(self):
        text = chr(0x201E) + "Zitat" + chr(0x201C) + ' und "Code-Wert" daneben'
        self.assertEqual(unicode_lint.fix(text), text)

    def test_inline_code_is_protected_from_quote_findings(self):
        text = '`"code"`'
        self.assertEqual(unicode_lint.lint(text), [])

    def test_tilde_fenced_code_is_protected_from_quote_findings(self):
        text = '~~~python\nprint("x")\n~~~'
        self.assertEqual(unicode_lint.lint(text), [])

    def test_yaml_frontmatter_quotes_are_protected(self):
        text = '---\ntitle: "Mein Beitrag"\n---\n\nProsa ohne Quotes.'
        self.assertFalse(any(item["kind"] == "straight_quote" for item in unicode_lint.lint(text)))

    def test_markdown_image_title_quotes_are_protected(self):
        text = '![Alt](https://example.com/b.png "Titel")'
        self.assertFalse(any(item["kind"] == "straight_quote" for item in unicode_lint.lint(text)))

    def test_html_attribute_quotes_are_protected(self):
        text = '<iframe title="Eingebetteter Beitrag" src="https://example.com/e"></iframe>'
        self.assertFalse(any(item["kind"] == "straight_quote" for item in unicode_lint.lint(text)))

    def test_straight_quotes_in_html_text_are_reported(self):
        text = '<p class="intro">Er sagte "Hallo".</p>'
        findings = [item for item in unicode_lint.lint(text) if item["kind"] == "straight_quote"]

        self.assertEqual([item["char"] for item in findings], ['"', '"'])

    def test_markdown_table_rows_are_protected(self):
        text = '| 1 | Unpassendes "Fazit" | MEDIUM |\n\nProsa "Hallo".'
        findings = [item for item in unicode_lint.lint(text) if item["kind"] == "straight_quote"]
        self.assertEqual(len(findings), 2)

    def test_prose_straight_quotes_next_to_frontmatter_still_flagged(self):
        text = '---\ntitle: "Mein Beitrag"\n---\n\nEr sagte "Hallo".'
        findings = [item for item in unicode_lint.lint(text) if item["kind"] == "straight_quote"]
        self.assertEqual(len(findings), 2)

    def test_dash_line_in_document_middle_is_not_frontmatter(self):
        text = 'Einleitung.\n\n---\ntitle: "Mitte"\n---\n'
        findings = [item for item in unicode_lint.lint(text) if item["kind"] == "straight_quote"]
        self.assertEqual(len(findings), 2)

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
                    any(start <= index < end for start, end in ranges),
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

    def test_many_unmatched_openers_are_processed_linearly(self):
        text = "„" * 4000
        start = time.process_time()
        findings = unicode_lint.lint(text)
        elapsed = time.process_time() - start

        self.assertEqual(len(findings), 4000)
        self.assertTrue(all(item["kind"] == "unclosed_german_quote" for item in findings))
        self.assertLess(elapsed, 1.0, f"lint() brauchte {elapsed:.2f} s CPU-Zeit")

    def test_invalid_write_combination_is_usage_error(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--text", "Test", "--write"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("--write requires --fix and --file", proc.stderr)

    def test_atomic_fix_write_preserves_crlf_and_leaves_no_temp_file(self):
        raw = "Er sagte „Hallo”.\r\nZweite Zeile.\r\n"
        expected = "Er sagte „Hallo“.\r\nZweite Zeile.\r\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "crlf.md"
            path.write_bytes(raw.encode("utf-8"))
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--file",
                    str(path),
                    "--fix",
                    "--write",
                    "--fail-on",
                    "never",
                ],
                capture_output=True,
                text=True,
            )
            fixed = path.read_bytes().decode("utf-8")
            remaining_files = [item.name for item in Path(tmp).iterdir()]

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(fixed, expected)
        self.assertEqual(remaining_files, ["crlf.md"])

    def test_cli_json_falls_back_to_ascii_when_stdout_cannot_encode_a_finding(self):
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "cp1252"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--text", "a\u200bb"],
            capture_output=True,
            text=True,
            env=env,
        )

        self.assertEqual(proc.returncode, 1)
        report = json.loads(proc.stdout)
        self.assertEqual(report["findings"][0]["codepoint"], "U+200B")


if __name__ == "__main__":
    unittest.main()
