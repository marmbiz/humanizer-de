#!/usr/bin/env python3
"""Optional hunspell-backed before/after invariant for new unknown words."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import print_json, resolve_exit_code


DICTIONARY = "de_DE"
WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)


def hunspell_binary() -> str | None:
    return shutil.which("hunspell")


def run_hunspell(text: str, binary: str | None = None) -> subprocess.CompletedProcess[str]:
    command = [binary or "hunspell", "-d", DICTIONARY, "-l"]
    return subprocess.run(
        command,
        input=text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def availability_reason() -> str | None:
    binary = hunspell_binary()
    if binary is None:
        return "hunspell_missing"

    try:
        result = run_hunspell("Test\n", binary=binary)
    except Exception:
        return "dictionary_missing"

    if result.returncode != 0:
        return "dictionary_missing"
    if result.stderr and "can't open" in result.stderr.casefold():
        return "dictionary_missing"
    return None


def unavailable_report(reason: str) -> dict:
    return {"available": False, "reason": reason, "findings": []}


def unknown_words(text: str) -> set[str]:
    words = "\n".join(WORD_RE.findall(text))
    result = run_hunspell(f"{words}\n" if words else "")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "hunspell failed")
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def diff_unknowns(before_set: set[str], after_set: set[str]) -> dict | None:
    new_words = after_set - before_set
    if not new_words:
        return None
    return {
        "kind": "new_unknown_words",
        "severity": "warning",
        "words": sorted(new_words),
    }


def lint(before: str, after: str) -> dict:
    reason = availability_reason()
    if reason is not None:
        return unavailable_report(reason)

    finding = diff_unknowns(unknown_words(before), unknown_words(after))
    findings = [finding] if finding is not None else []
    return {"ok": not findings, "available": True, "findings": findings}


def load_text(value: str | None, path: Path | None) -> str:
    if path is not None:
        return path.read_text(encoding="utf-8")
    return value or ""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare before/after passages for new hunspell-unknown words.")
    before = parser.add_mutually_exclusive_group(required=True)
    before.add_argument("--before", help="Before passage as inline text.")
    before.add_argument("--before-file", type=Path, help="Read before passage from file.")
    after = parser.add_mutually_exclusive_group(required=True)
    after.add_argument("--after", help="After passage as inline text.")
    after.add_argument("--after-file", type=Path, help="Read after passage from file.")
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="never")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    before = load_text(args.before, args.before_file)
    after = load_text(args.after, args.after_file)
    report = lint(before, after)
    print_json(report)
    findings = report["findings"] if report.get("available", True) else []
    return resolve_exit_code(args.fail_on, findings)


if __name__ == "__main__":
    raise SystemExit(main())
