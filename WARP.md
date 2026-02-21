# WARP – Humanizer (Deutsch) Entwicklerleitfaden (v2.2.0-de.2)

**WARP** = "Workflow, Architecture, References, Principles"

Dieser Leitfaden hilft Ihnen, das Humanizer-Deutsch-Projekt zu verstehen, zu warten und zu erweitern.

---

## Projekt-Überblick

### Struktur

```
humanizer-de/
├── SKILL.md              # Hauptimplementierung (die Quelle der Wahrheit)
├── README.md             # Benutzer-Dokumentation
├── WARP.md               # Dieser Datei (Entwickler-Leitfaden)
├── tone-of-voice.txt     # Deutsche Stilrichtlinien (Referenz)
└── .github/              # GitHub-Konfiguration (optional)
    └── workflows/        # CI/CD-Pipelines (optional)
```

### Die Dateien

| Datei | Zweck | Wartung |
|-------|-------|---------|
| **SKILL.md** | Definiert alle 31 Muster und deren Logik | Primäre Quelle; hier beginnt jede Änderung |
| **README.md** | Wie Benutzer das Skill verwenden | Muss mit SKILL.md synchron bleiben |
| **WARP.md** | Developer-Dokumentation | Dieser Leitfaden – aktualisieren Sie ihn, wenn sich die Struktur ändert |
| **tone-of-voice.txt** | Deutsche Schreib-Authentizität-Richtlinien | Referenz für Beispiele und Dokumentation |

---

## Workflow

### 1. Ein neues Muster hinzufügen

**Szenario:** Sie haben ein neues KI-Schreibmuster identifiziert, das nicht in der aktuellen Liste enthalten ist.

**Schritte:**

1. **Im SKILL.md forschen**: Überprüfen Sie alle 31 bestehenden Muster, um sicherzustellen, dass das Muster nicht bereits abgedeckt ist.

2. **Deutsche Wikipedia prüfen**: Das primäre Referenzmaterial ist [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) auf der Deutschen Wikipedia. Prüfen Sie, ob das neue Muster dort genannt wird.

3. **Pattern Template verwenden**:
   ```
   #### [Nummer]. [Deutscher Name]
   **Problem:** [Kurze Erklärung]

   Häuffige Indikatoren:
   - [Indikator 1]
   - [Indikator 2]

   **Warum LLMs das tun:** [Grund aus dem Training]

   **Beispiel:**
   ❌ Schlecht: [KI-generiertes Beispiel]
   ✓ Besser: [Humanisiertes Beispiel]
   ```

4. **Beispiele schreiben**:
   - Das schlechte Beispiel sollte offensichtlich KI-generiert sein
   - Das bessere Beispiel sollte authentisch deutsch klingen
   - Verwenden Sie die Richtlinien in `tone-of-voice.txt`

5. **Kategorie wählen**: Ordnen Sie es einer der 5 Kategorien zu:
   - Sprache und Tonfall (12)
   - Stil (4)
   - Kommunikation (6)
   - Auszeichnungstext (6)
   - Verschiedenes (3)

6. **README.md aktualisieren**: Fügen Sie das Muster der Zusammenfassung hinzu.

7. **Nummer aktualisieren**: Wenn Sie ein Muster hinzufügen, passen Sie alle späteren Nummern an.

### 1b. Upstream-Sync aus `blader/humanizer`

Bei jedem Update des Original-Skills:

1. Letzten Upstream-Stand prüfen (Release/Tag; falls keines vorhanden: `main`-HEAD-Commit dokumentieren).
2. Upstream `SKILL.md`, `README.md`, `WARP.md` laden.
3. Diff gegen `humanizer-de` erstellen.
4. Relevante Änderungen übernehmen (Workflow, Prompt-Logik, Beispiele).
5. Deutsche Anpassungen erhalten (DACH-Stil, deutsche Wikipedia, lokale Metadaten).
6. Versionshistorie in `README.md` aktualisieren.

### 2. Ein bestehendes Muster verbessern

**Szenario:** Ein Benutzer gibt Feedback, dass ein Muster nicht funktioniert oder verbessert werden könnte.

**Schritte:**

1. **Im SKILL.md lokalisieren**: Finden Sie das Muster nach Nummer oder Name.

2. **Beispiele überprüfen**: Sind die Beispiele klar und realistisch?

3. **Indikatoren erweitern**: Gibt es andere häuffige Wendungen, die das Muster ausmachen?

4. **Erklärung klären**: Ist die "Warum LLMs das tun"-Erklärung zutreffend?

5. **Änderungen dokumentieren**: Notieren Sie in Ihrem Commit, was verbessert wurde.

6. **README.md aktualisieren**: Spiegeln Sie Änderungen in der Benutzerdokumentation.

### 3. Muster zusammenführen oder teilen

**Szenario:** Zwei Muster sind zu ähnlich, oder ein Muster umfasst zu viel.

