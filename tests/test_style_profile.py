import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "style_profile.py"

spec = importlib.util.spec_from_file_location("style_profile", SCRIPT)
style_profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style_profile)


METRIC_KEYS = {
    "mean_sentence_len",
    "stddev_sentence_len",
    "stddev_mean_ratio",
    "len_buckets",
    "subject_initial_ratio",
    "connector_density",
    "repeated_openers",
    "paragraph_uniformity",
    "address_counts",
    "particle_count",
    "emoji_count",
    "rhetorical_questions",
    "nominal_style_ratio",
    "type_token_ratio",
}

UNIFORM_TEXT = (
    "Das System prüft heute alle neuen Dateien im Ordner. "
    "Das System liest danach alle alten Berichte im Archiv. "
    "Das System sortiert später alle offenen Anfragen im Postfach. "
    "Das System sendet abends alle fertigen Antworten im Paket. "
    "Das System speichert nachts alle neuen Einträge im Katalog. "
    "Das System zählt morgens alle offenen Punkte im Plan. "
    "Das System meldet mittags alle klaren Ergebnisse im Bericht. "
    "Das System schließt zuletzt alle alten Vorgänge im Register."
)

VARIED_TEXT = (
    "Kurz gesagt: nein. "
    "Wer den Bericht liest, merkt schnell, dass die Zahlen aus dem letzten Quartal deutlich besser ausfallen, als das Team im Frühjahr erwartet hatte. "
    "Warum? "
    "Weil zwei Kunden früher bestellt haben. "
    "Der Rest der Geschichte ist schnell erzählt, denn nach dem Sommer kamen kaum noch Rückfragen, und die offenen Posten schrumpften von Woche zu Woche. "
    "Ein Detail bleibt offen. "
    "Ob sich dieser Trend hält, weiß niemand, aber die Vorzeichen für das kommende Jahr wirken freundlicher als zuletzt. "
    "Mehr steht im Anhang."
)


def run_json(argv):
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        exit_code = style_profile.main(argv)
    return exit_code, json.loads(stdout.getvalue())


