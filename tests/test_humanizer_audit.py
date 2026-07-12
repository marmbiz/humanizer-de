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
    def test_file_json_output_shape_and_unicode_collapse(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text('"Text" "Mehr"', encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["file"], str(path))
        self.assertEqual(report["mode"], "sachlich")
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

    def test_without_precise_keeps_default_report_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "clean.md"
            path.write_text("Das Team prüft die Datei. Danach endet der Test.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(set(report), {"file", "mode", "ok", "summary", "style_profile", "findings"})
        self.assertEqual(set(report["summary"]), {"rhythm", "preflight", "counts"})
        self.assertEqual(set(report["summary"]["counts"]), {"unicode", "rhythm", "german_pattern", "register"})
        self.assertNotIn("precise", report["summary"])
        self.assertNotIn("syntax", report)

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

    def test_duplicate_particle_findings_are_collapsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("Das ist ja schon wichtig.", encoding="utf-8")

            exit_code, report = run_json(["--file", str(path), "--mode", "sachlich"])

        self.assertEqual(exit_code, 0)
        particle_findings = [item for item in report["findings"] if item.get("kind") == "particles_outside_locker"]
        self.assertEqual(len(particle_findings), 1)
        self.assertEqual(particle_findings[0]["source"], "german_pattern")
        self.assertEqual(report["summary"]["counts"]["german_pattern"], 1)
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
