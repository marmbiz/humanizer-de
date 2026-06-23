import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PatternCatalogTests(unittest.TestCase):
    def test_catalog_contains_exactly_66_pattern_ids(self):
        text = (ROOT / "references" / "patterns.md").read_text()
        ids = [int(match) for match in re.findall(r"^####\s+(\d+)\.", text, re.MULTILINE)]
        self.assertEqual(sorted(ids), list(range(1, 67)))
        self.assertEqual(len(ids), 66)

    def test_catalog_keeps_required_sections(self):
        text = (ROOT / "references" / "patterns.md").read_text()
        self.assertIn("## Kurzreferenz", text)
        self.assertIn("## Die 66 Muster", text)
        self.assertIn("#### 52. Diff-verankertes Schreiben [MEDIUM]", text)
        self.assertIn("#### 53. Lückenfüllende Spekulation [HIGH]", text)
        self.assertIn("#### 54. Doppelpunkt-Titel-Schema [MEDIUM]", text)
        self.assertIn("#### 55. Gleichförmiger Satzrhythmus [MEDIUM]", text)
        self.assertIn("#### 56. Aphorismus-Formeln [MEDIUM]", text)
        self.assertIn("#### 57. Markdown-Struktur-Artefakte [MEDIUM]", text)
        self.assertIn("#### 58. Abstrakta-Stapel und Hypernym-Präferenz [MEDIUM]", text)
        self.assertIn("#### 59. Erfundene Ich-Erfahrung und forcierte Lockerheit [HIGH]", text)
        self.assertIn("#### 60. Synonym-Rotation für dieselbe Entität [MEDIUM]", text)
        self.assertIn("#### 61. Isometrisches Dokument [MEDIUM]", text)
        self.assertIn("#### 62. Markerloser Schließzwang [MEDIUM]", text)
        self.assertIn("#### 63. Modalpartikel-Anomalie [LOW]", text)
        self.assertIn("#### 64. KI-Marker-Vokabular [MEDIUM]", text)
        self.assertIn("#### 65. Kopula-Vermeidung [MEDIUM]", text)
        self.assertIn("#### 66. Fake-Analyse-Anhang [MEDIUM]", text)

    def test_pattern_46_examples_use_real_codepoints(self):
        text = (ROOT / "references" / "patterns.md").read_text()
        section = text.split("#### 46. Falsche deutsche Anführungszeichen [HIGH]", 1)[1]
        section = section.split("#### 47. Englische Titel-Großschreibung [MEDIUM]", 1)[0]

        self.assertIn(chr(0x201E) + "Text" + chr(0x201C), section)
        self.assertIn(chr(0x201A) + "Text" + chr(0x2018), section)
        self.assertIn(chr(0x201E) + "Text" + chr(0x201D), section)
        self.assertIn(chr(0x201C) + "Text" + chr(0x201D), section)
        self.assertIn(chr(0x201E) + "Text" + chr(0x201D) + " statt " + chr(0x201E) + "Text" + chr(0x201C), text)

        for line in section.splitlines():
            if "U+201C" in line and "gerade ASCII" not in line and "(\"...\")" not in line:
                self.assertNotIn(chr(0x0022) + " (U+201C", line)
            if "U+2018" in line:
                self.assertNotIn(chr(0x0027) + " (U+2018", line)

    def test_pattern_49_apostrophe_uses_real_codepoints(self):
        text = (ROOT / "references" / "patterns.md").read_text()
        section = text.split("#### 49. Apostroph-Fehler [MEDIUM]", 1)[1]
        section = section.split("#### 50. Interpunktion bei Stichpunkt-Aufzählungen [LOW]", 1)[0]

        self.assertIn(chr(0x2019) + " (U+2019", section)
        self.assertIn(chr(0x0027) + " (U+0027", section)


if __name__ == "__main__":
    unittest.main()
