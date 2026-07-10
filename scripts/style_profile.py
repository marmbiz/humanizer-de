#!/usr/bin/env python3
"""Report raw style metrics for German text — numbers only, no interpretation.

The profile is equally valid for human and machine text: it contains no
pattern numbers, no suspicions, and no verdicts. Interpretation stays with
the model or reviewer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import german_pattern_lint
import register_lint
import rhythm_lint


TARGETS_PATH = SCRIPT_DIR.parent / "references" / "style-targets.json"
USER_PROFILE_PATH = Path(".humanizer") / "profile.json"

KNOWN_METRICS = frozenset(
    {
        "mean_sentence_len",
        "stddev_sentence_len",
        "stddev_mean_ratio",
        "subject_initial_ratio",
        "connector_density",
        "repeated_openers",
        "particle_count",
        "emoji_count",
        "rhetorical_questions",
        "nominal_style_ratio",
        "type_token_ratio",
    }
)


def load_targets() -> dict:
    return json.loads(TARGETS_PATH.read_text(encoding="utf-8"))


def valid_corridor(corridor: object) -> bool:
    if not isinstance(corridor, dict) or not corridor:
        return False
    if not set(corridor) <= {"min", "max"}:
        return False
    return all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in corridor.values())


def load_user_profile(path: Path, targets: dict) -> tuple[dict, list[str]]:
    """Read metric overrides from a user profile; invalid input degrades to warnings."""
    if not path.is_file():
        return {}, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        return {}, [f"user profile {path} ignored: {error}"]
    if not isinstance(data, dict):
        return {}, [f"user profile {path} ignored: top level must be an object"]

    warnings: list[str] = []
    overrides: dict = {}
    raw_overrides = data.get("overrides", {})
    if not isinstance(raw_overrides, dict):
        return {}, [f"user profile {path} ignored: 'overrides' must be an object"]
    for target_name, corridors in raw_overrides.items():
        if target_name not in targets:
            warnings.append(f"user profile: unknown target '{target_name}' ignored")
            continue
        if not isinstance(corridors, dict):
            warnings.append(f"user profile: overrides for '{target_name}' must be an object, ignored")
            continue
        for metric, corridor in corridors.items():
            if metric not in KNOWN_METRICS:
                warnings.append(f"user profile: unknown metric '{target_name}.{metric}' ignored")
                continue
            if not valid_corridor(corridor):
                warnings.append(f"user profile: invalid corridor for '{target_name}.{metric}' ignored (need min/max numbers)")
                continue
            overrides.setdefault(target_name, {})[metric] = corridor
    return overrides, warnings


def merge_targets(targets: dict, overrides: dict) -> dict:
    """Overlay user corridors over the base targets; an override replaces the whole corridor."""
    merged = {name: dict(corridors) for name, corridors in targets.items()}
    for target_name, corridors in overrides.items():
        merged.setdefault(target_name, {}).update(corridors)
    return merged


def delta(metrics: dict, corridors: dict, overridden: frozenset = frozenset()) -> dict:
    report = {}
    for name, corridor in corridors.items():
        value = metrics[name]
        in_range = True
        if "min" in corridor and value < corridor["min"]:
            in_range = False
        if "max" in corridor and value > corridor["max"]:
            in_range = False
        entry = {"value": value, "range": corridor, "in_range": in_range}
        if name in overridden:
            entry["override"] = True
        report[name] = entry
    return report


def nominal_style_ratio(text: str, word_count: int) -> float:
    if not word_count:
        return 0.0
    hits = sum(german_pattern_lint.count_marker(text, marker) for marker in german_pattern_lint.ABSTRACTA)
    return rhythm_lint.rounded(hits / word_count * 100)


def type_token_ratio(words: list[str]) -> float:
    if not words:
        return 0.0
    return rhythm_lint.rounded(len({word.lower() for word in words}) / len(words))


def profile(text: str, source: str) -> dict:
    rhythm_report = rhythm_lint.analyze(text, file=source)
    document = rhythm_report["document"]
    clean_text = rhythm_lint.strip_protected(text)
    _, blocks = rhythm_lint.split_blocks(clean_text)
    prose_text = "\n".join(blocks)
    register_features = register_lint.features(prose_text, exclude_blockquotes=True)
    words = rhythm_lint.tokens(prose_text)
    word_count = len(words)

    metrics = {
        "mean_sentence_len": document["mean_sentence_length"],
        "stddev_sentence_len": document["stddev_sentence_length"],
        "stddev_mean_ratio": document["stddev_mean_ratio"],
        "len_buckets": document["sentence_length_buckets"],
        "subject_initial_ratio": document["subject_initial_ratio"],
        "connector_density": document["connector_density"],
        "repeated_openers": len(document["repeated_openers"]),
        "paragraph_uniformity": document["paragraph_sentence_counts_uniform"],
        "address_counts": {
            "du": register_features["du_count"],
            "sie": register_features["sie_formal_count"],
            "wir": register_features["wir_count"],
            "man": register_features["man_count"],
        },
        "particle_count": register_features["modal_particle_count"],
        "emoji_count": register_features["emoji_count"],
        "rhetorical_questions": register_features["rhetorical_questions"],
        "nominal_style_ratio": nominal_style_ratio(prose_text, word_count),
        "type_token_ratio": type_token_ratio(words),
    }

    return {
        "meta": {
            "source": source,
            "word_count": word_count,
            "sentence_count": document["sentence_count"],
        },
        "metrics": metrics,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report raw style metrics without interpretation.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="UTF-8 text file to profile.")
    source.add_argument("--text", help="Text to profile.")
    parser.add_argument("--target", help="Profile name from references/style-targets.json; adds a delta section.")
    parser.add_argument(
        "--profile",
        type=Path,
        default=USER_PROFILE_PATH,
        help="User profile JSON with corridor overrides (default: .humanizer/profile.json).",
    )
    parser.add_argument("--no-profile", action="store_true", help="Ignore any user profile; use base targets only.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    corridors = None
    overridden: frozenset = frozenset()
    if args.target:
        targets = load_targets()
        if args.target not in targets:
            known = ", ".join(sorted(targets))
            print(f"error: unknown target profile '{args.target}' (known: {known})", file=sys.stderr)
            return 2
        if not args.no_profile:
            overrides, warnings = load_user_profile(args.profile, targets)
            for warning in warnings:
                print(f"warning: {warning}", file=sys.stderr)
            targets = merge_targets(targets, overrides)
            overridden = frozenset(overrides.get(args.target, {}))
        corridors = targets[args.target]
    if args.file:
        text = args.file.read_text(encoding="utf-8")
        source = str(args.file)
    else:
        text = args.text
        source = "<text>"
    report = profile(text, source)
    if corridors is not None:
        report["delta"] = delta(report["metrics"], corridors, overridden)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
