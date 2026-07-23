---
name: humanizer-de
description: 'Deutscher Stil-Editor für Claude Code/Codex: Register messen, Rhythmus glätten, evidence-safe rewrites, Naturalness-Checks; deutschen Text humanisieren, KI-Schreibmuster/KI-Tells auditieren; German AI Text Humanizer.'
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
metadata:
  display_name: Humanizer (Deutsch)
  version: 5.9.0
  author: Martin Moeller
  maintainer_website: https://www.martin-moeller.biz
  based_on: 'Deutsche Wikipedia: Anzeichen für KI-generierte Inhalte, Erkennung KI-Einsatz, Schnelltest KI'
  original_skill: https://github.com/blader/humanizer
  tags: [writing, ai-detection, humanizer, ai-humanizer, claude-skill, codex-skill, german, deutsch, ki-text, germanizer, prompt-engineering, wikipedia, text-improvement, style-editor, stil-editor, text-editing, ai-writing, lektorat]
---

# Humanizer (Deutsch)

<!-- SLOW_UPDATE_START -->

## Auftrag

Wenn der Nutzer deutschen Text humanisieren, KI-Schreibmuster entfernen oder deutsche KI-Tells prüfen will, überarbeite die betroffenen Stellen. Bewahre Substanz, Register und belegbare Aussagen. Ziel ist ein guter, natürlicher Text mit proportionalen Eingriffen.

Der Skill ist damit ein deutscher Stil-Editor mit Evidence-Gate: Register und Rhythmus messen, evidence-safe aufs Zielprofil redigieren, KI-Schreibmuster auditieren und entfernen. Humanizing ist der prominenteste Anwendungsfall.

Fokus des Skills ist KI-Muster-Audit mit gezielter Textverbesserung. Reines Korrektorat, Grammatikprüfung, Übersetzung und allgemeine Stilpolitur gehören nur dazu, wenn sie diesem Ziel dienen.

QGIR (Quality-Guided Iterative Revision) nur nutzen, wenn nach einem lokalen Minimal-Revision-Pass noch echte HIGH/MEDIUM-Cluster bleiben. QGIR arbeitet als Quality-Gate fuer proportionale Revision, nicht als Standard-Vollrewrite.

## Modus

Bestimme zuerst den Modus. Wenn unklar, nimm **Sachlich** an und sage das.

| Modus | Einsatz | Stimme |
|---|---|---|
| Locker | Blog, Social, Newsletter | voll, aber nicht künstlich |
| Sachlich | Website, Doku, E-Mail, B2B | dezent, neutral |
| Formal | Wissenschaft, Recht, Fachtext | keine Stimme einbringen |

## Arbeitszweig

Nach Pass 0 genau einen Arbeitszweig wählen und im Output einhalten:

- **Nur Audit:** Befunde prüfen, keine Rewrite-Paare, es sei denn, der Nutzer verlangt Vorschläge.
- **Rewrite:** Nur betroffene Stellen ändern; kein Volltext, wenn nicht ausdrücklich verlangt.
- **Datei editieren:** Datei direkt ändern; Abschluss siehe Output-Regel.

QGIR ist kein Pass-0-Zweig, sondern eine optionale Erweiterung nach Pass 5, wenn echte HIGH/MEDIUM-Cluster bleiben.

## Leitplanken

