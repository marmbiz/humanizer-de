#!/usr/bin/env python3
"""spaCy-backed measurements for the Humanizer-de PoC.

This module is intentionally isolated under research/. It imports the current
stdlib-only production linters for word lists and anchor baseline behavior, but
does not modify or monkeypatch them.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import importlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

german_pattern_lint = importlib.import_module("scripts.german_pattern_lint")
evidence_lint = importlib.import_module("scripts.evidence_lint")

MODEL = "de_core_news_sm"
NOUN_POS = {"NOUN", "PROPN"}
VERB_POS = {"VERB", "AUX"}
FINITE_VERB_POS = {"VERB", "AUX"}
ENTITY_LABELS = {"PER", "LOC", "ORG", "MISC"}
HARD_ANCHOR_KINDS = {"number", "date", "url", "doi", "paragraph", "code", "quote"}


@dataclass(frozen=True)
class MatchHit:
    category: str
    marker: str
    text: str
    start: int
    end: int

    @property
    def key(self) -> tuple[str, str]:
        return (self.category, self.marker)


def load_nlp() -> spacy.Language:
    return spacy.load(MODEL)


def token_text(token: Token) -> str:
    return token.text.lower()


def token_lemma(token: Token) -> str:
    return token.lemma_.lower()


def has_morph(token: Token, key: str, value: str) -> bool:
    return value in token.morph.get(key)


def sentence_text(span: Span) -> str:
    return span.text.strip()


def is_passive_aux(token: Token) -> bool:
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


def detect_passive(doc: Doc) -> list[dict]:
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


def is_finite_verb_or_aux(token: Token) -> bool:
    return token.pos_ in FINITE_VERB_POS and has_morph(token, "VerbForm", "Fin")


def has_subject(sent: Span) -> bool:
    return any(token.dep_ == "sb" for token in sent)


def detect_subjectless_fragment(doc: Doc) -> list[dict]:
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


def detect_pattern39(doc: Doc) -> list[dict]:
    findings = detect_passive(doc) + detect_subjectless_fragment(doc)
    by_sentence: dict[tuple[str, str], dict] = {}
    for item in findings:
        key = (item["kind"], item["sentence"])
        by_sentence[key] = item
    return list(by_sentence.values())


def nominal_verb_ratio(doc: Doc) -> dict:
    sentences: list[dict] = []
    total_nouns = 0
    total_verbs = 0
    for sent in doc.sents:
        tokens = [token for token in sent if not token.is_punct and not token.is_space]
        noun_count = sum(1 for token in tokens if token.pos_ in NOUN_POS)
        verb_count = sum(1 for token in tokens if token.pos_ in VERB_POS)
        total_nouns += noun_count
        total_verbs += verb_count
        sentences.append(
            {
                "sentence": sentence_text(sent),
                "nouns": noun_count,
                "verbs": verb_count,
                "ratio": ratio(noun_count, verb_count),
            }
        )
    return {
        "nouns": total_nouns,
        "verbs": total_verbs,
        "ratio": ratio(total_nouns, total_verbs),
        "sentences": sentences,
    }


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return float(numerator) if numerator else 0.0
    return numerator / denominator


def marker_id(category: str, marker: str) -> str:
    return f"{category}:{marker}"


def phrase_lemmas(nlp: spacy.Language, phrase: str) -> list[str]:
    return [
        token_lemma(token)
        for token in nlp(phrase)
        if not token.is_punct and not token.is_space
    ]


def lemma_values(lemma: str) -> list[str]:
    return sorted({lemma, lemma.capitalize()})


def phrase_pattern(lemmas: list[str]) -> list[dict]:
    return [{"LEMMA": {"IN": lemma_values(lemma)}} for lemma in lemmas]


def lower_pattern(phrase: str) -> list[dict]:
    return [
        {"LOWER": token.lower()}
        for token in re.findall(r"\w+", phrase, flags=re.UNICODE)
    ]


def build_phrase_matcher(nlp: spacy.Language) -> Matcher:
    matcher = Matcher(nlp.vocab)
    list_map = {
        "ai_marker": german_pattern_lint.AI_MARKERS,
        "copula_avoidance": german_pattern_lint.COPULA_AVOIDANCE,
        "abstractum": german_pattern_lint.ABSTRACTA,
    }
    for category, markers in list_map.items():
        for marker in markers:
            if category == "copula_avoidance" and marker in {"stellt", "stellt dar"}:
                continue
            lemmas = phrase_lemmas(nlp, marker)
            patterns = []
            if lemmas:
                patterns.append(phrase_pattern(lemmas))
            lowered = lower_pattern(marker)
            if lowered:
                patterns.append(lowered)
            if not patterns:
                continue
            matcher.add(marker_id(category, marker), patterns)
    return matcher


def is_modal_particle(token: Token) -> bool:
    lower = token_text(token)
    if lower not in german_pattern_lint.PARTICLES:
        return False
    if lower == "ja":
        return token.pos_ == "ADV" and token.dep_ == "mo"
    if lower == "mal":
        return token.text == "mal" and token.dep_ in {"mo", "oa"} and token.pos_ in {"ADV", "NOUN"}
    if lower == "schon":
        next_token = token.nbor(1) if token.i + 1 < len(token.doc) else None
        if token.i == token.sent.start and next_token is not None and next_token.pos_ in {"ADP", "NOUN", "PROPN"}:
            return False
        return token.dep_ == "mo"
    return token.dep_ == "mo" or token.pos_ in {"ADV", "PART"}


def detect_stellt_dar(doc: Doc) -> list[MatchHit]:
    hits: list[MatchHit] = []
    for token in doc:
        if token_lemma(token) != "stellen":
            continue
        particles = [
            child
            for child in token.children
            if token_lemma(child) == "dar" and child.dep_ == "svp"
        ]
        for particle in particles:
            start = min(token.i, particle.i)
            end = max(token.i, particle.i) + 1
            hits.append(MatchHit("copula_avoidance", "stellt dar", doc[start:end].text, start, end))
    return hits


def detect_lemma_phrases(doc: Doc, matcher: Matcher | None = None) -> list[MatchHit]:
    if matcher is None:
        raise ValueError("detect_lemma_phrases requires a matcher from build_phrase_matcher(nlp).")
    hits: list[MatchHit] = []
    for match_id, start, end in matcher(doc):
        label = doc.vocab.strings[match_id]
        category, marker = label.split(":", 1)
        span = doc[start:end]
        hits.append(MatchHit(category, marker, span.text, start, end))
    hits.extend(detect_stellt_dar(doc))
    for token in doc:
        if is_modal_particle(token):
            hits.append(MatchHit("particle", token_text(token), token.text, token.i, token.i + 1))
    return dedupe_hits(hits)


def detect_lemma_phrases_with_nlp(nlp: spacy.Language, text: str) -> list[MatchHit]:
    doc = nlp(text)
    return detect_lemma_phrases(doc, build_phrase_matcher(nlp))


def dedupe_hits(hits: Iterable[MatchHit]) -> list[MatchHit]:
    seen: set[tuple[str, str, int, int]] = set()
    result: list[MatchHit] = []
    for hit in sorted(hits, key=lambda item: (item.start, item.end, item.category, item.marker)):
        key = (hit.category, hit.marker, hit.start, hit.end)
        if key in seen:
            continue
        seen.add(key)
        result.append(hit)
    return result


def spacy_name_anchors(doc: Doc) -> set[str]:
    return {
        evidence_lint.normalize(ent.text)
        for ent in doc.ents
        if ent.label_ in ENTITY_LABELS and evidence_lint.normalize(ent.text)
    }


def spacy_anchors(nlp: spacy.Language, text: str) -> dict[str, set[str]]:
    anchors = evidence_lint.anchors(text)
    anchors["proper_name"] = spacy_name_anchors(nlp(text))
    return anchors


def anchor_drift_from_sets(before_anchors: dict[str, set[str]], after_anchors: dict[str, set[str]]) -> list[dict]:
    findings: list[dict] = []
    for kind in sorted(before_anchors):
        removed = before_anchors[kind] - after_anchors.get(kind, set())
        added = after_anchors.get(kind, set()) - before_anchors[kind]
        severity = "blocker" if kind in HARD_ANCHOR_KINDS else "warning"
        if removed:
            evidence_lint.add_finding(
                findings,
                severity,
                f"removed_{kind}",
                f"{kind} anchor removed or changed.",
                list(removed),
            )
        if added:
            evidence_lint.add_finding(
                findings,
                severity,
                f"added_{kind}",
                f"New {kind} anchor introduced.",
                list(added),
            )
    return findings


def spacy_anchor_lint(nlp: spacy.Language, before: str, after: str) -> list[dict]:
    findings = anchor_drift_from_sets(spacy_anchors(nlp, before), spacy_anchors(nlp, after))

    before_auth = evidence_lint.authority_profile(before)
    after_auth = evidence_lint.authority_profile(after)
    stronger = after_auth["strong"] - before_auth["strong"]
    weaker_removed = before_auth["weak"] - after_auth["weak"]
    if stronger:
        evidence_lint.add_finding(
            findings,
            "blocker",
            "authority_strengthened",
            "Authority marker was strengthened.",
            list(stronger),
        )
    if weaker_removed and after_auth["strong"]:
        evidence_lint.add_finding(
            findings,
            "warning",
            "hedge_removed",
            "Hedging may have been removed.",
            list(weaker_removed),
        )

    before_direction = evidence_lint.direction_profile(before)
    after_direction = evidence_lint.direction_profile(after)
    if (
        ("increase" in before_direction and "decrease" in after_direction)
        or ("decrease" in before_direction and "increase" in after_direction)
    ):
        evidence_lint.add_finding(
            findings,
            "blocker",
            "claim_direction_changed",
            "Claim direction changed between increase and decrease.",
            sorted(before_direction | after_direction),
        )

    return findings


def regex_anchor_lint(before: str, after: str) -> list[dict]:
    return evidence_lint.lint(before, after)


def finding_kinds(findings: Iterable[dict]) -> set[str]:
    return {item["kind"] for item in findings}


def precision_recall_f1(tp: int, fp: int, fn: int) -> dict[str, float | int]:
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def binary_metrics(expected: Iterable[bool], actual: Iterable[bool]) -> dict[str, float | int]:
    tp = fp = fn = tn = 0
    for exp, act in zip(expected, actual, strict=True):
        if exp and act:
            tp += 1
        elif exp and not act:
            fn += 1
        elif not exp and act:
            fp += 1
        else:
            tn += 1
    metrics = precision_recall_f1(tp, fp, fn)
    metrics["tn"] = tn
    return metrics


def counter_metrics(expected: Iterable[tuple[str, str]], actual: Iterable[tuple[str, str]]) -> dict[str, float | int]:
    expected_counter = Counter(expected)
    actual_counter = Counter(actual)
    tp = sum((expected_counter & actual_counter).values())
    fp = sum((actual_counter - expected_counter).values())
    fn = sum((expected_counter - actual_counter).values())
    return precision_recall_f1(tp, fp, fn)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    def cell(value: object) -> str:
        if isinstance(value, float):
            return f"{value:.3f}"
        return str(value).replace("\n", " ")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return "\n".join(lines)


def json_default(value: object) -> object:
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, MatchHit):
        return value.__dict__
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def dump_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=json_default)
