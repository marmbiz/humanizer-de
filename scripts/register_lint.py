#!/usr/bin/env python3
"""Report register and profile drift in German text passages."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
import importlib.util
import json
import re
import sys
from pathlib import Path


SYNTAX_SCRIPT = Path(__file__).resolve().parent / "syntax_lint.py"
_SYNTAX_LINT = None

MODAL_PARTICLES = {"ja", "doch", "eben", "halt", "wohl", "mal", "schon", "ohnehin"}
DU_FORMS = ("du", "dir", "dich", "dein", "deine", "deinen", "deinem", "deiner", "deines")
SIE_FORMS = ("Sie", "Ihnen", "Ihr", "Ihre", "Ihren", "Ihrem", "Ihrer", "Ihres")
SIE_FORMS_RE = re.compile(rf"\b(?:{'|'.join(re.escape(form) for form in SIE_FORMS)})\b")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF]")


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


def precise_status(precise: bool) -> dict | None:
    if not precise:
        return None

    syntax_lint = load_syntax_lint()
    if not hasattr(syntax_lint, "_HUMANIZER_PRECISE_CACHE"):
        syntax_lint._HUMANIZER_PRECISE_CACHE = syntax_lint.load_nlp()

    nlp, reason = syntax_lint._HUMANIZER_PRECISE_CACHE
    if nlp is None:
        return {"requested": True, "active": False, "reason": reason or "spacy_missing"}
    return {"requested": True, "active": True}


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


def count_words(text: str, words: Iterable[str]) -> int:
    lowered = text.lower()
    return sum(len(re.findall(rf"\b{re.escape(word)}\b", lowered)) for word in words)


def features(text: str) -> dict:
    clean_text = strip_protected(text)
    return {
        "du_count": count_words(clean_text, DU_FORMS),
        "sie_formal_count": len(SIE_FORMS_RE.findall(clean_text)),
        "wir_count": count_words(clean_text, {"wir", "uns", "unser", "unsere", "unseren"}),
        "man_count": count_words(clean_text, {"man"}),
        "modal_particle_count": count_words(clean_text, MODAL_PARTICLES),
        "emoji_count": len(EMOJI_RE.findall(clean_text)),
        "rhetorical_questions": len(re.findall(r"\?\s*(?:$|\n|[A-ZÄÖÜ])", clean_text)),
    }


def add(findings: list[dict], severity: str, kind: str, message: str) -> None:
    findings.append({"severity": severity, "kind": kind, "message": message})


def lint(text: str, mode: str = "sachlich", expected_address: str | None = None, precise: bool = False) -> dict:
    found = features(text)
    findings: list[dict] = []

    if found["du_count"] and found["sie_formal_count"]:
        add(findings, "warning", "mixed_address", "Du- and Sie-address appear in the same passage.")
    if expected_address == "du" and found["sie_formal_count"]:
        add(findings, "blocker", "unexpected_sie", "Profile expects du-address, but formal Sie appears.")
    if expected_address == "sie" and found["du_count"]:
        add(findings, "blocker", "unexpected_du", "Profile expects Sie-address, but du-address appears.")
    if expected_address == "wir" and (found["du_count"] or found["sie_formal_count"]):
        add(findings, "blocker", "unexpected_direct_address", "Profile expects wir-address, but du/Sie-address appears.")
    if expected_address == "neutral" and (found["du_count"] or found["sie_formal_count"] or found["wir_count"]):
        add(findings, "blocker", "unexpected_direct_address", "Profile expects neutral address, but direct address appears.")
    if mode in {"sachlich", "formal"} and found["modal_particle_count"]:
        add(findings, "warning", "particles_outside_locker", "Modal particles should not be added in Sachlich/Formal.")
    if mode == "formal" and (found["emoji_count"] or found["rhetorical_questions"]):
        add(findings, "blocker", "formal_voice_intrusion", "Formal mode should not add emojis or rhetorical engagement.")
    if mode == "locker" and found["modal_particle_count"] > 3:
        add(findings, "warning", "particle_overdose", "Locker mode uses too many modal particles.")

    report = {"ok": not findings, "mode": mode, "expected_address": expected_address, "features": found, "findings": findings}
    status = precise_status(precise)
    if status is not None:
        report["precise"] = status
    return report


def check_fixture(path: Path, precise: bool = False) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    report = lint(
        data["text"],
        mode=data.get("mode", "sachlich"),
        expected_address=data.get("expected_address"),
        precise=precise,
    )
    expected = set(data.get("expect_kinds", []))
    actual = {item["kind"] for item in report["findings"]}
    return {"fixture": str(path), "ok": actual == expected, "report": report}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report German register/profile drift.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    source.add_argument("--fixture", type=Path)
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default="sachlich")
    parser.add_argument("--expected-address", choices=["du", "sie", "wir", "neutral"])
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.fixture:
        files = sorted(args.fixture.glob("*.json")) if args.fixture.is_dir() else [args.fixture]
        results = [check_fixture(file_path, precise=args.precise) for file_path in files]
        print(json.dumps({"ok": all(item["ok"] for item in results), "results": results}, ensure_ascii=False, indent=2))
        return 0 if all(item["ok"] for item in results) else 1

    text = args.file.read_text(encoding="utf-8") if args.file else args.text or ""
    report = lint(text, mode=args.mode, expected_address=args.expected_address, precise=args.precise)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] == "blocker" for item in report["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
