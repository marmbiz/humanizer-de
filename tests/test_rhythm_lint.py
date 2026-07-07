import io
import importlib.util
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "rhythm_lint.py"

spec = importlib.util.spec_from_file_location("rhythm_lint", SCRIPT)
rhythm_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rhythm_lint)


def pattern_ids(report):
    return {item["pattern"] for item in report["suspicions"]}


def run_cli(argv):
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        exit_code = rhythm_lint.main(argv)
    return exit_code, json.loads(stdout.getvalue())


class RhythmLintTests(unittest.TestCase):
    def test_sir_cluster_flags_pattern_55(self):
        # SIR fires only when high ratio AND (low variance OR repeated openers).
        # All 8 sentences subjektinitial + identical 2-token opener = cluster condition met.
        text = (
            "Das Team plant jeden Morgen die Aufgaben für den Sprint. "
            "Das Team prüft danach die offenen Punkte im Board. "
            "Das Team schreibt am Nachmittag die Tests für das Modul. "
            "Das Team sammelt am Abend Rückmeldungen aus dem Workshop. "
            "Das Team dokumentiert alle Entscheidungen im Protokoll. "
            "Das Team verteilt danach die Aufgaben an die Beteiligten. "
            "Das Team aktualisiert anschließend die Notizen im Wiki. "
            "Das Team prüft zuletzt die Darstellung auf mobilen Geräten."
        )
        self.assertIn(55, pattern_ids(rhythm_lint.analyze(text)))

    def test_sir_alone_does_not_flag_pattern_55(self):
        # High SIR without low variance or repeated openers must not fire alone —
        # empirically 95% of human German blog posts exceed SIR 0.75.
        # Sentence lengths deliberately spread (3–30 words) to keep stddev/mean >= 0.6.
        text = (
            "Gut. "
            "Der Entwickler schreibt Tests. "
            "Die Designerin prüft am frühen Abend die vollständige Darstellung auf allen mobilen Geräten, "
            "weil die Nutzerzahlen dort seit Monaten steigen. "
            "Das Team plant. "
            "Die Gruppe dokumentiert alle wichtigen Entscheidungen aus dem langen Workshop in einem sehr ausführlichen Protokoll, "
            "das später auch als Grundlage für den nächsten Sprint dienen soll. "
            "Der Dienst startet neu. "
            "Die Leitung verteilt die Aufgaben."
        )
        report = rhythm_lint.analyze(text)
        sir_hits = [s for s in report["suspicions"] if s["pattern"] == 55 and "subject-initial" in s["reason"]]
        self.assertEqual(sir_hits, [])

    def test_varied_text_does_not_flag_pattern_55(self):
        text = (
            "Zunächst startet der Test. "
            "Weil die Daten fehlen, pausiert das Team und prüft die Quelle. "
            "In der Nacht verarbeitet der Dienst eine große Datei mit alten Buchungen und neuen Randfällen. "
            "Das reicht. "
            "Mit dem nächsten Lauf sinkt die Fehlerrate deutlich, obwohl ein Import weiterhin langsam bleibt. "
            "Nachdem die Warnung verschwunden ist, löscht niemand die Notizen aus dem Protokoll. "
            "Dann folgt nur ein kurzer Check. "
            "Für die Freigabe sammelt Maria die offenen Punkte, weil zwei Teams denselben Dienst nutzen."
        )
        self.assertNotIn(55, pattern_ids(rhythm_lint.analyze(text)))

    def test_main_clause_run_not_flagged_as_suspicion(self):
        # Muster 51 removed from suspicion output: has_subjunction() misses relative clauses,
        # infinitive groups and coordination — fires on 100% of human German blog posts.
        # main_clause_run is still measured in the document block.
        text = (
            "Das Team plant die Migration. "
            "Die Gruppe prüft die Daten. "
            "Der Dienst speichert die Werte. "
            "Die Leitung startet den Rollout."
        )
        report = rhythm_lint.analyze(text)
        self.assertNotIn(51, pattern_ids(report))
        self.assertGreaterEqual(report["document"]["max_main_clause_run"], 4)

    def test_code_block_content_is_ignored(self):
        text = (
            "```\n"
            "Das Team plant die Arbeit. Die Gruppe prüft die Daten. "
            "Der Dienst speichert die Werte. Die Leitung startet den Rollout. "
            "Das Team plant die Arbeit. Die Gruppe prüft die Daten. "
            "Der Dienst speichert die Werte. Die Leitung startet den Rollout.\n"
            "```\n\n"
            "Kurz."
        )
        report = rhythm_lint.analyze(text)
        self.assertEqual(report["document"]["sentence_count"], 1)
        self.assertNotIn(55, pattern_ids(report))
        self.assertNotIn(51, pattern_ids(report))

    def test_markdown_table_rows_are_not_prose_blocks(self):
        text = (
            "Ein kurzer Vorspann erklärt die Tabelle.\n\n"
            "| Nr. | Muster | Schwere |\n"
            "|---|---|---|\n"
            '| 1 | Mechanische Konjunktionen ("darüber hinaus", "außerdem") | HIGH |\n'
            '| 2 | Abschnitts-Zusammenfassungen ("insgesamt") | HIGH |\n'
            '| 3 | Persuasive Floskeln ("Im Kern", "In Wirklichkeit") | MEDIUM |\n\n'
            "Ein kurzer Nachsatz beendet den Abschnitt."
        )
        report = rhythm_lint.analyze(text)

        self.assertEqual(report["document"]["sentence_count"], 2)
        self.assertEqual(report["document"]["connector_density"], 0)
        self.assertNotIn(4, pattern_ids(report))

    def test_html_summary_lines_are_not_prose_blocks(self):
        text = (
            "<details>\n"
            "<summary><strong>Inhalt</strong></summary>\n\n"
            "Ein echter Satz bleibt sichtbar.\n\n"
            "</details>\n"
            "<details>\n"
            "<summary><strong>Inhalt</strong></summary>\n\n"
            "Ein zweiter Satz bleibt sichtbar.\n\n"
            "</details>\n"
        )
        report = rhythm_lint.analyze(text)

        self.assertEqual(report["document"]["sentence_count"], 2)
        self.assertEqual(report["document"]["repeated_openers"], [])

    def test_version_list_openers_do_not_count_as_repeated_openers(self):
        text = (
            "- **5.1.1** - Skill-Routing geschärft.\n"
            "- **5.1.0** - Vier Muster geschärft.\n"
            "- **4.3.1** - Naturalness-Guidance geschärft.\n"
            "- **4.3.0** - Factual-Reliability-Gate geschärft.\n"
        )
        report = rhythm_lint.analyze(text)

        self.assertEqual(report["document"]["repeated_openers"], [])

    def test_connector_density_flags_pattern_4(self):
        text = "Darüber hinaus prüft das Team die Werte. Darüber hinaus speichert es die Notizen."
        self.assertIn(4, pattern_ids(rhythm_lint.analyze(text)))

    def test_skill_doc_scope_does_not_surface_pattern_51(self):
        text = (
            "Prüfe den Modus. Lies die Quelle. Markiere die Lücke. "
            "Bewahre den Satz. Entferne den Platzhalter. Melde den Befund. "
            "Teste die Ausgabe. Stoppe bei Fehlern."
        )
        report = rhythm_lint.analyze(text, scope="skill_doc")
        self.assertNotIn(51, pattern_ids(report))

    def test_formal_mode_does_not_surface_pattern_51(self):
        text = (
            "Die Datenerhebung wurde abgeschlossen. "
            "Die Auswertung wurde dokumentiert. "
            "Die Ergebnisse wurden geprüft. "
            "Die Methode wurde beschrieben."
        )
        report = rhythm_lint.analyze(text, mode="formal")
        self.assertNotIn(51, pattern_ids(report))

    def test_cli_default_omits_paragraph_details(self):
        exit_code, report = run_cli(["--text", "Kurz. Noch ein Satz."])
        self.assertEqual(exit_code, 0)
        self.assertNotIn("paragraphs", report)
        self.assertNotIn("paragraph_sentence_counts", report["document"])
        self.assertNotIn("connector_density_by_paragraph", report["document"])
        self.assertIn("sentence_length_buckets", report["document"])
        self.assertIn("syntactic_complexity_variance", report["document"])
        self.assertIn("paragraph_sentence_counts_uniform", report["document"])
        self.assertIn("raw_suspicions", report)
        self.assertIn("suppressed", report)
        self.assertIn("suspicions", report)

    def test_cli_include_paragraphs_restores_full_output(self):
        exit_code, report = run_cli(["--text", "Kurz. Noch ein Satz.", "--include-paragraphs"])
        self.assertEqual(exit_code, 0)
        self.assertIn("paragraphs", report)
        self.assertIn("paragraph_sentence_counts", report["document"])
        self.assertIn("connector_density_by_paragraph", report["document"])

    def test_sentence_length_buckets_are_deterministic(self):
        text = (
            "Kurz. "
            "Dieser Satz hat genau acht Wörter für den kurzen Bereich. "
            "Dieser längere Satz enthält mehrere Wörter, bleibt aber bewusst innerhalb des mittleren Bereichs, "
            "damit die Grenze zwischen kurz und lang sauber geprüft wird. "
            "Dieser sehr lange Satz enthält viele zusätzliche Wörter, weil die Messung den langen Bereich oberhalb "
            "von achtundzwanzig Wörtern zuverlässig zählen soll und deshalb genug Material für eine belastbare Probe braucht."
        )
        report = rhythm_lint.analyze(text)
        buckets = report["document"]["sentence_length_buckets"]

        self.assertEqual(buckets["counts"], {"short_lt_12": 2, "medium_12_to_28": 1, "long_gt_28": 1})
        self.assertEqual(buckets["ratios"], {"short_lt_12": 0.5, "medium_12_to_28": 0.25, "long_gt_28": 0.25})


if __name__ == "__main__":
    unittest.main()
