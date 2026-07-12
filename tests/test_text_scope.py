import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import register_lint
import rhythm_lint
import style_profile
import text_scope


class TextScopeTests(unittest.TestCase):
    def test_masking_preserves_offsets_and_has_explicit_quote_scope(self):
        text = (
            "---\ntitle: Du bist ja gemeint.\n---\n"
            "| du | ja |\n|---|---|\n"
            "> Sie prüfen das.\n"
            "Eigene Prosa bleibt."
        )

        document = text_scope.mask_text(text, scope=text_scope.DOCUMENT_PROSE)
        authored = text_scope.mask_text(text, scope=text_scope.AUTHORED_PROSE)

        self.assertEqual(len(document), len(text))
        self.assertEqual([i for i, char in enumerate(document) if char == "\n"], [i for i, char in enumerate(text) if char == "\n"])
        self.assertNotIn("title", document)
        self.assertNotIn("| du |", document)
        self.assertIn("Sie prüfen", document)
        self.assertNotIn("Sie prüfen", authored)
        self.assertIn("Eigene Prosa bleibt", authored)

    def test_frontmatter_does_not_change_prose_metrics(self):
        base = " ".join(
            [
                "Das System prüft heute alle Dateien.",
                "Das System liest danach die Berichte.",
                "Das System sortiert später die Anfragen.",
                "Das System sendet abends die Antworten.",
                "Das System speichert nachts die Einträge.",
                "Das System zählt morgens die Punkte.",
                "Das System meldet mittags die Ergebnisse.",
            ]
        )
        with_frontmatter = "---\ntitle: Das System erfindet einen achten Satz.\nauthor: Du\n---\n\n" + base

        base_report = rhythm_lint.analyze(base)
        scoped_report = rhythm_lint.analyze(with_frontmatter)
        base_profile = style_profile.profile(base, "base")
        scoped_profile = style_profile.profile(with_frontmatter, "scoped")

        self.assertEqual(scoped_report["document"], base_report["document"])
        self.assertEqual(scoped_profile["meta"]["word_count"], base_profile["meta"]["word_count"])
        self.assertEqual(scoped_profile["metrics"], base_profile["metrics"])

    def test_table_content_does_not_change_register_or_style_metrics(self):
        base = "Ein kurzer Satz bleibt. Danach folgt eine sachliche Erklärung."
        with_table = base + "\n\n| Ansprache | Partikel |\n|---|---|\n| du | ja |\n| Sie | doch |"

        self.assertEqual(register_lint.features(with_table), register_lint.features(base))
        self.assertEqual(style_profile.profile(with_table, "table")["metrics"], style_profile.profile(base, "base")["metrics"])
        self.assertEqual(
            style_profile.profile(with_table, "table")["meta"]["word_count"],
            style_profile.profile(base, "base")["meta"]["word_count"],
        )

    def test_typographic_scope_keeps_html_text_but_masks_tag_syntax(self):
        text = '<p class="intro">Er sagte "Hallo".</p>'

        document = text_scope.mask_text(text, scope=text_scope.DOCUMENT_PROSE)
        typography = text_scope.mask_text(text, scope=text_scope.TYPOGRAPHIC_PROSE)

        self.assertNotIn("Er sagte", document)
        self.assertIn('Er sagte "Hallo".', typography)
        self.assertNotIn('class="intro"', typography)

    def test_fenced_code_closes_only_with_its_opening_delimiter(self):
        base = "Sachliche Prosa bleibt bestehen."
        cases = (
            base + "\n\n```text\nDu bist ja gemeint.\n~~~\nSie prüfen doch alles.\n```\n",
            base + "\n\n~~~text\nDu bist ja gemeint.\n```\nSie prüfen doch alles.\n~~~\n",
        )

        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(register_lint.features(text), register_lint.features(base))
                self.assertEqual(rhythm_lint.analyze(text)["document"], rhythm_lint.analyze(base)["document"])
                self.assertEqual(
                    style_profile.profile(text, "fenced")["metrics"],
                    style_profile.profile(base, "base")["metrics"],
                )

    def test_fenced_code_accepts_longer_closer_and_masks_unclosed_block(self):
        closed = "Vorher.\n\n```text\nDu bist ja gemeint.\n````\n\nNachher."
        unclosed = "Vorher.\n\n~~~text\nDu bist ja gemeint."

        self.assertIn("Nachher.", text_scope.mask_text(closed))
        self.assertNotIn("Du bist", text_scope.mask_text(closed))
        self.assertNotIn("Du bist", text_scope.mask_text(unclosed))

    def test_authored_scope_excludes_every_blockquote_feature(self):
        quoted = "> Du prüfst ja unsere Datei. Senden Sie uns Ihre Fassung? 👩‍💻\n"
        text = "Sachliche eigene Prosa.\n\n" + quoted

        conservative = register_lint.features(text)
        authored = register_lint.features(text, nlp=lambda _: [])

        self.assertGreater(conservative["du_count"], 0)
        for name in (
            "du_count",
            "sie_formal_count",
            "wir_count",
            "modal_particle_count",
            "emoji_count",
            "rhetorical_questions",
        ):
            self.assertEqual(authored[name], 0, name)
        self.assertEqual(rhythm_lint.analyze(text)["document"]["sentence_count"], 1)
        self.assertEqual(style_profile.profile(text, "quoted")["metrics"], style_profile.profile("Sachliche eigene Prosa.", "base")["metrics"])

    def test_all_wir_inflections_are_counted(self):
        text = "Wir helfen uns mit unser, unsere, unseren, unserem, unserer und unseres."

        self.assertEqual(register_lint.features(text)["wir_count"], 8)
        self.assertIn("unexpected_direct_address", {item["kind"] for item in register_lint.lint(text, expected_address="neutral")["findings"]})

    def test_sentence_split_keeps_closing_quote_with_previous_sentence(self):
        text = "Er sagte: „Hallo.“ Danach ging er weiter."

        self.assertEqual(rhythm_lint.split_sentences(text), ["Er sagte: „Hallo.“", "Danach ging er weiter."])

    def test_list_items_do_not_create_uniform_paragraphs(self):
        text = "- Erster Punkt.\n- Zweiter Punkt.\n- Dritter Punkt.\n- Vierter Punkt."
        document = rhythm_lint.analyze(text)["document"]

        self.assertEqual(document["sentence_count"], 4)
        self.assertEqual(document["paragraph_sentence_counts"], [])
        self.assertFalse(document["paragraph_sentence_counts_uniform"])

    def test_heading_words_are_not_part_of_style_profile(self):
        base = "Ein Hund läuft schnell."
        with_heading = "# Herausforderungen für uns, ja\n\n" + base

        base_profile = style_profile.profile(base, "base")
        heading_profile = style_profile.profile(with_heading, "heading")

        self.assertEqual(heading_profile["meta"]["word_count"], base_profile["meta"]["word_count"])
        self.assertEqual(heading_profile["metrics"], base_profile["metrics"])


if __name__ == "__main__":
    unittest.main()
