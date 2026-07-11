import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PATTERN_COUNT = 66
PATTERN_HEADING_RE = re.compile(r"^#### (\d{1,2})\. (.+?) \[(HIGH|MEDIUM|LOW)\]$")
README_ROW_RE = re.compile(r"^\| (\d+) \| (.+?) \| (HIGH|MEDIUM|LOW) \|$")
CATEGORY_BLOCK_RE = re.compile(
    r"<summary><strong>(.+?) \((\d+) Muster\)</strong></summary>(.*?)</details>",
    re.DOTALL,
)


def readme_catalog_section():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    section = text.split("## 66 Muster in 10 Kategorien", 1)[1]
    return re.split(r"\n## ", section, maxsplit=1)[0]


def pattern_headings():
    text = (ROOT / "references" / "patterns.md").read_text(encoding="utf-8")
    entries = {}
    for line in text.splitlines():
        match = PATTERN_HEADING_RE.fullmatch(line)
        if match:
            entries[int(match.group(1))] = (match.group(2), match.group(3))
    return entries


def readme_rows(section):
    entries = {}
    for line in section.splitlines():
        match = README_ROW_RE.fullmatch(line)
        if not match:
            continue
        pattern_id = int(match.group(1))
        if pattern_id in entries:
            raise AssertionError(f"README enthält Muster {pattern_id} doppelt")
        entries[pattern_id] = (match.group(2).strip(), match.group(3))
    return entries


def title_matches(readme_title, pattern_title):
    if readme_title == pattern_title:
        return True
    return readme_title.startswith(pattern_title + " (") and readme_title.endswith(")")


class ReadmePatternsSyncTests(unittest.TestCase):
    def test_readme_rows_match_pattern_headings(self):
        rows = readme_rows(readme_catalog_section())
        headings = pattern_headings()

        self.assertEqual(
            sorted(rows),
            list(range(1, EXPECTED_PATTERN_COUNT + 1)),
            "README-Katalog enthält nicht genau die Muster 1..66",
        )
        for pattern_id in range(1, EXPECTED_PATTERN_COUNT + 1):
            readme_title, readme_severity = rows[pattern_id]
            pattern_title, pattern_severity = headings[pattern_id]
            self.assertTrue(
                title_matches(readme_title, pattern_title),
                f"README-Titel für Muster {pattern_id} weicht ab: "
                f"{readme_title!r} vs. {pattern_title!r}",
            )
            self.assertEqual(
                readme_severity,
                pattern_severity,
                f"README-Schwere für Muster {pattern_id} weicht ab",
            )

    def test_readme_category_counts_match_rows(self):
        section = readme_catalog_section()
        blocks = CATEGORY_BLOCK_RE.findall(section)
        self.assertTrue(blocks, "Keine <details>-Kategorienblöcke gefunden")

        total = 0
        for name, declared, body in blocks:
            actual = len([line for line in body.splitlines() if README_ROW_RE.fullmatch(line)])
            self.assertEqual(
                actual,
                int(declared),
                f"README-Kategorie '{name}' deklariert {declared} Muster, enthält aber {actual}",
            )
            total += actual
        self.assertEqual(total, EXPECTED_PATTERN_COUNT)


if __name__ == "__main__":
    unittest.main()
