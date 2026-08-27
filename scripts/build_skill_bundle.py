#!/usr/bin/env python3
"""Build the uploadable skill bundle (ZIP) for claude.ai and other Skill hosts."""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import handle_cli_input_errors, print_json  # noqa: E402

BUNDLE_NAME = "humanizer-de"
DEFAULT_OUTPUT = ROOT / "dist" / f"{BUNDLE_NAME}.zip"

# Everything is listed by name: a directory sweep would pick up untracked files and make
# the archive depend on the working tree instead of the commit.
BUNDLE_FILES = (
    "SKILL.md",
    "LICENSE",
    "NOTICE",
    "assets/checkliste-ki-tells.md",
)

# The nine files SKILL.md routes into.
BUNDLE_REFERENCES = (
    "de-naturalness.md",
    "decision-tables.md",
    "evidence-ledger.md",
    "patterns.md",
    "qgir.md",
    "quality-rubric.md",
    "register-profiles.md",
    "style-targets.json",
    "user-profile.md",
)

# Scripts SKILL.md or its pipeline calls, plus the three modules they import. Repo tooling stays out:
# it needs tests/ fixtures or an external CLI and only fails inside the bundle.
BUNDLE_SCRIPTS = (
    "cli_output.py",
    "doctor.py",
    "evidence_lint.py",
    "german_pattern_lint.py",
    "humanizer_audit.py",
    "register_lint.py",
    "rhythm_lint.py",
    "spell_lint.py",
    "style_profile.py",
    "syntax_lint.py",
    "text_scope.py",
    "unicode_lint.py",
    "verify_changes.py",
)

# Fixed timestamp keeps repeated builds byte-identical for the same input.
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def bundle_paths() -> tuple[str, ...]:
    return (
        BUNDLE_FILES
        + tuple(f"references/{name}" for name in BUNDLE_REFERENCES)
        + tuple(f"scripts/{name}" for name in BUNDLE_SCRIPTS)
    )


def collect_members(root: Path = ROOT) -> list[tuple[Path, str]]:
    """Return (source path, archive name) pairs, sorted for a stable archive."""
    members: list[tuple[Path, str]] = []
    for name in bundle_paths():
        source = root / name
        if not source.is_file():
            raise FileNotFoundError(f"Bundle-Datei fehlt: {name}")
        members.append((source, f"{BUNDLE_NAME}/{name}"))
    members.sort(key=lambda member: member[1])
    return members


def build(output: Path, root: Path = ROOT) -> dict[str, object]:
    members = collect_members(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for source, arcname in members:
            info = zipfile.ZipInfo(arcname, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            # Pinned: ZipInfo defaults this to the build platform, which would give
            # Windows builds a different checksum for identical content.
            info.create_system = 3
            archive.writestr(info, source.read_bytes())
    return {
        "output": str(output),
        "file_count": len(members),
        "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Zielpfad des Archivs (Standard: {DEFAULT_OUTPUT.relative_to(ROOT)})",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


@handle_cli_input_errors
def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result = build(args.output)
    if args.format == "json":
        print_json(result)
    else:
        print(f"{result['output']} ({result['file_count']} Dateien, {result['bytes']} Bytes)")
        print(f"sha256  {result['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