**Zusammenführen:**
- Beide Muster sollten konzeptionell zu einem zusammenpassen
- Alle Indikatoren in das verbleibende Muster verschieben
- Das verschmolzene Muster neu nummerieren
- Alle folgenden Muster umkennzeichnen

**Teilen:**
- Das Muster hat zu viele unterschiedliche Indikatoren
- Erstellen Sie zwei separate Muster für verschiedene Probleme
- Alle darauffolgenden Muster neu nummerieren

---

## Architektur

### Pattern-Format

Jedes Muster folgt dieser Struktur:

```markdown
#### [Nummer]. [Deutscher Titel]
**Problem:** [Kurze Erklärung des Kernproblems]

Häuffige Indikatoren:
- [Spezifische Wörter oder Strukturen]

**Warum LLMs das tun:** [Trainings-Grund – was im Trainingsmaterial zu diesem Verhalten führt]

**Beispiel:**
❌ Schlecht: [Text, der dieses Muster zeigt]
✓ Besser: [Verbesserter Text, der das Muster behebt]
```

**Wichtig:**
- Alle Beispiele sollten *realistische* KI-Outputs sein
- Das "Besser"-Beispiel sollte *authentisch deutsch* klingen
- Verwenden Sie `tone-of-voice.txt` als Referenz

### Kategorisierung

Die 31 Muster sind in 5 Kategorien eingeteilt:

| Kategorie | Anzahl | Fokus |
|-----------|--------|-------|
| Sprache und Tonfall | 12 | Wortwahlund Tonprobleme |
| Stil | 4 | Formatierung und visuelle Struktur |
| Kommunikation | 6 | Chatbot-artiges Verhalten |
| Auszeichnungstext | 6 | Markdown/Wikitext/Referenz-Probleme |
| Verschiedenes | 3 | Alles andere |

---

## Referenzen

### Primäre Quellen

1. **[Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte)** – Deutsche Wikipedia
   - Die offizielle Referenz für dieses Projekt
   - Wird regelmäßig von Wikipedia-Editoren aktualisiert
   - Hier neu erkannte Muster sollten zuerst dokumentiert werden

