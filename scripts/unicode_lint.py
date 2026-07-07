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


def codepoint(char: str) -> str:
    return f"U+{ord(char):04X}"


def protected_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    patterns = [
        (r"```.*?```", 0),
        (r"`[^`\n]+`", 0),
        (r"https?://[^\s<>)]+", 0),
        (r"\b[\w.-]+@[\w.-]+\.[A-Za-z]{2,}\b", 0),
        (r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", 0),
        (r"(?m)^\|.*\|[ \t]*$", 0),
        (r"\]\([^()\s]+[ \t]+(\"[^\"\n]*\")\)", 1),
        (r"<[A-Za-z/!][^<>\n]*>", 0),
    ]
    for pattern, group in patterns:
        for match in re.finditer(pattern, text, re.DOTALL):
            ranges.append(match.span(group))
    ranges.sort()
    return ranges


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


def lint(text: str) -> list[dict]:
    findings: list[dict] = []
    ranges = protected_ranges(text)
    in_range = range_checker(ranges)
    paired_quote_indices: set[int] = set()

    for index, char in enumerate(text):
        if is_hidden_char(char):
            add_finding(findings, 43, "hidden_unicode", index, char, "Remove hidden Unicode character.")

    quote_styles = set()
    for index, char in enumerate(text):
        if in_range(index):
            continue
        if char in {OPEN_DE, CLOSE_DE, WRONG_CLOSE_DE, OPEN_DE_SINGLE, CLOSE_DE_SINGLE, WRONG_CLOSE_SINGLE, ASCII_QUOTE, "\u00ab", "\u00bb"}:
            quote_styles.add(char)

    for index, char in enumerate(text):
        if char != OPEN_DE or in_range(index):
            continue
        closing_index = None
        closing_char = ""
        for probe in range(index + 1, len(text)):
            if in_range(probe):
                continue
            if text[probe] in {CLOSE_DE, WRONG_CLOSE_DE, ASCII_QUOTE}:
                closing_index = probe
                closing_char = text[probe]
                break
        if closing_index is None:
            add_finding(findings, 46, "unclosed_german_quote", index, char, "Opening German quote has no closing quote.")
        else:
            paired_quote_indices.update({index, closing_index})
            if closing_char == WRONG_CLOSE_DE:
                add_finding(findings, 46, "wrong_german_closing_quote", closing_index, closing_char, "Use U+201C after U+201E, not U+201D.")
            elif closing_char == ASCII_QUOTE:
                add_finding(findings, 46, "ascii_german_closing_quote", closing_index, closing_char, "Use U+201C after U+201E, not ASCII quote.")

    for index, char in enumerate(text):
        if char != OPEN_DE_SINGLE or in_range(index):
            continue
        closing_index = None
        closing_char = ""
        for probe in range(index + 1, len(text)):
            if in_range(probe):
                continue
            if text[probe] in {CLOSE_DE_SINGLE, WRONG_CLOSE_SINGLE, ASCII_QUOTE}:
                closing_index = probe
                closing_char = text[probe]
                break
        if closing_index is None:
            add_finding(findings, 46, "unclosed_single_german_quote", index, char, "Opening single German quote has no closing quote.")
        else:
            paired_quote_indices.update({index, closing_index})
            if closing_char == WRONG_CLOSE_SINGLE:
                add_finding(findings, 46, "wrong_single_german_closing_quote", closing_index, closing_char, "Use U+2018 after U+201A, not U+2019.")
            elif closing_char == ASCII_QUOTE:
                add_finding(findings, 46, "ascii_single_german_closing_quote", closing_index, closing_char, "Use U+2018 after U+201A, not ASCII quote.")

    for index, char in enumerate(text):
        if char != OPEN_EN or index in paired_quote_indices or in_range(index):
            continue
        closing_index = None
        for probe in range(index + 1, len(text)):
            if in_range(probe):
                continue
            if text[probe] == WRONG_CLOSE_DE:
                closing_index = probe
                break
        if closing_index is not None:
            paired_quote_indices.update({index, closing_index})
            add_finding(findings, 46, "english_curly_quotes", index, char, "English curly quote pair in German prose; review German quote style.")

    for index, char in enumerate(text):
        if index in paired_quote_indices or in_range(index):
            continue
        if char == WRONG_CLOSE_DE:
            add_finding(findings, 46, "stray_wrong_german_closing_quote", index, char, "Wrong German closing quote without matching U+201E opener.")
        elif char == WRONG_CLOSE_SINGLE and not looks_like_german_apostrophe(text, index):
            add_finding(findings, 46, "stray_wrong_single_german_closing_quote", index, char, "Wrong single German closing quote without matching U+201A opener.")

    for index, char in enumerate(text):
        if char == ASCII_QUOTE and not in_range(index):
            add_finding(findings, 46, "straight_quote", index, char, "Straight ASCII quote in prose; review German quote style.")

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
    ranges = protected_ranges(text)
    in_range = range_checker(ranges)
    chars = []
    for index, char in enumerate(text):
        if is_hidden_char(char):
            continue
        chars.append(char)
    cleaned = "".join(chars)
    ranges = protected_ranges(cleaned)
    in_range = range_checker(ranges)
    chars = list(cleaned)

    for index, char in enumerate(chars):
        if char != OPEN_DE or in_range(index):
            continue
        for probe in range(index + 1, len(chars)):
            if in_range(probe):
                continue
            if chars[probe] == WRONG_CLOSE_DE:
                chars[probe] = CLOSE_DE
                break
            if chars[probe] in {CLOSE_DE, ASCII_QUOTE}:
                break
    for index, char in enumerate(chars):
        if char != OPEN_DE_SINGLE or in_range(index):
            continue
        for probe in range(index + 1, len(chars)):
            if in_range(probe):
                continue
            if chars[probe] == WRONG_CLOSE_SINGLE:
                chars[probe] = CLOSE_DE_SINGLE
                break
            if chars[probe] in {CLOSE_DE_SINGLE, ASCII_QUOTE}:
                break
    return "".join(chars)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint Humanizer-de Unicode patterns 43 and 46.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to lint.")
    source.add_argument("--file", type=Path, help="UTF-8 text file to lint.")
    parser.add_argument("--fix", action="store_true", help="Apply safe fixes in output.")
    parser.add_argument("--write", action="store_true", help="Write fixed text back to --file. Requires --fix.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.write and (not args.fix or not args.file):
        raise SystemExit("--write requires --fix and --file")

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

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
