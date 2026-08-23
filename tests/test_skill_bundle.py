import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_skill_bundle.py"
BUNDLE_NAME = "humanizer-de"


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_into(directory: Path) -> Path:
    output = directory / f"{BUNDLE_NAME}.zip"
    subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output)],
        check=True,
        capture_output=True,
    )
    return output


class SkillBundleTests(unittest.TestCase):
    """The uploadable bundle must carry everything SKILL.md routes into."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.bundle = build_into(Path(cls._tmp.name))
        with zipfile.ZipFile(cls.bundle) as archive:
            cls.names = archive.namelist()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_bundle_root_matches_skill_name(self):
        # Skill hosts derive the skill name from the top-level folder.
        self.assertIn(f"{BUNDLE_NAME}/SKILL.md", self.names)
        roots = {name.split("/", 1)[0] for name in self.names}
        self.assertEqual(roots, {BUNDLE_NAME})

    def test_referenced_reference_files_are_bundled(self):
        skill = read_utf8(ROOT / "SKILL.md")
        referenced = set(re.findall(r"references/[\w.-]+\.(?:md|json)", skill))
        self.assertTrue(referenced, "SKILL.md verweist auf keine references/-Datei")
        for name in sorted(referenced):
            self.assertIn(f"{BUNDLE_NAME}/{name}", self.names, name)

    def test_referenced_scripts_are_bundled(self):
        skill = read_utf8(ROOT / "SKILL.md")
        referenced = set(re.findall(r"(?:scripts/)?(\w+_lint\.py|\w+_audit\.py|doctor\.py|style_profile\.py)", skill))
        self.assertTrue(referenced, "SKILL.md nennt kein Script")
        for name in sorted(referenced):
            self.assertIn(f"{BUNDLE_NAME}/scripts/{name}", self.names, name)

    def test_bundle_excludes_build_artifacts(self):
        for name in self.names:
            self.assertNotIn("__pycache__", name)
            self.assertFalse(name.endswith(".pyc"), name)
            self.assertFalse(name.endswith("build_skill_bundle.py"), name)

    def test_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as other:
            second = build_into(Path(other))
            self.assertEqual(self.bundle.read_bytes(), second.read_bytes())

    def test_bundle_runs_standalone(self):
        # The upload path has no repo around it: the extracted folder must be enough.
        with tempfile.TemporaryDirectory() as workdir:
            work = Path(workdir)
            with zipfile.ZipFile(self.bundle) as archive:
                archive.extractall(work)
            sample = work / "probe.md"
            sample.write_text(
                "Die Lage ist ernst. Die Lage ist klar. Die Lage ist bekannt.\n\n"
                "Es ist wichtig zu beachten, dass niemand widerspricht. "
                "Zusammenfassend bleibt wenig zu sagen.\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/humanizer_audit.py",
                    "--file",
                    str(sample),
                    "--mode",
                    "sachlich",
                    "--format",
                    "json",
                    "--no-profile",
                ],
                cwd=work / BUNDLE_NAME,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"preflight"', result.stdout)


if __name__ == "__main__":
    unittest.main()
