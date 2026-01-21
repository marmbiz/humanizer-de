# Humanizer (Deutsch)

KI-Schreibmuster erkennen und entfernen. Für deutschsprachige Texte.

**Autor:** Martin Moeller | [www.martin-moeller.biz](https://www.martin-moeller.biz)

**Basiert auf:** [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) der Deutschen Wikipedia
**Original Skill:** [Humanizer](https://github.com/blader/humanizer) von [blader](https://github.com/blader)

---

## Was ist das?

Dieses Skill erkennt Schreibmuster, die typisch für KI-Sprachmodelle sind – und hilft Ihnen, sie zu entfernen.

Das Ergebnis ist nicht sterile Korrektur. Es ist Überarbeitung, die Ihrem Text echte deutsche Stimme gibt. Gutes Schreiben darf Ecken haben – es sollte sogar welche haben.

Das Skill folgt deutschen Schreibkonventionen und den Prinzipien von EEAT (Expertise, Erfahrung, Autorität, Vertrauenswürdigkeit).

---

## Installation

### Option 1: Verzeichnis kopieren

1. Kopieren Sie alle Dateien aus diesem Ordner nach `~/.claude/skills/humanizer-de/`
2. Starten Sie Claude Code neu oder laden Sie die Skills neu

### Option 2: Symbolic Link (Linux/Mac)

```bash
ln -s /Users/mm/Local\ Sites/humanizer ~/.claude/skills/humanizer-de
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

Das Skill analysiert **31 verschiedene KI-Schreibmuster** in 5 Kategorien:

### Sprache und Tonfall (12 Muster)
- Übermäßige Betonung von Symbolik ("steht als Zeugnis")
- Werbesprache und Superlative ("atemberaubend")
- Redaktionelle Kommentare ("es ist wichtig zu bemerken")
- Mechanische Konjunktionen ("darüber hinaus", "außerdem")
- Abschnitts-Zusammenfassungen ("insgesamt")
- Unpassendes "Fazit"
- Zu perfekte Schlussfolgerungen
- Negative Parallelismen ("nicht nur... sondern auch")
- Trikolon-Überbenutzung (Regel der Drei)
- Oberflächliche Partizip-I-Konstruktionen
- Vage Autoritäten ("Branchenberichte zeigen")
- Falsche Erweiterungen ("von... bis")

### Stil (4 Muster)
- Übermäßige Fettschrift
- Falsche Listen-Formatierung
- Emojis vor Überschriften
- Gedankenstriche-Überbenutzung (Anglizismus)

### Kommunikation (6 Muster)
- Briefartiges Schreiben
- Kollaborative Kommunikation ("Ich hoffe, das hilft")
- Hinweise auf Wissensgrenzen ("Stand Datum")
- Prompt-Ablehnung ("Als KI kann ich nicht...")
- Platzhaltertext ("[Name einfügen]")
- Links zu Suchanfragen statt Referenzen

### Auszeichnungstext (6 Muster)
- Markdown statt Wikitext
- Fehlerhafter Wikitext
- Defekte Links
- Ungültige DOI/ISBNs
- Inkorrekte Referenzen-Formate
- Falsche Kategorien

### Verschiedenes (3 Muster)
- Abrupte Abbrüche
- Wechsel im Schreibstil
- Ausführliche Bearbeitungszusammenfassungen in Ich-Form

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
