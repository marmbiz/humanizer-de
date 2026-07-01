#!/usr/bin/env python3
"""Regression probe for the de_core_news_sm labels used by this PoC."""

from __future__ import annotations

import sys

from spacy_measures import is_passive_aux, load_nlp


CASES = {
    "passive_fragment": "Keine Konfigurationsdatei nötig. Die Ergebnisse werden automatisch gespeichert.",
    "passive_agent": "Der Bericht wurde vom Team geprüft.",
    "future": "Ich werde das morgen tun.",
    "active_abstract_agent": "Die Analyse zeigt einen klaren Trend.",
}


def token_rows(doc) -> list[str]:
    rows = []
    for token in doc:
        if token.is_space:
            continue
        rows.append(
            f"  {token.text!r:<24} pos={token.pos_:<8} tag={token.tag_:<8} "
            f"dep={token.dep_:<6} head={token.head.text:<18} morph={token.morph}"
        )
    return rows


def assert_probe(nlp) -> None:
    passive_doc = nlp(CASES["passive_fragment"])
    first_sent, second_sent = list(passive_doc.sents)
    if first_sent.root.text != "Konfigurationsdatei" or first_sent.root.pos_ != "NOUN":
        raise AssertionError("Expected subjectless fragment root to be NOUN 'Konfigurationsdatei'.")
    if any(token.pos_ in {"VERB", "AUX"} and "Fin" in token.morph.get("VerbForm") for token in first_sent):
        raise AssertionError("Expected subjectless fragment to contain no finite verb/AUX.")
    passive_auxes = [token for token in second_sent if is_passive_aux(token)]
    if [token.lemma_ for token in passive_auxes] != ["werden"]:
        raise AssertionError("Expected passive 'werden' AUX with oc VVPP participle.")

    agent_doc = nlp(CASES["passive_agent"])
    if not any(token.dep_ == "sbp" and token.lemma_ == "von" for token in agent_doc):
        raise AssertionError("Expected passive agent phrase to use dep_=sbp on 'von/vom'.")

    future_doc = nlp(CASES["future"])
    future_aux = next(token for token in future_doc if token.lemma_ == "werden")
    future_ocs = [child for child in future_aux.children if child.dep_ == "oc"]
    if not future_ocs or future_ocs[0].tag_ != "VVINF" or "Inf" not in future_ocs[0].morph.get("VerbForm"):
        raise AssertionError("Expected future/modal 'werden' oc child to be VVINF/VerbForm=Inf.")
    if is_passive_aux(future_aux):
        raise AssertionError("Future/modal 'werden' must not match passive.")

    active_doc = nlp(CASES["active_abstract_agent"])
    root = next(token for token in active_doc if token.dep_ == "ROOT")
    if root.pos_ != "VERB" or not any(child.dep_ == "sb" for child in root.children):
        raise AssertionError("Expected 'Die Analyse zeigt...' to be an active clause with sb subject.")
    if any(is_passive_aux(token) for token in active_doc):
        raise AssertionError("Active abstract-agent clause must not match passive.")


def main() -> int:
    nlp = load_nlp()
    assert_probe(nlp)
    print(f"spaCy model: {nlp.meta.get('name')} {nlp.meta.get('version')}")
    print("Tagset probe: OK")
    for name, text in CASES.items():
        print(f"\nTEXT ({name}): {text}")
        print("\n".join(token_rows(nlp(text))))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Tagset probe failed: {exc}", file=sys.stderr)
        raise