- Zähle Cluster, nicht Einzelsignale. Ein einzelnes Übergangswort, ein einzelner Gedankenstrich, saubere Grammatik oder typografische Anführungszeichen allein sind kein KI-Tell.
- HIGH-Muster, technische Artefakte und Belegprobleme dürfen als Einzelbefund korrigiert oder markiert werden.
- Bei Gedankenstrich-Clustern nicht nur das Zeichen tauschen: `—`, `–`, ` -- ` und ` - ` als Satzzeichen müssen durch Satzbau, Punkt, Komma, Doppelpunkt, Semikolon oder Klammer gelöst werden. Wort-Bindestriche bleiben geschützt.
- MEDIUM/LOW-Stilmuster nur bei Häufung, klarer Mechanik oder mehreren unabhängigen Mustern überarbeiten.
- Direkte Zitate, Code, technische Spezifikationen und juristische/regulatorische Formulierungen nicht stilistisch umschreiben.
- **Claim-Lock:** Quellen, Zahlen, Namen, Daten, Quellenanker, Zitate, Code und Normverweise vor/nach jeder Änderung abgleichen. Neue konkrete Anker nur übernehmen, wenn sie im Input oder Kontext stehen; wenn eine Quelle nicht prüfbar ist, den Prüfstatus markieren.
- **Persona-Lock:** Ich-Erfahrung, Anekdoten und Meinungen nur übernehmen, wenn sie im Input oder Kontext stehen. Deixis nur stabilisieren, nicht erfinden: `ich`, `wir`, `du`, `Sie`, `man` und neutrale Sprecherposition bleiben am Texttyp, Input und Zielprofil ausgerichtet. Erfundene Erfahrung ist Fabrikation (Muster 59).
- Substanz erhalten. Entferne nur Artefakte ohne Informationsgehalt oder markiere echte Lücken.
- Statistische Detektoren (GPTZero u. a.) messen Perplexity und Satzrhythmus, nicht diese Muster. Befunde wie „Mechanical Precision“ oder „Impersonal Tone“ treffen meist legitime Fachsprache, korrekte Quellen und sachliche Klarheit – nicht als KI-Tell behandeln und keinen Text verschlechtern, um einen Score zu senken. Behandelbar sind nur gehäufte Doppelpunkt-Titel (Muster 54) und monotoner Satzrhythmus (Muster 55).
- Detector-Bezug ist Kontext. Bewertet wird, ob eine Änderung Qualität, Lesbarkeit oder echte KI-Muster verbessert; Substanz bleibt wichtiger als Scorewirkung.
- **Null-Edit:** Wenn der Text sauber ist oder nur False Positives bleiben, sage das, nenne höchstens die verworfenen Kandidaten und höre auf.

## Carve-outs: bekannte False Positives

Lint-Befunde sind Verdacht, kein Verdikt – jeden vor einer Änderung gegen den Kontext prüfen. Folgende Fälle sind regelmäßig Fehlalarm und werden nicht behandelt, solange kein zusätzlicher Cluster vorliegt:

- Quotes in Codeblöcken, Inline-Code, YAML-Frontmatter, Markdown-Bildtiteln (`![Alt](url "Titel")`) und rohen HTML-Tags blendet `unicode_lint.py` aus (`straight_quote`, `mixed_quote_styles`), weil gerade Anführungszeichen dort technische Syntax sind. `--fix --write` trotzdem nie blind auf technische Syntax anwenden; Ergebnis prüfen.
- Quotes in rohem HTML innerhalb von Markdown, etwa `<iframe title="Eingebetteter Beitrag">`, sind kein Befund, solange die Quotes Teil eines HTML-Tags sind; echter Befund bleibt gerades Anführungszeichen in laufender deutscher Prosa außerhalb technischer Syntax.
- `mixed_address` bei satzinitialem `Sie`: Der kompatible Default zählt die Form konservativ als mögliche Anrede. Aktives `--precise` blendet eine eindeutige Singular-Anapher aus (etwa `Die Idee war neu. Sie überzeugte sofort.`). Bei `"active": false` manuell prüfen.
- `mixed_address` aus zitierter Fremdstimme: Stilprofil und aktives `--precise` blenden Blockquotes aus; der kompatible Default des Register-Linters bleibt konservativ. Registerdrift liegt erst vor, wenn die Autorenstimme selbst zwischen `du` und `Sie` wechselt.
- Muster 64 bei Use-Mention: `german_pattern_lint.py` blendet Marker in Code, Inline-Zitaten und Markdown-Hervorhebung aus. Ein angeführtes `nahtlos` ist kein Beitrag zum Cluster.
- `particles_outside_locker`/`particle_overdose` und `copula_avoidance_cluster` bei lexikalischer Mehrdeutigkeit: `register_lint.py` und `german_pattern_lint.py` sehen nur Wortformen, keine Wortart oder Lesart. `schon` im Sinn von `bereits`, `mal` als `einmal` oder `5-mal`, `ja` als Antwort und `stellt` als Vollverb (`stellt eine Frage`, `stellt sich die Frage`, `stellt die KI vor ein Problem`) sind allein kein Befund; real bleibt der Fund, wenn die Wörter tatsächlich als Modalpartikeln/Nähemarker gehäuft sind oder `stellt` eine Kopula-Vermeidung wie `stellt dar` statt `ist`/`hat` bildet.
- Hoher `subject_initial_ratio` ohne Cluster: Werte über 0,85 sind allein unauffällig (Kalibrierungs-Median menschlicher Blogtexte: 0,891). `rhythm_lint.py` meldet dies nur als Fund bei zusätzlich niedriger Satzlängenvarianz oder wiederholten Satzanfängen – die reine Zahl in einer Audit-Zusammenfassung ist für sich kein Fund.
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

