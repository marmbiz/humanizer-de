---
name: Humanizer (Deutsch)
description: Erkennt und entfernt KI-generierte Schreibmuster aus deutschsprachigen Texten. Basierend auf der deutschen und englischen Wikipedia-Leitlinie zu KI-Schreibmustern, inklusive zweitem Anti-KI-Audit-Durchlauf. Erkennt u.a. aufgeblähte Symbolik, Werbesprache, mechanische Konjunktionen, vage Autoritäten, Gedankenstriche-Übernutzung, Trikolon, KI-Vokabular, negative Parallelismen, persuasive Floskeln, Signposting und fragmentierte Überschriften.
version: 2.3.0-de.1
author: Martin Moeller
maintainer_website: "https://www.martin-moeller.biz"
based_on: "German + English Wikipedia: Anzeichen/Signs of AI writing"
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
6. **NICHT ANFASSEN prüfen** – Verstöße rückgängig machen.
7. **Finaler Anti-KI-Pass**: "Was macht den Text noch offensichtlich KI-generiert?" Kurze, konkrete Tells benennen. Dann: "Jetzt so umschreiben, dass es nicht offensichtlich KI-generiert wirkt." Zweite Überarbeitung liefern.

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
| 8 | Negative Parallelismen | MEDIUM | "nicht nur... sondern auch", symmetrische Satzstrukturen |
| 9 | Trikolon (Regel der Drei) | MEDIUM | Tripel-Aufzählungen ohne echten Grund |
| 10 | Partizip-I-Konstruktionen | HIGH | "gewährleistend", "hervorhebend", "ermöglichend" |
| 11 | Vage Autoritäten | HIGH | "Branchenberichte zeigen", "Manche argumentieren" |
| 12 | Falsche Erweiterung ("von... bis") | MEDIUM | "von traditionellen bis modernen" |
| 13 | Übermäßige Fettschrift | MEDIUM | **wichtige Wörter** in Absätzen fett |
| 14 | Falsche Listen | LOW | `•` statt `-`, Markdown-Syntax statt Wikitext |
| 15 | Emojis vor Überschriften | LOW | "🎓 Bildung", "📊 Statistiken" |
| 16 | Gedankenstriche Überbenutzung | MEDIUM | Em-Dashes als Anglizismus, mehrere pro Absatz |
| 17 | Briefartiges Schreiben | HIGH | "Betreff:", "Liebe Wikipedia-Editoren", "Mit freundlichen Grüßen" |
| 18 | Kollaborative Kommunikation | HIGH | "Ich hoffe, das hilft", "Natürlich!", "Lassen Sie mich wissen" |
| 19 | Hinweise auf Wissensgrenzen | HIGH | "Stand [Datum]", "Bis zu meinem letzten Update" |
| 20 | Prompt-Ablehnung | HIGH | "Als KI-Sprachmodell kann ich nicht...", "Es tut mir leid, aber..." |
| 21 | Platzhaltertext | HIGH | "[Name einfügen]", "[Datum hier]", "TODO:" |
| 22 | Links zu Suchanfragen | HIGH | "https://www.google.com/search?q=..." |
| 23 | Markdown statt Wikitext | MEDIUM | `# Überschrift` statt `== Überschrift ==` |
| 24 | Fehlerhafter Wikitext | MEDIUM | Unvollständige Template-Tags, ungültige Syntax |
| 25 | Defekte Links | MEDIUM | 404-Fehler, Links zu nicht-existenten Artikeln |
| 26 | Ungültige DOI/ISBNs | MEDIUM | Erfundene Referenzen mit ungültigen Checksummen |
| 27 | Inkorrekte Referenzen-Format | MEDIUM | Englisches Datumsformat, falsche Reihenfolge |
| 28 | Falsche Kategorien | MEDIUM | `[[Category:...]]` statt `[[Kategorie:...]]` |
| 29 | Abrupte Abbrüche | LOW | Text bricht mitten im Satz ab |
| 30 | Wechsel im Schreibstil | MEDIUM | Absätze klingen wie verschiedene Autoren |
| 31 | Bearbeitungszusammenfassungen in Ich-Form | LOW | "Ich habe einen Absatz über...", "Meine Änderungen..." |
| 32 | Persuasive Autoritäts-Floskeln | MEDIUM | "Die eigentliche Frage ist", "Im Kern", "In Wirklichkeit" |
| 33 | Signposting und Ankündigungen | MEDIUM | "Schauen wir uns an", "Hier ist, was Sie wissen müssen" |
| 34 | Fragmentierte Überschriften | LOW | Generischer Einzeiler nach Überschrift ("Geschwindigkeit zählt.") |

## Die 34 Muster

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

