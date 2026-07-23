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
import style_profile
import syntax_lint
import unicode_lint
from cli_output import print_json, resolve_exit_code


SOURCES = ("unicode", "rhythm", "german_pattern", "register")
RHYTHM_KEYS = (
    "sentence_count",
    "mean_sentence_length",
    "stddev_sentence_length",
    "stddev_mean_ratio",
    "sentence_length_buckets",
    "syntactic_complexity_variance",
    "subject_initial_ratio",
    "connector_density",
    "heading_count",
    "colon_heading_count",
    "paragraph_sentence_counts_uniform",
)
LATEST_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site",
    "venv",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run compact Humanizer-de lint audit.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="UTF-8 text file to audit.")
    source.add_argument("--latest", type=Path, help="Directory whose newest recursive *.md file should be audited.")
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default=None)
    parser.add_argument("--format", choices=["json", "md"], default="json")
    user_profile = parser.add_mutually_exclusive_group()
    user_profile.add_argument(
        "--profile",
        type=Path,
        help="User profile JSON with corridor overrides (default: .humanizer/profile.json).",
    )
    user_profile.add_argument(
        "--no-profile",
        action="store_true",
        help="Ignore any user profile (.humanizer/profile.json); use base targets only.",
    )
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="never")
    return parser.parse_args(argv)


def latest_markdown_file(directory: Path) -> Path:
    if not directory.is_dir():
        raise ValueError("--latest requires a directory")
    candidates = []
    for path in directory.rglob("*.md"):
        if not path.is_file() or path.is_symlink():
            continue
        relative_parts = path.relative_to(directory).parts
        if any(part.startswith(".") or part in LATEST_EXCLUDED_DIRS for part in relative_parts):
            continue
        candidates.append(path)
    if not candidates:
        raise ValueError(f"No eligible *.md files found under {directory}")
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


def add_driver(drivers: list[dict], kind: str, detail: str, weight: int) -> int:
    drivers.append({"kind": kind, "detail": detail, "weight": weight})
    return weight