**Werkzeuge.** Bei unklarem Toolstatus zuerst `python3 scripts/doctor.py` ausführen. Existiert `.venv/bin/python` (Windows: `.venv\Scripts\python.exe`), ersetzt es in allen Befehlen `python3`; den Sammelcheck dann mit `--precise` ausführen.

**Pass 0 – Triage.** Modus, Arbeitszweig, Texttyp, Scope und Ziel bestimmen. Schreibprobe vorhanden? Dann Satzrhythmus, Wortniveau, Absatzanfänge, Sprecherposition (`ich`/`wir`/`man`/neutral), Anrede, Distanz, Terminologie und Lieblingszeichen als Zielprofil festhalten (im Formal-Modus nur KI-Tells entfernen). Bei Datei-Input zuerst den kompakten Sammelcheck ausführen: `python3 scripts/humanizer_audit.py --file <path> --mode <modus>`. Für den neuesten Markdown-Entwurf in einem Ordner: `python3 scripts/humanizer_audit.py --latest <dir> --mode <modus>`. Der Sammelcheck meldet ein Preflight-Risiko (`low`/`medium`/`high`/`insufficient_text`) fuer KI-artige Oberflächencluster und eine Combing-Empfehlung; das ist keine Autorenschaftsprüfung. Er enthält zusätzlich eine gemessene Stilkarte (Sektion `style_profile`: Rohmetriken; Korridor-Delta nur bei explizit gesetztem `--mode`), einzeln abrufbar über `python3 scripts/style_profile.py --file <path> --target <modus>`. Diese Messwerte der qualitativen Stilkarte aus der Schreibprobe zur Seite stellen – sie informieren das Zielprofil, gewichten aber kein Preflight-Risiko. Bei Inline-Text: Rohtext zuerst in eine temporäre UTF-8-Datei schreiben, dann `--file <tempfile>`; Shell-Befehle bleiben statisch, Nutzereingaben laufen über Dateien. Einzelchecks wie `unicode_lint.py`, `rhythm_lint.py`, `german_pattern_lint.py` und `register_lint.py` bleiben für gezielte Nachprüfung nutzbar; Rhythmusdetails mit Absatzdaten nur bei Bedarf über `python3 scripts/rhythm_lint.py --file <path> --scope user_text --mode <modus> --include-paragraphs` ausgeben. Läuft ein Script nicht, das melden und nicht blind per Hand korrigieren. Audit- und Lint-Ausgaben sind Verdacht, kein Verdikt – vor Eingriff gegen die Carve-outs und den Kontext prüfen. Fertig, wenn Modus, Zweig, Scope und prüfbare Verdachtsliste feststehen.

