import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "humanizer_two_pass.py"
SPEC = importlib.util.spec_from_file_location("humanizer_two_pass", SCRIPT)
two_pass = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(two_pass)


class HumanizerTwoPassTests(unittest.TestCase):
    def test_confirmation_only_discards_candidates_touching_quotes_or_persona(self):
        original = "Echt. Regional. Fakt 42 bleibt. Dynamisch und nahtlos."
        ledger = {
            "register": "sachlich",
            "candidates": [
                {"id": "c1", "source": "Echt.", "patterns": ["9"], "reason": "Form", "goal": "glätten", "action": "rewrite", "scope": "sentence"},
                {"id": "c2", "source": "Fakt 42 bleibt.", "patterns": ["64"], "reason": "Form", "goal": "glätten", "action": "rewrite", "scope": "sentence"},
                {"id": "c3", "source": "Dynamisch und nahtlos.", "patterns": ["64"], "reason": "Floskel", "goal": "konkret", "action": "rewrite", "scope": "sentence"},
            ],
            "protected": {
                "facts": ["42"],
                "quotes": [],
                "terms": [],
                "persona": ["Echt."],
            },
        }

        confirmed = two_pass.confirm_ledger(original, ledger)

        self.assertEqual([item["id"] for item in confirmed["candidates"]], ["c2", "c3"])
        self.assertEqual(
            confirmed["discarded_candidates"],
            [{"id": "c1", "reason": "overlaps_protected_anchor"}],
        )
        result = two_pass.apply_edits(
            original,
            confirmed,
            {
                "edits": [
                    {"candidate_id": "c2", "replacement": "Fakt 42 bleibt."},
                    {"candidate_id": "c3", "replacement": "Konkret."},
                ]
            },
        )
        self.assertEqual(result, "Echt. Regional. Fakt 42 bleibt. Konkret.")
        self.assertEqual(two_pass.protected_violations(original, result, confirmed), [])
        with self.assertRaisesRegex(ValueError, "changed owned facts anchor"):
            two_pass.apply_edits(
                original,
                confirmed,
                {"edits": [{"candidate_id": "c2", "replacement": "Fakt bleibt."}]},
            )

    def test_protected_anchor_order_cannot_change(self):
        ledger = {
            "protected": {"facts": ["Alice", "Bob"], "quotes": [], "terms": [], "persona": []}
        }

        self.assertEqual(
            two_pass.protected_violations("Alice folgt Bob.", "Bob folgt Alice.", ledger),
            ["protected anchor order changed"],
        )
        self.assertEqual(
            two_pass.protected_violations(
                "Alice Bob Alice Bob",
                "Alice Alice Bob Bob",
                ledger,
            ),
            ["protected anchor order changed"],
        )
        self.assertEqual(
            two_pass.protected_violations(
                "Das Enzympräparat hilft.",
                "Die Enzympräparate helfen.",
                {"protected": {"facts": [], "quotes": [], "terms": ["Enzympräparat"], "persona": []}},
            ),
            ["terms: anchor count changed: 'Enzympräparat'"],
        )

    def test_candidate_contract_rejects_ambiguous_overlap_and_unknown_edits(self):
        candidate = {"id": "c1", "source": "aa", "patterns": ["9"], "reason": "Form", "goal": "ändern", "action": "rewrite", "scope": "phrase"}
        with self.assertRaisesRegex(ValueError, "exactly once"):
            two_pass.candidate_spans("aaa", [candidate])
        with self.assertRaisesRegex(ValueError, "exactly once"):
            two_pass.candidate_spans("Smartphone", [{**candidate, "source": "Smart"}])

        overlapping = [
            {"id": "c1", "source": "(abc)", "patterns": ["9"], "reason": "Form", "goal": "ändern", "action": "rewrite", "scope": "phrase"},
            {"id": "c2", "source": "abc", "patterns": ["9"], "reason": "Form", "goal": "ändern", "action": "rewrite", "scope": "phrase"},
        ]
        with self.assertRaisesRegex(ValueError, "overlapping"):
            two_pass.candidate_spans("(abc)", overlapping)

        ledger = {"candidates": [], "protected": {"facts": [], "quotes": [], "terms": [], "persona": []}}
        with self.assertRaisesRegex(ValueError, "unknown candidate"):
            two_pass.apply_edits("Text.", ledger, {"edits": [{"candidate_id": "c9", "replacement": "Neu."}]})

    def test_confirmation_rejects_descriptive_protection_anchor(self):
        ledger = {
            "register": "locker",
            "candidates": [],
            "protected": {
                "facts": [],
                "quotes": [],
                "terms": [],
                "persona": ["Wir-Erzählstimme des Familienbetriebs"],
            },
        }

        with self.assertRaisesRegex(ValueError, "anchor missing from original"):
            two_pass.confirm_ledger("Wir backen seit drei Generationen.", ledger)

    def test_confirmation_discards_invalid_multisentence_candidate_only(self):
        invalid = {
            "id": "c1",
            "source": "Ganz einfach. Ganz schnell. Ganz ohne ELSTER.",
            "action": "delete",
            "scope": "sentence",
        }
        valid = {
            "id": "c2",
            "source": "smarte",
            "action": "delete",
            "scope": "phrase",
        }
        confirmed = two_pass.confirm_ledger(
            "Ganz einfach. Ganz schnell. Ganz ohne ELSTER. Die smarte Lösung.",
            {
                "register": "sachlich",
                "candidates": [invalid, valid],
                "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
            },
        )

        self.assertEqual(confirmed["candidates"], [valid])
        self.assertEqual(
            confirmed["discarded_candidates"],
            [{"id": "c1", "reason": "invalid_candidate_contract"}],
        )

    def test_empty_replacement_does_not_leave_double_space(self):
        ledger = {
            "candidates": [
                {"id": "c1", "source": "smarte", "patterns": ["2"], "reason": "Floskel", "goal": "streichen", "action": "delete", "scope": "phrase"}
            ]
        }

        result = two_pass.apply_edits(
            "Die smarte Lösung.", ledger, {"edits": [{"candidate_id": "c1", "replacement": ""}]}
        )

        self.assertEqual(result, "Die Lösung.")
        self.assertEqual(
            two_pass.apply_edits(
                "Die App synchronisiert nahtlos.",
                {"candidates": [{**ledger["candidates"][0], "source": "nahtlos"}]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "Die App synchronisiert.",
        )

        heading = {**ledger["candidates"][0], "source": "Werbezeile\n", "scope": "heading"}
        self.assertEqual(
            two_pass.apply_edits(
                "Absatz.\n\nWerbezeile\n\nWeiter.\n",
                {"candidates": [heading]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "Absatz.\n\nWeiter.\n",
        )
        crlf_heading = {**heading, "source": "Werbezeile\r\n"}
        self.assertEqual(
            two_pass.apply_edits(
                "Absatz.\r\n\r\nWerbezeile\r\n\r\nWeiter.\r\n",
                {"candidates": [crlf_heading]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "Absatz.\r\n\r\nWeiter.\r\n",
        )

        sentence = {**heading, "source": "Werbung.", "scope": "sentence"}
        self.assertEqual(
            two_pass.apply_edits(
                "Sachlich. Werbung.\n",
                {"candidates": [sentence]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "Sachlich.\n",
        )
        self.assertEqual(
            two_pass.apply_edits(
                "A.\n\nWerbung.\n\nB.\n",
                {"candidates": [sentence]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "A.\n\nB.\n",
        )

        self.assertEqual(
            two_pass.apply_edits(
                "Werbung.\n\nSachlich.\n",
                {"candidates": [sentence]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "Sachlich.\n",
        )
        self.assertEqual(
            two_pass.apply_edits(
                "Werbung.\n\n    code block\n",
                {"candidates": [sentence]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "    code block\n",
        )
        sentence_with_newline = {**sentence, "source": "Werbung.\n"}
        self.assertEqual(
            two_pass.apply_edits(
                "Werbung.\n    if x:\n",
                {"candidates": [sentence_with_newline]},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            ),
            "    if x:\n",
        )
        adjective = {**ledger["candidates"][0], "id": "c2"}
        self.assertEqual(
            two_pass.apply_edits(
                "Werbung.\n    if x: smarte Lösung\n",
                {"candidates": [sentence_with_newline, adjective]},
                {
                    "edits": [
                        {"candidate_id": "c1", "replacement": ""},
                        {"candidate_id": "c2", "replacement": ""},
                    ]
                },
            ),
            "    if x: Lösung\n",
        )

    def test_rewrite_candidate_requires_nonempty_replacement(self):
        candidate = {
            "id": "c1",
            "source": "Dynamisch.",
            "patterns": ["2"],
            "reason": "Floskel",
            "goal": "konkretisieren",
            "action": "rewrite",
            "scope": "sentence",
        }

        with self.assertRaisesRegex(ValueError, "empty replacement"):
            two_pass.apply_edits(
                "Dynamisch.",
                {"candidates": [candidate], "protected": {}},
                {"edits": [{"candidate_id": "c1", "replacement": ""}]},
            )
        for replacement in (
            "Konkret",
            "Konkret.\n# Neu",
            "# Neu.",
            "- Konkret.",
            "> Konkret.",
            "1. Konkret.",
            "    Konkret.",
        ):
            with self.assertRaisesRegex(ValueError, "line structure"):
                two_pass.apply_edits(
                    "Dynamisch.",
                    {"candidates": [candidate], "protected": {}},
                    {"edits": [{"candidate_id": "c1", "replacement": replacement}]},
                )

        heading = {**candidate, "source": "Dynamisch\n", "scope": "heading"}
        with self.assertRaisesRegex(ValueError, "line structure"):
            two_pass.apply_edits(
                "Dynamisch\nFolgezeile.\n",
                {"candidates": [heading], "protected": {}},
                {"edits": [{"candidate_id": "c1", "replacement": "Konkret"}]},
            )
        for replacement in ("Erste Zeile\nZweite Zeile\n", "Konkret\r\n"):
            with self.assertRaisesRegex(ValueError, "line structure"):
                two_pass.apply_edits(
                    "Dynamisch\nFolgezeile.\n",
                    {"candidates": [heading], "protected": {}},
                    {"edits": [{"candidate_id": "c1", "replacement": replacement}]},
                )

        phrase = {**candidate, "source": "die intelligente App.", "scope": "phrase"}
        phrase_ledger = {
            "candidates": [phrase],
            "protected": {"facts": [], "terms": []},
        }
        for replacement in ("die App", "die App!"):
            with self.assertRaisesRegex(ValueError, "line structure"):
                two_pass.apply_edits(
                    "Das ist: die intelligente App.",
                    phrase_ledger,
                    {"edits": [{"candidate_id": "c1", "replacement": replacement}]},
                )
        self.assertEqual(
            two_pass.apply_edits(
                "Das ist: die intelligente App.",
                phrase_ledger,
                {"edits": [{"candidate_id": "c1", "replacement": "die App."}]},
            ),
            "Das ist: die App.",
        )
        markdown_heading = {**heading, "source": "# Dynamisch\n"}
        with self.assertRaisesRegex(ValueError, "line structure"):
            two_pass.apply_edits(
                "# Dynamisch\nFolgezeile.\n",
                {"candidates": [markdown_heading], "protected": {}},
                {"edits": [{"candidate_id": "c1", "replacement": "Konkret\n"}]},
            )
        plain_heading = {**heading, "source": "Dynamisch\n"}
        for replacement in ("### Konkret\n", "- Konkret\n", "---\n"):
            with self.assertRaisesRegex(ValueError, "line structure"):
                two_pass.apply_edits(
                    "Dynamisch\nFolgezeile.\n",
                    {"candidates": [plain_heading], "protected": {}},
                    {"edits": [{"candidate_id": "c1", "replacement": replacement}]},
                )

    def test_structural_scope_and_delete_policy_block_relabeling(self):
        heading = {
            "id": "c1",
            "source": "die richtige Wahl ist",
            "patterns": ["2"],
            "reason": "generische Überschrift",
            "goal": "streichen",
            "action": "delete",
            "scope": "heading",
        }
        with self.assertRaisesRegex(ValueError, "complete line"):
            two_pass.candidate_spans("Warum X die richtige Wahl ist\nInhalt.", [heading])

        sentence = {**heading, "source": "können nicht irren.", "scope": "sentence"}
        with self.assertRaisesRegex(ValueError, "complete sentence"):
            two_pass.candidate_spans("3.400 Betriebe können nicht irren.", [sentence])
        abbreviation_fragment = {**heading, "source": "eine smarte Lösung.", "scope": "sentence"}
        with self.assertRaisesRegex(ValueError, "complete sentence"):
            two_pass.candidate_spans("Das ist z. B. eine smarte Lösung.", [abbreviation_fragment])
        multiple_sentences = {**heading, "source": "Werbung. Noch mehr Werbung.", "scope": "sentence"}
        with self.assertRaisesRegex(ValueError, "complete sentence"):
            two_pass.candidate_spans("Werbung. Noch mehr Werbung.", [multiple_sentences])
        after_quote = {**heading, "source": "Danach geht es weiter.", "scope": "sentence"}
        self.assertEqual(
            two_pass.candidate_spans("Er sagt: „So ist es.“ Danach geht es weiter.", [after_quote])["c1"][:2],
            (len("Er sagt: „So ist es.“ "), len("Er sagt: „So ist es.“ Danach geht es weiter.")),
        )

        list_sentence = {**heading, "source": "Werbung.", "scope": "sentence"}
        with self.assertRaisesRegex(ValueError, "complete sentence"):
            two_pass.candidate_spans("1. Werbung.\n", [list_sentence])
        markdown_heading = {**heading, "source": "# Warum X?", "scope": "sentence"}
        with self.assertRaisesRegex(ValueError, "complete sentence"):
            two_pass.candidate_spans("# Warum X?\nInhalt.\n", [markdown_heading])
        full_list_item = {**heading, "source": "- Werbung.\n", "action": "rewrite", "scope": "sentence"}
        self.assertEqual(
            two_pass.candidate_spans("- Werbung.\n- Weiter.\n", [full_list_item])["c1"][:2],
            (0, len("- Werbung.\n")),
        )
        with self.assertRaisesRegex(ValueError, "line structure"):
            two_pass.apply_edits(
                "- Werbung.\n- Weiter.\n",
                {"candidates": [full_list_item], "protected": {}},
                {"edits": [{"candidate_id": "c1", "replacement": "Sachlich."}]},
            )

        full_heading = {**heading, "source": "Warum X die richtige Wahl ist\n"}
        ledger = {
            "candidates": [full_heading],
            "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
        }
        with self.assertRaisesRegex(ValueError, "delete-only"):
            two_pass.apply_edits(
                "Warum X die richtige Wahl ist\nInhalt.",
                ledger,
                {"edits": [{"candidate_id": "c1", "replacement": "Warum X passt\n"}]},
            )

        partial = {
            **heading,
            "source": "Über 42 Betriebe vertrauen bereits",
            "action": "rewrite",
            "scope": "phrase",
        }
        confirmed = two_pass.confirm_ledger(
            "Über 42 Betriebe vertrauen bereits auf X.",
            {
                "register": "sachlich",
                "candidates": [partial],
                "protected": {"facts": ["42"], "quotes": [], "terms": [], "persona": []},
            },
        )
        self.assertEqual(confirmed["candidates"], [])
        self.assertEqual(confirmed["discarded_candidates"][0]["reason"], "partial_structural_unit")

        for original, source in (
            ("Warum RechnungsHeld die Wahl ist\n", "die Wahl ist"),
            ("## Warum RechnungsHeld?\n", "RechnungsHeld"),
            ("Über 3.400 Betriebe können nicht irren.\n", "können nicht irren"),
        ):
            interior = {**partial, "source": source}
            confirmed = two_pass.confirm_ledger(
                original,
                {
                    "register": "sachlich",
                    "candidates": [interior],
                    "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
                },
            )
            self.assertEqual(confirmed["candidates"], [])
            self.assertEqual(confirmed["discarded_candidates"][0]["reason"], "partial_structural_unit")

        for original, source in (
            ("Er sagt: „So ist es.“ Smarte Lösung.", "Smarte"),
            ("- Smarte Lösung.\n", "Smarte"),
            ("> Smarte Lösung.\n", "Smarte"),
        ):
            sentence_start = {**partial, "source": source}
            confirmed = two_pass.confirm_ledger(
                original,
                {
                    "register": "sachlich",
                    "candidates": [sentence_start],
                    "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
                },
            )
            self.assertEqual(confirmed["candidates"], [])

        bounded = {**partial, "source": "die intelligente App, die viel tut."}
        confirmed = two_pass.confirm_ledger(
            "Konkret heißt das: die intelligente App, die viel tut.",
            {
                "register": "sachlich",
                "candidates": [bounded],
                "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
            },
        )
        self.assertEqual(confirmed["candidates"], [bounded])

        for original, source in (
            ("Die Lösung ist schnell, smart, sicher.", "smart"),
            ("Die Lösung ist **smart**.", "smart"),
        ):
            skeleton = {**partial, "source": source, "action": "delete"}
            confirmed = two_pass.confirm_ledger(
                original,
                {
                    "register": "sachlich",
                    "candidates": [skeleton],
                    "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
                },
            )
            self.assertEqual(confirmed["candidates"], [])
            self.assertEqual(confirmed["discarded_candidates"][0]["reason"], "partial_structural_unit")

    def test_delete_cannot_remove_unique_fact_but_may_remove_duplicate(self):
        candidate = {
            "id": "c1",
            "source": "Fakt 42.\n",
            "patterns": ["2"],
            "reason": "Schablone",
            "goal": "streichen",
            "action": "delete",
            "scope": "heading",
        }
        ledger = {
            "register": "sachlich",
            "candidates": [candidate],
            "protected": {"facts": ["42"], "quotes": [], "terms": [], "persona": []},
        }
        confirmed = two_pass.confirm_ledger("Fakt 42.\nInhalt.", ledger)
        self.assertEqual(confirmed["candidates"], [])
        self.assertEqual(confirmed["discarded_candidates"][0]["reason"], "deletes_unique_protected_anchor")

        duplicate = two_pass.confirm_ledger("Fakt 42.\nNoch einmal 42.", ledger)
        self.assertEqual(duplicate["candidates"], [candidate])
        self.assertEqual(two_pass.protected_violations("42 und 42", "42", ledger), [])
        self.assertTrue(two_pass.protected_violations("42", "42 und 42", ledger))

    def test_rewrite_cannot_relocate_anchor_removed_by_another_edit(self):
        original = "Floskel 42. Fakt 42. Unklar."
        ledger = {
            "candidates": [
                {"id": "c1", "source": "Floskel 42.", "action": "delete", "scope": "sentence"},
                {"id": "c2", "source": "Unklar.", "action": "rewrite", "scope": "sentence"},
            ],
            "protected": {"facts": ["42"], "quotes": [], "terms": [], "persona": []},
        }

        with self.assertRaisesRegex(ValueError, "changed owned facts anchor"):
            two_pass.apply_edits(
                original,
                ledger,
                {
                    "edits": [
                        {"candidate_id": "c1", "replacement": ""},
                        {"candidate_id": "c2", "replacement": "42 Konkret."},
                    ]
                },
            )

    def test_main_uses_two_fresh_calls_and_only_applies_confirmed_candidate(self):
        audit = {
            "register": "sachlich",
            "candidates": [
                {
                    "id": "c1",
                    "source": "smarte",
                    "patterns": ["2"],
                    "reason": "Floskel",
                    "goal": "streichen",
                    "action": "delete",
                    "scope": "phrase",
                }
            ],
            "advisories": [{"source": "Lösung", "reason": "Quelle nicht verifiziert"}],
            "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
        }
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            source = temp / "source.md"
            out = temp / "out"
            source.write_text("Die smarte Lösung.\n", encoding="utf-8")
            with (
                mock.patch.object(
                    two_pass,
                    "run_model",
                    side_effect=[(audit, None), ({"edits": [{"candidate_id": "c1", "replacement": ""}]}, None)],
                ) as run,
                mock.patch.object(
                    two_pass, "deterministic_audit", return_value={"preflight": {}, "findings": []}
                ),
                mock.patch.object(two_pass, "evidence_gate", return_value=[]),
                mock.patch("builtins.print"),
            ):
                code = two_pass.main(
                    ["--file", str(source), "--out-dir", str(out)]
                )

            self.assertEqual(code, 0)
            self.assertEqual(run.call_count, 2)
            self.assertNotEqual(run.call_args_list[0].kwargs["cwd"], run.call_args_list[1].kwargs["cwd"])
            self.assertIn("BESTÄTIGTES LEDGER", run.call_args_list[1].args[0])
            self.assertEqual((out / "result.md").read_text(encoding="utf-8"), "Die Lösung.\n")
            diff = (out / "changes.diff").read_text(encoding="utf-8")
            self.assertIn("--- original.md", diff)
            self.assertIn("+++ result.md", diff)
            self.assertIn("-Die smarte Lösung.", diff)
            self.assertIn("+Die Lösung.", diff)
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            verification = json.loads((out / "verify.json").read_text(encoding="utf-8"))
            self.assertEqual(report["advisory_count"], 1)
            self.assertEqual(report["advisories"], audit["advisories"])
            self.assertEqual(report["verification"]["identical"], verification["identical"])
            self.assertEqual(
                report["verification"]["changed_ratio"], verification["tokens"]["changed_ratio"]
            )

    def test_main_normalizes_before_freezing_protected_anchors(self):
        original = 'Er sagt „Wort".\n'
        normalized = "Er sagt „Wort“.\n"
        audit = {
            "register": "sachlich",
            "candidates": [],
            "advisories": [],
            "protected": {"facts": [], "quotes": ["„Wort“"], "terms": [], "persona": []},
        }
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            source = temp / "source.md"
            out = temp / "out"
            source.write_text(original, encoding="utf-8")

            def deterministic_audit(path, _mode):
                self.assertEqual(path, out / "normalized.md")
                self.assertEqual(path.read_text(encoding="utf-8"), normalized)
                return {"preflight": {}, "findings": []}

            def evidence_gate(before, _after, _out):
                self.assertEqual(before, out / "normalized.md")
                self.assertEqual(before.read_text(encoding="utf-8"), normalized)
                return []

            with (
                mock.patch.object(two_pass, "run_model", return_value=(audit, None)) as run,
                mock.patch.object(two_pass, "deterministic_audit", side_effect=deterministic_audit),
                mock.patch.object(two_pass, "evidence_gate", side_effect=evidence_gate),
                mock.patch("builtins.print"),
            ):
                code = two_pass.main(["--file", str(source), "--out-dir", str(out)])

            self.assertEqual(code, 0)
            self.assertIn(normalized, run.call_args.args[0])
            self.assertEqual((out / "original.md").read_text(encoding="utf-8"), original)
            self.assertEqual((out / "normalized.md").read_text(encoding="utf-8"), normalized)
            self.assertEqual((out / "result.md").read_text(encoding="utf-8"), normalized)
            diff = (out / "changes.diff").read_text(encoding="utf-8")
            self.assertIn('-Er sagt „Wort".', diff)
            self.assertIn('+Er sagt „Wort“.', diff)
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(
                report["unicode_fix"],
                {
                    "changed": True,
                    "sha256_before": two_pass.hashlib.sha256(original.encode()).hexdigest(),
                    "sha256_after": two_pass.hashlib.sha256(normalized.encode()).hexdigest(),
                },
            )
            self.assertEqual(report["protected_violations"], [])
            self.assertEqual(report["verification"]["typography"], {'"': -1, "“": 1})

    def test_model_calls_disable_tools(self):
        envelope = json.dumps(
            {"subtype": "success", "structured_output": {}, "total_cost_usd": 0.01}
        )
        completed = mock.Mock(stdout=envelope, stderr="", returncode=0)
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            with (
                mock.patch.object(two_pass.shutil, "which", return_value="/bin/claude"),
                mock.patch.object(two_pass.subprocess, "run", return_value=completed) as run,
            ):
                two_pass.run_model(
                    "prompt",
                    {"type": "object"},
                    model=None,
                    timeout=1,
                    cwd=temp,
                    raw_path=temp / "raw.json",
                    max_budget_usd=None,
                )

        command = run.call_args.args[0]
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertNotIn("--add-dir", command)

    def test_codex_model_is_ephemeral_read_only_and_rejects_tool_use(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            codex_home = temp / "source-codex-home"
            legacy_skill = codex_home / "skills" / "humanizer-de" / "SKILL.md"
            nested_skill = codex_home / "skills" / "humanizer-de" / "skills" / "humanizer-de" / "SKILL.md"
            legacy_skill.parent.mkdir(parents=True)
            nested_skill.parent.mkdir(parents=True)
            legacy_skill.touch()
            nested_skill.touch()
            (codex_home / "auth.json").write_text("secret", encoding="utf-8")
            user_home = temp / "user"
            recommended_skill = user_home / ".agents" / "skills" / "humanizer-de" / "SKILL.md"
            recommended_skill.parent.mkdir(parents=True)
            recommended_skill.touch()

            def completed(command, **_kwargs):
                response = Path(command[command.index("--output-last-message") + 1])
                response.write_text('{"edits": []}\n', encoding="utf-8")
                events = [
                    {"type": "item.completed", "item": {"type": "agent_message", "text": "{}"}},
                    {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}},
                ]
                return mock.Mock(
                    stdout="\n".join(json.dumps(event) for event in events),
                    stderr="",
                    returncode=0,
                )

            with (
                mock.patch.object(two_pass.shutil, "which", return_value="/bin/codex"),
                mock.patch.object(two_pass.subprocess, "run", side_effect=completed) as run,
                mock.patch.object(two_pass.Path, "home", return_value=user_home),
                mock.patch.dict(two_pass.os.environ, {"CODEX_HOME": str(codex_home)}),
            ):
                result, cost = two_pass.run_model(
                    "prompt",
                    two_pass.EDIT_SCHEMA,
                    model=None,
                    timeout=1,
                    cwd=temp,
                    raw_path=temp / "raw.json",
                    max_budget_usd=None,
                    provider="codex",
                )

            command = run.call_args.args[0]
            self.assertEqual(result, {"edits": []})
            self.assertIsNone(cost)
            self.assertIn("--ephemeral", command)
            self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
            self.assertIn("--ignore-user-config", command)
            self.assertIn("--ignore-rules", command)
            self.assertIn("project_doc_max_bytes=0", command)
            self.assertIn('cli_auth_credentials_store="file"', command)
            disabled = [command[index + 1] for index, value in enumerate(command) if value == "--disable"]
            self.assertEqual(
                disabled,
                [
                    "plugins",
                    "shell_tool",
                    "unified_exec",
                    "skill_search",
                    "tool_suggest",
                    "apps",
                    "browser_use",
                    "computer_use",
                    "image_generation",
                    "multi_agent",
                    "multi_agent_v2",
                    "hooks",
                ],
            )
            self.assertIn('web_search="disabled"', command)
            self.assertIn("tools.view_image=false", command)
            skill_config = next(value for value in command if value.startswith("skills.config="))
            for skill in (legacy_skill, nested_skill, recommended_skill):
                self.assertIn(json.dumps(str(skill)), skill_config)
            self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)

            tool_event = mock.Mock(
                stdout=json.dumps(
                    {"type": "item.completed", "item": {"type": "command_execution", "command": "ls"}}
                ),
                stderr="",
                returncode=0,
            )
            with (
                mock.patch.object(two_pass.shutil, "which", return_value="/bin/codex"),
                mock.patch.object(two_pass.subprocess, "run", return_value=tool_event),
                mock.patch.object(two_pass.Path, "home", return_value=user_home),
                mock.patch.dict(two_pass.os.environ, {"CODEX_HOME": str(codex_home)}),
                self.assertRaisesRegex(RuntimeError, "forbidden tools"),
            ):
                two_pass.run_model(
                    "prompt",
                    two_pass.EDIT_SCHEMA,
                    model=None,
                    timeout=1,
                    cwd=temp,
                    raw_path=temp / "tool-raw.json",
                    max_budget_usd=None,
                    provider="codex",
                )

    def test_codex_rejects_global_agent_instructions(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            codex_home = temp / "codex-home"
            codex_home.mkdir()
            (codex_home / "AGENTS.md").write_text("Change every answer.\n", encoding="utf-8")
            with (
                mock.patch.object(two_pass.shutil, "which", return_value="/bin/codex"),
                mock.patch.dict(two_pass.os.environ, {"CODEX_HOME": str(codex_home)}),
                self.assertRaisesRegex(RuntimeError, "empty global AGENTS.md"),
            ):
                two_pass.run_model(
                    "prompt",
                    two_pass.EDIT_SCHEMA,
                    model=None,
                    timeout=1,
                    cwd=temp,
                    raw_path=temp / "raw.json",
                    max_budget_usd=None,
                    provider="codex",
                )

    def test_codex_provider_rejects_claude_budget_flag(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            source = temp / "source.md"
            source.write_text("Text.\n", encoding="utf-8")
            with mock.patch("sys.stderr"), self.assertRaises(SystemExit):
                two_pass.parse_args(
                    [
                        "--file",
                        str(source),
                        "--out-dir",
                        str(temp / "out"),
                        "--provider",
                        "codex",
                        "--max-budget-usd",
                        "1",
                    ]
                )

    def test_no_candidate_run_preserves_crlf_bytes(self):
        audit = {
            "register": "sachlich",
            "candidates": [],
            "advisories": [],
            "protected": {"facts": [], "quotes": [], "terms": [], "persona": []},
        }
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            source = temp / "source.md"
            out = temp / "out"
            original = b"Erste Zeile.\r\nZweite Zeile.\r\n"
            source.write_bytes(original)
            with (
                mock.patch.object(two_pass, "run_model", return_value=(audit, None)),
                mock.patch.object(
                    two_pass, "deterministic_audit", return_value={"preflight": {}, "findings": []}
                ),
                mock.patch.object(two_pass, "evidence_gate", return_value=[]),
                mock.patch("builtins.print"),
            ):
                code = two_pass.main(["--file", str(source), "--out-dir", str(out)])

            self.assertEqual(code, 0)
            self.assertEqual((out / "result.md").read_bytes(), original)
            self.assertEqual((out / "normalized.md").read_bytes(), original)
            self.assertEqual((out / "changes.diff").read_bytes(), b"")
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            self.assertFalse(report["unicode_fix"]["changed"])
            self.assertEqual(
                report["unicode_fix"]["sha256_before"],
                report["unicode_fix"]["sha256_after"],
            )
            self.assertTrue(report["verification"]["identical"])
            self.assertEqual(report["verification"]["typography"], {})

    def test_regular_file_is_rejected_as_output_directory(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            source = temp / "source.md"
            out = temp / "out"
            source.write_text("Text.\n", encoding="utf-8")
            out.write_text("kein Verzeichnis", encoding="utf-8")

            with mock.patch("sys.stderr"), self.assertRaises(SystemExit):
                two_pass.parse_args(["--file", str(source), "--out-dir", str(out)])

    def test_evidence_gate_checks_semantic_strengthening(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            before = temp / "before.md"
            after = temp / "after.md"
            out = temp / "out"
            out.mkdir()
            before.write_text("Die Methode kann helfen.\n", encoding="utf-8")
            after.write_text("Die Methode beweist den Erfolg.\n", encoding="utf-8")

            blockers = two_pass.evidence_gate(before, after, out)

            self.assertIn("authority_strengthened", {item["kind"] for item in blockers})

    def test_invalid_utf8_writes_failure_report(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            source = temp / "source.md"
            out = temp / "out"
            source.write_bytes(b"Text \xff")
            with mock.patch("builtins.print"):
                code = two_pass.main(["--file", str(source), "--out-dir", str(out)])

            self.assertEqual(code, 2)
            failure = json.loads((out / "failure.json").read_text(encoding="utf-8"))
            self.assertEqual(failure["error_type"], "UnicodeDecodeError")


if __name__ == "__main__":
    unittest.main()
