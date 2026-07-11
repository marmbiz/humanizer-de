import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "patterns.md"
EXPECTED_PATTERN_COUNT = 66
CATALOG_HEADING = f"## Die {EXPECTED_PATTERN_COUNT} Muster"
PATTERN_HEADING_RE = re.compile(r"^#### (\d{1,2})\. (.+?) \[(HIGH|MEDIUM|LOW)\]$")
SHORT_REFERENCE_RE = re.compile(r"^## Kurzreferenz\s*$\n(?P<section>.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
SHORT_REFERENCE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(HIGH|MEDIUM|LOW)\s*\|.*\|\s*$")


def read_catalog():
    return CATALOG_PATH.read_text(encoding="utf-8")


def parse_pattern_headings(text):
    entries = {}
    for line in text.splitlines():
        match = PATTERN_HEADING_RE.fullmatch(line)
        if match:
            entries[int(match.group(1))] = (match.group(2), match.group(3))
    return entries


def extract_short_reference_section(text):
    match = SHORT_REFERENCE_RE.search(text)
    if not match:
        raise AssertionError("Kurzreferenz-Abschnitt fehlt")
    return match.group("section")


def parse_short_reference_entries(section):
    entries = {}
    for line in section.splitlines():
        match = SHORT_REFERENCE_ROW_RE.fullmatch(line)
        if not match:
            continue
        pattern_id = int(match.group(1))
        if pattern_id in entries:
            raise AssertionError(f"Kurzreferenz enthält Muster {pattern_id} doppelt")
        entries[pattern_id] = (match.group(2).strip(), match.group(3))
    return entries


def extract_pattern_section(pattern_id):
    text = read_catalog()
    pattern = rf"^#### {pattern_id}\..*?(?=^#### \d+\.|^### |^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Muster {pattern_id} nicht gefunden")
    return match.group(0)


def extract_short_reference_row(pattern_id):
    section = extract_short_reference_section(read_catalog())
    match = re.search(rf"^\|\s*{pattern_id}\s*\|.*\|\s*$", section, re.MULTILINE)
    if not match:
        raise AssertionError(f"Kurzreferenz fehlt Muster {pattern_id}")
    return match.group(0)


