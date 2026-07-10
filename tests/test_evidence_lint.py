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


def spacy_model_available():
    try:
        import spacy

        spacy.load("de_core_news_sm")
    except Exception:
        return False
    return True


SPACY_MODEL_AVAILABLE = spacy_model_available()


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

    def test_swiss_guillemets_are_protected_quotes(self):
        before = "Im Bericht steht: «unter zwei Minuten Wartezeit»."
        after = "Im Bericht steht: «unter drei Minuten Wartezeit»."

        found = kinds(evidence_lint.lint(before, after))

        self.assertIn("removed_quote", found)
        self.assertIn("added_quote", found)

    def test_apostrophes_in_contractions_are_not_quote_anchors(self):
        text = "Wenn's heute klappt, gibt's morgen mehr."

        self.assertEqual(evidence_lint.anchors(text)["quote"], set())

    def test_number_anchor_keeps_sign_unit_and_comparator(self):
        cases = (
            ("Die Marge beträgt -5 Prozent.", "Die Marge beträgt 5 Prozent."),
            ("Die Quote liegt bei 12%.", "Die Quote liegt bei 12."),
            ("Es sind mindestens 12 Fälle.", "Es sind höchstens 12 Fälle."),
        )

        for before, after in cases:
            with self.subTest(before=before, after=after):
                found = kinds(evidence_lint.lint(before, after))
                self.assertIn("removed_number", found)
                self.assertIn("added_number", found)

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

    def test_name_suffix_is_not_silently_stripped(self):
        before = "Wir arbeiten mit Mercedes."
        after = "Wir arbeiten mit Merced."

        found = kinds(evidence_lint.lint(before, after))

        self.assertIn("removed_proper_name", found)
        self.assertIn("added_proper_name", found)

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

    def test_default_keeps_single_token_abstract_noun_after_verb(self):
        before = "Der Bericht bleibt kurz."
        after = "Der Bericht hat Relevanz."
        self.assertIn("added_proper_name", kinds(evidence_lint.lint(before, after)))

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

    def test_write_and_load_ledger_roundtrip_preserves_anchors(self):
        before = (
            "Die Wartezeit sank am 3. Mai 2024 um 12 Prozent. "
            "Details stehen unter https://example.org/bericht."
        )

        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            expected = evidence_lint.write_ledger(before, ledger_path)
            loaded = evidence_lint.load_ledger(ledger_path)
            document = json.loads(ledger_path.read_text(encoding="utf-8"))

        self.assertEqual(loaded, expected)
        self.assertEqual(loaded, evidence_lint.anchors(before))
        self.assertEqual(document["schema_version"], 2)
        self.assertEqual(document["extraction_policy"], {"mode": "default"})

    def test_ledger_catches_multi_pass_number_drift_against_original(self):
        original = "Die Fehlerquote sank laut Bericht um 12 Prozent."
        pass1 = "Laut Bericht sank die Fehlerquote um rund 12 Prozent."
        pass2 = "Laut Bericht sank die Fehlerquote um etwa ein Achtel."
        pass3 = "Der Bericht beschreibt eine spürbar geringere Fehlerquote."

        ledger_anchors = evidence_lint.anchors(original)

        self.assertIn("removed_number", kinds(evidence_lint.lint(pass1, pass2)))
        self.assertNotIn("removed_number", kinds(evidence_lint.lint(pass2, pass3)))
        self.assertIn("removed_number", kinds(evidence_lint.lint_with_anchors(ledger_anchors, pass3)))


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

    def test_ledger_mode_matches_anchor_lint(self):
        before = "Die Fehlerquote sank laut Bericht um 12 Prozent."
        after = "Der Bericht beschreibt eine geringere Fehlerquote."

        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            evidence_lint.write_ledger(before, ledger_path)
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--ledger", str(ledger_path), "--after", after],
                capture_output=True,
                text=True,
            )
            expected = evidence_lint.lint_with_anchors(evidence_lint.load_ledger(ledger_path), after)

        self.assertEqual(proc.returncode, 1)
        self.assertEqual(json.loads(proc.stdout)["findings"], expected)

    def test_ledger_mode_rejects_before_argument(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--ledger", "ledger.json", "--before", "alt", "--after", "neu"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("--ledger cannot be combined with --before or --before-file", proc.stderr)

    def test_no_input_is_usage_error(self):
        proc = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)

        self.assertEqual(proc.returncode, 2)
        self.assertIn("pair mode requires", proc.stderr)

    def test_empty_fixture_directory_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--fixture", tmp],
                capture_output=True,
                text=True,
            )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("no JSON fixture files found", proc.stderr)

    def test_ledger_mode_rejects_extraction_policy_mismatch(self):
        before = "Wir arbeiten mit Mercedes."
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            evidence_lint.write_ledger(before, ledger_path)
            data = json.loads(ledger_path.read_text(encoding="utf-8"))
            data["extraction_policy"] = {
                "mode": "spacy_ner",
                "model": "core_news_sm",
                "model_version": "test",
            }
            ledger_path.write_text(json.dumps(data), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--ledger", str(ledger_path), "--after", before],
                capture_output=True,
                text=True,
            )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("extraction policy does not match", proc.stderr)

    def test_schema_one_ledger_remains_readable(self):
        before = "Die Quote beträgt 12 Prozent."
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            data = {
                "schema_version": 1,
                "anchors": evidence_lint.serializable_anchors(evidence_lint.anchors(before)),
            }
            ledger_path.write_text(json.dumps(data), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--ledger", str(ledger_path), "--after", before],
                capture_output=True,
                text=True,
            )

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout)["ledger_extraction_policy"], "legacy_unknown")


@unittest.skipUnless(SPACY_MODEL_AVAILABLE, "spaCy German model is not available")
class EvidenceLintPreciseTests(unittest.TestCase):
    def test_precise_filters_single_token_abstract_noun_after_verb(self):
        before = "Der Bericht bleibt kurz."
        after = "Der Bericht hat Relevanz."

        self.assertNotIn("added_proper_name", kinds(evidence_lint.lint(before, after, precise=True)))

    def test_precise_keeps_new_multiword_name(self):
        before = "Sie trifft eine Person."
        after = "Sie trifft Angela Merkel."
        findings = evidence_lint.lint(before, after, precise=True)
        added = [item for item in findings if item["kind"] == "added_proper_name"]

        self.assertTrue(added)
        self.assertIn("Angela Merkel", added[0]["values"])

    def test_precise_keeps_internal_uppercase_name(self):
        before = "Die Behörde prüft."
        after = "Die BaFin prüft."
        findings = evidence_lint.lint(before, after, precise=True)
        added = [item for item in findings if item["kind"] == "added_proper_name"]

        self.assertTrue(added)
        self.assertIn("BaFin", added[0]["values"])


if __name__ == "__main__":
    unittest.main()