def preflight_assessment(
    rhythm_report: dict,
    german_findings: list[dict],
    register_findings: list[dict],
    mode: str,
) -> dict:
    document = rhythm_report.get("document", {})
    sentence_count = document.get("sentence_count", 0)
    drivers: list[dict] = []
    score = 0
    quality_warning = (
        "Combing may improve burstiness or mimicry metrics, but it can degrade text quality, "
        "precision, readability, or register."
    )
    short_sample = sentence_count < 8
    if short_sample:
        add_driver(
            drivers,
            "short_sample",
            f"sentence_count={sentence_count}; rhythm preflight needs at least 8",
            0,
        )

    stddev_ratio = document.get("stddev_mean_ratio", 0.0)
    subject_ratio = document.get("subject_initial_ratio", 0.0)
    opener_count = len(document.get("repeated_openers", []))
    connector_count = max(document.get("connector_density_by_paragraph", []), default=0)
    buckets = document.get("sentence_length_buckets", {}).get("ratios", {})
    short_ratio = buckets.get("short_lt_12", 0.0)
    long_ratio = buckets.get("long_gt_28", 0.0)

    if not short_sample and stddev_ratio < 0.4:
        score += add_driver(drivers, "low_burstiness", f"stddev/mean={stddev_ratio}", 2)
    if not short_sample and short_ratio < 0.15 and long_ratio < 0.1:
        score += add_driver(
            drivers,
            "compressed_sentence_mix",
            f"short_lt_12={short_ratio}, long_gt_28={long_ratio}",
            1,
        )
    if not short_sample and opener_count >= 2:
        score += add_driver(drivers, "repeated_openers", f"count={opener_count}", 2)
    if not short_sample and subject_ratio > 0.85 and (stddev_ratio < 0.6 or opener_count >= 2):
        score += add_driver(drivers, "subject_initial_cluster", f"subject_initial_ratio={subject_ratio}", 1)
    if not short_sample and document.get("paragraph_sentence_counts_uniform"):
        score += add_driver(drivers, "uniform_paragraphs", "paragraph sentence counts are near-uniform", 1)
    if not short_sample and connector_count > 1:
        score += add_driver(
            drivers,
            "mechanical_connectors",
            f"max_connector_density_per_paragraph={connector_count}",
            1,
        )

    weighted_kinds = {
        "ai_marker_cluster": 2,
        "copula_avoidance_cluster": 1,
        "abstraction_cluster": 1,
        "colon_heading_cluster": 1,
    }
    for item in german_findings:
        kind = item.get("kind", "")
        if kind in weighted_kinds:
            score += add_driver(drivers, kind, evidence_summary(item.get("evidence", "")), weighted_kinds[kind])

    if any(item.get("severity") == "blocker" for item in register_findings):
        score += add_driver(drivers, "register_blocker", "register drift blocks automatic stylization", 0)

    if short_sample and score == 0:
        risk = "insufficient_text"
    elif score >= 4:
        risk = "high"
    elif score >= 2:
        risk = "medium"
    else:
        risk = "low"

    if risk == "insufficient_text":
        recommendation = "audit_only"
        combing = {"auto": False, "max_iterations": 0, "reason": "too_few_sentences"}
    elif mode == "formal":
        recommendation = "humanizer_pass_without_auto_combing"
        combing = {"auto": False, "max_iterations": 0, "reason": "formal_mode"}
    elif risk == "high":
        recommendation = "humanizer_pass_plus_combing"
        combing = {"auto": True, "max_iterations": 2, "reason": "strong_cluster"}
    elif risk == "medium":
        recommendation = "humanizer_pass; combing_if_rhythm_remains"
        combing = {"auto": False, "max_iterations": 2, "reason": "review_after_pass_5"}
    else:
        recommendation = "no_rewrite_or_local_edit_only"
        combing = {"auto": False, "max_iterations": 0, "reason": "no_cluster"}

    return {
        "risk": risk,
        "score": score,
        "drivers": drivers[:6],
        "recommendation": recommendation,
        "combing": combing,
        "quality_warning": quality_warning,
    }


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
        summary = item.get("message", item.get("kind", "german pattern"))
        if "evidence" in item:
            summary = f"{summary}: {evidence_summary(item['evidence'])}"
        compact_item = {
            "source": "german_pattern",
            "pattern": item.get("pattern", 0),
            "kind": item.get("kind", "unknown"),
            "severity": item.get("severity", "warning"),
            "summary": short_text(summary),
        }
        if item.get("advisory"):
            compact_item["advisory"] = True
        compact.append(compact_item)
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


def style_profile_section(
    text: str,
    path: Path,
    mode: str,
    mode_explicit: bool,
    use_profile: bool = True,
    profile_path: Path = style_profile.USER_PROFILE_PATH,
) -> dict:
    profile_report = style_profile.profile(text, str(path))
    section = {
        "word_count": profile_report["meta"]["word_count"],
        "sentence_count": profile_report["meta"]["sentence_count"],
        "metrics": profile_report["metrics"],
    }
    if mode_explicit:
        targets = style_profile.load_targets()
        overridden: frozenset = frozenset()
        if use_profile:
            overrides, warnings = style_profile.load_user_profile(profile_path, targets)
            for warning in warnings:
                print(f"warning: {warning}", file=sys.stderr)
            targets = style_profile.merge_targets(targets, overrides)
            overridden = frozenset(overrides.get(mode, {}))
        if mode in targets:
            section["delta"] = style_profile.delta(profile_report["metrics"], targets[mode], overridden)
    return section


def analyze_file(
    path: Path,
    mode: str,
    mode_explicit: bool = False,
    use_profile: bool = True,
    precise: bool = False,
    profile_path: Path = style_profile.USER_PROFILE_PATH,
) -> dict:
    text = path.read_text(encoding="utf-8")

    unicode_findings = unicode_lint.lint(text)
    rhythm_report = rhythm_lint.analyze(text, file=str(path), scope="user_text", mode=mode)
    german_report = german_pattern_lint.lint(text, mode=mode, precise=precise)
    register_report = register_lint.lint(text, mode=mode, precise=precise)
    syntax_report = None
    if precise:
        # nlp aus dem geteilten Prozess-Cache der Linter wiederverwenden,
        # damit das Modell pro Audit-Lauf nur einmal geladen wird.
        _, cached_nlp = register_lint.precise_context(precise)
        syntax_report = syntax_lint.lint(text, nlp=cached_nlp)

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
    preflight = preflight_assessment(
        rhythm_report,
        german_report["findings"],
        register_report["findings"],
        mode,
    )

    report = {
        "file": str(path),
        "mode": mode,
        "ok": sum(counts.values()) == 0,
        "summary": {
            "rhythm": rhythm_summary(rhythm_report),
            "preflight": preflight,
            "counts": counts,
        },
        "style_profile": style_profile_section(
            text,
            path,
            mode,
            mode_explicit,
            use_profile,
            profile_path,
        ),
        "findings": findings,
    }
    if precise:
        report["summary"]["precise"] = register_report.get("precise") or german_report.get("precise")
        report["syntax"] = syntax_report
    return report


