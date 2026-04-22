---
name: Humanizer (Deutsch)
description: Erkennt und entfernt KI-generierte Schreibmuster aus deutschsprachigen Texten. Basierend auf Wikipedia-Leitlinien (Anzeichen für KI-generierte Inhalte, Erkennung KI-Einsatz, Schnelltest KI), inklusive zweitem Anti-KI-Audit-Durchlauf und optionaler Stimmkalibrierung. Erkennt u.a. aufgeblähte Symbolik, Werbesprache, mechanische Konjunktionen, vage Autoritäten, Gedankenstriche-Übernutzung, Trikolon, KI-Vokabular, negative Parallelismen, Passivkonstruktionen, persuasive Floskeln, Signposting, fragmentierte Überschriften, rhetorische Fake-Fragen, Menschheits-Eröffnungen, "heutige Welt"-Framing, aspirative Unternehmensschlüsse, Konditional-Stapel, fehlkalibriertes epistemisches Vertrauen, Beleginkongruenz, versteckte Unicode-Zeichen, Standard-Kapitel ohne Substanz und Anglizismus-Strukturen.
version: 3.2.4-de.1
author: Martin Moeller
maintainer_website: "https://www.martin-moeller.biz"
based_on: "Deutsche Wikipedia: Anzeichen für KI-generierte Inhalte, Erkennung KI-Einsatz, Schnelltest KI"
original_skill: "https://github.com/blader/humanizer"
tags: [writing, ai-detection, german, wikipedia, text-improvement]
allowed_tools: [Read, Write, Edit, Grep, Glob]
---

# Humanizer (Deutsch)

Ein Skill zur Erkennung und Entfernung von KI-generierten Schreibmustern aus deutschsprachigen Texten.

## Philosophie

Dies ist kein steriler Korrektur-Skill. Ziel ist nicht, den Text einfach zu bereinigen, sondern ihm eine echte deutsche Stimme zu geben. Gutes deutsches Schreiben darf Ecken haben – es sollte sogar welche haben.

Das Skill befolgt die Prinzipien von EEAT (Expertise, Erfahrung, Autorität, Vertrauenswürdigkeit) und regionale deutsche Schreibkonventionen, um Texte authentisch und überzeugend zu gestalten.

## Wann verwenden Sie den Skill?

- Wenn Sie verdächtigen, dass Text von einem KI-Sprachmodell generiert wurde
- Wenn Ihr Text zu "glatt" oder zu "perfekt" klingt
- Wenn Sie Wikipedia-Artikel oder ähnliche Dokumente überarbeiten möchten
- Wenn Sie eigene KI-generierte Outputs verfeinern möchten

## Benutzung

```
/humanizer [optional: Anweisungen für bestimmte Muster]
```

Oder direkt: "Humanisiere diesen Text" oder "Entferne KI-Muster aus diesem Abschnitt"

## Schritt 0: Modus bestimmen

| Modus | Beispiele | Stimme einbringen |
|---|---|---|
| **Locker** | Blogposts, Social Media, Newsletter | Voll – Rhythmus, Meinung, Persönlichkeit hinzufügen |
| **Sachlich** | Geschäftsberichte, Produktdokumentation, E-Mails | Moderat – KI-Tells entfernen, neutral bleiben |
| **Formal** | Wissenschaftliche Arbeiten, juristische Texte, Fachdokumentation | Minimal – nur Tells entfernen, Struktur erhalten |

Im Zweifel: **Sachlich** annehmen und die Annahme benennen.
"Stimme einbringen" gilt nur für den Modus **Locker**. Im Modus **Formal** schadet es aktiv.

## Aufgabe und Ablauf

Wenn Sie einen Text humanisieren, arbeiten Sie in dieser Reihenfolge:

