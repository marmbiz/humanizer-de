#!/usr/bin/env python3
"""Measure the changes between two edited text files without judging them."""

from __future__ import annotations

import argparse
import sys
from difflib import SequenceMatcher
from itertools import zip_longest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import rhythm_lint
import text_scope
from cli_output import handle_cli_input_errors, print_json, print_text, read_user_text, require_file


TYPOGRAPHY = ('"', "'", "„", "“", "”", "‚", "‘", "’", "—", "–", ";", " -- ")


def token_changes(before: str, after: str) -> dict:
    before_tokens = rhythm_lint.tokens(text_scope.mask_text(before))
    after_tokens = rhythm_lint.tokens(text_scope.mask_text(after))
    replaced = inserted = deleted = 0

    for tag, before_start, before_end, after_start, after_end in SequenceMatcher(
        None, before_tokens, after_tokens, autojunk=False
    ).get_opcodes():
        before_size = before_end - before_start
        after_size = after_end - after_start
        if tag == "replace":
            paired = min(before_size, after_size)
            replaced += paired
            deleted += before_size - paired
            inserted += after_size - paired
        elif tag == "delete":
            deleted += before_size
        elif tag == "insert":
            inserted += after_size

    changed = replaced + inserted + deleted
    ratio = changed / len(before_tokens) if before_tokens else (1.0 if changed else 0.0)
    return {
        "before": len(before_tokens),
        "after": len(after_tokens),
        "replaced": replaced,
        "inserted": inserted,
        "deleted": deleted,
        "changed_ratio": round(ratio, 3),
    }


def typography_changes(before: str, after: str) -> dict:
    before_prose = text_scope.mask_text(before)
    after_prose = text_scope.mask_text(after)
    return {
        symbol: {
            "before": before_prose.count(symbol),
            "after": after_prose.count(symbol),
            "delta": after_prose.count(symbol) - before_prose.count(symbol),
        }
        for symbol in TYPOGRAPHY
    }


def line_value(line: str | None) -> tuple[str | None, bool]:
    if line is None:
        return None, False
    value = line.removesuffix("\n").removesuffix("\r")
    return value[:200], len(value) > 200


def changed_lines(before: str, after: str) -> dict:
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)
    total = 0
    pairs = []

    for tag, before_start, before_end, after_start, after_end in SequenceMatcher(
        None, before_lines, after_lines, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            continue
        for before_line, after_line in zip_longest(
            before_lines[before_start:before_end], after_lines[after_start:after_end]
        ):
            total += 1
            if len(pairs) == 10:
                continue
            before_value, before_truncated = line_value(before_line)
            after_value, after_truncated = line_value(after_line)
            pairs.append(
                {
                    "before": before_value,
                    "after": after_value,
                    "truncated": before_truncated or after_truncated,
                }
            )

    return {"count": total, "pairs": pairs}


def build_report(before: str, after: str) -> dict:
    return {
        "identical": before == after,
        "tokens": token_changes(before, after),
        "typography": typography_changes(before, after),
        "changed_lines": changed_lines(before, after),
    }


def markdown(report: dict) -> str:
    tokens = report["tokens"]
    typography = [
        f"{symbol!r} {entry['delta']:+d}"
        for symbol, entry in report["typography"].items()
        if entry["delta"]
    ]
    lines = [
        f"Identical: {str(report['identical']).lower()}",
        (
            f"Tokens: {tokens['before']} -> {tokens['after']}; "
            f"replaced {tokens['replaced']}, inserted {tokens['inserted']}, "
            f"deleted {tokens['deleted']}; changed_ratio {tokens['changed_ratio']}"
        ),
        f"Typography: {', '.join(typography) if typography else 'no deltas'}",
        (
            f"ChangedLines: {report['changed_lines']['count']} "
            f"(showing {len(report['changed_lines']['pairs'])})"
        ),
    ]
    for pair in report["changed_lines"]["pairs"]:
        lines.append(f"- {pair['before'] or ''} => {pair['after'] or ''}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure actual changes between two text files.")
    parser.add_argument("--before-file", required=True, type=Path, help="UTF-8 file before editing.")
    parser.add_argument("--after-file", required=True, type=Path, help="UTF-8 file after editing.")
    parser.add_argument("--format", choices=("json", "md"), default="json", help="Output format (default: json).")
    args = parser.parse_args(argv)
    require_file(parser, args.before_file, "--before-file")
    require_file(parser, args.after_file, "--after-file")
    return args


@handle_cli_input_errors
def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = build_report(read_user_text(args.before_file), read_user_text(args.after_file))
    if args.format == "md":
        print_text(markdown(report))
    else:
        print_json(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
