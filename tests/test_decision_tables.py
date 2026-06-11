import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DecisionTableTests(unittest.TestCase):
    def test_overlap_tables_cover_required_patterns(self):
        text = (ROOT / "references" / "decision-tables.md").read_text()
        for pattern_id in ("11", "26", "42", "53", "5", "6", "34", "44", "58", "59", "60", "61", "62", "64", "65"):
            self.assertIn(f"| {pattern_id} |", text)
        self.assertIn("## Evidenz: 11 / 26 / 42 / 53", text)
        self.assertIn("## Floskeln und Schablonen: 1 / 2 / 32 / 56 / 58 / 60 / 64 / 65", text)
        self.assertIn("## Struktur: 5 / 6 / 34 / 44 / 61 / 62", text)
        self.assertIn("## Evidenz zweiter Ordnung: 59", text)

    def test_v40_rows_are_present(self):
        text = (ROOT / "references" / "decision-tables.md").read_text()
        self.assertIn("Hypernym/Nominalstil ersetzt eine im Text belegte Konkretion", text)
        self.assertIn("Rotierende Bezeichnungen fuer denselben Referenten", text)
        self.assertIn("Anekdote/Ich-Erfahrung ohne Traeger im Autorenkontext", text)
        self.assertIn("Absaetze/Sektionen/Listen durchgehend gleich lang und symmetrisch", text)
        self.assertIn("Bewertender Abschlusssatz ohne neue Information am Absatzende", text)
        self.assertIn(
            '| Frequenz-Marker-Vokabeln in Haeufung ("beleuchten", "spannend", "nahtlos", "Landschaft" figurativ) | 64 | Durch gewoehnliches Wort ersetzen; fachgebundene Verwendung stehen lassen |',
            text,
        )
        self.assertIn(
            '| Ersatzkonstruktion statt "ist"/"hat" ("fungiert als", "verfuegt ueber") in Haeufung | 65 | Auf Kopula zurueckfuehren, wenn keine Information verloren geht |',
            text,
        )
        self.assertIn(
            "| Symbolische Aufladung statt nuechterner Ersatzkonstruktion | 1, nicht 65 | Siehe Muster 1 |",
            text,
        )

    def test_mode_matrix_is_present(self):
        text = (ROOT / "references" / "decision-tables.md").read_text()
        self.assertIn("## Modusmatrix", text)
        self.assertIn("Formal", text)
        self.assertIn("Muster 45", text)


if __name__ == "__main__":
    unittest.main()
