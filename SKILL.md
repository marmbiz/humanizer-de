---
name: humanizer-de
description: deutschen Text humanisieren, KI-Schreibmuster/KI-Tells auditieren; German AI Text Humanizer für Claude Code/Codex, evidence-safe rewrites, Register- und Naturalness-Checks.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
metadata:
  display_name: Humanizer (Deutsch)
  version: 5.1.0
  author: Martin Moeller
  maintainer_website: https://www.martin-moeller.biz
  based_on: 'Deutsche Wikipedia: Anzeichen für KI-generierte Inhalte, Erkennung KI-Einsatz, Schnelltest KI'
  original_skill: https://github.com/blader/humanizer
  tags: [writing, ai-detection, humanizer, ai-humanizer, claude-skill, codex-skill, german, deutsch, ki-text, germanizer, prompt-engineering, wikipedia, text-improvement]
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
- Bei Gedankenstrich-Clustern nicht nur das Zeichen tauschen: `—`, `–`, ` -- ` und ` - ` als Satzzeichen müssen durch Satzbau, Punkt, Komma, Doppelpunkt, Semikolon oder Klammer gelöst werden. Wort-Bindestriche bleiben geschützt.
- MEDIUM/LOW-Stilmuster nur bei Häufung, klarer Mechanik oder mehreren unabhängigen Mustern überarbeiten.
- Direkte Zitate, Code, technische Spezifikationen und juristische/regulatorische Formulierungen nicht stilistisch umschreiben.
- Quellen nur aus Input oder Kontext übernehmen. Wenn eine Quelle nicht prüfbar ist, den Prüfstatus markieren.
- Ich-Erfahrung, Anekdoten und Meinungen nur übernehmen, wenn sie im Input oder Kontext stehen. Erfundene Erfahrung ist Fabrikation (Muster 59).
- Deixis nur stabilisieren, nicht erfinden: `ich`, `wir`, `du`, `Sie`, `man` und neutrale Sprecherposition bleiben am Texttyp, Input und Zielprofil ausgerichtet.
- Zahlen, Namen, Daten, Quellenanker, Zitate, Code und Normverweise vor/nach jeder Änderung abgleichen. Neue konkrete Anker nur übernehmen, wenn sie im Input oder Kontext stehen.
- Substanz erhalten. Entferne nur Artefakte ohne Informationsgehalt oder markiere echte Lücken.
- Statistische Detektoren (GPTZero u. a.) messen Perplexity und Satzrhythmus, nicht diese Muster. Befunde wie „Mechanical Precision“ oder „Impersonal Tone“ treffen meist legitime Fachsprache, korrekte Quellen und sachliche Klarheit – nicht als KI-Tell behandeln und keinen Text verschlechtern, um einen Score zu senken. Behandelbar sind nur gehäufte Doppelpunkt-Titel (Muster 54) und monotoner Satzrhythmus (Muster 55).
- Detector-Bezug ist Kontext. Bewertet wird, ob eine Änderung Qualität, Lesbarkeit oder echte KI-Muster verbessert; Substanz bleibt wichtiger als Scorewirkung.
- Wenn der Text sauber ist, sage das und höre auf.

## Carve-outs: bekannte False Positives

Lint-Befunde sind Verdacht, kein Verdikt – jeden vor einer Änderung gegen den Kontext prüfen. Folgende Fälle sind regelmäßig Fehlalarm und werden nicht behandelt, solange kein zusätzlicher Cluster vorliegt:

