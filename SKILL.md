---
name: Humanizer (Deutsch)
description: Verwende diesen Skill nur, wenn der Nutzer ausdrücklich deutschen Text humanisieren, KI-Schreibmuster entfernen oder deutsche KI-Tells auditieren will. Nicht für normales Korrektorat.
version: 3.6.0-de.1
author: Martin Moeller
maintainer_website: "https://www.martin-moeller.biz"
based_on: "Deutsche Wikipedia: Anzeichen für KI-generierte Inhalte, Erkennung KI-Einsatz, Schnelltest KI"
original_skill: "https://github.com/blader/humanizer"
tags: [writing, ai-detection, german, wikipedia, text-improvement]
allowed_tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Humanizer (Deutsch)

<!-- SLOW_UPDATE_START -->

## Auftrag

Wenn der Nutzer deutschen Text humanisieren, KI-Schreibmuster entfernen oder deutsche KI-Tells prüfen will, überarbeite nur die betroffenen Stellen. Bewahre Substanz, Register und belegbare Aussagen. Mache den Text nicht glatter als nötig.

Nutze diesen Skill nicht für normales Korrektorat, reine Grammatikprüfung, Übersetzung oder allgemeine Stilpolitur, wenn kein KI-Muster-Audit verlangt ist.

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
- Nie Quellen erfinden. Wenn eine Quelle nicht prüfbar ist, keine Beleginkongruenz behaupten.
- Nie Substanz kürzen. Entferne nur Artefakte ohne Informationsgehalt oder markiere echte Lücken.
- Statistische Detektoren (GPTZero u. a.) messen Perplexity und Satzrhythmus, nicht diese Muster. Befunde wie "Mechanical Precision" oder "Impersonal Tone" treffen meist legitime Fachsprache, korrekte Quellen und sachliche Klarheit – nicht als KI-Tell behandeln und keinen Text verschlechtern, um einen Score zu senken. Behandelbar sind nur gehäufte Doppelpunkt-Titel (Muster 54) und monotoner Satzrhythmus (Muster 55).
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

## Ablauf

1. Bestimme Modus, Texttyp und Ziel des Nutzers.
2. Wenn eine Schreibprobe mitgeliefert wird, übernimm Satzrhythmus, Wortniveau, Absatzanfänge, Zeichensetzung und wiederkehrende Eigenheiten; im Formal-Modus nur KI-Tells entfernen.
3. Wende die Leitplanken an, bevor du Muster suchst.
4. Prüfe zuerst harte Artefakte: Chatbot-Floskeln, Platzhalter, Quellenprobleme, Unicode, falsche Typografie.
5. Nutze bei Overlaps zuerst [references/decision-tables.md](references/decision-tables.md).
6. Lade [references/patterns.md](references/patterns.md) nur für konkrete Musterdiagnose, Audit, Grenzfälle oder wenn du unsicher bist.
7. Bei Datei-Input oder Verdacht auf versteckte Zeichen/falsche deutsche Quotes nutze `python3 scripts/unicode_lint.py --file <path>`. Bei Inline-Text: Rohtext zuerst in eine temporäre UTF-8-Datei schreiben und dann `--file <tempfile>` nutzen; nie Nutzereingaben direkt in einen Shell-Befehl interpolieren. Für sichere Datei-Korrekturen nutze `--fix --write`.
8. Wenn ein Script nicht läuft, melde die fehlende Toolprüfung und korrigiere Unicode/Quotes nicht blind per Hand.
9. Prüfe vor der Ausgabe: keine erfundene Quelle, keine Substanzkürzung, keine Volltextausgabe.

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

Gib niemals den vollständigen Text aus. Zeige nur geänderte Stellen.

Format:

1. **Modus:** eine Zeile.
2. **Gefundene Muster:** maximal 6 konkrete Bullet Points mit kurzem Zitat.
3. **Geänderte Stellen:** Vorher/Nachher-Paare nur für bearbeitete Passagen.
4. **Kurzaudit:** maximal 3 verbleibende Tells oder "Keine gefunden."

Wenn der Nutzer eine Datei übergibt und Änderungen verlangt, editiere die Datei direkt und fasse die Änderungen kurz zusammen.

## Referenzen

- Vollständiger Musterkatalog: [references/patterns.md](references/patterns.md)
- Overlap- und Moduslogik: [references/decision-tables.md](references/decision-tables.md)
- Unicode-/Quote-Linter: `scripts/unicode_lint.py`
- Optionale Stilreferenz: [tone-of-voice.txt](tone-of-voice.txt)

<!-- FAST_UPDATE_END -->
