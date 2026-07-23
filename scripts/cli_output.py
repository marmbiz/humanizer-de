#!/usr/bin/env python3
"""Portable JSON output helpers for command-line tools."""

from __future__ import annotations

import json
import sys
from typing import Any


def resolve_exit_code(policy: str, findings: list[dict]) -> int:
    if policy == "never":
        return 0
    if policy == "blocker":
        return 1 if any(item.get("severity") == "blocker" for item in findings) else 0
    return 1 if findings else 0


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
