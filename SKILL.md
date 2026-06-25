---
name: Humanizer (Deutsch)
description: >-
  Fokus: deutschen Text humanisieren, KI-Schreibmuster entfernen und deutsche KI-Tells auditieren.
version: 4.1.0
author: Martin Moeller
maintainer_website: 'https://www.martin-moeller.biz'
based_on: 'Deutsche Wikipedia: Anzeichen für KI-generierte Inhalte, Erkennung KI-Einsatz, Schnelltest KI'
original_skill: 'https://github.com/blader/humanizer'
tags: [writing, ai-detection, german, wikipedia, text-improvement]
allowed_tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Humanizer (Deutsch)

<!-- SLOW_UPDATE_START -->

## Auftrag

Wenn der Nutzer deutschen Text humanisieren, KI-Schreibmuster entfernen oder deutsche KI-Tells prüfen will, überarbeite die betroffenen Stellen. Bewahre Substanz, Register und belegbare Aussagen. Ziel ist ein guter, natürlicher Text mit proportionalen Eingriffen.

Fokus des Skills ist KI-Muster-Audit mit gezielter Textverbesserung. Reines Korrektorat, Grammatikprüfung, Übersetzung und allgemeine Stilpolitur gehören nur dazu, wenn sie diesem Ziel dienen.

QGIR (Quality-Guided Iterative Revision) nur nutzen, wenn nach einem lokalen Minimal-Revision-Pass noch echte HIGH/MEDIUM-Cluster bleiben. QGIR arbeitet als Quality-Gate fuer proportionale Revision, nicht als Standard-Vollrewrite.

## Modus

Bestimme zuerst den Modus. Wenn unklar, nimm **Sachlich** an und sage das.

| Modus | Einsatz | Stimme |
|---|---|---|
| Locker | Blog, Social, Newsletter | voll, aber nicht künstlich |
| Sachlich | Website, Doku, E-Mail, B2B | dezent, neutral |
| Formal | Wissenschaft, Recht, Fachtext | keine Stimme einbringen |

## Leitplanken

- Zähle Cluster, nicht Einzelsignale. Ein einzelnes Übergangswort, ein einzelner Gedankenstrich, saubere Grammatik oder typografische Anführungszeichen allein sind kein KI-Tell.
- HIGH-Muster, technische Artefakte und Belegprobleme dürfen als Einzelbefund korrigiert oder markiert werden.
- MEDIUM/LOW-Stilmuster nur bei Häufung, klarer Mechanik oder mehreren unabhängigen Mustern überarbeiten.
- Direkte Zitate, Code, technische Spezifikationen und juristische/regulatorische Formulierungen nicht stilistisch umschreiben.
- Quellen nur aus Input oder Kontext übernehmen. Wenn eine Quelle nicht prüfbar ist, den Prüfstatus markieren.
- Ich-Erfahrung, Anekdoten und Meinungen nur übernehmen, wenn sie im Input oder Kontext stehen. Erfundene Erfahrung ist Fabrikation (Muster 59).
- Zahlen, Namen, Daten, Quellenanker, Zitate, Code und Normverweise vor/nach jeder Änderung abgleichen. Neue konkrete Anker nur übernehmen, wenn sie im Input oder Kontext stehen.
- Substanz erhalten. Entferne nur Artefakte ohne Informationsgehalt oder markiere echte Lücken.
- Statistische Detektoren (GPTZero u. a.) messen Perplexity und Satzrhythmus, nicht diese Muster. Befunde wie „Mechanical Precision“ oder „Impersonal Tone“ treffen meist legitime Fachsprache, korrekte Quellen und sachliche Klarheit – nicht als KI-Tell behandeln und keinen Text verschlechtern, um einen Score zu senken. Behandelbar sind nur gehäufte Doppelpunkt-Titel (Muster 54) und monotoner Satzrhythmus (Muster 55).
- Detector-Bezug ist Kontext. Bewertet wird, ob eine Änderung Qualität, Lesbarkeit oder echte KI-Muster verbessert; Substanz bleibt wichtiger als Scorewirkung.
- Wenn der Text sauber ist, sage das und höre auf.

