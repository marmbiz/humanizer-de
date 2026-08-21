import os
import stat
import tempfile
import unittest
from pathlib import Path

from scripts.cli_output import atomic_write_text


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


if __name__ == "__main__":
    unittest.main()
