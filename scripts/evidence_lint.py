#!/usr/bin/env python3
"""Conservatively compare before/after passages for factual anchor drift."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import print_json, resolve_exit_code


SYNTAX_SCRIPT = SCRIPT_DIR / "syntax_lint.py"
_SYNTAX_LINT = None
LEDGER_SCHEMA_VERSION = 2
LEGACY_LEDGER_SCHEMA_VERSIONS = {1}

ANCHOR_PATTERNS = {
    "number": re.compile(
        r"(?<![\w.,])"
        r"(?:(?:mindestens|höchstens|hoechstens|mehr\s+als|weniger\s+als|über|ueber|unter|bis\s+zu)\s+|[+\-−]\s*|[vV])?"
        r"\d+(?:[.,]\d+)*"
        r"(?:\s*(?:%|Prozent|€|Euro|EUR|km|kg|Mio\.?|Millionen))?"
        r"(?!\w)",
        re.IGNORECASE,
    ),
    "date": re.compile(
        r"\b(?:\d{1,2}\.\s*(?:Januar|Februar|März|Maerz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4}|\d{4}-\d{2}-\d{2})\b",
        re.IGNORECASE,
    ),
    "url": re.compile(r"https?://[^\s<>)]+"),
    "doi": re.compile(r"\b(?:doi:\s*)?10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b", re.IGNORECASE),
    "paragraph": re.compile(r"§+\s*\d+[a-zA-Z]*(?:\s*Abs\.\s*\d+)?"),
    "code": re.compile(r"`[^`\n]+`"),
}

QUOTE_PATTERNS = (
    re.compile(r"„([^„“]{3,})“"),
    re.compile(r"‚([^‚‘]{3,})‘"),
    re.compile(r"“([^“”]{3,})”"),
    re.compile(r"«([^«»]{3,})»"),
    re.compile(r"»([^«»]{3,})«"),
    re.compile(r"‹([^‹›]{3,})›"),
    re.compile(r"›([^‹›]{3,})‹"),
    re.compile(r'"([^"]{3,})"'),
    re.compile(r"(?<!\w)'([^']{3,})'(?!\w)"),
    # Preserve quoted content even when Unicode lint still needs to repair a
    # mismatched closer. Valid pairs above remain the preferred extraction.
    re.compile(r'["„“”«»‹›]([^"„“”«»‹›]{3,})["„“”«»‹›]'),
    re.compile(r"(?<!\w)[‚‘’']([^‚‘’']{3,})[‚‘’'](?!\w)"),
)

# Schema-v1 ledgers contain anchors produced by these exact patterns. Keep
# their after-side extraction stable even as the current extractor improves.
LEGACY_ANCHOR_PATTERNS = {
    "number": re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:%|Prozent|Euro|EUR|km|kg|Mio\.?|Millionen)?\b", re.IGNORECASE),
    "date": re.compile(
        r"\b(?:\d{1,2}\.\s*(?:Januar|Februar|März|Maerz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4}|\d{4}-\d{2}-\d{2})\b",
        re.IGNORECASE,
    ),
    "url": re.compile(r"https?://[^\s<>)]+"),
    "doi": re.compile(r"\b(?:doi:\s*)?10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b", re.IGNORECASE),
    "paragraph": re.compile(r"§+\s*\d+[a-zA-Z]*(?:\s*Abs\.\s*\d+)?"),
    "code": re.compile(r"`[^`\n]+`"),
    "quote": re.compile(r'["„“‚‘”\']([^"„“‚‘”\']{3,})["„“‚‘”\']'),
}

AUTHORITY_MARKERS = {
    "strong": {
        "belegt",
        "beweist",
        "zeigt",
        "nachweislich",
        "muss",
        "immer",
        "zweifellos",
        "zweifelsfrei",
        "spricht klar dafür",
        "spricht klar dafuer",
        "spricht eindeutig dafür",
        "spricht eindeutig dafuer",
    },
    "weak": {
        "kann",
        "koennte",
        "könnte",
        "vermutlich",
        "moeglicherweise",
        "möglicherweise",
        "laut",
        "scheint",
        "nicht sicher",
        "unsicher",
        "unklar",
        "fraglich",
        "womöglich",
        "womoeglich",
        "eventuell",
        "dürfte",
        "duerfte",
        "unter umständen",
        "unter umstaenden",
        "ich vermute",
        "ich glaube",
    },
}
DIRECTION_MARKERS = {
    "increase": {
        "erhoeht",
        "erhoehte",
        "erhöht",
        "erhöhte",
        "gestiegen",
        "stieg",
        "steigt",
        "verbessert",
        "verbesserte",
        "zunahm",
    },
    "decrease": {
        "gesunken",
        "nahm ab",
        "reduziert",
        "reduzierte",
        "sank",
        "senkt",
        "senkte",
        "verringert",
        "verringerte",
    },
}

CAPITALIZED_RE = re.compile(r"\b(?:[A-ZÄÖÜ][\wÄÖÜäöüß-]+(?:\s+[A-ZÄÖÜ][\wÄÖÜäöüß-]+){0,3})\b")
DETERMINERS = {
    "der", "die", "das", "des", "dem", "den",
    "ein", "eine", "einer", "eines", "einem", "einen",
    "im", "am", "zum", "zur", "beim", "vom", "ins", "ans", "aufs",
}
ABSTRACT_NOUN_STOPLIST = {
    "lösung", "loesung", "problem", "priorität", "prioritaet", "herausforderung",
    "bedeutung", "aspekt", "aspekte", "faktor", "faktoren", "prozess", "prozesse",
    "maßnahme", "massnahme", "ziel", "ziele", "ansatz", "ergebnis", "ergebnisse",
    "vorteil", "vorteile", "nachteil", "nachteile", "grundlage", "rahmen",
    "bereich", "bereiche", "thema", "themen", "inhalt", "inhalte", "beispiel",
    "beispiele", "möglichkeit", "moeglichkeit", "entwicklung", "zukunft",
}
COMMON_SENTENCE_STARTS = {
    "Der",
    "Die",
    "Das",
    "Ein",
    "Eine",
    "Im",
    "In",
    "Nach",
    "Vor",
    "Zu",
    "Für",
    "Mit",
    "Ohne",
    "Sie",
    "Ihnen",
    "Ihr",
    "Ihre",
}


def load_syntax_lint():
    global _SYNTAX_LINT
    if _SYNTAX_LINT is not None:
        return _SYNTAX_LINT

    module = sys.modules.get("syntax_lint")
    if module is None:
        spec = importlib.util.spec_from_file_location("syntax_lint", SYNTAX_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        sys.modules["syntax_lint"] = module
        spec.loader.exec_module(module)

    _SYNTAX_LINT = module
    return module


def precise_context(precise: bool) -> tuple[dict | None, object | None]:
    if not precise:
        return None, None

    syntax_lint = load_syntax_lint()
    if not hasattr(syntax_lint, "_HUMANIZER_PRECISE_CACHE"):
        syntax_lint._HUMANIZER_PRECISE_CACHE = syntax_lint.load_nlp()

    nlp, reason = syntax_lint._HUMANIZER_PRECISE_CACHE
    if nlp is None:
        return {"requested": True, "active": False, "reason": reason or "spacy_missing"}, None
    return {"requested": True, "active": True}, nlp


def precise_status(precise: bool) -> dict | None:
    status, _ = precise_context(precise)
    return status


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).strip(".,;:()[]")


def name_key(value: str) -> str:
    return value.casefold()


def token_in_named_entity(doc: object, start: int, end: int) -> bool:
    for ent in doc.ents:
        if ent.label_ in {"PER", "ORG", "LOC", "MISC"} and ent.start_char <= start and end <= ent.end_char:
            return True
    return False


def proper_name_anchors(text: str, nlp: object | None = None) -> set[str]:
    # Known default-path gap: single-token common nouns after verbs that are
    # not in the stoplist (e.g. "hat Relevanz") still slip through as
    # proper_name; --precise can filter that class with spaCy NER.
    names: set[str] = set()
    doc = nlp(text) if nlp is not None else None
    for match in CAPITALIZED_RE.finditer(text):
        raw = match.group(0)
        tokens = raw.split()
        pos = 0
        while tokens and (tokens[0] in COMMON_SENTENCE_STARTS or tokens[0].lower() in DETERMINERS):
            pos = raw.index(tokens[0], pos) + len(tokens[0])
            tokens = tokens[1:]
        if not tokens:
            continue
        value = normalize(" ".join(tokens))
        if len(value) <= 2:
            continue
        if value.lower() in {"prozent", "euro"}:
            continue
        if len(tokens) >= 2:
            names.add(value)
            continue
        token = tokens[0]
        if re.search(r"\d", token) or token[1:] != token[1:].lower():
            names.add(value)
            continue
        token_start = match.start() + raw.index(token, pos)
        token_end = token_start + len(token)
        prefix = text[:token_start]
        preceding = re.search(r"([\wÄÖÜäöüß-]+)\s+$", prefix)
        if preceding and preceding.group(1).lower() in DETERMINERS:
            continue
        if not prefix.strip() or re.search(r"[.!?:]\s+$", prefix) or re.search(r"\n[ \t]*$", prefix):
            continue
        if token.lower() in ABSTRACT_NOUN_STOPLIST:
            continue
        if doc is not None and not token_in_named_entity(doc, token_start, token_end):
            continue
        names.add(value)
    return names


def anchors(text: str, nlp: object | None = None) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {kind: set() for kind in anchor_kinds()}
    for kind, pattern in ANCHOR_PATTERNS.items():
        for match in pattern.finditer(text):
            normalized = normalize(match.group(0))
            if normalized:
                result[kind].add(normalized)

    for pattern in QUOTE_PATTERNS:
        for match in pattern.finditer(text):
            normalized = normalize(match.group(1))
            if normalized:
                result["quote"].add(normalized)

    result["proper_name"] = proper_name_anchors(text, nlp=nlp)
    return result


def legacy_anchors(text: str, nlp: object | None = None) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {kind: set() for kind in anchor_kinds()}
    for kind, pattern in LEGACY_ANCHOR_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(1) if kind == "quote" else match.group(0)
            normalized = normalize(value)
            if normalized:
                result[kind].add(normalized)
    result["proper_name"] = proper_name_anchors(text, nlp=nlp)
    return result


def authority_profile(text: str) -> dict[str, set[str]]:
    lowered = text.lower()
    return {
        level: {marker for marker in markers if re.search(rf"\b{re.escape(marker)}\b", lowered)}
        for level, markers in AUTHORITY_MARKERS.items()
    }


def authority_level(profile: dict[str, set[str]]) -> int:
    """Return the assertion level; hedges are evaluated separately."""
    return 1 if profile["strong"] else 0


def direction_profile(text: str) -> set[str]:
    lowered = text.lower()
    result: set[str] = set()
    for direction, markers in DIRECTION_MARKERS.items():
        if any(re.search(rf"\b{re.escape(marker)}\b", lowered) for marker in markers):
            result.add(direction)
    return result


def add_finding(findings: list[dict], severity: str, kind: str, message: str, values: list[str]) -> None:
    findings.append({"severity": severity, "kind": kind, "message": message, "values": sorted(values)})


def anchor_kinds() -> tuple[str, ...]:
    return tuple(ANCHOR_PATTERNS) + ("quote", "proper_name")


def serializable_anchors(anchor_map: dict[str, set[str]]) -> dict[str, list[str]]:
    return {kind: sorted(anchor_map.get(kind, set())) for kind in anchor_kinds()}


def anchor_counts(anchor_map: dict[str, set[str]]) -> dict[str, int]:
    return {kind: len(anchor_map.get(kind, set())) for kind in anchor_kinds()}


def add_anchor_findings(
    findings: list[dict],
    before_anchors: dict[str, set[str]],
    after_anchors: dict[str, set[str]],
) -> None:
    hard_kinds = {"number", "date", "url", "doi", "paragraph", "code", "quote"}
    for kind in sorted(anchor_kinds()):
        if kind == "proper_name":
            # Compare capitalization-insensitively, but report the original
            # surface forms. Suffix stripping would hide real name changes.
            before_keys = {name_key(value) for value in before_anchors.get(kind, set())}
            after_keys = {name_key(value) for value in after_anchors.get(kind, set())}
            removed = {value for value in before_anchors.get(kind, set()) if name_key(value) not in after_keys}
            added = {value for value in after_anchors.get(kind, set()) if name_key(value) not in before_keys}
        else:
            removed = before_anchors.get(kind, set()) - after_anchors.get(kind, set())
            added = after_anchors.get(kind, set()) - before_anchors.get(kind, set())
        severity = "blocker" if kind in hard_kinds else "warning"
        if removed:
            add_finding(findings, severity, f"removed_{kind}", f"{kind} anchor removed or changed.", list(removed))
        if added:
            add_finding(findings, severity, f"added_{kind}", f"New {kind} anchor introduced.", list(added))


def lint_with_anchors(
    before_anchors: dict[str, set[str]],
    after: str,
    precise: bool = False,
    legacy: bool = False,
) -> list[dict]:
    _, nlp = precise_context(precise)
    findings: list[dict] = []
    after_anchors = legacy_anchors(after, nlp=nlp) if legacy else anchors(after, nlp=nlp)
    add_anchor_findings(findings, before_anchors, after_anchors)
    return findings


def lint(before: str, after: str, precise: bool = False) -> list[dict]:
    _, nlp = precise_context(precise)
    findings: list[dict] = []
    add_anchor_findings(findings, anchors(before, nlp=nlp), anchors(after, nlp=nlp))

    before_auth = authority_profile(before)
    after_auth = authority_profile(after)
    stronger = after_auth["strong"] if authority_level(after_auth) > authority_level(before_auth) else set()
    weaker_removed = before_auth["weak"] - after_auth["weak"]
    if stronger:
        add_finding(findings, "blocker", "authority_strengthened", "Authority marker was strengthened.", list(stronger))
    if weaker_removed and after_auth["strong"]:
        add_finding(findings, "warning", "hedge_removed", "Hedging may have been removed.", list(weaker_removed))

    before_direction = direction_profile(before)
    after_direction = direction_profile(after)
    if (
        ("increase" in before_direction and "decrease" in after_direction)
        or ("decrease" in before_direction and "increase" in after_direction)
    ):
        add_finding(
            findings,
            "blocker",
            "claim_direction_changed",
            "Claim direction changed between increase and decrease.",
            sorted(before_direction | after_direction),
        )

    return findings


def load_text(value: str | None, path: Path | None) -> str:
    if path is not None:
        return path.read_text(encoding="utf-8")
    return value or ""


def extraction_policy(precise: bool) -> tuple[dict[str, str], object | None]:
    _, nlp = precise_context(precise)
    if nlp is None:
        return {"mode": "default"}, None

    meta = getattr(nlp, "meta", {})
    return {
        "mode": "spacy_ner",
        "model": str(meta.get("name") or "unknown"),
        "model_version": str(meta.get("version") or "unknown"),
    }, nlp


def write_ledger(text: str, path: Path, precise: bool = False) -> dict[str, set[str]]:
    policy, nlp = extraction_policy(precise)
    before_anchors = anchors(text, nlp=nlp)
    data = {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "extraction_policy": policy,
        "anchors": serializable_anchors(before_anchors),
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return before_anchors


def load_ledger_document(path: Path) -> tuple[dict[str, set[str]], dict[str, str] | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"{path}: cannot read ledger: {exc.strerror}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path}: ledger must be a JSON object")
    schema_version = data.get("schema_version")
    if schema_version not in LEGACY_LEDGER_SCHEMA_VERSIONS | {LEDGER_SCHEMA_VERSION}:
        raise ValueError(f"{path}: unsupported schema_version {data.get('schema_version')!r}")
    policy = data.get("extraction_policy")
    if schema_version == LEDGER_SCHEMA_VERSION:
        if not isinstance(policy, dict) or policy.get("mode") not in {"default", "spacy_ner"}:
            raise ValueError(f"{path}: missing or invalid 'extraction_policy' object")
        expected_keys = {"mode"} if policy["mode"] == "default" else {"mode", "model", "model_version"}
        if set(policy) != expected_keys or not all(isinstance(value, str) for value in policy.values()):
            raise ValueError(f"{path}: invalid 'extraction_policy' fields")
    else:
        policy = None
    ledger_anchors = data.get("anchors")
    if not isinstance(ledger_anchors, dict):
        raise ValueError(f"{path}: missing or invalid 'anchors' object")

    missing = [kind for kind in anchor_kinds() if kind not in ledger_anchors]
    if missing:
        raise ValueError(f"{path}: ledger anchors missing keys: {', '.join(missing)}")

    result: dict[str, set[str]] = {}
    for kind in anchor_kinds():
        values = ledger_anchors[kind]
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise ValueError(f"{path}: ledger anchors.{kind} must be a list of strings")
        result[kind] = set(values)
    return result, policy


def check_fixture(path: Path, precise: bool = False) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings = lint(data["before"], data["after"], precise=precise)
    expected = data.get("expect_kinds")
    ok = True
    if expected is not None:
        actual = {item["kind"] for item in findings}
        ok = actual == set(expected)
    return [{"fixture": str(path), "ok": ok, "findings": findings}]


def check_fixtures(path: Path, precise: bool = False) -> list[dict]:
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    if not files or not all(file_path.is_file() for file_path in files):
        raise ValueError(f"{path}: no JSON fixture files found")
    return [item for file_path in files for item in check_fixture(file_path, precise=precise)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare before/after passages for factual anchor drift.")
    parser.add_argument("--before", help="Before passage as inline text.")
    parser.add_argument("--after", help="After passage as inline text.")
    parser.add_argument("--before-file", type=Path, help="Read before passage from file.")
    parser.add_argument("--after-file", type=Path, help="Read after passage from file.")
    parser.add_argument("--write-ledger", type=Path, help="Write original before anchors to a JSON ledger and exit.")
    parser.add_argument("--ledger", type=Path, help="Read original anchors from a JSON ledger instead of --before.")
    parser.add_argument("--fixture", type=Path, help="JSON fixture file or directory.")
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    parser.add_argument("--fail-on", choices=["never", "blocker", "any"], default="blocker")
    args = parser.parse_args(argv)
    if args.before is not None and args.before_file is not None:
        parser.error("--before and --before-file are mutually exclusive")
    if args.after is not None and args.after_file is not None:
        parser.error("--after and --after-file are mutually exclusive")
    if args.ledger and (args.before is not None or args.before_file is not None):
        parser.error("--ledger cannot be combined with --before or --before-file")
    if args.ledger and args.write_ledger:
        parser.error("--ledger cannot be combined with --write-ledger")
    if args.fixture and (args.ledger or args.write_ledger):
        parser.error("--fixture cannot be combined with --ledger or --write-ledger")
    has_before = args.before is not None or args.before_file is not None
    has_after = args.after is not None or args.after_file is not None
    if args.fixture:
        if has_before or has_after:
            parser.error("--fixture cannot be combined with before/after arguments")
    elif args.write_ledger:
        if not has_before:
            parser.error("--write-ledger requires --before or --before-file")
        if has_after:
            parser.error("--write-ledger cannot be combined with --after or --after-file")
    elif args.ledger:
        if not has_after:
            parser.error("--ledger requires --after or --after-file")
    elif not has_before or not has_after:
        parser.error("pair mode requires one before source and one after source")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.fixture:
        try:
            results = check_fixtures(args.fixture, precise=args.precise)
        except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        report = {"ok": all(item["ok"] for item in results), "results": results}
        status = precise_status(args.precise)
        if status is not None:
            report["precise"] = status
        print_json(report)
        return 0 if all(item["ok"] for item in results) else 1

    if args.write_ledger:
        before = load_text(args.before, args.before_file)
        before_anchors = write_ledger(before, args.write_ledger, precise=args.precise)
        report = {
            "ok": True,
            "ledger": str(args.write_ledger),
            "anchor_counts": anchor_counts(before_anchors),
        }
        if args.precise:
            report["precise_scope"] = "before_anchors"
        status = precise_status(args.precise)
        if status is not None:
            report["precise"] = status
        print_json(report)
        return 0

    after = load_text(args.after, args.after_file)
    if args.ledger:
        try:
            before_anchors, ledger_policy = load_ledger_document(args.ledger)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        current_policy, _ = extraction_policy(args.precise)
        if ledger_policy is not None and ledger_policy != current_policy:
            print(
                "error: ledger extraction policy does not match this diff run "
                f"(ledger={ledger_policy!r}, current={current_policy!r})",
                file=sys.stderr,
            )
            return 2
        findings = lint_with_anchors(
            before_anchors,
            after,
            precise=args.precise,
            legacy=ledger_policy is None,
        )
        report = {
            "ok": not findings,
            "findings": findings,
            "ledger": str(args.ledger),
            "ledger_extraction_policy": ledger_policy or "legacy_unknown",
        }
        if args.precise:
            report["precise_scope"] = "after_anchors"
    else:
        before = load_text(args.before, args.before_file)
        findings = lint(before, after, precise=args.precise)
        report = {"ok": not findings, "findings": findings}
    status = precise_status(args.precise)
    if status is not None:
        report["precise"] = status
    print_json(report)
    return resolve_exit_code(args.fail_on, findings)


if __name__ == "__main__":
    raise SystemExit(main())
