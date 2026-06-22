import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "rhythm_lint.py"

spec = importlib.util.spec_from_file_location("rhythm_lint", SCRIPT)
rhythm_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rhythm_lint)


def pattern_ids(report):
    return {item["pattern"] for item in report["suspicions"]}


class RhythmLintTests(unittest.TestCase):
    def test_monotonous_subject_initial_text_flags_pattern_55(self):
        text = (
            "Das Team plant jeden Morgen die Aufgaben für den Sprint genau. "
            "Die Gruppe prüft danach die offenen Punkte im Board sorgfältig. "
            "Der Entwickler schreibt am Nachmittag die Tests für das Modul. "
            "Die Designerin sammelt am Abend Rückmeldungen aus dem Workshop. "
            "Das Team dokumentiert alle Entscheidungen in einem kurzen Protokoll. "
            "Die Gruppe verteilt danach die Aufgaben an die Beteiligten. "
            "Der Entwickler aktualisiert anschließend die Notizen im gemeinsamen Wiki. "
            "Die Designerin prüft zuletzt die Darstellung auf mobilen Geräten."
        )
        self.assertIn(55, pattern_ids(rhythm_lint.analyze(text)))

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

    def test_four_main_clauses_flag_pattern_51(self):
        text = (
            "Das Team plant die Migration. "
            "Die Gruppe prüft die Daten. "
            "Der Dienst speichert die Werte. "
            "Die Leitung startet den Rollout."
        )
        self.assertIn(51, pattern_ids(rhythm_lint.analyze(text)))

    def test_embedded_subclauses_do_not_flag_pattern_51(self):
        text = (
            "Das Team plant die Migration, weil der Termin steht. "
            "Die Gruppe prüft die Daten, während der Dienst wartet. "
            "Der Dienst speichert die Werte, nachdem der Import endet. "
            "Die Leitung startet den Rollout, wenn die Tests laufen."
        )
        self.assertNotIn(51, pattern_ids(rhythm_lint.analyze(text)))

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

    def test_connector_density_flags_pattern_4(self):
        text = "Darüber hinaus prüft das Team die Werte. Darüber hinaus speichert es die Notizen."
        self.assertIn(4, pattern_ids(rhythm_lint.analyze(text)))

    def test_skill_doc_scope_suppresses_instruction_rhythm(self):
        text = (
            "Prüfe den Modus. Lies die Quelle. Markiere die Lücke. "
            "Bewahre den Satz. Entferne den Platzhalter. Melde den Befund. "
            "Teste die Ausgabe. Stoppe bei Fehlern."
        )
        report = rhythm_lint.analyze(text, scope="skill_doc")
        self.assertNotIn(51, pattern_ids(report))
        self.assertTrue(any(item["pattern"] == 51 for item in report["suppressed"]))

    def test_formal_mode_suppresses_rhythm_style_suspicion(self):
        text = (
            "Die Datenerhebung wurde abgeschlossen. "
            "Die Auswertung wurde dokumentiert. "
            "Die Ergebnisse wurden geprüft. "
            "Die Methode wurde beschrieben."
        )
        report = rhythm_lint.analyze(text, mode="formal")
        self.assertNotIn(51, pattern_ids(report))
        self.assertTrue(report["suppressed"])


if __name__ == "__main__":
    unittest.main()
