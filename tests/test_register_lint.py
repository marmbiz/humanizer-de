import io
import importlib.util
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "register_lint.py"
STYLE_PROFILE_SCRIPT = ROOT / "scripts" / "style_profile.py"

spec = importlib.util.spec_from_file_location("register_lint", SCRIPT)
register_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(register_lint)

style_profile_spec = importlib.util.spec_from_file_location("style_profile", STYLE_PROFILE_SCRIPT)
style_profile = importlib.util.module_from_spec(style_profile_spec)
style_profile_spec.loader.exec_module(style_profile)


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
        text = "İ Du kannst die Datei prüfen. Bitte senden Sie danach die Freigabe."
        report = register_lint.lint(text)
        self.assertIn("mixed_address", kinds(report))
        finding = next(item for item in report["findings"] if item["kind"] == "mixed_address")
        self.assertEqual(
            [text[span["start"]:span["end"]] for span in finding["spans"]],
            ["Du", "Sie"],
        )
        self.assertEqual(report["features"], register_lint.features(text))

    def test_formal_question_is_warning_not_blocker(self):
        text = "Welche Folgen hat der Effekt?"
        report = register_lint.lint(text, mode="formal")

        finding = next(item for item in report["findings"] if item["kind"] == "formal_questions")
        self.assertEqual(finding["severity"], "warning")
        self.assertEqual(
            finding["message"],
            "Questions in formal mode: verify they are genuine content questions, not added rhetorical engagement.",
        )
        self.assertEqual([text[span["start"]:span["end"]] for span in finding["spans"]], ["?"])
        self.assertNotIn("formal_voice_intrusion", kinds(report))
        self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))

        with redirect_stdout(io.StringIO()):
            exit_code = register_lint.main(
                ["--text", text, "--mode", "formal", "--fail-on", "blocker"]
            )
        self.assertEqual(exit_code, 0)

    def test_bmp_emojis_trigger_formal_voice_intrusion(self):
        texts = (
            "Die Prüfung wurde abgeschlossen. ✅",
            "Die Auswertung enthält einen Warnhinweis. ⚠️",
            "Die Freigabe wurde abgelehnt. ❌",
            "Die Untersuchung betrifft die Herzgesundheit. ❤️",
            "Das Ergebnis wurde bestätigt. ✓",
            "Das Ergebnis wurde verworfen. ✗",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertGreaterEqual(register_lint.features(text)["emoji_count"], 1)
                report = register_lint.lint(text, mode="formal")
                self.assertFalse(report["ok"])
                finding = next(
                    item for item in report["findings"] if item["kind"] == "formal_voice_intrusion"
                )
                self.assertEqual(finding["severity"], "blocker")
                self.assertEqual(finding["message"], "Formal mode should not add emojis.")
                self.assertNotIn("formal_questions", kinds(report))

    def test_non_emoji_symbols_do_not_trigger_formal_voice_intrusion(self):
        texts = (
            "Der Inhalt ist urheberrechtlich geschützt ©.",
            "Die Marke ist registriert ®.",
            "Der Ablauf führt von links nach rechts →.",
            "Die Befehlstaste wird mit ⌘ bezeichnet.",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertEqual(register_lint.features(text)["emoji_count"], 0)
                report = register_lint.lint(text, mode="formal")
                self.assertNotIn("formal_voice_intrusion", kinds(report))

    def test_style_profile_emoji_count_matches_register_features(self):
        text = "Die Freigabe wurde erteilt. ✅ Die Warnung bleibt bestehen. ⚠️"

        register_count = register_lint.features(text)["emoji_count"]
        profile_count = style_profile.profile(text, "emoji-parity")["metrics"]["emoji_count"]

        self.assertEqual(profile_count, register_count)

    def test_particles_outside_locker_are_reported(self):
        report = register_lint.lint("Das ist ja schon wichtig.", mode="sachlich")
        self.assertIn("particles_outside_locker", kinds(report))

    def test_non_particle_readings_are_not_counted(self):
        texts = (
            "Vegetarisch: Ja",
            "Ja. Die Prüfung ist abgeschlossen.",
            "Die Probe wurde 5-mal geprüft, einmal morgens und dreimal abends.",
            "Schon einfache Organismen besitzen einen solchen Abwehrmechanismus.",
        )

        for text in texts:
            with self.subTest(text=text):
                report = register_lint.lint(text, mode="sachlich")
                self.assertEqual(report["features"]["modal_particle_count"], 0)
                self.assertNotIn("particles_outside_locker", kinds(report))

    def test_real_modal_particle_cluster_is_reported(self):
        text = "Das ist ja doch schon wichtig. Man könnte das eben mal prüfen."
        report = register_lint.lint(text, mode="sachlich")

        self.assertEqual(report["features"]["modal_particle_count"], 5)
        self.assertIn("particles_outside_locker", kinds(report))

    def test_locker_allows_sparse_particle(self):
        report = register_lint.lint(
            "Nun ist ja ein Gesetz beschlossen worden. Das ist doch keine neue Politik.",
            mode="locker",
        )
        self.assertEqual(report["features"]["modal_particle_count"], 2)
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

    def test_anaphoric_sie_with_du_form_stays_counted_without_precise(self):
        text = "Die Stilkarte gibt es auch einzeln, wenn dich die Messwerte interessieren. Sie kommt als JSON."
        report = register_lint.lint(text)

        self.assertIn("mixed_address", kinds(report))

    def test_sentence_initial_ihr_stays_counted_without_precise(self):
        texts = (
            "Du prüfst das. Ihr habt Fragen.",
            "Du prüfst das. Ihr Passwort ist abgelaufen.",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertIn("mixed_address", kinds(register_lint.lint(text)))

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

    def test_precise_ignores_anaphoric_sie_despite_du_form_in_previous_sentence(self):
        texts = (
            "Die Stilkarte gibt es auch einzeln, wenn die Messwerte interessieren. Sie kommt als JSON.",
            "Die Stilkarte gibt es auch einzeln, wenn dich die Messwerte interessieren. Sie kommt als JSON.",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertNotIn("mixed_address", kinds(register_lint.lint(text, precise=True)))

    def test_precise_uses_word_class_for_non_particle_readings(self):
        text = "Es ist das zweite Mal, dass die Prüfung stattfindet, doch Schäden entstanden nicht."
        report = register_lint.lint(text, mode="sachlich", precise=True)

        self.assertEqual(report["features"]["modal_particle_count"], 0)
        self.assertNotIn("particles_outside_locker", kinds(report))

    def test_precise_keeps_real_author_voice_address_shift(self):
        text = "Du prüfst den Text. Bitte senden Sie danach die Freigabe."
        report = register_lint.lint(text, precise=True)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_keeps_real_sie_address(self):
        text = "Bitte prüfen Sie das. Du siehst es dann."
        report = register_lint.lint(text, precise=True)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_ignores_sentence_initial_informal_plural_ihr(self):
        # "könnt" gehört dazu, weil das kleine Modell das Verb dort als dritte
        # Person Singular vertaggt. Erkannt wird deshalb am Pronomen, nicht am Verb.
        for text in (
            "Du prüfst das. Ihr habt Fragen.",
            "Du prüfst das. Ihr seid dran.",
            "Du prüfst das. Ihr könnt loslegen.",
            "Du prüfst das. Ihr wollt mehr.",
        ):
            with self.subTest(text=text):
                self.assertNotIn("mixed_address", kinds(register_lint.lint(text, precise=True)))

    def test_precise_keeps_sentence_initial_possessive_ihr(self):
        text = "Du prüfst das. Ihr Passwort ist abgelaufen."
        report = register_lint.lint(text, precise=True)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_keeps_plural_anaphora_as_conservative_gap(self):
        text = "Die Teams arbeiteten getrennt. Sie trafen sich nur freitags. Und du merkst das."
        report = register_lint.lint(text, precise=True)

        self.assertIn("mixed_address", kinds(report))

    def test_precise_ignores_inline_quoted_foreign_voice(self):
        texts = (
            "Du dokumentierst den Hinweis „Bitte prüfen Sie Ihre Angaben“ und gehst weiter.",
            'Du dokumentierst den Hinweis "Bitte prüfen Sie Ihre Angaben" und gehst weiter.',
            "Sie dokumentieren den Hinweis «Du musst das prüfen» und fahren fort.",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertNotIn("mixed_address", kinds(register_lint.lint(text, precise=True)))

    def test_precise_keeps_real_address_outside_inline_quotes(self):
        texts = (
            "Du prüfst den Text. Bitte senden Sie danach die Freigabe.",
            "Du prüfst den „finalen“ Text. Bitte senden Sie danach die Freigabe.",
            "Du kennst den Hinweis „Bitte prüfen Sie“. Senden Sie danach die Freigabe.",
            "Du kennst den Hinweis „Bitte prüfen Sie”.",
        )

        for text in texts:
            with self.subTest(text=text):
                self.assertIn("mixed_address", kinds(register_lint.lint(text, precise=True)))

    def test_precise_ignores_sie_address_in_blockquote(self):
        text = "Du prüfst die Daten.\n\n> Bitte prüfen Sie Ihre Angaben.\n\nDann passt es."
        report = register_lint.lint(text, precise=True)
        _, nlp = register_lint.precise_context(True)

        self.assertNotIn("mixed_address", kinds(report))
        self.assertEqual(report["features"], register_lint.features(text, nlp=nlp))


if __name__ == "__main__":
    unittest.main()
