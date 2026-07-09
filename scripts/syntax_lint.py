#!/usr/bin/env python3
"""Optional spaCy precision stage; without spaCy, regex linters stay authoritative."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


MODEL = "de_core_news_sm"
SCRIPT_DIR = Path(__file__).resolve().parent
NOUN_POS = {"NOUN", "PROPN"}
VERB_POS = {"VERB", "AUX"}
FINITE_VERB_POS = {"VERB", "AUX"}

def load_nlp() -> tuple[Any | None, str | None]:
    try:
        import spacy
    except Exception:
        return None, "spacy_missing"

    try:
        return spacy.load(MODEL), None
    except Exception:
        return None, "model_missing"


def load_sibling_module(name: str) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] != "\n":
            chars[index] = " "


def prose_text(text: str) -> str:
    chars = list(text)
    unicode_lint = load_sibling_module("unicode_lint")
    rhythm_lint = load_sibling_module("rhythm_lint")

    for start, end in unicode_lint.protected_ranges(text):
        mask_range(chars, start, end)

    offset = 0
    for line in text.splitlines(keepends=True):
        body_end = len(line.rstrip("\r\n"))
        body = line[:body_end]
        if rhythm_lint.is_markdown_heading(body) or rhythm_lint.is_list_item(body):
            mask_range(chars, offset, offset + body_end)
        offset += len(line)

    for index, char in enumerate(chars):
        if char in {"*", "_"}:
            chars[index] = " "

    return "".join(chars)


def token_lemma(token: Any) -> str:
    return token.lemma_.lower()


def has_morph(token: Any, key: str, value: str) -> bool:
    return value in token.morph.get(key)


def sentence_text(span: Any) -> str:
    return span.text.strip()


def is_passive_aux(token: Any) -> bool:
    if token.pos_ != "AUX" or token_lemma(token) != "werden":
        return False
    for child in token.children:
        if (
            child.dep_ == "oc"
            and child.pos_ == "VERB"
            and child.tag_ == "VVPP"
            and has_morph(child, "VerbForm", "Part")
        ):
            return True
    return False


def detect_passive(doc: Any) -> list[dict]:
    findings: list[dict] = []
    for sent in doc.sents:
        passive_auxes = [token for token in sent if is_passive_aux(token)]
        if not passive_auxes:
            continue
        agent_tokens = [
            token
            for token in sent
            if token.dep_ == "sbp" and token_lemma(token) in {"von", "durch"}
        ]
        findings.append(
            {
                "kind": "passive",
                "sentence": sentence_text(sent),
                "aux": [token.text for token in passive_auxes],
                "agent_phrase": [token.text for token in agent_tokens],
            }
        )
    return findings


def is_finite_verb_or_aux(token: Any) -> bool:
    return token.pos_ in FINITE_VERB_POS and has_morph(token, "VerbForm", "Fin")


def has_subject(sent: Any) -> bool:
    return any(token.dep_ == "sb" for token in sent)


def detect_subjectless_fragment(doc: Any) -> list[dict]:
    findings: list[dict] = []
    for sent in doc.sents:
        content = [token for token in sent if not token.is_punct and not token.is_space]
        if not content:
            continue
        if not any(token.is_alpha for token in content):
            continue
        finite_verbs = [token for token in sent if is_finite_verb_or_aux(token)]
        root = sent.root
        no_finite_clause = root.pos_ not in FINITE_VERB_POS and not finite_verbs
        finite_without_subject = bool(finite_verbs) and not has_subject(sent)
        if no_finite_clause or finite_without_subject:
            findings.append(
                {
                    "kind": "subjectless_fragment",
                    "sentence": sentence_text(sent),
                    "root": root.text,
                    "root_pos": root.pos_,
                    "finite_verbs": [token.text for token in finite_verbs],
                }
            )
    return findings


def nominal_verb_ratio(doc: Any) -> dict:
    total_nouns = 0
    total_verbs = 0
    for sent in doc.sents:
        tokens = [token for token in sent if not token.is_punct and not token.is_space]
        noun_count = sum(1 for token in tokens if token.pos_ in NOUN_POS)
        verb_count = sum(1 for token in tokens if token.pos_ in VERB_POS)
        total_nouns += noun_count
        total_verbs += verb_count
    return {
        "nouns": total_nouns,
        "verbs": total_verbs,
        "ratio": ratio(total_nouns, total_verbs),
    }


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return float(numerator) if numerator else 0.0
    return numerator / denominator


def unavailable_report(reason: str) -> dict:
    return {"available": False, "reason": reason, "metrics": None, "findings": []}


def lint(text: str, nlp: Any | None = None) -> dict:
    if nlp is None:
        nlp, reason = load_nlp()
        if nlp is None:
            return unavailable_report(reason or "spacy_missing")

    doc = nlp(prose_text(text))
    sentences = list(doc.sents)
    passive_findings = detect_passive(doc)
    fragment_findings = detect_subjectless_fragment(doc)
    noun_verb = nominal_verb_ratio(doc)

    findings = [
        {
            "pattern": 39,
            "kind": "passive_sentence",
            "severity": "info",
            "sentence": item["sentence"],
            "aux": item["aux"],
            "agent_phrase": item["agent_phrase"],
        }
        for item in passive_findings
    ]
    findings.extend(
        {
            "kind": "subjectless_fragment",
            "severity": "info",
            "sentence": item["sentence"],
        }
        for item in fragment_findings
    )

    return {
        "available": True,
        "metrics": {
            "noun_verb_ratio": noun_verb["ratio"],
            "sentence_count": len(sentences),
            "passive_sentence_count": len(passive_findings),
            "passive_ratio": ratio(len(passive_findings), len(sentences)),
        },
        "findings": findings,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report optional spaCy-backed syntax metrics.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    text = args.file.read_text(encoding="utf-8") if args.file else args.text or ""
    print(json.dumps(lint(text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
