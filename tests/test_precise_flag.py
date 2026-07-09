import builtins
import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

TEXT = (
    "Du kannst die maßgeschneiderten Lösungen nahtlos beleuchten. "
    "Bitte senden Sie das Ergebnis, denn es fungiert als Grundlage und dient als Beispiel. "
    "Das ist ja wichtig: Maßnahmen, Aspekte und Prozesse bleiben sichtbar."
)
BEFORE = "Der Bericht nennt 12 Prozent für Alpha."
AFTER = TEXT + " Der Bericht nennt 13 Prozent für Alpha und Beta."

EXPECTED_REGISTER_JSON = """{
  "ok": false,
  "mode": "sachlich",
  "expected_address": "du",
  "features": {
    "du_count": 1,
    "sie_formal_count": 1,
    "wir_count": 0,
    "man_count": 0,
    "modal_particle_count": 1,
    "emoji_count": 0,
    "rhetorical_questions": 0
  },
  "findings": [
    {
      "severity": "warning",
      "kind": "mixed_address",
      "message": "Du- and Sie-address appear in the same passage."
    },
    {
      "severity": "blocker",
      "kind": "unexpected_sie",
      "message": "Profile expects du-address, but formal Sie appears."
    },
    {
      "severity": "warning",
      "kind": "particles_outside_locker",
      "message": "Modal particles should not be added in Sachlich/Formal."
    }
  ]
}
"""

EXPECTED_GERMAN_PATTERN_JSON = """{
  "ok": false,
  "mode": "sachlich",
  "findings": [
    {
      "pattern": 64,
      "kind": "ai_marker_cluster",
      "severity": "warning",
      "evidence": {
        "beleuchten": 1,
        "nahtlos": 1,
        "maßgeschneidert": 1
      }
    },
    {
      "pattern": 65,
      "kind": "copula_avoidance_cluster",
      "severity": "warning",
      "evidence": {
        "fungiert als": 1,
        "dient als": 1
      }
    },
    {
      "pattern": 58,
      "kind": "abstraction_cluster",
      "severity": "warning",
      "evidence": {
        "maßnahmen": 1,
        "aspekte": 1,
        "lösungen": 1,
        "prozesse": 1
      }
    },
    {
      "pattern": 63,
      "kind": "particles_outside_locker",
      "severity": "warning",
      "evidence": {
        "count": 1
      }
    }
  ]
}
"""

EXPECTED_EVIDENCE_JSON = """{
  "ok": false,
  "findings": [
    {
      "severity": "blocker",
      "kind": "removed_number",
      "message": "number anchor removed or changed.",
      "values": [
        "12 Prozent"
      ]
    },
    {
      "severity": "blocker",
      "kind": "added_number",
      "message": "New number anchor introduced.",
      "values": [
        "13 Prozent"
      ]
    },
    {
      "severity": "warning",
      "kind": "added_proper_name",
      "message": "New proper_name anchor introduced.",
      "values": [
        "Beta",
        "Lösungen"
      ]
    }
  ]
}
"""


def load_script(name):
    script = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_linters():
    sys.modules.pop("syntax_lint", None)
    return {
        "register": load_script("register_lint"),
        "german_pattern": load_script("german_pattern_lint"),
        "evidence": load_script("evidence_lint"),
    }


def run_cli(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = module.main(argv)
    return exit_code, stdout.getvalue(), json.loads(stdout.getvalue())


def run_all(modules, precise=False):
    flag = ["--precise"] if precise else []
    return {
        "register": run_cli(
            modules["register"],
            ["--text", TEXT, "--mode", "sachlich", "--expected-address", "du", *flag],
        ),
        "german_pattern": run_cli(
            modules["german_pattern"],
            ["--text", TEXT, "--mode", "sachlich", *flag],
        ),
        "evidence": run_cli(
            modules["evidence"],
            ["--before", BEFORE, "--after", AFTER, *flag],
        ),
    }


def spacy_model_available():
    try:
        import spacy

        spacy.load("de_core_news_sm")
    except Exception:
        return False
    return True


SPACY_MODEL_AVAILABLE = spacy_model_available()


class PreciseFlagSnapshotTests(unittest.TestCase):
    def test_reports_without_flag_match_snapshots(self):
        results = run_all(load_linters())

        self.assertEqual(results["register"][0], 1)
        self.assertEqual(results["register"][1], EXPECTED_REGISTER_JSON)
        self.assertEqual(results["german_pattern"][0], 0)
        self.assertEqual(results["german_pattern"][1], EXPECTED_GERMAN_PATTERN_JSON)
        self.assertEqual(results["evidence"][0], 1)
        self.assertEqual(results["evidence"][1], EXPECTED_EVIDENCE_JSON)


class PreciseFlagMissingSpacyTests(unittest.TestCase):
    def test_precise_without_spacy_reports_inactive_and_keeps_findings(self):
        modules = load_linters()
        default_results = run_all(modules)

        real_import = builtins.__import__

        def import_without_spacy(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "spacy" or name.startswith("spacy."):
                raise ModuleNotFoundError("No module named 'spacy'")
            return real_import(name, globals, locals, fromlist, level)

        sys.modules.pop("syntax_lint", None)
        with mock.patch("builtins.__import__", side_effect=import_without_spacy):
            precise_results = run_all(modules, precise=True)

        for name, default_result in default_results.items():
            default_code, _, default_report = default_result
            precise_code, _, precise_report = precise_results[name]
            self.assertEqual(precise_code, default_code)
            self.assertEqual(
                precise_report["precise"],
                {"requested": True, "active": False, "reason": "spacy_missing"},
            )
            precise_without_meta = dict(precise_report)
            precise_without_meta.pop("precise")
            self.assertEqual(precise_without_meta, default_report)


@unittest.skipUnless(SPACY_MODEL_AVAILABLE, "spaCy German model is not available")
class PreciseFlagSpacyTests(unittest.TestCase):
    def test_precise_with_spacy_reports_active(self):
        results = run_all(load_linters(), precise=True)

        for _, _, report in results.values():
            self.assertEqual(report["precise"], {"requested": True, "active": True})


if __name__ == "__main__":
    unittest.main()
