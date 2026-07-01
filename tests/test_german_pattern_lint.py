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


class GermanPatternLintTests(unittest.TestCase):
    def test_ai_marker_cluster(self):
        text = "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft."
        self.assertIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_single_marker_is_not_cluster(self):
        text = "Die robuste Statistik nutzt ein dynamisches Routing."
        self.assertNotIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_copula_avoidance_cluster(self):
        text = "Die Plattform fungiert als Werkzeug und verfügt über mehrere Module."
        self.assertIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_formal_particles_are_reported(self):
        text = "Die Entscheidung ist ja eben wichtig."
        self.assertIn("particles_outside_locker", kinds(german_pattern_lint.lint(text, mode="formal")))

    def test_particle_stems_do_not_match_unrelated_words(self):
        text = "Das Ergebnis stammt aus dem Januar. Wir mussten die Haltung mehrmals ändern, ebenso die Malerei."
        self.assertNotIn("particles_outside_locker", kinds(german_pattern_lint.lint(text, mode="formal")))


if __name__ == "__main__":
    unittest.main()
