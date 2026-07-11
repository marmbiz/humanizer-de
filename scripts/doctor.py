#!/usr/bin/env python3
"""Diagnose the local Humanizer-DE installation without reading user text."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import print_json


SUCCESS_STATUSES = {"ok", "available", "active"}


def check(
    check_id: str,
    label: str,
    status: str,
    *,
    required: bool,
    version: str | None = None,
    detail: str | None = None,
    path: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": check_id,
        "label": label,
        "status": status,
        "required": required,
    }
    if version:
        item["version"] = version
    if detail:
        item["detail"] = detail
    if path:
        item["path"] = path
    return item


def run_command(
    command: list[str],
    *,
    input_text: str | None = None,
    timeout: int = 20,
) -> tuple[subprocess.CompletedProcess[str] | None, str | None]:
    try:
        result = subprocess.run(
            command,
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, str(error)
    return result, None


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_version(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = re.search(r"(?m)^\s{2}version:\s*['\"]?([^'\"\s]+)", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def package_checks(root: Path) -> tuple[list[dict[str, Any]], str | None]:
    required_paths = (
        root / "SKILL.md",
        root / "skills" / "humanizer-de" / "SKILL.md",
        root / "scripts" / "humanizer_audit.py",
        root / "references" / "patterns.md",
    )
    missing = [path.relative_to(root).as_posix() for path in required_paths if not path.is_file()]
    version = skill_version(root / "SKILL.md")
    base_status = "ok" if not missing and version else "error"
    base_detail = f"missing: {', '.join(missing)}" if missing else None

    checks = [
        check("base_skill", "Basis-Skill", base_status, required=True, version=version, detail=base_detail),
    ]

    manifests: dict[str, tuple[str, Path]] = {
        "claude_plugin": ("Claude-Paket", root / ".claude-plugin" / "plugin.json"),
        "codex_plugin": ("Codex-Paket", root / ".codex-plugin" / "plugin.json"),
    }
    versions: dict[str, str | None] = {"skill": version}
    for check_id, (label, path) in manifests.items():
        try:
            data = read_json(path)
            manifest_version = data.get("version")
            versions[check_id] = manifest_version
            status = "ok" if data.get("name") == "humanizer-de" and manifest_version else "error"
            checks.append(
                check(check_id, label, status, required=True, version=manifest_version, path=str(path))
            )
        except (OSError, json.JSONDecodeError) as error:
            versions[check_id] = None
            checks.append(check(check_id, label, "error", required=True, detail=str(error), path=str(path)))

    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    try:
        marketplace = read_json(marketplace_path)
        plugins = marketplace.get("plugins", [])
        marketplace_version = plugins[0].get("version") if plugins else None
    except (OSError, json.JSONDecodeError, AttributeError):
        marketplace_version = None
    versions["marketplace"] = marketplace_version

    known_versions = [value for value in versions.values() if value]
    synced = len(known_versions) == len(versions) and len(set(known_versions)) == 1
    checks.append(
        check(
            "version_sync",
            "Versions-Sync",
            "ok" if synced else "error",
            required=True,
            version=known_versions[0] if synced else None,
            detail=None if synced else json.dumps(versions, ensure_ascii=False, sort_keys=True),
        )
    )
    return checks, version


def select_python(root: Path) -> Path:
    candidates = (
        root / ".venv" / "bin" / "python",
        root / ".venv" / "Scripts" / "python.exe",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return Path(sys.executable)


def python_checks(root: Path) -> list[dict[str, Any]]:
    python = select_python(root)
    result, error = run_command([str(python), "--version"])
    if result is None or result.returncode != 0:
        detail = error or (result.stderr.strip() if result else "interpreter failed")
        return [check("python", "Python", "error", required=True, detail=detail, path=str(python))]
    version_output = (result.stdout or result.stderr).strip()
    version = version_output.removeprefix("Python ")
    checks = [check("python", "Python", "available", required=True, version=version, path=str(python))]

    probe = """
import importlib.metadata
import json

payload = {"spacy": None, "model": None, "model_error": None}
try:
    import spacy
    payload["spacy"] = importlib.metadata.version("spacy")
    try:
        nlp = spacy.load("de_core_news_sm")
        payload["model"] = nlp.meta.get("version")
    except Exception as error:
        payload["model_error"] = str(error)
except Exception as error:
    payload["spacy_error"] = str(error)
