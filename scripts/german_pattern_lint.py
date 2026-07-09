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


REGISTER_SCRIPT = Path(__file__).resolve().parent / "register_lint.py"
register_spec = importlib.util.spec_from_file_location("register_lint", REGISTER_SCRIPT)
register_lint = importlib.util.module_from_spec(register_spec)
register_spec.loader.exec_module(register_lint)

SYNTAX_SCRIPT = Path(__file__).resolve().parent / "syntax_lint.py"
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
PARTICLES = tuple(sorted(register_lint.MODAL_PARTICLES))
STELLT_DAR_RE = re.compile(
    r"\bstell(?:t|te|ten|en)\b(?:\s+\S+){0,6}?\s+dar\b"
    r"|\bdarstell(?:t|te|ten|en)\b"
    r"|\bdargestellt\b"
    r"|\bdarzustellen\b"
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


def precise_status(precise: bool) -> dict | None:
    status, _ = precise_context(precise)
    return status


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


def count_particle(text: str, marker: str) -> int:
    lowered = text.lower()
    return len(re.findall(rf"\b{re.escape(marker)}\b", lowered))


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

    particle_count = sum(count_particle(lowered, marker) for marker in PARTICLES)
    if mode in {"sachlich", "formal"} and particle_count:
        findings.append({"pattern": 63, "kind": "particles_outside_locker", "severity": "warning", "evidence": {"count": particle_count}})
    if mode == "locker" and particle_count > 3:
        findings.append({"pattern": 63, "kind": "particle_overdose", "severity": "warning", "evidence": {"count": particle_count}})

    colon_headings = [
        line.strip()
        for line in clean_text.splitlines()
        if re.match(r"^\s{0,3}#{1,3}\s+.+:.+", line)
    ]
    if len(colon_headings) >= 2:
        findings.append({"pattern": 54, "kind": "colon_heading_cluster", "severity": "warning", "evidence": colon_headings})

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
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    source.add_argument("--fixture", type=Path)
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default="sachlich")
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="never")
    return parser.parse_args(argv)


def exit_code(findings: list[dict], fail_on: str) -> int:
    if fail_on == "never":
        return 0
    if fail_on == "blocker":
        return 1 if any(item["severity"] == "blocker" for item in findings) else 0
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.fixture:
        files = sorted(args.fixture.glob("*.json")) if args.fixture.is_dir() else [args.fixture]
        results = [check_fixture(file_path, precise=args.precise) for file_path in files]
        print(json.dumps({"ok": all(item["ok"] for item in results), "results": results}, ensure_ascii=False, indent=2))
        return 0 if all(item["ok"] for item in results) else 1

    text = args.file.read_text(encoding="utf-8") if args.file else args.text or ""
    report = lint(text, mode=args.mode, precise=args.precise)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return exit_code(report["findings"], args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
