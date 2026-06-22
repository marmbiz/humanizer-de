#!/usr/bin/env python3
"""Check deterministic invariants for Humanizer-de scenario review outputs.

Scenario files use a JSON subset of YAML so the runner has no third-party dependency.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCRIPT = ROOT / "scripts" / "evidence_lint.py"
spec = importlib.util.spec_from_file_location("evidence_lint", EVIDENCE_SCRIPT)
evidence_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence_lint)

REQUIRED_KEYS = {"id", "mode", "input", "expected_behavior", "forbidden_changes", "output_contract"}
PERSONAL_EXPERIENCE_RE = re.compile(
    r"\b(?:Als ich|ich habe erlebt|ein Kunde erzählte|aus meiner Praxis|letzte Woche)\b",
    re.IGNORECASE,
)


def words(text: str) -> list[str]:
    return re.findall(r"\S+", text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def load_scenario(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - set(data)
    if missing:
        raise ValueError(f"{path}: missing keys {sorted(missing)}")
    return data


def invariant_violations(scenario: dict, output: str) -> list[str]:
    violations: list[str] = []
    input_text = scenario["input"]
    output_norm = normalize(output)
    input_norm = normalize(input_text)

    if input_norm and input_norm in output_norm:
        violations.append("full_text_output")
    elif len(words(output)) >= max(80, int(len(words(input_text)) * 0.8)):
        violations.append("possible_full_text_output")

    evidence_findings = evidence_lint.lint(input_text, output)
    if any(
        item["severity"] == "blocker" and (item["kind"].startswith("added_") or item["kind"].startswith("removed_"))
        for item in evidence_findings
    ) or any(item["kind"] == "added_proper_name" for item in evidence_findings):
        violations.append("new_factual_anchor")
    if any(item["kind"] == "authority_strengthened" for item in evidence_findings):
        violations.append("authority_strengthened")

    if PERSONAL_EXPERIENCE_RE.search(output) and not PERSONAL_EXPERIENCE_RE.search(input_text):
        violations.append("invented_experience")

    if scenario["mode"] == "Formal" and re.search(r"\b(?:du|dir|dich|ja|doch|halt|spannend\?)\b", output, re.IGNORECASE):
        violations.append("formal_register_break")

    for forbidden in scenario.get("forbidden_phrases", []):
        if forbidden.lower() in output.lower():
            violations.append("forbidden_phrase")
            break

    return sorted(set(violations))


def check_scenario(path: Path) -> dict:
    scenario = load_scenario(path)
    sample_results = []
    ok = True
    for sample in scenario.get("sample_outputs", []):
        actual = set(invariant_violations(scenario, sample["text"]))
        expected = set(sample.get("expect_violations", []))
        sample_ok = expected.issubset(actual)
        ok = ok and sample_ok
        sample_results.append(
            {
                "name": sample.get("name", "sample"),
                "ok": sample_ok,
                "expected": sorted(expected),
                "actual": sorted(actual),
            }
        )
    return {"file": str(path), "id": scenario["id"], "ok": ok, "sample_results": sample_results}


def scenario_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(list(path.glob("*.yaml")) + list(path.glob("*.yml")) + list(path.glob("*.json")))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Humanizer-de scenario contracts.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--check-invariants", action="store_true", help="Check sample output invariants.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    results = [check_scenario(path) for path in scenario_files(args.path)]
    ok = all(item["ok"] for item in results)
    print(json.dumps({"ok": ok, "count": len(results), "results": results}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
