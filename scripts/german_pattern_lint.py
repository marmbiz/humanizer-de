#!/usr/bin/env python3
"""Report German naturalness pattern clusters for Humanizer-de."""

from __future__ import annotations

import argparse
import bisect
import functools
import importlib.util
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_output import (
    handle_cli_input_errors,
    print_json,
    read_json_object,
    read_user_text,
    require_file,
    resolve_exit_code,
)
import evidence_lint
import text_scope


REGISTER_SCRIPT = SCRIPT_DIR / "register_lint.py"
register_spec = importlib.util.spec_from_file_location("register_lint", REGISTER_SCRIPT)
register_lint = importlib.util.module_from_spec(register_spec)
register_spec.loader.exec_module(register_lint)

SYNTAX_SCRIPT = SCRIPT_DIR / "syntax_lint.py"
_SYNTAX_LINT = None


AI_MARKERS = (
    "beleuchten",
    "eintauchen",
    "unterstreichen",
    "aufzeigen",
    "spannend",
    "entscheidend",
    "maßgeblich",
    "massgeblich",
    "nahtlos",
    "vielschichtig",
    "facettenreich",
    "dynamisch",
    "ganzheitlich",
    "maßgeschneidert",
    "massgeschneidert",
    "digitale landschaft",
    "zusammenspiel",
)
AD_QUANTITY_PATTERN = (
    r"(?:(?i:über|ueber|mehr\s+als)\s+)?\d+(?:[.\u00a0 ]\d{3})*"
    r"(?![ \t]*(?:(?i:prozent)\b|%))"
)
AD_AUDIENCE_PATTERN = (
    r"(?:ihnen|uns|(?:(?:den|der)\s+)?"
    rf"(?:{AD_QUANTITY_PATTERN}\s+)?"
    r"(?:kunden|kundinnen|kundschaft|nutzer(?:n|innen)?|nutzerschaft|"
    r"betriebe(?:n)?|unternehmen|familien|mitglieder(?:n)?|community|"
    r"anwender(?:n|innen)?))"
)
AD_SOCIAL_PROOF_RES = (
    re.compile(
        rf"\b{AD_QUANTITY_PATTERN}\s+[A-ZÄÖÜ][^\W\d_]*"
        r"(?:[ \t]+[^\W\d_]+){0,4}[ \t]+"
        r"(?:(?i:können|koennen)\s+nicht\s+(?i:irren)"
        r"|(?i:vertrauen)(?:\s+(?i:bereits))?)\b"
    ),
    re.compile(rf"\b{AD_QUANTITY_PATTERN}\s+(?i:zufriedene\s+kunden)\b"),
    re.compile(
        rf"\b(?:schließen|schliessen)\s+sie\s+sich\s+{AD_AUDIENCE_PATTERN}\s+an\b",
        re.IGNORECASE,
    ),
)
AD_SECTION_RE = re.compile(
    r"(?:das\s+sagen\s+unsere\s+kunden"
    r"|was\s+unsere\s+kunden\s+sagen"
    r"|kundenstimmen"
    r"|stimmen\s+unserer\s+kunden"
    r"|das\s+sagen\s+kunden\s+(?:über|ueber)\s+uns"
    r"|(?:überzeugen|ueberzeugen)\s+sie\s+sich\s+selbst"
    r"|warum\s+.+?\s+die\s+richtige\s+wahl(?:\s+(?:für|fuer)\s+.+?)?\s+ist"
    r"|ihre\s+vorteile\s+auf\s+einen\s+blick)",
    re.IGNORECASE,
)
MARKDOWN_HEADING_RE = re.compile(
    r"^[ \t]{0,3}#{1,6}[ \t]+(?P<title>.*?)(?:[ \t]+#+)?[ \t]*$"
)
AD_CTA_RES = (
    re.compile(r"\bregistrieren\s+sie\s+sich\s+(?:noch\s+heute|jetzt)\b", re.IGNORECASE),
    re.compile(r"\bjetzt\s+(?:kostenlos\s+)?testen\b", re.IGNORECASE),
    re.compile(r"\bstarten\s+sie\s+(?:jetzt|heute)\b", re.IGNORECASE),
    re.compile(r"\bsichern\s+sie\s+sich\b", re.IGNORECASE),
    re.compile(r"\btesten\s+sie\b[^.!?\r\n]{1,80}?\bkostenlos\b", re.IGNORECASE),
)
COPULA_AVOIDANCE = (
    "fungiert als",
    "dient als",
    "verfügt über",
    "verfuegt ueber",
    "zeichnet sich",
    "erweist sich als",
    "repräsentiert",
    "repraesentiert",
)
ABSTRACTA = (
    "maßnahmen",
    "massnahmen",
    "aspekte",
    "lösungen",
    "loesungen",
    "herausforderungen",
    "faktoren",
    "prozesse",
)
# Marker, die der Standard-Stamm nicht erreicht: Er streicht nur ein End-"en",
# deshalb bleiben die beiden Formen auf "e" im Plural stecken. "prozess" allein
# waere zu weit und trafe auch Prozessor und prozessual.
MARKER_PATTERNS = {
    "aspekte": re.compile(r"\baspekt(?:e|en|es)?\b", re.IGNORECASE),
    "prozesse": re.compile(r"\bprozess(?:e|en|es)?\b", re.IGNORECASE),
}
NEGATION_PARALLELISM_RES = (
    re.compile(
        r"\b[Kk]eine?[nmrs]?\b[^,.;:!?\r\n]{1,45},\s*"
        r"[Kk]eine?[nmrs]?\b[^,.;:!?\r\n]{0,45}"
    ),
    re.compile(
        r"\b[Nn]icht\b[^,.;:!?\r\n]{1,45},\s*"
        r"[Nn]icht\b[^,.;:!?\r\n]{0,45}"
    ),
)
FACTUAL_CONTRAST_VALUE_PATTERN = (
    r"(?:(?:am|im|um|ab|seit)\s+)?(?:"
    r"montags?|dienstags?|mittwochs?|donnerstags?|freitags?|samstags?|sonntags?"
    r"|(?:januar|februar|märz|maerz|april|mai|juni|juli|august|september|oktober|november|dezember)"
    r"(?:\s+\d{4})?"
    r"|heute|morgen|gestern|\d{1,4}(?:[:/-]\d{1,4})*"
    r"(?:\s*(?:[%€]|[A-Za-zÄÖÜäöüß]{1,20}\.?)(?:/[A-Za-zÄÖÜäöüß]{1,10})?)?"
    r")"
)
ANTITHESIS_OPERAND_PATTERN = rf"(?:{FACTUAL_CONTRAST_VALUE_PATTERN}|[0-9A-Za-zÄÖÜäöüß-]+)"
ANTITHESIS_RES = (
    re.compile(
        r"\bnicht\b(?!\s+(?:nur|allein|bloß|bloss|ausschließlich|ausschliesslich)\b)"
        r"(?P<left>[^,.;:!?\r\n]{1,80})"
        r"(?:,\s*|[^\S\r\n]+(?:--?|[–—])[^\S\r\n]+)"
        r"sondern\b(?!\s+auch\b)(?P<right>[^,.;:!?\r\n]{1,80})",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b(?P<left>{ANTITHESIS_OPERAND_PATTERN})\s+und\s+"
        rf"nicht\b(?!\s+(?:nur|allein|bloß|bloss|ausschließlich|ausschliesslich)\b)\s+"
        rf"(?P<right>{ANTITHESIS_OPERAND_PATTERN})",
        re.IGNORECASE,
    ),
    # Nachgestellter Kontrast-Schwanz als Satzschluss: "X, nicht Y." Left deckt nur den
    # Operanden direkt vor dem Komma, damit der Fakten-Carve-out beidseitige
    # Wert-Korrekturen ("am Dienstag, nicht am Mittwoch.") weiter ausschließen kann.
    # Das Schlusszeichen braucht folgenden Leerraum oder Textende (schließt Dezimal-,
    # Tausender- und Domain-Punkte aus) und darf nicht auf ein Einzelzeichen-Token
    # folgen (schließt Abkürzungen wie "z. B." und Ordinalpunkte wie "am 3. Mai" aus).
    re.compile(
        rf"\b(?P<left>{ANTITHESIS_OPERAND_PATTERN})\s*,\s*"
        r"nicht\b(?!\s+(?:nur|allein|bloß|bloss|ausschließlich|ausschliesslich)\b)\s+"
        r"(?P<right>[^,.;:!?\r\n]{1,80}?)(?<!\s[0-9A-Za-zÄÖÜäöüß])[.!?](?=\s|$)",
        re.IGNORECASE,
    ),
)
FACTUAL_CONTRAST_VALUE_RE = re.compile(
    rf"\s*{FACTUAL_CONTRAST_VALUE_PATTERN}\s*",
    re.IGNORECASE,
)
ANTITHESIS_CLUSTER_MIN_COUNT = 4
ANTITHESIS_CLUSTER_MIN_PER_1000_WORDS = 3.0
WORD_RE = re.compile(r"[^\W_]+(?:[-'][^\W_]+)?")
DASH_PUNCTUATION_RE = re.compile(r"[–—]|(?<=[^\S\r\n])--?(?=[^\S\r\n])")
DASH_NUMBER_RANGE_RE = re.compile(r"\d[^\S\r\n]*(?:[–—]|--?)[^\S\r\n]*\d")
DASH_PARAGRAPH_RE = re.compile(r"(?m)(?:^[^\r\n]*\S[^\r\n]*(?:\r?\n|$))+")
DASH_CLUSTER_MIN_COUNT = 5
DASH_CLUSTER_MIN_PER_1000_WORDS = 15.0
DASH_DISTRIBUTED_MIN_COUNT = 3
DASH_DISTRIBUTED_MIN_PARAGRAPHS = 4
BOLD_SPAN_RE = re.compile(r"\*\*[^*\r\n]+?\*\*")
BOLD_OVERDOSE_THRESHOLD = 5
STELLT_DAR_RE = re.compile(
    r"\bstell(?:t|te|ten|en)\b(?:\s+\S+){0,6}?\s+dar\b"
    r"|\bdarstell(?:t|te|ten|en)\b"
    r"|\bdargestellt\b"
    r"|\bdarzustellen\b",
    re.IGNORECASE,
)
ADDRESS_VALIDATION_RE = re.compile(
    r"\b(?:du\s+bist\s+nicht\s+(?:zu\s+|einfach\s+nur\s+)?"
    r"(?:sensibel|empfindlich|emotional|bedürftig|anspruchsvoll|schwierig|schwach|faul|anstrengend)"
    r"|du\s+(?:überreagierst\s+nicht|reagierst\s+nicht\s+über|fühlst\s+nicht\s+falsch)"
    r"|deine\s+gefühle\s+sind\s+(?:völlig\s+)?(?:berechtigt|valide|verständlich)"
    r"|deine\s+reaktion(?:en)?\s+(?:ist|sind)\s+(?:völlig\s+)?(?:berechtigt|valide|verständlich)"
    r"|du\s+wurdest\s+(?:nur\s+)?(?:zu\s+lange\s+)?"
    r"(?:nicht\s+ernst\s+genommen|kleingehalten|emotional\s+vernachlässigt))\b",
    re.IGNORECASE,
)
ADDRESS_VALIDATION_MESSAGE = (
    "Kandidat für unbelegte Adressaten-Validierung: Kontext prüfen "
    "(Beratungsauftrag? Zitat? Sachklärung?)"
)


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


