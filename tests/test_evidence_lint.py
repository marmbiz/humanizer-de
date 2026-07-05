import importlib.util
import json
import subprocess
import sys
import tempfile
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

    def test_blocks_direction_reversal_with_same_anchor(self):
        before = "Die Fehlerquote sank um 12 Prozent."
        after = "Die Fehlerquote stieg um 12 Prozent."
        self.assertIn("claim_direction_changed", kinds(evidence_lint.lint(before, after)))


class EvidenceLintCliTests(unittest.TestCase):
    def run_pair(self, before: str, after: str) -> tuple[int, dict]:
        with tempfile.TemporaryDirectory() as tmp:
            before_path = Path(tmp) / "before.txt"
            after_path = Path(tmp) / "after.txt"
            before_path.write_text(before, encoding="utf-8")
            after_path.write_text(after, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--before-file", str(before_path), "--after-file", str(after_path)],
                capture_output=True,
                text=True,
            )
        return proc.returncode, json.loads(proc.stdout)

    def test_file_pair_mode_blocker_exits_1(self):
        code, report = self.run_pair(
            "Die Wartezeit sank laut Bericht.",
            "Die Wartezeit sank laut Bericht um 63 Prozent.",
        )
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        blockers = [item for item in report["findings"] if item["severity"] == "blocker"]
        self.assertIn("added_number", {item["kind"] for item in blockers})

    def test_file_pair_mode_clean_exits_0(self):
        code, report = self.run_pair(
            "Die API liefert Status 200 und ein leeres Array.",
            "Die API liefert Status 200. Sie gibt ein leeres Array zurück.",
        )
        self.assertEqual(code, 0)
        self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))


if __name__ == "__main__":
    unittest.main()
