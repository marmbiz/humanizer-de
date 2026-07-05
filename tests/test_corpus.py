import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "corpus"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


unicode_lint = load_module("unicode_lint", ROOT / "scripts" / "unicode_lint.py")
rhythm_lint = load_module("rhythm_lint", ROOT / "scripts" / "rhythm_lint.py")
style_profile = load_module("style_profile", ROOT / "scripts" / "style_profile.py")


class CorpusTests(unittest.TestCase):
    def test_golden_corpus_expectations(self):
        for input_path in sorted(CORPUS.glob("case_*_input.md")):
            with self.subTest(case=input_path.name):
                text = input_path.read_text()
                expected_path = input_path.with_name(input_path.name.replace("_input.md", "_expected.json"))
                expected = json.loads(expected_path.read_text())
                word_count = len(re.findall(r"\S+", text))

                self.assertGreaterEqual(word_count, 150)
                self.assertLessEqual(word_count, 300)

                unicode_patterns = {item["pattern"] for item in unicode_lint.lint(text)}
                rhythm_patterns = {item["pattern"] for item in rhythm_lint.analyze(text, file=str(input_path))["suspicions"]}

                expected_unicode = set(expected["unicode_patterns"])
                expected_rhythm = set(expected["rhythm_patterns"])

                if expected_unicode:
                    self.assertTrue(expected_unicode.issubset(unicode_patterns))
                else:
                    self.assertEqual(unicode_patterns, set())

                if expected_rhythm:
                    self.assertTrue(expected_rhythm.issubset(rhythm_patterns))
                else:
                    self.assertEqual(rhythm_patterns, set())

                ranges = expected.get("style_profile_ranges")
                if ranges:
                    metrics = style_profile.profile(text, str(input_path))["metrics"]
                    for metric, corridor in ranges.items():
                        value = metrics[metric]
                        self.assertGreaterEqual(value, corridor["min"], f"{metric} below corridor")
                        self.assertLessEqual(value, corridor["max"], f"{metric} above corridor")


if __name__ == "__main__":
    unittest.main()