class PatternCatalogTests(unittest.TestCase):
    def test_catalog_contains_exactly_66_pattern_ids(self):
        text = read_catalog()
        ids = [int(match) for match in re.findall(r"^####\s+(\d+)\.", text, re.MULTILINE)]
        self.assertEqual(sorted(ids), list(range(1, EXPECTED_PATTERN_COUNT + 1)))
        self.assertEqual(len(ids), EXPECTED_PATTERN_COUNT)

    def test_category_counts_match_actual(self):
        text = (ROOT / "references" / "patterns.md").read_text(encoding="utf-8")
        catalog = text.split("## Die 66 Muster", 1)[1]

        declared = {}
        actual = {}
        category = None
        for line in catalog.splitlines():
            heading = re.match(r"^### (.+?) \((\d+) Muster\)\s*$", line)
            if heading:
                category = heading.group(1)
                self.assertNotIn(category, declared, f"Kategorie doppelt: {category}")
                declared[category] = int(heading.group(2))
                actual[category] = 0
            elif re.match(r"^##(?!##)", line):
                category = None
            elif category is not None and re.match(r"^#### \d+\.", line):
                actual[category] += 1

        self.assertTrue(declared, "Keine Kategorie-Headings gefunden")
        for category, count in declared.items():
            self.assertEqual(
                actual[category],
                count,
                f"Kategorie '{category}' deklariert {count} Muster, enthält aber {actual[category]}",
            )
        self.assertEqual(sum(declared.values()), 66)

    def test_catalog_keeps_required_sections(self):
        text = read_catalog()
        self.assertIn("## Kurzreferenz", text)
        self.assertIn("## Statistische Detektoren (GPTZero u. a.)", text)
        self.assertIn(CATALOG_HEADING, text)

    def test_pattern_headings_have_required_format(self):
        text = read_catalog()
        pattern_lines = [line for line in text.splitlines() if line.startswith("####")]

        self.assertTrue(pattern_lines, "Keine Musterzeilen gefunden")
        for line in pattern_lines:
            match = PATTERN_HEADING_RE.fullmatch(line)
            self.assertIsNotNone(match, f"Musterzeile hat falsches Format: {line}")
            self.assertTrue(match.group(2).strip(), f"Muster {match.group(1)} hat leeren Titel")

    def test_short_reference_matches_pattern_headings(self):
        text = read_catalog()
        short_reference_section = extract_short_reference_section(text)
        self.assertIn("| # | Muster | Schwere | Schlüssel-Indikatoren |", short_reference_section)
        self.assertIn("|---|--------|---------|-----------------------|", short_reference_section)

        short_reference = parse_short_reference_entries(short_reference_section)
        pattern_headings = parse_pattern_headings(text)

        for pattern_id in range(1, EXPECTED_PATTERN_COUNT + 1):
            self.assertIn(pattern_id, short_reference, f"Kurzreferenz fehlt Muster {pattern_id}")
            self.assertIn(pattern_id, pattern_headings, f"####-Block fehlt Muster {pattern_id}")
            self.assertEqual(
                short_reference[pattern_id],
                pattern_headings[pattern_id],
                f"Kurzreferenz stimmt für Muster {pattern_id} nicht mit dem ####-Block überein",
            )

        for pattern_id in sorted(set(short_reference) - set(pattern_headings)):
            self.fail(f"Kurzreferenz enthält zusätzliches Muster {pattern_id}")
        for pattern_id in sorted(set(pattern_headings) - set(short_reference)):
            self.fail(f"####-Blöcke enthalten zusätzliches Muster {pattern_id}")

    def test_every_pattern_has_haltbarkeit(self):
        haltbarkeit_re = re.compile(
            r"^<!-- haltbarkeit: (kern|jahrgang stand=\d{4}-\d{2}) -->$", re.MULTILINE
        )
        any_haltbarkeit_re = re.compile(r"^<!-- haltbarkeit:.*-->$", re.MULTILINE)

        for pattern_id in range(1, EXPECTED_PATTERN_COUNT + 1):
            section = extract_pattern_section(pattern_id)
            annotations = any_haltbarkeit_re.findall(section)
            self.assertEqual(
                len(annotations),
                1,
                f"Muster {pattern_id} braucht genau ein haltbarkeit-Attribut, hat {len(annotations)}",
            )
            self.assertRegex(
                annotations[0],
                haltbarkeit_re,
                f"Muster {pattern_id} hat ungültiges haltbarkeit-Attribut: {annotations[0]!r}",
            )
            first_line, second_line = section.splitlines()[:2]
            self.assertEqual(
                second_line,
                annotations[0],
                f"haltbarkeit-Attribut von Muster {pattern_id} steht nicht direkt unter dem Heading",
            )

    def test_pattern_16_broadens_dash_rule_without_banning_word_hyphens(self):
        section = extract_pattern_section(16)

        self.assertIn("` - `", section)
        self.assertIn("` -- `", section)
        self.assertIn("Der Tell verschwindet nicht, wenn nur das Glyph gewechselt wird", section)
        self.assertIn("Bindestrich in Komposita, Namen, URLs, IDs", section)

    def test_pattern_26_is_factual_reliability_gate(self):
        section = extract_pattern_section(26)

        self.assertIn("Factual Reliability", section)
        self.assertIn("Jede konkrete Referenz zuerst als ungeprüft behandeln", section)
        self.assertIn("[QUELLE NICHT VERIFIZIERT]", section)
        self.assertIn("Nie eine Ersatzquelle erfinden", section)

    def test_pattern_46_examples_use_real_codepoints(self):
        section = extract_pattern_section(46)
        short_reference_row = extract_short_reference_row(46)

        self.assertIn(chr(0x201E) + "Text" + chr(0x201C), section)
        self.assertIn(chr(0x201A) + "Text" + chr(0x2018), section)
        self.assertIn(chr(0x201E) + "Text" + chr(0x201D), section)
        self.assertIn(chr(0x201C) + "Text" + chr(0x201D), section)
        self.assertIn(
            chr(0x201E) + "Text" + chr(0x201D) + " statt " + chr(0x201E) + "Text" + chr(0x201C),
            short_reference_row,
        )

        for line in section.splitlines():
            if "U+201C" in line and "gerade ASCII" not in line and "(\"...\")" not in line:
                self.assertNotIn(chr(0x0022) + " (U+201C", line)
            if "U+2018" in line:
                self.assertNotIn(chr(0x0027) + " (U+2018", line)

    def test_pattern_49_apostrophe_uses_real_codepoints(self):
        section = extract_pattern_section(49)

        self.assertIn(chr(0x2019) + " (U+2019", section)
        self.assertIn(chr(0x0027) + " (U+0027", section)

    def test_pattern_64_states_evidence_boundary(self):
        pattern_64 = extract_pattern_section(64)
        normalized_64 = " ".join(pattern_64.split())

        self.assertIn("englische Wissenschaftssprache", normalized_64)
        self.assertIn("nicht abschließend geklärt", normalized_64)
        self.assertIn("Erst ab 3+ Markern", normalized_64)


if __name__ == "__main__":
    unittest.main()
