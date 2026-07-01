#!/usr/bin/env python3
"""Run the spaCy PoC fixtures and corpus comparison."""

from __future__ import annotations

from collections import Counter
import argparse
import json
from pathlib import Path
import statistics

from spacy_measures import (
    ROOT,
    build_phrase_matcher,
    counter_metrics,
    detect_lemma_phrases,
    detect_passive,
    detect_pattern39,
    detect_subjectless_fragment,
    dump_json,
    evidence_lint,
    finding_kinds,
    german_pattern_lint,
    load_nlp,
    markdown_table,
    nominal_verb_ratio,
    regex_anchor_lint,
    spacy_anchor_lint,
    spacy_name_anchors,
)


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
RESULTS = HERE / "results"
EXTERNAL_POSTS = Path("/Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(value: float) -> str:
    return f"{value:.3f}"


def bool_mark(value: bool) -> str:
    return "yes" if value else "no"


def evaluate_pattern39(nlp) -> dict:
    data = load_json(FIXTURES / "pattern39.json")
    expected: list[bool] = []
    actual: list[bool] = []
    rows: list[dict] = []
    protected_fp = 0
    for case in data["cases"]:
        doc = nlp(case["text"])
        passive = detect_passive(doc)
        fragments = detect_subjectless_fragment(doc)
        predicted = bool(passive or fragments)
        wanted = bool(case["expect_passive"] or case["expect_fragment"])
        expected.append(wanted)
        actual.append(predicted)
        if case.get("protected_negative") and predicted:
            protected_fp += 1
        rows.append(
            {
                "id": case["id"],
                "expected": wanted,
                "actual": predicted,
                "passive": bool(passive),
                "fragment": bool(fragments),
                "protected_negative": bool(case.get("protected_negative")),
                "text": case["text"],
            }
        )
    metrics = binary_metrics(expected, actual)
    return {
        "name": "Passiv + subjektlose Fragmente",
        "metrics": metrics,
        "protected_false_positives": protected_fp,
        "success": protected_fp == 0 and metrics["precision"] == 1.0 and metrics["recall"] == 1.0,
        "rows": rows,
    }


def binary_metrics(expected: list[bool], actual: list[bool]) -> dict:
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
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": precision, "recall": recall, "f1": f1}


def evaluate_nominal_style(nlp) -> dict:
    data = load_json(FIXTURES / "nominal_style.json")
    scored = []
    for case in data["cases"]:
        result = nominal_verb_ratio(nlp(case["text"]))
        scored.append(
            {
                "id": case["id"],
                "expected_label": case["label"],
                "expected_nominal": case["label"] == "nominal",
                "ratio": result["ratio"],
                "nouns": result["nouns"],
                "verbs": result["verbs"],
                "text": case["text"],
            }
        )
    nominal_count = sum(1 for item in scored if item["expected_nominal"])
    ranked = sorted(scored, key=lambda item: (item["ratio"], item["nouns"]), reverse=True)
    predicted_nominal_ids = {item["id"] for item in ranked[:nominal_count]}
    expected = []
    actual = []
    correct = 0
    for item in scored:
        predicted = item["id"] in predicted_nominal_ids
        item["predicted_nominal"] = predicted
        expected.append(item["expected_nominal"])
        actual.append(predicted)
        if predicted == item["expected_nominal"]:
            correct += 1
    metrics = binary_metrics(expected, actual)
    return {
        "name": "Nomen-Verb-Verhältnis",
        "metrics": metrics,
        "correct_ranked": correct,
        "total": len(scored),
        "success": correct >= 18,
        "rows": sorted(scored, key=lambda item: item["id"]),
    }


def expected_hit_keys(case: dict) -> list[tuple[str, str]]:
    return [(item["category"], item["marker"]) for item in case.get("expected", [])]


def evaluate_lemma_phrases(nlp) -> dict:
    data = load_json(FIXTURES / "lemma_phrases.json")
    matcher = build_phrase_matcher(nlp)
    expected_all: list[tuple[str, str]] = []
    actual_all: list[tuple[str, str]] = []
    rows: list[dict] = []
    flexion_failures: list[str] = []
    carveout_false_positives: list[str] = []
    for case in data["cases"]:
        doc = nlp(case["text"])
        hits = detect_lemma_phrases(doc, matcher)
        expected = expected_hit_keys(case)
        actual = [hit.key for hit in hits]
        expected_all.extend(expected)
        actual_all.extend(actual)
        missing = Counter(expected) - Counter(actual)
        extra = Counter(actual) - Counter(expected)
        if case.get("flexion_target") and missing:
            flexion_failures.append(case["id"])
        if case.get("carveout_negative") and extra:
            carveout_false_positives.append(case["id"])
        rows.append(
            {
                "id": case["id"],
                "expected": [f"{cat}:{marker}" for cat, marker in expected],
                "actual": [f"{hit.category}:{hit.marker}:{hit.text}" for hit in hits],
                "ok": not missing and not extra,
                "text": case["text"],
            }
        )
    metrics = counter_metrics(expected_all, actual_all)
    return {
        "name": "Lemma-Floskeln",
        "metrics": metrics,
        "flexion_failures": flexion_failures,
        "carveout_false_positives": carveout_false_positives,
        "success": not flexion_failures and not carveout_false_positives,
        "rows": rows,
    }


def evaluate_ner(nlp) -> dict:
    data = load_json(FIXTURES / "ner_anchors.json")
    regex_expected_entities: list[tuple[str, str]] = []
    regex_actual_entities: list[tuple[str, str]] = []
    spacy_expected_entities: list[tuple[str, str]] = []
    spacy_actual_entities: list[tuple[str, str]] = []
    entity_rows: list[dict] = []
    for case in data["entities"]:
        expected = [("proper_name", value) for value in case["expected_names"]]
        regex_actual = [("proper_name", value) for value in evidence_lint.anchors(case["text"])["proper_name"]]
        spacy_actual = [("proper_name", value) for value in spacy_name_anchors(nlp(case["text"]))]
        regex_expected_entities.extend(expected)
        regex_actual_entities.extend(regex_actual)
        spacy_expected_entities.extend(expected)
        spacy_actual_entities.extend(spacy_actual)
        entity_rows.append(
            {
                "id": case["id"],
                "expected": [value for _, value in expected],
                "regex": [value for _, value in regex_actual],
                "spacy": [value for _, value in spacy_actual],
                "text": case["text"],
            }
        )

    regex_expected_drift: list[tuple[str, str]] = []
    regex_actual_drift: list[tuple[str, str]] = []
    spacy_expected_drift: list[tuple[str, str]] = []
    spacy_actual_drift: list[tuple[str, str]] = []
    drift_rows: list[dict] = []
    for case in data["drift_pairs"]:
        expected = [("finding", kind) for kind in case.get("expected_kinds", [])]
        regex_findings = regex_anchor_lint(case["before"], case["after"])
        spacy_findings = spacy_anchor_lint(nlp, case["before"], case["after"])
        regex_actual = [("finding", kind) for kind in finding_kinds(regex_findings)]
        spacy_actual = [("finding", kind) for kind in finding_kinds(spacy_findings)]
        regex_expected_drift.extend(expected)
        regex_actual_drift.extend(regex_actual)
        spacy_expected_drift.extend(expected)
        spacy_actual_drift.extend(spacy_actual)
        drift_rows.append(
            {
                "id": case["id"],
                "expected": [kind for _, kind in expected],
                "regex": sorted(finding_kinds(regex_findings)),
                "spacy": sorted(finding_kinds(spacy_findings)),
                "before": case["before"],
                "after": case["after"],
            }
        )

    regex_entity_metrics = counter_metrics(regex_expected_entities, regex_actual_entities)
    spacy_entity_metrics = counter_metrics(spacy_expected_entities, spacy_actual_entities)
    regex_drift_metrics = counter_metrics(regex_expected_drift, regex_actual_drift)
    spacy_drift_metrics = counter_metrics(spacy_expected_drift, spacy_actual_drift)
    success = (
        spacy_drift_metrics["precision"] >= regex_drift_metrics["precision"]
        and spacy_drift_metrics["recall"] >= regex_drift_metrics["recall"]
    )
    return {
        "name": "NER-Anker",
        "metrics": spacy_drift_metrics,
        "regex_drift_metrics": regex_drift_metrics,
        "spacy_drift_metrics": spacy_drift_metrics,
        "regex_entity_metrics": regex_entity_metrics,
        "spacy_entity_metrics": spacy_entity_metrics,
        "success": success,
        "entity_rows": entity_rows,
        "drift_rows": drift_rows,
    }


def corpus_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for path in sorted((ROOT / "tests" / "corpus").rglob("*.md")):
        files.append(("golden", path))
    for path in sorted(EXTERNAL_POSTS.glob("*.md")):
        files.append(("lab-posts", path))
    return files


def compare_corpora(nlp) -> dict:
    matcher = build_phrase_matcher(nlp)
    rows = []
    for group, path in corpus_files():
        text = path.read_text(encoding="utf-8")
        doc = nlp(text)
        pattern_report = german_pattern_lint.lint(text)
        lemma_hits = detect_lemma_phrases(doc, matcher)
        nominal = nominal_verb_ratio(doc)
        passive = detect_passive(doc)
        fragments = detect_subjectless_fragment(doc)
        regex_names = evidence_lint.anchors(text)["proper_name"]
        spacy_names = spacy_name_anchors(doc)
        rows.append(
            {
                "group": group,
                "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                "regex_pattern_kinds": sorted(item["kind"] for item in pattern_report["findings"]),
                "spacy_passive": len(passive),
                "spacy_fragments": len(fragments),
                "nominal_ratio": nominal["ratio"],
                "nouns": nominal["nouns"],
                "verbs": nominal["verbs"],
                "lemma_hits": len(lemma_hits),
                "lemma_markers": sorted({f"{hit.category}:{hit.marker}" for hit in lemma_hits}),
                "regex_names": len(regex_names),
                "spacy_names": len(spacy_names),
            }
        )
    lab_ratios = [row["nominal_ratio"] for row in rows if row["group"] == "lab-posts"]
    distribution = {
        "count": len(lab_ratios),
        "min": min(lab_ratios) if lab_ratios else 0,
        "median": statistics.median(lab_ratios) if lab_ratios else 0,
        "mean": statistics.fmean(lab_ratios) if lab_ratios else 0,
        "max": max(lab_ratios) if lab_ratios else 0,
    }
    return {"rows": rows, "lab_nominal_distribution": distribution}


def write_fixture_report(results: dict) -> None:
    rows = []
    for key in ["pattern39", "nominal_style", "lemma_phrases"]:
        item = results[key]
        metrics = item["metrics"]
        rows.append(
            [
                item["name"],
                metrics["precision"],
                metrics["recall"],
                metrics["f1"],
                bool_mark(item["success"]),
            ]
        )
    ner = results["ner"]
    regex_metrics = ner["regex_drift_metrics"]
    spacy_metrics = ner["spacy_drift_metrics"]
    rows.append(
        [
            "NER-Anker Drift (Regex baseline)",
            regex_metrics["precision"],
            regex_metrics["recall"],
            regex_metrics["f1"],
            "baseline",
        ]
    )
    rows.append(
        [
            "NER-Anker Drift (spaCy names)",
            spacy_metrics["precision"],
            spacy_metrics["recall"],
            spacy_metrics["f1"],
            bool_mark(ner["success"]),
        ]
    )
    content = [
        "# spaCy PoC Fixture Report",
        "",
        markdown_table(["Messung", "Precision", "Recall", "F1", "Success"], rows),
        "",
        "## Pattern 39 Cases",
        "",
        markdown_table(
            ["ID", "Expected", "Actual", "Passive", "Fragment", "Protected"],
            [
                [
                    row["id"],
                    bool_mark(row["expected"]),
                    bool_mark(row["actual"]),
                    bool_mark(row["passive"]),
                    bool_mark(row["fragment"]),
                    bool_mark(row["protected_negative"]),
                ]
                for row in results["pattern39"]["rows"]
            ],
        ),
        "",
        "## Nominal Style Cases",
        "",
        markdown_table(
            ["ID", "Label", "Predicted Nominal", "Nouns", "Verbs", "Ratio"],
            [
                [
                    row["id"],
                    row["expected_label"],
                    bool_mark(row["predicted_nominal"]),
                    row["nouns"],
                    row["verbs"],
                    row["ratio"],
                ]
                for row in results["nominal_style"]["rows"]
            ],
        ),
        "",
        "## Lemma Phrase Cases",
        "",
        markdown_table(
            ["ID", "OK", "Expected", "Actual"],
            [
                [
                    row["id"],
                    bool_mark(row["ok"]),
                    ", ".join(row["expected"]),
                    ", ".join(row["actual"]),
                ]
                for row in results["lemma_phrases"]["rows"]
            ],
        ),
        "",
        "## NER Entity Cases",
        "",
        markdown_table(
            ["ID", "Expected", "Regex", "spaCy"],
            [
                [
                    row["id"],
                    ", ".join(row["expected"]),
                    ", ".join(row["regex"]),
                    ", ".join(row["spacy"]),
                ]
                for row in results["ner"]["entity_rows"]
            ],
        ),
        "",
        "## NER Drift Cases",
        "",
        markdown_table(
            ["ID", "Expected", "Regex", "spaCy"],
            [
                [
                    row["id"],
                    ", ".join(row["expected"]),
                    ", ".join(row["regex"]),
                    ", ".join(row["spacy"]),
                ]
                for row in results["ner"]["drift_rows"]
            ],
        ),
        "",
    ]
    (RESULTS / "fixture_report.md").write_text("\n".join(content), encoding="utf-8")


def write_corpus_report(corpus: dict) -> None:
    rows = corpus["rows"]
    distribution = corpus["lab_nominal_distribution"]
    content = [
        "# spaCy PoC Corpus Comparison",
        "",
        "## Lab-Post Nominal Ratio Distribution",
        "",
        markdown_table(
            ["Count", "Min", "Median", "Mean", "Max"],
            [[distribution["count"], distribution["min"], distribution["median"], distribution["mean"], distribution["max"]]],
        ),
        "",
        "## Files",
        "",
        markdown_table(
            [
                "Group",
                "File",
                "Regex Pattern Kinds",
                "Passive",
                "Fragments",
                "N/V Ratio",
                "Lemma Hits",
                "Regex Names",
                "spaCy Names",
            ],
            [
                [
                    row["group"],
                    row["file"],
                    ", ".join(row["regex_pattern_kinds"]),
                    row["spacy_passive"],
                    row["spacy_fragments"],
                    row["nominal_ratio"],
                    row["lemma_hits"],
                    row["regex_names"],
                    row["spacy_names"],
                ]
                for row in rows
            ],
        ),
        "",
    ]
    (RESULTS / "corpus_comparison.md").write_text("\n".join(content), encoding="utf-8")


def run() -> dict:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nlp = load_nlp()
    results = {
        "model": {"name": nlp.meta.get("name"), "version": nlp.meta.get("version")},
        "pattern39": evaluate_pattern39(nlp),
        "nominal_style": evaluate_nominal_style(nlp),
        "lemma_phrases": evaluate_lemma_phrases(nlp),
        "ner": evaluate_ner(nlp),
    }
    corpus = compare_corpora(nlp)
    write_fixture_report(results)
    write_corpus_report(corpus)
    (RESULTS / "fixture_report.json").write_text(dump_json(results), encoding="utf-8")
    (RESULTS / "corpus_comparison.json").write_text(dump_json(corpus), encoding="utf-8")
    return {"fixtures": results, "corpus": corpus}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run spaCy PoC comparison.")
    parser.add_argument("--json", action="store_true", help="Print full JSON instead of compact summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = run()
    if args.json:
        print(dump_json(output))
    else:
        rows = []
        fixtures = output["fixtures"]
        for key in ["pattern39", "nominal_style", "lemma_phrases"]:
            item = fixtures[key]
            metrics = item["metrics"]
            rows.append(
                [
                    item["name"],
                    pct(metrics["precision"]),
                    pct(metrics["recall"]),
                    pct(metrics["f1"]),
                    bool_mark(item["success"]),
                ]
            )
        ner = fixtures["ner"]
        metrics = ner["spacy_drift_metrics"]
        rows.append(
            [
                "NER-Anker Drift",
                pct(metrics["precision"]),
                pct(metrics["recall"]),
                pct(metrics["f1"]),
                bool_mark(ner["success"]),
            ]
        )
        print(markdown_table(["Messung", "Precision", "Recall", "F1", "Success"], rows))
        print(f"\nWrote reports to {RESULTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
