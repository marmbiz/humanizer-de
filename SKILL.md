---
name: Humanizer (Deutsch)
description: Erkennt und entfernt KI-generierte Schreibmuster aus deutschsprachigen Texten. Basierend auf der deutschen und englischen Wikipedia-Leitlinie zu KI-Schreibmustern, inklusive zweitem Anti-KI-Audit-Durchlauf.
version: 2.2.0-de.2
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

## Aufgabe und Ablauf

Wenn Sie einen Text humanisieren, arbeiten Sie in dieser Reihenfolge:

1. KI-Muster im Text erkennen
2. Problematische Stellen neu schreiben
3. Bedeutung und Fakten erhalten
4. Zielton einhalten (formal, technisch, locker, etc.)
5. Eine echte menschliche Stimme einbauen
6. Finalen Anti-KI-Pass ausführen:
   - Frage: "Was macht den Text noch offensichtlich KI-generiert?"
   - Kurze, konkrete Tells benennen
   - Zweite Überarbeitung liefern: "Jetzt so umschreiben, dass es nicht offensichtlich KI-generiert wirkt."

## Persönlichkeit und Stimme

Ein "sauberer" Text ohne KI-Muster ist noch nicht automatisch menschlich. Zu glatte Texte bleiben verdächtig.

Achten Sie deshalb zusätzlich auf:
- Variierendes Satztempo (kurz/lang gemischt)
- Konkrete Perspektive statt neutraler Floskeln
- Ehrliche Nuancen statt glatter Eindeutigkeit
- Gezielte Ich-Perspektive, wenn der Kontext sie erlaubt
- Weniger Symmetrie, mehr natürliche Sprache

## Die 31 Muster

### Sprache und Tonfall (12 Muster)

#### 1. Übermäßige Betonung von Symbolik
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

---

#### 2. Werbesprache und Superlative
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

---

#### 3. Redaktionelle Kommentare und Meta-Sprache
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

---

#### 4. Mechanische Konjunktionen
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

---

#### 5. Abschnitts-Zusammenfassungen
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

---

#### 6. Unpassendes "Fazit"
**Problem:** Wikipedia-Artikel enden mit explizitem "Fazit", was unpassend ist.

Häufige Indikatoren:
- "== Fazit =="
- "== Zusammenfassung =="
- Explizite Conclusion-Sektion

**Warum LLMs das tun:** Akademische Schreibweise wird als Struktur imitiert.

**Lösung:** Entfernen oder in natürliche Übergänge umwandeln.

---

#### 7. Schlussfolgerungen mit zu starker Dichotomie
**Problem:** "Trotz X... steht Y vor Z" – zu perfekt gedachte Gegensätze.

Häufige Indikatoren:
- "Trotz seiner Erfolge steht das Unternehmen vor Herausforderungen"
- "Obwohl... jedoch..."
- "Während X... bleibt Y..."

**Warum LLMs das tun:** Binäre Argumentationsstruktur im Training.

**Beispiel:**

❌ Schlecht: "Trotz seiner technologischen Fortschritte steht das Land vor wirtschaftlichen Herausforderungen."

✓ Besser: "Das Land macht technologische Fortschritte, kämpft aber mit wirtschaftlichen Problemen."

---

#### 8. Negative Parallelismen
**Problem:** "Nicht nur... sondern auch" – zu argumentativ, zu literarisch.

Häufige Indikatoren:
- "nicht nur... sondern auch"
- "weder... noch... sondern"
- Symmetrische Satzstrukturen

**Warum LLMs das tun:** Rhetorische Effekte aus literarischen Quellen.

**Beispiel:**

❌ Schlecht: "Die Stadt ist nicht nur ein Handelszentrum, sondern auch ein Kulturzentrum."

✓ Besser: "Die Stadt ist Handels- und Kulturzentrum."

---

#### 9. Trikolon (Regel der Drei)
**Problem:** Übermäßige Nutzung der Regel-der-Drei als rhetorisches Mittel.

Häufige Indikatoren:
- Drei parallele Sätze/Phrasen hintereinander
- "X, Y und Z waren alle charakteristisch für..."
- Tripel-Aufzählungen ohne echten Grund

**Warum LLMs das tun:** Trikolon ist ein starkes rhetorisches Muster in der Schreibweise.

**Beispiel:**

❌ Schlecht: "Die Wirtschaft war vielfältig, kreativ und widerstandsfähig."

✓ Besser: "Die Wirtschaft war kreativ und widerstandsfähig."

---

