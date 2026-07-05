import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
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
