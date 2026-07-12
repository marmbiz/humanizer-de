#!/usr/bin/env python3
"""Lint and optionally fix Humanizer-de Unicode patterns 43 and 46."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from bisect import bisect_right
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import print_json
import text_scope


HIDDEN_RANGES = (
    (0x200B, 0x200D),
    (0x2060, 0x2064),
    (0x202A, 0x202E),
    (0x2066, 0x2069),
)
HIDDEN_SINGLE = {0x00AD, 0xFEFF}

OPEN_DE = "\u201e"
CLOSE_DE = "\u201c"
WRONG_CLOSE_DE = "\u201d"
OPEN_DE_SINGLE = "\u201a"
CLOSE_DE_SINGLE = "\u2018"
WRONG_CLOSE_SINGLE = "\u2019"
OPEN_EN = "\u201c"
ASCII_QUOTE = '"'


def is_hidden_char(char: str) -> bool:
    code = ord(char)
    if code in HIDDEN_SINGLE:
        return True
    return any(start <= code <= end for start, end in HIDDEN_RANGES)


def is_emoji_codepoint(char: str) -> bool:
    code = ord(char)
    return (
        0x1F000 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
        or 0x2300 <= code <= 0x23FF
        or 0x2B00 <= code <= 0x2BFF
        or code in {0x00A9, 0x00AE, 0x203C, 0x2049, 0x3030, 0x303D, 0x3297, 0x3299}
    )


def is_emoji_zwj(text: str, index: int) -> bool:
    if text[index] != "\u200d":
        return False

    left = index - 1
    while left >= 0 and text[left] in {"\ufe0e", "\ufe0f"}:
        left -= 1
    right = index + 1
    while right < len(text) and text[right] in {"\ufe0e", "\ufe0f"}:
        right += 1
    return left >= 0 and right < len(text) and is_emoji_codepoint(text[left]) and is_emoji_codepoint(text[right])


def is_hidden_at(text: str, index: int) -> bool:
    return is_hidden_char(text[index]) and not is_emoji_zwj(text, index)


def codepoint(char: str) -> str:
    return f"U+{ord(char):04X}"


def protected_ranges(text: str) -> list[tuple[int, int]]:
    ranges = text_scope.protected_ranges(text, scope=text_scope.TYPOGRAPHIC_PROSE)
    link_title_re = re.compile(r"\]\([^()\s]+[ \t]+(\"[^\"\n]*\")\)")
    ranges.extend(match.span(1) for match in link_title_re.finditer(text))
    return merge_ranges(ranges)


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def range_checker(ranges: list[tuple[int, int]]):
    merged = merge_ranges(ranges)
    starts = [item[0] for item in merged]
    ends = [item[1] for item in merged]

    def contains(index: int) -> bool:
        pos = bisect_right(starts, index) - 1
        return pos >= 0 and index < ends[pos]

    return contains


def in_ranges(index: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in ranges)


def add_finding(findings: list[dict], pattern: int, kind: str, index: int, char: str, message: str) -> None:
    findings.append(
        {
            "pattern": pattern,
            "kind": kind,
            "index": index,
            "char": char,
            "codepoint": codepoint(char),
            "name": unicodedata.name(char, "UNKNOWN"),
            "message": message,
        }
    )


def preceding_word(text: str, index: int) -> str:
    match = re.search(r"[\wÄÖÜäöüß]+$", text[:index], re.UNICODE)
    return match.group(0) if match else ""


def looks_like_german_apostrophe(text: str, index: int) -> bool:
    word = preceding_word(text, index)
    if not word:
        return False
    lower_word = word.lower()
    if lower_word.endswith(("s", "x", "z", "ce")):
        return True
    next_char = text[index + 1] if index + 1 < len(text) else ""
    return bool(next_char and next_char.isalpha())


def scan_quotes(text: str, in_range) -> tuple[list[dict], dict[int, str], set[str]]:
    findings: list[dict] = []
    replacements: dict[int, str] = {}
    quote_styles: set[str] = set()
    double_openers: list[int] = []
    single_openers: list[int] = []
    english_double_openers: list[int] = []

    for index, char in enumerate(text):
        if in_range(index):
            continue
        if char in {
            OPEN_DE,
            CLOSE_DE,
            WRONG_CLOSE_DE,
            OPEN_DE_SINGLE,
            CLOSE_DE_SINGLE,
            WRONG_CLOSE_SINGLE,
            ASCII_QUOTE,
            "\u00ab",
            "\u00bb",
        }:
            quote_styles.add(char)

        if char == OPEN_DE:
            double_openers.append(index)
        elif char == OPEN_DE_SINGLE:
            single_openers.append(index)
        elif char == CLOSE_DE:
            if double_openers:
                double_openers.pop()
            else:
                english_double_openers.append(index)
        elif char == CLOSE_DE_SINGLE:
            if single_openers:
                single_openers.pop()
        elif char == WRONG_CLOSE_DE:
            if double_openers:
                double_openers.pop()
                replacements[index] = CLOSE_DE
                add_finding(
                    findings,
                    46,
                    "wrong_german_closing_quote",
                    index,
                    char,
                    "Use U+201C after U+201E, not U+201D.",
                )
            elif english_double_openers:
                opener = english_double_openers.pop()
                add_finding(
                    findings,
                    46,
                    "english_curly_quotes",
                    opener,
                    OPEN_EN,
                    "English curly quote pair in German prose; review German quote style.",
                )
            else:
                add_finding(
                    findings,
                    46,
                    "stray_wrong_german_closing_quote",
                    index,
                    char,
                    "Wrong German closing quote without matching U+201E opener.",
                )
        elif char == WRONG_CLOSE_SINGLE:
            if single_openers:
                single_openers.pop()
                replacements[index] = CLOSE_DE_SINGLE
                add_finding(
                    findings,
                    46,
                    "wrong_single_german_closing_quote",
                    index,
                    char,
                    "Use U+2018 after U+201A, not U+2019.",
                )
            elif not looks_like_german_apostrophe(text, index):
                add_finding(
                    findings,
                    46,
                    "stray_wrong_single_german_closing_quote",
                    index,
                    char,
                    "Wrong single German closing quote without matching U+201A opener.",
                )
        elif char == ASCII_QUOTE:
            double_index = double_openers[-1] if double_openers else -1
            single_index = single_openers[-1] if single_openers else -1
            if double_index > single_index:
                double_openers.pop()
                add_finding(
                    findings,
                    46,
                    "ascii_german_closing_quote",
                    index,
                    char,
                    "Use U+201C after U+201E, not ASCII quote.",
                )
            elif single_index >= 0:
                single_openers.pop()
                add_finding(
                    findings,
                    46,
                    "ascii_single_german_closing_quote",
                    index,
                    char,
                    "Use U+2018 after U+201A, not ASCII quote.",
                )

            add_finding(findings, 46, "straight_quote", index, char, "Straight ASCII quote in prose; review German quote style.")

    for index in double_openers:
        add_finding(findings, 46, "unclosed_german_quote", index, OPEN_DE, "Opening German quote has no closing quote.")
    for index in single_openers:
        add_finding(
            findings,
            46,
            "unclosed_single_german_quote",
            index,
            OPEN_DE_SINGLE,
            "Opening single German quote has no closing quote.",
        )

    return findings, replacements, quote_styles


def lint(text: str) -> list[dict]:
    findings: list[dict] = []
    ranges = protected_ranges(text)
    in_range = range_checker(ranges)

    for index, char in enumerate(text):
        if is_hidden_at(text, index):
            add_finding(findings, 43, "hidden_unicode", index, char, "Remove hidden Unicode character.")

    quote_findings, _, quote_styles = scan_quotes(text, in_range)
    findings.extend(quote_findings)

    style_families = 0
    if quote_styles & {OPEN_DE, CLOSE_DE, WRONG_CLOSE_DE}:
        style_families += 1
    if quote_styles & {"\u00ab", "\u00bb"}:
        style_families += 1
    if ASCII_QUOTE in quote_styles:
        style_families += 1
    if style_families > 1:
        findings.append(
            {
                "pattern": 46,
                "kind": "mixed_quote_styles",
                "index": None,
                "char": None,
                "codepoint": None,
                "name": None,
                "message": "Mixed quote styles in prose; review consistency.",
            }
        )

    return findings


def fix(text: str) -> str:
    chars = []
    for index, char in enumerate(text):
        if is_hidden_at(text, index):
            continue
        chars.append(char)
    cleaned = "".join(chars)
    ranges = protected_ranges(cleaned)
    in_range = range_checker(ranges)
    chars = list(cleaned)
    _, replacements, _ = scan_quotes(cleaned, in_range)
    for index, replacement in replacements.items():
        chars[index] = replacement
    return "".join(chars)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint Humanizer-de Unicode patterns 43 and 46.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to lint.")
    source.add_argument("--file", type=Path, help="UTF-8 text file to lint.")
    parser.add_argument("--fix", action="store_true", help="Apply safe fixes in output.")
    parser.add_argument("--write", action="store_true", help="Write fixed text back to --file. Requires --fix.")
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="any")
    args = parser.parse_args(argv)
    if args.write and (not args.fix or not args.file):
        parser.error("--write requires --fix and --file")
    return args


def exit_code(findings: list[dict], fail_on: str) -> int:
    if fail_on == "never":
        return 0
    if fail_on == "blocker":
        return 1 if any(item.get("severity") == "blocker" for item in findings) else 0
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    findings = lint(text)
    fixed_text = fix(text) if args.fix else text

    if args.write and fixed_text != text:
        args.file.write_text(fixed_text, encoding="utf-8")

    result = {
        "ok": not findings,
        "findings": findings,
        "changed": fixed_text != text,
    }
    if args.fix and not args.write:
        result["fixed_text"] = fixed_text

    print_json(result)
    return exit_code(findings, args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
