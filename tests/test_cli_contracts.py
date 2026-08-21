import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class CliContractTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def json_report(self, name: str, *args: str) -> dict | list:
        proc = self.run_script(name, *args)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def assert_usage_error(self, proc: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("error:", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def without_offsets_or_paths(self, value):
        if isinstance(value, dict):
            return {
                key: self.without_offsets_or_paths(item)
                for key, item in value.items()
                if key not in {"start", "end", "index", "file", "source"}
            }
        if isinstance(value, list):
            return [self.without_offsets_or_paths(item) for item in value]
        return value

    def test_explicit_empty_argv_never_reads_host_arguments(self):
        scripts = (
            "register_lint",
            "rhythm_lint",
            "evidence_lint",
            "unicode_lint",
            "style_profile",
            "doctor",
            "detection_snapshot",
            "fp_corpus_report",
            "run_review_eval",
            "german_pattern_lint",
            "humanizer_audit",
        )

        class Parsed(Exception):
            pass

        for name in scripts:
            with self.subTest(script=name):
                spec = importlib.util.spec_from_file_location(f"argv_{name}", SCRIPTS / f"{name}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                with mock.patch.object(module, "parse_args", side_effect=Parsed) as parse_args:
                    with mock.patch.object(sys, "argv", ["pytest", "-k", "something", "--tb=short"]):
                        with self.assertRaises(Parsed):
                            module.main([])
                parse_args.assert_called_once_with([])

    def test_text_linters_require_an_explicit_source(self):
        for name in ("register_lint.py", "german_pattern_lint.py", "syntax_lint.py"):
            with self.subTest(name=name):
                proc = self.run_script(name)
                self.assertEqual(proc.returncode, 2)
                self.assertIn("one of the arguments", proc.stderr)

    def test_spell_lint_requires_both_sides(self):
        no_input = self.run_script("spell_lint.py")
        before_only = self.run_script("spell_lint.py", "--before", "Alt")
        after_only = self.run_script("spell_lint.py", "--after", "Neu")

        self.assertEqual(no_input.returncode, 2)
        self.assertEqual(before_only.returncode, 2)
        self.assertEqual(after_only.returncode, 2)
        self.assertIn("--after", before_only.stderr)
        self.assertIn("--before", after_only.stderr)

    def test_fixture_linters_reject_empty_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("register_lint.py", "german_pattern_lint.py"):
                with self.subTest(name=name):
                    proc = self.run_script(name, "--fixture", tmp)
                    self.assertEqual(proc.returncode, 2)
                    self.assertIn("contains no JSON files", proc.stderr)

    def test_non_utf8_user_files_are_usage_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            latin1 = root / "latin1.md"
            latin1.write_bytes(b"Der Text ist sch\xf6n und gut.\n")
            corpus = root / "corpus"
            corpus.mkdir()
            (corpus / "latin1.md").write_bytes(latin1.read_bytes())
            commands = (
                ("register_lint.py", "--file", str(latin1)),
                ("rhythm_lint.py", "--file", str(latin1)),
                ("syntax_lint.py", "--file", str(latin1)),
                ("unicode_lint.py", "--file", str(latin1)),
                ("style_profile.py", "--file", str(latin1)),
                ("german_pattern_lint.py", "--file", str(latin1)),
                ("humanizer_audit.py", "--file", str(latin1)),
                (
                    "spell_lint.py",
                    "--before-file",
                    str(latin1),
                    "--after-file",
                    str(latin1),
                ),
                (
                    "evidence_lint.py",
                    "--before-file",
                    str(latin1),
                    "--after-file",
                    str(latin1),
                ),
                ("fp_corpus_report.py", "--corpus-dir", str(corpus)),
            )

            for command in commands:
                with self.subTest(script=command[0]):
                    self.assert_usage_error(self.run_script(*command))

    def test_missing_and_directory_file_arguments_are_usage_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = str(Path(tmp) / "missing.md")
            for value in (missing, tmp):
                commands = (
                    ("register_lint.py", "--file", value),
                    ("rhythm_lint.py", "--file", value),
                    ("syntax_lint.py", "--file", value),
                    ("unicode_lint.py", "--file", value),
                    ("style_profile.py", "--file", value),
                    ("german_pattern_lint.py", "--file", value),
                    ("humanizer_audit.py", "--file", value),
                )
                for command in commands:
                    with self.subTest(script=command[0], value=value):
                        self.assert_usage_error(self.run_script(*command))

    def test_malformed_fixture_json_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "malformed.json"
            fixture.write_text("{", encoding="utf-8")
            for name in ("register_lint.py", "german_pattern_lint.py", "evidence_lint.py"):
                with self.subTest(script=name):
                    self.assert_usage_error(self.run_script(name, "--fixture", str(fixture)))

    def test_fixture_entry_missing_text_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "missing-text.json"
            fixture.write_text("{}", encoding="utf-8")
            for name in ("register_lint.py", "german_pattern_lint.py"):
                with self.subTest(script=name):
                    self.assert_usage_error(self.run_script(name, "--fixture", str(fixture)))

    def test_genuine_fixture_expectation_mismatch_exits_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "mismatch.json"
            fixture.write_text(
                json.dumps({"text": "Ein kurzer Text.", "expect_kinds": ["mixed_address"]}),
                encoding="utf-8",
            )
            proc = self.run_script("register_lint.py", "--fixture", str(fixture))

        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertNotIn("error:", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_crlf_fixture_spans_round_trip_against_raw_text(self):
        raw = "Hallo Leser.\r\nHier sprichst du mit uns.\r\nDann kommen Sie vorbei.\r\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "crlf.md"
            path.write_bytes(raw.encode("utf-8"))
            report = self.json_report(
                "register_lint.py", "--file", str(path), "--fail-on", "never"
            )

        finding = next(item for item in report["findings"] if item["kind"] == "mixed_address")
        slices = [raw[span["start"]:span["end"]] for span in finding["spans"]]
        self.assertEqual(slices, ["du", "Sie"])

    def test_lf_and_crlf_user_text_reports_match_except_offsets(self):
        lf_text = """---
title: "Geschützt"
---

Hallo Leser.
Hier sprichst du mit uns.
Dann kommen Sie vorbei.

Kein Plan,
kein Ziel.
Das ist nicht Wert 1,
sondern Wirkung 1.
Das ist nicht Wert 2,
sondern Wirkung 2.
Das ist nicht Wert 3,
sondern Wirkung 3.
Das ist nicht Wert 4,
sondern Wirkung 4.
Du bist
nicht sensibel.

**Wichtig** und **Dringend** und **Sicher** und **Klar** und **Einfach**.
| Feld | "geschützt" |
<p class="intro">Diese Zeile ist technisch.</p>

Die Auswertung wird
von uns geprüft. Er sagte "Hallo".
"""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            lf_path = tmp_path / "lf.md"
            crlf_path = tmp_path / "crlf.md"
            lf_path.write_bytes(lf_text.encode("utf-8"))
            crlf_path.write_bytes(lf_text.replace("\n", "\r\n").encode("utf-8"))

            lf_corpus = tmp_path / "lf-corpus"
            crlf_corpus = tmp_path / "crlf-corpus"
            lf_corpus.mkdir()
            crlf_corpus.mkdir()
            (lf_corpus / "sample.md").write_bytes(lf_text.encode("utf-8"))
            (crlf_corpus / "sample.md").write_bytes(
                lf_text.replace("\n", "\r\n").encode("utf-8")
            )

            commands = (
                ("register_lint.py", "--file", "{path}", "--fail-on", "never"),
                ("german_pattern_lint.py", "--file", "{path}"),
                ("rhythm_lint.py", "--file", "{path}"),
                ("style_profile.py", "--file", "{path}"),
                ("syntax_lint.py", "--file", "{path}"),
                ("unicode_lint.py", "--file", "{path}", "--fail-on", "never"),
                ("humanizer_audit.py", "--file", "{path}", "--precise"),
                (
                    "evidence_lint.py",
                    "--before-file",
                    "{path}",
                    "--after-file",
                    "{path}",
                    "--fail-on",
                    "never",
                ),
                ("spell_lint.py", "--before-file", "{path}", "--after-file", "{path}"),
                ("fp_corpus_report.py", "--corpus-dir", "{corpus}"),
            )

            for command in commands:
                with self.subTest(script=command[0]):
                    lf_args = [arg.format(path=lf_path, corpus=lf_corpus) for arg in command]
                    crlf_args = [
                        arg.format(path=crlf_path, corpus=crlf_corpus) for arg in command
                    ]
                    lf_report = self.json_report(*lf_args)
                    crlf_report = self.json_report(*crlf_args)
                    self.assertEqual(
                        self.without_offsets_or_paths(lf_report),
                        self.without_offsets_or_paths(crlf_report),
                    )


if __name__ == "__main__":
    unittest.main()