- Quotes in Codeblöcken und Inline-Code blendet `unicode_lint.py` bereits aus (`straight_quote`, `mixed_quote_styles`); YAML-Frontmatter und Markdown-Bildtitel (`![Alt](url "Titel")`) dagegen nicht – dort ist das Geradzeichen technische Syntax, kein Tell. `--fix --write` nie blind auf Frontmatter oder Bildtitel anwenden.
- Quotes in rohem HTML innerhalb von Markdown blendet `unicode_lint.py` ebenfalls nicht aus (`straight_quote`, `mixed_quote_styles`): Attribute wie `<iframe title="Eingebetteter Beitrag">` brauchen gerade Anführungszeichen. Kein Befund, solange die Quotes Teil eines HTML-Tags sind; echter Befund bleibt gerades Anführungszeichen in laufender deutscher Prosa außerhalb technischer Syntax.
- `mixed_address`, wenn `Sie`/`Ihr` nur satzinitial großgeschrieben ist: `register_lint.py` zählt jedes großgeschriebene `Sie`/`Ihr` als formelle Anrede. Ist das Wort grammatisch 3. Person und nur durch Satzanfang großgeschrieben (Anapher auf ein vorheriges Nomen, etwa `Die Idee war neu. Sie überzeugte sofort.`), ist das keine Anredemischung, auch wenn im selben Absatz `du` steht.
- `mixed_address`, wenn formelles `Sie`/`Ihnen` nur in zitierter oder referierter Fremdstimme steht, etwa Bot- oder UI-Kopie im Blockquote, während die Autorenstimme `du` nutzt: `register_lint.py` trennt Zitatregister nicht vom Fließtext. Kein Befund, solange die formelle Anrede zur zitierten Quelle gehört; echter Registerbruch bleibt, wenn die Autorenstimme außerhalb von Zitaten selbst zwischen `du` und `Sie` driftet.
- Muster 64 (KI-Marker-Vokabular) bei Use-Mention: `german_pattern_lint.py` zählt Wortstämme roh, auch in Zitaten oder Kursivsetzung. Wer über das Füllwort `nahtlos` als angeführtes Beispiel schreibt, verwendet es nicht; kein Beitrag zum Cluster.
- `particles_outside_locker`/`particle_overdose` und `copula_avoidance_cluster` bei lexikalischer Mehrdeutigkeit: `register_lint.py` und `german_pattern_lint.py` sehen nur Wortformen, keine Wortart oder Lesart. `schon` im Sinn von `bereits`, `mal` als `einmal` oder `5-mal`, `ja` als Antwort und `stellt` als Vollverb (`stellt eine Frage`, `stellt sich die Frage`, `stellt die KI vor ein Problem`) sind allein kein Befund; real bleibt der Fund, wenn die Wörter tatsächlich als Modalpartikeln/Nähemarker gehäuft sind oder `stellt` eine Kopula-Vermeidung wie `stellt dar` statt `ist`/`hat` bildet.
- Hoher `subject_initial_ratio` ohne Cluster: Werte über 0,85 sind allein unauffällig (Kalibrierungs-Median menschlicher Blogtexte: 0,887). `rhythm_lint.py` meldet dies nur als Fund bei zusätzlich niedriger Satzlängenvarianz oder wiederholten Satzanfängen – die reine Zahl in einer Audit-Zusammenfassung ist für sich kein Fund.
- Doppelpunkt im Einzeltitel (Muster 54): erst ab 2+ gleich gebauten Doppelpunkt-Titeln im selben Dokument behandeln, nie einen einzelnen Haupttitel oder ein Label (UI, Quellenangabe, Zeit-/Ortsangabe).

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

**Pass 0 – Triage.** Modus, Texttyp, Scope und Ziel bestimmen. Schreibprobe vorhanden? Dann Satzrhythmus, Wortniveau, Absatzanfänge, Sprecherposition (`ich`/`wir`/`man`/neutral), Anrede, Distanz, Terminologie und Lieblingszeichen als Zielprofil festhalten (im Formal-Modus nur KI-Tells entfernen). Bei Datei-Input zuerst den kompakten Sammelcheck ausführen: `python3 scripts/humanizer_audit.py --file <path> --mode <modus>`. Für den neuesten Markdown-Entwurf in einem Ordner: `python3 scripts/humanizer_audit.py --latest <dir> --mode <modus>`. Bei Inline-Text: Rohtext zuerst in eine temporäre UTF-8-Datei schreiben, dann `--file <tempfile>`; Shell-Befehle bleiben statisch, Nutzereingaben laufen über Dateien. Einzelchecks wie `unicode_lint.py`, `rhythm_lint.py`, `german_pattern_lint.py` und `register_lint.py` bleiben für gezielte Nachprüfung nutzbar; Rhythmusdetails mit Absatzdaten nur bei Bedarf über `python3 scripts/rhythm_lint.py --file <path> --scope user_text --mode <modus> --include-paragraphs` ausgeben. Läuft ein Script nicht, das melden und nicht blind per Hand korrigieren. Audit- und Lint-Ausgaben sind Verdacht, kein Verdikt – vor Eingriff gegen die Carve-outs und den Kontext prüfen.

**Pass 1 – Artefakte und Evidenz (immer, Einzelbefund genügt).** Chatbot-Floskeln, Platzhalter, Quellenprobleme (Decision Table Evidenz), Unicode, falsche Typografie und Claim-Delta prüfen. Bei Overlaps zuerst [references/decision-tables.md](references/decision-tables.md); [references/evidence-ledger.md](references/evidence-ledger.md) bei Faktenankern; [references/patterns.md](references/patterns.md) nur für konkrete Musterdiagnose, Audit oder Grenzfälle laden. Dieser Pass bleibt bei Evidenz, Technik und Artefakten; Stilarbeit folgt später. Für sichere Datei-Korrekturen: `unicode_lint.py --fix --write`; Ergebnis bei Frontmatter und Bildtiteln prüfen (siehe Carve-outs).

