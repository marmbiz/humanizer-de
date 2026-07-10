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


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import text_scope


SYNTAX_SCRIPT = SCRIPT_DIR / "syntax_lint.py"
_SYNTAX_LINT = None

MODAL_PARTICLES = {"ja", "doch", "eben", "halt", "wohl", "mal", "schon", "ohnehin"}
DU_FORMS = ("du", "dir", "dich", "dein", "deine", "deinen", "deinem", "deiner", "deines")
SIE_FORMS = ("Sie", "Ihnen", "Ihr", "Ihre", "Ihren", "Ihrem", "Ihrer", "Ihres")
WIR_FORMS = ("wir", "uns", "unser", "unsere", "unseren", "unserem", "unserer", "unseres")
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


def protected_ranges(text: str) -> list[tuple[int, int]]:
    return text_scope.protected_ranges(text)


def strip_protected(text: str, exclude_blockquotes: bool = False) -> str:
    scope = text_scope.AUTHORED_PROSE if exclude_blockquotes else text_scope.DOCUMENT_PROSE
    return text_scope.mask_text(text, scope=scope)


def blockquote_ranges(text: str) -> list[tuple[int, int]]:
    return text_scope.blockquote_ranges(text)


def is_in_ranges(start: int, end: int, ranges: Iterable[tuple[int, int]]) -> bool:
    return any(start < range_end and end > range_start for range_start, range_end in ranges)


def count_words(text: str, words: Iterable[str]) -> int:
    lowered = text.lower()
    return sum(len(re.findall(rf"\b{re.escape(word)}\b", lowered)) for word in words)


def is_sentence_initial_sie(text: str, start: int) -> bool:
    prefix = text[:start]
    return not prefix.strip() or re.search(r"[.!?:]\s+$", prefix) is not None


def has_morph(token: object, key: str, value: str) -> bool:
    return value in token.morph.get(key)


def token_for_match(doc: object, start: int, end: int):
    for token in doc:
        if token.idx == start and token.idx + len(token.text) == end:
            return token
    return None


def previous_sentence(doc: object, token: object):
    sentences = list(doc.sents)
    for index, sent in enumerate(sentences):
        if sent.start <= token.i < sent.end:
            return sentences[index - 1] if index > 0 else None
    return None


def contains_du_form(text: str) -> bool:
    return count_words(text, DU_FORMS) > 0


def contains_imperative(sent: object) -> bool:
    return any("Imp" in token.morph.get("Mood") or token.tag_ == "VVIMP" for token in sent)


def previous_sentence_allows_anaphora(doc: object, token: object) -> bool:
    sent = previous_sentence(doc, token)
    if sent is None:
        return True
    return not contains_imperative(sent) and not contains_du_form(sent.text)


def is_anaphoric_sie(match: re.Match, text: str, doc: object) -> bool:
    if match.group(0) != "Sie":
        return False
    if not is_sentence_initial_sie(text, match.start()):
        return False

    token = token_for_match(doc, match.start(), match.end())
    if token is None:
        return False
    return (
        token.text == "Sie"
        and has_morph(token, "Person", "3")
        and has_morph(token, "Case", "Nom")
        and has_morph(token, "Number", "Sing")
        and previous_sentence_allows_anaphora(doc, token)
    )


def sie_formal_count(text: str, nlp: object | None = None) -> int:
    blockquotes = blockquote_ranges(text) if nlp is not None else []
    doc = nlp(text) if nlp is not None else None
    count = 0
    for match in SIE_FORMS_RE.finditer(text):
        if is_in_ranges(match.start(), match.end(), blockquotes):
            continue
        if doc is not None and is_anaphoric_sie(match, text, doc):
            continue
        count += 1
    return count


def features(text: str, nlp: object | None = None, exclude_blockquotes: bool | None = None) -> dict:
    if exclude_blockquotes is None:
        exclude_blockquotes = nlp is not None
    clean_text = strip_protected(text, exclude_blockquotes=exclude_blockquotes)
    return {
        "du_count": count_words(clean_text, DU_FORMS),
        "sie_formal_count": sie_formal_count(clean_text, nlp=nlp),
        "wir_count": count_words(clean_text, WIR_FORMS),
        "man_count": count_words(clean_text, {"man"}),
        "modal_particle_count": count_words(clean_text, MODAL_PARTICLES),
        "emoji_count": len(EMOJI_RE.findall(clean_text)),
        "rhetorical_questions": len(re.findall(r"\?\s*(?:$|\n|[A-ZÄÖÜ])", clean_text)),
    }


def add(findings: list[dict], severity: str, kind: str, message: str) -> None:
    findings.append({"severity": severity, "kind": kind, "message": message})


def lint(text: str, mode: str = "sachlich", expected_address: str | None = None, precise: bool = False) -> dict:
    status, nlp = precise_context(precise)
    found = features(text, nlp=nlp)
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
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="blocker")
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
    report = lint(text, mode=args.mode, expected_address=args.expected_address, precise=args.precise)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return exit_code(report["findings"], args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
