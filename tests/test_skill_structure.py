import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "5.3.0"
EXPECTED_PATTERN_COUNT = 66


class SkillStructureTests(unittest.TestCase):
    def test_skill_is_sop_router(self):
        text = (ROOT / "SKILL.md").read_text()
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

        body = text.split("---", 2)[-1]
        self.assertLessEqual(len(re.findall(r"\S+", body)), 2000)

    def test_skill_frontmatter_is_hybrid_safe(self):
        text = (ROOT / "SKILL.md").read_text()
        frontmatter = text.split("---", 2)[1]

        self.assertIn("name: humanizer-de", frontmatter)
        self.assertIn("allowed-tools:", frontmatter)
        self.assertIn("metadata:", frontmatter)
        self.assertNotIn("allowed_tools:", frontmatter)
        self.assertNotRegex(frontmatter, r"(?m)^name:\s+Humanizer \(Deutsch\)$")

        agent_yaml = (ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn('display_name: "Humanizer (Deutsch)"', agent_yaml)
        self.assertIn("$humanizer-de", agent_yaml)
        self.assertIn("allow_implicit_invocation: true", agent_yaml)

        skill_wrapper = ROOT / "skills" / "humanizer-de"
        self.assertTrue((skill_wrapper / "SKILL.md").is_symlink())
        self.assertTrue((skill_wrapper / "references").is_symlink())
        self.assertTrue((skill_wrapper / "scripts").is_symlink())

    def test_description_is_narrow(self):
        text = (ROOT / "SKILL.md").read_text()
        match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertLessEqual(len(description), 220)
        self.assertIn("deutschen Text humanisieren", description)

    def test_output_prelude_has_suppression_clause(self):
        text = (ROOT / "SKILL.md").read_text()

        self.assertIn("Less machine. More voice.", text)
        self.assertIn("Weglassen bei Raw-JSON", text)

    def test_release_metadata_stays_in_sync(self):
        skill_text = (ROOT / "SKILL.md").read_text()
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        codex_plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        codex_marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text()
        )
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        marketplace_plugin = marketplace["plugins"][0]
        codex_marketplace_plugin = codex_marketplace["plugins"][0]
        readme_text = (ROOT / "README.md").read_text()
        patterns_text = (ROOT / "references" / "patterns.md").read_text()
        decision_text = (ROOT / "references" / "decision-tables.md").read_text()
        coverage_text = (ROOT / "docs" / "coverage-matrix.md").read_text()
        warp_text = (ROOT / "WARP.md").read_text()

        self.assertRegex(skill_text, rf"version:\s+['\"]?{re.escape(EXPECTED_VERSION)}['\"]?")
        self.assertEqual(plugin["version"], EXPECTED_VERSION)
        self.assertEqual(codex_plugin["version"], EXPECTED_VERSION)
        self.assertEqual(marketplace_plugin["version"], EXPECTED_VERSION)
        self.assertEqual(codex_marketplace["name"], "humanizer-de")
        self.assertEqual(codex_marketplace_plugin["name"], "humanizer-de")
        self.assertEqual(codex_marketplace_plugin["source"]["path"], "./")
        self.assertEqual(codex_marketplace_plugin["policy"]["installation"], "AVAILABLE")
        self.assertIn("codex plugin marketplace add marmbiz/humanizer-de", readme_text)
        self.assertIn(f"- **{EXPECTED_VERSION}**", readme_text)
        self.assertIn(f"v{EXPECTED_VERSION}", patterns_text)
        self.assertIn(f"v{EXPECTED_VERSION}", decision_text)
        self.assertIn(f"v{EXPECTED_VERSION}", coverage_text)

        expected_pattern_label = f"{EXPECTED_PATTERN_COUNT} Muster"
        self.assertIn(expected_pattern_label, plugin["description"])
        self.assertIn(expected_pattern_label, codex_plugin["description"])
        self.assertIn(expected_pattern_label, marketplace_plugin["description"])
        self.assertIn("Supports Claude Code and Codex", readme_text)
        self.assertIn("Supports Claude Code and Codex", plugin["description"])
        self.assertIn("Supports Claude Code and Codex", codex_plugin["description"])
        self.assertIn("Supports Claude Code and Codex", marketplace_plugin["description"])
        self.assertIn("Claude/Codex", (ROOT / "agents" / "openai.yaml").read_text())
        self.assertNotIn("65 Muster", plugin["description"])
        self.assertNotIn("65 Muster", codex_plugin["description"])
        self.assertNotIn("65 Muster", marketplace_plugin["description"])
        self.assertIn("GitHub Release", readme_text)
        self.assertIn("GitHub Release", warp_text)
        self.assertIn("Tag `vX.Y.Z`", warp_text)

    def test_p0_docs_define_research_and_coverage_boundaries(self):
        research = (ROOT / "docs" / "naturalness-research-brief.md").read_text()
        coverage = (ROOT / "docs" / "coverage-matrix.md").read_text()

        self.assertIn("Status: P0 research safeguard", research)
        self.assertIn("Repo heuristic", research)
        self.assertIn("Source Ledger Template", research)
        self.assertIn('Do not write "Studien zeigen"', research)
        self.assertIn("AI-detector evasion", research)

        self.assertIn("Status: P0 source-of-truth matrix", coverage)
        self.assertIn("Pattern catalog", coverage)
        self.assertIn("deterministic linters", coverage)
        self.assertIn("Scenario contracts", coverage)
        self.assertIn("Disallowed Coverage Claims", coverage)
        self.assertIn("All 66 patterns are deterministically detected", coverage)
        self.assertIn("Unsourced Idea Intake", research)
        self.assertIn("Maximize entropy", research)

    def test_naturalness_guidance_blocks_unsafe_persona_and_entropy_moves(self):
        skill = (ROOT / "SKILL.md").read_text()
        naturalness = (ROOT / "references" / "de-naturalness.md").read_text()
        profiles = (ROOT / "references" / "register-profiles.md").read_text()
        research = (ROOT / "docs" / "naturalness-research-brief.md").read_text()

        self.assertIn("Deixis nur stabilisieren, nicht erfinden", skill)
        self.assertIn("Keine künstlichen Fragmente, Regelbrüche oder Partikel einsetzen", skill)
        self.assertIn("Textqualität, Präzision oder Lesbarkeit schlechter werden können", skill)

        self.assertIn("Deixis und Sprecherposition", naturalness)
        self.assertIn("Diskursmarker und pragmatische Haltung", naturalness)
        self.assertIn("Verbalstil statt Nominalstil", naturalness)
        self.assertIn("Anti-Entropy-Reflex", naturalness)
        self.assertIn("trotzdem Textqualität, Präzision oder Lesbarkeit verschlechtern", naturalness)

        self.assertIn("deictic_center", profiles)
        self.assertIn("Sprecherposition bleibt stabil", profiles)

        self.assertIn("Accepted as internal heuristics only", research)
        self.assertIn("Rejected as unsafe defaults", research)

    def test_ai_involvement_audit_stays_roadmap_not_active_skill(self):
        skill = (ROOT / "SKILL.md").read_text()
        readme = (ROOT / "README.md").read_text()
        research = (ROOT / "docs" / "naturalness-research-brief.md").read_text()

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

        self.assertIn("Roadmap Ideas", research)
        self.assertIn("Calibrated AI-involvement audit", research)
        self.assertIn("labeled German benchmark", research)
        self.assertIn("not authorship proof or uncalibrated percentages", research)

    def test_readme_examples_preserve_claim_boundaries(self):
        readme = (ROOT / "README.md").read_text()

        self.assertIn("berücksichtigt sie als Zielprofil", readme)
        self.assertNotIn("wendet sie auf das Rewrite an", readme)
        self.assertIn("in 8 Ländern und hat einen Umsatz von 50 Millionen Euro", readme)
        self.assertNotIn("in 8 Ländern mit einem Umsatz von 50 Millionen Euro", readme)
        self.assertIn("Die Produktivität fiel positiv auf. Der Umsatz verdreifachte sich.", readme)
        self.assertNotIn("in\ndiesem Zeitraum", readme)

    def test_discoverability_metadata_is_present(self):
        readme = (ROOT / "README.md").read_text()
        skill = (ROOT / "SKILL.md").read_text()
        agent_yaml = (ROOT / "agents" / "openai.yaml").read_text()
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        codex_plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())

        for phrase in [
            "German AI Text Humanizer",
            "Claude Humanizer Deutsch",
            "KI-Texte humanisieren Deutsch",
            "marmbiz/humanizer-de",
            "deutschsprachiger Humanizer Skill für Claude Code und Codex",
        ]:
            self.assertIn(phrase, readme)

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