**Pass 2 – Lexik (Cluster-Regel).** Floskel-Muster, KI-Marker-Vokabular (Muster 64), Kopula-Vermeidung (Muster 65), Abstrakta-Stapel (Muster 58): Hypernyme und Nominalstil dort auflösen, wo der konkrete Sachverhalt im Text oder Kontext steht. Konkretion kommt aus belegtem Material; unbelegte Lücken sichtbar markieren.

**Pass 3 – Struktur (Cluster-Regel).** Überschriften-Schemata, isometrische Absätze (Muster 61), substanzlose Sektionen, Listen-Parallelismus, Schließzwang (Muster 62). Erst nach diesem Pass steht die endgültige Absatzstruktur.

**Pass 4 – Rhythmus (Locker/Sachlich: standardmäßig an; Formal: nur auf Wunsch).** Konkrete Stellschrauben:
- Vorfeld rotieren: höchstens ~2 von 3 Sätzen subjektinitial. Varianten: Adverbial, vorangestellter Nebensatz, Objekt, Präpositionalphrase.
- Satzlänge spreizen: pro längerem Absatz mindestens ein Satz unter 6 Wörtern oder über 25 – nur wo die Aussage es trägt.
- Absatzlängen entzerren: nicht jeder Absatz 3–5 Sätze.
- Konnektor-Budget: höchstens ein mechanischer Konnektor pro Absatz; Übergänge bevorzugt über inhaltliche Anknüpfung (Thema-Rhema).
- Nur Modus Locker: sparsame Modalpartikeln (Muster 63), maximal eine pro Absatz. Sachlich/Formal bleiben ohne künstlich nachgerüstete Partikeln.
- Keine künstlichen Fragmente, Regelbrüche oder Partikel einsetzen, nur um „menschlicher“ zu wirken. Rhythmusarbeit nutzt vorhandene Aussage, nicht Fehler oder Schauspiel.

**Pass 5 – Selbst-Audit (immer).** Eigene Änderungen gegen Katalog, Zielprofil und Claim-Lock prüfen: Hat eine Ersetzungsregel neue Monotonie erzeugt (gleiche Ersatzkonstruktion 3+ Mal → Strategie rotieren, vgl. Muster 16 vs. 51)? Quellen, Erfahrung (Muster 59), Faktenanker, Substanz und Output-Länge bleiben durch Input oder Kontext gedeckt. Danach Kurzaudit ausgeben.

**QGIR – begrenzte zweite Runde (optional).** Nur wenn nach Pass 5 echte HIGH/MEDIUM-Cluster bleiben und Claim/Register/Naturalness-Gates grün sind. Maximal 2 normale Pässe, dritter nur bei dokumentiertem schweren Restcluster. Stoppen, sobald weitere Änderungen nur Glattheit, Stimme oder Detektorwirkung verbessern würden. Details: [references/qgir.md](references/qgir.md).

## Entscheidungstabellen

Evidenz:
- Muster 11: vage Autorität ohne konkrete Quelle.
- Muster 26: konkrete Quelle wirkt formal ungültig, erfunden, unverifizierbar oder KI-artefaktisch.
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
5. **Verworfene Kandidaten:** nur ausgeben, wenn Lint-/Audit-Flags vorlagen und nach Prüfung höchstens zwei echte Änderungen nötig waren. Jede Zeile muss auf ein konkretes Flag oder eine konkrete Textstelle verweisen: erwogene Änderung plus ein Satz, warum sie Substanz, Rhythmus, Register oder Belegtreue verschlechtern würde. Ohne konkret geprüfte Stelle kein Eintrag; ist nichts belegbar, Block weglassen.

Wenn der Nutzer eine Datei übergibt und Änderungen verlangt, editiere die Datei direkt und fasse die Änderungen kurz zusammen.

## Referenzen

- Vollständiger Musterkatalog: [references/patterns.md](references/patterns.md)
- Overlap- und Moduslogik: [references/decision-tables.md](references/decision-tables.md)
- QGIR-Loop und Stop-Regeln: [references/qgir.md](references/qgir.md)
- Faktenanker/Claim-Delta: [references/evidence-ledger.md](references/evidence-ledger.md)
- Registerprofile: [references/register-profiles.md](references/register-profiles.md)
- Deutsche Naturalness-Karten: [references/de-naturalness.md](references/de-naturalness.md)
- Kompakter Sammelcheck: `scripts/humanizer_audit.py`
- Unicode-/Quote-Linter: `scripts/unicode_lint.py`
- Rhythmus-/Burstiness-Messung: `scripts/rhythm_lint.py` (`--include-paragraphs` fuer volle Absatzdaten)
- Evidence-/Register-/Naturalness-Checks: `scripts/evidence_lint.py`, `scripts/register_lint.py`, `scripts/german_pattern_lint.py`

<!-- FAST_UPDATE_END -->
