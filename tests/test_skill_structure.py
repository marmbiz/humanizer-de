import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "5.18.1"
EXPECTED_PATTERN_COUNT = 72


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SkillStructureTests(unittest.TestCase):
    def test_skill_is_sop_router(self):
        text = read_utf8(ROOT / "SKILL.md")
        self.assertRegex(text, rf"version:\s+['\"]?{re.escape(EXPECTED_VERSION)}['\"]?")
        self.assertIn("<!-- SLOW_UPDATE_START -->", text)
        self.assertIn("<!-- FAST_UPDATE_START -->", text)
        self.assertIn("## Arbeitszweig", text)
        self.assertIn("Claim-Lock", text)
        self.assertIn("Persona-Lock", text)
        self.assertIn("Null-Edit", text)
        self.assertIn("QGIR ist kein Pass-0-Zweig", text)
        for pass_id in range(6):
            segment = re.search(
                rf"\*\*Pass {pass_id}\b[\s\S]*?(?=\n\n\*\*Pass {pass_id + 1}\b|\n\n\*\*QGIR\b)",
                text,
            )
            self.assertIsNotNone(segment, f"Pass {pass_id} section missing")
            self.assertIn("Fertig, wenn", segment.group(0), f"Pass {pass_id} missing done criterion")
        self.assertIn("references/patterns.md", text)
        self.assertIn("references/decision-tables.md", text)
        self.assertIn("references/qgir.md", text)
        self.assertIn("scripts/unicode_lint.py", text)
        self.assertIn("scripts/rhythm_lint.py", text)
        self.assertIn(".venv/bin/python", text)
        self.assertIn("make lt FILE=<datei>", text)

        body = text.split("---", 2)[-1]
        # Grenze am 2026-08-03 von 2000 auf 2300 angehoben (Autor-Entscheid).
        # Anlass: SKILL.md rief nur 20 der 72 Muster namentlich auf, 19 weitere
        # waren ueber Linter erreichbar. 44 Muster hatten keinen Weg in die
        # Arbeit -- Muster 9 (Trikolon) blieb deshalb in einem Autorentext
        # unbemerkt. Die Pass-Annotation in patterns.md plus der Audit-Zweig
        # kosten rund 150 Woerter und schliessen die Luecke fuer alle 72.
        # Die Grenze bleibt bestehen: SKILL.md ist ein Router, kein Handbuch.
        self.assertLessEqual(len(re.findall(r"\S+", body)), 2300)

    def test_skill_frontmatter_is_hybrid_safe(self):
        text = read_utf8(ROOT / "SKILL.md")
        frontmatter = text.split("---", 2)[1]

        self.assertIn("name: humanizer-de", frontmatter)
        self.assertIn("allowed-tools:", frontmatter)
        self.assertIn("metadata:", frontmatter)
        self.assertNotIn("allowed_tools:", frontmatter)
        self.assertNotRegex(frontmatter, r"(?m)^name:\s+Humanizer \(Deutsch\)$")

        agent_yaml = read_utf8(ROOT / "agents" / "openai.yaml")
        self.assertIn('display_name: "Humanizer (Deutsch)"', agent_yaml)
        self.assertIn("$humanizer-de", agent_yaml)
        self.assertIn("allow_implicit_invocation: true", agent_yaml)

        skill_wrapper = ROOT / "skills" / "humanizer-de"
        wrapper_file = skill_wrapper / "SKILL.md"
        wrapper_text = read_utf8(wrapper_file)
        self.assertTrue(wrapper_file.is_file())
        self.assertFalse(wrapper_file.is_symlink())
        self.assertIn("name: humanizer-de", wrapper_text)
        self.assertIn("../../SKILL.md", wrapper_text)
        self.assertIn("Plugin-Root", wrapper_text)
        self.assertEqual({path.name for path in skill_wrapper.iterdir()}, {"SKILL.md"})
        self.assertFalse(any(path.is_symlink() for path in skill_wrapper.rglob("*")))

    def test_skill_frontmatter_survives_yaml_parsing(self):
        # Regression for PR #1 (ueberBrot): an unquoted plain scalar containing
        # ": " (e.g. description: Fokus: ...) is invalid YAML and made
        # YAML-based skill installers report "No valid skills found".
        frontmatters = {
            path: read_utf8(path).split("---", 2)[1]
            for path in (ROOT / "SKILL.md", ROOT / "skills" / "humanizer-de" / "SKILL.md")
        }

        plain_scalar = re.compile(r"(?m)^(\s*)([A-Za-z][\w-]*):[ \t]+(?!['\"|>#\[{])(.+\S)[ \t]*$")
        for path, frontmatter in frontmatters.items():
            for match in plain_scalar.finditer(frontmatter):
                self.assertNotIn(
                    ": ",
                    match.group(3),
                    f"{path.name}: unquoted frontmatter value of '{match.group(2)}' "
                    "contains ': ' and breaks YAML parsing - quote the value",
                )

        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed; plain-scalar guard above covers the regression")
        for path, frontmatter in frontmatters.items():
            data = yaml.safe_load(frontmatter)
            self.assertIsInstance(data, dict, path.name)
            self.assertIsInstance(data.get("name"), str, path.name)
            self.assertTrue(str(data.get("description", "")).strip(), path.name)

    def test_description_is_narrow(self):
        text = read_utf8(ROOT / "SKILL.md")
        match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertLessEqual(len(description), 220)
        self.assertIn("bestehenden deutschen Text", description)
        self.assertIn("deutschen Text humanisieren", description)

    def test_trigger_eval_fixture_is_wellformed(self):
        cases = json.loads(read_utf8(ROOT / "tests" / "trigger_eval.json"))

        self.assertEqual(set(cases), {"should_trigger", "should_not_trigger"})
        self.assertGreaterEqual(len(cases["should_trigger"]), 10)
        self.assertGreaterEqual(len(cases["should_not_trigger"]), 10)
        self.assertTrue(all(isinstance(case, str) and case.strip() for group in cases.values() for case in group))
        self.assertFalse(set(cases["should_trigger"]) & set(cases["should_not_trigger"]))

    def test_output_prelude_has_suppression_clause(self):
        text = read_utf8(ROOT / "SKILL.md")

        self.assertIn("Less machine. More voice.", text)
        self.assertIn("Weglassen bei Raw-JSON", text)

    def test_release_metadata_stays_in_sync(self):
        skill_text = read_utf8(ROOT / "SKILL.md")
        plugin = json.loads(read_utf8(ROOT / ".claude-plugin" / "plugin.json"))
        codex_plugin = json.loads(read_utf8(ROOT / ".codex-plugin" / "plugin.json"))
        codex_marketplace = json.loads(
            read_utf8(ROOT / ".agents" / "plugins" / "marketplace.json")
        )
        marketplace = json.loads(read_utf8(ROOT / ".claude-plugin" / "marketplace.json"))
        marketplace_plugin = marketplace["plugins"][0]
        codex_marketplace_plugin = codex_marketplace["plugins"][0]
        readme_text = read_utf8(ROOT / "README.md")
        patterns_text = read_utf8(ROOT / "references" / "patterns.md")
        decision_text = read_utf8(ROOT / "references" / "decision-tables.md")
        coverage_text = read_utf8(ROOT / "docs" / "coverage-matrix.md")
        warp_text = read_utf8(ROOT / "WARP.md")
        checklist_text = read_utf8(ROOT / "assets" / "checkliste-ki-tells.md")

        self.assertRegex(skill_text, rf"version:\s+['\"]?{re.escape(EXPECTED_VERSION)}['\"]?")
        self.assertEqual(plugin["version"], EXPECTED_VERSION)
        self.assertEqual(codex_plugin["version"], EXPECTED_VERSION)
        self.assertNotIn("version", marketplace_plugin)
        self.assertEqual(codex_marketplace["name"], "humanizer-de")
        self.assertEqual(codex_marketplace_plugin["name"], "humanizer-de")
        self.assertEqual(codex_marketplace_plugin["source"]["path"], "./")
        self.assertEqual(codex_marketplace_plugin["policy"]["installation"], "AVAILABLE")
        self.assertIn("codex plugin marketplace add marmbiz/humanizer-de", readme_text)
        self.assertIn(f"- **{EXPECTED_VERSION}**", readme_text)
        self.assertIn(f"v{EXPECTED_VERSION}", patterns_text.splitlines()[2])
        self.assertIn(f"v{EXPECTED_VERSION}", decision_text.splitlines()[2])
        self.assertIn(f"v{EXPECTED_VERSION}", coverage_text)
        self.assertEqual(
            warp_text.splitlines()[0],
            f"# WARP - Humanizer (Deutsch) Entwicklerleitfaden (v{EXPECTED_VERSION})",
        )

        expected_pattern_label = f"{EXPECTED_PATTERN_COUNT} Muster"
        self.assertIn(expected_pattern_label, plugin["description"])
        self.assertIn(expected_pattern_label, codex_plugin["description"])
        self.assertIn(expected_pattern_label, codex_plugin["interface"]["longDescription"])
        self.assertIn(expected_pattern_label, marketplace_plugin["description"])
        self.assertIn(
            f"vollständige Katalog mit {EXPECTED_PATTERN_COUNT} Mustern",
            checklist_text,
        )
        self.assertIn("Supports Claude Code and Codex", plugin["description"])
        self.assertIn("Supports Claude Code and Codex", codex_plugin["description"])
        self.assertIn("Supports Claude Code and Codex", marketplace_plugin["description"])
        self.assertIn("Claude/Codex", read_utf8(ROOT / "agents" / "openai.yaml"))
        self.assertNotIn("65 Muster", plugin["description"])
        self.assertNotIn("65 Muster", codex_plugin["description"])
        self.assertNotIn("65 Muster", marketplace_plugin["description"])
        self.assertIn("GitHub Release", readme_text)
        self.assertIn("GitHub Release", warp_text)
        self.assertIn("Tag `vX.Y.Z`", warp_text)

    def test_readme_flowchart_tracks_the_skill(self):
        # Das Mermaid-Diagramm ist release-sync-pflichtig, wurde aber von keinem
        # Test gehalten und driftete dreimal unbemerkt: Die E1-Markierungspflicht
        # beim Null-Edit fehlte seit 5.13.0, der Audit-Zweig seit 5.15.0.
        # Der Waechter prueft nur, dass jedes Konzept ueberhaupt im Diagramm
        # vorkommt, solange SKILL.md es fuehrt -- keine Formulierung.
        skill_text = read_utf8(ROOT / "SKILL.md")
        readme_text = read_utf8(ROOT / "README.md")

        diagram = re.search(r"```mermaid\n(.*?)```", readme_text, re.S)
        self.assertIsNotNone(diagram, "README: Mermaid-Diagramm fehlt")
        diagram = diagram.group(1)

        # Keine Pruefung einzelner Pass-Nummern: Das Diagramm fasst "Pass 2-4"
        # zu einem Kasten zusammen, das ist gewollte Vereinfachung.
        if "Audit-Zweig" in skill_text:
            # Nicht auf "Audit" pruefen: Das steckt auch in "Selbst-Audit -
            # Pass 5", der Waechter wuerde nie anschlagen. Der Audit-Zweig ist
            # ein eigener Weg und braucht eine eigene Verzweigung.
            self.assertIn("Audit-Zweig", diagram,
                          "SKILL.md kennt den Audit-Zweig, das Diagramm nicht")
            self.assertIn("72", diagram,
                          "Der Audit-Zweig prueft den vollen Katalog; "
                          "das Diagramm nennt die Musterzahl nicht")
        if "unbelegte oder erfundene Quellen werden immer markiert" in skill_text:
            self.assertRegex(diagram, r"markier",
                             "SKILL.md markiert unbelegte Quellen auch beim "
                             "Null-Edit; das Diagramm zeigt es nicht")

        knoten = set(re.findall(r"(\w+)\s*[\[({]", diagram))
        kanten = []
        for zeile in diagram.splitlines():
            if "-->" not in zeile:
                continue
            links, rechts = zeile.split("-->", 1)
            a, b = re.match(r"\s*(\w+)", links), re.match(r"\s*(\w+)", rechts)
            if a and b:
                kanten.append((a.group(1), b.group(1)))
        erreichbar, offen = set(), ["T"]
        while offen:
            knoten_id = offen.pop()
            if knoten_id in erreichbar:
                continue
            erreichbar.add(knoten_id)
            offen += [b for a, b in kanten if a == knoten_id]
        self.assertLessEqual(knoten, erreichbar,
                             f"Diagramm: unerreichbare Knoten {sorted(knoten - erreichbar)}")

        # Sackgassen sind der eigentliche Fehlerfall: Bis 5.15.1 endete der
        # Null-Edit-Ast im Nichts, weil die E1-Markierungspflicht fehlte.
        # Endpunkte sind nur die beiden Ergebnisknoten.
        ENDPUNKTE = {"B", "O"}
        mit_ausgang = {a for a, _ in kanten}
        sackgassen = knoten - mit_ausgang - ENDPUNKTE
        self.assertFalse(sackgassen,
                         f"Diagramm: Ast endet im Nichts bei {sorted(sackgassen)} "
                         "- jeder Weg muss zu einem Ergebnis führen")

    def test_precision_requirements_pin_spacy_runtime_imports(self):
        requirements = read_utf8(ROOT / "requirements-precise.txt")

        self.assertRegex(requirements, r"(?m)^click==\d")
        self.assertRegex(requirements, r"(?m)^spacy==\d")
        self.assertIn("de_core_news_sm-3.8.0", requirements)

    def test_p0_docs_define_research_and_coverage_boundaries(self):
        research = read_utf8(ROOT / "docs" / "naturalness-research-brief.md")
        coverage = read_utf8(ROOT / "docs" / "coverage-matrix.md")

        self.assertIn('Do not write "Studien zeigen"', research)
        self.assertIn("AI-detector evasion", research)

        self.assertIn("Status: P0 source-of-truth matrix", coverage)
        self.assertIn("Pattern catalog", coverage)
        self.assertIn("deterministic linters", coverage)
        self.assertIn("Scenario contracts", coverage)
        self.assertIn("Disallowed Coverage Claims", coverage)
        self.assertIn("All 72 patterns are deterministically detected", coverage)

    def test_naturalness_guidance_blocks_unsafe_persona_and_entropy_moves(self):
        skill = read_utf8(ROOT / "SKILL.md")
        naturalness = read_utf8(ROOT / "references" / "de-naturalness.md")
        profiles = read_utf8(ROOT / "references" / "register-profiles.md")

        self.assertIn("Deixis nur stabilisieren, nicht erfinden", skill)
        self.assertIn("Keine künstlichen Fragmente, Regelbrüche oder Partikel einsetzen", skill)
        self.assertIn("Textqualität, Präzision oder Lesbarkeit schlechter werden können", skill)

        self.assertIn("Deixis und Sprecherposition", naturalness)
        self.assertIn("Diskursmarker und pragmatische Haltung", naturalness)
        self.assertIn("Verbalstil statt Nominalstil", naturalness)
        self.assertIn("45 Anglizismus-Strukturen", naturalness)
        self.assertIn("harte Anglizismus-Strukturen (Muster 45", skill)
        self.assertIn("Anti-Entropy-Reflex", naturalness)
        self.assertIn("trotzdem Textqualität, Präzision oder Lesbarkeit verschlechtern", naturalness)

        self.assertIn("deictic_center", profiles)
        self.assertIn("word_level", profiles)
        self.assertIn("paragraph_openers", profiles)
        self.assertIn("Sprecherposition bleibt stabil", profiles)
        self.assertIn("situatives Register, nicht die ganze Stimme", profiles)

    def test_quality_rubric_exists_and_is_anchored_in_pass_5(self):
        rubric = (ROOT / "references" / "quality-rubric.md")
        self.assertTrue(rubric.exists())

        rubric_text = read_utf8(rubric)
        self.assertIn("Leserführung", rubric_text)
        self.assertIn("Argumentdichte", rubric_text)
        self.assertIn("Stimmkonsistenz", rubric_text)
        self.assertIn("Sparsamkeit", rubric_text)
        self.assertIn("Urteilsraster, kein Linter", rubric_text)

        skill = read_utf8(ROOT / "SKILL.md")
        pass_5 = re.search(r"\*\*Pass 5\b[\s\S]*?(?=\n\n\*\*|\Z)", skill)
        self.assertIsNotNone(pass_5)
        self.assertIn("references/quality-rubric.md", pass_5.group(0))

    def test_ai_involvement_audit_stays_roadmap_not_active_skill(self):
        skill = read_utf8(ROOT / "SKILL.md")
        readme = read_utf8(ROOT / "README.md")

        self.assertNotIn("references/ai-involvement-audit.md", skill)
        self.assertNotIn("Hinweisdichte", skill)
        self.assertFalse((ROOT / "references" / "ai-involvement-audit.md").exists())
        self.assertIn("Preflight-Risiko", skill)
        self.assertIn("keine Autorenschaftsprüfung", skill)
        self.assertIn("Combing-Gate", skill)
        self.assertIn("sentence_length_buckets", skill)
        self.assertIn("Preflight-Risiko", readme)
        self.assertIn("keine Aussage zur Autorenschaft", readme)
        self.assertIn("kontrollierten Nachkamm", readme)
        self.assertIn("schlechter werden können", readme)

    def test_readme_examples_preserve_claim_boundaries(self):
        readme = read_utf8(ROOT / "README.md")

        self.assertNotIn("wendet sie auf das Rewrite an", readme)
        self.assertNotIn("in 8 Ländern mit einem Umsatz von 50 Millionen Euro", readme)
        self.assertNotIn("in\ndiesem Zeitraum", readme)

    def test_readme_install_onboarding_is_explicit(self):
        readme = read_utf8(ROOT / "README.md")
        installation = readme.split("## Installation", 1)[1].split("## Benutzung", 1)[0]

        self.assertIn("### Was dabei installiert wird", installation)
        self.assertIn("**Nicht installiert werden:**", installation)
        self.assertIn("### Installation prüfen (alle Wege)", installation)
        self.assertIn("### Version und Updates", installation)
        self.assertIn("https://code.claude.com/docs/en/discover-plugins", installation)
        self.assertIn("https://learn.chatgpt.com/docs/plugins", installation)
        self.assertNotIn("mkdir -p ~/.codex/skills", installation)

        self.assertIn("### Installationsregeln für Assistenten", readme)
        self.assertIn("Keine Zusatzsoftware ohne Zustimmung", readme)
        self.assertIn("`$HOME/.claude/skills/humanizer-de/`", readme)
        self.assertIn("Aktivierung nicht behaupten", readme)

    def test_readme_keeps_navigation_contracts(self):
        readme = read_utf8(ROOT / "README.md")
        self.assertRegex(
            readme,
            r"<details>\s*<summary><strong>Ältere Versionen</strong></summary>",
        )

        for anchor in [
            "warum-nutzen",
            "tipps-zur-nutzung",
            "wann-hilfreich--und-wann-nicht",
            "datenschutz--sicherheit",
            "philosophie",
            "feedback--beitrag",
            "verwandte-ressourcen",
        ]:
            self.assertIn(f'<a id="{anchor}"></a>', readme)

    def test_discoverability_metadata_is_present(self):
        readme = read_utf8(ROOT / "README.md")
        skill = read_utf8(ROOT / "SKILL.md")
        agent_yaml = read_utf8(ROOT / "agents" / "openai.yaml")
        plugin = json.loads(read_utf8(ROOT / ".claude-plugin" / "plugin.json"))
        codex_plugin = json.loads(read_utf8(ROOT / ".codex-plugin" / "plugin.json"))

        self.assertIn("German AI Text Humanizer", skill)
        self.assertIn("German AI text humanizer for Claude/Codex", agent_yaml)
        self.assertNotIn("Nicht als Detektor-Garantie", readme)
        self.assertNotIn("Undetectable-Tool", readme)

        required_keywords = {
            "ai-humanizer",
            "claude-skill",
            "claude-code",
            "codex-skill",
            "ki-text",
            "ki-texte-humanisieren",
            "germanizer",
            "prompt-engineering",
        }
        self.assertTrue(required_keywords.issubset(set(plugin["keywords"])))
        self.assertTrue(required_keywords.issubset(set(codex_plugin["keywords"])))


if __name__ == "__main__":
    unittest.main()