def marker_stem(marker: str) -> str:
    if marker.endswith("en") and len(marker) > 5:
        return marker[:-2]
    return marker


@functools.lru_cache(maxsize=8)
def mention_ranges(text: str) -> tuple[tuple[int, int], ...]:
    ranges = [
        match.span()
        for pattern in evidence_lint.VALID_QUOTE_PATTERNS
        for match in pattern.finditer(text)
    ]
    patterns = [
        r"```.*?```",
        r"`[^`\r\n]+`",
        # Nachbar-Schutz: Sternchen in **Fettdruck** dürfen keine Spans
        # öffnen oder schließen.
        r"(?<!\*)\*(?!\*)[^*\r\n]+(?<!\*)\*(?!\*)",
        # Wortgrenzen-Schutz: Unterstriche in snake_case dürfen keine Spans
        # öffnen oder schließen.
        r"(?<!\w)_[^_\r\n]+_(?!\w)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.DOTALL):
            ranges.append(match.span())
    return tuple(text_scope.merge_ranges(ranges))


def in_mention(index: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    position = bisect.bisect_left(ranges, (index + 1,)) - 1
    return position >= 0 and index < ranges[position][1]


def overlaps_mention(start: int, end: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    position = bisect.bisect_left(ranges, (end,)) - 1
    return position >= 0 and ranges[position][1] > start


@functools.lru_cache(maxsize=8)
def foreign_voice_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Erwähnungen plus Blockquotes: alles, was nicht der Autorenstimme zählt.

    Wie in `excluded_spans` gelten Blockquotes als Fremdrede, damit ein Zitat
    keinen Marker-Cluster der Autorenstimme erzeugt.
    """
    return tuple(
        text_scope.merge_ranges([*mention_ranges(text), *text_scope.blockquote_ranges(text)])
    )


def marker_spans(text: str, marker: str) -> list[tuple[int, int]]:
    ranges = foreign_voice_ranges(text)
    override = MARKER_PATTERNS.get(marker)
    if override is not None:
        matches = override.finditer(text)
    elif " " in marker:
        matches = re.finditer(r"\b" + re.escape(marker).replace(r"\ ", r"\s+") + r"\w*\b", text, re.IGNORECASE)
    else:
        stem = marker_stem(marker)
        matches = re.finditer(rf"\b{re.escape(stem)}\w*\b", text, re.IGNORECASE)
    return [match.span() for match in matches if not in_mention(match.start(), ranges)]


def count_marker(text: str, marker: str) -> int:
    return len(marker_spans(text, marker))


def evidence_text(match: re.Match) -> str:
    return match.group().replace("\r\n", "\n").replace("\r", "\n").strip()


def collect_marker_hits(text: str, markers: tuple[str, ...]) -> tuple[dict[str, int], list[tuple[int, int]]]:
    hits: dict[str, int] = {}
    spans: list[tuple[int, int]] = []
    for marker in markers:
        matched = marker_spans(text, marker)
        if matched:
            hits[marker] = len(matched)
            spans.extend(matched)
    return hits, spans


def authored_pattern_spans(
    text: str,
    patterns: tuple[re.Pattern, ...],
    excluded_spans: tuple[tuple[int, int], ...],
) -> list[tuple[int, int]]:
    return text_scope.merge_ranges(
        [
            match.span()
            for pattern in patterns
            for match in pattern.finditer(text)
            if not overlaps_mention(match.start(), match.end(), excluded_spans)
        ]
    )


def ad_section_spans(
    text: str,
    excluded_spans: tuple[tuple[int, int], ...],
) -> list[tuple[int, int]]:
    lines: list[tuple[int, str]] = []
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        lines.append((offset, raw_line.rstrip("\r\n")))
        offset += len(raw_line)

    spans: list[tuple[int, int]] = []
    for index, (start, line) in enumerate(lines):
        stripped = line.strip()
        heading = MARKDOWN_HEADING_RE.fullmatch(line)
        if heading:
            title = heading.group("title").strip()
        elif (
            len(stripped) <= 120
            and (index == 0 or not lines[index - 1][1].strip())
            and (index == len(lines) - 1 or not lines[index + 1][1].strip())
        ):
            title = stripped
        else:
            continue
        if not AD_SECTION_RE.fullmatch(title):
            continue
        span = (start + len(line) - len(line.lstrip()), start + len(line.rstrip()))
        if not overlaps_mention(*span, excluded_spans):
            spans.append(span)
    return spans


def stellt_dar_dependency_spans(text: str, nlp: object) -> list[tuple[int, int]]:
    doc = nlp(text)
    spans: list[tuple[int, int]] = []
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma == "darstellen":
            spans.append((token.idx, token.idx + len(token.text)))
            continue
        if lemma != "stellen" or "Fin" not in token.morph.get("VerbForm"):
            continue
        particle = next(
            (child for child in token.children if child.dep_ == "svp" and child.text.lower() == "dar"),
            None,
        )
        if particle is not None:
            spans.append(
                (
                    min(token.idx, particle.idx),
                    max(token.idx + len(token.text), particle.idx + len(particle.text)),
                )
            )
    return spans


def lint(text: str, mode: str = "sachlich", precise: bool = False) -> dict:
    status, nlp = precise_context(precise)
    clean_text = register_lint.strip_protected(text)
    findings: list[dict] = []

    ai_hits, ai_spans = collect_marker_hits(clean_text, AI_MARKERS)
    if sum(ai_hits.values()) >= 3:
        findings.append(
            {
                "pattern": 64,
                "kind": "ai_marker_cluster",
                "severity": "warning",
                "evidence": ai_hits,
                "spans": text_scope.serialize_spans(ai_spans),
            }
        )

    foreign_spans = foreign_voice_ranges(clean_text)
    ad_spans = {
        "social_proof": authored_pattern_spans(clean_text, AD_SOCIAL_PROOF_RES, foreign_spans),
        "ad_section": ad_section_spans(clean_text, foreign_spans),
        "cta_stack": authored_pattern_spans(clean_text, AD_CTA_RES, foreign_spans),
    }
    ad_spans = {name: spans for name, spans in ad_spans.items() if spans}
    anchor_classes = ad_spans.keys() & {"social_proof", "ad_section"}
    if anchor_classes and (
        len(ad_spans) >= 2 or any(len(ad_spans[name]) >= 2 for name in anchor_classes)
    ):
        findings.append(
            {
                "pattern": 2,
                "kind": "ad_boilerplate_cluster",
                "severity": "warning",
                "evidence": {
                    name: [text[start:end].strip() for start, end in spans]
                    for name, spans in ad_spans.items()
                },
                "spans": text_scope.serialize_spans(
                    [span for spans in ad_spans.values() for span in spans]
                ),
            }
        )

    copula_hits, copula_spans = collect_marker_hits(clean_text, COPULA_AVOIDANCE)
    separable_spans = [match.span() for match in STELLT_DAR_RE.finditer(clean_text)]
    if nlp is not None:
        separable_spans = stellt_dar_dependency_spans(clean_text, nlp)
    if separable_spans:
        copula_hits["stellt ... dar"] = len(separable_spans)
        copula_spans.extend(separable_spans)
    if sum(copula_hits.values()) >= 2:
        findings.append(
            {
                "pattern": 65,
                "kind": "copula_avoidance_cluster",
                "severity": "warning",
                "evidence": copula_hits,
                "spans": text_scope.serialize_spans(copula_spans),
            }
        )

    abstract_hits, abstract_spans = collect_marker_hits(clean_text, ABSTRACTA)
    if sum(abstract_hits.values()) >= 3:
        findings.append(
            {
                "pattern": 58,
                "kind": "abstraction_cluster",
                "severity": "warning",
                "evidence": abstract_hits,
                "spans": text_scope.serialize_spans(abstract_spans),
            }
        )

    colon_headings: list[str] = []
    colon_heading_spans: list[tuple[int, int]] = []
    markdown_heading_spans: list[tuple[int, int]] = []
    offset = 0
    for raw_line in clean_text.splitlines(keepends=True):
        line = raw_line.splitlines()[0]
        start = offset + len(line) - len(line.lstrip())
        end = offset + len(line.rstrip())
        if MARKDOWN_HEADING_RE.fullmatch(line):
            markdown_heading_spans.append((start, end))
        if re.match(r"^\s{0,3}#{1,3}\s+.+:.+", line):
            colon_headings.append(line.strip())
            colon_heading_spans.append((start, end))
        offset += len(raw_line)
    if len(colon_headings) >= 2:
        findings.append(
            {
                "pattern": 54,
                "kind": "colon_heading_cluster",
                "severity": "warning",
                "evidence": colon_headings,
                "spans": text_scope.serialize_spans(colon_heading_spans),
            }
        )

    excluded_spans = tuple(
        text_scope.merge_ranges(
            [
                *text_scope.protected_ranges(text),
                *mention_ranges(text),
                *text_scope.blockquote_ranges(text),
            ]
        )
    )
    negation_matches = sorted(
        (
            match.start(),
            match.end(),
            evidence_text(match),
        )
        for pattern in NEGATION_PARALLELISM_RES
        for match in pattern.finditer(clean_text)
        # Start-only protection keeps an incidental inline quotation from blinding
        # an authored whole-sentence figure.
        if not in_mention(match.start(), excluded_spans)
    )
    evidence = [matched_text for _, _, matched_text in negation_matches]
    if evidence:
        findings.append(
            {
                "pattern": 8,
                "kind": "negation_parallelism",
                "severity": "warning",
                "evidence": evidence,
                "spans": text_scope.serialize_spans([(start, end) for start, end, _ in negation_matches]),
            }
        )

    antithesis_candidates = sorted(
        (
            match.start(),
            match.end(),
            evidence_text(match),
        )
        for pattern in ANTITHESIS_RES
        for match in pattern.finditer(clean_text)
        # Operand-level protection needs overlap because a protected arm can sit
        # inside an otherwise unprotected match.
        if not overlaps_mention(match.start(), match.end(), excluded_spans)
        and not (
            {"left", "right"} <= match.groupdict().keys()
            and FACTUAL_CONTRAST_VALUE_RE.fullmatch(match.group("left"))
            and FACTUAL_CONTRAST_VALUE_RE.fullmatch(match.group("right"))
        )
    )
    antithesis_matches = []
    covered_until = -1
    for candidate in antithesis_candidates:
        start, end, _ = candidate
        if start >= covered_until:
            antithesis_matches.append(candidate)
            covered_until = max(covered_until, end)
    word_count = sum(
        1
        for match in WORD_RE.finditer(clean_text)
        if not overlaps_mention(match.start(), match.end(), foreign_spans)
    )
    antithesis_density = len(antithesis_matches) * 1000 / word_count if word_count else 0.0
    if (
        len(antithesis_matches) >= ANTITHESIS_CLUSTER_MIN_COUNT
        and antithesis_density >= ANTITHESIS_CLUSTER_MIN_PER_1000_WORDS
    ):
        findings.append(
            {
                "pattern": 8,
                "kind": "negation_antithesis_cluster",
                "severity": "warning",
                "evidence": {
                    "count": len(antithesis_matches),
                    "per_1000_words": round(antithesis_density, 2),
                    "matches": [matched_text for _, _, matched_text in antithesis_matches],
                },
                "spans": text_scope.serialize_spans(
                    [(start, end) for start, end, _ in antithesis_matches]
                ),
            }
        )

    numeric_range_spans = tuple(match.span() for match in DASH_NUMBER_RANGE_RE.finditer(clean_text))
    contrast_spans = tuple(
        text_scope.merge_ranges(
            [(start, end) for start, end, _ in (*negation_matches, *antithesis_candidates)]
        )
    )
    dash_spans = [
        match.span()
        for match in DASH_PUNCTUATION_RE.finditer(clean_text)
        if not any(
            overlaps_mention(match.start(), match.end(), ranges)
            for ranges in (
                foreign_spans,
                tuple(markdown_heading_spans),
                numeric_range_spans,
                contrast_spans,
            )
        )
    ]
    dash_clusters: list[tuple[list[tuple[int, int]], float]] = []
    distributed_dash_paragraphs: list[tuple[list[tuple[int, int]], float]] = []
    for paragraph in DASH_PARAGRAPH_RE.finditer(clean_text):
        spans = [span for span in dash_spans if paragraph.start() <= span[0] < paragraph.end()]
        if len(spans) < DASH_DISTRIBUTED_MIN_COUNT:
            continue
        paragraph_word_count = len(WORD_RE.findall(paragraph.group()))
        density = len(spans) * 1000 / paragraph_word_count if paragraph_word_count else 0.0
        distributed_dash_paragraphs.append((spans, density))
        if len(spans) >= DASH_CLUSTER_MIN_COUNT and density >= DASH_CLUSTER_MIN_PER_1000_WORDS:
            dash_clusters.append((spans, density))
    triggered_dash_paragraphs = (
        distributed_dash_paragraphs
        if len(distributed_dash_paragraphs) >= DASH_DISTRIBUTED_MIN_PARAGRAPHS
        else dash_clusters
    )
    if triggered_dash_paragraphs:
        clustered_spans = [span for spans, _ in triggered_dash_paragraphs for span in spans]
        findings.append(
            {
                "pattern": 16,
                "kind": "dash_cluster",
                "severity": "warning",
                "evidence": {
                    "count": len(clustered_spans),
                    "max_per_1000_words": round(
                        max(density for _, density in triggered_dash_paragraphs), 2
                    ),
                    "matches": [text[start:end] for start, end in clustered_spans],
                },
                "spans": text_scope.serialize_spans(clustered_spans),
            }
        )

    bold_matches = [
        match
        for match in BOLD_SPAN_RE.finditer(clean_text)
        if (match.start() == 0 or clean_text[match.start() - 1] != "*")
        and (match.end() == len(clean_text) or clean_text[match.end()] != "*")
        and not overlaps_mention(match.start(), match.end(), foreign_spans)
    ]
    bold_span_count = len(bold_matches)
    if bold_span_count >= BOLD_OVERDOSE_THRESHOLD:
        findings.append(
            {
                "pattern": 13,
                "kind": "bold_overdose",
                "severity": "warning",
                "evidence": {"count": bold_span_count},
                "spans": text_scope.serialize_spans([match.span() for match in bold_matches]),
            }
        )

    address_validation_matches = [
        match
        for match in ADDRESS_VALIDATION_RE.finditer(clean_text)
        # Start-only protection keeps an incidental inline quotation from blinding
        # the whole authored statement.
        if not in_mention(match.start(), excluded_spans)
    ]
    if address_validation_matches:
        findings.append(
            {
                "pattern": 72,
                "kind": "address_validation_candidate",
                "severity": "info",
                "advisory": True,
                "message": ADDRESS_VALIDATION_MESSAGE,
                "evidence": [evidence_text(match) for match in address_validation_matches],
                "spans": text_scope.serialize_spans([match.span() for match in address_validation_matches]),
            }
        )

    # mode is report metadata only and does not control detection.
    report = {"ok": not findings, "mode": mode, "findings": findings}
    if status is not None:
        report["precise"] = status
    return report


def check_fixture(path: Path, precise: bool = False) -> dict:
    data = read_json_object(path, label="fixture", required=("text",))
    report = lint(data["text"], mode=data.get("mode", "sachlich"), precise=precise)
    expected = set(data.get("expect_kinds", []))
    actual = {item["kind"] for item in report["findings"]}
    return {"fixture": str(path), "ok": actual == expected, "report": report}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report German naturalness pattern clusters.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    source.add_argument("--fixture", type=Path)
    parser.add_argument("--mode", choices=["locker", "sachlich", "formal"], default="sachlich")
    parser.add_argument("--precise", action="store_true", help="spaCy-gestützte Verfeinerung, wenn installiert; sonst wirkungslos")
    parser.add_argument("--fail-on", choices=["never", "any"], default="never")
    args = parser.parse_args(argv)
    require_file(parser, args.file, "--file")
    if args.fixture:
        if not args.fixture.exists():
            parser.error(f"fixture path does not exist: {args.fixture}")
        if args.fixture.is_dir() and not any(args.fixture.glob("*.json")):
            parser.error(f"fixture directory contains no JSON files: {args.fixture}")
    return args


@handle_cli_input_errors
def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.fixture:
        files = sorted(args.fixture.glob("*.json")) if args.fixture.is_dir() else [args.fixture]
        results = [check_fixture(file_path, precise=args.precise) for file_path in files]
        print_json({"ok": all(item["ok"] for item in results), "results": results})
        return 0 if all(item["ok"] for item in results) else 1

    text = read_user_text(args.file) if args.file else args.text or ""
    report = lint(text, mode=args.mode, precise=args.precise)
    print_json(report)
    return resolve_exit_code(args.fail_on, report["findings"])


if __name__ == "__main__":
    raise SystemExit(main())