1. **Modus bestimmen** (Locker / Sachlich / Formal). Annahme benennen, wenn unklar.
2. **HIGH-Muster scannen.** Alle korrigieren. (Muster 10: im Formal-Modus überspringen.)
3. **MEDIUM-Muster scannen.** Je nach Modus korrigieren.
4. **LOW-Muster scannen.** Korrigieren wenn klar vorhanden; im Formal-Modus überspringen.
5. **Stimme einbringen**, wenn Modus Locker.
6. **Nie Substanz kürzen.** Sachliche Aussagen und Informationsgehalt des Originals bleiben erhalten; Sätze umschreiben statt streichen. **Ausgenommen:** KI-Artefakte ohne Informationsgehalt, deren Lösung im jeweiligen Muster explizit „entfernen" oder „löschen" lautet (u. a. Muster 2, 3, 6, 17, 18, 19, 20, 21, 22, 24, 43). Diese Artefakte werden bereinigt, nicht umgeschrieben – das ist keine Substanzkürzung. Absatzanzahl und Informationsgehalt bleiben im substanztragenden Teil unverändert.
7. **NICHT ANFASSEN prüfen** – Verstöße rückgängig machen.
8. **Gedankenstrich-Scan**: Text nach gehäuften Gedankenstrichen (–, —, --) durchsuchen. Mehr als ein Gedankenstrich pro Absatz → ersetzen (siehe Muster 16, inkl. Ausnahme „Kein Problem, wenn"). Bei konsistenter Häufung über 3+ Absätze gilt die Leitplanke zu weichen Mustern: markieren statt automatisch umschreiben.
9. **Finaler Anti-KI-Pass**: "Was macht den Text noch offensichtlich KI-generiert?" Kurze, konkrete Tells benennen. Dann: "Jetzt so umschreiben, dass es nicht offensichtlich KI-generiert wirkt." Zweite Überarbeitung liefern.

## Stimmkalibrierung (optional)

Wenn der Benutzer eine Schreibprobe mitliefert (eigener Text), analysieren Sie diese vor dem Umschreiben:

1. **Probe zuerst lesen.** Notieren Sie:
   - Satzlängen-Muster (kurz und knapp? Lang und fließend? Gemischt?)
   - Wortwahl-Niveau (umgangssprachlich? Akademisch? Dazwischen?)
   - Wie Absätze beginnen (direkt rein? Erst Kontext setzen?)
   - Zeichensetzungs-Gewohnheiten (viele Gedankenstriche? Klammer-Einschübe? Semikolons?)
   - Wiederkehrende Formulierungen oder sprachliche Eigenheiten
   - Wie Übergänge funktionieren (explizite Konnektoren? Einfach nächster Punkt?)

2. **Stimme im Rewrite übernehmen.** Nicht nur KI-Muster entfernen – durch Muster aus der Probe ersetzen. Wenn der Autor kurze Sätze schreibt, keine langen produzieren. Wenn er "Zeug" und "Sachen" sagt, nicht zu "Elemente" und "Komponenten" upgraden.

3. **Ohne Probe** auf das Standardverhalten zurückfallen (natürliche, abwechslungsreiche Stimme aus dem Abschnitt "Persönlichkeit und Stimme").

### Probe bereitstellen
- Inline: "Humanisiere diesen Text. Hier ist eine Probe meines Schreibstils: [Probe]"
- Datei: "Humanisiere diesen Text. Verwende meinen Stil aus [Dateipfad] als Referenz."

## Kurzreferenz

| # | Muster | Schwere | Schlüssel-Indikatoren |
|---|--------|---------|-----------------------|
| 1 | Übermäßige Betonung von Symbolik | HIGH | "steht als Zeugnis", "spielt eine wichtige Rolle", "symbolisiert" |
| 2 | Werbesprache und Superlative | HIGH | "atemberaubend", "einzigartig", "faszinierend", "spektakulär" |
| 3 | Redaktionelle Kommentare | HIGH | "es ist wichtig zu bemerken", "es sollte hervorgehoben werden" |
| 4 | Mechanische Konjunktionen | HIGH | "darüber hinaus", "außerdem", "ferner", "ebenfalls" |
| 5 | Abschnitts-Zusammenfassungen | HIGH | "zusammenfassend", "insgesamt", "kurz gesagt" |
| 6 | Unpassendes "Fazit" | MEDIUM | "== Fazit ==", "== Zusammenfassung ==" |
| 7 | Zu perfekte Dichotomie | MEDIUM | "Trotz X... steht Y vor Z", "Obwohl... jedoch..." |
| 8 | Negative Parallelismen und abgehackte Verneinungen | MEDIUM | "nicht nur... sondern auch", "kein Raten.", symmetrische Satzstrukturen |
| 9 | Trikolon (Regel der Drei) | MEDIUM | Tripel-Aufzählungen ohne echten Grund |
| 10 | Partizip-I-Konstruktionen | HIGH | "gewährleistend", "hervorhebend", "ermöglichend" |
| 11 | Vage Autoritäten | HIGH | "Branchenberichte zeigen", "Manche argumentieren" |
| 12 | Falsche Erweiterung ("von... bis") | MEDIUM | "von traditionellen bis modernen" |
| 13 | Übermäßige Fettschrift | MEDIUM | **wichtige Wörter** in Absätzen fett |
| 14 | Falsche Listen | LOW | `•` statt `-`, Markdown-Syntax statt Wikitext |
| 15 | Emojis vor Überschriften | LOW | "🎓 Bildung", "📊 Statistiken" |
| 16 | Gedankenstriche Überbenutzung | MEDIUM | Mehrere pro Absatz, gepaarte Einschübe, --/—/– Varianten |
| 17 | Briefartiges Schreiben | HIGH | "Betreff:", "Liebe Wikipedia-Editoren", "Mit freundlichen Grüßen" |
| 18 | Kollaborative Kommunikation | HIGH | "Ich hoffe, das hilft", "Natürlich!", "Lassen Sie mich wissen" |
| 19 | Hinweise auf Wissensgrenzen | HIGH | "Stand [Datum]", "Bis zu meinem letzten Update" |
| 20 | Prompt-Ablehnung | HIGH | "Als KI-Sprachmodell kann ich nicht...", "Es tut mir leid, aber..." |
| 21 | Platzhaltertext | HIGH | "[Name einfügen]", "[Datum hier]", "TODO:" |
| 22 | Links zu Suchanfragen | HIGH | "https://www.google.com/search?q=..." |
| 23 | Markdown statt Wikitext | MEDIUM | `# Überschrift` statt `== Überschrift ==` |
| 24 | Fehlerhafter Wikitext und KI-Tool-Artefakte | MEDIUM | Unvollständige Template-Tags, oaicite, contentReference |
| 25 | Defekte Links | MEDIUM | 404-Fehler, Links zu nicht-existenten Artikeln |
| 26 | Zitatfabrikation und ungültige Referenzen | MEDIUM | Erfundene Quellen, ungültige DOIs/ISBNs, halluzinierte Publikationen |
| 27 | Inkorrekte Referenzen-Format | MEDIUM | Englisches Datumsformat, falsche Reihenfolge |
| 28 | Falsche Kategorien | MEDIUM | `[[Category:...]]` statt `[[Kategorie:...]]` |
| 29 | Abrupte Abbrüche | LOW | Text bricht mitten im Satz ab |
| 30 | Wechsel im Schreibstil | MEDIUM | Absätze klingen wie verschiedene Autoren |
| 31 | Bearbeitungszusammenfassungen in Ich-Form | LOW | "Ich habe einen Absatz über...", "Meine Änderungen..." |
| 32 | Persuasive Autoritäts-Floskeln | MEDIUM | "Die eigentliche Frage ist", "Im Kern", "In Wirklichkeit" |
| 33 | Signposting und Ankündigungen | MEDIUM | "Schauen wir uns an", "Hier ist, was Sie wissen müssen" |
| 34 | Fragmentierte Überschriften | LOW | Generischer Einzeiler nach Überschrift ("Geschwindigkeit zählt.") |
| 35 | Rhetorische Fragen als Fake-Engagement | MEDIUM | "Aber was bedeutet das?", "Haben Sie sich jemals gefragt?" |
| 36 | Universelle Menschheitserfahrungs-Eröffnung | MEDIUM | "Seit jeher", "Seit Anbeginn der Zivilisation", "Schon immer" |
| 37 | "In der heutigen X-Welt" Framing | MEDIUM | "In der heutigen digitalen Welt", "Im Zeitalter der..." |
| 38 | Aspirativer Unternehmensschluss | MEDIUM | "bestens aufgestellt", "die Möglichkeiten sind grenzenlos" |
| 39 | Passivkonstruktionen und subjektlose Fragmente | MEDIUM | "wurde durchgeführt", "es wird empfohlen", "Keine Konfiguration nötig." |
| 40 | Konditional-Stapel | MEDIUM | "Wenn das Argument stimmt, und wenn die Evidenz...", gehäufte "wenn"-Klauseln |
| 41 | Fehlkalibriertes epistemisches Vertrauen | MEDIUM | Über-Behauptung: "grundlegend", "entscheidend"; Über-Absicherung: "scheint möglicherweise" |
| 42 | Beleginkongruenz | HIGH | Quelle existiert, belegt aber die Aussage nicht |
| 43 | Versteckte Unicode-Zeichen | HIGH | Zero-Width-Space (U+200B), Soft-Hyphen, BOM, Bidi-Controls (U+202A–E, U+2066–9) |
| 44 | Standard-Kapitel ohne Substanz | MEDIUM | Standard-Überschrift + unbelegter Fülltext; nicht kürzen, sondern konkretisieren/integrieren |
| 45 | Anglizismus-Strukturen | MEDIUM | Harte Calques & False Friends: "am Ende des Tages", "eventuell" = "schließlich", "aktuell" = "tatsächlich" |

## Die 45 Muster

### Sprache und Tonfall (12 Muster)

#### 1. Übermäßige Betonung von Symbolik [HIGH]
**Problem:** Bestimmte Wendungen erzeugen symbolische, zu perfekte Bedeutungen.

Häufige Indikatoren:
- "steht als Zeugnis für"
- "ist ein Beweis für"
- "spielt eine wichtige Rolle bei"
- "steht für"
- "symbolisiert"

**Warum LLMs das tun:** Trainiert auf philosophischen Texten und Wikipedia-Artikeln mit erhöhtem abstraktem Diskurs.

**Beispiel:**

❌ Schlecht: "Die Kathedrale steht als Zeugnis für die künstlerische Brillanz des Mittelalters."

✓ Besser: "Die Kathedrale zeigt die Handwerkskunst des Mittelalters – und beeindruckt noch heute."

#### 2. Werbesprache und Superlative [HIGH]
**Problem:** Übertriebene Begeisterung, die mehr nach Marketing als nach neutraler Beschreibung klingt.

Häufige Indikatoren:
- "reiches kulturelles Erbe"
- "atemberaubend"
- "unbedingt besuchen"
- "spektakulär"
- "faszinierend"
- "einzigartig"

**Warum LLMs das tun:** Marketing-Texte sind im Trainingsmaterial überrepräsentiert.

**Beispiel:**

❌ Schlecht: "Die atemberaubende Altstadt mit ihrem reichen kulturellen Erbe zieht Besucher aus aller Welt an."

✓ Besser: "Die Altstadt zieht Besucher an. Ihre Geschichte reicht Jahrhunderte zurück."

#### 3. Redaktionelle Kommentare und Meta-Sprache [HIGH]
**Problem:** Der Text beschreibt sich selbst, statt direkten Inhalt zu vermitteln.

Häufige Indikatoren:
- "es ist wichtig zu bemerken"
- "es kann nicht ignoriert werden"
- "keine Diskussion wäre vollständig ohne"
- "es sollte hervorgehoben werden"
- "es ist erwähnenswert"

**Warum LLMs das tun:** Versucht, Gewichtung und Relevanz zu signalisieren, wo der Kontext unklar ist.

**Beispiel:**

❌ Schlecht: "Es ist wichtig zu bemerken, dass die Bevölkerung in diesem Zeitraum gewachsen ist."

✓ Besser: "Die Bevölkerung wuchs zwischen 1950 und 2000 um 30 Prozent."

#### 4. Mechanische Konjunktionen [HIGH]
**Problem:** Bestimmte Übergangswörter werden übermäßig mechanisch und klischeehaft eingesetzt.

Häufige Indikatoren:
- "darüber hinaus" (zu häufig)
- "außerdem"
- "ferner"
- "gleichzeitig"
- "ebenfalls"

**Warum LLMs das tun:** Diese Wörter sind strukturelle Marker im Training und werden übernutzt.

**Beispiel:**

❌ Schlecht: "Das Unternehmen wurde 1990 gegründet. Darüber hinaus beschäftigt es heute 500 Mitarbeiter. Darüber hinaus ist es in 15 Ländern tätig."

✓ Besser: "Das Unternehmen wurde 1990 gegründet und beschäftigt heute 500 Mitarbeiter in 15 Ländern."

#### 5. Abschnitts-Zusammenfassungen [HIGH]
**Problem:** Jeder Absatz wird automatisch zusammengefasst, statt natürlich zu fließen.

Häufige Indikatoren:
- "zusammenfassend"
- "abschließend"
- "insgesamt"
- "im Wesentlichen"
- "kurz gesagt"

**Warum LLMs das tun:** Versucht, Struktur zu schaffen, wo sie nicht nötig ist.

**Beispiel:**

❌ Schlecht: "Die Region hat drei Universitäten, ein Krankenhaus und eine Bibliothek. Insgesamt verfügt die Stadt über gute Infrastruktur."

✓ Besser: "Die Region hat drei Universitäten, ein Krankenhaus und eine Bibliothek – eine gute Grundversorgung."

#### 6. Unpassendes "Fazit" [MEDIUM]
**Problem:** Wikipedia-Artikel enden mit explizitem "Fazit", was unpassend ist.

Häufige Indikatoren:
- "== Fazit =="
- "== Zusammenfassung =="
- Explizite Conclusion-Sektion

**Warum LLMs das tun:** Akademische Schreibweise wird als Struktur imitiert.

**Lösung:** Entfernen oder in natürliche Übergänge umwandeln.

#### 7. Schlussfolgerungen mit zu starker Dichotomie [MEDIUM]
**Problem:** "Trotz X... steht Y vor Z" – zu perfekt gedachte Gegensätze.

Häufige Indikatoren:
- "Trotz seiner Erfolge steht das Unternehmen vor Herausforderungen"
- "Obwohl... jedoch..."
- "Während X... bleibt Y..."

**Warum LLMs das tun:** Binäre Argumentationsstruktur im Training.

**Beispiel:**

❌ Schlecht: "Trotz seiner technologischen Fortschritte steht das Land vor wirtschaftlichen Herausforderungen."

✓ Besser: "Das Land macht technologische Fortschritte, kämpft aber mit wirtschaftlichen Problemen."

#### 8. Negative Parallelismen und abgehackte Verneinungen [MEDIUM]
**Problem:** "Nicht nur... sondern auch" – zu argumentativ, zu literarisch. Dazu kommen abgehackte Verneinungsfragmente am Satzende wie "kein Raten", "kein Aufwand", die als Kurzform statt als echter Satz angehängt werden.

Häufige Indikatoren:
- "nicht nur... sondern auch"
- "weder... noch... sondern"
- Symmetrische Satzstrukturen
- Abgehackte Verneinungen am Satzende: "kein Raten.", "keine Kompromisse.", "kein Aufwand."

**Warum LLMs das tun:** Rhetorische Effekte aus literarischen Quellen. Die abgehackten Fragmente imitieren knappen Werbetext.

**Beispiel:**

❌ Schlecht: "Die Stadt ist nicht nur ein Handelszentrum, sondern auch ein Kulturzentrum."

✓ Besser: "Die Stadt ist Handels- und Kulturzentrum."

❌ Schlecht (abgehackte Verneinung): "Die Optionen kommen aus dem gewählten Element, kein Raten."

✓ Besser: "Die Optionen kommen aus dem gewählten Element, ohne dass der Nutzer raten muss."

#### 9. Trikolon und schematische Aufzählungen (Regel der Drei) [MEDIUM]
**Problem:** Übermäßige Nutzung der Regel-der-Drei als rhetorisches Mittel. Zusätzlich: auffällige Rundzahlen bei Listen (5, 7 oder 10 Punkte) als schematisches Muster.

Häufige Indikatoren:
- Drei parallele Sätze/Phrasen hintereinander
- "X, Y und Z waren alle charakteristisch für..."
- Tripel-Aufzählungen ohne echten Grund
- Listen mit verdächtig runder Länge (genau 5, 7 oder 10 Punkte), wenn die Sache selbst keine solche Struktur verlangt

**Warum LLMs das tun:** Trikolon ist ein starkes rhetorisches Muster in der Schreibweise. Runde Listenlängen entstehen durch Trainingsdaten, in denen „Top 5/7/10"-Artikel häufig vorkommen.

**Beispiel:**

❌ Schlecht: "Die Wirtschaft war vielfältig, kreativ und widerstandsfähig."

✓ Besser: "Die Wirtschaft war kreativ und widerstandsfähig."

#### 10. Oberflächliche Analysen mit Partizip I [HIGH]
**Problem:** Zu viele "-end" Partizipien, die Aktion beschreiben ohne echte Tiefe.

Häufige Indikatoren:
- "gewährleistend"
- "hervorhebend"
- "zeigend"
- "darstellend"
- "ermöglichend"

**Warum LLMs das tun:** Diese Konstruktionen sind grammatikalisch korrekt, erzeugen aber einen oberflächlichen, technischen Ton.

**Formal-Modus-Ausnahme:** In wissenschaftlichen Texten sind Partizip-I-Konstruktionen stilistisch akzeptiert. In diesem Modus überspringen.

**Beispiel:**

❌ Schlecht: "Die Technologie ermöglicht, dass Unternehmen ihre Effizienz steigern, ihre Kosten senken und ihre Konkurrenzfähigkeit verbessern."

✓ Besser: "Die Technologie hilft Unternehmen effizienter zu werden, Kosten zu senken und konkurrenzfähig zu bleiben."

#### 11. Vage Autoritäten [HIGH]
**Problem:** Unspezifische Quellen, die keinen echten Beweis liefern.

Häufige Indikatoren:
- "Branchenberichte zeigen"
- "Beobachter haben zitiert"
- "Es wird gesagt"
- "Manche argumentieren"
- "Mehrere Studien deuten darauf hin" (ohne Quelle)

**Warum LLMs das tun:** Kann keine echten Quellen zitieren, also erfindet es Platzhalter.

**Abgrenzung:** Muster 11 = keine konkrete Quelle genannt. Muster 26 = Quelle fabriziert (existiert nicht). Muster 42 = Quelle existiert, belegt aber die Aussage nicht.

Keine Quelle erfinden. Entweder: echte Quelle einfügen wenn bekannt, Zuschreibung entfernen, oder mit [ECHTE QUELLE NÖTIG] markieren.

**Beispiel:**

❌ Schlecht: "Branchenberichte zeigen, dass der Markt wächst."

✓ Besser: "Der Markt wächst (laut Wirtschaftsministerium 2024)." oder "Der Markt wächst – ein Trend, der seit 2020 beobachtet wird."

#### 12. Falsche Erweiterung ("von... bis") [MEDIUM]
**Problem:** "Von X bis Y" figurativ verwendet, wo es nicht passt.

Häufige Indikatoren:
- "von traditionellen bis modernen"
- "von klein bis groß"
- "von arm bis reich"
- Übertragene Verwendung von Bereichsbeschreibungen

**Warum LLMs das tun:** Stylistische Marker aus Fachtext-Training.

**Beispiel:**

❌ Schlecht: "Die Stadt zieht Menschen von verschiedensten bis progressivsten Überzeugungen an."

✓ Besser: "Die Stadt zieht Menschen mit sehr unterschiedlichen Überzeugungen an."

### Stil (4 Muster)

#### 13. Übermäßige Fettschrift [MEDIUM]
**Problem:** Bold wird für Emphasis statt für echte Struktur verwendet.

Häufige Indikatoren:
- **wichtige Wörter** in Absätzen fett
- Mehrere fettgedruckte Wörter pro Absatz
- Bold für Hervorhebung statt für Struktur

**Warum LLMs das tun:** Versucht, Wichtigkeit zu signalisieren, wo Klarheit hilft.

**Lösung:** Entfernen oder in Überschriften umwandeln.

#### 14. Falsche Listen [LOW]
**Problem:** Bullet-Punkte in nicht-Wikitext-Format in Wikipedia-Artikel.

Häufige Indikatoren:
- `•` statt `-` oder `*`
- `–` statt `*` für Aufzählungen
- Markdown-Syntax statt Wikitext

**Warum LLMs das tun:** Trainiert auf Markdown und Office-Formaten.

**Lösung:** In korrektes Wikitext-Format konvertieren.

#### 15. Emojis vor Überschriften [LOW]
**Problem:** Emojis werden verwendet, um visuelle Struktur zu schaffen.

Häufige Indikatoren:
- "🎓 Bildung"
- "📊 Statistiken"
- "🌍 Globaler Kontext"

**Warum LLMs das tun:** Modern wirken, aber nicht für Wikipedia.

**Lösung:** Entfernen.

#### 16. Gedankenstriche Überbenutzung [MEDIUM]
**Problem:** Gedankenstriche (–, —, --) werden von LLMs als Stilmittel übermäßig eingesetzt. Ein einzelner Gedankenstrich pro Absatz kann legitim sein; mehrere pro Absatz sind ein starker KI-Tell.

Häufige Indikatoren:
- "Das Projekt – durchgeführt von..." (statt Komma)
- Mehrere Gedankenstriche pro Absatz
- Als Satzzeichen statt Klammer verwendet
- Gepaarte Einschübe: "Der Bericht – der drei Kontinente abdeckte – kam zum Schluss..."
- Spaced Em-Dashes: "Die Politik — ohne Vorwarnung angekündigt — betrifft..."
- Doppelstriche als Ersatz: "Die Änderungen -- laut Kritikern überfällig -- treten sofort in Kraft."

**Warum LLMs das tun:** Englische Schreibweise wird imitiert. Gepaarte Einschübe sehen eingeschoben aus, nicht geschrieben.

**Ersetzungshierarchie** (in Prioritätsreihenfolge):
1. **Punkt** (80% der Fälle – zwei Sätze statt eines mit Strich)
2. **Komma**
3. **Doppelpunkt**
4. **Semikolon**
5. **Klammer**
6. **Satz umschreiben**

**Beispiel:**

❌ Schlecht: "Die neue Regelung – ohne Vorwarnung angekündigt – betrifft Tausende. Die Änderungen – laut Kritikern überfällig – treten sofort in Kraft."

✓ Besser: "Die neue Regelung wurde ohne Vorwarnung angekündigt und betrifft Tausende. Die Änderungen treten sofort in Kraft, was Kritiker für überfällig halten."

**Kein Problem, wenn:** Ein einzelner Gedankenstrich pro Absatz als bewusstes Stilmittel dient und sich nicht wiederholt.

### Kommunikation (6 Muster)

#### 17. Briefartiges Schreiben [HIGH]
**Problem:** Artikel sind als Briefe strukturiert, nicht als Inhalte.

Häufige Indikatoren:
- "Betreff: ..."
- "Liebe Wikipedia-Editoren"
- "Vielen Dank für..."
- "Mit freundlichen Grüßen"

**Warum LLMs das tun:** ChatBot-Verhalten, nicht Enzyklopädie-Verhalten.

**Lösung:** Vollständig entfernen oder umschreiben.

#### 18. Kollaborative Kommunikation [HIGH]
**Problem:** Der Text spricht den Leser direkt an, statt Fakten bereitzustellen.

Häufige Indikatoren:
- "Ich hoffe, das hilft"
- "Natürlich!"
- "Lassen Sie mich wissen"
- "Bitte fragen Sie, wenn..."
- "Wie Sie sehen können..."
- "Ich helfe Ihnen gerne"
- "Selbstverständlich!"

Vollständig löschen. Beim eigentlichen Inhalt anfangen.

**Warum LLMs das tun:** Trainiert, höflich und engagiert zu sein.

**Beispiel:**

❌ Schlecht: "Wie Sie sehen können, war die Produktivität beeindruckend. Lassen Sie mich wissen, wenn Sie weitere Fragen haben!"

✓ Besser: "Die Produktivität war in dieser Zeit bemerkenswert."

#### 19. Hinweise auf Wissensgrenzen [HIGH]
**Problem:** Der Text offenbart seine KI-Natur durch Datums-Hinweise.

Häufige Indikatoren:
- "Stand [Datum]"
- "Bis zu meinem letzten Update"
- "Nach meinem Wissen"
- "[Aktualisierung erforderlich]"

**Warum LLMs das tun:** Versucht, Ehrlichkeit zu zeigen.

**Lösung:** Entfernen oder in neutrale Quellen umwandeln.

#### 20. Prompt-Ablehnung [HIGH]
**Problem:** Der Text lehnt Anfragen ab wie ein Chatbot.

Häufige Indikatoren:
- "Als KI-Sprachmodell kann ich nicht..."
- "Es tut mir leid, aber..."
- "Ich kann keine aktuelle Information bereitstellen..."
- "Das liegt außerhalb meiner Fähigkeiten"

**Warum LLMs das tun:** Sicherheitsrichtlinien und Höflichkeit.

**Lösung:** Entfernen vollständig.

#### 21. Platzhaltertext [HIGH]
**Problem:** Template-Platzhalter wurden nicht gefüllt.

Häufige Indikatoren:
- "[Name einfügen]"
- "[Datum hier]"
- "[Quelle erforderlich]" (in Artikel statt Meta)
- "TODO:"
- "[Bearbeiter Name]"

**Warum LLMs das tun:** Kann keine echten Werte generieren, hinterlässt Platzhalter.

**Lösung:** Entfernen. Füllen nur, wenn der tatsächliche Wert aus dem übergebenen Kontext sicher ableitbar ist; externe Recherche liegt außerhalb des Skill-Umfangs. Im Zweifel entfernen.

#### 22. Links zu Suchanfragen statt Referenzen [HIGH]
**Problem:** URLs sind Google-Suchanfragen statt echte Referenzen.

Häufige Indikatoren:
- "https://www.google.com/search?q=..."
- "https://duckduckgo.com/?q=..."
- Suchanfragen in Fußnoten

**Warum LLMs das tun:** Kann keine echte URL recherchieren.

**Lösung:** Entfernen. Ersetzen nur, wenn eine echte, im Kontext vorhandene Quelle verfügbar ist; eigene Web-Recherche liegt außerhalb des Skill-Umfangs. Eine Quelle zu erfinden ist verboten (siehe Leitplanken).

### Auszeichnungstext (6 Muster)

#### 23. Markdown statt Wikitext [MEDIUM]
**Problem:** Markdown-Syntax in Wikipedia-Artikel statt Wikitext.

Häufige Indikatoren:
- `*fett*` oder `**fett**` statt `'''fett'''`
- `# Überschrift` statt `== Überschrift ==`
- `[Link](url)` statt `[Link url]`

**Warum LLMs das tun:** Trainiert auf Markdown-Quellen.

**Lösung:** Konvertieren zu Wikitext.

#### 24. Fehlerhafter Wikitext und KI-Tool-Artefakte [MEDIUM]
**Problem:** Wikitext-Syntax ist ungültig oder unvollständig. Zusätzlich hinterlassen KI-Tools technische Artefakte im Text.

Häufige Indikatoren:
- "gehe zu [[Suche Nr. 42]]"
- Unvollständige Template-Tags
- `{{cite book|author=` ohne Schließ-`}}`
- `oaicite:0` oder `oaicite:ref` Tags (ChatGPT-Artefakt)
- `contentReference[oaicite:0]` Spans
- `turn0search0` Referenzen (Copilot-Artefakt)
- Markdown-Formatierung in Word- oder PDF-Dokumenten

**Warum LLMs das tun:** Wikitext-Syntax wurde nicht korrekt generiert. KI-Tools fügen interne Referenz-Tags ein, die im Export nicht bereinigt werden.

**Lösung:** Reparieren oder entfernen. KI-Tool-Artefakte immer vollständig löschen.

#### 25. Defekte Links [MEDIUM]
**Problem:** Zu viele rote Links oder tote Referenzen.

Häufige Indikatoren:
- 404 Fehler in Referenzen
- Links zu nicht-existenten Artikeln
- Tippfehler in Kategorien oder Artikeln

**Warum LLMs das tun:** Halluziniert Artikel-Titel.

**Lösung:** Prüfen und korrigieren oder entfernen.

#### 26. Zitatfabrikation und ungültige Referenzen [MEDIUM]
**Problem:** LLMs erfinden Quellen, die echt aussehen, aber nicht existieren. Das reicht von ungültigen DOI-Prüfziffern bis zu komplett halluzinierten Publikationen.

Häufige Indikatoren:
- DOI mit ungültiger Prüfziffer
- ISBN mit Tippfehler
- Erfundene akademische Quellen (Journal existiert nicht, Ausgabe existiert nicht)
- Autoren existieren, aber die genannte Publikation nicht
- Defekte externe Links mit `utm_source=`-Parametern – besonders verdächtig: `utm_source=chatgpt.com`, `utm_source=claude.ai`, `utm_source=gemini.google.com`, `utm_source=perplexity.ai` (direkter KI-Fingerabdruck)
- Unbenutzte benannte Referenzen (`<ref name="..."/>` ohne zugehörige Definition)

**Warum LLMs das tun:** Kann keine echten Quellen recherchieren und erzeugt plausibel aussehende Referenzen aus dem Training.

**Lösung:** Formale Plausibilität jeder Quelle mit den verfügbaren Mitteln prüfen (Format, interne Konsistenz, DOI-/ISBN-Prüfziffer, `utm_source`-Fingerabdrücke, existierende Autoren-Publikation-Kombinationen im übergebenen Kontext). Externe Online-Verifikation liegt außerhalb des Skill-Umfangs – in diesem Fall mit [QUELLE NICHT VERIFIZIERT] markieren. Bei nachweisbarer Fabrikation: entfernen. Nie eine Quelle erfinden oder stehen lassen, die als erfunden erkannt wurde.

#### 27. Inkorrekte Referenzen-Format [MEDIUM]
**Problem:** Zitierformat entspricht nicht deutschen Wikipedia-Standards.

Häufige Indikatoren:
- Englisches Datumsformat statt deutsches
- Falsche Reihenfolge (Nachname, Vorname)
- Incompatible Zitierstyle

**Warum LLMs das tun:** Englisches Training dominiert.

**Lösung:** Anpassung an deutsches Format (z.B. `1. Januar 2024` statt `January 1, 2024`).

#### 28. Falsche Kategorien [MEDIUM]
**Problem:** Kategorien sind nicht-existent oder nicht-deutsch.

Häufige Indikatoren:
- `[[Category:American Writers]]` statt `[[Kategorie:Amerikanische Schriftsteller]]`
- Erfundene Kategorien
- Rote Kategorie-Links

**Warum LLMs das tun:** Trainiert auf englischen Wikipedia-Kategorien.

**Lösung:** Zu korrekten deutschen Kategorien korrigieren.

### Verschiedenes (3 Muster)

#### 29. Abrupte Abbrüche [LOW]
**Problem:** Text bricht mitten im Satz ab.

Häufige Indikatoren:
- "Die Gründung der Stadt war..."
- Unvollständige Sätze
- Trailing text ohne Sinn

**Warum LLMs das tun:** Token-Limit erreicht oder Ausgabe wurde unterbrochen.

**Lösung:** Löschen oder vervollständigen mit echten Informationen.

#### 30. Wechsel im Schreibstil [MEDIUM]
**Problem:** Plötzlicher Wechsel von informell zu formell oder umgekehrt.

Häufige Indikatoren:
- Absätze klingen wie verschiedene Autoren
- Abrupt wechselnde Tonalität
- Mix aus akademisch und umgangssprachlich

**Warum LLMs das tun:** Verschiedene Trainingsdaten-Quellen.

**Lösung:** Harmonisieren zum konsistenten Stil.

#### 31. Ausführliche Bearbeitungszusammenfassungen in Ich-Form [LOW]
**Problem:** Edit-Summaries sind verbose und persönlich.

Häufige Indikatoren:
- "Ich habe einen Absatz über..."
- "Meine Änderungen verbessern..."
- "Ich denke, dass..."

**Warum LLMs das tun:** Chatbot-Verhalten auch in Metadaten.

**Lösung:** Entfernen oder in neutrale Form umwandeln ("Absatz über X hinzugefügt").

### Rhetorik und Struktur (7 Muster)

#### 32. Persuasive Autoritäts-Floskeln [MEDIUM]

**Wendungen, auf die Sie achten sollten:** "Die eigentliche Frage ist", "Im Kern", "In Wirklichkeit", "Was wirklich zählt", "Im Grunde genommen", "Das tiefere Problem", "Worauf es wirklich ankommt", "Der Kern der Sache", "Letztlich geht es um"

**Problem:** LLMs verwenden diese Wendungen, um gewöhnliche Aussagen als verborgene Erkenntnisse zu verpacken. Die "Wahrheit", die folgt, ist meist eine Wiederholung des bereits Gesagten. Anders als Muster 1 (Symbolik-Inflation, die die Bedeutung von Fakten aufbläht) und Muster 3 (Redaktionelle Kommentare, die Sätze aufpolstern), erzeugt dieses Muster gezielt den Eindruck, durch Lärm zu einer tieferen Einsicht vorzudringen, die nicht existiert.

**Kein Problem, wenn:** Der Autor einen echten rhetorischen Schwenk in einem Meinungsartikel oder Essay macht, wo Neuformulierung der Punkt ist und die folgende Aussage sich inhaltlich vom Vorherigen unterscheidet.

**Beispiel:**

❌ Schlecht: "Die eigentliche Frage ist, ob Teams sich anpassen können. Im Kern geht es um organisatorische Bereitschaft. In Wirklichkeit kommt es auf die Integration in bestehende Arbeitsabläufe an."

✓ Besser: "Ob Teams sich anpassen können, hängt vor allem von der organisatorischen Bereitschaft ab und davon, wie bereitwillig sie bestehende Arbeitsabläufe ändern."

#### 33. Signposting und Ankündigungen [MEDIUM]

**Wendungen, auf die Sie achten sollten:** "Schauen wir uns an", "Lassen Sie uns erkunden", "Hier ist, was Sie wissen müssen", "Die Sache ist die", "Was als Nächstes passiert", "Ohne weitere Umschweife", "Jetzt werfen wir einen Blick auf", "Kommen wir zu", "Tauchen wir ein"

**Problem:** LLMs kündigen an, was sie gleich tun werden, statt es einfach zu tun. Diese Wendungen bremsen den Leser mit Meta-Kommentar zur Textstruktur. Sie stammen aus dem Chatbot-Dialog-Training, wo das Modell seine eigene Antwort kommentiert, bevor es Inhalt liefert. Unterscheidet sich von Muster 18 (Kollaborative Kommunikation), das Chatbot-Höflichkeitsfloskeln abdeckt; dieses Muster betrifft Meta-Struktur-Vorspanne, die Inhalt ankündigen ohne ihn zu liefern.

**Kein Problem, wenn:** Der Text ein Live-Präsentationsskript, Vorlesungstranskript oder interaktives Tutorial ist, wo direkte Ansprache des Publikums erwartet wird.

**Beispiel:**

❌ Schlecht: "Schauen wir uns an, wie Caching in Next.js funktioniert. Hier ist, was Sie wissen müssen. Lassen Sie uns das Schritt für Schritt durchgehen."

✓ Besser: "Next.js cached auf vier Ebenen: Request-Memoization, Data-Cache, Full-Route-Cache und Router-Cache auf dem Client."

#### 34. Fragmentierte Überschriften [LOW]

**Anzeichen:** Ein Ein-Satz- oder Ein-Fragment-Absatz direkt nach einer Überschrift, gefolgt vom eigentlichen Inhalt. Die verwaiste Zeile wiederholt typischerweise die Überschrift in anderen Worten oder macht eine generische Aussage ("Geschwindigkeit zählt.", "Sicherheit ist alles.", "Testen ist entscheidend.").

**Problem:** LLMs setzen einen kurzen, generischen Satz nach einer Überschrift als rhetorischen "Aufhänger" vor dem eigentlichen Absatz. Die verwaiste Zeile fügt keine Information hinzu, die die Überschrift nicht bereits signalisiert. Entfernen und die Überschrift ihre Arbeit machen lassen.

**Kein Problem, wenn:** Der kurze Einstieg spezifisch ist und Information enthält, die die Überschrift nicht hat (z.B. ein Datum, eine Zahl, eine benannte These). Bewusst stilistische Einstiege in Essays oder Reden können ebenfalls legitim sein.

**Beispiel:**

❌ Schlecht:
> ## Performance
>
> Geschwindigkeit zählt.
>
> Wenn Nutzer eine langsame Seite sehen, verlassen sie die Website. Eine Google-Studie von 2023 ergab, dass 53% der mobilen Nutzer Seiten verlassen, die länger als drei Sekunden laden.

✓ Besser:
> ## Performance
>
> Wenn Nutzer eine langsame Seite sehen, verlassen sie die Website. Eine Google-Studie von 2023 ergab, dass 53% der mobilen Nutzer Seiten verlassen, die länger als drei Sekunden laden.

#### 35. Rhetorische Fragen als Fake-Engagement [MEDIUM]

**Wendungen, auf die Sie achten sollten:** "Aber was bedeutet das für...?", "Haben Sie sich jemals gefragt, warum...?", "Doch was steckt dahinter?", "Was heißt das konkret?", "Wer profitiert davon?", "Warum ist das wichtig?"

**Problem:** LLMs streuen rhetorische Fragen ein, um Engagement vorzutäuschen. Die Frage wird sofort im nächsten Satz beantwortet – der Leser hatte nie eine echte Wahl, mitzudenken. Anders als Muster 33 (Signposting, das Inhalt ankündigt), simuliert dieses Muster einen Dialog, der keiner ist. Die Frage fügt nichts hinzu; sie verzögert nur die eigentliche Aussage.

**Kein Problem, wenn:** Der Text ein FAQ-Format hat, eine tatsächliche Frage-Antwort-Struktur verfolgt oder der Autor eine provokante These aufstellt, die er dann widerlegt.

**Beispiel:**

❌ Schlecht: "Aber was bedeutet das für den Mittelstand? Die Antwort ist einfacher als gedacht: Unternehmen müssen sich anpassen."

✓ Besser: "Der Mittelstand muss sich anpassen."

#### 36. Universelle Menschheitserfahrungs-Eröffnung [MEDIUM]

**Wendungen, auf die Sie achten sollten:** "Seit jeher", "Seit Anbeginn der Zivilisation", "Schon immer hat die Menschheit...", "Im Laufe der Geschichte", "Seit Menschengedenken", "Von Anfang an", "Schon die alten Griechen/Römer..."

**Problem:** LLMs eröffnen Texte mit grandiosen Menschheitsaussagen, um einem Alltagsthema historisches Gewicht zu verleihen. Ein Blogpost über Projektmanagement beginnt dann mit "Seit Anbeginn der Zivilisation haben Menschen nach Wegen gesucht, Arbeit zu organisieren." Die Eröffnung ist austauschbar, sagt nichts Konkretes und passt auf jedes Thema. Anders als Muster 1 (Symbolik-Inflation, das einzelne Fakten aufbläht), bläst dieses Muster den gesamten Einstieg auf.

**Kein Problem, wenn:** Der historische Bezug spezifisch ist (Datum, Name, Ort) und direkt zum Thema führt. Ein Geschichtsartikel darf so beginnen.

**Beispiel:**

❌ Schlecht: "Seit Anbeginn der Zivilisation suchen Menschen nach Wegen, effizienter zu kommunizieren. Im Zeitalter der Digitalisierung hat sich diese Suche grundlegend verändert."

✓ Besser: "E-Mail hat den Geschäftsbrief abgelöst. Slack hat die E-Mail nicht abgelöst – aber den Ton verändert."

#### 37. "In der heutigen X-Welt" Framing [MEDIUM]

**Wendungen, auf die Sie achten sollten:** "In der heutigen digitalen Welt", "In einer zunehmend vernetzten Welt", "In Zeiten von...", "Im Zeitalter der Digitalisierung", "In der heutigen schnelllebigen Gesellschaft", "In einer Welt, in der...", "Angesichts der rasanten Entwicklung"

**Problem:** LLMs rahmen gewöhnliche Themen mit Zeitgeist-Floskeln, die nichts aussagen. Jeder weiß, dass die Welt digital und vernetzt ist – das muss nicht in jedem Absatz stehen. Die Formulierung ist so generisch, dass sie auf jeden Artikel passt, und genau das macht sie zum KI-Tell. Anders als Muster 36 (Menschheits-Eröffnung, die in die Vergangenheit greift), greift dieses Muster in die Gegenwart, um Relevanz vorzutäuschen.

**Kein Problem, wenn:** Der Kontext tatsächlich einen historischen Vergleich erfordert ("Im Gegensatz zur analogen Verwaltung der 1990er-Jahre...") und spezifisch wird.

**Beispiel:**

❌ Schlecht: "In der heutigen digitalen Welt ist eine starke Online-Präsenz für Unternehmen unerlässlich."

✓ Besser: "Ohne Website findet ein Handwerksbetrieb heute kaum noch Kunden unter 40."

#### 38. Aspirativer Unternehmensschluss [MEDIUM]

**Wendungen, auf die Sie achten sollten:** "bestens aufgestellt für die Zukunft", "die Möglichkeiten sind grenzenlos", "bereit für die nächste Stufe", "an der Schwelle zu einer neuen Ära", "die Weichen sind gestellt", "mit Zuversicht in die Zukunft blicken", "das Potenzial ist enorm", "auf Erfolgskurs"

**Problem:** LLMs schließen Texte mit optimistischen Zukunftsaussagen, die nichts Konkretes sagen. Der Schluss klingt nach Pressemitteilung oder Geschäftsbericht-Phrasen. Anders als Muster 7 (Dichotomie-Schluss, der "Trotz X... steht Y vor Z" nutzt) und Muster 5 (Abschnitts-Zusammenfassung), erzeugt dieses Muster einen unverdienten Optimismus-Kick am Ende.

**Kein Problem, wenn:** Der Text tatsächlich ein Geschäftsbericht oder eine Pressemitteilung ist, wo solche Formulierungen Konvention sind.

**Beispiel:**

❌ Schlecht: "Mit dieser Strategie ist das Unternehmen bestens aufgestellt für die Zukunft. Die Möglichkeiten sind grenzenlos."

✓ Besser: "Ob die Strategie aufgeht, zeigt sich im nächsten Quartal."

### Argumentation und Evidenz (3 Muster)

#### 39. Passivkonstruktionen und subjektlose Fragmente [MEDIUM]

**Problem:** LLMs verstecken den Akteur durch Passiv oder lassen das Subjekt ganz weg. Fragmente wie "Keine Konfiguration nötig." oder "Wird automatisch gespeichert." verschleiern, wer handelt. Aktive Formulierungen machen den Satz klarer und direkter.

Häufige Indikatoren:
- "wurde durchgeführt" (statt "Team X führte durch")
- "es wird empfohlen" (statt "wir empfehlen")
- "Keine Konfiguration nötig."
- "Wird automatisch gespeichert."
- "Kann ohne Weiteres angepasst werden."

**Warum LLMs das tun:** Passiv erzeugt einen objektiven, formellen Ton, der auf den ersten Blick akademisch wirkt. Subjektlose Fragmente imitieren knappen Dokumentationsstil.

**Formal-Modus-Ausnahme:** In wissenschaftlichen Texten sind Passivkonstruktionen Konvention ("wurde analysiert", "es konnte gezeigt werden"). In diesem Modus nur bei klarer Übernutzung eingreifen.

**Beispiel:**

❌ Schlecht: "Keine Konfigurationsdatei nötig. Die Ergebnisse werden automatisch gespeichert."

✓ Besser: "Sie brauchen keine Konfigurationsdatei. Das System speichert die Ergebnisse automatisch."

#### 40. Konditional-Stapel [MEDIUM]

**Problem:** LLMs häufen "wenn"-Klauseln in Schlussfolgerungen, statt direkt auszusagen, was die Analyse ergeben hat. Eine einzelne Bedingung an einem echten Verzweigungspunkt ist normal; ein Cluster davon in einer Conclusion signalisiert, dass der Autor nicht hinter seiner eigenen Arbeit steht.

Häufige Indikatoren:
- "Wenn das Argument stimmt, und wenn die Evidenz diese Lesart stützt..."
- "Sofern der Kontext wie beschrieben war..."
- Mehrere "wenn/falls/sofern"-Klauseln in einem Absatz
- Hedging-Ketten in Schlussfolgerungen

**Warum LLMs das tun:** Versucht, Verantwortung für Aussagen zu vermeiden, indem jede Behauptung durch Bedingungen relativiert wird.

**Kein Problem, wenn:** Der Text tatsächlich unterschiedliche Szenarien analysiert, bei denen die Bedingungen echte Verzweigungen darstellen.

**Beispiel:**

❌ Schlecht: "Wenn das Argument stimmt, und wenn die Evidenz diese Lesart stützt, dann könnte die Politik einen gewissen Effekt gehabt haben – sofern der Kontext wie beschrieben war."

✓ Besser: "Die Evidenz stützt das Argument, dass die Politik in diesem Kontext einen Effekt hatte."

#### 41. Fehlkalibriertes epistemisches Vertrauen [MEDIUM]

**Problem:** LLMs schwanken zwischen zwei Extremen: Über-Behauptung (Aussagen mit "grundlegend", "entscheidend", "zweifellos" aufladen) und Über-Absicherung (alles mit "scheint möglicherweise", "könnte eventuell" relativieren). Beide Extreme sind KI-Tells. Die Lösung ist nicht, Behauptungen durch Hedges zu ersetzen, sondern den Anspruch zu verengen.

Häufige Indikatoren:
- Über-Behauptung: "grundlegend verändert", "entscheidend geprägt", "zweifellos", "vollständig revolutioniert"
- Über-Absicherung: "scheint möglicherweise", "könnte eventuell", "dürfte unter Umständen"
- Beides im selben Text (starke Behauptungen in einem Absatz, maximales Hedging im nächsten)

**Warum LLMs das tun:** Über-Behauptung kommt aus dem Training auf persuasive Texte. Über-Absicherung aus RLHF und Sicherheitstraining, das Vorsicht belohnt.

**Kein Problem, wenn:** Der Autor bewusst eine starke These aufstellt (Essay, Meinungsartikel) oder echte Unsicherheit benennt ("Die Daten lassen keine eindeutige Schlussfolgerung zu").

**Beispiel:**

❌ Schlecht (Über-Behauptung): "Die Daten zeigen zweifellos, dass Remote-Arbeit die Produktivität grundlegend verändert hat."

✓ Besser: "In den untersuchten Unternehmen stieg die Produktivität im ersten Jahr der Remote-Arbeit um durchschnittlich 8 Prozent."

❌ Schlecht (Über-Absicherung): "Es scheint, dass die Politik möglicherweise einen gewissen Effekt auf die Ergebnisse gehabt haben könnte."

✓ Besser: "Die Politik führte in zwei von drei untersuchten Fällen zu einer moderaten Verbesserung."

### Ergänzungen (4 Muster)

Diese Muster sind in Version 3.2 neu aufgenommen und konzeptuell den bestehenden Kategorien zugeordnet.

#### 42. Beleginkongruenz [HIGH]

**Kategorie:** Argumentation und Evidenz

**Problem:** Die angegebene Quelle existiert und ist formal korrekt zitiert, belegt aber die getroffene Aussage nicht. Anders als Muster 26 (fabrizierte Quellen) ist die Referenz real – nur der Inhalt passt nicht zur Behauptung.

Häufige Indikatoren:
- Die Quelle behandelt das Thema nur am Rand, wird aber als zentraler Beleg präsentiert
- Widerspruch zwischen Aussage und Quelle (Quelle sagt das Gegenteil oder differenziert stärker)
- Scope-Mismatch: Zeitraum, Region oder Population der Quelle passt nicht zur Behauptung (z. B. US-Studie als Beleg für deutsche Verhältnisse, Studie von 2015 für Aussage über 2024)
- Jahreszahlen in der Aussage weichen von denen der Quelle ab
- Konkrete Zahlen werden zitiert, die so in der Quelle nicht stehen
- Seitenzahl verweist auf Inhalte, die nichts mit der Aussage zu tun haben
- Sekundärquelle (Blog, Zeitungsartikel) wird als Primärbeleg für eine Forschungsaussage präsentiert
- Eine allgemeine Übersichtsquelle wird für eine sehr spezifische Aussage herangezogen

**Warum LLMs das tun:** Abrufbare Quellen aus dem Training werden thematisch passend zugeordnet, ohne dass der konkrete Inhalt gegen die Aussage geprüft werden kann.

**Operative Schranke:** Nur dann als Beleginkongruenz markieren, wenn die Quelle tatsächlich geprüft wurde oder eindeutig prüfbar ist (Link funktioniert, Seite nennbar, Volltext zugänglich). Ohne Prüfmöglichkeit keine Kongruenz-Vorwürfe erheben – sonst droht Halluzination in die andere Richtung.

**Lösung:** Quellennachweis gegen die konkrete Aussage prüfen, sofern möglich. Bei nachweisbarer Inkongruenz entweder Aussage an Quelle anpassen, Quelle ersetzen oder mit `[BELEG PRÜFEN]` markieren. Bei nicht prüfbarer Quelle keine Kongruenz-Diagnose erheben. Fabrikationsindikatoren (erfundene DOI/ISBN, nicht existierendes Journal) fallen unter Muster 26.

**Beispiel:**

❌ Schlecht: „Laut einer Studie des Fraunhofer-Instituts aus 2019 stieg die Produktivität deutscher Remote-Teams um 23 Prozent.<ref>Fraunhofer IAO: Arbeiten in der Corona-Pandemie, 2020.</ref>"
(Quelle existiert, stammt aber aus 2020 und nennt keine 23 Prozent.)

✓ Besser: Quelle auf tatsächlichen Inhalt prüfen, Aussage an die Quelle anpassen oder passende Quelle suchen.

#### 43. Versteckte Unicode-Zeichen [HIGH]

**Kategorie:** Auszeichnungstext

**Problem:** KI-Tools hinterlassen unsichtbare Unicode-Zeichen im Text. Diese sind für das Auge nicht wahrnehmbar, stören aber Wiki-Syntax, Volltextsuche, Screenreader und Textvergleich. Ergänzt Muster 24 um die unsichtbare Ebene. Nur echte Hidden Characters – sichtbare Typografie (Anführungszeichen, Apostrophe) gehört nicht hierher.

Häufige Indikatoren:
- Zero-Width Space (U+200B)
- Zero-Width Non-Joiner (U+200C)
- Zero-Width Joiner (U+200D)
- Word Joiner (U+2060)
- Byte Order Mark (U+FEFF) mitten im Text
- Soft-Hyphen (U+00AD) an ungewöhnlichen Stellen
- Bidi-Steuerzeichen: U+202A–U+202E (Left/Right-to-Left Embedding/Override/Pop), U+2066–U+2069 (Isolates)

**Warum LLMs das tun:** Modelle produzieren gelegentlich Tokens mit unsichtbaren Sonderzeichen. Copy-Paste aus KI-Oberflächen schleppt zusätzliche Formatierungsartefakte mit. Bidi-Controls können auch gezielt zur Verschleierung von Prompt-Inhalten genutzt werden.

**Lösung:** Regex-Scan auf `[\u200B-\u200D\u2060\uFEFF\u00AD\u202A-\u202E\u2066-\u2069]` und ersatzlos entfernen. Nicht verwechseln mit legitimen Unicode-Gebrauchsfällen: U+00A0 (geschütztes Leerzeichen) in stehenden Wendungen wie „5 km" oder „§ 12" ist korrekt und gehört nicht in dieses Muster.

#### 44. Standard-Kapitel ohne Substanz [MEDIUM]

**Kategorie:** Stil

**Problem:** Das Problem ist **nicht** die Überschrift an sich, sondern der generische, unbelegte Fülltext darunter. Überschriften wie „Bedeutung" oder „Relevanz" können in enzyklopädischen Texten legitim sein, wenn der Abschnitt konkrete Belege enthält. Tell ist die Kombination aus Standard-Überschrift + substanzloser Allgemeinplätze.

**Abgrenzung:**
- Muster 5 (Zusammenfassungen): Sprachmarker „zusammenfassend" im Fließtext
- Muster 6 (Fazit): spezifisch die Überschrift „Fazit"/„Zusammenfassung"
- Muster 34 (Fragmentierte Überschriften): Einzeiler direkt nach Überschrift
- Muster 44: ganzer Abschnitt unter Standard-Überschrift ohne konkrete Information

Häufige Indikatoren:
- Überschriften: „== Herausforderungen ==", „== Zukunftsperspektiven ==", „== Bedeutung ==", „== Relevanz ==", „== Ausblick ==", „== Chancen und Risiken =="
- Darunter: allgemeine Aussagen ohne konkrete Fakten, Zahlen oder Belege
- Prognose-Sprech ohne Träger („Experten erwarten", „es ist zu erwarten")
- Bloße Wiederholung von Punkten aus früheren Abschnitten unter neuer Überschrift

**Warum LLMs das tun:** Nachahmung formaler akademischer und journalistischer Strukturen. Standard-Kapitel füllen Platz, wo keine konkrete Information verfügbar ist.

**Lösung:** Nicht kürzen (Leitplanke „Nie kürzen" gilt). Vorgehen in dieser Reihenfolge:
1. **Substanz finden:** Prüfen, ob unter der Überschrift tatsächlich eine Aussage steckt, die bloß verwässert formuliert ist. Wenn ja: konkretisieren, Belege einfügen.
2. **Integrieren:** Falls der Abschnitt nur thematisch Bekanntes wiederholt, Inhalt in bestehende thematische Kapitel verschieben und die Standard-Überschrift entfernen. Der Text selbst bleibt im Artikel erhalten.
3. **Umwidmen:** Generische Überschrift durch spezifische ersetzen („Zukunftsperspektiven" → „Marktprognosen 2025–2030"), wenn der Inhalt das trägt.
4. **Fallback bei echter Substanzlosigkeit:** Wenn weder konkrete Aussage noch tragbare Paraphrase noch thematische Zuordnung möglich ist, Abschnitt mit `[SUBSTANZ PRÜFEN]` markieren und wörtlich stehen lassen. Streichung oder Inhaltsergänzung liegt dann beim menschlichen Redigat, nicht beim Skill-Durchlauf. So bleibt die „Nie kürzen"-Leitplanke gewahrt, ohne Inhalt zu erfinden.

**Beispiel:**

❌ Schlecht:
> == Zukunftsperspektiven ==
>
> Die Zukunft der Technologie ist vielversprechend. Experten erwarten weitere Fortschritte und neue Einsatzmöglichkeiten. Unternehmen sollten sich frühzeitig auf die Veränderungen einstellen.

✓ Besser (umgewidmet + konkretisiert):
> == Marktprognosen ==
>
> Der VDMA erwartet bis 2030 ein jährliches Marktwachstum von 12 Prozent.<ref>VDMA Branchenbericht 2024, S. 42.</ref> Treiber sind vor allem der Ausbau industrieller Anwendungen.

#### 45. Anglizismus-Strukturen [MEDIUM]

**Kategorie:** Sprache und Tonfall

**Problem:** KI überträgt englische Satzmuster, Kollokationen und Bedeutungen wörtlich ins Deutsche. Das Muster zielt nur auf **harte Transfers**: Calques (Lehnübersetzungen), False Friends (Falschfreunde) und syntaktische Muster, die im Deutschen als Übersetzungsdeutsch auffallen. Einzelne Anglizismen in Business- oder Umgangssprache sind **kein** Anzeichen.

Harte Indikatoren (klare Tells):
- **Calques:** „am Ende des Tages" (at the end of the day), „in Reihenfolge zu" (in order to), „zu Beginn mit" (to begin with), „das macht keinen Unterschied für mich" (that makes no difference to me)
- **False Friends:** „eventuell" als „schließlich" (eventually, korrekt: „schließlich"/„am Ende"), „aktuell" als „tatsächlich" (actually, korrekt: „tatsächlich"/„eigentlich"), „sensibel" als „vernünftig/umsichtig" (sensible, korrekt: „vernünftig"/„besonnen")
- **Syntaktische Transfers:** englische Wortstellung in Relativsätzen („das Unternehmen, welches gegründet wurde in 1990"), nachgestellte Präpositionalphrasen nach englischem Muster („das Buch über Berlin von Peter Schneider geschrieben")

**Kein belastbarer Tell (weglassen):**
- „basiert auf", „in Bezug auf", „adressieren" – in Geschäfts- und Wissenschaftsdeutsch etabliert
- „Sinn machen" – im heutigen Standarddeutsch etabliert; stilistische Präferenz, kein KI-Tell
- „realisieren" im Sinne von „erkennen/begreifen" – lexikalisch etabliert (Duden, DWDS)
- „kontrollieren" als „beherrschen" – Bedeutungen überlappen im Deutschen bereits
- Unnötige Possessivpronomen – allgemeines Übersetzungsdeutsch, Stilglättung
- Einzelne Lehnwörter („Meeting", „Team", „Feedback") – im Zielregister oft normal

**Register-Hinweis:**
- **False Friends** (eventuell/aktuell/sensibel in falscher Bedeutung) sind semantische Fehler – immer korrigieren, unabhängig vom Register.
- **Calques und syntaktische Transfers** sind registerabhängig. In Blogposts, Social-Media-Texten und Business-Dokumentation können sie etabliert sein; dort nur eingreifen, wenn sie gehäuft auftreten oder das Zielregister formal ist.

**Warum LLMs das tun:** Englisches Trainingsmaterial dominiert. Deutsche Ausgaben folgen englischen Strukturen, besonders bei direkter Übersetzung aus englischen Quellen.

**Lösung:** Durch deutsches Äquivalent ersetzen. Prüffrage: Würde ein Muttersprachler ohne englische Vorlage so formulieren?

**Beispiel:**

❌ Schlecht: „Am Ende des Tages erkannte das Team eventuell, dass die Strategie aktuell nicht trug."
(eventuell = eventually = „schließlich"; aktuell = actually = „tatsächlich")

✓ Besser: „Schließlich erkannte das Team, dass die Strategie tatsächlich nicht trug."

## Quick Checklist (Vor-Ausgabe-Audit)

Vor der Ausgabe schnell prüfen:

- [ ] Drei aufeinanderfolgende Sätze gleiche Länge, ohne dass eine Stimmprobe diesen Rhythmus vorgibt? → Einen aufbrechen
- [ ] Generischer, inhaltsloser Einzeiler direkt nach einer Überschrift? → Entfernen oder integrieren (Muster 34). Bewusste Punchlines am Absatzende sind davon ausgenommen.
- [ ] Gedankenstrich vor einer „Enthüllung" als wiederkehrendes Muster (mehrfach im Text oder mehr als einer pro Absatz)? → Ersetzen (Muster 16). Ein einzelner, bewusst gesetzter Gedankenstrich ist zulässig.
- [ ] Metapher wird unmittelbar danach redundant erklärt? → Redundanz auflösen, Substanz erhalten
- [ ] "Darüber hinaus" / "Jedoch" / "Ferner" mechanisch? → Streichen oder umformulieren (Muster 4)
- [ ] Regel der Drei ohne sachlichen Grund? → Auf 2 oder 4 ändern (Muster 9)
- [ ] Passiv wo Aktiv möglich wäre (außer im Formal-Modus, dort nur bei klarer Übernutzung)? → Akteur benennen (Muster 39)
- [ ] Quelle geprüft und belegt die Aussage? → Bei nachweisbarer Inkongruenz `[BELEG PRÜFEN]` markieren; bei nicht prüfbarer Quelle keine Kongruenz-Diagnose (Muster 42)
- [ ] Unsichtbare Unicode-Zeichen im Text? → Entfernen (Muster 43)
- [ ] Standard-Kapitel mit unbelegtem Fülltext? → Konkretisieren, umwidmen, integrieren, oder bei echter Substanzlosigkeit mit `[SUBSTANZ PRÜFEN]` markieren und stehen lassen (Muster 44)
- [ ] Calques (z. B. „am Ende des Tages", „in Reihenfolge zu")? → Registerabhängig: im Formal-Modus ersetzen; in Locker und Sachlich nur bei Häufung oder auffälliger Wörtlichkeit (Muster 45)
- [ ] False Friends („eventuell" im Sinn „schließlich", „aktuell" im Sinn „tatsächlich", „sensibel" im Sinn „vernünftig")? → Immer korrigieren, unabhängig vom Modus (Muster 45)

## Persönlichkeit und Stimme

Ein "sauberer" Text ohne KI-Muster ist noch nicht automatisch menschlich. Zu glatte Texte bleiben verdächtig.

**Hinweis:** Stimme einbringen gilt nur im Modus **Locker**. Im Modus **Sachlich** dezent halten. Im Modus **Formal** nicht anwenden.

Achten Sie deshalb zusätzlich auf:
- Variierendes Satztempo (kurz/lang gemischt)
- Konkrete Perspektive statt neutraler Floskeln
- Ehrliche Nuancen statt glatter Eindeutigkeit
- Gezielte Ich-Perspektive, wenn der Kontext sie erlaubt
- Weniger Symmetrie, mehr natürliche Sprache

## Nicht anfassen

- **Direkte Zitate von echten Personen.** Als [ZITAT – NICHT BEARBEITET] markieren.
- **Technische Spezifikationen, Formeln, Code.** Genauigkeit geht vor Stil.
- **Juristische oder regulatorische Sprache.** Bestimmte Formulierungen haben rechtliches Gewicht.
- **Weiche stilistische Muster, die 3+ Mal konsistent auftreten.** Gilt nur für MEDIUM/LOW-Muster aus stilistischen Kategorien (Betonung, Übergänge, Parallelismen, Register, Interpunktion). Solche Häufungen können bewusste Stilwahl sein – mit [MÖGLICHE STILISTISCHE WAHL – NICHT BEARBEITET] markieren und Häufigkeit nennen. **Nicht** anwenden auf: HIGH-Muster, technisch/strukturelle Befunde (Muster 21–24, 43), belegbezogene Befunde (Muster 11, 26, 42), False Friends aus Muster 45. Diese sind bei jedem Vorkommen einzeln zu korrigieren oder zu markieren – ihre Häufung verstärkt das Problem, sie wird nicht zur stilistischen Wahl.

## Leitplanken

- Nie eine Quelle erfinden. Echte Quelle, markieren, oder entfernen.
- Nie Stimme in formale/akademische Texte einbringen.
- Nie direkte Zitate von echten Personen bearbeiten.
- Nie **weiche stilistische Muster** (MEDIUM/LOW) bearbeiten, die 3+ Mal konsistent auftreten – stattdessen markieren. HIGH-Muster, Strukturbefunde (21–24, 43), belegbezogene Befunde (11, 26, 42) und False Friends (45) sind ausgenommen und bleiben einzeln zu korrigieren.
- Nie **Substanz** kürzen. Sachliche Aussagen und Informationsgehalt bleiben erhalten; Sätze umschreiben statt streichen. Artefakte ohne Informationsgehalt, deren Lösung im Muster explizit „entfernen/löschen" lautet (u. a. Muster 2, 3, 6, 17, 18, 19, 20, 21, 22, 24, 43), sind davon ausgenommen.
- Wenn der Text bereits sauber ist: das sagen und aufhören.
- **Kombinations-Prinzip:** Gilt nur für die **stilistische Gesamtdiagnose** „wirkt der Text KI-generiert?". Für diese Einschätzung ist ein einzelnes weiches Muster selten aussagekräftig – erst die Kombination mehrerer stilistischer Muster aus unterschiedlichen Kategorien rechtfertigt eine breite Überarbeitung. **Ausgenommen:** Technische/strukturelle Befunde (Muster 21, 22, 23, 24, 43), belegbezogene Befunde (Muster 11, 26, 42) und eindeutige Regelverstöße dürfen und sollen schon als Einzelbefund korrigiert werden. HIGH-Muster bleiben wie in Schritt 2 des Ablaufs beschrieben einzeln zu scannen.
- **Geltungsbereich:** Arbeitet auf direkt übergebenem Text. Dateibasierte Nutzung erfordert Read/Write in `allowed_tools`.

## Ausgabeformat

**Niemals den vollständigen Text ausgeben.** Nur geänderte Stellen zeigen.

Ausgabe in vier Stufen:

1. **Modus** (eine Zeile)
2. **Gefundene Muster:** Liste der erkannten KI-Tells (max. 6 Bullet Points, konkret mit Zitat aus dem Text)
3. **Geänderte Stellen:** Nur die überarbeiteten Abschnitte, jeweils als Vorher/Nachher-Paar
4. **Kurzaudit + finale Korrekturen:** Max. 3 verbleibende Tells + nur die nochmals geänderten Sätze. "Keine gefunden." wenn sauber.

Wenn eine Datei übergeben wird: Änderungen direkt mit dem Edit-Tool in die Datei schreiben, keinen Text ausgeben.

## Verwendungsbeispiel

### Input
```
Die atemberaubende Schönheit der Schweizer Alpen steht als Zeugnis für die Großartigkeit der Natur.
Diese Gebirgskette spielt eine wichtige Rolle bei der Gestaltung der europäischen Geographie und Kultur.
Darüber hinaus ist die Region von unschätzbarem Wert für Wanderer und Touristen.
Zusammenfassend kann man sagen, dass die Alpen ein wichtiges kulturelles Erbe darstellen, das
es zu schützen gilt. Lassen Sie mich wissen, wenn Sie weitere Informationen benötigen!
```

### Modus
Sachlich (angenommen – kein Kontext angegeben)

### Gefundene Muster
- Muster 1 [HIGH]: "steht als Zeugnis für" → Symbolik-Floskel
- Muster 1 [HIGH]: "spielt eine wichtige Rolle bei" → Symbolik-Floskel
- Muster 4 [HIGH]: "Darüber hinaus" → mechanische Konjunktion
- Muster 5 [HIGH]: "Zusammenfassend kann man sagen" → Abschnitts-Zusammenfassung
- Muster 18 [HIGH]: "Lassen Sie mich wissen" → kollaborative Kommunikation

### Geänderte Stellen

**Satz 1:**
❌ "Die atemberaubende Schönheit der Schweizer Alpen steht als Zeugnis für die Großartigkeit der Natur."
✓ "Die Schweizer Alpen beeindrucken – nicht wegen ihrer Höhe allein, sondern wegen ihrer Präsenz."

**Satz 2–3:**
❌ "Diese Gebirgskette spielt eine wichtige Rolle bei der Gestaltung der europäischen Geographie und Kultur. Darüber hinaus ist die Region von unschätzbarem Wert für Wanderer und Touristen."
✓ "Die Gebirgskette prägt Europas Geographie und Kultur seit Jahrhunderten. Wanderer und Touristen kommen aus diesem Grund."

**Satz 4–5:**
❌ "Zusammenfassend kann man sagen, dass die Alpen ein wichtiges kulturelles Erbe darstellen, das es zu schützen gilt. Lassen Sie mich wissen, wenn Sie weitere Informationen benötigen!"
✓ "Als Kultur- und Naturraum haben die Alpen bis heute großes Gewicht – und sollten entsprechend geschützt werden."

### Kurzaudit
- Satzrhythmus noch etwas gleichförmig (alle Sätze ähnlich lang)
- "großes Gewicht" bleibt etwas abstrakt

**Finale Korrektur (nur geänderter Satz):**
❌ "Als Kultur- und Naturraum haben die Alpen bis heute großes Gewicht – und sollten entsprechend geschützt werden."
✓ "Als Kultur- und Naturraum sind die Alpen seit Jahrhunderten relevant. Schutz ist keine Option, sondern Pflicht."

## Hinweise zum Skill

- Dieses Skill ist ein **Tool zur Verbesserung**, nicht zur Bestrafung
- Es funktioniert am besten bei Texten, die offensichtlich von KI stammen
- Bei etablierten Autoren oder subtilen Fällen kann es weniger hilfreich sein
- Verwenden Sie es iterativ: Mehrere Durchläufe führen oft zu besseren Ergebnissen
- Es ersetzt keine menschliche Redaktion – nutzen Sie es als Erste-Sicht-Tool

**Basiert auf:** [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) – Deutsche Wikipedia

**Original Skill:** [Humanizer](https://github.com/blader/humanizer) (Englische Version)
