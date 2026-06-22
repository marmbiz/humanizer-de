import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evidence_lint.py"

spec = importlib.util.spec_from_file_location("evidence_lint", SCRIPT)
evidence_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence_lint)


def kinds(findings):
    return {item["kind"] for item in findings}


class EvidenceLintTests(unittest.TestCase):
    def test_blocks_new_number(self):
        before = "Die Wartezeit sank laut Bericht."
        after = "Die Wartezeit sank laut Bericht um 63 Prozent."
        self.assertIn("added_number", kinds(evidence_lint.lint(before, after)))

    def test_blocks_changed_quote(self):
        before = "Im Bericht steht: „unter zwei Minuten Wartezeit“."
        after = "Im Bericht steht: „unter drei Minuten Wartezeit“."
        found = kinds(evidence_lint.lint(before, after))
        self.assertIn("removed_quote", found)
        self.assertIn("added_quote", found)

    def test_allows_sentence_split_with_same_anchor(self):
        before = "Die API liefert Status 200 und ein leeres Array."
        after = "Die API liefert Status 200. Sie gibt ein leeres Array zurück."
        self.assertFalse(any(item["severity"] == "blocker" for item in evidence_lint.lint(before, after)))

    def test_warns_new_proper_name(self):
        before = "Die Stadt veröffentlichte den Bericht."
        after = "Die Stadt Köln veröffentlichte den Bericht."
        self.assertIn("added_proper_name", kinds(evidence_lint.lint(before, after)))


if __name__ == "__main__":
    unittest.main()
