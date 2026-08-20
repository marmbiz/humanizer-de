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
    def test_word_regex_keeps_unicode_words_and_existing_joiner_semantics(self):
        text = "Résumé Émile Première Café Erdoğan Škoda Ørsted Nord-Süd-Achse gibt's"

        self.assertEqual(
            german_pattern_lint.WORD_RE.findall(text),
            ["Résumé", "Émile", "Première", "Café", "Erdoğan", "Škoda", "Ørsted", "Nord-Süd", "Achse", "gibt's"],
        )

    def test_ai_marker_cluster(self):
        text = "Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft."
        self.assertIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ai_marker_cluster_ignores_blockquote(self):
        text = "> Der Text beleuchtet das vielschichtige Zusammenspiel in einer dynamischen Landschaft.\n"
        self.assertNotIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_single_marker_is_not_cluster(self):
        text = "Die robuste Statistik nutzt ein dynamisches Routing."
        self.assertNotIn("ai_marker_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ai_marker_mentions_in_quotes_are_not_cluster(self):
        text = (
            "Im Review ging es um Wörter wie „Nahtlos“, „beleuchten“ und "
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

    def test_ad_boilerplate_social_proof_variants(self):
        variants = (
            "Über 3.400 Handwerksbetriebe in Deutschland vertrauen bereits.",
            "3.400 Handwerksbetriebe können nicht irren.",
            "Schließen Sie sich ihnen an.",
            "Mehr als 3.400 zufriedene Kunden.",
        )
        for variant in variants:
            with self.subTest(variant=variant):
                text = f"{variant} Registrieren Sie sich jetzt."
                finding = next(
                    item
                    for item in german_pattern_lint.lint(text)["findings"]
                    if item["kind"] == "ad_boilerplate_cluster"
                )
                self.assertIn(variant.rstrip("."), finding["evidence"]["social_proof"])

    def test_ad_boilerplate_section_variants(self):
        variants = (
            "Das sagen unsere Kunden",
            "Was unsere Kunden sagen",
            "Kundenstimmen",
            "Stimmen unserer Kunden",
            "Das sagen Kunden über uns",
            "Überzeugen Sie sich selbst",
            "Warum RechnungsHeld die richtige Wahl für Ihren Betrieb ist",
            "Ihre Vorteile auf einen Blick",
        )
        for variant in variants:
            with self.subTest(variant=variant):
                text = f"# {variant}\n## Ihre Vorteile auf einen Blick\n"
                self.assertIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ad_boilerplate_cta_variants(self):
        variants = (
            "Registrieren Sie sich noch heute",
            "Registrieren Sie sich jetzt",
            "Jetzt testen",
            "Jetzt kostenlos testen",
            "Starten Sie jetzt",
            "Starten Sie heute",
            "Sichern Sie sich Ihren Zugang",
            "Testen Sie RechnungsHeld 30 Tage kostenlos",
        )
        for variant in variants:
            with self.subTest(variant=variant):
                text = f"3.400 zufriedene Kunden. {variant}."
                finding = next(
                    item
                    for item in german_pattern_lint.lint(text)["findings"]
                    if item["kind"] == "ad_boilerplate_cluster"
                )
                self.assertTrue(
                    any(variant.startswith(match) for match in finding["evidence"]["cta_stack"])
                )

    def test_ad_boilerplate_single_class_once_is_not_cluster(self):
        text = (
            "Einleitung.\n"
            "Das sagen unsere Kunden\n"
            "Der Bericht folgt.\n"
            "Registrieren Sie sich jetzt."
        )
        self.assertNotIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ad_boilerplate_ignores_factual_text(self):
        text = (
            "Im Jahr 2024 wurden 3.400 Kunden befragt. "
            "Der Bericht dokumentiert Methode, Stichprobe und Ergebnisse."
        )
        self.assertNotIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ad_boilerplate_ignores_survey_percentages(self):
        text = (
            "Laut der Studie vertrauen der Regierung nur wenige.\n"
            "12 Prozent der Befragten vertrauen den Parteien.\n"
            "38 Prozent der Befragten vertrauen den Gerichten.\n"
            "Die Erhebung lief von Januar bis Maerz 2021."
        )
        self.assertNotIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ad_boilerplate_ignores_legal_join_commands(self):
        text = (
            "Betroffene koennen sich dem Verfahren anschliessen.\n"
            "Schliessen Sie sich dem Musterverfahren an, wenn Sie einen Bescheid erhalten haben.\n"
            "Schliessen Sie sich der Sammelklage an. Die Frist endet am 30. Juni."
        )
        self.assertNotIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ad_boilerplate_ignores_technical_documentation_ctas(self):
        text = (
            "Das Paket benoetigt Python 3.11. Jetzt testen: pip install beispiel.\n"
            "Starten Sie jetzt den Entwicklungsserver. Die Konfiguration liegt in config.toml."
        )
        self.assertNotIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_ad_boilerplate_requires_anchor_class(self):
        self.assertIn(
            "ad_boilerplate_cluster",
            kinds(german_pattern_lint.lint("3.400 zufriedene Kunden. Jetzt testen.")),
        )
        self.assertNotIn(
            "ad_boilerplate_cluster",
            kinds(german_pattern_lint.lint("Jetzt testen. Starten Sie jetzt.")),
        )

    def test_ad_boilerplate_finds_standalone_title_line(self):
        text = (
            "Einleitung.\n\n"
            "Das sagen Kunden über uns\n\n"
            "3.400 zufriedene Kunden."
        )
        report = german_pattern_lint.lint(text)
        finding = next(
            item for item in report["findings"] if item["kind"] == "ad_boilerplate_cluster"
        )

        self.assertEqual(finding["severity"], "warning")
        self.assertIn("Das sagen Kunden über uns", finding["evidence"]["ad_section"])
        self.assertEqual(
            {text[span["start"]:span["end"]] for span in finding["spans"]},
            {
                "Das sagen Kunden über uns",
                "3.400 zufriedene Kunden",
            },
        )

    def test_ad_boilerplate_ignores_foreign_prose(self):
        text = (
            "---\n"
            "social: 3.400 zufriedene Kunden\n"
            "cta: Registrieren Sie sich jetzt\n"
            "---\n"
            "Im Entwurf stehen „3.400 zufriedene Kunden“ und "
            "„Schließen Sie sich ihnen an“.\n"
            "> Registrieren Sie sich jetzt.\n"
            "> Sichern Sie sich Ihren Zugang.\n"
            "```text\n"
            "Registrieren Sie sich jetzt. Sichern Sie sich Ihren Zugang.\n"
            "```\n"
        )
        self.assertNotIn("ad_boilerplate_cluster", kinds(german_pattern_lint.lint(text)))

    def test_copula_avoidance_cluster(self):
        text = "Die Plattform fungiert als Werkzeug und verfügt über mehrere Module."
        self.assertIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_multiword_marker_counts_line_break(self):
        self.assertEqual(german_pattern_lint.count_marker("fungiert\nals", "fungiert als"), 1)

    def test_multiword_marker_counts_non_breaking_space(self):
        self.assertEqual(german_pattern_lint.count_marker("fungiert\u00a0als", "fungiert als"), 1)

    def test_multiword_marker_counts_repeated_spaces(self):
        self.assertEqual(german_pattern_lint.count_marker("fungiert  als", "fungiert als"), 1)

    def test_multiword_marker_span_references_original_text(self):
        text = "fungiert\u00a0als"
        spans = german_pattern_lint.marker_spans(text, "fungiert als")

        self.assertEqual([text[start:end] for start, end in spans], [text])

    def test_copula_avoidance_cluster_ignores_blockquote(self):
        text = "> Die Plattform fungiert als Werkzeug und verfügt über mehrere Module.\n"
        self.assertNotIn("copula_avoidance_cluster", kinds(german_pattern_lint.lint(text)))

    def test_abstraction_cluster_counts_singular_aspekt_and_prozess(self):
        text = "Ein Aspekt prägt den Prozess. Ein weiterer Aspekt verändert den Prozess. Der Prozess endet."
        self.assertIn("abstraction_cluster", kinds(german_pattern_lint.lint(text)))

    def test_abstraction_cluster_ignores_blockquote(self):
        text = "> Ein Aspekt prägt den Prozess. Ein weiterer Aspekt verändert den Prozess. Der Prozess endet.\n"
        self.assertNotIn("abstraction_cluster", kinds(german_pattern_lint.lint(text)))

    def test_abstraction_cluster_counts_plural_aspekte_and_prozesse(self):
        text = "Mehrere Aspekte prägen die Prozesse. Weitere Aspekte verändern diese Prozesse. Die Prozesse enden."
        self.assertIn("abstraction_cluster", kinds(german_pattern_lint.lint(text)))

    def test_abstraction_cluster_ignores_prozessor_and_prozessual(self):
        text = "Der Prozessor ersetzt zwei Prozessoren. Prozessual bleiben prozessuale und prozessualen Fragen offen."
        self.assertNotIn("abstraction_cluster", kinds(german_pattern_lint.lint(text)))

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

    def test_negation_parallelism(self):
        text = "Kein Server, keine Datenbank. Kein Dashboard nötig."
        report = german_pattern_lint.lint(text)
        self.assertIn("negation_parallelism", kinds(report))
        self.assertNotIn("negation_antithesis_cluster", kinds(report))

    def test_negation_parallelism_between_bold_lead_ins(self):
        text = "**Setup:** Kein Server, keine Datenbank. **Fazit:** einfach."
        self.assertIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_italic_use_mention(self):
        text = "Im Beispiel steht: *Kein Server, keine Datenbank.*"
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_factual_correction(self):
        text = "Ich will nicht Tee, sondern Kaffee."
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_single_negation(self):
        text = "Keine Sorge, das passt schon."
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_quoted_example(self):
        text = "Im Beispiel steht: „Kein Server, keine Datenbank.“"
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_keeps_inline_quoted_term(self):
        text = "Kein Server, keine „Datenbank im Keller“ mehr."
        self.assertIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_ignores_figure_starting_in_quoted_material(self):
        text = "Im Text steht: „Kein Server“, keine Datenbank."
        self.assertNotIn("negation_parallelism", kinds(german_pattern_lint.lint(text)))

    def test_negation_parallelism_three_part_span_round_trips_with_inline_quote(self):
        text = "Kein Auto-Rewrite, kein künstlicher Konnektor-„Fix“, kein nummeriertes Muster."
        report = german_pattern_lint.lint(text)
        finding = next(item for item in report["findings"] if item["kind"] == "negation_parallelism")

        self.assertEqual(
            [text[span["start"]:span["end"]] for span in finding["spans"]],
            finding["evidence"],
        )

    def test_negation_antithesis_cluster(self):
        text = (
            "Nicht abwarten, sondern machen. Nicht erklären, sondern liefern. "
            "Nicht verwalten, sondern gestalten. Laut und nicht leise lautet die Devise."
        )
        self.assertIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_for_repeated_not_but(self):
        text = (
            "Nicht reden, sondern handeln. Nicht planen, sondern anfangen. "
            "Nicht prüfen, sondern glauben. Nicht zweifeln, sondern folgen."
        )
        self.assertIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_for_repeated_and_not(self):
        text = (
            "Die Ansage ist laut und nicht leise. Der Plan bleibt starr und nicht beweglich. "
            "Die Antwort wirkt glatt und nicht ehrlich. Der Ton ist scharf und nicht sachlich."
        )
        self.assertIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_keeps_rhetorical_and_not_matches(self):
        text = (
            "Die Richtung bleibt vorwärts und nicht rückwärts. "
            "Die Antwort wirkt ehrlich und nicht taktisch. "
            "Der Ton ist mutig und nicht zaghaft. Die Lösung bleibt offen und nicht starr."
        )
        report = german_pattern_lint.lint(text)
        finding = next(item for item in report["findings"] if item["kind"] == "negation_antithesis_cluster")
        self.assertEqual(
            finding["evidence"]["matches"],
            [
                "vorwärts und nicht rückwärts",
                "ehrlich und nicht taktisch",
                "mutig und nicht zaghaft",
                "offen und nicht starr",
            ],
        )

    def test_negation_antithesis_cluster_ignores_single_substantive_contrast(self):
        text = "Die Auswertung bewertet nicht die Person, sondern das Verfahren."
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_factual_corrections(self):
        text = (
            "Der Termin ist nicht Montag, sondern Dienstag. "
            "Die Abgabe ist nicht Mittwoch, sondern Donnerstag. "
            "Das Treffen ist nicht Freitag, sondern Samstag. "
            "Der Prüfmonat ist nicht Januar, sondern Februar."
        )
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_and_not_weekday_corrections(self):
        text = (
            "Der Termin ist Montag und nicht Dienstag. "
            "Die Abgabe ist Mittwoch und nicht Donnerstag. "
            "Das Treffen ist Freitag und nicht Samstag. "
            "Der Monat ist Januar und nicht Februar."
        )
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_unit_and_month_year_corrections(self):
        for text in (
            "Nicht 10 Prozent, sondern 12 Prozent. " * 4,
            "Nicht 10 Euro, sondern 12 Euro. " * 4,
            "Nicht 10 Minuten, sondern 12 Minuten. " * 4,
            "Nicht 10 Kilogramm, sondern 12 Kilogramm. " * 4,
            "Nicht 10 Meter, sondern 12 Meter. " * 4,
            "Nicht 10 Gigabyte, sondern 12 Gigabyte. " * 4,
            "Nicht Juli 2025, sondern August 2025. " * 4,
        ):
            with self.subTest(text=text):
                self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_and_not_unit_month_and_number_corrections(self):
        for text in (
            "Wir liefern 10 Prozent und nicht 12 Prozent. " * 4,
            "Wir berechnen 10 Euro und nicht 12 Euro. " * 4,
            "Wir planen 10 Minuten und nicht 12 Minuten. " * 4,
            "Wir wiegen 10 Kilogramm und nicht 12 Kilogramm. " * 4,
            "Wir messen 10 Meter und nicht 12 Meter. " * 4,
            "Wir speichern 10 Gigabyte und nicht 12 Gigabyte. " * 4,
            "Wir planen Juli 2025 und nicht August 2025. " * 4,
            "Der Wert ist 10 und nicht 12. " * 4,
        ):
            with self.subTest(text=text):
                self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_for_trailing_contrast_tails(self):
        text = (
            "Der Test prüft das Produkt, nicht den Nutzer. "
            "Unser Support spricht Handwerk, nicht Amtsdeutsch. "
            "Das Modell optimiert auf Plausibilität, nicht auf Wahrheit. "
            "Im Zentrum steht die Antwort, nicht der Verweis."
        )
        self.assertIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_for_mixed_trailing_and_classic_forms(self):
        text = (
            "Der Test prüft das Produkt, nicht den Nutzer. "
            "Im Zentrum steht die Antwort, nicht der Verweis. "
            "Nicht abwarten, sondern machen. Laut und nicht leise lautet die Devise."
        )
        self.assertIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_trailing_value_corrections(self):
        for text in (
            "Die Lieferung kommt am Dienstag, nicht am Mittwoch. " * 4,
            "Der Termin liegt im August, nicht im September. " * 4,
            "Die Messung ergab 12 Prozent, nicht 10 Prozent. " * 4,
            "Der Vertrag gilt ab Mai, nicht ab Juni. " * 4,
            "Der Stichtag ist morgen, nicht heute. " * 4,
        ):
            with self.subTest(text=text):
                self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_trailing_correlatives(self):
        text = "Es geht um Qualität, nicht nur um Tempo. " * 4
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_trailing_tail_requires_sentence_end(self):
        text = "Es zählt Qualität, nicht Tempo\n" * 4
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_trailing_tail_ignores_non_sentence_periods(self):
        for text in (
            "Wir prüfen Inhalte, nicht z. B. Formate der Konkurrenz. " * 4,
            "Der Kurs kostet 1.200 Euro, nicht mehr als 2.400 Euro im Jahr. " * 4,
            "Er schrieb an die Redaktion, nicht an mm.biz oder andere. " * 4,
            "Der Termin ist am 5. Mai, nicht am 3. Mai wie geplant. " * 4,
        ):
            with self.subTest(text=text):
                self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_trailing_tail_overlapping_classic_form_counts_once(self):
        text = "Nicht Absicht, sondern Gewohnheit, nicht Bosheit. " * 2
        candidates = sorted(
            match.span()
            for pattern in german_pattern_lint.ANTITHESIS_RES
            for match in pattern.finditer(text)
        )
        self.assertTrue(
            any(right[0] < left[1] for left, right in zip(candidates, candidates[1:]))
        )
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_low_document_density(self):
        text = "Wort " * 1400 + (
            "Nicht abwarten, sondern machen. Nicht erklären, sondern liefern. "
            "Nicht verwalten, sondern gestalten. Laut und nicht leise lautet die Devise."
        )
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_density_ignores_foreign_voice_words(self):
        authored = (
            "Nicht abwarten, sondern machen. Nicht erklären, sondern liefern. "
            "Nicht verwalten, sondern gestalten. Laut und nicht leise lautet die Devise."
        )
        baseline = next(
            item
            for item in german_pattern_lint.lint(authored)["findings"]
            if item["kind"] == "negation_antithesis_cluster"
        )
        with_quote = authored + "\n\n> " + "Fremdwort " * 1400
        finding = next(
            item
            for item in german_pattern_lint.lint(with_quote)["findings"]
            if item["kind"] == "negation_antithesis_cluster"
        )
        self.assertEqual(finding["evidence"], baseline["evidence"])

    def test_negation_antithesis_cluster_ignores_use_mentions(self):
        text = (
            "Im Leitfaden stehen „nicht abwarten, sondern machen“ und "
            "`nicht erklären, sondern liefern`. Die Varianten "
            "*nicht verwalten, sondern gestalten* und "
            "_laut und nicht leise_ werden nur zitiert."
        )
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_shared_quote_pairs(self):
        for opener, closer in (("«", "»"), ("“", "”")):
            text = " ".join(
                f"Im Beispiel steht {opener}{example}{closer}."
                for example in (
                    "nicht abwarten, sondern machen",
                    "nicht erklären, sondern liefern",
                    "nicht verwalten, sondern gestalten",
                    "laut und nicht leise",
                )
            )
            with self.subTest(opener=opener):
                self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_ignores_partially_protected_arms(self):
        for text in (
            "Nicht `abwarten`, sondern machen. " * 4,
            "Nicht «abwarten», sondern machen. " * 4,
            "Nicht https://example.com, sondern lokal. " * 4,
            "Nicht <code>remote</code>, sondern lokal. " * 4,
        ):
            with self.subTest(text=text):
                self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_cluster_counts_overlapping_forms_once(self):
        text = "Nicht laut und nicht leise, sondern klar. " * 2
        self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_negation_antithesis_overlapping_candidate_spans_round_trip(self):
        text = "Nicht laut und nicht leise, sondern klar. " * 4
        candidates = sorted(
            match.span()
            for pattern in german_pattern_lint.ANTITHESIS_RES
            for match in pattern.finditer(text)
        )
        self.assertTrue(
            any(right[0] < left[1] for left, right in zip(candidates, candidates[1:]))
        )

        report = german_pattern_lint.lint(text)
        finding = next(item for item in report["findings"] if item["kind"] == "negation_antithesis_cluster")

        self.assertEqual(finding["evidence"]["count"], 4)
        self.assertEqual(
            [text[span["start"]:span["end"]] for span in finding["spans"]],
            finding["evidence"]["matches"],
        )

    def test_negation_antithesis_rejected_overlap_does_not_extend_coverage(self):
        text = "Klar und nicht laut, sondern nicht leise und nicht schrill. " * 4
        report = german_pattern_lint.lint(text)
        finding = next(item for item in report["findings"] if item["kind"] == "negation_antithesis_cluster")

        self.assertEqual(finding["evidence"]["count"], 8)

    def test_negation_antithesis_cluster_ignores_correlatives(self):
        for adverb in ("nur", "allein", "bloß", "bloss", "ausschließlich", "ausschliesslich"):
            for form, text in (
                (
                    "sondern_auch",
                    f"Nicht {adverb} Tempo, sondern auch Sorgfalt zählt. "
                    f"Nicht {adverb} Technik, sondern auch Abstimmung hilft. "
                    f"Nicht {adverb} Kosten, sondern auch Nutzen werden geprüft. "
                    f"Nicht {adverb} heute, sondern auch morgen bleibt Zeit.",
                ),
                (
                    "sondern_without_auch",
                    f"Nicht {adverb} abwarten, sondern machen. " * 4,
                ),
                (
                    "und_nicht",
                    f"Tempo und nicht {adverb} Sorgfalt zählt. "
                    f"Technik und nicht {adverb} Abstimmung hilft. "
                    f"Kosten und nicht {adverb} Nutzen werden geprüft. "
                    f"Heute und nicht {adverb} morgen bleibt Zeit.",
                ),
            ):
                with self.subTest(adverb=adverb, form=form):
                    self.assertNotIn("negation_antithesis_cluster", kinds(german_pattern_lint.lint(text)))

    def test_dash_cluster_for_all_sentence_punctuation_variants(self):
        clauses = (
            "Die Oberfläche wirkt klar{dash}jedes Element sitzt an seinem Platz.",
            "Der Ablauf bleibt einfach{dash}niemand muss lange suchen.",
            "Die Hilfe erscheint sofort{dash}genau dann, wenn sie gebraucht wird.",
            "Das Ergebnis überzeugt{dash}ohne unnötige Reibung.",
            "So wird jeder Schritt leichter{dash}von Anfang bis Ende.",
        )
        for dash in (" — ", " – ", " -- ", " - "):
            with self.subTest(dash=dash):
                text = " ".join(clause.format(dash=dash) for clause in clauses)
                finding = next(
                    item
                    for item in german_pattern_lint.lint(text)["findings"]
                    if item["kind"] == "dash_cluster"
                )

                self.assertEqual(finding["pattern"], 16)
                self.assertEqual(finding["severity"], "warning")
                self.assertEqual(finding["evidence"]["count"], 5)
                self.assertEqual(
                    [text[span["start"]:span["end"]] for span in finding["spans"]],
                    finding["evidence"]["matches"],
                )

    def test_dash_cluster_for_dashes_distributed_across_paragraphs(self):
        paragraph = "Der Plan — gut durchdacht — steht. Die Umsetzung — sofort — beginnt."
        text = "\n\n".join([paragraph] * 6)

        findings = [
            item
            for item in german_pattern_lint.lint(text)["findings"]
            if item["kind"] == "dash_cluster"
        ]

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["evidence"]["count"], 24)
        self.assertEqual(
            [text[span["start"]:span["end"]] for span in findings[0]["spans"]],
            ["—"] * 24,
        )

    def test_dash_cluster_ignores_headings_word_hyphens_and_number_ranges(self):
        text = (
            "# Eins – Überblick\n## Zwei — Details\n### Drei - Praxis\n"
            "KI-Tell, 2D-Spiegelung und E-Mail. "
            "Die Zeiträume 2019–2021, S. 12–15, 10–20 % und 10 – 20 bleiben Bereiche."
        )
        self.assertNotIn("dash_cluster", kinds(german_pattern_lint.lint(text)))

    def test_dash_cluster_ignores_foreign_prose(self):
        text = (
            "Im Entwurf steht: „Klar — direkt — einfach — sicher — überzeugend.“\n"
            "> Klar — direkt — einfach — sicher — überzeugend.\n"
            "`Klar — direkt — einfach — sicher — überzeugend.`\n"
            "*Klar — direkt — einfach — sicher — überzeugend.*"
        )
        self.assertNotIn("dash_cluster", kinds(german_pattern_lint.lint(text)))

    def test_dash_cluster_requires_count_and_paragraph_density(self):
        paired_insertions = (
            "Dass es offenbar keinem – nicht einmal den Designern – aufzufallen scheint. "
            "Gesucht wird ein Objekt – zum Beispiel von einem Foto – zum Spiegeln."
        )
        low_density = "Wort " * 400 + "A — B. C — D. E — F. G — H. I — J."
        for text in (paired_insertions, low_density):
            with self.subTest(text=text[-80:]):
                self.assertNotIn("dash_cluster", kinds(german_pattern_lint.lint(text)))

    def test_dash_cluster_does_not_duplicate_m8_dash_antithesis(self):
        text = "Nicht reden – sondern handeln. " * 5
        report = german_pattern_lint.lint(text)

        self.assertIn("negation_antithesis_cluster", kinds(report))
        self.assertNotIn("dash_cluster", kinds(report))

    def test_mention_detectors_ignore_blockquotes(self):
        text = (
            "> Kein Server, keine Datenbank.\n"
            "> Nicht reden, sondern handeln.\n"
            "> Nicht planen, sondern anfangen.\n"
            "> Nicht prüfen, sondern glauben.\n"
            "> Nicht zweifeln, sondern folgen.\n"
            "> Du bist nicht zu sensibel.\n"
        )

        self.assertTrue(
            {
                "negation_parallelism",
                "negation_antithesis_cluster",
                "address_validation_candidate",
            }.isdisjoint(kinds(german_pattern_lint.lint(text)))
        )

    def test_bold_overdose(self):
        text = "**Alpha:** eins. **Beta:** zwei. **Gamma:** drei. **Delta:** vier. **Epsilon:** fünf."
        self.assertIn("bold_overdose", kinds(german_pattern_lint.lint(text)))

    def test_bold_overdose_ignores_blockquote_voice(self):
        text = "\n".join(f"> **{word}**" for word in ("Alpha", "Beta", "Gamma", "Delta", "Epsilon"))
        self.assertNotIn("bold_overdose", kinds(german_pattern_lint.lint(text)))

    def test_bold_overdose_counts_six_long_spans(self):
        text = "\n".join(f"**{letter * 81}**" for letter in "abcdef")
        self.assertIn("bold_overdose", kinds(german_pattern_lint.lint(text)))

    def test_bold_overdose_does_not_count_cross_span_phantoms(self):
        spans = ["kurz", "A" * 81, "knapp", "B" * 81, "klein", "C" * 81]
        text = " ".join(f"**{span}**" for span in spans)
        finding = next(
            item
            for item in german_pattern_lint.lint(text)["findings"]
            if item["kind"] == "bold_overdose"
        )
        self.assertEqual(finding["evidence"]["count"], 6)

    def test_bold_overdose_threshold_remains_five_for_long_spans(self):
        text = "\n".join(f"**{letter * 81}**" for letter in "abcd")
        self.assertNotIn("bold_overdose", kinds(german_pattern_lint.lint(text)))

    def test_bold_overdose_ignores_four_spans(self):
        text = "**Alpha:** eins. **Beta:** zwei. **Gamma:** drei. **Delta:** vier."
        self.assertNotIn("bold_overdose", kinds(german_pattern_lint.lint(text)))

    def test_bold_overdose_ignores_single_span(self):
        text = "Dieser Hinweis ist **wichtig** für die Auswertung."
        self.assertNotIn("bold_overdose", kinds(german_pattern_lint.lint(text)))

    def test_colon_heading_spans_keep_splitlines_semantics(self):
        text = "  # Eins: Inhalt  \u2028## Zwei: Inhalt"
        report = german_pattern_lint.lint(text)
        finding = next(item for item in report["findings"] if item["kind"] == "colon_heading_cluster")

        self.assertEqual(
            [text[span["start"]:span["end"]] for span in finding["spans"]],
            ["# Eins: Inhalt", "## Zwei: Inhalt"],
        )

    def test_address_validation_candidate_is_info_advisory(self):
        report = german_pattern_lint.lint("Du bist nicht zu sensibel.")
        finding = next(
            item for item in report["findings"] if item["kind"] == "address_validation_candidate"
        )

        self.assertEqual(finding["pattern"], 72)
        self.assertEqual(finding["severity"], "info")
        self.assertTrue(finding["advisory"])
        self.assertEqual(
            finding["message"],
            "Kandidat für unbelegte Adressaten-Validierung: Kontext prüfen "
            "(Beratungsauftrag? Zitat? Sachklärung?)",
        )

    def test_address_validation_candidate_ignores_quoted_use_mention(self):
        text = 'Der Satz „Du bist nicht zu sensibel“ ist hier nur ein Beispiel.'
        self.assertNotIn("address_validation_candidate", kinds(german_pattern_lint.lint(text)))


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
