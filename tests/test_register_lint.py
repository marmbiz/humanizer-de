import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "register_lint.py"

spec = importlib.util.spec_from_file_location("register_lint", SCRIPT)
register_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(register_lint)


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


class RegisterLintTests(unittest.TestCase):
    def test_mixed_du_sie_is_reported(self):
        report = register_lint.lint("Du kannst die Datei prüfen. Bitte senden Sie danach die Freigabe.")
        self.assertIn("mixed_address", kinds(report))

    def test_formal_voice_intrusion_is_blocker(self):
        report = register_lint.lint("Die Studie zeigt den Effekt. Klingt spannend?", mode="formal")
        self.assertIn("formal_voice_intrusion", kinds(report))

    def test_particles_outside_locker_are_reported(self):
        report = register_lint.lint("Das ist ja schon wichtig.", mode="sachlich")
        self.assertIn("particles_outside_locker", kinds(report))

    def test_locker_allows_sparse_particle(self):
        report = register_lint.lint("Das hilft ja im Alltag.", mode="locker")
        self.assertEqual(kinds(report), set())

    def test_protected_code_is_not_counted_as_register(self):
        text = (
            "Sachlicher Text.\n\n"
            "```mermaid\n"
            "G -- ja --> O\n"
            "Wie Sie sehen können, hilft das.\n"
            "```\n\n"
            "Noch ein Satz."
        )
        report = register_lint.lint(text, mode="sachlich")

        self.assertEqual(kinds(report), set())

    def test_neutral_profile_blocks_direct_address(self):
        du_report = register_lint.lint("Du bekommst die Auswertung morgen.", expected_address="neutral")
        sie_report = register_lint.lint("Sie erhalten die Auswertung morgen.", expected_address="neutral")
        wir_report = register_lint.lint("Wir prüfen die Auswertung morgen.", expected_address="neutral")
        self.assertIn("unexpected_direct_address", kinds(du_report))
        self.assertIn("unexpected_direct_address", kinds(sie_report))
        self.assertIn("unexpected_direct_address", kinds(wir_report))

    def test_wir_profile_blocks_du_or_sie(self):
        du_report = register_lint.lint("Du bekommst die Auswertung morgen.", expected_address="wir")
        sie_report = register_lint.lint("Sie erhalten die Auswertung morgen.", expected_address="wir")
        self.assertIn("unexpected_direct_address", kinds(du_report))
        self.assertIn("unexpected_direct_address", kinds(sie_report))

    def test_sentence_initial_sie_stays_counted_without_precise(self):
        text = "Die Idee war neu. Sie überzeugte sofort. Und du merkst das."
        report = register_lint.lint(text)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_without_spacy_keeps_blockquote_sie(self):
        text = "Du prüfst die Daten.\n\n> Bitte prüfen Sie Ihre Angaben.\n\nDann passt es."
        default_report = register_lint.lint(text)

        syntax_lint = register_lint.load_syntax_lint()
        sentinel = object()
        original = getattr(syntax_lint, "_HUMANIZER_PRECISE_CACHE", sentinel)
        syntax_lint._HUMANIZER_PRECISE_CACHE = (None, "spacy_missing")
        try:
            report = register_lint.lint(text, precise=True)
        finally:
            if original is sentinel:
                del syntax_lint._HUMANIZER_PRECISE_CACHE
            else:
                syntax_lint._HUMANIZER_PRECISE_CACHE = original

        self.assertEqual(
            report["precise"],
            {"requested": True, "active": False, "reason": "spacy_missing"},
        )
        self.assertEqual(report["features"], default_report["features"])
        self.assertEqual(report["findings"], default_report["findings"])
        self.assertIn("mixed_address", kinds(report))


@unittest.skipUnless(SPACY_MODEL_AVAILABLE, "spaCy German model is not available")
class RegisterLintPreciseTests(unittest.TestCase):
    def test_precise_ignores_sentence_initial_anaphoric_sie(self):
        text = "Die Idee war neu. Sie überzeugte sofort. Und du merkst das."
        report = register_lint.lint(text, precise=True)

        self.assertNotIn("mixed_address", kinds(report))

    def test_precise_keeps_real_sie_address(self):
        text = "Bitte prüfen Sie das. Du siehst es dann."
        report = register_lint.lint(text, precise=True)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_keeps_plural_anaphora_as_conservative_gap(self):
        text = "Die Teams arbeiteten getrennt. Sie trafen sich nur freitags. Und du merkst das."
        report = register_lint.lint(text, precise=True)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_ignores_sie_address_in_blockquote(self):
        text = "Du prüfst die Daten.\n\n> Bitte prüfen Sie Ihre Angaben.\n\nDann passt es."
        report = register_lint.lint(text, precise=True)

        self.assertNotIn("mixed_address", kinds(report))


if __name__ == "__main__":
    unittest.main()