print(json.dumps(payload))
"""
    probe_result, probe_error = run_command([str(python), "-c", probe])
    payload: dict[str, Any] = {}
    if probe_result is not None and probe_result.returncode == 0:
        try:
            payload = json.loads(probe_result.stdout)
        except json.JSONDecodeError:
            payload = {}
    spacy_version = payload.get("spacy")
    model_version = payload.get("model")
    checks.append(
        check(
            "spacy",
            "spaCy",
            "available" if spacy_version else "missing",
            required=False,
            version=spacy_version,
            detail=payload.get("spacy_error") or probe_error,
        )
    )
    checks.append(
        check(
            "german_model",
            "Deutsch-Modell",
            "available" if model_version else "missing",
            required=False,
            version=model_version,
            detail=payload.get("model_error"),
        )
    )

    precise_result, precise_error = run_command(
        [
            str(python),
            str(root / "scripts" / "register_lint.py"),
            "--text",
            "Die Idee war neu. Sie überzeugte sofort.",
            "--precise",
        ]
    )
    precise: dict[str, Any] = {}
    if precise_result is not None and precise_result.returncode == 0:
        try:
            precise = json.loads(precise_result.stdout).get("precise", {})
        except json.JSONDecodeError:
            precise = {}
    active = precise.get("active") is True
    checks.append(
        check(
            "precise",
            "--precise",
            "active" if active else "inactive",
            required=False,
            detail=precise.get("reason") or precise_error,
        )
    )
    return checks


def hunspell_checks() -> list[dict[str, Any]]:
    binary = shutil.which("hunspell")
    if not binary:
        return [
            check("hunspell", "Hunspell", "missing", required=False),
            check("hunspell_de", "de_DE-Wörterbuch", "missing", required=False),
        ]

    version_result, version_error = run_command([binary, "--version"])
    version_line = ""
    if version_result is not None:
        version_line = (version_result.stdout or version_result.stderr).splitlines()[0]
    version_match = re.search(r"Hunspell\s+([0-9.]+)", version_line)
    version = version_match.group(1) if version_match else None
    hunspell_status = "available" if version_result is not None and version_result.returncode == 0 else "error"

    dictionary_result, dictionary_error = run_command(
        [binary, "-d", "de_DE", "-l"],
        input_text="Test\n",
    )
    dictionary_ok = dictionary_result is not None and dictionary_result.returncode == 0
    dictionary_detail = dictionary_error
    if dictionary_result is not None and not dictionary_ok:
        dictionary_detail = dictionary_result.stderr.strip() or dictionary_result.stdout.strip()
    return [
        check(
            "hunspell",
            "Hunspell",
            hunspell_status,
            required=False,
            version=version,
            detail=version_error,
            path=binary,
        ),
        check(
            "hunspell_de",
            "de_DE-Wörterbuch",
            "available" if dictionary_ok else "missing",
            required=False,
            detail=dictionary_detail,
        ),
    ]


def java_binary() -> str | None:
    candidates = []
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidates.append(Path(java_home) / "bin" / "java")
    candidates.extend(
        [
            Path("/opt/homebrew/opt/openjdk@17/bin/java"),
            Path("/usr/local/opt/openjdk@17/bin/java"),
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return shutil.which("java")


def languagetool_checks() -> list[dict[str, Any]]:
    binary = shutil.which("languagetool")
    lt_status = "missing"
    lt_version = None
    lt_detail = None
    if binary:
        result, error = run_command([binary, "--version"], timeout=30)
        if result is not None and result.returncode == 0:
            lt_status = "available"
            match = re.search(r"LanguageTool version\s+([^\s]+)", result.stdout or result.stderr)
            lt_version = match.group(1) if match else None
        else:
            lt_status = "error"
            lt_detail = error or (result.stderr.strip() if result else None)

    java = java_binary()
    java_status = "missing"
    java_version = None
    java_detail = None
    if java:
        result, error = run_command([java, "-version"])
        if result is not None and result.returncode == 0:
            java_status = "available"
            match = re.search(r'version "([^"]+)"', result.stderr or result.stdout)
            java_version = match.group(1) if match else None
        else:
            java_status = "error"
            java_detail = error or (result.stderr.strip() if result else None)
    return [
        check(
            "languagetool",
            "LanguageTool",
            lt_status,
            required=False,
            version=lt_version,
            detail=lt_detail,
            path=binary,
        ),
        check(
            "java",
            "Java",
            java_status,
            required=False,
            version=java_version,
            detail=java_detail,
            path=java,
        ),
    ]


def build_report(root: Path = ROOT) -> dict[str, Any]:
    package_items, version = package_checks(root)
    checks = package_items + python_checks(root) + hunspell_checks() + languagetool_checks()
    required_checks = [item for item in checks if item["required"]]
    optional_checks = [item for item in checks if not item["required"]]
    ok = all(item["status"] in SUCCESS_STATUSES for item in required_checks)
    full = ok and all(item["status"] in SUCCESS_STATUSES for item in optional_checks)
    return {
        "name": "humanizer-de",
        "version": version,
        "ok": ok,
        "full": full,
        "summary": "full" if full else ("base_only" if ok else "error"),
        "privacy": "No user text or content files were read.",
        "checks": checks,
    }


def format_report(report: dict[str, Any]) -> str:
    lines = ["Humanizer-DE Doctor", f"Version: {report.get('version') or 'unknown'}", ""]
    width = max((len(item["label"]) for item in report["checks"]), default=0)
    for item in report["checks"]:
        extras = []
        if item.get("version"):
            extras.append(str(item["version"]))
        if item.get("path"):
            extras.append(str(item["path"]))
        if item.get("detail"):
            extras.append(str(item["detail"]))
        suffix = f" · {' · '.join(extras)}" if extras else ""
        lines.append(f"{item['label']:<{width}}  {item['status'].upper():<9}{suffix}")
    lines.extend(
        [
            "",
            f"Gesamt: {report['summary'].upper()}",
            "Datenschutz: Es wurden keine Nutzertexte oder Inhaltsdateien gelesen.",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose the local Humanizer-DE toolchain.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument(
        "--require-full",
        action="store_true",
        help="Exit 1 unless every optional tool is available and --precise is active.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report()
    if args.json:
        print_json(report)
    else:
        print(format_report(report))
    if not report["ok"]:
        return 1
    if args.require_full and not report["full"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
