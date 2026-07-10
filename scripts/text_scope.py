#!/usr/bin/env python3
"""Offset-preserving Markdown structure scopes shared by text analyzers."""

from __future__ import annotations

import re


DOCUMENT_PROSE = "document_prose"
AUTHORED_PROSE = "authored_prose"
SCOPES = {DOCUMENT_PROSE, AUTHORED_PROSE}

BLOCKQUOTE_LINE_RE = re.compile(r"(?m)^[ \t]{0,3}>.*(?:\n|$)")
TABLE_LINE_RE = re.compile(r"(?m)^[ \t]*\|.*\|[ \t]*(?:\n|$)")
FRONTMATTER_RE = re.compile(
    r"\A(?:\ufeff)?---[ \t]*\r?\n.*?\r?\n(?:---|\.\.\.)[ \t]*(?=\r?\n|\Z)",
    re.DOTALL,
)

STRUCTURAL_PATTERNS = (
    re.compile(r"(?:```|~~~).*?(?:```|~~~)", re.DOTALL),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"https?://[^\s<>)]+"),
    re.compile(r"\b[\w.-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"<!--[\s\S]*?-->"),
    TABLE_LINE_RE,
    re.compile(r"(?m)^[ \t]*</?[A-Za-z][^>\n]*>[ \t]*(?:\n|$)"),
    re.compile(r"(?m)^[ \t]*<[A-Za-z][^>\n]*>.*</[A-Za-z][^>\n]*>[ \t]*(?:\n|$)"),
    re.compile(r"<[A-Za-z/!][^<>\n]*>"),
)


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def blockquote_ranges(text: str) -> list[tuple[int, int]]:
    return [match.span() for match in BLOCKQUOTE_LINE_RE.finditer(text)]


def protected_ranges(text: str, scope: str = DOCUMENT_PROSE) -> list[tuple[int, int]]:
    if scope not in SCOPES:
        raise ValueError(f"unknown text scope: {scope}")

    ranges: list[tuple[int, int]] = []
    frontmatter = FRONTMATTER_RE.search(text)
    if frontmatter:
        ranges.append(frontmatter.span())
    for pattern in STRUCTURAL_PATTERNS:
        ranges.extend(match.span() for match in pattern.finditer(text))
    if scope == AUTHORED_PROSE:
        ranges.extend(blockquote_ranges(text))
    return merge_ranges(ranges)


def mask_text(text: str, scope: str = DOCUMENT_PROSE) -> str:
    """Replace excluded content with spaces while preserving offsets and newlines."""
    chars = list(text)
    for start, end in protected_ranges(text, scope=scope):
        for index in range(start, end):
            if chars[index] not in {"\n", "\r"}:
                chars[index] = " "
    return "".join(chars)