def md_finding_line(item: dict) -> str:
    kind = f" {item['kind']}" if item.get("kind") else ""
    count = f" x{item['count']}" if item.get("count") else ""
    return f"- {item['severity']} pattern {item['pattern']}{kind}{count}: {item['summary']}"


def format_markdown(report: dict) -> str:
    rhythm = report["summary"]["rhythm"]
    preflight = report["summary"]["preflight"]
    bucket_ratios = rhythm["sentence_length_buckets"]["ratios"]
    driver_kinds = ", ".join(item["kind"] for item in preflight["drivers"]) or "none"
    lines = [
        f"Mode: {report['mode']}",
        f"File: {report['file']}",
        (
            "Preflight: "
            f"risk={preflight['risk']}, "
            f"score={preflight['score']}, "
            f"recommendation={preflight['recommendation']}, "
            f"combing_auto={str(preflight['combing']['auto']).lower()}, "
            "quality_risk=may_degrade_text_quality, "
            f"drivers={driver_kinds}"
        ),
        (
            "Rhythm: "
            f"sentences={rhythm['sentence_count']}, "
            f"mean={rhythm['mean_sentence_length']}, "
            f"stddev={rhythm['stddev_sentence_length']}, "
            f"stddev/mean={rhythm['stddev_mean_ratio']}, "
            f"short/medium/long={bucket_ratios['short_lt_12']}/{bucket_ratios['medium_12_to_28']}/{bucket_ratios['long_gt_28']}, "
            f"complexity_var={rhythm['syntactic_complexity_variance']}, "
            f"subject_initial={rhythm['subject_initial_ratio']}, "
            f"connectors={rhythm['connector_density']}, "
            f"headings={rhythm['heading_count']}, "
            f"colon_headings={rhythm['colon_heading_count']}, "
            f"uniform_paragraphs={str(rhythm['paragraph_sentence_counts_uniform']).lower()}"
        ),
    ]
    style = report["style_profile"]
    metrics = style["metrics"]
    style_line = (
        "StyleProfile: "
        f"words={style['word_count']}, "
        f"nominal_style_ratio={metrics['nominal_style_ratio']}, "
        f"type_token_ratio={metrics['type_token_ratio']}, "
        f"particles={metrics['particle_count']}, "
        f"emojis={metrics['emoji_count']}"
    )
    if "delta" in style:
        out_of_range = [name for name, item in style["delta"].items() if not item["in_range"]]
        style_line += f", delta_out_of_range={','.join(out_of_range) or 'none'}"
        overridden = [name for name, item in style["delta"].items() if item.get("override")]
        if overridden:
            style_line += f", profile_overrides={','.join(overridden)}"
    lines.append(style_line)
    lines.append("Findings:")
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
    if args.profile is not None and not args.profile.is_file():
        print(f"error: --profile requires an existing file: {args.profile}", file=sys.stderr)
        return 2
    profile_path = args.profile if args.profile is not None else style_profile.USER_PROFILE_PATH
    try:
        path = input_path(args)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    report = analyze_file(
        path,
        args.mode or "sachlich",
        mode_explicit=args.mode is not None,
        use_profile=not args.no_profile,
        profile_path=profile_path,
        precise=args.precise,
    )
    if args.format == "md":
        print(format_markdown(report))
    else:
        print_json(report)
    return resolve_exit_code(args.fail_on, report["findings"])


if __name__ == "__main__":
    raise SystemExit(main())