## Modusmatrix

| Klasse | Locker | Sachlich | Formal |
|---|---|---|---|
| HIGH Artefakt/Chatbot/Technik | ändern/entfernen | ändern/entfernen | ändern/entfernen |
| HIGH Evidenz/Quelle | markieren/korrigieren | markieren/korrigieren | markieren/korrigieren |
| HIGH Stil | ändern | ändern | nur wenn nicht fachkonventionell; Muster 10 überspringen |
| MEDIUM Technik/Struktur | ändern | ändern | markieren oder vorsichtig ändern |
| MEDIUM weicher Stil | bei Häufung ändern | bei Häufung/klarer Mechanik ändern | meist nur markieren |
| LOW Format | ändern, wenn störend | ändern bei Regelverstoß | meist überspringen |

False Friends aus Muster 45 immer korrigieren. Calques und syntaktische Transfers im Formal-Modus korrigieren; sonst nur bei Häufung oder auffälliger Wörtlichkeit.

<!-- SLOW_UPDATE_END -->

<!-- FAST_UPDATE_START -->

## Ablauf: Fünf Pässe in fester Reihenfolge

Spätere Pässe dürfen frühere nicht invalidieren. Rhythmus immer zuletzt.

**Pass 0 – Triage.** Modus, Texttyp, Scope und Ziel bestimmen. Schreibprobe vorhanden? Dann Satzrhythmus, Wortniveau, Absatzanfänge, Anrede, Distanz, Terminologie und Lieblingszeichen als Zielprofil festhalten (im Formal-Modus nur KI-Tells entfernen). Bei Datei-Input: `python3 scripts/unicode_lint.py --file <path>` und `python3 scripts/rhythm_lint.py --file <path> --scope user_text --mode <modus>` ausführen, Kennzahlen notieren. Bei Inline-Text: Rohtext zuerst in eine temporäre UTF-8-Datei schreiben, dann `--file <tempfile>`; Shell-Befehle bleiben statisch, Nutzereingaben laufen über Dateien. Läuft ein Script nicht, das melden und nicht blind per Hand korrigieren.

**Pass 1 – Artefakte und Evidenz (immer, Einzelbefund genügt).** Chatbot-Floskeln, Platzhalter, Quellenprobleme (Decision Table Evidenz), Unicode, falsche Typografie und Claim-Delta prüfen. Bei Overlaps zuerst [references/decision-tables.md](references/decision-tables.md); [references/evidence-ledger.md](references/evidence-ledger.md) bei Faktenankern; [references/patterns.md](references/patterns.md) nur für konkrete Musterdiagnose, Audit oder Grenzfälle laden. Dieser Pass bleibt bei Evidenz, Technik und Artefakten; Stilarbeit folgt später. Für sichere Datei-Korrekturen: `unicode_lint.py --fix --write`.

**Pass 2 – Lexik (Cluster-Regel).** Floskel-Muster, KI-Marker-Vokabular (Muster 64), Kopula-Vermeidung (Muster 65), Abstrakta-Stapel (Muster 58): Hypernyme und Nominalstil dort auflösen, wo der konkrete Sachverhalt im Text oder Kontext steht. Konkretion kommt aus belegtem Material; unbelegte Lücken sichtbar markieren.

**Pass 3 – Struktur (Cluster-Regel).** Überschriften-Schemata, isometrische Absätze (Muster 61), substanzlose Sektionen, Listen-Parallelismus, Schließzwang (Muster 62). Erst nach diesem Pass steht die endgültige Absatzstruktur.

