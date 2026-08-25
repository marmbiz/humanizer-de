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
    def test_tokens_keep_unicode_words_and_existing_joiner_semantics(self):
        text = "Résumé Émile Première Café Erdoğan Škoda Ørsted Nord-Süd-Achse gibt's"

        self.assertEqual(
            rhythm_lint.tokens(text),
            ["Résumé", "Émile", "Première", "Café", "Erdoğan", "Škoda", "Ørsted", "Nord-Süd", "Achse", "gibt's"],
        )

    def test_sentence_split_does_not_mask_words_ending_like_abbreviations(self):
        text = "Das ist ein Haus. Danach geht es nach Mallorca. Anschließend folgt der Schluss."

        self.assertEqual(
            rhythm_lint.split_sentences(text),
            ["Das ist ein Haus.", "Danach geht es nach Mallorca.", "Anschließend folgt der Schluss."],
        )

    def test_sentence_split_keeps_real_abbreviations(self):
        text = "Das gilt z. B. für Berlin. Siehe S. 12. Danach folgt mehr."

        self.assertEqual(
            rhythm_lint.split_sentences(text),
            ["Das gilt z. B. für Berlin.", "Siehe S. 12.", "Danach folgt mehr."],
        )

    def test_sentence_split_keeps_abs_abbreviation(self):
        text = "Nach § 12 Abs. 3 gilt die Frist."

        self.assertEqual(rhythm_lint.split_sentences(text), [text])

    def test_sentence_split_keeps_art_abbreviation(self):
        text = "Gemäß Art. 5 der Verordnung entfällt."

        self.assertEqual(rhythm_lint.split_sentences(text), [text])

    def test_sentence_split_keeps_msp_abbreviation(self):
        text = "Siehe Msp. 14 des Kommentars."

        self.assertEqual(rhythm_lint.split_sentences(text), [text])

    def test_sentence_split_keeps_numbered_list_items_whole(self):
        text = "1. Erster Punkt\n2. Zweiter Punkt\n3. Dritter Punkt"

        self.assertEqual(
            rhythm_lint.split_sentences(text),
            ["1. Erster Punkt", "2. Zweiter Punkt", "3. Dritter Punkt"],
        )

    def test_sentence_split_keeps_german_ordinals(self):
        texts = (
            "Im 19. Jahrhundert begann die Industrialisierung.",
            "Die 3. Auflage erschien später.",
            "Am 1. Advent beginnt die Feier.",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertEqual(rhythm_lint.split_sentences(text), [text])

    def test_sentence_split_keeps_genuine_boundary_after_number(self):
        text = "Wir zählten 3. Danach war Schluss."

        self.assertEqual(
            rhythm_lint.split_sentences(text),
            ["Wir zählten 3.", "Danach war Schluss."],
        )

    def test_bom_prefixed_markdown_heading_keeps_document_metrics(self):
        base = "# Titel: Kontext\n\nErster Satz hier. Zweiter Satz dort.\n"

        plain = rhythm_lint.analyze(base)["document"]
        with_bom = rhythm_lint.analyze("\ufeff" + base)["document"]

        self.assertEqual(with_bom, plain)
        self.assertEqual(with_bom["heading_count"], 1)
        self.assertEqual(with_bom["sentence_count"], 2)

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

    def test_adverbial_openers_are_not_subject_initial(self):
        text = " ".join(
            f"{opener} prüft das Team die Akte."
            for opener in ("Allerdings", "Natürlich", "Vielleicht", "Häufig", "Insbesondere")
        )
        self.assertEqual(rhythm_lint.subject_initial_ratio(rhythm_lint.split_sentences(text)), 0.0)

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

    def test_html_summary_text_remains_in_prose_scope(self):
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

        self.assertEqual(report["document"]["sentence_count"], 4)
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

    def test_skill_doc_scope_suppresses_pattern_55(self):
        text = (
            "Prüfe den Modus. Lies die Quelle. Markiere die Lücke. "
            "Bewahre den Satz. Entferne den Platzhalter. Melde den Befund. "
            "Teste die Ausgabe. Stoppe bei Fehlern."
        )
        self.assertIn(55, pattern_ids(rhythm_lint.analyze(text)))

        report = rhythm_lint.analyze(text, scope="skill_doc")
        self.assertNotIn(55, pattern_ids(report))
        self.assertIn(55, {item["pattern"] for item in report["suppressed"]})

    def test_formal_mode_suppresses_pattern_61(self):
        text = (
            "Die Datenerhebung wurde abgeschlossen.\n\n"
            "Die Auswertung wurde dokumentiert.\n\n"
            "Die Ergebnisse wurden geprüft.\n\n"
            "Die Methode wurde beschrieben."
        )
        self.assertIn(61, pattern_ids(rhythm_lint.analyze(text)))

        report = rhythm_lint.analyze(text, mode="formal")
        self.assertNotIn(61, pattern_ids(report))
        self.assertIn(61, {item["pattern"] for item in report["suppressed"]})

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
