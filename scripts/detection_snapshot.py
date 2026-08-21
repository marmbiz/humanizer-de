#!/usr/bin/env python3
"""Report current deterministic fixture coverage and tolerated false positives."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import (
    atomic_write_text,
    handle_cli_input_errors,
    json_for_stdout,
    print_json,
    read_json_object,
    read_user_text,
)
import doctor
import fp_corpus_report


CORPUS_DIR = ROOT / "tests" / "corpus"
FP_CORPUS_DIR = ROOT / "tests" / "fp_corpus"
FixtureChecker = Callable[[Path], dict]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def contract(expected: set, actual: set, *, exact: bool) -> dict:
    return {
        "expected": sorted(expected),
        "actual": sorted(actual),
        "missing": sorted(expected - actual),
        "additional": sorted(actual - expected),
        "contract_ok": actual == expected if exact else (expected <= actual if expected else not actual),
    }


def golden_contracts() -> list[dict]:
    results = []
    for input_path in sorted(CORPUS_DIR.glob("case_*_input.md")):
        expected_path = input_path.with_name(input_path.name.replace("_input.md", "_expected.json"))
        expected = read_json_object(expected_path, label="golden expectation")
        text = read_user_text(input_path)
        actual_by_source = {
            "unicode": {item["pattern"] for item in fp_corpus_report.unicode_lint.lint(text)},
            "rhythm": {
                item["pattern"]
                for item in fp_corpus_report.rhythm_lint.analyze(text, file=str(input_path))["suspicions"]
            },
        }
        for source, key in (("unicode", "unicode_patterns"), ("rhythm", "rhythm_patterns")):
            results.append(
                {
                    "fixture": relative(input_path),
                    "source": source,
                    **contract(set(expected[key]), actual_by_source[source], exact=False),
                }
            )
    return results


def kind_contracts(directory: Path, source: str, checker: FixtureChecker) -> list[dict]:
    results = []
    for path in sorted(directory.glob("*.json")):
        data = read_json_object(path, label="fixture", required=("text",))
        checked = checker(path)
        actual = {item["kind"] for item in checked["report"]["findings"]}
        results.append(
            {
                "fixture": relative(path),
                "source": source,
                **contract(set(data.get("expect_kinds", [])), actual, exact=True),
            }
        )
    return results


def fixture_hash() -> str:
    paths = sorted(
        [
            *CORPUS_DIR.glob("case_*"),
            *CORPUS_DIR.glob("de-naturalness/*.json"),
            *CORPUS_DIR.glob("register/*.json"),
            *FP_CORPUS_DIR.glob("*"),
        ]
    )
    digest = hashlib.sha256()
    for path in paths:
        if path.is_file():
            digest.update(relative(path).encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def build_snapshot(revision: str | None = None) -> dict:
    contracts = {
        "golden": golden_contracts(),
        "german_pattern": kind_contracts(
            CORPUS_DIR / "de-naturalness",
            "german_pattern",
            fp_corpus_report.german_pattern_lint.check_fixture,
        ),
        "register": kind_contracts(
            CORPUS_DIR / "register",
            "register",
            fp_corpus_report.register_lint.check_fixture,
        ),
    }
    flat_contracts = [item for group in contracts.values() for item in group]
    false_positives = fp_corpus_report.build_report()
    expected = sum(len(item["expected"]) for item in flat_contracts)
    missing = sum(len(item["missing"]) for item in flat_contracts)
    return {
        "schema_version": 1,
        "report_only": True,
        "version": doctor.skill_version(ROOT / "SKILL.md"),
        "revision": revision,
        "fixture_sha256": fixture_hash(),
        "summary": {
            "fixture_contracts": len(flat_contracts),
            "contract_failures": sum(not item["contract_ok"] for item in flat_contracts),
            "expected_detections": expected,
            "detected_expected": expected - missing,
            "additional_detections": sum(len(item["additional"]) for item in flat_contracts),
            "tolerated_false_positive_findings": sum(
                sum(findings.values()) for findings in false_positives.values()
            ),
        },
        "contracts": contracts,
        "false_positive_corpus": false_positives,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=os.environ.get("GITHUB_SHA"))
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the JSON snapshot atomically instead of stdout.",
    )
    args = parser.parse_args(argv)
    if args.output is not None and not args.output.parent.is_dir():
        parser.error(f"--output parent directory does not exist: {args.output.parent}")
    return args


@handle_cli_input_errors
def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    snapshot = build_snapshot(args.revision)
    if args.output is None:
        print_json(snapshot)
    else:
        atomic_write_text(args.output, json_for_stdout(snapshot) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
