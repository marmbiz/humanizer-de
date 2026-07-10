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
FENCE_OPEN_LINE_RE = re.compile(r"^[ \t]{0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
FENCE_CLOSE_LINE_RE = re.compile(r"^[ \t]{0,3}(?P<fence>`+|~+)[ \t]*$")

STRUCTURAL_PATTERNS = (
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


def fenced_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    open_fence: tuple[int, str, int] | None = None
    offset = 0

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if open_fence is None:
            match = FENCE_OPEN_LINE_RE.fullmatch(body)
            if match:
                fence = match.group("fence")
                info = match.group("info")
                if fence[0] != "`" or "`" not in info:
                    open_fence = (offset, fence[0], len(fence))
        else:
            start, delimiter, minimum_length = open_fence
            match = FENCE_CLOSE_LINE_RE.fullmatch(body)
            if match:
                fence = match.group("fence")
                if fence[0] == delimiter and len(fence) >= minimum_length:
                    ranges.append((start, offset + len(line)))
                    open_fence = None
        offset += len(line)

    if open_fence is not None:
        ranges.append((open_fence[0], len(text)))
    return ranges


def protected_ranges(text: str, scope: str = DOCUMENT_PROSE) -> list[tuple[int, int]]:
    if scope not in SCOPES:
        raise ValueError(f"unknown text scope: {scope}")

    ranges: list[tuple[int, int]] = []
    frontmatter = FRONTMATTER_RE.search(text)
    if frontmatter:
        ranges.append(frontmatter.span())
    ranges.extend(fenced_code_ranges(text))
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