**Pass 1 – Artefakte und Evidenz (immer, Einzelbefund genügt).** Chatbot-Floskeln, Platzhalter, Quellenprobleme (Decision Table Evidenz), Unicode, falsche Typografie und Claim-Delta prüfen. Bei Overlaps zuerst [references/decision-tables.md](references/decision-tables.md); [references/evidence-ledger.md](references/evidence-ledger.md) bei Faktenankern; [references/patterns.md](references/patterns.md) nur für konkrete Musterdiagnose, Audit oder Grenzfälle laden. Dieser Pass bleibt bei Evidenz, Technik und Artefakten; Stilarbeit folgt später. Für sichere Datei-Korrekturen: `unicode_lint.py --fix --write`; Ergebnis bei Frontmatter und Bildtiteln prüfen (siehe Carve-outs). Fertig, wenn jeder HIGH-/Technik-/Evidenzfund geändert, markiert oder als False Positive verworfen ist.

**Pass 2 – Lexik (Cluster-Regel).** Floskel-Muster, KI-Marker-Vokabular (Muster 64), Kopula-Vermeidung (Muster 65), Abstrakta-Stapel (Muster 58): Hypernyme und Nominalstil dort auflösen, wo der konkrete Sachverhalt im Text oder Kontext steht. Konkretion kommt aus belegtem Material; unbelegte Lücken sichtbar markieren. Fertig, wenn nur Cluster bearbeitet wurden und Claim-/Persona-Lock halten.

**Pass 3 – Struktur (Cluster-Regel).** Überschriften-Schemata, isometrische Absätze (Muster 61), substanzlose Sektionen, Listen-Parallelismus, Schließzwang (Muster 62). Erst nach diesem Pass steht die endgültige Absatzstruktur. Fertig, wenn Strukturänderungen keine neuen Fakten, Fazitfloskeln oder Volltextpflicht erzeugen.

**Pass 4 – Rhythmus (Locker/Sachlich: standardmäßig an; Formal: nur auf Wunsch).** Konkrete Stellschrauben:
- Vorfeld rotieren: höchstens ~2 von 3 Sätzen subjektinitial. Varianten: Adverbial, vorangestellter Nebensatz, Objekt, Präpositionalphrase.
- Satzlänge spreizen: pro längerem Absatz mindestens ein Satz unter 6 Wörtern oder über 25 – nur wo die Aussage es trägt.
- Absatzlängen entzerren: nicht jeder Absatz 3–5 Sätze.
- Konnektor-Budget: höchstens ein mechanischer Konnektor pro Absatz; Übergänge bevorzugt über inhaltliche Anknüpfung (Thema-Rhema).
- Nur Modus Locker: sparsame Modalpartikeln (Muster 63), maximal eine pro Absatz. Sachlich/Formal bleiben ohne künstlich nachgerüstete Partikeln.
- Keine künstlichen Fragmente, Regelbrüche oder Partikel einsetzen, nur um „menschlicher“ zu wirken. Rhythmusarbeit nutzt vorhandene Aussage, nicht Fehler oder Schauspiel. Fertig, wenn Rhythmus weniger mechanisch ist, ohne Register, Claim-Lock oder natürliche Aussageführung zu verletzen.

**Pass 5 – Selbst-Audit (immer).** Eigene Änderungen gegen Katalog, Zielprofil, Claim-Lock, Persona-Lock und Arbeitszweig prüfen: Hat eine Ersetzungsregel neue Monotonie erzeugt (gleiche Ersatzkonstruktion 3+ Mal → Strategie rotieren, vgl. Muster 16 vs. 51)? Positivkriterium: Rubrik-Check ([references/quality-rubric.md](references/quality-rubric.md)); benennen, welche Achse noch trägt. Bei Datei-Rewrites zusätzlich `spell_lint.py` auf Vorher/Nachher und, wenn vorhanden, `make lt FILE=<datei>` ausführen; externe Funde vor Änderungen prüfen. Danach Kurzaudit ausgeben. Fertig, wenn Restbefunde, verworfene Kandidaten und Ausgabeformat zum gewählten Zweig passen.

