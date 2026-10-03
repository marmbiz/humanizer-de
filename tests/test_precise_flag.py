import builtins
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lint
import german_pattern_lint
import humanizer_audit
import register_lint
import syntax_lint

LINTERS = {
    "register": register_lint,
    "german_pattern": german_pattern_lint,
    "evidence": evidence_lint,
}

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
      "message": "Possible Du/Sie address mix; verify that capitalized forms are direct address, not anaphora or quoted voice.",
      "spans": [
        {
          "start": 0,
          "end": 2
        },
        {
          "start": 74,
          "end": 77
        }
      ]
    },
    {
      "severity": "blocker",
      "kind": "unexpected_sie",
      "message": "Profile expects du-address, but formal Sie appears.",
      "spans": [
        {
          "start": 74,
          "end": 77
        }
      ]
    },
    {
      "severity": "warning",
      "kind": "particles_outside_locker",
      "message": "Modal particles should not be added in Sachlich/Formal.",
      "spans": [
        {
          "start": 155,
          "end": 157
        }
      ]
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
      },
      "spans": [
        {
          "start": 14,
          "end": 31
        },
        {
          "start": 41,
          "end": 48
        },
        {
          "start": 49,
          "end": 59
        }
      ]
    },
    {
      "pattern": 65,
      "kind": "copula_avoidance_cluster",
      "severity": "warning",
      "evidence": {
        "fungiert als": 1,
        "dient als": 1
      },
      "spans": [
        {
          "start": 100,
          "end": 112
        },
        {
          "start": 127,
          "end": 136
        }
      ]
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
      },
      "spans": [
        {
          "start": 32,
          "end": 40
        },
        {
          "start": 167,
          "end": 176
        },
        {
          "start": 178,
          "end": 185
        },
        {
          "start": 190,
          "end": 198
        }
      ]
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


def run_cli(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = module.main(argv)
    return exit_code, stdout.getvalue(), json.loads(stdout.getvalue())


def run_all(precise=False):
    flag = ["--precise"] if precise else []
    return {
        "register": run_cli(
            LINTERS["register"],
            ["--text", TEXT, "--mode", "sachlich", "--expected-address", "du", *flag],
        ),
        "german_pattern": run_cli(
            LINTERS["german_pattern"],
            ["--text", TEXT, "--mode", "sachlich", *flag],
        ),
        "evidence": run_cli(
            LINTERS["evidence"],
            ["--before", BEFORE, "--after", AFTER, *flag],
        ),
    }


SPACY_MODEL_AVAILABLE = (
    importlib.util.find_spec("spacy") is not None
    and importlib.util.find_spec("de_core_news_sm") is not None
)


class PreciseFlagSnapshotTests(unittest.TestCase):
    def test_default_path_does_not_import_spacy(self):
        result = subprocess.run(
            [sys.executable, "-c", """
import builtins
attempts = []
original_import = builtins.__import__

def without_spacy(name, *args, **kwargs):
    if name == 'spacy' or name.startswith('spacy.'):
        attempts.append(name)
        raise ModuleNotFoundError(name)
    return original_import(name, *args, **kwargs)

builtins.__import__ = without_spacy
import evidence_lint, german_pattern_lint, register_lint, syntax_lint
evidence_lint.lint('Der Text bleibt.', 'Der Text bleibt.')
german_pattern_lint.lint('Der Text bleibt.')
register_lint.lint('Der Text bleibt.')
assert not attempts, attempts
"""],
            cwd=SCRIPTS,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_reports_without_flag_match_snapshots(self):
        results = run_all()

        self.assertEqual(results["register"][0], 1)
        self.assertEqual(results["register"][1], EXPECTED_REGISTER_JSON)
        self.assertEqual(results["german_pattern"][0], 0)
        self.assertEqual(results["german_pattern"][1], EXPECTED_GERMAN_PATTERN_JSON)
        self.assertEqual(results["evidence"][0], 1)
        self.assertEqual(results["evidence"][1], EXPECTED_EVIDENCE_JSON)


class PreciseFlagMissingSpacyTests(unittest.TestCase):
    def test_precise_without_spacy_reports_inactive_and_keeps_findings(self):
        syntax_lint._precise_nlp.cache_clear()
        self.addCleanup(syntax_lint._precise_nlp.cache_clear)
        default_results = run_all()

        real_import = builtins.__import__

        def import_without_spacy(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "spacy" or name.startswith("spacy."):
                raise ModuleNotFoundError("No module named 'spacy'")
            return real_import(name, globals, locals, fromlist, level)

        with mock.patch("builtins.__import__", side_effect=import_without_spacy):
            precise_results = run_all(precise=True)

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
    def test_precise_linters_and_audit_share_one_model_load(self):
        syntax_lint._precise_nlp.cache_clear()
        self.addCleanup(syntax_lint._precise_nlp.cache_clear)
        with mock.patch.object(syntax_lint, "load_nlp", wraps=syntax_lint.load_nlp) as load_nlp:
            results = run_all(precise=True)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "text.md"
                path.write_text(TEXT, encoding="utf-8")
                audit = humanizer_audit.analyze_file(path, "sachlich", precise=True)

        for _, _, report in results.values():
            self.assertEqual(report["precise"], {"requested": True, "active": True})
        self.assertTrue(audit["syntax"]["available"])
        load_nlp.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
