#!/usr/bin/env python3
"""Check deterministic invariants for Humanizer-de scenario review outputs.

Scenario files use a JSON subset of YAML so the runner has no third-party dependency.
"""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
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

REGISTER_SCRIPT = ROOT / "scripts" / "register_lint.py"
register_spec = importlib.util.spec_from_file_location("register_lint", REGISTER_SCRIPT)
register_lint = importlib.util.module_from_spec(register_spec)
register_spec.loader.exec_module(register_lint)

RHYTHM_SCRIPT = ROOT / "scripts" / "rhythm_lint.py"
rhythm_spec = importlib.util.spec_from_file_location("rhythm_lint", RHYTHM_SCRIPT)
rhythm_lint = importlib.util.module_from_spec(rhythm_spec)
rhythm_spec.loader.exec_module(rhythm_lint)

STYLE_PROFILE_SCRIPT = ROOT / "scripts" / "style_profile.py"
style_profile_spec = importlib.util.spec_from_file_location("style_profile", STYLE_PROFILE_SCRIPT)
style_profile = importlib.util.module_from_spec(style_profile_spec)
style_profile_spec.loader.exec_module(style_profile)

REQUIRED_KEYS = {"id", "mode", "input", "expected_behavior", "quality_risks", "output_contract"}
PRELUDE_RE = re.compile(r"less machine\.\s*more voice\.", re.IGNORECASE)
PERSONAL_EXPERIENCE_RE = re.compile(
    r"\b(?:Als ich|ich habe erlebt|ein Kunde erzählte|aus meiner Praxis|letzte Woche)\b",
    re.IGNORECASE,
)
DU_RE = re.compile(rf"\b(?:{'|'.join(re.escape(form) for form in register_lint.DU_FORMS)})\b", re.IGNORECASE)
SIE_RE = re.compile(rf"\b(?:{'|'.join(re.escape(form) for form in register_lint.SIE_FORMS)})\b")
SENTENCE_SIMILARITY_THRESHOLD = 0.72


