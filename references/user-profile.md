# Nutzerprofil: Feedback-Persistenz

Wiederkehrende Stilvorlieben des Nutzers überleben die Session in `.humanizer/profile.json`
im Arbeitsverzeichnis. Die Datei ist optional; fehlt sie, gelten die Basis-Korridore aus
`references/style-targets.json` unverändert.

## Format

```json
{
  "schema_version": 1,
  "overrides": {
    "sachlich": { "particle_count": { "max": 1 } }
  },
  "notes": [
    { "date": "2026-07-06", "note": "Modalpartikel in Einleitungen beibehalten." }
  ]
}
```

- `overrides` ist strukturgleich zu `style-targets.json`: Profilname → Metrik → Korridor
  (`min`/`max`). Nur Metriken aus dem Stilprofil-Report sind zulässig; unbekannte Profile,
  Metriken oder kaputte Korridore erzeugen eine Warnung und werden ignoriert.
- `notes` sind datierte, freitextliche Regeln. Niemals Nutzertexte oder Textauszüge
  speichern — das Profil hält Regeln fest, keine Korpusse.

## Leseweg

`humanizer_audit.py` und `style_profile.py` lesen die Datei automatisch und legen die
Overrides über die Basis-Korridore. Konfliktregel: **Override ersetzt den Korridor der
Metrik komplett** (kein Tiefen-Merge von `min`/`max`). Überschriebene Korridore tragen im
Delta-Report `"override": true`; das Markdown-Format zeigt sie als `profile_overrides=…`.
`--no-profile` erzwingt die Basis-Korridore (für reproduzierbare Läufe); `--profile <pfad>`
liest bei beiden Skripten einen abweichenden Ort (explizit fehlender Pfad ist ein Fehler).

## Abschluss-Dialog

Nur führen, wenn der Nutzer im Lauf Änderungen zurückgenommen oder wiederholt in dieselbe
Richtung korrigiert hat (etwa Partikeln behalten, kürzere Sätze bevorzugt). Dann am Ende
einmal strukturiert fragen, ob diese Regel gemerkt werden soll — konkret benennen, welcher
Korridor oder welche Notiz sich ändern würde.

Bei Zustimmung `profile.json` aktualisieren:

- Bestehende Einträge mergen, nie ohne ausdrückliche Aufforderung löschen.
- Nur Korridor-Overrides und Regeln als Notiz festhalten, niemals Nutzertext zitieren.
- Beim ersten Anlegen einmalig darauf hinweisen, `.humanizer/` in die `.gitignore` des
  Projekts aufzunehmen; nie selbst fremde `.gitignore`-Dateien editieren.

Ohne erkennbares Korrektur-Muster keinen Dialog führen und nichts schreiben.

## Feedback-Ledger (`decisions.jsonl`)

Getroffene Nutzerentscheidungen über angenommene oder verworfene Kandidaten können zusätzlich
append-only in `.humanizer/decisions.jsonl` gesammelt werden. Die Datei liegt neben
`profile.json`, nicht darin, und nutzt eine JSON-Zeile pro Entscheidung:

```json
{"date": "2026-07-09", "pattern": 64, "lexem": "nahtlos", "mode": "sachlich", "decision": "rejected", "reason": "Wort ist hier Fachbegriff des Kunden"}
{"date": "2026-07-09", "rule": "rhythm/opener_echo", "mode": "locker", "decision": "accepted", "reason": "Openerdopplung war unbeabsichtigt"}
```

- `pattern` (Muster-Nr.) ODER `rule` (Slug für Nicht-Katalog-Regeln) — genau eins von beiden.
- `lexem` optional (einzelnes Wort/Stem, KEIN Satz, KEIN Span).
- `mode` hält den Laufmodus fest.
- `decision`: `accepted` | `rejected`; `reason` freitextlich, beschreibt die REGEL, nie die
  Fundstelle.
- **Privacy hart:** keine Textauszüge, keine Zitate, keine Spans, keine Dateipfade des
  Nutzertexts. Der Ledger hält Entscheidungen über Regeln fest, keine Korpusse.

Abschluss-Dialog: Wenn der Nutzer in einem Lauf konkrete Kandidaten annimmt oder ablehnt, pro
getroffener Nutzer-Entscheidung eine Zeile an `.humanizer/decisions.jsonl` anhängen. Die Datei
bei Bedarf anlegen; bestehende Zeilen nie umschreiben oder löschen ohne explizite Aufforderung.
Beim ersten Anlegen einmalig darauf hinweisen, `.humanizer/` in die `.gitignore` des Projekts
aufzunehmen; nie selbst fremde `.gitignore`-Dateien editieren.

Stufe 1 sammelt nur: keine Auswertung, keine Aggregation, kein Einfluss auf Linter, Preflight
oder Profil. Eval und `make verify` lesen `decisions.jsonl` nie.
