#!/usr/bin/env python3
"""Portable JSON output helpers for command-line tools."""

from __future__ import annotations

import json
import sys
from typing import Any


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
