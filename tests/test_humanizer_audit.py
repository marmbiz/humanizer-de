import io
import importlib.util
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "humanizer_audit.py"

spec = importlib.util.spec_from_file_location("humanizer_audit", SCRIPT)
humanizer_audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(humanizer_audit)

SPACY_AVAILABLE = (
    importlib.util.find_spec("spacy") is not None
    and importlib.util.find_spec("de_core_news_sm") is not None
)


def run_cli(argv):
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        exit_code = humanizer_audit.main(argv)
    return exit_code, stdout.getvalue()


def run_json(argv):
    exit_code, output = run_cli(argv)
    return exit_code, json.loads(output)


def clear_precise_cache():
    if hasattr(humanizer_audit.syntax_lint, "_HUMANIZER_PRECISE_CACHE"):
        delattr(humanizer_audit.syntax_lint, "_HUMANIZER_PRECISE_CACHE")


class HumanizerAuditTests(unittest.TestCase):
    def test_sibling_linters_share_register_module(self):
        self.assertIs(humanizer_audit.german_pattern_lint.register_lint, humanizer_audit.register_lint)

    def test_file_json_output_shape_and_unicode_collapse(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text('"Text" "Mehr"', encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["file"], str(path))
        self.assertEqual(report["mode"], "sachlich")
        self.assertEqual(report["offset_unit"], "unicode_codepoint")
        self.assertFalse(report["ok"])
        self.assertEqual(set(report["summary"]), {"rhythm", "preflight", "counts"})
        self.assertEqual(set(report["summary"]["counts"]), {"unicode", "rhythm", "german_pattern", "register"})
        self.assertEqual(report["summary"]["counts"]["unicode"], 4)
        for key in humanizer_audit.RHYTHM_KEYS:
            self.assertIn(key, report["summary"]["rhythm"])
        self.assertEqual(report["summary"]["preflight"]["risk"], "insufficient_text")
        self.assertFalse(report["summary"]["preflight"]["combing"]["auto"])
        self.assertIn("degrade text quality", report["summary"]["preflight"]["quality_warning"])

        unicode_findings = [item for item in report["findings"] if item["source"] == "unicode"]
        self.assertEqual(len(unicode_findings), 1)
        self.assertEqual(unicode_findings[0]["kind"], "straight_quote")
        self.assertEqual(unicode_findings[0]["count"], 4)
        self.assertEqual(
            unicode_findings[0]["spans"],
            [{"start": 0, "end": 1}, {"start": 5, "end": 6}, {"start": 7, "end": 8}, {"start": 12, "end": 13}],
        )
        for item in report["findings"]:
            self.assertIn("source", item)
            self.assertIn("pattern", item)
            self.assertIn("severity", item)
            self.assertIn("summary", item)

    def test_ok_flag_is_true_without_active_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "clean.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["ok"])
        self.assertEqual(report["findings"], [])
        self.assertEqual(sum(report["summary"]["counts"].values()), 0)
        self.assertEqual(report["summary"]["preflight"]["risk"], "insufficient_text")

    def test_fix_safe_writes_only_existing_unicode_fixes_before_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_bytes("„Text\"\u200b\r\n".encode("utf-8"))

            exit_code, report = run_json(["--file", str(path), "--fix-safe"])

            self.assertEqual(exit_code, 0)
            self.assertEqual(path.read_bytes(), "„Text“\r\n".encode("utf-8"))
            self.assertEqual(
                report["safe_fix"],
                {
                    "changed": True,
                    "scope": ["hidden_unicode", "unambiguous_german_closing_quotes"],
                },
            )
            self.assertEqual(report["summary"]["counts"]["unicode"], 0)
            self.assertIn("SafeFix: changed=true", humanizer_audit.format_markdown(report))

    @unittest.skipIf(os.name == "nt", "symlink creation is not portable on Windows CI")
    def test_fix_safe_refuses_symlink_without_touching_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target.md"
            link = Path(tmp) / "link.md"
            target.write_text("„Text\"\u200b", encoding="utf-8")
            link.symlink_to(target)
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                exit_code = humanizer_audit.main(["--file", str(link), "--fix-safe"])

            self.assertEqual(exit_code, 2)
            self.assertTrue(link.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "„Text\"\u200b")
            self.assertIn("--fix-safe refuses symlink input", stderr.getvalue())

    def test_address_validation_candidate_is_gate_neutral_advisory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.md"
            path.write_text("Du bist nicht zu sensibel.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path), "--fail-on", "any"])

        finding = next(
            item for item in report["findings"] if item["kind"] == "address_validation_candidate"
        )
        self.assertEqual(exit_code, 0)
        self.assertEqual(finding["pattern"], 72)
        self.assertEqual(finding["severity"], "info")
        self.assertTrue(finding["advisory"])
        self.assertIn("Kandidat für unbelegte Adressaten-Validierung", finding["summary"])
        self.assertFalse(report["ok"])

    def test_without_precise_keeps_default_report_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "clean.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            set(report),
            {"file", "mode", "offset_unit", "ok", "summary", "style_profile", "findings"},
        )
        self.assertEqual(set(report["summary"]), {"rhythm", "preflight", "counts"})
        self.assertEqual(set(report["summary"]["counts"]), {"unicode", "rhythm", "german_pattern", "register"})
        self.assertNotIn("precise", report["summary"])
        self.assertNotIn("syntax", report)

    def test_spans_reference_original_text_after_masked_markdown(self):
        text = (
            "---\ntitle: nahtlos beleuchten dynamisch du Sie\n---\n\n"
            "```text\nnahtlos beleuchten dynamisch du Sie\n```\n\n"
            "> Ein Zitat steht vor dem Befund.\n\n"
            "İ😀 Du prüfst den Text. Bitte senden Sie den Bericht. "
            "Der Text beleuchtet einen dynamischen, vielschichtigen Prozess. "
            'Er nennt ihn "klar".\u200b'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scoped.md"
            path.write_bytes(text.encode("utf-8"))

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        finding = next(item for item in report["findings"] if item.get("kind") == "ai_marker_cluster")
        self.assertEqual(
            [text[span["start"]:span["end"]].lower() for span in finding["spans"]],
            ["beleuchtet", "dynamischen", "vielschichtigen"],
        )
        register_finding = next(item for item in report["findings"] if item.get("kind") == "mixed_address")
        self.assertEqual(
            [text[span["start"]:span["end"]] for span in register_finding["spans"]],
            ["Du", "Sie"],
        )
        straight_quotes = next(item for item in report["findings"] if item.get("kind") == "straight_quote")
        self.assertEqual(
            [text[span["start"]:span["end"]] for span in straight_quotes["spans"]],
            ['"', '"'],
        )
        hidden = next(item for item in report["findings"] if item.get("kind") == "hidden_unicode")
        self.assertEqual(
            [text[span["start"]:span["end"]] for span in hidden["spans"]],
            ["\u200b"],
        )

    def test_unicode_spans_cover_document_boundaries(self):
        text = '"Mitte\u200b'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "boundaries.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        by_kind = {item["kind"]: item for item in report["findings"]}
        self.assertEqual(by_kind["straight_quote"]["spans"], [{"start": 0, "end": 1}])
        self.assertEqual(
            by_kind["hidden_unicode"]["spans"],
            [{"start": len(text) - 1, "end": len(text)}],
        )

    def test_precise_without_spacy_reports_status_and_keeps_findings(self):
        text = "Die Idee war neu. Sie überzeugte sofort. Und du merkst das."
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            clear_precise_cache()
            _, default_report = run_json(["--file", str(path)])
            with mock.patch.object(humanizer_audit.syntax_lint, "load_nlp", return_value=(None, "spacy_missing")):
                clear_precise_cache()
                exit_code, precise_report = run_json(["--file", str(path), "--precise"])
            clear_precise_cache()

        self.assertEqual(exit_code, 0)
        self.assertEqual(precise_report["findings"], default_report["findings"])
        self.assertEqual(precise_report["summary"]["counts"], default_report["summary"]["counts"])
        self.assertEqual(
            precise_report["summary"]["precise"],
            {"requested": True, "active": False, "reason": "spacy_missing"},
        )
        self.assertEqual(
            precise_report["syntax"],
            {"available": False, "reason": "spacy_missing", "metrics": None, "findings": []},
        )

    def test_precise_syntax_findings_are_visible_advisory_and_do_not_change_ok(self):
        syntax_report = {
            "available": True,
            "metrics": {},
            "findings": [
                {
                    "pattern": 39,
                    "kind": "passive_sentence",
                    "severity": "info",
                    "sentence": "Der Bericht wird geprüft.",
                },
                {
                    "kind": "subjectless_fragment",
                    "severity": "info",
                    "sentence": "Nach sorgfältiger Prüfung.",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            clear_precise_cache()
            with mock.patch.object(
                humanizer_audit.syntax_lint,
                "load_nlp",
                return_value=(None, "spacy_missing"),
            ), mock.patch.object(humanizer_audit.syntax_lint, "lint", return_value=syntax_report):
                exit_code, report = run_json(
                    ["--file", str(path), "--precise", "--fail-on", "any"]
                )
            clear_precise_cache()

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["ok"])
        self.assertEqual(sum(report["summary"]["counts"].values()), 0)
        self.assertNotIn("syntax", report["summary"]["counts"])
        self.assertEqual(
            [item for item in report["findings"] if item["source"] == "syntax"],
            [
                {
                    "source": "syntax",
                    "pattern": 39,
                    "kind": "passive_sentence",
                    "severity": "info",
                    "advisory": True,
                    "summary": "Der Bericht wird geprüft.",
                },
                {
                    "source": "syntax",
                    "pattern": 0,
                    "kind": "subjectless_fragment",
                    "severity": "info",
                    "advisory": True,
                    "summary": "Nach sorgfältiger Prüfung.",
                },
            ],
        )

    @unittest.skipUnless(SPACY_AVAILABLE, "spaCy German model not installed")
    def test_precise_with_spacy_reports_active_status_and_syntax(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            clear_precise_cache()
            exit_code, report = run_json(["--file", str(path), "--precise"])
            clear_precise_cache()

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["summary"]["precise"], {"requested": True, "active": True})
        self.assertTrue(report["syntax"]["available"])
        self.assertIn("metrics", report["syntax"])
        self.assertIn("findings", report["syntax"])

    def test_short_text_with_connectors_is_insufficient_text(self):
        text = (
            "Das Team prüft den Entwurf. "
            "Außerdem klärt es die offenen Punkte. "
            "Zudem dokumentiert es die nächsten Schritte."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["summary"]["rhythm"]["connector_density"], 2)
        self.assertEqual(report["summary"]["preflight"]["risk"], "insufficient_text")
        self.assertFalse(report["summary"]["preflight"]["combing"]["auto"])
        self.assertFalse(
            any(
                item["kind"] == "mechanical_connectors"
                for item in report["summary"]["preflight"]["drivers"]
            )
        )

    def test_mechanical_connectors_ignore_two_spread_across_paragraphs(self):
        text = (
            "Das Team prüft heute den Entwurf. Außerdem klärt es offene Fragen. "
            "Die Redaktion notiert jeden Befund. Am Abend endet die Sitzung.\n\n"
            "Die Gruppe beginnt am nächsten Morgen. Zudem ordnet sie die Rückmeldungen. "
            "Ein Kollege prüft alle Verweise. Danach geht die Fassung ins Lektorat."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["summary"]["rhythm"]["connector_density"], 2)
        self.assertFalse(
            any(
                item["kind"] == "mechanical_connectors"
                for item in report["summary"]["preflight"]["drivers"]
            )
        )

    def test_mechanical_connectors_flag_two_in_same_paragraph(self):
        text = (
            "Das Team prüft heute den Entwurf. Außerdem klärt es offene Fragen. "
            "Zudem ordnet es die Rückmeldungen. Die Redaktion notiert jeden Befund. "
            "Am Abend endet die Sitzung. Die Gruppe beginnt am nächsten Morgen. "
            "Ein Kollege prüft alle Verweise. Danach geht die Fassung ins Lektorat."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        driver = next(
            item
            for item in report["summary"]["preflight"]["drivers"]
            if item["kind"] == "mechanical_connectors"
        )
        self.assertEqual(driver["detail"], "max_connector_density_per_paragraph=2")
        self.assertEqual(driver["weight"], 1)

    def test_negation_antithesis_cluster_contributes_to_preflight(self):
        text = (
            "Nicht abwarten, sondern machen. Der Plan ist mutig und nicht vorsichtig. "
            "Wir sollten nicht erklären, sondern liefern. Die Antwort bleibt klar und nicht beliebig. "
            "Kurz danach beginnt die Prüfung. Eine ausführliche Diskussion mit allen Beteiligten "
            "klärt anschließend die offenen fachlichen Fragen. Am Ende steht ein Befund. "
            "Nach der Freigabe liest jemand sämtliche Verweise noch einmal sorgfältig. "
            "Später endet die Arbeit."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        preflight = report["summary"]["preflight"]
        driver = next(item for item in preflight["drivers"] if item["kind"] == "negation_antithesis_cluster")
        self.assertEqual(driver["weight"], 2)
        self.assertIn(preflight["risk"], {"medium", "high"})

    def test_ad_boilerplate_cluster_contributes_two_to_preflight(self):
        rhythm_report = {
            "document": {
                "sentence_count": 8,
                "stddev_mean_ratio": 0.6,
                "subject_initial_ratio": 0.5,
                "repeated_openers": [],
                "connector_density_by_paragraph": [0],
                "sentence_length_buckets": {
                    "ratios": {"short_lt_12": 0.15, "long_gt_28": 0.1}
                },
                "paragraph_sentence_counts_uniform": False,
            }
        }
        before = humanizer_audit.preflight_assessment(rhythm_report, [], [], "sachlich")
        after = humanizer_audit.preflight_assessment(
            rhythm_report,
            [{"kind": "ad_boilerplate_cluster", "evidence": {"ad_section": ["Kundenstimmen"]}}],
            [],
            "sachlich",
        )

        self.assertEqual(after["score"], before["score"] + 2)
        self.assertIn(after["risk"], {"medium", "high"})

    def test_low_preflight_includes_calibration_note_and_markdown_line(self):
        expected = (
            "risk=low means no calibrated signal fired, not that the text is clean. "
            "Signal coverage is weakest for advertising, social-media and essay/thought-leadership "
            "registers, where AI patterns can pass unseen."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das Team prüft den Entwurf.", encoding="utf-8")

            _, report = run_json(["--file", str(path)])

        report["summary"]["preflight"] = humanizer_audit.preflight_assessment(
            {
                "document": {
                    "sentence_count": 8,
                    "stddev_mean_ratio": 0.6,
                    "subject_initial_ratio": 0.5,
                    "repeated_openers": [],
                    "connector_density_by_paragraph": [0],
                    "sentence_length_buckets": {
                        "ratios": {"short_lt_12": 0.15, "long_gt_28": 0.1}
                    },
                    "paragraph_sentence_counts_uniform": False,
                }
            },
            [],
            [],
            "sachlich",
        )
        preflight = report["summary"]["preflight"]
        self.assertEqual(preflight["risk"], "low")
        self.assertEqual(preflight["calibration_note"], expected)
        lines = humanizer_audit.format_markdown(report).splitlines()
        preflight_index = next(i for i, line in enumerate(lines) if line.startswith("Preflight: "))
        self.assertEqual(lines[preflight_index + 1], f"Calibration: {expected}")

    def test_non_low_preflight_omits_calibration_note_and_markdown_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das Team prüft den Entwurf.", encoding="utf-8")

            _, report = run_json(["--file", str(path)])

        preflight = report["summary"]["preflight"]
        self.assertNotEqual(preflight["risk"], "low")
        self.assertNotIn("calibration_note", preflight)
        self.assertNotIn("\nCalibration: ", humanizer_audit.format_markdown(report))

    def test_antithesis_summary_keeps_density_before_long_matches(self):
        text = (
            "Nicht abwarten, sondern machen. Der Plan ist mutig und nicht vorsichtig. "
            "Wir sollten nicht erklären, sondern liefern. Die Antwort bleibt klar und nicht beliebig. "
            "Die Prüfung ist sorgfältig und nicht flüchtig. Wir wollen nicht vertagen, sondern entscheiden. "
            "Kurz danach beginnt die Prüfung. Eine ausführliche Diskussion mit allen Beteiligten "
            "klärt anschließend die offenen fachlichen Fragen. Am Ende steht ein Befund. "
            "Nach der Freigabe liest jemand sämtliche Verweise noch einmal sorgfältig. "
            "Später endet die Arbeit."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        finding = next(
            item for item in report["findings"] if item.get("kind") == "negation_antithesis_cluster"
        )
        driver = next(
            item
            for item in report["summary"]["preflight"]["drivers"]
            if item["kind"] == "negation_antithesis_cluster"
        )
        self.assertIn("per_1000_words=", finding["summary"])
        self.assertIn("per_1000_words=", driver["detail"])
        self.assertLessEqual(len(finding["summary"]), 140)

    def test_markdown_format_is_compact_and_grouped(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text('"Text"', encoding="utf-8")

            exit_code, output = run_cli(["--file", str(path), "--format", "md"])

        self.assertEqual(exit_code, 0)
        self.assertTrue(output.startswith("Mode: sachlich\n"))
        self.assertIn("Preflight: risk=", output)
        self.assertIn("quality_risk=may_degrade_text_quality", output)
        self.assertIn("Rhythm: sentences=", output)
        self.assertIn("short/medium/long=", output)
        self.assertIn("Findings:\nunicode:", output)
        self.assertIn("straight_quote x2", output)
        self.assertIn("rhythm:\n- none", output)
        self.assertNotIn('"findings"', output)

    def test_markdown_finding_line_caps_long_span_lists(self):
        item = {
            "severity": "warning",
            "pattern": 43,
            "kind": "hidden_unicode",
            "count": 7,
            "summary": "Remove hidden Unicode character.",
            "spans": [{"start": index, "end": index + 1} for index in range(7)],
        }

        line = humanizer_audit.md_finding_line(item)

        self.assertIn("spans=0:1,1:2,2:3,3:4,4:5,+2_more", line)
        self.assertNotIn("5:6", line)

    def test_preflight_high_risk_enables_auto_combing(self):
        text = (
            "Das System beleuchtet nahtlos dynamische Prozesse. "
            "Das System unterstreicht ganzheitlich wichtige Aspekte. "
            "Das System zeigt facettenreich zentrale Faktoren. "
            "Das System fungiert als Lösung. "
            "Das System verfügt über Module. "
            "Das System prüft neue Maßnahmen. "
            "Das System bündelt große Herausforderungen. "
            "Das System liefert passende Ergebnisse."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(text, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["summary"]["preflight"]["risk"], "high")
        self.assertTrue(report["summary"]["preflight"]["combing"]["auto"])
        self.assertEqual(report["summary"]["preflight"]["combing"]["max_iterations"], 2)
        driver_kinds = {item["kind"] for item in report["summary"]["preflight"]["drivers"]}
        self.assertIn("low_burstiness", driver_kinds)
        self.assertIn("ai_marker_cluster", driver_kinds)

    def test_particle_findings_come_from_register(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das ist ja schon wichtig.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path), "--mode", "sachlich"])

        self.assertEqual(exit_code, 0)
        particle_findings = [item for item in report["findings"] if item.get("kind") == "particles_outside_locker"]
        self.assertEqual(len(particle_findings), 1)
        self.assertEqual(particle_findings[0]["source"], "register")
        self.assertEqual(report["summary"]["counts"]["german_pattern"], 0)
        self.assertEqual(report["summary"]["counts"]["register"], 1)

    def test_style_profile_section_without_mode_has_no_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        style = report["style_profile"]
        self.assertEqual(set(style), {"word_count", "sentence_count", "metrics"})
        self.assertGreater(style["word_count"], 0)
        self.assertEqual(style["sentence_count"], 2)
        for key in (
            "mean_sentence_len",
            "stddev_mean_ratio",
            "connector_density",
            "address_counts",
            "particle_count",
            "nominal_style_ratio",
            "type_token_ratio",
        ):
            self.assertIn(key, style["metrics"])

    def test_style_profile_delta_appears_with_explicit_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path), "--mode", "sachlich"])

        self.assertEqual(exit_code, 0)
        style = report["style_profile"]
        self.assertIn("delta", style)
        self.assertGreater(len(style["delta"]), 0)
        for name, item in style["delta"].items():
            self.assertEqual(set(item), {"value", "range", "in_range"})
            self.assertEqual(item["value"], style["metrics"][name])
            self.assertIsInstance(item["in_range"], bool)

    def test_explicit_profile_overrides_style_corridor(self):
        payload = {
            "schema_version": 1,
            "overrides": {"sachlich": {"particle_count": {"max": 99}}},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            profile_path = Path(tmp) / "profile.json"
            path.write_text("Das ist ja schon wichtig.", encoding="utf-8")
            profile_path.write_text(json.dumps(payload), encoding="utf-8")

            exit_code, report = run_json(
                ["--file", str(path), "--mode", "sachlich", "--profile", str(profile_path)]
            )

        self.assertEqual(exit_code, 0)
        particle_delta = report["style_profile"]["delta"]["particle_count"]
        self.assertEqual(particle_delta["range"], {"max": 99})
        self.assertTrue(particle_delta["override"])

    def test_explicit_missing_profile_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            missing = Path(tmp) / "missing-profile.json"
            path.write_text("Das Team prüft die Datei.", encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = humanizer_audit.main(
                    ["--file", str(path), "--profile", str(missing)]
                )

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn(f"--profile requires an existing file: {missing}", stderr.getvalue())

    def test_missing_default_profile_remains_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "text.md"
            path.write_text("Das Team prüft die Datei.", encoding="utf-8")
            stderr = io.StringIO()
            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                with redirect_stderr(stderr):
                    exit_code, report = run_json(
                        ["--file", str(path), "--mode", "sachlich"]
                    )
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertNotIn("override", report["style_profile"]["delta"]["particle_count"])

    def test_no_profile_ignores_default_profile(self):
        payload = {
            "schema_version": 1,
            "overrides": {"sachlich": {"particle_count": {"max": 99}}},
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "text.md"
            profile_dir = root / ".humanizer"
            profile_dir.mkdir()
            path.write_text("Das ist ja schon wichtig.", encoding="utf-8")
            (profile_dir / "profile.json").write_text(json.dumps(payload), encoding="utf-8")
            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                _, with_profile = run_json(["--file", str(path), "--mode", "sachlich"])
                exit_code, without_profile = run_json(
                    ["--file", str(path), "--mode", "sachlich", "--no-profile"]
                )
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(exit_code, 0)
        self.assertTrue(with_profile["style_profile"]["delta"]["particle_count"]["override"])
        without_delta = without_profile["style_profile"]["delta"]["particle_count"]
        self.assertEqual(without_delta["range"], {"max": 0})
        self.assertNotIn("override", without_delta)

    def test_profile_and_no_profile_conflict(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            humanizer_audit.parse_args(
                ["--file", "text.md", "--profile", "profile.json", "--no-profile"]
            )

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("not allowed with argument --profile", stderr.getvalue())

    def test_latest_picks_newest_markdown_file_recursively(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_path = root / "old.md"
            nested = root / "nested"
            nested.mkdir()
            newest_path = nested / "newest.md"
            ignored_path = root / "ignored.txt"

            old_path.write_text("Alt.", encoding="utf-8")
            newest_path.write_text("Neu.", encoding="utf-8")
            ignored_path.write_text("Ignoriert.", encoding="utf-8")
            os.utime(old_path, (1_700_000_000, 1_700_000_000))
            os.utime(newest_path, (1_700_000_100, 1_700_000_100))
            os.utime(ignored_path, (1_700_000_200, 1_700_000_200))

            exit_code, report = run_json(["--latest", str(root)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["file"], str(newest_path))

    def test_latest_ignores_hidden_and_generated_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = root / "draft.md"
            hidden_dir = root / ".cache"
            hidden_dir.mkdir()
            cached = hidden_dir / "README.md"
            build_dir = root / "build"
            build_dir.mkdir()
            generated = build_dir / "report.md"
            hidden_file = root / ".notes.md"

            draft.write_text("Entwurf.", encoding="utf-8")
            cached.write_text("Cache.", encoding="utf-8")
            generated.write_text("Generiert.", encoding="utf-8")
            hidden_file.write_text("Versteckt.", encoding="utf-8")
            os.utime(draft, (1_700_000_000, 1_700_000_000))
            os.utime(cached, (1_700_000_300, 1_700_000_300))
            os.utime(generated, (1_700_000_200, 1_700_000_200))
            os.utime(hidden_file, (1_700_000_100, 1_700_000_100))

            exit_code, report = run_json(["--latest", str(root)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["file"], str(draft))

    def test_latest_with_only_generated_files_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / ".cache"
            cache.mkdir()
            (cache / "README.md").write_text("Cache.", encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = humanizer_audit.main(["--latest", tmp])

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("No eligible *.md files found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
