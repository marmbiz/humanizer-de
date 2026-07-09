#!/usr/bin/env python3
"""Report current false-positive corpus findings by file and kind."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "tests" / "fp_corpus"
SCRIPT_DIR = ROOT / "scripts"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


register_lint = load_module("register_lint")
german_pattern_lint = load_module("german_pattern_lint")
unicode_lint = load_module("unicode_lint")
rhythm_lint = load_module("rhythm_lint")
evidence_lint = load_module("evidence_lint")


def count(items: list[dict], counter: Counter[str]) -> None:
    for item in items:
        kind = item.get("kind") or item.get("reason")
        if kind:
            counter[kind] += 1


def markdown_findings(path: Path, precise: bool) -> dict[str, int]:
    text = path.read_text(encoding="utf-8")
    counter: Counter[str] = Counter()

    count(register_lint.lint(text, precise=precise)["findings"], counter)
    count(german_pattern_lint.lint(text, precise=precise)["findings"], counter)
    count(unicode_lint.lint(text), counter)
    count(rhythm_lint.analyze(text)["suspicions"], counter)

    return dict(sorted(counter.items()))


def evidence_findings(path: Path, precise: bool) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    counter: Counter[str] = Counter()
    count(evidence_lint.lint(data["before"], data["after"], precise=precise), counter)
    return dict(sorted(counter.items()))


def build_report(corpus_dir: Path = CORPUS_DIR, precise: bool = False) -> dict[str, dict[str, int]]:
    report: dict[str, dict[str, int]] = {}

    for path in sorted(corpus_dir.glob("*.md")):
        report[path.relative_to(ROOT).as_posix()] = markdown_findings(path, precise=precise)

    for path in sorted(corpus_dir.glob("*.json")):
        if path.name == "baseline.json":
            continue
        report[path.relative_to(ROOT).as_posix()] = evidence_findings(path, precise=precise)

    return dict(sorted(report.items()))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure the false-positive corpus.")
    parser.add_argument("--precise", action="store_true", help="Pass --precise behavior to supporting linters.")
    parser.add_argument("--corpus-dir", type=Path, default=CORPUS_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    print(json.dumps(build_report(args.corpus_dir, precise=args.precise), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
