import os
import stat
import tempfile
import unittest
from pathlib import Path

from scripts.cli_output import CliInputError, atomic_write_text


class CliOutputTests(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "Windows chmod exposes only the read-only bit")
    def test_atomic_write_preserves_existing_file_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "text.md"
            path.write_text("alt", encoding="utf-8")
            path.chmod(0o640)

            atomic_write_text(path, "neu")

            self.assertEqual(path.read_text(encoding="utf-8"), "neu")
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o640)

    @unittest.skipIf(os.name == "nt", "symlink creation is not portable on Windows CI")
    def test_atomic_write_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target.md"
            link = Path(tmp) / "link.md"
            target.write_text("alt", encoding="utf-8")
            link.symlink_to(target)

            with self.assertRaisesRegex(CliInputError, "refusing to replace symlink"):
                atomic_write_text(link, "neu")

            self.assertTrue(link.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "alt")


if __name__ == "__main__":
    unittest.main()
