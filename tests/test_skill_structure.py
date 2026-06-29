import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "4.3.1"
EXPECTED_PATTERN_COUNT = 66


class SkillStructureTests(unittest.TestCase):
    def test_skill_is_v43_sop_router(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertIn(f"version: {EXPECTED_VERSION}", text)
        self.assertIn("<!-- SLOW_UPDATE_START -->", text)
        self.assertIn("<!-- FAST_UPDATE_START -->", text)
        self.assertIn("references/patterns.md", text)
        self.assertIn("references/decision-tables.md", text)
        self.assertIn("references/qgir.md", text)
        self.assertIn("scripts/unicode_lint.py", text)
        self.assertIn("scripts/rhythm_lint.py", text)

        body = text.split("---", 2)[-1]
        self.assertLessEqual(len(re.findall(r"\S+", body)), 2000)

    def test_description_is_narrow(self):
        text = (ROOT / "SKILL.md").read_text()
        match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertLessEqual(len(description), 220)
        self.assertIn("deutschen Text humanisieren", description)

    def test_release_metadata_stays_in_sync(self):
        skill_text = (ROOT / "SKILL.md").read_text()
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        marketplace_plugin = marketplace["plugins"][0]
        readme_text = (ROOT / "README.md").read_text()
        patterns_text = (ROOT / "references" / "patterns.md").read_text()
        decision_text = (ROOT / "references" / "decision-tables.md").read_text()

        self.assertIn(f"version: {EXPECTED_VERSION}", skill_text)
        self.assertEqual(plugin["version"], EXPECTED_VERSION)
        self.assertEqual(marketplace_plugin["version"], EXPECTED_VERSION)
        self.assertIn(f"### {EXPECTED_VERSION} (aktuell)", readme_text)
        self.assertIn(f"v{EXPECTED_VERSION}", patterns_text)
        self.assertIn(f"v{EXPECTED_VERSION}", decision_text)

        expected_pattern_label = f"{EXPECTED_PATTERN_COUNT} Muster"
        self.assertIn(expected_pattern_label, plugin["description"])
        self.assertIn(expected_pattern_label, marketplace_plugin["description"])
        self.assertNotIn("65 Muster", plugin["description"])
        self.assertNotIn("65 Muster", marketplace_plugin["description"])

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

        self.assertIn("Deixis und Sprecherposition", naturalness)
        self.assertIn("Diskursmarker und pragmatische Haltung", naturalness)
        self.assertIn("Verbalstil statt Nominalstil", naturalness)
        self.assertIn("Anti-Entropy-Reflex", naturalness)

        self.assertIn("deictic_center", profiles)
        self.assertIn("Sprecherposition bleibt stabil", profiles)

        self.assertIn("Accepted as internal heuristics only", research)
        self.assertIn("Rejected as unsafe defaults", research)

    def test_ai_involvement_audit_stays_roadmap_not_active_skill(self):
        skill = (ROOT / "SKILL.md").read_text()
        research = (ROOT / "docs" / "naturalness-research-brief.md").read_text()

        self.assertNotIn("references/ai-involvement-audit.md", skill)
        self.assertNotIn("Hinweisdichte", skill)
        self.assertFalse((ROOT / "references" / "ai-involvement-audit.md").exists())

        self.assertIn("Roadmap Ideas", research)
        self.assertIn("Calibrated AI-involvement audit", research)
        self.assertIn("labeled German benchmark", research)
        self.assertIn("not authorship proof or uncalibrated percentages", research)


if __name__ == "__main__":
    unittest.main()