**Pass 4 – Rhythmus (Locker/Sachlich: standardmäßig an; Formal: nur auf Wunsch).** Konkrete Stellschrauben:
- Vorfeld rotieren: höchstens ~2 von 3 Sätzen subjektinitial. Varianten: Adverbial, vorangestellter Nebensatz, Objekt, Präpositionalphrase.
- Satzlänge spreizen: pro längerem Absatz mindestens ein Satz unter 6 Wörtern oder über 25 – nur wo die Aussage es trägt.
- Absatzlängen entzerren: nicht jeder Absatz 3–5 Sätze.
- Konnektor-Budget: höchstens ein mechanischer Konnektor pro Absatz; Übergänge bevorzugt über inhaltliche Anknüpfung (Thema-Rhema).
- Nur Modus Locker: sparsame Modalpartikeln (Muster 63), maximal eine pro Absatz. Sachlich/Formal bleiben ohne künstlich nachgerüstete Partikeln.

**Pass 5 – Selbst-Audit (immer).** Eigene Änderungen gegen Katalog, Zielprofil und Claim-Lock prüfen: Hat eine Ersetzungsregel neue Monotonie erzeugt (gleiche Ersatzkonstruktion 3+ Mal → Strategie rotieren, vgl. Muster 16 vs. 51)? Quellen, Erfahrung (Muster 59), Faktenanker, Substanz und Output-Länge bleiben durch Input oder Kontext gedeckt. Danach Kurzaudit ausgeben.

**QGIR – begrenzte zweite Runde (optional).** Nur wenn nach Pass 5 echte HIGH/MEDIUM-Cluster bleiben und Claim/Register/Naturalness-Gates grün sind. Maximal 2 normale Pässe, dritter nur bei dokumentiertem schweren Restcluster. Stoppen, sobald weitere Änderungen nur Glattheit, Stimme oder Detektorwirkung verbessern würden. Details: [references/qgir.md](references/qgir.md).

## Entscheidungstabellen

Evidenz:
- Muster 11: vage Autorität ohne konkrete Quelle.
- Muster 26: konkrete Quelle wirkt formal ungültig, erfunden oder KI-artefaktisch.
- Muster 42: Quelle existiert und wurde geprüft, belegt die Aussage aber nicht.
- Muster 53: Quelle fehlt oder schweigt, Text füllt die Lücke spekulativ.

Struktur:
- Muster 5: Zusammenfassungsmarker im Absatz.
- Muster 6: unpassende Fazit-/Zusammenfassungssektion.
- Muster 34: generischer Einzeiler direkt nach Überschrift.
- Muster 44: ganzer Standardabschnitt ohne konkrete Substanz.

## Output

Der Output konzentriert sich auf die geänderten Stellen statt auf einen vollständigen Neuabdruck.

Format:

1. **Modus:** eine Zeile.
2. **Gefundene Muster:** maximal 6 konkrete Bullet Points mit kurzem Zitat.
3. **Geänderte Stellen:** Vorher/Nachher-Paare nur für bearbeitete Passagen.
4. **Kurzaudit:** maximal 3 verbleibende Tells oder „Keine gefunden.“

Wenn der Nutzer eine Datei übergibt und Änderungen verlangt, editiere die Datei direkt und fasse die Änderungen kurz zusammen.

## Referenzen

- Vollständiger Musterkatalog: [references/patterns.md](references/patterns.md)
- Overlap- und Moduslogik: [references/decision-tables.md](references/decision-tables.md)
- QGIR-Loop und Stop-Regeln: [references/qgir.md](references/qgir.md)
- Faktenanker/Claim-Delta: [references/evidence-ledger.md](references/evidence-ledger.md)
- Registerprofile: [references/register-profiles.md](references/register-profiles.md)
- Deutsche Naturalness-Karten: [references/de-naturalness.md](references/de-naturalness.md)
- Unicode-/Quote-Linter: `scripts/unicode_lint.py`
- Rhythmus-/Burstiness-Messung: `scripts/rhythm_lint.py`
- Evidence-/Register-/Naturalness-Checks: `scripts/evidence_lint.py`, `scripts/register_lint.py`, `scripts/german_pattern_lint.py`

<!-- FAST_UPDATE_END -->
