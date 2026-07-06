import io
import importlib.util
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "humanizer_audit.py"

spec = importlib.util.spec_from_file_location("humanizer_audit", SCRIPT)
humanizer_audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(humanizer_audit)


def run_cli(argv):
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        exit_code = humanizer_audit.main(argv)
    return exit_code, stdout.getvalue()


def run_json(argv):
    exit_code, output = run_cli(argv)
    return exit_code, json.loads(output)


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


if __name__ == "__main__":
    unittest.main()
