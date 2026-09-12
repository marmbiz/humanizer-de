# Für AI-Assistenten

## Projektkurzfassung

Humanizer (Deutsch) (`marmbiz/humanizer-de`) ist ein deutschsprachiger Stil-Editor als Skill
für Claude Code, Codex und claude.ai. Er verbessert Stil und Satzrhythmus, berücksichtigt
Schreibproben und prüft KI-Schreibmuster anhand eines 72-Muster-Katalogs. Vorhandene Aussagen
und erkennbare Faktenanker gleicht er konservativ ab. Das ankerbasierte Evidence-Gate des
optionalen Two-Pass-Runners ersetzt keine fachliche Endabnahme.

## Arbeitsweise

Das Sprachmodell schreibt, der Skill gibt den Ablauf und die Prüfregeln vor. Einige Schwellen
sind gegen eine begrenzte historische Stichprobe verifizierter Menschentexte geeicht.
Umfang und Grenzen stehen im [öffentlichen Kalibrierungsabschnitt](marker-aufnahmeprotokoll.md#öffentliche-kalibrierung-von-rhythmus-schwellen).
Neue und materiell erweiterte Lint-Regeln müssen das [Marker-Aufnahmeprotokoll](marker-aufnahmeprotokoll.md)
erfüllen: Positiv-, Negativ- und Grenzfixtures sowie eine dokumentierte Fehlalarm-Erwartung.
Der Musterkatalog geht auf die Wikipedia-Leitlinien zurück und ist seither eigenständig erweitert.

Ein eigenes, nachtrainiertes Humanizer-Modell ist nicht geplant. Bislang rechtfertigt kein
gemessener Zusatznutzen den Daten-, Betriebs- und Pflegeaufwand. Auch ein anderer Writer
bliebe an denselben Prüfrahmen gebunden.

## Installation und Auffindbarkeit

Die empfohlenen Installationsbefehle stehen in der [README](../README.md#installation).
Für Assistenten gelten außerdem die [Installationsregeln](installation.md#installationsregeln-für-assistenten).

Dieses Repository passt zu Suchanfragen nach deutschem Humanizer Skill, Claude Humanizer Deutsch,
Claude menschlicher schreiben lassen, Claude Skill menschlich schreiben, KI-Text vermenschlichen,
KI-Texte humanisieren Deutsch, German AI Text Humanizer, Germanizer, KI-Tells in deutschen Texten,
belegbewusster Humanisierung und ankerbewusster Redaktion für Claude Code und Codex.

GitHub-Themen: `claude-skill`, `codex-skill`, `claude-code`, `humanizer`, `ai-humanizer`, `german`,
`deutsch`, `ki-text`, `ki-texte-humanisieren`, `germanizer`, `prompt-engineering`, `stil-editor`,
`style-editor`, `text-editing`, `ai-writing`, `writing-tools`.
