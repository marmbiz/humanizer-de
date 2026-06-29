#!/usr/bin/env python3
"""Report Humanizer-de rhythm suspicions, not findings.

The script measures deterministic rhythm and burstiness signals for patterns
4, 51, 54, 55, and 61. It deliberately returns suspicions only: cluster logic,
mode handling, source context, and carve-outs stay with the model or reviewer.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


SUBJUNCTIONS = {
    "weil",
    "obwohl",
    "dass",
    "nachdem",
    "wenn",
    "falls",
    "sofern",
    "während",
    "sodass",
    "damit",
    "ob",
    "als",
    "bevor",
    "seit",
    "seitdem",
    "bis",
    "indem",
}

INITIAL_FUNCTION_WORDS = SUBJUNCTIONS | {
    "dann",
    "dort",
    "hier",
    "heute",
    "gestern",
    "morgen",
    "zudem",
    "außerdem",
    "dennoch",
    "trotzdem",
    "dabei",
    "danach",
    "davor",
    "deshalb",
    "daher",
    "darum",
    "inzwischen",
    "mittlerweile",
    "schließlich",
    "zunächst",
    "erst",
    "später",
    "gleichzeitig",
    "so",
    "in",
    "an",
    "auf",
    "bei",
    "mit",
    "nach",
    "von",
    "vor",
    "zu",
    "über",
    "unter",
    "durch",
    "für",
    "gegen",
    "ohne",
    "um",
    "aus",
    "trotz",
    "wegen",
    "laut",
    "ab",
}

CONNECTORS = (
    "darüber hinaus",
    "zudem",
    "außerdem",
    "ferner",
    "des weiteren",
    "ebenfalls",
    "gleichzeitig",
    "überdies",
    "in der heutigen",
    "zusammenfassend",
    "insgesamt",
)

ABBREVIATIONS = (
    "z. B.",
    "z.B.",
    "u. a.",
    "u.a.",
    "d. h.",
    "d.h.",
    "bzw.",
    "ca.",
    "Dr.",
    "Prof.",
    "Nr.",
    "S.",
    "vgl.",
)

MONTHS = (
    "Januar",
    "Februar",
    "März",
    "Maerz",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
)

WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß0-9]+(?:[-'][A-Za-zÄÖÜäöüß0-9]+)?")
DOT = "<RH_DOT>"


def protected_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    patterns = [
        r"```.*?```",
        r"`[^`\n]+`",
        r"https?://[^\s<>)]+",
        r"\b[\w.-]+@[\w.-]+\.[A-Za-z]{2,}\b",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.DOTALL):
            ranges.append(match.span())
    ranges.sort()
    return ranges


def strip_protected(text: str) -> str:
    chars = list(text)
    for start, end in protected_ranges(text):
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def is_markdown_heading(line: str) -> bool:
    return bool(re.match(r"^\s{0,3}#{1,6}\s+\S", line))


def is_wikitext_heading(line: str) -> bool:
    return bool(re.match(r"^\s*={2,}\s*[^=].*?\s*={2,}\s*$", line))


def heading_text(line: str) -> str:
    stripped = line.strip()
    if is_markdown_heading(stripped):
        return re.sub(r"^#{1,6}\s+", "", stripped).strip()
    if is_wikitext_heading(stripped):
        return re.sub(r"^\s*=+\s*|\s*=+\s*$", "", stripped).strip()
    return stripped


def is_list_item(line: str) -> bool:
    return bool(re.match(r"^\s*(?:[-*+]|\d+[.)])\s+\S", line))


def split_blocks(text: str) -> tuple[list[str], list[str]]:
    headings: list[str] = []
    blocks: list[str] = []
    current: list[str] = []

    def flush_current() -> None:
        if current:
            block = " ".join(part.strip() for part in current if part.strip()).strip()
            if block:
                blocks.append(block)
            current.clear()

    for line in text.splitlines():
        if is_markdown_heading(line) or is_wikitext_heading(line):
            flush_current()
            headings.append(heading_text(line))
            continue
        if is_list_item(line):
            flush_current()
            blocks.append(re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line).strip())
            continue
        if not line.strip():
            flush_current()
            continue
        current.append(line)
    flush_current()
    return headings, blocks


def protect_sentence_periods(text: str) -> str:
    masked = text
    for abbreviation in ABBREVIATIONS:
        masked = re.sub(
            re.escape(abbreviation),
            lambda match: match.group(0).replace(".", DOT),
            masked,
            flags=re.IGNORECASE,
        )
    month_pattern = "|".join(re.escape(month) for month in MONTHS)
    masked = re.sub(
        rf"\b(\d{{1,2}})\.\s+(?=(?:{month_pattern})\b)",
        lambda match: match.group(1) + DOT + " ",
        masked,
    )
    masked = re.sub(r"\b(\d+)\.(\d+)\b", lambda match: match.group(1) + DOT + match.group(2), masked)
    return masked


def restore_sentence_periods(text: str) -> str:
    return text.replace(DOT, ".")


def split_sentences(text: str) -> list[str]:
    """Split on .!? after masking common abbreviations and simple dates."""
    masked = protect_sentence_periods(text)
    parts = re.split(r"(?<=[.!?])\s+", masked.strip())
    sentences = [restore_sentence_periods(part).strip() for part in parts if restore_sentence_periods(part).strip()]
    return sentences


def tokens(text: str) -> list[str]:
    return [match.group(0) for match in WORD_RE.finditer(text)]


def sentence_lengths(sentences: list[str]) -> list[int]:
    return [len(tokens(sentence)) for sentence in sentences if tokens(sentence)]


def mean(values: list[int]) -> float:
    return sum(values) / len(values) if values else 0.0


def stddev(values: list[int]) -> float:
    if not values:
        return 0.0
    value_mean = mean(values)
    return math.sqrt(sum((value - value_mean) ** 2 for value in values) / len(values))


def rounded(value: float) -> float:
    return round(value, 3)


def first_token(sentence: str) -> str:
    found = tokens(sentence)
    return found[0].lower() if found else ""


def subject_initial_ratio(sentences: list[str]) -> float:
    starters = [first_token(sentence) for sentence in sentences if first_token(sentence)]
    if not starters:
        return 0.0
    subject_initial = [starter for starter in starters if starter not in INITIAL_FUNCTION_WORDS]
    return len(subject_initial) / len(starters)


def has_subjunction(sentence: str) -> bool:
    return any(token.lower() in SUBJUNCTIONS for token in tokens(sentence))


def max_main_clause_run(sentences: list[str]) -> int:
    longest = 0
    current = 0
    for sentence in sentences:
        if has_subjunction(sentence):
            current = 0
        else:
            current += 1
            longest = max(longest, current)
    return longest


def connector_density(block: str) -> int:
    lowered = block.lower()
    return sum(len(re.findall(rf"\b{re.escape(connector)}\b", lowered)) for connector in CONNECTORS)


def repeated_openers(sentences: list[str]) -> list[dict]:
    seen: list[tuple[str, int]] = []
    repeats: list[dict] = []
    for index, sentence in enumerate(sentences):
        opener_tokens = [token.lower() for token in tokens(sentence)[:2]]
        if len(opener_tokens) < 2:
            continue
        opener = " ".join(opener_tokens)
        for previous_opener, previous_index in seen[-2:]:
            if opener == previous_opener:
                repeats.append(
                    {
                        "opener": opener,
                        "sentence": index + 1,
                        "previous_sentence": previous_index + 1,
                    }
                )
                break
        seen.append((opener, index))
    return repeats


def paragraph_report(index: int, block: str) -> dict:
    sentences = split_sentences(block)
    lengths = sentence_lengths(sentences)
    length_mean = mean(lengths)
    length_stddev = stddev(lengths)
    return {
        "index": index,
        "sentence_count": len(sentences),
        "mean_sentence_length": rounded(length_mean),
        "stddev_sentence_length": rounded(length_stddev),
        "stddev_mean_ratio": rounded(length_stddev / length_mean) if length_mean else 0.0,
        "subject_initial_ratio": rounded(subject_initial_ratio(sentences)),
        "max_main_clause_run": max_main_clause_run(sentences),
        "connector_density": connector_density(block),
        "repeated_openers": repeated_openers(sentences),
    }


def add_suspicion(
    suspicions: list[dict],
    pattern: int,
    reason: str,
    evidence: str,
    *,
    confidence: str = "medium",
    severity: str = "warning",
) -> None:
    suspicions.append(
        {
            "pattern": pattern,
            "reason": reason,
            "evidence": evidence,
            "confidence": confidence,
            "severity": severity,
            "suppressed_by_scope": False,
        }
    )


def suppress_suspicion(item: dict, scope: str, mode: str) -> dict:
    suppressed = dict(item)
    suppressed["suppressed_by_scope"] = True
    suppressed["scope"] = scope
    suppressed["mode"] = mode
    return suppressed


def apply_scope(suspicions: list[dict], scope: str, mode: str) -> tuple[list[dict], list[dict]]:
    active: list[dict] = []
    suppressed: list[dict] = []
    for item in suspicions:
        pattern = item["pattern"]
        should_suppress = False
        if scope == "skill_doc" and pattern in {51, 55, 61}:
            should_suppress = True
        if mode == "formal" and pattern in {51, 55, 61}:
            should_suppress = True
        if should_suppress:
            suppressed.append(suppress_suspicion(item, scope, mode))
        else:
            active.append(item)
    return active, suppressed


def analyze(text: str, file: str | None = None, scope: str = "user_text", mode: str = "sachlich") -> dict:
    clean_text = strip_protected(text)
    headings, blocks = split_blocks(clean_text)
    paragraph_reports = [paragraph_report(index + 1, block) for index, block in enumerate(blocks)]
    all_sentences = [sentence for block in blocks for sentence in split_sentences(block)]
    lengths = sentence_lengths(all_sentences)
    length_mean = mean(lengths)
    length_stddev = stddev(lengths)
    length_ratio = length_stddev / length_mean if length_mean else 0.0
    sentence_count = len(all_sentences)
    paragraph_sentence_counts = [report["sentence_count"] for report in paragraph_reports if report["sentence_count"]]
    uniform_paragraphs = len(paragraph_sentence_counts) >= 4 and max(paragraph_sentence_counts) - min(paragraph_sentence_counts) <= 2
    connector_counts = [report["connector_density"] for report in paragraph_reports]
    heading_count = len(headings)
    colon_heading_count = sum(1 for heading in headings if ":" in heading)
    colon_heading_ratio = colon_heading_count / heading_count if heading_count else 0.0
    opener_repeats = repeated_openers(all_sentences)
    main_clause_run = max_main_clause_run(all_sentences)
    subject_ratio = subject_initial_ratio(all_sentences)

    raw_suspicions: list[dict] = []
    if sentence_count >= 8 and length_ratio < 0.4:
        add_suspicion(
            raw_suspicions,
            55,
            "low sentence-length variance",
            f"stddev/mean={rounded(length_ratio)} across {sentence_count} sentences",
            confidence="high",
        )
    # SIR fires only as part of a cluster: high ratio AND (low variance OR repeated openers).
    # Standalone SIR > 0.75 fires on ~95% of human German blog posts (empirically validated
    # against 21 posts, median 0.887) — not a valid KI discriminator on its own.
    sir_cluster = subject_ratio > 0.85 and (length_ratio < 0.6 or len(opener_repeats) >= 2)
    if sentence_count >= 8 and sir_cluster:
        add_suspicion(
            raw_suspicions,
            55,
            "high subject-initial ratio",
            f"subject_initial_ratio={rounded(subject_ratio)} (cluster: stddev/mean={rounded(length_ratio)}, repeated_openers={len(opener_repeats)})",
        )
    if len(opener_repeats) >= 2:
        add_suspicion(
            raw_suspicions,
            55,
            "repeated sentence openers",
            f"{len(opener_repeats)} repeated two-token openers within a 3-sentence window",
        )
    # Muster 51 removed from suspicion output: has_subjunction() only checks a fixed list of
    # subordinating conjunctions and misses relative clauses, infinitive groups, coordination
    # and ellipses. Fires on 100% of human German blog posts — validity problem, not a threshold
    # issue. main_clause_run is still measured and reported in the document block for transparency.
    if uniform_paragraphs:
        add_suspicion(raw_suspicions, 61, "uniform paragraph lengths", f"paragraph_sentence_counts={paragraph_sentence_counts}")
    for report in paragraph_reports:
        if report["connector_density"] > 1:
            add_suspicion(
                raw_suspicions,
                4,
                "connector density",
                f"paragraph {report['index']} has connector_density={report['connector_density']}",
                confidence="high",
            )
    if colon_heading_count >= 2:
        add_suspicion(
            raw_suspicions,
            54,
            "colon heading ratio",
            f"{colon_heading_count}/{heading_count} headings contain a colon",
        )
    suspicions, suppressed = apply_scope(raw_suspicions, scope, mode)

    return {
        "file": file or "<text>",
        "scope": scope,
        "mode": mode,
        "document": {
            "sentence_count": sentence_count,
            "mean_sentence_length": rounded(length_mean),
            "stddev_sentence_length": rounded(length_stddev),
            "stddev_mean_ratio": rounded(length_ratio),
            "subject_initial_ratio": rounded(subject_ratio),
            "max_main_clause_run": main_clause_run,
            "paragraph_sentence_counts": paragraph_sentence_counts,
            "paragraph_sentence_counts_uniform": uniform_paragraphs,
            "connector_density": sum(connector_counts),
            "connector_density_by_paragraph": connector_counts,
            "heading_count": heading_count,
            "colon_heading_count": colon_heading_count,
            "colon_heading_ratio": rounded(colon_heading_ratio),
            "repeated_openers": opener_repeats,
        },
        "paragraphs": paragraph_reports,
        "raw_suspicions": raw_suspicions,
        "suppressed": suppressed,
        "suspicions": suspicions,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure Humanizer-de rhythm and burstiness signals.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="UTF-8 text file to analyze.")
    source.add_argument("--text", help="Text to analyze. Intended for smoke tests.")
    parser.add_argument("--scope", choices=["skill_doc", "user_text", "changed_passages"], default="user_text")
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default="sachlich")
    parser.add_argument("--include-paragraphs", action="store_true", help="Print full paragraph-level diagnostics.")
    return parser.parse_args(argv)


def compact_cli_report(report: dict) -> dict:
    compact = dict(report)
    document = dict(compact["document"])
    document.pop("paragraph_sentence_counts", None)
    document.pop("connector_density_by_paragraph", None)
    compact["document"] = document
    compact.pop("paragraphs", None)
    return compact


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.file:
        text = args.file.read_text(encoding="utf-8")
        file_name = str(args.file)
    else:
        text = args.text
        file_name = "<text>"
    report = analyze(text, file=file_name, scope=args.scope, mode=args.mode)
    if not args.include_paragraphs:
        report = compact_cli_report(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
