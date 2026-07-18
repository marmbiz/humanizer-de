import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "5.7.1"
EXPECTED_PATTERN_COUNT = 66


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
        self.assertLessEqual(len(re.findall(r"\S+", body)), 2000)

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

    def test_description_is_narrow(self):
        text = read_utf8(ROOT / "SKILL.md")
        match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertLessEqual(len(description), 220)
        self.assertIn("deutschen Text humanisieren", description)

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
        self.assertIn(f"v{EXPECTED_VERSION}", patterns_text.splitlines()[2])
        self.assertIn(f"v{EXPECTED_VERSION}", decision_text.splitlines()[2])
        self.assertIn(f"v{EXPECTED_VERSION}", coverage_text)

        expected_pattern_label = f"{EXPECTED_PATTERN_COUNT} Muster"
        self.assertIn(expected_pattern_label, plugin["description"])
        self.assertIn(expected_pattern_label, codex_plugin["description"])
        self.assertIn(expected_pattern_label, marketplace_plugin["description"])
        self.assertIn("Supports Claude Code and Codex", readme_text)
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

    def test_precision_requirements_pin_spacy_runtime_imports(self):
        requirements = read_utf8(ROOT / "requirements-precise.txt")

        self.assertRegex(requirements, r"(?m)^click==\d")
        self.assertRegex(requirements, r"(?m)^spacy==\d")
        self.assertIn("de_core_news_sm-3.8.0", requirements)

    def test_p0_docs_define_research_and_coverage_boundaries(self):
        research = read_utf8(ROOT / "docs" / "naturalness-research-brief.md")
        coverage = read_utf8(ROOT / "docs" / "coverage-matrix.md")

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
        skill = read_utf8(ROOT / "SKILL.md")
        naturalness = read_utf8(ROOT / "references" / "de-naturalness.md")
        profiles = read_utf8(ROOT / "references" / "register-profiles.md")
        research = read_utf8(ROOT / "docs" / "naturalness-research-brief.md")

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
        research = read_utf8(ROOT / "docs" / "naturalness-research-brief.md")

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
        readme = read_utf8(ROOT / "README.md")

        self.assertIn("berücksichtigt sie als Zielprofil", readme)
        self.assertNotIn("wendet sie auf das Rewrite an", readme)
        self.assertIn("in 8 Ländern und hat einen Umsatz von 50 Millionen Euro", readme)
        self.assertNotIn("in 8 Ländern mit einem Umsatz von 50 Millionen Euro", readme)
        self.assertIn("Die Produktivität fiel positiv auf. Der Umsatz verdreifachte sich.", readme)
        self.assertNotIn("in\ndiesem Zeitraum", readme)

    def test_readme_install_onboarding_is_explicit(self):
        readme = read_utf8(ROOT / "README.md")
        installation = readme.split("## Installation", 1)[1].split("## Benutzung", 1)[0]

        self.assertIn("Für den Basis-Skill ist kein Python nötig", installation)
        self.assertIn("Plugin und manuelle Skill-Kopie", installation)
        self.assertIn("### Was dabei installiert wird", installation)
        self.assertIn("**Nicht installiert werden:**", installation)
        self.assertIn("### Installation prüfen (alle Wege)", installation)
        self.assertIn("### Version und Updates", installation)
        self.assertIn("`~/.codex/skills/` ist nur ein Legacy-Pfad", installation)
        self.assertIn("`/reload-plugins`", installation)
        self.assertIn("https://code.claude.com/docs/en/discover-plugins", installation)
        self.assertIn("https://learn.chatgpt.com/docs/plugins", installation)
        self.assertNotIn("mkdir -p ~/.codex/skills", installation)

        self.assertIn("### Installationsregeln für Assistenten", readme)
        self.assertIn("Keine Zusatzsoftware ohne Zustimmung", readme)
        self.assertIn("`$HOME/.claude/skills/humanizer-de/`", readme)
        self.assertIn("Aktivierung nicht behaupten", readme)
        self.assertIn("py -m pip install -r requirements-precise.txt", readme)
        self.assertIn("python3.12 -m venv .venv", readme)
        self.assertIn("make doctor-full", readme)
        self.assertIn("py scripts/doctor.py --json", readme)
        self.assertIn("sudo apt install hunspell hunspell-de-de", readme)

    def test_readme_follows_the_user_journey(self):
        readme = read_utf8(ROOT / "README.md")
        headings = [
            "## Was ist das?",
            "## Installation",
            "## Benutzung",
            "## Beispiele",
            "## Fakten, Grenzen und Datenschutz",
            "## Wie der Skill arbeitet",
            "## Optionale Werkzeuge",
            "## 66 Muster in 10 Kategorien",
            "## Für AI-Assistenten",
            "## Entwicklung und Verifikation",
            "## Was ist neu?",
            "## Attribution",
            "## Lizenz",
        ]

        positions = [readme.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Installationsdetails, manuelle Wege und Updates", readme)
        self.assertIn("Power-User: lokaler Prüfablauf", readme)
        self.assertIn("Einzelchecks, Exit-Codes und Evidence-Gate", readme)
        self.assertIn("Ältere Versionen", readme)

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
