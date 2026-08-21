#!/usr/bin/env python3
"""Portable JSON output helpers for command-line tools."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from functools import wraps
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable


class CliInputError(ValueError):
    """Invalid or unreadable user-supplied CLI input."""


def handle_cli_input_errors(main: Callable[..., int]) -> Callable[..., int]:
    @wraps(main)
    def wrapped(*args: Any, **kwargs: Any) -> int:
        try:
            return main(*args, **kwargs)
        except SystemExit as error:
            if error.code != 2:
                raise
            return 2
        except CliInputError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2

    return wrapped


def require_file(
    parser: argparse.ArgumentParser,
    path: Path | None,
    option: str,
) -> None:
    if path is not None and not path.is_file():
        parser.error(f"{option} requires an existing file: {path}")


def read_user_text(path: Path) -> str:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return handle.read()
    except UnicodeError as error:
        raise CliInputError(f"{path}: file is not valid UTF-8") from error
    except OSError as error:
        reason = error.strerror or str(error)
        raise CliInputError(f"{path}: cannot read file: {reason}") from error


def atomic_write_text(path: Path, text: str, *, newline: str | None = None) -> None:
    temp_path = None
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    try:
        with NamedTemporaryFile(
            "w", encoding="utf-8", newline=newline, dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(text)
        if mode is not None:
            os.chmod(temp_path, mode)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def read_json_object(
    path: Path,
    *,
    label: str = "JSON file",
    required: tuple[str, ...] = (),
) -> dict:
    try:
        data = json.loads(read_user_text(path))
    except json.JSONDecodeError as error:
        raise CliInputError(f"{path}: invalid {label} JSON: {error.msg}") from error
    if not isinstance(data, dict):
        raise CliInputError(f"{path}: {label} must be a JSON object")
    missing = [key for key in required if key not in data]
    if missing:
        raise CliInputError(f"{path}: {label} missing required key: {', '.join(missing)}")
    return data


def resolve_exit_code(policy: str, findings: list[dict]) -> int:
    if policy == "never":
        return 0
    if policy == "blocker":
        return 1 if any(not item.get("advisory") and item.get("severity") == "blocker" for item in findings) else 0
    return 1 if any(not item.get("advisory") for item in findings) else 0


def json_for_stdout(payload: Any, *, indent: int = 2, sort_keys: bool = False) -> str:
    """Keep readable Unicode where supported and fall back to ASCII-safe JSON."""
    rendered = json.dumps(payload, ensure_ascii=False, indent=indent, sort_keys=sort_keys)
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding:
        try:
            rendered.encode(encoding)
        except (LookupError, UnicodeEncodeError):
            rendered = json.dumps(payload, ensure_ascii=True, indent=indent, sort_keys=sort_keys)
    return rendered


def print_json(payload: Any, *, indent: int = 2, sort_keys: bool = False) -> None:
    print(json_for_stdout(payload, indent=indent, sort_keys=sort_keys))


def text_for_stdout(value: str) -> str:
    """Escape characters that the active stdout encoding cannot represent."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        value.encode(encoding)
    except LookupError:
        return value.encode("ascii", errors="backslashreplace").decode("ascii")
    except UnicodeEncodeError:
        return value.encode(encoding, errors="backslashreplace").decode(encoding)
    return value


def print_text(value: str) -> None:
    print(text_for_stdout(value))
