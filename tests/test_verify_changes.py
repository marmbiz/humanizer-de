import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_changes.py"

spec = importlib.util.spec_from_file_location("verify_changes", SCRIPT)
verify_changes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_changes)


def run_files(before: str, after: str, output_format: str = "json"):
    with tempfile.TemporaryDirectory() as tmp:
        before_path = Path(tmp) / "before.md"
        after_path = Path(tmp) / "after.md"
        before_path.write_text(before, encoding="utf-8")
        after_path.write_text(after, encoding="utf-8")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = verify_changes.main(
                [
                    "--before-file",
                    str(before_path),
                    "--after-file",
                    str(after_path),
                    "--format",
                    output_format,
                ]
            )
    output = stdout.getvalue()
    return exit_code, json.loads(output) if output_format == "json" else output


class VerifyChangesTests(unittest.TestCase):
    def test_identical_files_have_no_changes(self):
        exit_code, report = run_files('Ein Satz mit „Zitat“ und Semikolon;\n', 'Ein Satz mit „Zitat“ und Semikolon;\n')

        self.assertEqual(exit_code, 0)
        self.assertTrue(report["identical"])
        self.assertEqual(report["tokens"]["changed_ratio"], 0.0)
        self.assertTrue(all(item["delta"] == 0 for item in report["typography"].values()))
        self.assertEqual(report["changed_lines"], {"count": 0, "pairs": []})

    def test_ascii_double_quote_replaced_with_u201c_is_counted(self):
        _, report = run_files('Vorher "Zitat.', "Vorher “Zitat.")

        self.assertEqual(report["typography"]['"']["delta"], -1)
        self.assertEqual(report["typography"]["“"]["delta"], 1)

    def test_inserted_em_dash_and_semicolon_are_counted(self):
        _, report = run_files("Ein Satz bleibt.", "Ein Satz — er bleibt; wirklich.")

        self.assertEqual(report["typography"]["—"]["delta"], 1)
        self.assertEqual(report["typography"][";"]["delta"], 1)

    def test_code_fence_only_change_does_not_change_prose_metrics(self):
        before = 'Prosa bleibt.\n\n```text\n"alt" -- ;\n```\n'
        after = "Prosa bleibt.\n\n```text\n“neu” — ;;\n```\n"
        _, report = run_files(before, after)

        self.assertFalse(report["identical"])
        self.assertEqual(report["tokens"]["changed_ratio"], 0.0)
        self.assertEqual(report["tokens"]["before"], report["tokens"]["after"])
        self.assertTrue(all(item["delta"] == 0 for item in report["typography"].values()))
        self.assertEqual(report["changed_lines"]["count"], 1)

    def test_changed_ratio_for_one_of_four_tokens(self):
        _, report = run_files("eins zwei drei vier", "eins zwei anders vier")

        self.assertEqual(report["tokens"]["replaced"], 1)
        self.assertEqual(report["tokens"]["inserted"], 0)
        self.assertEqual(report["tokens"]["deleted"], 0)
        self.assertEqual(report["tokens"]["changed_ratio"], 0.25)

    def test_markdown_contains_compact_core_lines(self):
        exit_code, output = run_files('Alt "Zitat.', "Neu “Zitat.", "md")

        self.assertEqual(exit_code, 0)
        self.assertIn("Identical: false", output)
        self.assertIn("Tokens:", output)
        self.assertIn("Typography:", output)
        self.assertIn("ChangedLines: 1 (showing 1)", output)
        self.assertIn("- Alt", output)
        self.assertIn("=> Neu", output)

    def test_missing_file_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "before.md"
            existing.write_text("Text", encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = verify_changes.main(
                    [
                        "--before-file",
                        str(existing),
                        "--after-file",
                        str(Path(tmp) / "missing.md"),
                    ]
                )

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("--after-file requires an existing file", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
