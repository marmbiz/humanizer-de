import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


FRONTMATTER_RE = re.compile(r"\A---\n(?P<frontmatter>.*?)\n---\n", re.DOTALL)
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):(?:\s*(.*))?$")


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")

    data = {}
    lines = match.group("frontmatter").splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        key_match = KEY_RE.match(line)
        if key_match is None:
            raise AssertionError(f"Invalid frontmatter line: {line!r}")

        key, value = key_match.groups()
        value = (value or "").strip()

        if value in {">", ">-"}:
            index += 1
            block = []
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith("  ")):
                block.append(lines[index][2:] if lines[index].startswith("  ") else "")
                index += 1
            data[key] = " ".join(part.strip() for part in block if part.strip())
            continue

        if value.startswith("'") and value.endswith("'"):
            data[key] = value[1:-1].replace("''", "'")
        elif value.startswith('"') and value.endswith('"'):
            data[key] = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [part.strip() for part in value[1:-1].split(",") if part.strip()]
        else:
            if re.search(r":(?:\s|$)", value):
                raise AssertionError(f"{key} must quote or fold colon-containing YAML scalars")
            data[key] = value

        index += 1

    return data


class SkillStructureTests(unittest.TestCase):
    def test_skill_is_v41_sop_router(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertRegex(text, r"version: 4\.\d+\.\d+")
        self.assertIn("<!-- SLOW_UPDATE_START -->", text)
        self.assertIn("<!-- FAST_UPDATE_START -->", text)
        self.assertIn("references/patterns.md", text)
        self.assertIn("references/decision-tables.md", text)
        self.assertIn("references/qgir.md", text)
        self.assertIn("scripts/unicode_lint.py", text)
        self.assertIn("scripts/rhythm_lint.py", text)

        body = text.split("---", 2)[-1]
        self.assertLessEqual(len(re.findall(r"\S+", body)), 2000)

    def test_frontmatter_metadata_is_valid(self):
        text = (ROOT / "SKILL.md").read_text()
        metadata = parse_frontmatter(text)

        self.assertEqual(metadata["name"], "Humanizer (Deutsch)")
        self.assertEqual(metadata["version"], "4.1.0")
        self.assertIsInstance(metadata["description"], str)

        description = metadata["description"]
        self.assertLessEqual(len(description), 220)
        self.assertIn("deutschen Text humanisieren", description)

    def test_frontmatter_rejects_colon_in_plain_scalar(self):
        text = """---
name: Humanizer (Deutsch)
description: Fokus: deutschen Text humanisieren, KI-Schreibmuster entfernen und deutsche KI-Tells auditieren.
version: 4.1.0
---
"""

        with self.assertRaisesRegex(AssertionError, "quote or fold"):
            parse_frontmatter(text)


if __name__ == "__main__":
    unittest.main()