#### 10. Oberflächliche Analysen mit Partizip I
**Problem:** Zu viele "-end" Partizipien, die Aktion beschreiben ohne echte Tiefe.

Häufige Indikatoren:
- "gewährleistend"
- "hervorhebend"
- "zeigend"
- "darstellend"
- "ermöglichend"

**Warum LLMs das tun:** Diese Konstruktionen sind grammatikalisch korrekt, erzeugen aber einen oberflächlichen, technischen Ton.

**Beispiel:**

❌ Schlecht: "Die Technologie ermöglicht, dass Unternehmen ihre Effizienz steigern, ihre Kosten senken und ihre Konkurrenzfähigkeit verbessern."

✓ Besser: "Die Technologie hilft Unternehmen effizienter zu werden, Kosten zu senken und konkurrenzfähig zu bleiben."

---

#### 11. Vage Autoritäten
**Problem:** Unspezifische Quellen, die keinen echten Beweis liefern.

Häufige Indikatoren:
- "Branchenberichte zeigen"
- "Beobachter haben zitiert"
- "Es wird gesagt"
- "Manche argumentieren"
- "Mehrere Studien deuten darauf hin" (ohne Quelle)

**Warum LLMs das tun:** Kann echte Quellen nicht zitieren, also erfinden es Platzhalter.

**Beispiel:**

❌ Schlecht: "Branchenberichte zeigen, dass der Markt wächst."

✓ Besser: "Der Markt wächst (laut Wirtschaftsministerium 2024)." oder "Der Markt wächst – ein Trend, der seit 2020 beobachtet wird."

---

#### 12. Falsche Erweiterung ("von... bis")
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

---

### Stil (4 Muster)

#### 13. Übermäßige Fettschrift
**Problem:** Bold wird für Emphasis statt für echte Struktur verwendet.

Häufige Indikatoren:
- **wichtige Wörter** in Absätzen fett
- Mehrere fettgedruckte Wörter pro Absatz
- Bold für Hervorhebung statt für Struktur

**Warum LLMs das tun:** Versucht, Wichtigkeit zu signalisieren, wo Klarheit hilft.

**Lösung:** Entfernen oder in Überschriften umwandeln.

---

#### 14. Falsche Listen
**Problem:** Bullet-Punkte in nicht-Wikitext-Format in Wikipedia-Artikel.

Häufige Indikatoren:
- `•` statt `-` oder `*`
- `–` statt `*` für Aufzählungen
- Markdown-Syntax statt Wikitext

**Warum LLMs das tun:** Trainiert auf Markdown und Office-Formaten.

**Lösung:** In korrektes Wikitext-Format konvertieren.

---

#### 15. Emojis vor Überschriften
**Problem:** Emojis werden verwendet, um visuelle Struktur zu schaffen.

Häufige Indikatoren:
- "🎓 Bildung"
- "📊 Statistiken"
- "🌍 Globaler Kontext"

**Warum LLMs das tun:** Modern wirken, aber nicht für Wikipedia.

**Lösung:** Entfernen.

---

#### 16. Gedankenstriche Überbenutzung
**Problem:** Em-Dashes (Gedankenstriche) als Anglizismus zu häufig.

Häufige Indikatoren:
- "Das Projekt – durchgeführt von..." (statt Komma)
- Mehrere Gedankenstriche pro Absatz
- Als Satzzeichen statt Klammer verwendet

**Warum LLMs das tun:** Englische Schreibweise wird imitiert.

**Lösung:** In deutsche Struktur umwandeln (Komma, Klammer, oder Punkt).

---

### Kommunikation (6 Muster)

#### 17. Briefartiges Schreiben
**Problem:** Artikel sind als Briefe strukturiert, nicht als Inhalte.

Häufige Indikatoren:
- "Betreff: ..."
- "Liebe Wikipedia-Editoren"
- "Vielen Dank für..."
- "Mit freundlichen Grüßen"

**Warum LLMs das tun:** ChatBot-Verhalten, nicht Enzyklopädie-Verhalten.

**Lösung:** Vollständig entfernen oder umschreiben.

---

#### 18. Kollaborative Kommunikation
**Problem:** Der Text spricht den Leser direkt an, statt Fakten bereitzustellen.

Häufige Indikatoren:
- "Ich hoffe, das hilft"
- "Natürlich!"
- "Lassen Sie mich wissen"
- "Bitte fragen Sie, wenn..."
- "Wie Sie sehen können..."

**Warum LLMs das tun:** Trainiert, höflich und engagiert zu sein.

**Beispiel:**

