#!/usr/bin/env python3
"""Report German naturalness pattern clusters for Humanizer-de."""

from __future__ import annotations

import argparse
import functools
import importlib.util
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import print_json, resolve_exit_code


REGISTER_SCRIPT = SCRIPT_DIR / "register_lint.py"
register_spec = importlib.util.spec_from_file_location("register_lint", REGISTER_SCRIPT)
register_lint = importlib.util.module_from_spec(register_spec)
register_spec.loader.exec_module(register_lint)

SYNTAX_SCRIPT = SCRIPT_DIR / "syntax_lint.py"
_SYNTAX_LINT = None


AI_MARKERS = (
    "beleuchten",
    "eintauchen",
    "unterstreichen",
    "aufzeigen",
    "spannend",
    "entscheidend",
    "maßgeblich",
    "massgeblich",
    "nahtlos",
    "vielschichtig",
    "facettenreich",
    "dynamisch",
    "ganzheitlich",
    "maßgeschneidert",
    "massgeschneidert",
    "digitale landschaft",
    "zusammenspiel",
)
COPULA_AVOIDANCE = (
    "fungiert als",
    "dient als",
    "verfügt über",
    "verfuegt ueber",
    "zeichnet sich",
    "erweist sich als",
    "repräsentiert",
    "repraesentiert",
)
ABSTRACTA = (
    "maßnahmen",
    "massnahmen",
    "aspekte",
    "lösungen",
    "loesungen",
    "herausforderungen",
    "faktoren",
    "prozesse",
)
NEGATION_PARALLELISM_RES = (
    re.compile(r"\b[Kk]eine?[nmrs]?\b[^,.;:!?\n]{1,45},\s*[Kk]eine?[nmrs]?\b"),
    re.compile(r"\b[Nn]icht\b[^,.;:!?\n]{1,45},\s*[Nn]icht\b"),
)
BOLD_SPAN_RE = re.compile(r"\*\*[^*\n]{1,80}\*\*")
BOLD_OVERDOSE_THRESHOLD = 5
STELLT_DAR_RE = re.compile(
    r"\bstell(?:t|te|ten|en)\b(?:\s+\S+){0,6}?\s+dar\b"
    r"|\bdarstell(?:t|te|ten|en)\b"
    r"|\bdargestellt\b"
    r"|\bdarzustellen\b"
)
ADDRESS_VALIDATION_RE = re.compile(
    r"\b(?:du\s+bist\s+nicht\s+(?:zu\s+|einfach\s+nur\s+)?"
    r"(?:sensibel|empfindlich|emotional|bedürftig|anspruchsvoll|schwierig|schwach|faul|anstrengend)"
    r"|du\s+(?:überreagierst\s+nicht|reagierst\s+nicht\s+über|fühlst\s+nicht\s+falsch)"
    r"|deine\s+gefühle\s+sind\s+(?:völlig\s+)?(?:berechtigt|valide|verständlich)"
    r"|deine\s+reaktion(?:en)?\s+(?:ist|sind)\s+(?:völlig\s+)?(?:berechtigt|valide|verständlich)"
    r"|du\s+wurdest\s+(?:nur\s+)?(?:zu\s+lange\s+)?"
    r"(?:nicht\s+ernst\s+genommen|kleingehalten|emotional\s+vernachlässigt))\b",
    re.IGNORECASE,
)
ADDRESS_VALIDATION_MESSAGE = (
    "Kandidat für unbelegte Adressaten-Validierung: Kontext prüfen "
    "(Beratungsauftrag? Zitat? Sachklärung?)"
)