#### 8. Negative Parallelismen [MEDIUM]
**Problem:** "Nicht nur... sondern auch" – zu argumentativ, zu literarisch.

Häufige Indikatoren:
- "nicht nur... sondern auch"
- "weder... noch... sondern"
- Symmetrische Satzstrukturen

**Warum LLMs das tun:** Rhetorische Effekte aus literarischen Quellen.

**Beispiel:**

❌ Schlecht: "Die Stadt ist nicht nur ein Handelszentrum, sondern auch ein Kulturzentrum."

✓ Besser: "Die Stadt ist Handels- und Kulturzentrum."

#### 9. Trikolon (Regel der Drei) [MEDIUM]
**Problem:** Übermäßige Nutzung der Regel-der-Drei als rhetorisches Mittel.

Häufige Indikatoren:
- Drei parallele Sätze/Phrasen hintereinander
- "X, Y und Z waren alle charakteristisch für..."
- Tripel-Aufzählungen ohne echten Grund

**Warum LLMs das tun:** Trikolon ist ein starkes rhetorisches Muster in der Schreibweise.

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
**Problem:** Em-Dashes (Gedankenstriche) als Anglizismus zu häufig.

Häufige Indikatoren:
- "Das Projekt – durchgeführt von..." (statt Komma)
- Mehrere Gedankenstriche pro Absatz
- Als Satzzeichen statt Klammer verwendet

**Warum LLMs das tun:** Englische Schreibweise wird imitiert.

**Lösung:** In deutsche Struktur umwandeln (Komma, Klammer, oder Punkt).

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

**Lösung:** Entfernen oder recherchieren und füllen.

#### 22. Links zu Suchanfragen statt Referenzen [HIGH]
**Problem:** URLs sind Google-Suchanfragen statt echte Referenzen.

Häufige Indikatoren:
- "https://www.google.com/search?q=..."
- "https://duckduckgo.com/?q=..."
- Suchanfragen in Fußnoten

**Warum LLMs das tun:** Kann keine echte URL recherchieren.

**Lösung:** Entfernen oder durch echte Quellen ersetzen.

### Auszeichnungstext (6 Muster)

#### 23. Markdown statt Wikitext [MEDIUM]
**Problem:** Markdown-Syntax in Wikipedia-Artikel statt Wikitext.

Häufige Indikatoren:
- `*fett*` oder `**fett**` statt `'''fett'''`
- `# Überschrift` statt `== Überschrift ==`
- `[Link](url)` statt `[Link url]`

**Warum LLMs das tun:** Trainiert auf Markdown-Quellen.

**Lösung:** Konvertieren zu Wikitext.

#### 24. Fehlerhafter Wikitext [MEDIUM]
**Problem:** Wikitext-Syntax ist ungültig oder unvollständig.

Häufige Indikatoren:
- "gehe zu [[Suche Nr. 42]]"
- Unvollständige Template-Tags
- `{{cite book|author=` ohne Schließ-`}}`

**Warum LLMs das tun:** Wikitext-Syntax wurde nicht korrekt generiert.

**Lösung:** Reparieren oder entfernen.

#### 25. Defekte Links [MEDIUM]
**Problem:** Zu viele rote Links oder tote Referenzen.

Häufige Indikatoren:
- 404 Fehler in Referenzen
- Links zu nicht-existenten Artikeln
- Tippfehler in Kategorien oder Artikeln

**Warum LLMs das tun:** Halluziniert Artikel-Titel.

**Lösung:** Prüfen und korrigieren oder entfernen.

#### 26. Ungültige DOI/ISBNs [MEDIUM]
**Problem:** Erfundene Referenzen mit ungültigen Checksummen.

Häufige Indikatoren:
- DOI mit ungültiger Prüfziffer
- ISBN mit Tippfehler
- Erfundene akademische Quellen

**Warum LLMs das tun:** Kann keine echten Nummern recherchieren.

**Lösung:** Verifizieren oder entfernen.

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

### Rhetorik und Struktur (3 Muster)

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
- **Muster, die 3+ Mal konsistent auftreten.** Als bewusste stilistische Entscheidung behandeln. Mit [MÖGLICHE STILISTISCHE WAHL – NICHT BEARBEITET] markieren und Häufigkeit nennen.

## Leitplanken

- Nie eine Quelle erfinden. Echte Quelle, markieren, oder entfernen.
- Nie Stimme in formale/akademische Texte einbringen.
- Nie direkte Zitate von echten Personen bearbeiten.
- Nie Muster bearbeiten, die 3+ Mal konsistent auftreten – stattdessen markieren.
- Wenn der Text bereits sauber ist: das sagen und aufhören.
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