class StyleProfileShapeTests(unittest.TestCase):
    def test_report_shape_and_types(self):
        exit_code, report = run_json(["--text", UNIFORM_TEXT])

        self.assertEqual(exit_code, 0)
        self.assertEqual(set(report), {"meta", "metrics"})
        self.assertEqual(set(report["meta"]), {"source", "word_count", "sentence_count"})
        self.assertEqual(report["meta"]["source"], "<text>")
        self.assertIsInstance(report["meta"]["word_count"], int)
        self.assertIsInstance(report["meta"]["sentence_count"], int)

        metrics = report["metrics"]
        self.assertEqual(set(metrics), METRIC_KEYS)
        for key in ("mean_sentence_len", "stddev_sentence_len", "stddev_mean_ratio", "subject_initial_ratio", "nominal_style_ratio", "type_token_ratio"):
            self.assertIsInstance(metrics[key], (int, float), key)
        for key in ("connector_density", "repeated_openers", "particle_count", "emoji_count", "rhetorical_questions"):
            self.assertIsInstance(metrics[key], int, key)
        self.assertIsInstance(metrics["paragraph_uniformity"], bool)
        self.assertEqual(set(metrics["len_buckets"]), {"counts", "ratios"})
        for section in metrics["len_buckets"].values():
            self.assertEqual(set(section), {"short_lt_12", "medium_12_to_28", "long_gt_28"})
        self.assertEqual(set(metrics["address_counts"]), {"du", "sie", "wir", "man"})
        for value in metrics["address_counts"].values():
            self.assertIsInstance(value, int)

    def test_no_interpretation_keys_in_output(self):
        exit_code, report = run_json(["--text", UNIFORM_TEXT])

        self.assertEqual(exit_code, 0)
        serialized = json.dumps(report)
        for forbidden in ("pattern", "suspicion", "severity", "finding", "risk", "recommendation"):
            self.assertNotIn(forbidden, serialized)

    def test_file_input_sets_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text(VARIED_TEXT, encoding="utf-8")

            exit_code, report = run_json(["--file", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["meta"]["source"], str(path))
        self.assertGreater(report["meta"]["word_count"], 0)


class StyleProfileTargetTests(unittest.TestCase):
    def test_target_adds_delta_section(self):
        exit_code, report = run_json(["--text", UNIFORM_TEXT, "--target", "sachlich"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(set(report), {"meta", "metrics", "delta"})
        for name, entry in report["delta"].items():
            self.assertIn(name, METRIC_KEYS)
            self.assertEqual(set(entry), {"value", "range", "in_range"})
            self.assertIsInstance(entry["in_range"], bool)
            self.assertTrue(set(entry["range"]) <= {"min", "max"})

    def test_target_sachlich_separates_fixtures(self):
        _, uniform = run_json(["--text", UNIFORM_TEXT, "--target", "sachlich"])
        _, varied = run_json(["--text", VARIED_TEXT, "--target", "sachlich"])

        self.assertFalse(uniform["delta"]["stddev_mean_ratio"]["in_range"])
        self.assertFalse(uniform["delta"]["repeated_openers"]["in_range"])
        self.assertTrue(varied["delta"]["stddev_mean_ratio"]["in_range"])
        self.assertTrue(varied["delta"]["repeated_openers"]["in_range"])

    def test_unknown_target_fails_cleanly(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = style_profile.main(["--text", UNIFORM_TEXT, "--target", "episch"])

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("episch", stderr.getvalue())

    def test_in_range_boundaries(self):
        min_only = style_profile.delta({"m": 0.4}, {"m": {"min": 0.4}})
        self.assertTrue(min_only["m"]["in_range"])
        self.assertFalse(style_profile.delta({"m": 0.399}, {"m": {"min": 0.4}})["m"]["in_range"])

        max_only = style_profile.delta({"m": 1}, {"m": {"max": 1}})
        self.assertTrue(max_only["m"]["in_range"])
        self.assertFalse(style_profile.delta({"m": 2}, {"m": {"max": 1}})["m"]["in_range"])

        corridor = {"m": {"min": 0.4, "max": 0.9}}
        self.assertTrue(style_profile.delta({"m": 0.4}, corridor)["m"]["in_range"])
        self.assertTrue(style_profile.delta({"m": 0.9}, corridor)["m"]["in_range"])
        self.assertFalse(style_profile.delta({"m": 0.3}, corridor)["m"]["in_range"])
        self.assertFalse(style_profile.delta({"m": 0.91}, corridor)["m"]["in_range"])

    def test_targets_file_uses_known_metrics_and_lint_modes(self):
        targets = style_profile.load_targets()
        self.assertEqual(set(targets), {"locker", "sachlich", "formal"})
        for corridors in targets.values():
            for metric, corridor in corridors.items():
                self.assertIn(metric, METRIC_KEYS)
                self.assertTrue(set(corridor) <= {"min", "max"})
                self.assertTrue(corridor)


class UserProfileTests(unittest.TestCase):
    def write_profile(self, tmp: str, payload) -> Path:
        path = Path(tmp) / "profile.json"
        content = payload if isinstance(payload, str) else json.dumps(payload)
        path.write_text(content, encoding="utf-8")
        return path

    def test_missing_profile_is_silent(self):
        overrides, warnings = style_profile.load_user_profile(Path("/nonexistent/profile.json"), style_profile.load_targets())
        self.assertEqual(overrides, {})
        self.assertEqual(warnings, [])

    def test_broken_json_degrades_to_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_profile(tmp, "{not json")
            overrides, warnings = style_profile.load_user_profile(path, style_profile.load_targets())
        self.assertEqual(overrides, {})
        self.assertEqual(len(warnings), 1)
        self.assertIn("ignored", warnings[0])

    def test_unknown_target_and_metric_are_skipped_with_warning(self):
        payload = {
            "schema_version": 1,
            "overrides": {
                "episch": {"particle_count": {"max": 5}},
                "sachlich": {
                    "particle_count": {"max": 1},
                    "unbekannte_metrik": {"max": 1},
                    "emoji_count": {"max": "viele"},
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_profile(tmp, payload)
            overrides, warnings = style_profile.load_user_profile(path, style_profile.load_targets())
        self.assertEqual(overrides, {"sachlich": {"particle_count": {"max": 1}}})
        self.assertEqual(len(warnings), 3)

    def test_missing_or_unsupported_schema_is_ignored(self):
        payloads = (
            {"overrides": {"sachlich": {"particle_count": {"max": 99}}}},
            {"schema_version": 2, "overrides": {"sachlich": {"particle_count": {"max": 99}}}},
            {"schema_version": True, "overrides": {"sachlich": {"particle_count": {"max": 99}}}},
        )
        for payload in payloads:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                path = self.write_profile(tmp, payload)
                overrides, warnings = style_profile.load_user_profile(path, style_profile.load_targets())

            self.assertEqual(overrides, {})
            self.assertEqual(len(warnings), 1)
            self.assertIn("schema_version must be 1", warnings[0])

    def test_invalid_numeric_corridors_cannot_override_targets(self):
        payload = {
            "schema_version": 1,
            "overrides": {
                "sachlich": {
                    "particle_count": {"min": 5, "max": 1},
                    "emoji_count": {"max": float("nan")},
                    "repeated_openers": {"max": float("inf")},
                }
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_profile(tmp, payload)
            overrides, warnings = style_profile.load_user_profile(path, style_profile.load_targets())

        self.assertEqual(overrides, {})
        self.assertEqual(len(warnings), 3)
        targets = style_profile.merge_targets(style_profile.load_targets(), overrides)
        report = style_profile.delta(
            {"particle_count": 999},
            {"particle_count": targets["sachlich"]["particle_count"]},
        )
        self.assertFalse(report["particle_count"]["in_range"])

    def test_merge_override_replaces_whole_corridor(self):
        base = {"sachlich": {"stddev_mean_ratio": {"min": 0.4}, "particle_count": {"max": 0}}}
        merged = style_profile.merge_targets(base, {"sachlich": {"stddev_mean_ratio": {"max": 2.0}}})

        self.assertEqual(merged["sachlich"]["stddev_mean_ratio"], {"max": 2.0})
        self.assertEqual(merged["sachlich"]["particle_count"], {"max": 0})
        self.assertEqual(base["sachlich"]["stddev_mean_ratio"], {"min": 0.4})

    def test_delta_marks_overridden_metrics(self):
        report = style_profile.delta({"m": 1, "n": 2}, {"m": {"max": 3}, "n": {"max": 3}}, frozenset({"m"}))
        self.assertTrue(report["m"]["override"])
        self.assertNotIn("override", report["n"])

    def test_cli_profile_overrides_target_corridor(self):
        payload = {"schema_version": 1, "overrides": {"sachlich": {"particle_count": {"max": 99}}}}
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_profile(tmp, payload)
            _, with_profile = run_json(["--text", UNIFORM_TEXT, "--target", "sachlich", "--profile", str(path)])
            _, without_profile = run_json(["--text", UNIFORM_TEXT, "--target", "sachlich", "--profile", str(path), "--no-profile"])

        self.assertEqual(with_profile["delta"]["particle_count"]["range"], {"max": 99})
        self.assertTrue(with_profile["delta"]["particle_count"]["override"])
        self.assertEqual(without_profile["delta"]["particle_count"]["range"], {"max": 0})
        self.assertNotIn("override", without_profile["delta"]["particle_count"])

    def test_cli_broken_profile_warns_and_continues(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_profile(tmp, "{not json")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = style_profile.main(["--text", UNIFORM_TEXT, "--target", "sachlich", "--profile", str(path)])

        self.assertEqual(exit_code, 0)
        self.assertIn("warning:", stderr.getvalue())
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["delta"]["particle_count"]["range"], {"max": 0})


class StyleProfileContrastTests(unittest.TestCase):
    def test_uniform_text_has_low_variance_and_high_repetition(self):
        _, report = run_json(["--text", UNIFORM_TEXT])
        metrics = report["metrics"]

        self.assertLess(metrics["stddev_mean_ratio"], 0.2)
        self.assertGreater(metrics["repeated_openers"], 2)
        self.assertGreater(metrics["subject_initial_ratio"], 0.9)
        self.assertLess(metrics["type_token_ratio"], 0.6)

    def test_varied_text_has_higher_variance_and_lexical_diversity(self):
        _, uniform = run_json(["--text", UNIFORM_TEXT])
        _, varied = run_json(["--text", VARIED_TEXT])

        self.assertGreater(varied["metrics"]["stddev_mean_ratio"], uniform["metrics"]["stddev_mean_ratio"])
        self.assertGreater(varied["metrics"]["type_token_ratio"], uniform["metrics"]["type_token_ratio"])
        self.assertLess(varied["metrics"]["repeated_openers"], uniform["metrics"]["repeated_openers"])
        self.assertGreater(varied["metrics"]["stddev_mean_ratio"], 0.4)
        self.assertGreater(varied["metrics"]["len_buckets"]["ratios"]["short_lt_12"], 0.3)
        self.assertGreater(varied["metrics"]["rhetorical_questions"], 0)

    def test_nominal_style_ratio_counts_abstracta(self):
        _, plain = run_json(["--text", "Der Hund läuft schnell durch den Park."])
        _, nominal = run_json(["--text", "Die Maßnahmen betreffen Prozesse, Faktoren und Herausforderungen sowie Lösungen und Aspekte."])

        self.assertEqual(plain["metrics"]["nominal_style_ratio"], 0.0)
        self.assertGreater(nominal["metrics"]["nominal_style_ratio"], 10.0)


if __name__ == "__main__":
    unittest.main()
