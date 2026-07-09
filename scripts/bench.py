#!/usr/bin/env python3
"""Run dev-only CPU benchmarks for the Humanizer-de linters."""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DEFAULT_BASELINE = ROOT / "tests" / "bench_baseline.json"
DEFAULT_SIZES_KB = (10, 70, 280)
DEFAULT_RUNS = 3
SEED = 20260709
TOLERANCE_UP = 1.3

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import humanizer_audit
import rhythm_lint
import unicode_lint


Benchmark = Callable[[str, Path], object]


SENTENCES = (
    "Das Team prueft die Passage, weil kleine stilistische Abweichungen im Gesamtbild sichtbar werden.",
    "Im ersten Entwurf standen mehrere Hinweise nebeneinander; jetzt fuehrt jeder Absatz einen eigenen Gedanken aus.",
    "Die Analyse bleibt nuetzlich, wenn sie konkrete Befunde nennt und keine pauschalen Urteile vorgibt.",
    "Gerade bei laengeren Markdown-Dateien muessen Code, Tabellen, Links und Fliesstext getrennt betrachtet werden.",
    "Die Redaktion vergleicht die Fassung mit dem Ausgangstext und markiert nur Befunde, die wirklich tragen.",
    "Ein kurzer Satz hilft.",
    "Danach folgt ein laengerer Satz mit einer eingebetteten Begruendung, damit die Rhythmusmessung unterschiedliche Laengen sieht.",
    '„Praezision vor Effekt", sagte die Projektleitung, und notierte die offene Frage direkt im Protokoll.',
    "Neben dem Bericht steht `konfiguration_alpha` als Codefragment, das der Unicode-Linter schuetzen soll.",
    "Weitere Details liegen unter https://example.org/projekt/bericht, werden hier aber nur als Kontext erwaehnt.",
    "Die Zahl 42 bleibt im Text, weil Evidenzanker in spaeteren Pruefungen nicht versehentlich wandern duerfen.",
    "Auf der zweiten Ebene steht ein Absatz, der sachlich klingt, aber trotzdem genug Variation fuer die Messung liefert.",
    "Manchmal beginnt ein Satz mit einem Umstand, manchmal mit dem Subjekt, und manchmal mit einer Einschraenkung.",
    "Diese Mischung ist absichtlich unspektakulaer, damit der Benchmark echte Linterarbeit statt Sonderfaelle misst.",
    "Zum Schluss benennt der Abschnitt eine Entscheidung: Die Aenderung wird dokumentiert, aber nicht dramatisiert.",
)

HEADINGS = (
    "Ausgangslage",
    "Befund und Kontext",
    "Redaktionelle Pruefung",
    "Risiko: Abgrenzung",
    "Naechster Schritt",
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic Humanizer-de CPU benchmarks.")
    parser.add_argument("--check", action="store_true", help="Compare results with tests/bench_baseline.json.")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE, help="Baseline JSON for --check.")
    parser.add_argument("--sizes", type=int, nargs="+", default=list(DEFAULT_SIZES_KB), help="Benchmark sizes in KB.")
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS, help="Runs per benchmark point; median is reported.")
    return parser.parse_args(argv)


def paragraph(rng: random.Random, paragraph_index: int) -> str:
    sentence_count = rng.randint(3, 7)
    offset = rng.randrange(len(SENTENCES))
    sentences = [SENTENCES[(offset + paragraph_index + step) % len(SENTENCES)] for step in range(sentence_count)]
    if paragraph_index % 7 == 3:
        sentences.append("- Pruefpunkt: klare Quelle, stabile Zahl, nachvollziehbarer Kontext.")
    if paragraph_index % 11 == 5:
        sentences.append("| Feld | Wert |\n|---|---|\n| Modus | sachlich |")
    return " ".join(sentences)


def synthetic_markdown(size_kb: int) -> str:
    rng = random.Random(SEED + size_kb)
    target_bytes = size_kb * 1024
    blocks = ["---\ntitle: Benchmark Probe\nlang: de\n---\n"]
    paragraph_index = 0
    while len("\n\n".join(blocks).encode("utf-8")) < target_bytes:
        if paragraph_index % 6 == 0:
            heading = HEADINGS[(paragraph_index // 6) % len(HEADINGS)]
            blocks.append(f"## {heading}")
        blocks.append(paragraph(rng, paragraph_index))
        paragraph_index += 1
    return "\n\n".join(blocks)


def benchmark_functions() -> dict[str, Benchmark]:
    return {
        "unicode_lint": lambda text, _path: unicode_lint.lint(text),
        "rhythm_lint": lambda text, path: rhythm_lint.analyze(
            text,
            file=str(path),
            scope="user_text",
            mode="sachlich",
        ),
        "humanizer_audit": lambda _text, path: humanizer_audit.analyze_file(
            path,
            mode="sachlich",
            mode_explicit=False,
            use_profile=False,
            precise=False,
        ),
    }


def median_cpu_seconds(func: Benchmark, text: str, path: Path, runs: int) -> float:
    timings = []
    for _ in range(runs):
        start = time.process_time()
        func(text, path)
        timings.append(time.process_time() - start)
    return round(statistics.median(timings), 6)


def run_benchmarks(sizes_kb: list[int], runs: int) -> dict[str, dict[str, float]]:
    if runs < 1:
        raise ValueError("--runs must be at least 1")
    if any(size < 1 for size in sizes_kb):
        raise ValueError("--sizes values must be positive")

    texts = {size: synthetic_markdown(size) for size in sizes_kb}
    results: dict[str, dict[str, float]] = {name: {} for name in benchmark_functions()}
    with tempfile.TemporaryDirectory(prefix="humanizer-bench-") as tmp:
        tmp_path = Path(tmp)
        paths: dict[int, Path] = {}
        for size, text in texts.items():
            path = tmp_path / f"sample-{size}kb.md"
            path.write_text(text, encoding="utf-8")
            paths[size] = path
        for name, func in benchmark_functions().items():
            for size in sizes_kb:
                results[name][f"{size}kb"] = median_cpu_seconds(func, texts[size], paths[size], runs)
    return results


def load_baseline(path: Path) -> dict:
    if not path.is_file():
        print(f"baseline file not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def regression_messages(results: dict[str, dict[str, float]], baseline: dict) -> list[str]:
    messages = []
    for bench_name, size_results in results.items():
        baseline_sizes = baseline.get(bench_name)
        if not isinstance(baseline_sizes, dict):
            messages.append(f"baseline missing benchmark: {bench_name}")
            continue
        for size_label, current in size_results.items():
            if size_label not in baseline_sizes:
                messages.append(f"baseline missing point: {bench_name} {size_label}")
                continue
            base = float(baseline_sizes[size_label])
            limit = base * TOLERANCE_UP
            if current > limit:
                messages.append(
                    f"benchmark regression: {bench_name} {size_label} "
                    f"current={current:.6f}s baseline={base:.6f}s limit={limit:.6f}s"
                )
    return messages


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or [])
    baseline = load_baseline(args.baseline) if args.check else None
    try:
        results = run_benchmarks(args.sizes, args.runs)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps(results, indent=2, sort_keys=True))
    if baseline is not None:
        messages = regression_messages(results, baseline)
        if messages:
            for message in messages:
                print(message, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