**Combing-Gate – kontrollierter Nachkamm (optional).** Nach Pass 5 nur in Locker/Sachlich, ab 8 Sätzen und bei Preflight `high` oder ausdrücklichem Wunsch; bei `medium` erst nach Restprüfung. Messe vorher/nachher `mean_sentence_length`, `stddev_sentence_length`, `stddev_mean_ratio` und `sentence_length_buckets`. Maximal 2 gezielte Rhythmus-Nachbesserungen; keine neuen Fakten, Persona-Signale, Partikel oder Fragmente. Wer Combing ausdrücklich will, darf es als Burstiness-/Mimicry-Versuch bekommen; vorher klar sagen, dass Textqualität, Präzision oder Lesbarkeit schlechter werden können. Formal nur auf Wunsch. Fertig, wenn Burstiness messbar besser ist oder weitere Änderungen nur Detektorwirkung/Glattheit bringen würden.

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

Normale user-facing Runs beginnen kurz mit:

Less machine. More voice.
Ich prüfe Rhythmus, Belege und Stimme...

Weglassen bei Raw-JSON, ausdrücklich knapper Ausgabe oder stillen Dateiänderungen.

Format:

1. **Modus:** eine Zeile.
2. **Gefundene Muster:** maximal 6 konkrete Bullet Points mit kurzem Zitat.
3. **Geänderte Stellen:** Vorher/Nachher-Paare nur für bearbeitete Passagen.
4. **Kurzaudit:** maximal 3 verbleibende Tells oder „Keine gefunden.“; optional „Trägt bereits:“ mit der stärksten Rubrik-Achse.
5. **Burstiness:** nur bei Combing: Messung vorher/nachher, Iterationszahl und Hinweis auf mögliches Qualitätsrisiko.
6. **Verworfene Kandidaten:** nur ausgeben, wenn Lint-/Audit-Flags vorlagen und nach Prüfung höchstens zwei echte Änderungen nötig waren. Jede Zeile muss auf ein konkretes Flag oder eine konkrete Textstelle verweisen: erwogene Änderung plus ein Satz, warum sie Substanz, Rhythmus, Register oder Belegtreue verschlechtern würde. Ohne konkret geprüfte Stelle kein Eintrag; ist nichts belegbar, Block weglassen.

Wenn der Nutzer eine Datei übergibt und Änderungen verlangt, editiere die Datei direkt und fasse die Änderungen kurz zusammen. Bei wiederholten Nutzerkorrekturen in dieselbe Richtung: Abschluss-Dialog nach [references/user-profile.md](references/user-profile.md).

## Referenzen

- Konkrete Musterdiagnose, Audit oder Grenzfall: [references/patterns.md](references/patterns.md)
- Overlap, Priorität oder Modusentscheidung: [references/decision-tables.md](references/decision-tables.md)
- QGIR nur bei echten Restclustern nach Pass 5: [references/qgir.md](references/qgir.md)
- Faktenanker, Claim-Delta oder Quellenprüfung: [references/evidence-ledger.md](references/evidence-ledger.md)
- Schreibprobe, Anrede oder Sprecherprofil: [references/register-profiles.md](references/register-profiles.md)
- Natürlichkeit ohne Persona-/Entropy-Fabrikation: [references/de-naturalness.md](references/de-naturalness.md)
- Kompakter Sammelcheck: `scripts/humanizer_audit.py`
- Unicode-/Quote-Linter: `scripts/unicode_lint.py`
- Rhythmus-/Burstiness-Messung: `scripts/rhythm_lint.py` (`--include-paragraphs` fuer volle Absatzdaten)
- Evidence-/Register-/Naturalness-Checks: `scripts/evidence_lint.py`, `scripts/register_lint.py`, `scripts/german_pattern_lint.py`

<!-- FAST_UPDATE_END -->