def load_syntax_lint():
    global _SYNTAX_LINT
    if _SYNTAX_LINT is not None:
        return _SYNTAX_LINT

    module = sys.modules.get("syntax_lint")
    if module is None:
        spec = importlib.util.spec_from_file_location("syntax_lint", SYNTAX_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        sys.modules["syntax_lint"] = module
        spec.loader.exec_module(module)

    _SYNTAX_LINT = module
    return module


def precise_context(precise: bool) -> tuple[dict | None, object | None]:
    if not precise:
        return None, None

    syntax_lint = load_syntax_lint()
    if not hasattr(syntax_lint, "_HUMANIZER_PRECISE_CACHE"):
        syntax_lint._HUMANIZER_PRECISE_CACHE = syntax_lint.load_nlp()

    nlp, reason = syntax_lint._HUMANIZER_PRECISE_CACHE
    if nlp is None:
        return {"requested": True, "active": False, "reason": reason or "spacy_missing"}, None
    return {"requested": True, "active": True}, nlp


def marker_stem(marker: str) -> str:
    if marker.endswith("en") and len(marker) > 5:
        return marker[:-2]
    return marker


@functools.lru_cache(maxsize=8)
def mention_ranges(text: str) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    patterns = [
        r"```.*?```",
        r"`[^`\n]+`",
        r"„[^“\n]+“",
        r"‚[^‘\n]+‘",
        r'"[^"\n]+"',
        # Wortgrenzen-Schutz: Apostrophe in Kontraktionen („gibt's") und
        # Unterstriche in snake_case dürfen keine Spans öffnen/schließen.
        r"(?<!\w)'[^'\n]+'(?!\w)",
        r"\*[^*\n]+\*",
        r"(?<!\w)_[^_\n]+_(?!\w)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.DOTALL):
            ranges.append(match.span())
    ranges.sort()
    return tuple(ranges)


def in_mention(index: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    return any(start <= index < end for start, end in ranges)


def count_marker(text: str, marker: str) -> int:
    lowered = text.lower()
    ranges = mention_ranges(lowered)
    if " " in marker:
        matches = re.finditer(rf"\b{re.escape(marker)}\w*\b", lowered)
        return sum(1 for match in matches if not in_mention(match.start(), ranges))
    stem = marker_stem(marker)
    matches = re.finditer(rf"\b{re.escape(stem)}\w*\b", lowered)
    return sum(1 for match in matches if not in_mention(match.start(), ranges))


def count_stellt_dar_dependency(text: str, nlp: object) -> int:
    doc = nlp(text)
    count = 0
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma == "darstellen":
            count += 1
            continue
        if lemma != "stellen" or "Fin" not in token.morph.get("VerbForm"):
            continue
        if any(child.dep_ == "svp" and child.text.lower() == "dar" for child in token.children):
            count += 1
    return count


def lint(text: str, mode: str = "sachlich", precise: bool = False) -> dict:
    status, nlp = precise_context(precise)
    clean_text = register_lint.strip_protected(text)
    lowered = clean_text.lower()
    findings: list[dict] = []

    ai_hits = {marker: count_marker(lowered, marker) for marker in AI_MARKERS if count_marker(lowered, marker)}
    if sum(ai_hits.values()) >= 3:
        findings.append({"pattern": 64, "kind": "ai_marker_cluster", "severity": "warning", "evidence": ai_hits})

    copula_hits = {marker: count_marker(lowered, marker) for marker in COPULA_AVOIDANCE if count_marker(lowered, marker)}
    separable_hits = len(STELLT_DAR_RE.findall(lowered))
    if nlp is not None:
        separable_hits = count_stellt_dar_dependency(clean_text, nlp)
    if separable_hits:
        copula_hits["stellt ... dar"] = separable_hits
    if sum(copula_hits.values()) >= 2:
        findings.append({"pattern": 65, "kind": "copula_avoidance_cluster", "severity": "warning", "evidence": copula_hits})

    abstract_hits = {marker: count_marker(lowered, marker) for marker in ABSTRACTA if count_marker(lowered, marker)}
    if sum(abstract_hits.values()) >= 3:
        findings.append({"pattern": 58, "kind": "abstraction_cluster", "severity": "warning", "evidence": abstract_hits})

    colon_headings = [
        line.strip()
        for line in clean_text.splitlines()
        if re.match(r"^\s{0,3}#{1,3}\s+.+:.+", line)
    ]
    if len(colon_headings) >= 2:
        findings.append({"pattern": 54, "kind": "colon_heading_cluster", "severity": "warning", "evidence": colon_headings})

    mention_spans = mention_ranges(clean_text.lower())
    negation_matches = sorted(
        (
            match.start(),
            match.group().strip(),
        )
        for pattern in NEGATION_PARALLELISM_RES
        for match in pattern.finditer(clean_text)
        if not in_mention(match.start(), mention_spans)
    )
    evidence = [matched_text for _, matched_text in negation_matches]
    if evidence:
        findings.append(
            {
                "pattern": 8,
                "kind": "negation_parallelism",
                "severity": "warning",
                "evidence": evidence,
            }
        )

    bold_span_count = sum(
        1
        for match in BOLD_SPAN_RE.finditer(clean_text)
        if (match.start() == 0 or clean_text[match.start() - 1] != "*")
        and (match.end() == len(clean_text) or clean_text[match.end()] != "*")
    )
    if bold_span_count >= BOLD_OVERDOSE_THRESHOLD:
        findings.append(
            {
                "pattern": 13,
                "kind": "bold_overdose",
                "severity": "warning",
                "evidence": {"count": bold_span_count},
            }
        )

    address_validation_matches = [
        match.group().strip()
        for match in ADDRESS_VALIDATION_RE.finditer(clean_text)
        if not in_mention(match.start(), mention_spans)
    ]
    if address_validation_matches:
        findings.append(
            {
                "pattern": 72,
                "kind": "address_validation_candidate",
                "severity": "info",
                "advisory": True,
                "message": ADDRESS_VALIDATION_MESSAGE,
                "evidence": address_validation_matches,
            }
        )

    report = {"ok": not findings, "mode": mode, "findings": findings}
    if status is not None:
        report["precise"] = status
    return report


def check_fixture(path: Path, precise: bool = False) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    report = lint(data["text"], mode=data.get("mode", "sachlich"), precise=precise)
    expected = set(data.get("expect_kinds", []))
    actual = {item["kind"] for item in report["findings"]}
    return {"fixture": str(path), "ok": actual == expected, "report": report}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report German naturalness pattern clusters.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    source.add_argument("--fixture", type=Path)
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default="sachlich")
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="never")
    args = parser.parse_args(argv)
    if args.fixture:
        if not args.fixture.exists():
            parser.error(f"fixture path does not exist: {args.fixture}")
        if args.fixture.is_dir() and not any(args.fixture.glob("*.json")):
            parser.error(f"fixture directory contains no JSON files: {args.fixture}")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.fixture:
        files = sorted(args.fixture.glob("*.json")) if args.fixture.is_dir() else [args.fixture]
        results = [check_fixture(file_path, precise=args.precise) for file_path in files]
        print_json({"ok": all(item["ok"] for item in results), "results": results})
        return 0 if all(item["ok"] for item in results) else 1

    text = args.file.read_text(encoding="utf-8") if args.file else args.text or ""
    report = lint(text, mode=args.mode, precise=args.precise)
    print_json(report)
    return resolve_exit_code(args.fail_on, report["findings"])


if __name__ == "__main__":
    raise SystemExit(main())
