import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "german_pattern_lint.py"

spec = importlib.util.spec_from_file_location("german_pattern_lint", SCRIPT)
german_pattern_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(german_pattern_lint)


def kinds(report):
    return {item["kind"] for item in report["findings"]}


def spacy_model_available():
    try:
        import spacy

        spacy.load("de_core_news_sm")
    except Exception:
        return False
    return True


SPACY_MODEL_AVAILABLE = spacy_model_available()


class GermanPatternLintTests(unittest.TestCase):
    def test_ai_marker_cluster(self):
        text = "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft."
        self.assertIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_single_marker_is_not_cluster(self):
        text = "Die robuste Statistik nutzt ein dynamisches Routing."
        self.assertNotIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ai_marker_mentions_in_quotes_are_not_cluster(self):
        text = (
            "Im Review ging es um Wörter wie „nahtlos“, „beleuchten“ und "
            "„maßgeschneidert“, nicht um ihren Einsatz im Text."
        )
        self.assertNotIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ai_marker_cluster_ignores_extra_quote_marker(self):
        text = (
            "Der Text beleuchtet den Prozess, bleibt dynamisch und nutzt ein "
            "vielschichtiges Modell. Im Review fiel auch „nahtlos“."
        )
        report = german_pattern_lint.lint(text)
        finding = next(item for item in report["findings"] if item["kind"] == "ai_marker_cluster")
        self.assertEqual(sum(finding["evidence"].values()), 3)

    def test_ai_marker_mentions_in_markdown_are_not_cluster(self):
        text = "Im Glossar steht *nahtlos* neben `beleuchten` und *maßgeschneidert*."
        self.assertNotIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_apostrophes_do_not_open_mention_spans(self):
        text = (
            "Das gibt's öfter: Der Text beleuchtet den Prozess, bleibt dynamisch "
            "und wirkt vielschichtig, sagt's Team."
        )
        self.assertIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_copula_avoidance_cluster(self):
        text = "Die Plattform fungiert als Werkzeug und verfügt über mehrere Module."
        self.assertIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_single_stellt_dar_is_not_double_counted(self):
        text = "Dies stellt dar, was gemeint ist."
        self.assertNotIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_stellt_full_verbs_are_not_copula_avoidance(self):
        text = "Der Bericht stellt eine Frage. Das Team stellt den Plan nächste Woche vor."
        self.assertNotIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_stellt_dar_cluster_counts_separable_forms(self):
        text = "Der Absatz stellt den Ablauf dar. Die Grafik stellt die Rollen dar."
        report = german_pattern_lint.lint(text)
        self.assertIn("copula_avoidance_cluster", kinds(report))
        finding = next(item for item in report["findings"] if item["kind"] == "copula_avoidance_cluster")
        self.assertEqual(finding["evidence"], {"stellt ... dar": 2})

    def test_default_regex_counts_sentence_boundary_stellt_dar(self):
        text = "Dies stellt sicher. Kurz darauf legte er dar, was passiert, und fungiert als Beispiel."
        self.assertIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_formal_particles_are_reported(self):
        text = "Die Entscheidung ist ja eben wichtig."
        self.assertIn("particles_outside_locker", kinds(german_pattern_lint.lint(text, mode="formal")))

    def test_protected_code_particles_are_ignored(self):
        text = "Sachlicher Text.\n\n```mermaid\nG -- ja --> O\n```"
        self.assertNotIn("particles_outside_locker", kinds(german_pattern_lint.lint(text, mode="formal")))

    def test_particle_stems_do_not_match_unrelated_words(self):
        text = "Das Ergebnis stammt aus dem Januar. Wir mussten die Haltung mehrmals ändern, ebenso die Malerei."
        self.assertNotIn("particles_outside_locker", kinds(german_pattern_lint.lint(text, mode="formal")))

    def test_negation_parallelism(self):
        text = "Kein Server, keine Datenbank. Kein Dashboard nötig."
        self.assertIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_factual_correction(self):
        text = "Ich will nicht Tee, sondern Kaffee."
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_single_negation(self):
        text = "Keine Sorge, das passt schon."
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_quoted_example(self):
        text = "Im Beispiel steht: „Kein Server, keine Datenbank.“"
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))


@unittest.skipUnless(SPACY_MODEL_AVAILABLE, "spaCy German model is not available")
class GermanPatternLintPreciseTests(unittest.TestCase):
    def test_precise_ignores_sentence_boundary_stellt_dar(self):
        text = "Dies stellt sicher. Kurz darauf legte er dar, was passiert, und fungiert als Beispiel."
        report = german_pattern_lint.lint(text, precise=True)

        self.assertNotIn("copula_avoidance_cluster", kinds(report))

    def test_precise_keeps_real_stellt_dar_cluster(self):
        text = "Dies stellt einen Fortschritt dar und fungiert als Beispiel."
        report = german_pattern_lint.lint(text, precise=True)

        self.assertIn("copula_avoidance_cluster", kinds(report))


if __name__ == "__main__":
    unittest.main()
