#!/usr/bin/env python3
"""Offset-preserving Markdown structure scopes shared by text analyzers."""

from __future__ import annotations

import re


DOCUMENT_PROSE = "document_prose"
AUTHORED_PROSE = "authored_prose"
TYPOGRAPHIC_PROSE = "typographic_prose"
SCOPES = {DOCUMENT_PROSE, AUTHORED_PROSE, TYPOGRAPHIC_PROSE}

BLOCKQUOTE_LINE_RE = re.compile(r"(?m)^[ \t]{0,3}>.*(?:\r?\n|$)")
TABLE_LINE_RE = re.compile(r"(?m)^[ \t]*\|.*\|[ \t]*(?:\r?\n|$)")
# Accepted edge case: prose like "Fazit: alles gut" can look like YAML when a closer follows.
FRONTMATTER_RE = re.compile(
    r"\A(?:\ufeff)?---[ \t]*\r?\n(?=[ \t]*[A-Za-z_][A-Za-z0-9_.-]*:(?:[ \t]|\r?\n)).*?\r?\n(?:---|\.\.\.)[ \t]*(?=\r?\n|\Z)",
    re.DOTALL,
)
FENCE_OPEN_LINE_RE = re.compile(r"^[ \t]{0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
FENCE_CLOSE_LINE_RE = re.compile(r"^[ \t]{0,3}(?P<fence>`+|~+)[ \t]*$")
BACKTICK_RUN_RE = re.compile(r"`+")
MARKDOWN_LINE_RE = re.compile(r"[^\r\n]*(?:\r\n|\r|\n|\Z)")
LIST_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<marker>[-+*]|\d{1,9}[.)])(?P<padding>[ \t]+|$)")

TECHNICAL_PATTERNS = (
    re.compile(r"https?://[^\s<>)]+"),
    re.compile(r"\b[\w.-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"<!--[\s\S]*?-->"),
    TABLE_LINE_RE,
    re.compile(r"<[A-Za-z/!][^<>\r\n]*>"),
)

STRUCTURAL_BLOCK_PATTERNS = (
    re.compile(r"(?m)^[ \t]*</?[A-Za-z][^>\r\n]*>[ \t]*(?:\r?\n|$)"),
)


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def serialize_spans(ranges: list[tuple[int, int]]) -> list[dict[str, int]]:
    """Return sorted, distinct Python-codepoint offsets for JSON findings."""
    return [
        {"start": start, "end": end}
        for start, end in sorted(set(ranges))
        if 0 <= start < end
    ]


def blockquote_ranges(text: str) -> list[tuple[int, int]]:
    return [match.span() for match in BLOCKQUOTE_LINE_RE.finditer(text)]


def markdown_lines(text: str):
    for match in MARKDOWN_LINE_RE.finditer(text):
        if match.start() < match.end():
            yield match.start(), match.group()


def fenced_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    open_fence: tuple[int, str, int] | None = None

    for offset, line in markdown_lines(text):
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

    if open_fence is not None:
        ranges.append((open_fence[0], len(text)))
    return ranges


def inline_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []

    for offset, line in markdown_lines(text):
        body = line.rstrip("\r\n")
        runs = list(BACKTICK_RUN_RE.finditer(body))
        open_lengths: list[int] = []
        open_starts: list[int] = []
        for run in runs:
            start = run.start()
            length = len(run.group())
            backslashes = 0
            index = start - 1
            while index >= 0 and body[index] == "\\":
                backslashes += 1
                index -= 1
            if backslashes % 2:
                start += 1
                length -= 1
            open_starts.append(start)
            open_lengths.append(length)

        closers: list[int | None] = [None] * len(runs)
        next_run_by_length: dict[int, int] = {}
        for index in range(len(runs) - 1, -1, -1):
            length = open_lengths[index]
            if length:
                closers[index] = next_run_by_length.get(length)
            next_run_by_length[len(runs[index].group())] = index

        index = 0
        while index < len(runs):
            closer = closers[index]
            if closer is None:
                index += 1
                continue
            ranges.append((offset + open_starts[index], offset + runs[closer].end()))
            index = closer + 1
    return ranges


def indented_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    list_items: list[tuple[int, int]] = []
    code_start: int | None = None
    code_end = 0
    previous_blank = True

    for offset, line in markdown_lines(text):
        body = line.rstrip("\r\n")
        if not body.strip(" \t"):
            previous_blank = True
            continue

        indentation = 0
        for char in body:
            if char == " ":
                indentation += 1
            elif char == "\t":
                indentation += 4 - indentation % 4
            else:
                break

        marker = LIST_ITEM_RE.match(body)
        list_threshold = list_items[-1][1] + 4 if list_items else 4
        if marker and indentation < list_threshold:
            marker_indent = indentation
            while list_items and list_items[-1][0] >= marker_indent:
                list_items.pop()
            marker_end = indentation + len(marker.group("marker"))
            if body[marker.end():].strip(" \t"):
                content_indent = marker_end
                for char in marker.group("padding"):
                    if char == "\t":
                        content_indent += 4 - content_indent % 4
                    else:
                        content_indent += 1
                if content_indent - marker_end > 4:
                    content_indent = marker_end + 1
            else:
                content_indent = marker_end + 1
            list_items.append((marker_indent, content_indent))
        else:
            marker = None

        if not marker and list_items and indentation < list_items[-1][1]:
            stripped = body.lstrip(" \t")
            block_start = (
                re.match(r"#{1,6}(?:[ \t]|$)", stripped) is not None
                or stripped.startswith((">", "```", "~~~"))
                or re.fullmatch(r"(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,}", stripped) is not None
            )
            if previous_blank or block_start or code_start is not None:
                while list_items and indentation < list_items[-1][1]:
                    list_items.pop()
        threshold = list_items[-1][1] + 4 if list_items and not marker else 4
        is_indented_code = marker is None and indentation >= threshold

        if code_start is not None:
            if is_indented_code:
                code_end = offset + len(line)
            else:
                ranges.append((code_start, code_end))
                code_start = None
        elif is_indented_code and previous_blank:
            code_start = offset
            code_end = offset + len(line)

        previous_blank = False

    if code_start is not None:
        ranges.append((code_start, code_end))
    return ranges


def protected_ranges(text: str, scope: str = DOCUMENT_PROSE) -> list[tuple[int, int]]:
    if scope not in SCOPES:
        raise ValueError(f"unknown text scope: {scope}")

    ranges: list[tuple[int, int]] = []
    frontmatter = FRONTMATTER_RE.search(text)
    if frontmatter:
        ranges.append(frontmatter.span())
    ranges.extend(fenced_code_ranges(text))
    ranges.extend(inline_code_ranges(text))
    ranges.extend(indented_code_ranges(text))
    for pattern in TECHNICAL_PATTERNS:
        ranges.extend(match.span() for match in pattern.finditer(text))
    if scope in {DOCUMENT_PROSE, AUTHORED_PROSE}:
        for pattern in STRUCTURAL_BLOCK_PATTERNS:
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
