#!/usr/bin/env python3
"""Run compact Humanizer-de single-file audits in one process."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import german_pattern_lint
import register_lint
import rhythm_lint
import unicode_lint


SOURCES = ("unicode", "rhythm", "german_pattern", "register")
RHYTHM_KEYS = (
    "sentence_count",
    "mean_sentence_length",
    "stddev_mean_ratio",
    "subject_initial_ratio",
    "connector_density",
    "heading_count",
    "colon_heading_count",
    "paragraph_sentence_counts_uniform",
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run compact Humanizer-de lint audit.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="UTF-8 text file to audit.")
    source.add_argument("--latest", type=Path, help="Directory whose newest recursive *.md file should be audited.")
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default="sachlich")
    parser.add_argument("--format", choices=["json", "md"], default="json")
    return parser.parse_args(argv)


def latest_markdown_file(directory: Path) -> Path:
    if not directory.is_dir():
        raise ValueError("--latest requires a directory")
    candidates = [path for path in directory.rglob("*.md") if path.is_file()]
    if not candidates:
        raise ValueError(f"No *.md files found under {directory}")
    return max(candidates, key=lambda path: (path.stat().st_mtime, str(path)))


def input_path(args: argparse.Namespace) -> Path:
    if args.file:
        if not args.file.is_file():
            raise ValueError("--file requires an existing file")
        return args.file
    return latest_markdown_file(args.latest)


def short_text(value: object, width: int = 140) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    if len(text) <= width:
        return text
    return text[: max(0, width - 3)].rstrip() + "..."


def evidence_summary(evidence: object) -> str:
    if isinstance(evidence, dict):
        parts = [f"{key}={value}" for key, value in sorted(evidence.items())[:5]]
        if len(evidence) > 5:
            parts.append(f"+{len(evidence) - 5} more")
        return ", ".join(parts)
    if isinstance(evidence, list):
        parts = [short_text(item, width=50) for item in evidence[:3]]
        if len(evidence) > 3:
            parts.append(f"+{len(evidence) - 3} more")
        return ", ".join(parts)
    return short_text(evidence)


def rhythm_summary(report: dict) -> dict:
    document = report.get("document", {})
    return {key: document.get(key, 0) for key in RHYTHM_KEYS}


def compact_unicode_findings(findings: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for item in findings:
        kind = item.get("kind", "unknown")
        if kind not in grouped:
            grouped[kind] = {"first": item, "count": 0}
        grouped[kind]["count"] += 1

    compact: list[dict] = []
    for kind, group in grouped.items():
        first = group["first"]
        compact.append(
            {
                "source": "unicode",
                "pattern": first.get("pattern", 0),
                "kind": kind,
                "severity": "warning",
                "count": group["count"],
                "summary": short_text(first.get("message", kind)),
            }
        )
    return compact


def compact_rhythm_findings(suspicions: list[dict]) -> list[dict]:
    compact: list[dict] = []
    for item in suspicions:
        summary = item.get("reason", "rhythm suspicion")
        if item.get("evidence"):
            summary = f"{summary}: {item['evidence']}"
        compact.append(
            {
                "source": "rhythm",
                "pattern": item.get("pattern", 0),
                "severity": item.get("severity", "warning"),
                "summary": short_text(summary),
            }
        )
    return compact


def compact_german_pattern_findings(findings: list[dict]) -> list[dict]:
    compact: list[dict] = []
    for item in findings:
        summary = item.get("kind", "german pattern")
        if "evidence" in item:
            summary = f"{summary}: {evidence_summary(item['evidence'])}"
        compact.append(
            {
                "source": "german_pattern",
                "pattern": item.get("pattern", 0),
                "kind": item.get("kind", "unknown"),
                "severity": item.get("severity", "warning"),
                "summary": short_text(summary),
            }
        )
    return compact


def compact_register_findings(findings: list[dict]) -> list[dict]:
    compact: list[dict] = []
    for item in findings:
        compact.append(
            {
                "source": "register",
                "pattern": 0,
                "kind": item.get("kind", "unknown"),
                "severity": item.get("severity", "warning"),
                "summary": short_text(item.get("message", item.get("kind", "register finding"))),
            }
        )
    return compact


def analyze_file(path: Path, mode: str) -> dict:
    text = path.read_text(encoding="utf-8")

    unicode_findings = unicode_lint.lint(text)
    rhythm_report = rhythm_lint.analyze(text, file=str(path), scope="user_text", mode=mode)
    german_report = german_pattern_lint.lint(text, mode=mode)
    register_report = register_lint.lint(text, mode=mode)

    counts = {
        "unicode": len(unicode_findings),
        "rhythm": len(rhythm_report["suspicions"]),
        "german_pattern": len(german_report["findings"]),
        "register": len(register_report["findings"]),
    }
    findings = (
        compact_unicode_findings(unicode_findings)
        + compact_rhythm_findings(rhythm_report["suspicions"])
        + compact_german_pattern_findings(german_report["findings"])
        + compact_register_findings(register_report["findings"])
    )

    return {
        "file": str(path),
        "mode": mode,
        "ok": sum(counts.values()) == 0,
        "summary": {
            "rhythm": rhythm_summary(rhythm_report),
            "counts": counts,
        },
        "findings": findings,
    }


def md_finding_line(item: dict) -> str:
    kind = f" {item['kind']}" if item.get("kind") else ""
    count = f" x{item['count']}" if item.get("count") else ""
    return f"- {item['severity']} pattern {item['pattern']}{kind}{count}: {item['summary']}"


def format_markdown(report: dict) -> str:
    rhythm = report["summary"]["rhythm"]
    lines = [
        f"Mode: {report['mode']}",
        f"File: {report['file']}",
        (
            "Rhythm: "
            f"sentences={rhythm['sentence_count']}, "
            f"mean={rhythm['mean_sentence_length']}, "
            f"stddev/mean={rhythm['stddev_mean_ratio']}, "
            f"subject_initial={rhythm['subject_initial_ratio']}, "
            f"connectors={rhythm['connector_density']}, "
            f"headings={rhythm['heading_count']}, "
            f"colon_headings={rhythm['colon_heading_count']}, "
            f"uniform_paragraphs={str(rhythm['paragraph_sentence_counts_uniform']).lower()}"
        ),
        "Findings:",
    ]
    for source in SOURCES:
        lines.append(f"{source}:")
        source_findings = [item for item in report["findings"] if item["source"] == source]
        if source_findings:
            lines.extend(md_finding_line(item) for item in source_findings)
        else:
            lines.append("- none")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        path = input_path(args)
    except ValueError as error:
        raise SystemExit(str(error))

    report = analyze_file(path, args.mode)
    if args.format == "md":
        print(format_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