def words(text: str) -> list[str]:
    return re.findall(r"\S+", text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def sentences(text: str) -> list[str]:
    normalized: list[str] = []
    for item in rhythm_lint.split_sentences(text):
        sentence = normalize(item)
        if sentence:
            normalized.append(sentence)
    return normalized


def changed_sentence_ratio(before: str, after: str) -> float:
    before_sentences = sentences(before)
    after_sentences = sentences(after)
    if not before_sentences:
        return 0.0 if not after_sentences else 1.0
    if not after_sentences:
        return 1.0

    changed = 0
    for before_sentence in before_sentences:
        best = max(
            SequenceMatcher(None, before_sentence.lower(), after_sentence.lower()).ratio()
            for after_sentence in after_sentences
        )
        if best < SENTENCE_SIMILARITY_THRESHOLD:
            changed += 1

    added = 0
    for after_sentence in after_sentences:
        best = max(
            SequenceMatcher(None, after_sentence.lower(), before_sentence.lower()).ratio()
            for before_sentence in before_sentences
        )
        if best < SENTENCE_SIMILARITY_THRESHOLD:
            added += 1

    before_count = len(before_sentences)
    sentence_count_delta = abs(len(after_sentences) - before_count) / before_count
    before_chars = len(normalize(before))
    after_chars = len(normalize(after))
    char_expansion = max(0, after_chars - before_chars) / max(1, before_chars)
    return max(changed / before_count, added / before_count, sentence_count_delta, char_expansion)


def qgir_pass_trace(sample: dict) -> tuple[list[str], bool]:
    if "passes" not in sample:
        return [], False
    passes = sample["passes"]
    if not isinstance(passes, list) or not all(isinstance(item, str) for item in passes):
        return [], False
    return passes, True


def sample_output(sample: dict) -> str:
    text = sample.get("text")
    if isinstance(text, str):
        return text
    passes, valid_pass_trace = qgir_pass_trace(sample)
    return passes[-1] if valid_pass_trace and passes else ""


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

    evidence_findings = [] if scenario.get("machine_output") else evidence_lint.lint(input_text, output)
    if any(
        item["severity"] == "blocker" and (item["kind"].startswith("added_") or item["kind"].startswith("removed_"))
        for item in evidence_findings
    ) or any(item["kind"] == "added_proper_name" for item in evidence_findings):
        violations.append("new_factual_anchor")
    if any(item["kind"] == "authority_strengthened" for item in evidence_findings):
        violations.append("authority_strengthened")
    if any(item["kind"] == "claim_direction_changed" for item in evidence_findings):
        violations.append("claim_direction_changed")

    if PERSONAL_EXPERIENCE_RE.search(output) and not PERSONAL_EXPERIENCE_RE.search(input_text):
        violations.append("invented_experience")

    if scenario["mode"] == "Formal" and re.search(r"\b(?:du|dir|dich|ja|doch|halt|spannend\?)\b", output, re.IGNORECASE):
        violations.append("formal_register_break")

    for risky_phrase in scenario.get("risk_phrases", []):
        if risky_phrase.lower() in output.lower():
            violations.append("risky_phrase")
            break

    if scenario.get("machine_output") and PRELUDE_RE.search(output):
        violations.append("branding_prelude_in_machine_output")

    return sorted(set(violations))


def qgir_violations(scenario: dict, sample: dict) -> list[str]:
    contract = scenario.get("qgir_contract")
    if not contract:
        return []

    violations: list[str] = []
    passes, valid_pass_trace = qgir_pass_trace(sample)
    output = sample_output(sample)
    input_text = scenario["input"]

    max_passes = contract.get("max_passes")
    if max_passes is not None:
        if not valid_pass_trace:
            violations.append("qgir_missing_pass_trace")
        elif len(passes) > max_passes:
            violations.append("qgir_too_many_passes")

    max_changed_ratio = contract.get("max_changed_sentence_ratio")
    if max_changed_ratio is not None and changed_sentence_ratio(input_text, output) > float(max_changed_ratio):
        violations.append("edit_budget_exceeded")

    for anchor in contract.get("protected_anchors", []):
        if anchor not in output:
            violations.append("missing_protected_anchor")
            break

    required_address = contract.get("required_address")
    if required_address == "Sie" and (DU_RE.search(output) or (SIE_RE.search(input_text) and not SIE_RE.search(output))):
        violations.append("register_shift")
    elif required_address == "du" and (SIE_RE.search(output) or (DU_RE.search(input_text) and not DU_RE.search(output))):
        violations.append("register_shift")

    for marker in contract.get("register_drift_markers", []):
        if re.search(rf"\b{re.escape(marker)}\b", output, re.IGNORECASE):
            violations.append("register_shift")
            break

    return sorted(set(violations))


def style_profile_violations(scenario: dict, sample: dict) -> list[str]:
    contract = scenario.get("style_profile_contract")
    if not contract:
        return []

    violations: list[str] = []
    output = sample_output(sample)
    corridors = style_profile.load_targets()[contract["target"]]
    report = style_profile.delta(style_profile.profile(output, "<sample>")["metrics"], corridors)

    max_out_of_range = contract.get("max_out_of_range")
    if max_out_of_range is not None:
        out_of_range = sum(1 for item in report.values() if not item["in_range"])
        if out_of_range > max_out_of_range:
            violations.append("profile_out_of_range")

    for metric in contract.get("required_in_range", []):
        if not report[metric]["in_range"]:
            violations.append("profile_required_metric_failed")
            break

    return sorted(set(violations))


def check_scenario(path: Path, check_invariants: bool = True) -> dict:
    scenario = load_scenario(path)
    if not check_invariants:
        return {"file": str(path), "id": scenario["id"], "ok": True, "sample_results": []}
    sample_results = []
    ok = True
    for sample in scenario.get("sample_outputs", []):
        output = sample_output(sample)
        actual = (
            set(invariant_violations(scenario, output))
            | set(qgir_violations(scenario, sample))
            | set(style_profile_violations(scenario, sample))
        )
        expected = set(sample.get("expect_violations", []))
        if sample.get("expect_violations_exact"):
            sample_ok = expected == actual
        else:
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
    parser.add_argument(
        "--check-invariants",
        action="store_true",
        help="Check sample output invariants after loading scenario files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    results = [check_scenario(path, check_invariants=args.check_invariants) for path in scenario_files(args.path)]
    ok = all(item["ok"] for item in results)
    print(
        json.dumps(
            {"ok": ok, "count": len(results), "checked_invariants": args.check_invariants, "results": results},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
