import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "register_lint.py"

spec = importlib.util.spec_from_file_location("register_lint", SCRIPT)
register_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(register_lint)


def kinds(report):
    return {item["kind"] for item in report["findings"]}


class RegisterLintTests(unittest.TestCase):
    def test_mixed_du_sie_is_reported(self):
        report = register_lint.lint("Du kannst die Datei prüfen. Bitte senden Sie danach die Freigabe.")
        self.assertIn("mixed_address", kinds(report))

    def test_formal_voice_intrusion_is_blocker(self):
        report = register_lint.lint("Die Studie zeigt den Effekt. Klingt spannend?", mode="formal")
        self.assertIn("formal_voice_intrusion", kinds(report))

    def test_particles_outside_locker_are_reported(self):
        report = register_lint.lint("Das ist ja schon wichtig.", mode="sachlich")
        self.assertIn("particles_outside_locker", kinds(report))

    def test_locker_allows_sparse_particle(self):
        report = register_lint.lint("Das hilft ja im Alltag.", mode="locker")
        self.assertEqual(kinds(report), set())


if __name__ == "__main__":
    unittest.main()
