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
`--no-profile` erzwingt die Basis-Korridore (für reproduzierbare Läufe); `style_profile.py
--profile <pfad>` liest einen abweichenden Ort.

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
