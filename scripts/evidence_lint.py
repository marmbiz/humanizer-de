#!/usr/bin/env python3
"""Conservatively compare before/after passages for factual anchor drift."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ANCHOR_PATTERNS = {
    "number": re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:%|Prozent|Euro|EUR|km|kg|Mio\.?|Millionen)?\b", re.IGNORECASE),
    "date": re.compile(
        r"\b(?:\d{1,2}\.\s*(?:Januar|Februar|März|Maerz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4}|\d{4}-\d{2}-\d{2})\b",
        re.IGNORECASE,
    ),
    "url": re.compile(r"https?://[^\s<>)]+"),
    "doi": re.compile(r"\b(?:doi:\s*)?10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b", re.IGNORECASE),
    "paragraph": re.compile(r"§+\s*\d+[a-zA-Z]*(?:\s*Abs\.\s*\d+)?"),
    "code": re.compile(r"`[^`\n]+`"),
    "quote": re.compile(r"[\"„“‚‘”']([^\"„“‚‘”']{3,})[\"„“‚‘”']"),
}

AUTHORITY_MARKERS = {
    "strong": {"belegt", "beweist", "zeigt", "nachweislich", "muss", "immer"},
    "weak": {"kann", "koennte", "könnte", "vermutlich", "moeglicherweise", "möglicherweise", "laut", "scheint"},
}
DIRECTION_MARKERS = {
    "increase": {
        "erhoeht",
        "erhoehte",
        "erhöht",
        "erhöhte",
        "gestiegen",
        "stieg",
        "steigt",
        "verbessert",
        "verbesserte",
        "zunahm",
    },
    "decrease": {
        "gesunken",
        "nahm ab",
        "reduziert",
        "reduzierte",
        "sank",
        "senkt",
        "senkte",
        "verringert",
        "verringerte",
    },
}

CAPITALIZED_RE = re.compile(r"\b(?:[A-ZÄÖÜ][\wÄÖÜäöüß-]+(?:\s+[A-ZÄÖÜ][\wÄÖÜäöüß-]+){0,3})\b")
COMMON_SENTENCE_STARTS = {
    "Der",
    "Die",
    "Das",
    "Ein",
    "Eine",
    "Im",
    "In",
    "Nach",
    "Vor",
    "Zu",
    "Für",
    "Mit",
    "Ohne",
    "Sie",
    "Ihnen",
    "Ihr",
    "Ihre",
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).strip(".,;:()[]")


def anchors(text: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {kind: set() for kind in ANCHOR_PATTERNS}
    for kind, pattern in ANCHOR_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(1) if kind == "quote" else match.group(0)
            normalized = normalize(value)
            if normalized:
                result[kind].add(normalized)

    names: set[str] = set()
    for match in CAPITALIZED_RE.finditer(text):
        value = normalize(match.group(0))
        if value in COMMON_SENTENCE_STARTS:
            continue
        if len(value) <= 2:
            continue
        if value.lower() in {"prozent", "euro"}:
            continue
        names.add(value)
    result["proper_name"] = names
    return result


def authority_profile(text: str) -> dict[str, set[str]]:
    lowered = text.lower()
    return {
        level: {marker for marker in markers if re.search(rf"\b{re.escape(marker)}\b", lowered)}
        for level, markers in AUTHORITY_MARKERS.items()
    }


def direction_profile(text: str) -> set[str]:
    lowered = text.lower()
    result: set[str] = set()
    for direction, markers in DIRECTION_MARKERS.items():
        if any(re.search(rf"\b{re.escape(marker)}\b", lowered) for marker in markers):
            result.add(direction)
    return result


def add_finding(findings: list[dict], severity: str, kind: str, message: str, values: list[str]) -> None:
    findings.append({"severity": severity, "kind": kind, "message": message, "values": sorted(values)})


def lint(before: str, after: str) -> list[dict]:
    findings: list[dict] = []
    before_anchors = anchors(before)
    after_anchors = anchors(after)

    hard_kinds = {"number", "date", "url", "doi", "paragraph", "code", "quote"}
    for kind in sorted(before_anchors):
        removed = before_anchors[kind] - after_anchors.get(kind, set())
        added = after_anchors.get(kind, set()) - before_anchors[kind]
        severity = "blocker" if kind in hard_kinds else "warning"
        if removed:
            add_finding(findings, severity, f"removed_{kind}", f"{kind} anchor removed or changed.", list(removed))
        if added:
            add_finding(findings, severity, f"added_{kind}", f"New {kind} anchor introduced.", list(added))

    before_auth = authority_profile(before)
    after_auth = authority_profile(after)
    stronger = after_auth["strong"] - before_auth["strong"]
    weaker_removed = before_auth["weak"] - after_auth["weak"]
    if stronger:
        add_finding(findings, "blocker", "authority_strengthened", "Authority marker was strengthened.", list(stronger))
    if weaker_removed and after_auth["strong"]:
        add_finding(findings, "warning", "hedge_removed", "Hedging may have been removed.", list(weaker_removed))

    before_direction = direction_profile(before)
    after_direction = direction_profile(after)
    if (
        ("increase" in before_direction and "decrease" in after_direction)
        or ("decrease" in before_direction and "increase" in after_direction)
    ):
        add_finding(
            findings,
            "blocker",
            "claim_direction_changed",
            "Claim direction changed between increase and decrease.",
            sorted(before_direction | after_direction),
        )

    return findings


def load_text(value: str | None, path: Path | None) -> str:
    if path is not None:
        return path.read_text(encoding="utf-8")
    return value or ""


def check_fixture(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings = lint(data["before"], data["after"])
    expected = data.get("expect_kinds")
    ok = True
    if expected is not None:
        actual = {item["kind"] for item in findings}
        ok = actual == set(expected)
    return [{"fixture": str(path), "ok": ok, "findings": findings}]


def check_fixtures(path: Path) -> list[dict]:
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    return [item for file_path in files for item in check_fixture(file_path)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare before/after passages for factual anchor drift.")
    parser.add_argument("--before", help="Before passage as inline text.")
    parser.add_argument("--after", help="After passage as inline text.")
    parser.add_argument("--before-file", type=Path, help="Read before passage from file.")
    parser.add_argument("--after-file", type=Path, help="Read after passage from file.")
    parser.add_argument("--fixture", type=Path, help="JSON fixture file or directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.fixture:
        results = check_fixtures(args.fixture)
        print(json.dumps({"ok": all(item["ok"] for item in results), "results": results}, ensure_ascii=False, indent=2))
        return 0 if all(item["ok"] for item in results) else 1

    before = load_text(args.before, args.before_file)
    after = load_text(args.after, args.after_file)
    findings = lint(before, after)
    print(json.dumps({"ok": not findings, "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] == "blocker" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
