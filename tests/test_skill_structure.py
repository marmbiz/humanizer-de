import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillStructureTests(unittest.TestCase):
    def test_skill_is_v40_sop_router(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertIn("version: 4.0.0", text)
        self.assertIn("<!-- SLOW_UPDATE_START -->", text)
        self.assertIn("<!-- FAST_UPDATE_START -->", text)
        self.assertIn("references/patterns.md", text)
        self.assertIn("references/decision-tables.md", text)
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


if __name__ == "__main__":
    unittest.main()