❌ Schlecht: "Wie Sie sehen können, war die Produktivität beeindruckend. Lassen Sie mich wissen, wenn Sie weitere Fragen haben!"

✓ Besser: "Die Produktivität war in dieser Zeit bemerkenswert."

---

#### 19. Hinweise auf Wissensgrenzen
**Problem:** Der Text offenbart seine KI-Natur durch Datums-Hinweise.

Häufige Indikatoren:
- "Stand [Datum]"
- "Bis zu meinem letzten Update"
- "Nach meinem Wissen"
- "[Aktualisierung erforderlich]"

**Warum LLMs das tun:** Versucht, Ehrlichkeit zu zeigen.

**Lösung:** Entfernen oder in neutrale Quellen umwandeln.

---

#### 20. Prompt-Ablehnung
**Problem:** Der Text lehnt Anfragen ab wie ein Chatbot.

Häufige Indikatoren:
- "Als KI-Sprachmodell kann ich nicht..."
- "Es tut mir leid, aber..."
- "Ich kann keine aktuelle Information bereitstellen..."
- "Das liegt außerhalb meiner Fähigkeiten"

**Warum LLMs das tun:** Sicherheitsrichtlinien und Höflichkeit.

**Lösung:** Entfernen vollständig.

---

#### 21. Platzhaltertext
**Problem:** Template-Platzhalter wurden nicht gefüllt.

Häufige Indikatoren:
- "[Name einfügen]"
- "[Datum hier]"
- "[Quelle erforderlich]" (in Artikel statt Meta)
- "TODO:"
- "[Bearbeiter Name]"

**Warum LLMs das tun:** Kann keine echten Werte generieren, hinterlässt Platzhalter.

**Lösung:** Entfernen oder recherchieren und füllen.

---

#### 22. Links zu Suchanfragen statt Referenzen
**Problem:** URLs sind Google-Suchanfragen statt echte Referenzen.

Häufige Indikatoren:
- "https://www.google.com/search?q=..."
- "https://duckduckgo.com/?q=..."
- Suchanfragen in Fußnoten

**Warum LLMs das tun:** Kann keine echte URL recherchieren.

**Lösung:** Entfernen oder durch echte Quellen ersetzen.

---

### Auszeichnungstext (6 Muster)

#### 23. Markdown statt Wikitext
**Problem:** Markdown-Syntax in Wikipedia-Artikel statt Wikitext.

Häuffige Indikatoren:
- `*fett*` oder `**fett**` statt `'''fett'''`
- `# Überschrift` statt `== Überschrift ==`
- `[Link](url)` statt `[Link url]`

**Warum LLMs das tun:** Trainiert auf Markdown-Quellen.

**Lösung:** Konvertieren zu Wikitext.

---

#### 24. Fehlerhafter Wikitext
**Problem:** Wikitext-Syntax ist ungültig oder unvollständig.

Häuffige Indikatoren:
- "gehe zu [[Suche Nr. 42]]"
- Unvollständige Template-Tags
- `{{cite book|author=` ohne Schließ-`}}`

**Warum LLMs das tun:** Wikitext-Syntax wurde nicht korrekt generiert.

**Lösung:** Reparieren oder entfernen.

---

#### 25. Defekte Links
**Problem:** Zu viele rote Links oder tote Referenzen.

Häuffige Indikatoren:
- 404 Fehler in Referenzen
- Links zu nicht-existenten Artikeln
- Tippfehler in Kategorien oder Artikeln

**Warum LLMs das tun:** Halluziniert Artikel-Titel.

**Lösung:** Prüfen und korrigieren oder entfernen.

---

#### 26. Ungültige DOI/ISBNs
**Problem:** Erfundene Referenzen mit ungültigen Checksummen.

Häuffige Indikatoren:
- DOI mit ungültiger Prüfziffer
- ISBN mit Tippfehler
- Erfundene akademische Quellen

**Warum LLMs das tun:** Kann keine echten Nummern recherchieren.

**Lösung:** Verifizieren oder entfernen.

---

#### 27. Inkorrekte Referenzen-Format
**Problem:** Zitierformat entspricht nicht deutschen Wikipedia-Standards.

Häuffige Indikatoren:
- Englisches Datumsformat statt deutsches
- Falsche Reihenfolge (Nachname, Vorname)
- Incompatible Zitierstyle

**Warum LLMs das tun:** Englisches Training dominiert.

**Lösung:** Anpassung an deutsches Format (z.B. `1. Januar 2024` statt `January 1, 2024`).

---

#### 28. Falsche Kategorien
**Problem:** Kategorien sind nicht-existent oder nicht-deutsch.