2. **[Original Humanizer](https://github.com/blader/humanizer)** – Englische Version
   - Basis für die Projektstruktur
   - Reference für 24 englische Muster
   - Hilfe beim Verständnis der Philosophie

### Sekundäre Quellen

- **EEAT Guidelines:** [Google's Search Quality Guidelines](https://developers.google.com/search/docs/beginner/eeat-signals)
- **Deutsche Schreibweise:** [Duden Online](https://www.duden.de)
- **Wikipedia Style:** [Wikipedia Bearbeitungshilfe](https://de.wikipedia.org/wiki/Hilfe:Bearbeitungsanleitung)
- **AI Detection Research:** Akademische Paper zu LLM-Ausgabe-Charakteristiken

---

## Prinzipien

### 1. Authentizität vor Perfektion

Das Skill verbessert Texte, um sie authentischer, nicht perfekter zu machen.

**Falsch:** "Entfernen Sie alle Fehler" → Text wird steril
**Richtig:** "Machen Sie den Text naturalistisch" → Text klingt echt

### 2. Kontext über Regeln

Ein Muster könnte in einem Kontext gültig sein, in einem anderen aber nicht.

Beispiel: "Darüber hinaus" ist kein Problem in formalen Texten, wird aber zu häufig von KI-Modellen verwendet.

### 3. Deutsche Stimme

Der Fokus liegt auf *authentischem deutschem Schreiben*, nicht auf generischer Verbesserung.

- Deutsche Satzstrukturen
- Regionale Variabilität (DACH)
- Konventionen von deutschen Wikipedia-Artikeln

### 4. Transparenz

Das Skill sollte erklären, *warum* etwas ein Problem ist, nicht nur das Problem flaggen.

Jedes Muster hat eine "Warum LLMs das tun"-Erklärung, damit Benutzer verstehen, was los ist.

### 5. Menschlich-zentriert

Das Skill dient als *Werkzeug für menschliche Editoren*, nicht als Automatisierung.

Redaktoren sollten das Ergebnis überprüfen und können intelligent Änderungen ablehnen.

---

## Wartung

### Regelmäßige Aufgaben

**Monatlich:**
- Überprüfen Sie Issues und Pull Requests
- Sammeln Sie Benutzer-Feedback
- Suchen Sie auf der Wikipedia-Seite nach neuen Erkenntnissen

**Quartal:**
- Überprüfen Sie, ob neue LLM-Modelle neue Muster erzeugen
- Aktualisieren Sie Beispiele, falls nötig
- Prüfen Sie, ob Links/Referenzen noch gültig sind

**Jährlich:**
- Überprüfen Sie die Gesamtstruktur und Kohärenz
- Führen Sie größere Überarbeitungen durch, falls nötig
- Planen Sie Versionsnum-Updates

### Versionierung

Das Projekt folgt [Semantic Versioning](https://semver.org/):

- **Major (1.0.0 → 2.0.0):** Grundlegende Umstrukturierung
- **Minor (1.0.0 → 1.1.0):** Neue Muster hinzugefügt
- **Patch (1.0.0 → 1.0.1):** Verbesserungen an bestehenden Mustern

Aktuelle Version: **2.2.0-de.2** – Upstream v2.2.0 integriert, gegen `main` (`d8085c7`) geprüft, deutsche Anpassung erhalten

### Testing

**Manuelles Testen vor Release:**

1. **Installationstest:**
   ```bash
   cp -r humanizer-de ~/.codex/skills/humanizer-de
   ```

2. **Funktionstest:**
   ```
   /humanizer
   [KI-generierter Text]
   ```

3. **Pattern-Erkennungstest:**
   - Erstellen Sie Text mit bekannten Mustern
   - Überprüfen Sie, ob das Skill diese erkennt

4. **Dokumentations-Konsistenz:**
   - README.md listet alle Muster auf
   - SKILL.md definiert alle Muster
   - Nummern sind konsistent

---

## Lokal entwickeln

Dieses Projekt lebt in `/Users/mm/Local Sites/humanizer/`

### Änderungen testen

1. Bearbeiten Sie SKILL.md oder andere Dateien
2. Starten Sie Claude Code neu oder laden Sie Skills neu
3. Testen Sie mit `/humanizer [Text]`

### Datei-Synchronisation

Wenn Sie Muster in SKILL.md hinzufügen:
1. Aktualisieren Sie README.md (Muster-Zusammenfassung)
2. Aktualisieren Sie tone-of-voice.txt (falls nötig)
3. Überprüfen Sie, dass Nummern konsistent sind

### Backup erstellen

```bash
cp -r "/Users/mm/Local Sites/humanizer" "/Users/mm/Local Sites/humanizer-backup-$(date +%Y%m%d)"
```

---

## Häuffig gestellte Fragen

### F: Wer wartet dieses Projekt?

Martin Moeller ([www.martin-moeller.biz](https://www.martin-moeller.biz)) ist der Maintainer der deutschen Version.

### F: Warum nicht mehr oder weniger Muster?

Die 31 Muster basieren auf der Deutsch Wikipedia-Seite "Anzeichen für KI-generierte Inhalte". Wenn diese Seite aktualisiert wird, sollten wir das auch tun.

### F: Sollte ich englische Muster einfach übersetzen?

Nein. Das Englische Humanizer-Projekt hat 24 Muster. Die Deutsche Version hat 31, weil:
- Deutsche Wikipedia ist umfassender
- Deutschsprachige LLMs haben andere Muster
- Deutsche Grammatik ermöglicht andere Probleme

### F: Wie mit Widersprüchen bei Stilrichtlinien umgehen?

Beispiel: Ein Muster sagt "vermeiden Sie Partizip-I", aber `tone-of-voice.txt` sagt, es sei manchmal okay.

**Lösung:** Das Skill ist für Muster, nicht absolute Regeln. Wenn ein Muster vom Kontext abhängt, erklären Sie das in der Erklärung "Warum LLMs das tun".

### F: Sollte ich alle 31 Muster sofort testen?

Nein. Priorisieren Sie:
1. Muster, die Sie gerade hinzugefügt/geändert haben
2. Muster, über die Benutzer Feedback gegeben haben
3. Neue LLM-Muster, die Sie beobachten

### F: Wer wartet das Projekt?

Dieses Projekt wird von der Community gepflegt. Jeder kann:
- Issues öffnen
- Pull Requests senden
- Feedback geben

---

## Zusammenfassung für Maintainer

**Wenn Sie ein Issue/PR erhalten:**

1. **Kategorie:** Neues Muster? Bestehendes Muster verbessern? Dokumentation?
2. **Quelle:** Basiert es auf der Wikipedia-Seite? Echten KI-Outputs?
3. **Qualität:** Sind Beispiele klar? Ist die Erklärung gültig?
4. **Konsistenz:** Werden README.md und SKILL.md synchron gehalten?
5. **Test:** Funktioniert es in der Praxis?

**Wenn Sie Features priorisieren:**

1. Bugs die Funktionalität beeinträchtigen
2. Neue Muster von Wikipedia
3. Benutzerfeedback
4. Dokumentation verbessern

---

**Viel Erfolg bei der Wartung!**

*Das Humanizer-Deutsch-Projekt entwickelt sich weiter, wenn die KI-Technologie vorankommen und wir mehr über authentisches Schreiben lernen.*

---

**Projekt-Maintainer:** Martin Moeller (www.martin-moeller.biz)
**Lokal gespeichert:** `/Users/mm/Local Sites/humanizer/`
**Version:** 2.2.0-de.2
**Basiert auf:** Original Humanizer von blader + German Wikipedia Analyse
