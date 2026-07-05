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

    def test_common_noun_after_article_is_not_proper_name(self):
        before = "Es ist wichtig, das Problem zügig zu lösen. Danach geht es weiter."
        after = "Die Lösung des Problems hat Priorität. Danach geht es weiter."
        found = kinds(evidence_lint.lint(before, after))
        self.assertNotIn("removed_proper_name", found)
        self.assertNotIn("added_proper_name", found)

    def test_case_variant_is_not_anchor_change(self):
        before = "Wir besprechen das Problem."
        after = "Wir besprechen die Ursache des Problems."
        found = kinds(evidence_lint.lint(before, after))
        self.assertNotIn("removed_proper_name", found)
        self.assertNotIn("added_proper_name", found)

    def test_real_entities_still_flagged(self):
        before = "Der Konzern veröffentlichte Zahlen."
        after = "Die Deutsche Bahn veröffentlichte Zahlen."
        findings = evidence_lint.lint(before, after)
        added = [item for item in findings if item["kind"] == "added_proper_name"]
        self.assertTrue(added)
        self.assertIn("Deutsche Bahn", added[0]["values"])

    def test_acronym_after_article_is_kept(self):
        before = "Die Behörde prüft."
        after = "Die BaFin prüft."
        findings = evidence_lint.lint(before, after)
        added = [item for item in findings if item["kind"] == "added_proper_name"]
        self.assertTrue(added)
        self.assertIn("BaFin", added[0]["values"])

    def test_hard_anchors_unaffected(self):
        before = "Die Wartezeit sank laut Bericht."
        after = "Die Wartezeit sank laut Bericht um 63 Prozent."
        number_findings = [
            item for item in evidence_lint.lint(before, after) if item["kind"] == "added_number"
        ]
        self.assertTrue(number_findings)
        self.assertEqual(number_findings[0]["severity"], "blocker")

        before_url = "Details unter https://example.org/bericht stehen bereit."
        after_url = "Details stehen bereit."
        url_findings = [
            item for item in evidence_lint.lint(before_url, after_url) if item["kind"] == "removed_url"
        ]
        self.assertTrue(url_findings)
        self.assertEqual(url_findings[0]["severity"], "blocker")

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