Häuffige Indikatoren:
- `[[Category:American Writers]]` statt `[[Kategorie:Amerikanische Schriftsteller]]`
- Erfundene Kategorien
- Rote Kategorie-Links

**Warum LLMs das tun:** Trainiert auf englischen Wikipedia-Kategorien.

**Lösung:** Zu korrekten deutschen Kategorien korrigieren.

---

### Verschiedenes (3 Muster)

#### 29. Abrupte Abbrüche
**Problem:** Text bricht mitten im Satz ab.

Häuffige Indikatoren:
- "Die Gründung der Stadt war..."
- Incomplete sentences
- Trailing text ohne Sinn

**Warum LLMs das tun:** Token-Limit erreicht oder Ausgabe wurde unterbrochen.

**Lösung:** Löschen oder vervollständigen mit echten Informationen.

---

#### 30. Wechsel im Schreibstil
**Problem:** Plötzlicher Wechsel von informell zu formell oder umgekehrt.

Häuffige Indikatoren:
- Absätze klingen wie verschiedene Autoren
- Abrupt wechselnde Tonalität
- Mix aus akademisch und umgangssprachlich

**Warum LLMs das tun:** Verschiedene Trainingsdaten-Quellen.

**Lösung:** Harmonisieren zum konsistenten Stil.

---

#### 31. Ausführliche Bearbeitungszusammenfassungen in Ich-Form
**Problem:** Edit-Summaries sind verbose und persönlich.

Häuffige Indikatoren:
- "Ich habe einen Absatz über..."
- "Meine Änderungen verbessern..."
- "Ich denke, dass..."

**Warum LLMs das tun:** Chatbot-Verhalten auch in Metadaten.

**Lösung:** Entfernen oder in neutrale Form umwandeln ("Absatz über X hinzugefügt").

---

## Ausgabeformat

Geben Sie die Überarbeitung in drei Stufen aus:

1. **Entwurf (humanisiert):** Erste überarbeitete Version
2. **Kurzaudit:** "Was macht den Text noch offensichtlich KI-generiert?"
3. **Finale Version:** Zweiter Durchlauf nach dem Audit

Optional:
- Kurze Zusammenfassung der wichtigsten Änderungen (nur wenn hilfreich)

## Verwendungsbeispiel

### Input
```
Die atemberaubende Schönheit der Schweizer Alpen steht als Zeugnis für die Großartigkeit der Natur.
Diese Gebirgskette spielt eine wichtige Rolle bei der Gestaltung der europäischen Geographie und Kultur.
Darüber hinaus ist die Region von unschätzbarem Wert für Wanderer und Touristen.
Zusammenfassend kann man sagen, dass die Alpen ein wichtiges kulturelles Erbe darstellen, das
es zu schützen gilt. Lassen Sie mich wissen, wenn Sie weitere Informationen benötigen!
```

### Entwurf (humanisiert)
```
Die Schweizer Alpen beeindrucken durch ihre Landschaft. Diese Gebirgskette prägt Europas Geographie
und Kultur seit Jahrtausenden. Die Region ist bekannt bei Wanderern und zieht viele Touristen an.
Die Alpen sind wichtig für das europäische Kulturerbe und verdienen Schutz.
```

### Kurzaudit: Was macht den Text noch offensichtlich KI-generiert?
- Satzrhythmus ist noch etwas gleichförmig.
- Einige Formulierungen bleiben neutral-abstrakt ("wichtig für das Kulturerbe").

### Finale Version (nach Audit)
```
Die Schweizer Alpen sind markant, nicht nur wegen der Höhe, sondern wegen ihrer prägenden Rolle in Europas Landschaft und Geschichte.
Viele Menschen kommen zum Wandern, Klettern oder einfach, um die Region zu erleben.
Als Kultur- und Naturraum haben die Alpen bis heute großes Gewicht und sollten entsprechend geschützt werden.
```

---

## Hinweise zum Skill

- Dieses Skill ist ein **Tool zur Verbesserung**, nicht zur Bestrafung
- Es funktioniert am besten bei Texten, die offensichtlich von KI stammen
- Bei etablierten Autoren oder subtilen Fällen kann es weniger hilfreich sein
- Verwenden Sie es iterativ: Mehrere Durchläufe führen oft zu besseren Ergebnissen
- Es ersetzt keine menschliche Redaktion – nutzen Sie es als Erste-Sicht-Tool

---

**Basiert auf:** [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) – Deutsche Wikipedia

**Original Skill:** [Humanizer](https://github.com/blader/humanizer) (Englische Version)
