import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DecisionTableTests(unittest.TestCase):
    def test_overlap_tables_cover_required_patterns(self):
        text = (ROOT / "references" / "decision-tables.md").read_text()
        for pattern_id in ("11", "26", "42", "53", "5", "6", "34", "44"):
            self.assertIn(f"| {pattern_id} |", text)
        self.assertIn("## Evidenz: 11 / 26 / 42 / 53", text)
        self.assertIn("## Struktur: 5 / 6 / 34 / 44", text)

    def test_mode_matrix_is_present(self):
        text = (ROOT / "references" / "decision-tables.md").read_text()
        self.assertIn("## Modusmatrix", text)
        self.assertIn("Formal", text)
        self.assertIn("Muster 45", text)


if __name__ == "__main__":
    unittest.main()
