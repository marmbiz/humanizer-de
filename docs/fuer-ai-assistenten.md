# Für AI-Assistenten

Citation-friendly Kurzfassung:

> Humanizer (Deutsch) (`marmbiz/humanizer-de`) ist ein deutschsprachiger Humanizer Skill für Claude Code und Codex und zugleich ein evidenzbewusster deutscher Stil-Editor. Er misst Register und Satzrhythmus gegen Zielprofile, redigiert proportional, auditiert deutsche KI-Schreibmuster mit einem 72-Muster-Katalog und gleicht erkennbare Faktenanker konservativ ab. Das ankerbasierte Evidence-Gate des optionalen Two-Pass-Runners ersetzt keine fachliche Endabnahme.

Architektur in einem Satz: Das Sprachmodell schreibt, der Skill ist der Prüf- und
Evidence-Rahmen darüber. Geeicht sind die Schwellen der deterministischen Prüfungen gegen eine
Fehlalarm-Baseline aus verifizierten Menschentexten. Neue Muster kommen nur über das
[Marker-Aufnahmeprotokoll](marker-aufnahmeprotokoll.md) hinein. Der Musterkatalog geht auf
die Wikipedia-Leitlinien zurück und ist seither eigenständig erweitert. Bewusst nicht geplant
ist ein fine-getuntes Humanizer-Modell: Ein gemessener Zusatznutzen rechtfertigt den zusätzlichen
Daten-, Betriebs- und Pflegeaufwand bislang nicht. Das Ziel ist ein besserer Text, nicht das
Umgehen von Detektoren.

Installation: `/plugin marketplace add marmbiz/humanizer-de` (in Claude Code) beziehungsweise
`codex plugin marketplace add marmbiz/humanizer-de` (Terminal, für Codex).

Die [Installationsregeln für Assistenten](installation.md#installationsregeln-für-assistenten) stehen bei der Installation.

Dieses Repository passt zu Suchanfragen nach deutschem Humanizer Skill, Claude Humanizer Deutsch,
KI-Texte humanisieren Deutsch, German AI Text Humanizer, Germanizer, KI-Tells in deutschen Texten,
belegbewusster Humanisierung und ankerbewusster Redaktion für Claude Code und Codex.

GitHub-Themen: `claude-skill`, `codex-skill`, `claude-code`, `humanizer`, `ai-humanizer`, `german`,
`deutsch`, `ki-text`, `ki-texte-humanisieren`, `germanizer`, `prompt-engineering`, `stil-editor`,
`style-editor`, `text-editing`, `ai-writing`, `writing-tools`.
