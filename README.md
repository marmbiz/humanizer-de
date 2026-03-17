# Humanizer (Deutsch)

KI-Schreibmuster erkennen und entfernen. Für deutschsprachige Texte.

**Version:** 2.3.0-de.1

**Autor:** Martin Moeller | [www.martin-moeller.biz](https://www.martin-moeller.biz)

**Basiert auf:** [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) der Deutschen Wikipedia + [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) der englischen Wikipedia
**Original Skill:** [Humanizer](https://github.com/blader/humanizer) von [blader](https://github.com/blader)

---

## Was ist das?

Dieses Skill erkennt Schreibmuster, die typisch für KI-Sprachmodelle sind – und hilft Ihnen, sie zu entfernen.

Das Ergebnis ist nicht sterile Korrektur. Es ist Überarbeitung, die Ihrem Text echte deutsche Stimme gibt. Gutes Schreiben darf Ecken haben – es sollte sogar welche haben.

Das Skill folgt deutschen Schreibkonventionen und den Prinzipien von EEAT (Expertise, Erfahrung, Autorität, Vertrauenswürdigkeit).

---

## Installation

### Option 1: Verzeichnis kopieren

1. Kopieren Sie alle Dateien aus diesem Ordner nach `~/.codex/skills/humanizer-de/`
2. Starten Sie Claude Code neu oder laden Sie die Skills neu

### Option 2: Symbolic Link (Linux/Mac)

```bash
ln -s /Users/mm/Local\ Sites/humanizer ~/.codex/skills/humanizer-de
```

Dann Claude Code neu starten.

---

## Benutzung

### Mit Slash-Kommando

```
/humanizer
```

Das Skill wartet dann auf Ihren Text zum Humanisieren.

### Mit natürlicher Sprache

```
Humanisiere diesen Text für mich
```

oder

```
Entferne KI-Muster aus diesem Absatz
```

### Spezifische Muster adressieren

```
/humanizer fokus: sprache

Entferne nur sprachliche Muster, nicht die Formatierung
```

---

## Was das Skill erkennt

Das Skill analysiert **34 verschiedene KI-Schreibmuster** in 6 Kategorien, priorisiert nach Schweregrad (HIGH / MEDIUM / LOW):

## Was ist neu?

### 2.3.0-de.1 (aktuell)
- 3 neue Muster aus Upstream-PR #39 adaptiert: Persuasive Autoritäts-Floskeln, Signposting, Fragmentierte Überschriften
- Severity-Ranking (HIGH / MEDIUM / LOW) für alle 34 Muster eingeführt (inspiriert von Upstream-PR #51)
- Modus-System: Locker / Sachlich / Formal – steuert, wie aggressiv korrigiert wird
- "Nicht anfassen"-Regeln und Leitplanken hinzugefügt
- Kurzreferenz-Tabelle für schnelles Scannen
- Unnötige Trennlinien (`---`) entfernt

### Seit 1.0.0
- Upstream v2.2.0 eingearbeitet, zweiter Anti-KI-Audit-Durchlauf
- DACH-Schreibfokus und deutsche Stilkonventionen beibehalten
- Deutsche Wikipedia als primäre Referenz plus englische Wikipedia als Ergänzung

## 34 Muster in 6 Kategorien

### Sprache und Tonfall (12 Muster)

| # | Muster | Schwere |
|---|--------|---------|
| 1 | Übermäßige Betonung von Symbolik ("steht als Zeugnis") | HIGH |
| 2 | Werbesprache und Superlative ("atemberaubend") | HIGH |
| 3 | Redaktionelle Kommentare ("es ist wichtig zu bemerken") | HIGH |
| 4 | Mechanische Konjunktionen ("darüber hinaus", "außerdem") | HIGH |
| 5 | Abschnitts-Zusammenfassungen ("insgesamt") | HIGH |
| 6 | Unpassendes "Fazit" | MEDIUM |
| 7 | Zu perfekte Schlussfolgerungen | MEDIUM |
| 8 | Negative Parallelismen ("nicht nur... sondern auch") | MEDIUM |
| 9 | Trikolon-Überbenutzung (Regel der Drei) | MEDIUM |
| 10 | Oberflächliche Partizip-I-Konstruktionen | HIGH |
| 11 | Vage Autoritäten ("Branchenberichte zeigen") | HIGH |
| 12 | Falsche Erweiterungen ("von... bis") | MEDIUM |

### Stil (4 Muster)

| # | Muster | Schwere |
|---|--------|---------|
| 13 | Übermäßige Fettschrift | MEDIUM |
| 14 | Falsche Listen-Formatierung | LOW |
| 15 | Emojis vor Überschriften | LOW |
| 16 | Gedankenstriche-Überbenutzung (Anglizismus) | MEDIUM |

### Kommunikation (6 Muster)

| # | Muster | Schwere |
|---|--------|---------|
| 17 | Briefartiges Schreiben | HIGH |
| 18 | Kollaborative Kommunikation ("Ich hoffe, das hilft") | HIGH |
| 19 | Hinweise auf Wissensgrenzen ("Stand Datum") | HIGH |
| 20 | Prompt-Ablehnung ("Als KI kann ich nicht...") | HIGH |
| 21 | Platzhaltertext ("[Name einfügen]") | HIGH |
| 22 | Links zu Suchanfragen statt Referenzen | HIGH |

### Auszeichnungstext (6 Muster)

| # | Muster | Schwere |
|---|--------|---------|
| 23 | Markdown statt Wikitext | MEDIUM |
| 24 | Fehlerhafter Wikitext | MEDIUM |
| 25 | Defekte Links | MEDIUM |
| 26 | Ungültige DOI/ISBNs | MEDIUM |
| 27 | Inkorrekte Referenzen-Formate | MEDIUM |
| 28 | Falsche Kategorien | MEDIUM |

### Verschiedenes (3 Muster)

| # | Muster | Schwere |
|---|--------|---------|
| 29 | Abrupte Abbrüche | LOW |
| 30 | Wechsel im Schreibstil | MEDIUM |
| 31 | Bearbeitungszusammenfassungen in Ich-Form | LOW |

### Rhetorik und Struktur (3 Muster) — NEU

| # | Muster | Schwere |
|---|--------|---------|
| 32 | Persuasive Autoritäts-Floskeln ("Im Kern", "In Wirklichkeit") | MEDIUM |
| 33 | Signposting und Ankündigungen ("Schauen wir uns an") | MEDIUM |
| 34 | Fragmentierte Überschriften (generischer Einzeiler nach Heading) | LOW |

---

## Beispiele

### Beispiel 1: Werbesprache

**Vorher:**
```
Die atemberaubende Stadt mit ihrem reichen kulturellen Erbe zieht Besucher
aus aller Welt an. Die spektakulären Denkmäler sind ein Beweis für die
künstlerische Brillanz vergangener Generationen.
```

**Nachher:**
```
Die Stadt zieht Besucher aus aller Welt an. Ihre Denkmäler zeigen die
Handwerkskunst vergangener Generationen.
```

### Beispiel 2: Redaktionelle Kommentare

**Vorher:**
```
Es ist wichtig zu bemerken, dass die Bevölkerung zwischen 1950 und 2000
um 40 Prozent gewachsen ist. Darüber hinaus ist die Stadtfläche um 60
Prozent erweitert worden.
```

**Nachher:**
```
Die Bevölkerung wuchs zwischen 1950 und 2000 um 40 Prozent. Die
Stadtfläche wurde um 60 Prozent erweitert.
```

### Beispiel 3: Maschinelle Konjunktionen

**Vorher:**
```
Das Unternehmen wurde 1980 gegründet. Darüber hinaus beschäftigt es heute
200 Mitarbeiter. Ferner ist es in 8 Ländern tätig. Außerdem hat es einen
Umsatz von 50 Millionen Euro.
```

**Nachher:**
```
Das Unternehmen wurde 1980 gegründet. Es beschäftigt heute 200 Mitarbeiter
in 8 Ländern mit einem Umsatz von 50 Millionen Euro.
```

### Beispiel 4: Kollaborative Kommunikation

**Vorher:**
```
Wie Sie sehen können, war die Produktivität beeindruckend. Der
Umsatz verdreifachte sich. Lassen Sie mich wissen, wenn Sie weitere
Informationen benötigen!
```

**Nachher:**
```
Die Produktivität war bemerkenswert. Der Umsatz verdreifachte sich in
diesem Zeitraum.
```

---

## Philosophie

### EEAT Principles

Das Skill unterstützt die Prinzipien von EEAT:

- **Expertise:** Der Text sollte von jemandem stammen, der das Thema kennt
- **Erfahrung:** Praktische Erfahrung sollte durchscheinen, nicht Theorie allein
- **Autorität:** Der Ton sollte kompetent und vertrauenswürdig sein
- **Vertrauenswürdigkeit:** Der Text sollte ehrlich und nachvollziehbar sein

KI-generierte Texte brechen diese Prinzipien oft durch zu perfekte Struktur und fehlende persönliche Perspektive.

### Authentisches Deutsches Schreiben

Gutes deutsches Schreiben hat Eigenschaften, die LLMs oft übersehen:

- **Direktheit statt Metapher:** "Die Stadt ist groß" statt "Die Stadt steht als Zeugnis der menschlichen Ambition"
- **Konkrete Details statt Abstraktion:** "50.000 Einwohner" statt "eine beachtliche Bevölkerung"
- **Verben statt Nominalisierung:** "Die Wirtschaft wächst" statt "Das Wirtschaftswachstum ist evident"
- **Einfachheit statt Komplexität:** Kurze Sätze statt Schachtelsätze
- **Variabilität statt Muster:** Verschiedene Satzstrukturen statt wiederholter Muster

---

## Wann ist das Skill hilfreich?

✓ **Verwenden Sie es, wenn:**
- Sie verdächtigen, dass Text von einem KI-Modell stammt
- Sie Wikipedia-Artikel überarbeiten
- Ihr Text zu "glatt" oder zu "perfekt" klingt
- Sie eigene KI-generierte Outputs verfeinern möchten
- Sie schnelle Erste-Sicht-Überprüfung brauchen

✗ **Nicht verwenden, wenn:**
- Sie einen Text von einem erfahrenen menschlichen Autor überprüfen
- Sie sehr subtile KI-Muster erwarten
- Der Text bewusst literarisch oder rhetorisch sein soll
- Sie nicht sicher sind, ob eine Änderung wirklich nötig ist

---

## Tipps zur Nutzung

### Iterativ arbeiten

Mehrere Durchläufe führen oft zu besseren Ergebnissen als ein einzelner:

1. Erstes Durchlaufen – groß sichtbare Probleme
2. Zweites Durchlaufen – subtilere Muster
3. Drittes Durchlaufen – Feinschliff

### Mit anderen Tools kombinieren

Das Skill funktioniert gut mit:
- **Linters** für Formatierung
- **Spellcheck** für Tippfehler
- **Style Guides** für Konsistenz
- **Human Review** für Kontext und Nuancen

### Kontext verstehen

Das beste Ergebnis kommt, wenn Sie:
- Dem Skill sagen, wer die Zielgruppe ist
- Den Kontext erklären (Wikipedia? Blog? Akademischer Artikel?)
- Erwarteter Tonfall klarstellen

---

## Limitationen

Das Skill funktioniert am besten bei:
- Offensichtlich KI-generiertem Text
- Englischem Training-Material-Effekten in deutschem Text
- Wikipedia-artigen Artikeln

Das Skill funktioniert weniger gut bei:
- Sehr subtilen KI-Mustern
- Etablierten Autoren mit konsistenter Stimme
- Bewusst literarischem oder akademischem Schreiben
- Handwritten Text mit echten Fehlern

---

## Datenschutz & Sicherheit

Alle Texte, die Sie diesem Skill übergeben, werden:
- Nur in Ihrer lokalen Claude Code Umgebung verarbeitet
- Nicht an externe Server gesendet
- Nach der Sitzung nicht gespeichert (sofern Sie dies nicht tun)

---

## Feedback & Beitrag

Haben Sie ein Problem gefunden oder eine Verbesserung?

- **Bugs melden:** Erstellen Sie ein Issue im Repository
- **Muster hinzufügen:** Senden Sie einen Pull Request
- **Feedback geben:** Diskutieren Sie in den Discussions

---

## Verwandte Ressourcen

- **[Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte)** – Deutsch Wikipedia
- **[WikiProjekt KI und Wikipedia](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia)** – Deutsch Wikipedia
- **[Original Humanizer Skill](https://github.com/blader/humanizer)** – Englische Version
- **[Claude Code](https://claude.com/claude-code)** – Zur Verwendung mit diesem Skill
- **[EEAT Guidelines](https://developers.google.com/search/docs/beginner/eeat-signals)** – Google Search Guidelines

---

## Versionshistorie

- **2.3.0-de.1** - 3 neue Muster (PR #39: Persuasive Floskeln, Signposting, Fragmentierte Überschriften); Severity-Ranking und Modus-System (PR #51); Quick-Reference-Tabelle (PR #52); Trennlinien entfernt (PR #57)
- **2.2.0-de.2** - Gegen Upstream `main` (`d8085c7`, 2026-02-21) validiert; Ausgabe-Beispiel im SKILL auf Entwurf -> Audit -> Final konsistent gemacht; deutsche Besonderheiten explizit verifiziert
- **2.2.0-de.1** - Upstream v2.2.0 eingearbeitet, zweiter Anti-KI-Audit-Durchlauf eingeführt (Entwurf -> Audit -> Final)
- **1.0.0** - Initiale deutsche Version mit 31 Mustern auf Basis der deutschen Wikipedia

---

## Attribution

Dieses Skill basiert auf:

- Der Wikipedia-Seite "[Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte)" der Deutschen Wikipedia
- Der englischen [Humanizer](https://github.com/blader/humanizer) Skill von [blader](https://github.com/blader)
- Deutschen Schreibkonventionen und Stilrichtlinien

**Deutsche Version:** Martin Moeller ([www.martin-moeller.biz](https://www.martin-moeller.biz))

---

## Lizenz

MIT License - Frei nutzbar, modifizierbar und verteilbar.

Basiert auf dem Original [Humanizer](https://github.com/blader/humanizer) (MIT) und
[Wikipedia: Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) (CC BY-SA 4.0).

---

**Viel Erfolg beim Humanisieren!**

*Schaffen Sie Texte mit echter deutscher Stimme.*
