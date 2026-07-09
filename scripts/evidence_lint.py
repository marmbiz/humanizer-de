#!/usr/bin/env python3
"""Conservatively compare before/after passages for factual anchor drift."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


SYNTAX_SCRIPT = Path(__file__).resolve().parent / "syntax_lint.py"
_SYNTAX_LINT = None

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
DETERMINERS = {
    "der", "die", "das", "des", "dem", "den",
    "ein", "eine", "einer", "eines", "einem", "einen",
    "im", "am", "zum", "zur", "beim", "vom", "ins", "ans", "aufs",
}
ABSTRACT_NOUN_STOPLIST = {
    "lösung", "loesung", "problem", "priorität", "prioritaet", "herausforderung",
    "bedeutung", "aspekt", "aspekte", "faktor", "faktoren", "prozess", "prozesse",
    "maßnahme", "massnahme", "ziel", "ziele", "ansatz", "ergebnis", "ergebnisse",
    "vorteil", "vorteile", "nachteil", "nachteile", "grundlage", "rahmen",
    "bereich", "bereiche", "thema", "themen", "inhalt", "inhalte", "beispiel",
    "beispiele", "möglichkeit", "moeglichkeit", "entwicklung", "zukunft",
}
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


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).strip(".,;:()[]")


def name_key(value: str) -> str:
    key = value.casefold()
    if key.endswith("es") and len(key) > 5:
        return key[:-2]
    if key.endswith("s") and len(key) > 4:
        return key[:-1]
    return key


def token_in_named_entity(doc: object, start: int, end: int) -> bool:
    for ent in doc.ents:
        if ent.label_ in {"PER", "ORG", "LOC", "MISC"} and ent.start_char <= start and end <= ent.end_char:
            return True
    return False


def anchors(text: str, nlp: object | None = None) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {kind: set() for kind in ANCHOR_PATTERNS}
    for kind, pattern in ANCHOR_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(1) if kind == "quote" else match.group(0)
            normalized = normalize(value)
            if normalized:
                result[kind].add(normalized)

    # Known default-path gap: single-token common nouns after verbs that are
    # not in the stoplist (e.g. "hat Relevanz") still slip through as
    # proper_name; --precise can filter that class with spaCy NER.
    names: set[str] = set()
    doc = nlp(text) if nlp is not None else None
    for match in CAPITALIZED_RE.finditer(text):
        raw = match.group(0)
        tokens = raw.split()
        pos = 0
        while tokens and (tokens[0] in COMMON_SENTENCE_STARTS or tokens[0].lower() in DETERMINERS):
            pos = raw.index(tokens[0], pos) + len(tokens[0])
            tokens = tokens[1:]
        if not tokens:
            continue
        value = normalize(" ".join(tokens))
        if len(value) <= 2:
            continue
        if value.lower() in {"prozent", "euro"}:
            continue
        if len(tokens) >= 2:
            names.add(value)
            continue
        token = tokens[0]
        if re.search(r"\d", token) or token[1:] != token[1:].lower():
            names.add(value)
            continue
        token_start = match.start() + raw.index(token, pos)
        token_end = token_start + len(token)
        prefix = text[:token_start]
        preceding = re.search(r"([\wÄÖÜäöüß-]+)\s+$", prefix)
        if preceding and preceding.group(1).lower() in DETERMINERS:
            continue
        if not prefix.strip() or re.search(r"[.!?:]\s+$", prefix) or re.search(r"\n[ \t]*$", prefix):
            continue
        if token.lower() in ABSTRACT_NOUN_STOPLIST:
            continue
        if doc is not None and not token_in_named_entity(doc, token_start, token_end):
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


def lint(before: str, after: str, precise: bool = False) -> list[dict]:
    _, nlp = precise_context(precise)
    findings: list[dict] = []
    before_anchors = anchors(before, nlp=nlp)
    after_anchors = anchors(after, nlp=nlp)

    hard_kinds = {"number", "date", "url", "doi", "paragraph", "code", "quote"}
    for kind in sorted(before_anchors):
        if kind == "proper_name":
            # Compare case-variant-insensitively (Problem <-> Problems), but
            # report the original surface forms.
            before_keys = {name_key(value) for value in before_anchors[kind]}
            after_keys = {name_key(value) for value in after_anchors.get(kind, set())}
            removed = {value for value in before_anchors[kind] if name_key(value) not in after_keys}
            added = {value for value in after_anchors.get(kind, set()) if name_key(value) not in before_keys}
        else:
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


def check_fixture(path: Path, precise: bool = False) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings = lint(data["before"], data["after"], precise=precise)
    expected = data.get("expect_kinds")
    ok = True
    if expected is not None:
        actual = {item["kind"] for item in findings}
        ok = actual == set(expected)
    return [{"fixture": str(path), "ok": ok, "findings": findings}]


def check_fixtures(path: Path, precise: bool = False) -> list[dict]:
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    return [item for file_path in files for item in check_fixture(file_path, precise=precise)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare before/after passages for factual anchor drift.")
    parser.add_argument("--before", help="Before passage as inline text.")
    parser.add_argument("--after", help="After passage as inline text.")
    parser.add_argument("--before-file", type=Path, help="Read before passage from file.")
    parser.add_argument("--after-file", type=Path, help="Read after passage from file.")
    parser.add_argument("--fixture", type=Path, help="JSON fixture file or directory.")
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.fixture:
        results = check_fixtures(args.fixture, precise=args.precise)
        report = {"ok": all(item["ok"] for item in results), "results": results}
        status = precise_status(args.precise)
        if status is not None:
            report["precise"] = status
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if all(item["ok"] for item in results) else 1

    before = load_text(args.before, args.before_file)
    after = load_text(args.after, args.after_file)
    findings = lint(before, after, precise=args.precise)
    report = {"ok": not findings, "findings": findings}
    status = precise_status(args.precise)
    if status is not None:
        report["precise"] = status
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] == "blocker" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
