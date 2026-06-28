# Humanizer-de Pattern Catalog

Vollstaendiger Musterkatalog fuer Humanizer (Deutsch) v4.3.0. Nur bei konkreter Musterdiagnose, Audit oder Grenzfaellen laden.

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
| 16 | Dash-Satzzeichen und Gedankenstrich-Cluster | MEDIUM | Mehrere pro Absatz, gepaarte Einschübe, ` - ` / ` -- ` / `—` / `–` als Satzzeichen |
| 17 | Briefartiges Schreiben | HIGH | "Betreff:", "Liebe Wikipedia-Editoren", "Mit freundlichen Grüßen" |
| 18 | Kollaborative Kommunikation | HIGH | "Ich hoffe, das hilft", "Natürlich!", "Lassen Sie mich wissen" |
| 19 | Hinweise auf Wissensgrenzen | HIGH | "Stand [Datum]", "Bis zu meinem letzten Update" |
| 20 | Prompt-Ablehnung | HIGH | "Als KI-Sprachmodell kann ich nicht...", "Es tut mir leid, aber..." |
| 21 | Platzhaltertext | HIGH | "[Name einfügen]", "[Datum hier]", "TODO:" |
| 22 | Links zu Suchanfragen | HIGH | "https://www.google.com/search?q=..." |
| 23 | Markdown statt Wikitext | MEDIUM | `# Überschrift` statt `== Überschrift ==` |
| 24 | Fehlerhafter Wikitext und KI-Tool-Artefakte | MEDIUM | Unvollständige Template-Tags, oaicite, contentReference |
| 25 | Defekte Links | MEDIUM | 404-Fehler, Links zu nicht-existenten Artikeln |
| 26 | Zitatfabrikation und unverifizierbare Referenzen | HIGH | Erfundene Quellen, ungültige DOIs/ISBNs, halluzinierte Publikationen, echte Quelle belegt nichts |
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
| 46 | Falsche deutsche Anführungszeichen | HIGH | Falsches Schlusszeichen: „Text” statt „Text“ (U+201E/U+201C) |
| 47 | Englische Titel-Großschreibung | MEDIUM | "Die Neue KI Strategie" statt Satzschreibung |
| 48 | Englisches Dezimalformat und Datumsformat | LOW | "3.5" statt "3,5"; "May 12" statt "12. Mai" |
| 49 | Apostroph-Fehler | MEDIUM | "Peter's" statt "Peters", englisches Genitiv-Apostroph |
| 50 | Interpunktion bei Stichpunkt-Aufzählungen | LOW | Großbuchstaben und Punkte bei reinen Stichworten |
| 51 | Obsessive Parataxe | MEDIUM | Zu viele gleichförmige Hauptsätze ohne Subordination |
| 52 | Diff-verankertes Schreiben | MEDIUM | "wurde jetzt ergänzt", "neu hinzugefügt", "ersetzt die alte Lösung" |
| 53 | Lückenfüllende Spekulation | HIGH | "hält sich bedeckt", "macht keine Angaben", "vermutlich", obwohl Quelle fehlt |
| 54 | Doppelpunkt-Titel-Schema | MEDIUM | "Phrase: Was/Warum/Wie ..." gehäuft in Titel/H1/H2 |
| 55 | Gleichförmiger Satzrhythmus | MEDIUM | Sätze fast gleich lang, Subjekt zuerst, niedrige Burstiness |
| 56 | Aphorismus-Formeln | MEDIUM | "X ist die Sprache des Y", "X wird zur Falle", "die Währung von" |
| 57 | Markdown-Struktur-Artefakte | MEDIUM | Ein-Zeilen-Tabellen, übersprungene Heading-Ebenen (H2→H4), `---` vor Überschrift |
| 58 | Abstrakta-Stapel und Hypernym-Präferenz | MEDIUM | "Maßnahmen", "Aspekte", "Lösungen", Nominalstil statt belegter Konkretion |
| 59 | Erfundene Ich-Erfahrung und forcierte Lockerheit | HIGH | gestellte Anekdoten, "Ehrlich gesagt", "Spoiler:", behauptete Praxiserfahrung ohne Träger |
| 60 | Synonym-Rotation für dieselbe Entität | MEDIUM | "die Hansestadt", "die Elbmetropole" für denselben Referenten |
| 61 | Isometrisches Dokument | MEDIUM | alle Absätze/Sektionen/Listen-Items gleich lang, symmetrische Abdeckung |
| 62 | Markerloser Schließzwang | MEDIUM | bewertender Abschlusssatz ohne neue Information am Absatzende |
| 63 | Modalpartikel-Anomalie | LOW | Partikelarmut im Nähe-Register oder Partikel-Überdosis (nur Locker) |
| 64 | KI-Marker-Vokabular | MEDIUM | "beleuchten", "eintauchen", "spannend", "nahtlos", "die digitale Landschaft" in Häufung |
| 65 | Kopula-Vermeidung | MEDIUM | "fungiert als", "stellt dar", "verfügt über", "zeichnet sich aus durch" statt "ist"/"hat" |
| 66 | Fake-Analyse-Anhang | MEDIUM | "...was X unterstreicht/verdeutlicht/belegt", "...und zeigt damit, dass" – Relativsatz ohne neue Information |

## Statistische Detektoren (GPTZero u. a.)

Statistische Detektoren prüfen nicht die Muster aus diesem Katalog. Sie schätzen zwei Größen:

- **Perplexity** – wie vorhersagbar das nächste Wort ist. Glatte, fachlich präzise Prosa hat niedrige Perplexity.
- **Burstiness** – wie stark Satzlänge und -bau variieren. Gleichmäßige Kadenz hat niedrige Burstiness.

Die menschenlesbaren Labels dieser Tools ("Robotic Formality", "Mechanical Precision", "Impersonal Tone" ...) sind nur Übersetzungen dieser zwei Größen. Sie verteilen sich über fast den ganzen Text statt auf einzelne Floskeln. Entscheidend: **Diese Detektoren bestrafen oft genau das, was einen guten Fachtext ausmacht** – Fachbegriffe, korrekte Quellenattribution, sachliche Klarheit. Solche Befunde sind kein KI-Tell und werden nicht "behoben".

| Detektor-Label | Misst real | Handlung |
|---|---|---|
| Mechanical Precision | niedrige Perplexity durch Fachbegriffe | nicht behandeln – Fachsprache bewahren |
| Impersonal Tone | Passiv, Quellenattribution | nicht behandeln, außer Muster 39 liegt vor |
| Robotic Formality | klare Struktur, Doppelpunkt-Titel | nur bei Muster 54 (gehäufte Doppelpunkt-Titel) |
| Lacks Creativity / Lacks Creative Grammar | niedrige Burstiness | nur bei Muster 55/51, mit Carve-out |
| Mechanical Writing | gleichförmige Kadenz | nur bei Muster 55, mit Carve-out |

Der einzige substanzwahrende Hebel gegen niedrige Burstiness ist Muster 55 (Satzrhythmus spreizen). Niedrige Perplexity bei korrekter Fachsprache ist nicht "reparierbar", ohne den Text zu verschlechtern – und das ist nicht Aufgabe dieses Skills. Siehe SKILL.md-Leitplanke zu statistischen Detektoren.

## Die 66 Muster

### Sprache und Tonfall (17 Muster)

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

#### 58. Abstrakta-Stapel und Hypernym-Präferenz [MEDIUM]
**Kategorie:** Sprache und Tonfall
**Problem:** Das Modell wählt systematisch den Oberbegriff statt der Sache: "Maßnahmen", "Aspekte", "Lösungen", "Herausforderungen", "Faktoren", "Prozesse" – oft kombiniert mit Nominalstil ("die Umsetzung der Optimierung der Abläufe"). Der Text bleibt korrekt, sagt aber nichts Prüfbares. Das ist die behandelbare Hälfte niedriger Perplexity: Konkretisierung erhöht Informationsgehalt und Wortvarianz zugleich, ohne Fachsprache anzutasten.
Häufige Indikatoren:
- "verschiedene Maßnahmen", "zahlreiche Aspekte", "innovative Lösungen", "zentrale Faktoren"
- Nominalstil-Ketten: "die Nutzung", "die Bereitstellung", "die Umsetzung", "die Optimierung"
- Einzelne Marker-Vokabeln gehören zu Muster 64; Muster 58 greift, wenn der Oberbegriff eine im Text belegte Konkretion ersetzt
**Warum LLMs das tun:** Hypernyme sind die statistisch sichere Wahl; sie passen auf jeden Kontext und sind in zusammenfassenden Trainingsdaten überrepräsentiert.
**Kein Problem, wenn:** der Oberbegriff echte Mengen bündelt ("drei Maßnahmen: A, B, C") oder die Konkretion im übergebenen Kontext schlicht fehlt.
**Lösung:** Durch den konkreten Sachverhalt ersetzen, der im Text oder Kontext belegt ist. Fehlt er: stehen lassen oder `[KONKRETION NÖTIG]` markieren. Nie Details erfinden, um konkret zu wirken – das wäre Muster 53.
❌ Schlecht: "Die Stadt ergriff verschiedene Maßnahmen zur Verbesserung der Verkehrssituation."
✓ Besser: "Die Stadt sperrte zwei Durchgangsstraßen und senkte das Tempolimit auf 30 km/h."

#### 60. Synonym-Rotation für dieselbe Entität [MEDIUM]
**Kategorie:** Sprache und Tonfall
**Problem:** Zwanghafte Wiederholungsvermeidung: "die Hansestadt", "die Elbmetropole", "die Stadt an der Alster" für denselben Referenten. Menschen wiederholen das Wort oder pronominalisieren; die Rotation wirkt enzyklopädisch-bemüht und macht Texte schwerer lesbar, weil der Leser Referenzen neu auflösen muss.
Häufige Indikatoren:
- 3+ verschiedene Bezeichnungen für dieselbe Person/Stadt/Firma in einem Abschnitt
- Beinamen ohne Informationswert ("der Streaming-Riese", "das Münchner Unternehmen")
- Pronomen fast vollständig abwesend, obwohl Referenz eindeutig wäre
**Warum LLMs das tun:** Stilratgeber-Trainingsdaten bestrafen Wortwiederholung; das Modell übergeneralisiert die Regel.
**Kein Problem, wenn:** die Variante echte Information trägt (offizieller Beiname im relevanten Kontext) oder die Wiederholung im selben Satz tatsächlich hässlich klingt.
**Lösung:** Auf Grundwort + Pronomen zurückführen. Maximal eine Beiname-Variante pro Text, und nur mit Mehrwert.
❌ Schlecht: "Hamburg wächst. Die Hansestadt investiert in den Hafen. Die Elbmetropole gilt als Logistikzentrum."
✓ Besser: "Hamburg wächst. Die Stadt investiert in den Hafen und gilt als Logistikzentrum."

#### 63. Modalpartikel-Anomalie [LOW]
**Kategorie:** Sprache und Tonfall
**Problem:** Nur im Modus Locker behandeln, in Sachlich höchstens diagnostisch. Beide Extreme sind Tells: (a) Vollständige Abwesenheit von Modalpartikeln (ja, doch, eben, halt, wohl, mal, schon, ohnehin) in einem Text, der sonst Nähe-Register fährt – LLM-Deutsch ist partikelarm, weil Partikeln keine propositionale Funktion haben. (b) Partikel-Überdosis als Über-Humanisierung (vgl. Muster 59).
Häufige Indikatoren:
- Blog/Newsletter im Du-Ton ohne eine einzige Modalpartikel über mehrere Absätze
- Umgekehrt: mehrere Partikeln pro Satz ("Das ist ja eben halt schon wichtig")
**Warum LLMs das tun:** Modalpartikeln tragen Haltung statt Information; das Training optimiert auf Information. Bei "schreib locker"-Anweisungen kippt es ins Gegenteil.
**Kein Problem, wenn:** Sachlich/Formal – dort ist Partikelarmut korrekt und erwünscht.
**Lösung:** In Locker sparsam dosieren: höchstens eine Partikel pro Absatz, nur wo sie eine tatsächliche Haltung des Texts trägt. Nie mechanisch nachrüsten.
❌ Schlecht (Nähe-Register, partikelfrei): "Du kennst das Problem. Die Lösung ist einfach. Du brauchst nur drei Schritte."
✓ Besser: "Du kennst das Problem ja. Die Lösung ist simpel – drei Schritte reichen schon."

#### 64. KI-Marker-Vokabular [MEDIUM]
**Kategorie:** Sprache und Tonfall
**Problem:** Bestimmte Wörter kommen in deutschem Post-2023-KI-Text deutlich häufiger vor als in menschlichem Gebrauchstext — unabhängig davon, ob die Aussage stimmt. Einzeln sind sie unauffällig; ihr gemeinsames Auftreten ist das Signal. Adaptiert aus blader/humanizer Muster #7 ("Overused AI Vocabulary").
Häufige Indikatoren (Ko-Okkurrenz zählt):
- Verben: "beleuchten", "eintauchen", "unterstreichen", "aufzeigen", "entfesseln", "revolutionieren", "prägen" (figurativ)
- Adjektive: "spannend", "entscheidend", "maßgeblich", "nahtlos", "robust" (außerhalb der Technik), "vielschichtig", "facettenreich", "dynamisch", "ganzheitlich", "maßgeschneidert", "essenziell", "lebendig" (für Abstrakta)
- Abstrakta: "die (digitale/mediale/...) Landschaft" (figurativ), "das Zusammenspiel", "die Reise" (figurativ), "der Meilenstein", "das Spannungsfeld"
**Warum LLMs das tun:** Diese Wörter sind die deutschen Gegenstücke zu "delve", "tapestry", "showcase", "landscape" — RLHF-geprägte Vorzugsvokabeln, die Gewicht signalisieren sollen und in KI-Trainingszyklen selbstverstärkend häufiger werden.
**Abgrenzung:** Muster 2 = Werbesprache/Superlative ("atemberaubend"). Muster 58 = Hypernym ersetzt eine belegte Konkretion. Muster 64 = die Frequenz-Marker selbst, auch wenn der Satz informativ ist.
**Kein Problem, wenn:** das Wort fachlich gebunden ist ("robuste Statistik", "dynamisches Routing", "Meilenstein" im Projektplan) oder einzeln steht. Erst ab 3+ Markern im selben Text als Cluster behandeln.
**Lösung:** Durch das gewöhnliche Wort ersetzen ("beleuchten" → "untersuchen"/"beschreiben", "spannend" → streichen oder konkret begründen, "die digitale Landschaft" → das gemeinte konkrete Feld benennen).
❌ Schlecht: "Der Artikel beleuchtet das vielschichtige Zusammenspiel der Akteure in der digitalen Landschaft und zeigt spannende Entwicklungen auf."
✓ Besser: "Der Artikel beschreibt, wie die drei großen Anbieter aufeinander reagieren — und wo sich der Markt gerade dreht."

#### 65. Kopula-Vermeidung [MEDIUM]
**Kategorie:** Sprache und Tonfall
**Problem:** LLMs ersetzen das schlichte "ist"/"hat" durch gespreizte Ersatzkonstruktionen: "fungiert als", "dient als", "stellt ... dar", "repräsentiert", "bildet", "erweist sich als", "präsentiert sich als", "zeichnet sich durch ... aus", "verfügt über", "bietet", "beherbergt", "wartet mit ... auf". Der Satz klingt gehobener, sagt aber exakt dasselbe. Adaptiert aus blader/humanizer Muster #8 ("Copula Avoidance").
Häufige Indikatoren:
- "fungiert als" / "dient als" statt "ist"
- "verfügt über" / "bietet" / "beherbergt" statt "hat"
- "stellt einen wichtigen Bestandteil dar" statt "ist Teil von"
- "zeichnet sich durch hohe Qualität aus" statt "ist gut verarbeitet"
- Mehrere solcher Konstruktionen im selben Absatz
**Warum LLMs das tun:** Ersatzverben wirken im Training "wertiger" als die Kopula; Stilratgeber gegen Wortwiederholung verstärken die Vermeidung von "ist"/"hat".
**Abgrenzung:** Muster 1 = symbolische Aufladung ("steht als Zeugnis für"). Muster 65 = die nüchterne Ersatzkonstruktion ohne Symbolik. Muster 39 = Passiv/subjektlose Fragmente.
**Kein Problem, wenn:** die Konstruktion echte Zusatzinformation trägt ("dient als Notausgang" beschreibt eine Funktion, die vom Wesen abweicht) oder eine einzelne Wiederholung von "ist" vermeidet. Erst bei Häufung behandeln.
**Lösung:** Auf "ist"/"hat" zurückführen, wo keine Information verloren geht.
❌ Schlecht: "Die Galerie fungiert als Ausstellungsraum des Vereins und verfügt über vier Räume mit insgesamt 280 Quadratmetern."
✓ Besser: "Die Galerie ist der Ausstellungsraum des Vereins und hat vier Räume mit insgesamt 280 Quadratmetern."

#### 66. Fake-Analyse-Anhang [MEDIUM]
**Kategorie:** Sprache und Tonfall
**Problem:** LLMs hängen an normale Informationssätze scheinanalytische Relativsätze oder Anschlusskonstruktionen, die eine Schlussfolgerung vortäuschen, aber keine neue Information liefern. Erkennbar am Löschtest: Fällt „was X unterstreicht/zeigt/verdeutlicht" weg, geht keine Information verloren – der Hauptsatz steht vollständig. Die Konstruktion ist grammatikalisch korrekt; ihr Tell ist die funktionale Leere des Anhangs.
Häufige Indikatoren:
- „...was X unterstreicht / belegt / verdeutlicht / bestätigt / beweist"
- „...und zeigt / verdeutlicht damit, dass..."
- „...und unterstreicht die Bedeutung von..."
- „...und macht deutlich, wie wichtig..."
- „...was zeigt, dass hier Handlungsbedarf besteht"
**Warum LLMs das tun:** Training auf akademischen Texten, die Schlussfolgerungen explizit signalisieren; das Modell lernt, Gewicht durch Relativkonstruktionen auszudrücken, auch wenn kein neuer Gedanke folgt.
**Abgrenzung:** Muster 3 = eigenständige Sätze mit Meta-Kommentar ("es ist wichtig zu bemerken"). Muster 10 = Partizip-I beschreibt gleichzeitige Aktion ("ermöglichend"). Muster 62 = eigenständiger Schlusssatz am Absatzende. Muster 64 = einzelne Frequenz-Marker-Vokabeln; Muster 66 = die syntaktische Anhang-Konstruktion selbst.
**Kein Problem, wenn:** Der Relativsatz echte, aus dem Hauptsatz nicht ableitbare Information hinzufügt (z. B. "Die Studie wurde dreimal wiederholt, was die Replizierbarkeit nachweist" – wenn die Dreifachwiederholung tatsächlich das erste Replizierbarkeits-Signal im Text ist).
**Lösung:** Relativsatz streichen. Falls die Schlussfolgerung echte Information trägt: als eigenständigen Satz mit konkretem Beleg formulieren statt als Anhang.
❌ Schlecht: "Das Team lieferte die Migration in drei Wochen ab, was die hohe Effizienz des Vorgehens unterstreicht."
✓ Besser: "Das Team lieferte die Migration in drei Wochen ab." (oder: "...ab – geplant waren sechs.")

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

#### 16. Dash-Satzzeichen und Gedankenstrich-Cluster [MEDIUM]
**Problem:** Gedankenstriche und Dash-Ersatzzeichen (`–`, `—`, ` -- `, ` - `) werden von LLMs als rhetorische Kurzform übermäßig eingesetzt. Ein einzelner Gedankenstrich pro Absatz kann legitim sein; mehrere pro Absatz, gepaarte Einschübe oder ein mechanisches "nicht X – sondern Y"-Schema sind starke KI-Tells. Der Tell verschwindet nicht, wenn nur das Glyph gewechselt wird.

Häufige Indikatoren:
- "Das Projekt – durchgeführt von..." (statt Komma oder Klammer)
- Mehrere Gedankenstriche pro Absatz
- Als Satzzeichen statt Klammer verwendet
- Gepaarte Einschübe: "Der Bericht – der drei Kontinente abdeckte – kam zum Schluss..."
- Spaced Em-Dashes: "Die Politik — ohne Vorwarnung angekündigt — betrifft..."
- Doppelstriche als Ersatz: "Die Änderungen -- laut Kritikern überfällig -- treten sofort in Kraft."
- Spaced Hyphen als Dash-Ersatz: "Danke für die Einführung - ich setze dich auf bcc."
- Rhetorische Punchline: "Es geht nicht um Geschwindigkeit – es geht um Vertrauen."

**Warum LLMs das tun:** Englische Schreibweise, Marketingrhythmus und Chat-Oberflächen werden imitiert. Gepaarte Einschübe sehen eingeschoben aus, nicht geschrieben.

**Ersetzungshierarchie** (in Prioritätsreihenfolge):
1. **Punkt**: zwei vollständige Gedanken als zwei Sätze führen.
2. **Komma**: kurzer Einschub oder enge Apposition.
3. **Doppelpunkt**: Erklärung, Folge oder Liste.
4. **Semikolon**: zwei selbstständige, locker verbundene Hauptsätze.
5. **Klammer**: echter Nebengedanke.
6. **Streichen oder umbauen**: wenn der Einschub nur Schlagseite oder Pointe erzeugt.

**Beispiel:**

❌ Schlecht: "Die neue Regelung – ohne Vorwarnung angekündigt – betrifft Tausende. Die Änderungen – laut Kritikern überfällig – treten sofort in Kraft."

✓ Besser: "Die neue Regelung wurde ohne Vorwarnung angekündigt und betrifft Tausende. Die Änderungen treten sofort in Kraft, was Kritiker für überfällig halten."

❌ Schlecht: "Danke für die Einführung - ich setze dich auf bcc. Kein Stress - ich brauche nur ein klares Bild."

✓ Besser: "Danke für die Einführung. Ich setze dich auf bcc. Kein Stress, ich brauche nur ein klares Bild."

**Kein Problem, wenn:** Ein einzelner Gedankenstrich pro Absatz als bewusstes Stilmittel dient und sich nicht wiederholt; ein Bindestrich in Komposita, Namen, URLs, IDs oder Produktbezeichnungen steht (`E-Mail`, `Jean-Paul`, `user-id`); ein Bis-Strich echte Bereiche markiert (`2020–2024`).

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

**Lösung:** Mit den verfügbaren Mitteln prüfen (Syntax, Plausibilität, interne Konsistenz, offensichtliche Tippfehler im übergebenen Kontext). Bei nachweisbarem Defekt: korrigieren oder entfernen. Externe Online-Verifikation eines Links liegt außerhalb des Skill-Umfangs – in diesem Fall mit [LINK NICHT VERIFIZIERT] markieren statt blind zu entfernen.

#### 26. Zitatfabrikation und unverifizierbare Referenzen [HIGH]
**Problem:** LLMs erfinden Quellen, die echt aussehen, aber nicht existieren, oder ordnen reale Quellen einer Aussage zu, die sie nicht tragen. Das reicht von ungültigen DOI-/ISBN-Angaben bis zu komplett halluzinierten Publikationen, Aktenzeichen, Gerichtsentscheidungen, URLs oder Studien. Factual Reliability ist hier wichtiger als Stil: Eine polierte Passage mit falscher Quelle ist schlechter als eine sichtbare Lücke.

Häufige Indikatoren:
- DOI mit ungültiger Prüfziffer
- ISBN mit Tippfehler
- Erfundene akademische Quellen (Journal existiert nicht, Ausgabe existiert nicht)
- Autoren existieren, aber die genannte Publikation nicht
- Reale Quelle existiert, enthält aber die behauptete Zahl, Aussage oder das Zitat nicht
- Plausibles Aktenzeichen, Urteil, Gesetz, Studie oder Interview ohne auffindbaren Träger im übergebenen Material
- Defekte externe Links mit `utm_source=`-Parametern – besonders verdächtig: `utm_source=chatgpt.com`, `utm_source=claude.ai`, `utm_source=gemini.google.com`, `utm_source=perplexity.ai` (direkter KI-Fingerabdruck)
- Unbenutzte benannte Referenzen (`<ref name="..."/>` ohne zugehörige Definition)

**Warum LLMs das tun:** Kann keine echten Quellen recherchieren und erzeugt plausibel aussehende Referenzen aus dem Training.

**Lösung:** Jede konkrete Referenz zuerst als ungeprüft behandeln. Mit den verfügbaren Mitteln prüfen: Format, interne Konsistenz, DOI-/ISBN-Prüfziffer, `utm_source`-Fingerabdrücke, Autor-Publikation-Kombinationen, Seiten-/Datumslogik und ob die Quelle im übergebenen Material die konkrete Aussage trägt. Externe Online-Verifikation liegt außerhalb des Skill-Umfangs – in diesem Fall mit [QUELLE NICHT VERIFIZIERT] markieren. Bei nachweisbarer Fabrikation: entfernen. Nie eine Ersatzquelle erfinden oder eine erkannte Falschquelle stilistisch kaschieren.

❌ Schlecht: "Eine Studie von Hartmann und Doyle (2021) zeigt, dass KI-Texte in 87 Prozent der Fälle erkannt werden."

✓ Besser: "Für diese Zahl fehlt im Material eine prüfbare Quelle. [QUELLE NICHT VERIFIZIERT]"

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

### Rhetorik und Struktur (11 Muster)

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

**Problem:** LLMs streuen rhetorische Fragen ein, um Engagement vorzutäuschen. Die Frage wird sofort im nächsten Satz beantwortet – der Leser hatte nie eine echte Wahl, mitzudenken. Anders als Muster 33 (Signposting, das Inhalt ankündigt), simuliert dieses Muster einen Dialog, der keiner ist. Die Frage fügt nichts hinzu; sie verzögert nur die eigentliche Aussage. Verstärkte Form: zwei oder mehr rhetorische Fragen direkt hintereinander ("Funktioniert das? Macht es einen Unterschied? Wer profitiert davon?") – das erzeugt Pseudo-Spannung ohne Informationsgewinn.

**Kein Problem, wenn:** Der Text ein FAQ-Format hat, eine tatsächliche Frage-Antwort-Struktur verfolgt oder der Autor eine provokante These aufstellt, die er dann widerlegt. Eine einzelne, punktuell eingesetzte rhetorische Frage im Blog-/Essay-Stil ist unkritisch.

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

#### 52. Diff-verankertes Schreiben [MEDIUM]

**Kategorie:** Rhetorik und Struktur

**Problem:** Der Text beschreibt eine Änderungsgeschichte statt den aktuellen Sachverhalt. Das ist in Changelogs, Release Notes und Migrationsanleitungen richtig, aber in Dokumentation, Blogtexten, Hilfetexten und Kommentaren wirkt es wie ein Diff-Kommentar, der im eigentlichen Text stehen geblieben ist.

Häufige Indikatoren:
- "wurde jetzt ergänzt"
- "neu hinzugefügt"
- "ersetzt die alte Lösung"
- "bisher war X, nun ist Y"
- "die überarbeitete Version nutzt..."
- "mit diesem Update wird..."

**Warum LLMs das tun:** Modelle bekommen oft Diff-Kontext, Review-Kommentare oder Änderungsaufträge und erzählen danach den Umbau nach, statt die Zielversion als eigenständigen Text zu formulieren.

**Kein Problem, wenn:** Der Text tatsächlich versioniert ist: Changelog, Release Note, Commit-Message, Migration Guide, Review-Kommentar oder redaktionelle Notiz.

**Lösung:** Den Text so schreiben, dass er ohne Kenntnis der letzten Änderung funktioniert. Nicht "was wurde geändert?", sondern "was gilt jetzt?" beantworten.

**Beispiel:**

❌ Schlecht: "Die Plattform wurde jetzt um KI-gestützte Empfehlungen erweitert, die die alte manuelle Auswahl ersetzen."

✓ Besser: "Die Plattform empfiehlt passende Inhalte automatisch auf Basis des Nutzerverhaltens."

#### 56. Aphorismus-Formeln [MEDIUM]

**Kategorie:** Rhetorik und Struktur

**Wendungen, auf die Sie achten sollten:** "X ist die Sprache des Y", "X ist die Währung des Y", "X ist die Architektur des Y", "X wird zur Falle", "X ist kein Werkzeug, sondern ein Spiegel", "im Kern von X steht Y".

**Problem:** LLMs verwandeln eine gewöhnliche Aussage in einen wiederverwendbaren, tiefgründig klingenden Aphorismus. Die Schablone "X ist das Y des Z" suggeriert Bedeutung, fügt aber keine Präzision hinzu – sie ersetzt eine konkrete, prüfbare Behauptung durch eine griffige Leerformel. Solche Sätze lassen sich auf fast jedes Thema anwenden, gerade weil sie nichts Konkretes sagen.

**Warum LLMs das tun:** Aphoristische Formeln sind in zitierfreudigen Trainingsdaten (LinkedIn, Essays, Werbung) überrepräsentiert und gelten als "wertige" Schlusspointe. Das Modell greift sie ab, wenn es eine Aussage gewichtig wirken lassen will.

**Abgrenzung:** Muster 1 = Symbolik-Betonung ("steht als Zeugnis", "symbolisiert"). Muster 2 = Werbesprache/Superlative. Muster 32 = persuasive Autoritäts-Floskeln ("Im Kern", "In Wirklichkeit") als Einschub. Muster 56 = die aphoristische *Schablone* selbst, die eine konkrete Aussage durch eine wohlklingende Formel ersetzt.

**Kein Problem, wenn:** Ein etabliertes Sprichwort oder ein gekennzeichnetes Zitat bewusst eingesetzt wird; die Formulierung eine real belegte, konkrete Aussage trägt und nicht nur den Wohlklang.

**Lösung:** Die Formel durch die konkrete Behauptung ersetzen, auf die sie zielt. Fragen: Was genau wird hier behauptet, und stimmt es?

**Beispiel:**

❌ Schlecht: "Symmetrie ist die Sprache des Vertrauens. Effizienz wird zur Falle, sobald Teams die menschliche Ebene vergessen."

✓ Besser: "Symmetrische Layouts wirken auf Nutzer oft vorhersehbarer. Teams können Abläufe so weit optimieren, dass sie übersehen, wie Menschen sie tatsächlich verwenden."

#### 61. Isometrisches Dokument [MEDIUM]
**Kategorie:** Rhetorik und Struktur
**Problem:** Alle Absätze 3–5 Sätze, alle H2-Sektionen gleich lang, alle Listen-Items in derselben grammatischen Form und Länge, jeder Aspekt bekommt gleich viel Raum. Die Symmetrie überlebt Satz-Edits und ist deshalb ein stärkerer Tell als monotoner Satzbau. Menschliche Texte gewichten ungleich: ausführlich, wo der Autor etwas weiß; knapp, wo nicht.
Häufige Indikatoren:
- Absatzlängen fast konstant (Differenz selten mehr als ein Satz)
- Jede H2-Sektion ähnlich lang, jedes Pro bekommt ein Contra
- Listen, deren Items alle dieselbe Syntax haben ("Verb + Objekt + Nutzen")
**Warum LLMs das tun:** Ausgewogenheit wird im Training belohnt; das Modell verteilt Aufmerksamkeit gleichmäßig statt nach Substanz.
**Kein Problem, wenn:** Format-Konventionen die Gleichform erzwingen (Glossar, Datenblatt, FAQ, juristische Gliederung).
**Lösung:** Gewichtung an Substanz koppeln: die stärkste Sektion ausbauen lassen, die schwächste zusammenziehen oder integrieren (vgl. Muster 44). Listen-Items dürfen unterschiedlich lang sein. Keine Substanz erfinden, nur umverteilen.

#### 62. Markerloser Schließzwang [MEDIUM]
**Kategorie:** Rhetorik und Struktur
**Problem:** Jeder Absatz endet mit einem bewertenden Abschlusssatz, der nichts Neues sagt ("Damit ist die Grundlage gelegt.", "Das zahlt sich langfristig aus.", "So bleibt das System zukunftsfähig.") – Muster 5 ohne dessen Markerphrasen. Die strukturelle Funktion (Absatz "zumachen") ist der Tell, nicht die Wortwahl.
Häufige Indikatoren:
- Letzter Satz des Absatzes wiederholt oder bewertet das bereits Gesagte
- Kein Absatz endet mit einem Fakt, einer offenen Frage oder einem Detail
- Häufung von Zukunfts- oder Nutzen-Floskeln in Schlusssätzen
**Warum LLMs das tun:** Absatz-Kohärenz-Training belohnt explizite Abschlüsse; jeder Absatz wird als Miniatur-Aufsatz behandelt.
**Abgrenzung:** Muster 5 = Markerphrasen ("zusammenfassend", "insgesamt"). Muster 38 = aspirativer Unternehmensschluss am Textende. Muster 62 = der markerlose Bewertungssatz am Absatzende.
**Kein Problem, wenn:** der Schlusssatz eine neue Folgerung zieht oder echte Information ergänzt.
**Lösung:** Streichen. Ein Absatz darf offen enden; der nächste knüpft inhaltlich an (Thema-Rhema statt Schleife).
❌ Schlecht: "Die Migration dauerte sechs Wochen und kostete 40.000 Euro. Damit war ein wichtiger Meilenstein erreicht."
✓ Besser: "Die Migration dauerte sechs Wochen und kostete 40.000 Euro."

### Argumentation und Evidenz (5 Muster)

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

**Abgrenzung – Unpersönlicher Akteur:** Abstrakte Subjekte mit Aktionsverb ("Die Analyse zeigt", "Das Ergebnis belegt", "Die Studie bestätigt") sind kein Passiv und kein subjektloses Fragment – der Akteur ist das abstrakte Nomen. Muster 39 gilt nur bei echtem Passiv oder fehlendem Subjekt; abstrakte Akteure sind unkritisch, solange sie nicht mit Muster 66 (Fake-Analyse-Anhang) kombiniert werden.

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

#### 53. Lückenfüllende Spekulation [HIGH]

**Kategorie:** Argumentation und Evidenz

**Problem:** Wenn eine Quelle fehlt, füllt die KI die Lücke mit plausibel klingendem Fülltext. Besonders bei Personen, kleinen Unternehmen oder historischen Details entstehen dann Sätze über Privatsphäre, Zurückhaltung, wahrscheinliche Herkunft oder mutmaßliche Motive, obwohl der Text eigentlich sagen müsste: nicht belegt.

Häufige Indikatoren:
- "hält sich bedeckt"
- "macht keine Angaben zu seinem Privatleben"
- "meidet die Öffentlichkeit"
- "über die frühen Jahre ist wenig bekannt, was auf eine bewusste Zurückhaltung hindeutet"
- "vermutlich wuchs sie in einem bildungsnahen Umfeld auf"
- "dürfte seine spätere Arbeit geprägt haben"
- "es ist anzunehmen, dass..."

**Abgrenzung:**
- Muster 11 = vage Autorität ohne konkrete Quelle ("Beobachter sagen")
- Muster 19 = Wissensgrenzen-Disclaimer ("Bis zu meinem letzten Update")
- Muster 26 = Quelle ist fabriziert oder formal ungültig
- Muster 42 = Quelle existiert, belegt aber die Aussage nicht
- Muster 53 = Quelle fehlt oder schweigt, und der Text füllt die Lücke mit Spekulation

**Warum LLMs das tun:** Das Modell versucht, eine erwartete Biografie, Projektgeschichte oder Ursachenlogik zu vervollständigen. Wo Daten fehlen, erzeugt es generische Plausibilität.

**Lösung:** Spekulativen Fülltext entfernen oder als unbelegt markieren. Keine Motive, Herkunft oder Persönlichkeitsmerkmale ergänzen, wenn sie nicht im übergebenen Kontext stehen. Wenn die Lücke relevant ist: "Dazu liegen im vorliegenden Material keine Angaben vor." Wenn sie nicht relevant ist: Satz weglassen.

**Beispiel:**

❌ Schlecht: "Über ihre frühen Jahre ist wenig bekannt, was darauf hindeutet, dass sie ihr Privatleben bewusst aus der Öffentlichkeit heraushält. Vermutlich wuchs sie in einem bildungsnahen Umfeld auf, das ihr späteres Engagement prägte."

✓ Besser: "Zu ihren frühen Jahren liegen im vorliegenden Material keine belastbaren Angaben vor."

#### 59. Erfundene Ich-Erfahrung und forcierte Lockerheit [HIGH]
**Kategorie:** Argumentation und Evidenz
**Problem:** Auf "menschlich" getrimmter KI-Text simuliert Persönlichkeit: gestellte Anekdoten ("Als ich letzte Woche mit einem Kunden sprach..."), Pseudo-Nähe ("Ehrlich gesagt", "Keine Sorge", "Spoiler:"), behauptete Praxiserfahrung ohne Träger. Erfundene Erfahrung ist Fabrikation, kein Stilmittel – die Evidenz-Logik von Muster 26/53 gilt analog. Dies ist der Tell zweiter Ordnung: Er entsteht oft erst durch Humanisierungs-Versuche.
Häufige Indikatoren:
- Anekdoten ohne nachprüfbaren Träger ("Ein Kunde erzählte mir neulich...")
- Forcierte Mündlichkeit in Häufung: "Ehrlich gesagt", "Keine Sorge", "Spoiler:", "Na, erkannt?"
- Behauptete Erfahrungsjahre oder Projekthistorie, die nicht aus dem Autorenkontext stammt
**Warum LLMs das tun:** Anweisungen wie "schreib menschlich/persönlich" werden mit erfundener Ich-Evidenz beantwortet, weil persönliche Texte im Training Anekdoten enthalten.
**Abgrenzung:** Muster 18 = Chatbot-Höflichkeit. Muster 53 = Spekulation über Dritte. Muster 59 = erfundene Erfahrung des angeblichen Autors selbst.
**Kein Problem, wenn:** der Autor real existiert und die Erfahrung plausibel seine eigene ist (Schreibprobe, Autorenkontext, explizite Nutzerangabe) – dann nicht anfassen.
**Lösung:** Anekdote entfernen oder durch belegbare Beobachtung ersetzen. Beim eigenen Rewriting im Locker-Modus: Stimme nur aus der Schreibprobe oder explizit gelieferten Fakten speisen, nie generieren.
❌ Schlecht: "Ehrlich gesagt: Als ich letzte Woche ein Kundenprojekt migrierte, ist mir genau das passiert. Keine Sorge, die Lösung ist einfach."
✓ Besser: "Der Fehler tritt typischerweise bei Migrationen auf. Die Lösung: ..."

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
- Invisible Mathematical Operators: Function Application (U+2061), Invisible Times (U+2062), Invisible Separator (U+2063), Invisible Plus (U+2064) - werden teils als KI-Wasserzeichen eingesetzt
- Byte Order Mark (U+FEFF) mitten im Text
- Soft-Hyphen (U+00AD) an ungewöhnlichen Stellen
- Bidi-Steuerzeichen: U+202A-U+202E (Left/Right-to-Left Embedding/Override/Pop), U+2066-U+2069 (Isolates)

**Warum LLMs das tun:** Modelle produzieren gelegentlich Tokens mit unsichtbaren Sonderzeichen. Copy-Paste aus KI-Oberflächen schleppt zusätzliche Formatierungsartefakte mit. Bidi-Controls können auch gezielt zur Verschleierung von Prompt-Inhalten genutzt werden.

**Lösung:** Regex-Scan auf `[\u200B-\u200D\u2060-\u2064\uFEFF\u00AD\u202A-\u202E\u2066-\u2069]` und ersatzlos entfernen. U+2061-U+2064 (Invisible Mathematical Operators: Function Application, Invisible Times, Invisible Separator, Invisible Plus) werden von einigen KI-Tools als unsichtbare Wasserzeichen eingesetzt. Nicht verwechseln mit legitimen Unicode-Gebrauchsfällen: U+00A0 (geschütztes Leerzeichen) in stehenden Wendungen wie „5 km" oder „§ 12" ist korrekt und gehört nicht in dieses Muster.

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

### Typografie und Format (7 Muster)

#### 46. Falsche deutsche Anführungszeichen [HIGH]

**Kategorie:** Typografie

**Problem:** Claude und andere KI-Modelle setzen das schließende deutsche Anführungszeichen systematisch falsch. Korrekt ist: öffnend „ (U+201E, doppeltes tiefes Anführungszeichen) und schließend “ (U+201C, doppeltes oberes Anführungszeichen links). Stattdessen produziert Claude oft ” (U+201D, doppeltes oberes Anführungszeichen rechts) als Schlusszeichen, oder mischt englische Anführungszeichen ein. Dieses Problem ist per Prompt nicht zuverlässig behebbar und erfordert Post-Processing.

Korrekte deutsche Paare:
- Doppelt: „Text“ (U+201E ... U+201C)
- Einfach: ‚Text‘ (U+201A ... U+2018)
- Guillemets DE/AT: »Text« (U+00BB ... U+00AB)
- Guillemets CH: «Text» (U+00AB ... U+00BB)

**Beweiskraft – nur Asymmetrie ist ein KI-Tell:**

- **Harter KI-Tell (Asymmetrie):** deutsches öffnendes „ (U+201E) mit falschem Schlusszeichen.
  - „Text” – deutsches Öffnen, dann U+201D statt U+201C als Schluss
  - „Text" – deutsches Öffnen, dann gerades ASCII (U+0022) als Schluss
  Diese Mischung kommt aus der Zeichenwahl des Modells, nicht aus einem CMS. Als Einzelbefund behandelbar.
- **Kein KI-Tell (CMS/Editor):** durchgängig gerade ASCII-Anführungszeichen ("Text") im ganzen Dokument. Das erzeugen WordPress, Markdown-Export oder Editoren ohne Smart Quotes. Nicht als KI-Signal werten; nur auf Wunsch typografisch glätten.
- **Mehrdeutig:** durchgängig englische Curly Quotes (“Text”). Können Copy-Paste, Tool-Default oder Modell sein. Nur schwaches Indiz im Cluster, nie als Einzelbefund.

Gemischte Stile zählen nur, wenn die Mischung die Asymmetrie oben enthält; bloßes Pendeln zwischen geraden und typografischen Quotes ist Editor-Artefakt, kein Tell.

**Warum LLMs das tun:** Vermutlich Tokenisierung, Post-Processing oder UI-Rendering. Englische Trainingsmaterial dominiert die Zeichenwahl. Per Prompt nicht zuverlässig lösbar.

**Lösung:** Post-Processor/Linter einsetzen. Prüflogik: jedes öffnende „ (U+201E) muss ein schließendes “ (U+201C) haben; jedes öffnende ‚ (U+201A) muss ein schließendes ‘ (U+2018) haben. Gerade Quotes ("...") als "nicht typografisch" markieren. Englische Curly Quotes (“...”) als mehrdeutig flaggen, nicht automatisch als KI-Tell. Gültige Verschachtelung wie „Er sagte: ‚Hallo‘“ nicht als gemischten Stil werten.

#### 47. Englische Titel-Großschreibung [MEDIUM]

**Kategorie:** Typografie

**Problem:** KI überträgt die englische Title-Case-Konvention ins Deutsche: "Die Neue KI Strategie Für Unternehmen". Im Deutschen gilt Satzschreibung: nur das erste Wort und Substantive werden großgeschrieben.

Häufige Indikatoren:
- Adjektive, Verben oder Präpositionen in Überschriften großgeschrieben
- "Der Komplette Leitfaden Für Modernes Marketing"
- "Wie Unternehmen Von KI Profitieren Können"

**Warum LLMs das tun:** Englisches Title Case ist im Trainingsmaterial dominant. Deutsche Überschriften-Konvention wird nicht konsistent gelernt.

**Lösung:** In Überschriften nur Substantive und Satzanfang großschreiben. Prüffrage: Steht hier ein Substantiv, oder wurde ein englisches Muster übernommen?

**Beispiel:**

❌ Schlecht: "Die Zukunft Der Digitalen Transformation Im Mittelstand"

✓ Besser: "Die Zukunft der digitalen Transformation im Mittelstand"

#### 48. Englisches Dezimalformat und Datumsformat [LOW]

**Kategorie:** Typografie

**Problem:** KI verwendet englische Zahlen- und Datumsformate in deutschen Texten.

Häufige Indikatoren:
- Dezimalpunkt statt Komma: "3.5 Prozent" statt "3,5 Prozent"
- Tausenderpunkt fehlt oder falsch: "15000" statt "15.000"
- Englisches Datumsformat: "May 12, 2026" statt "12. Mai 2026"
- Monatsnamen auf Englisch in deutschem Fließtext

**Warum LLMs das tun:** Englische Formatkonventionen aus dem Trainingsmaterial bluten in deutsche Outputs.

**Lösung:** Dezimalkomma verwenden (3,5 statt 3.5). Tausenderpunkt setzen (15.000). Datumsformat: TT. Monat JJJJ.

#### 49. Apostroph-Fehler [MEDIUM]

**Kategorie:** Typografie

**Problem:** KI überträgt den englischen Genitiv-Apostroph ins Deutsche. Im Deutschen steht kein Apostroph vor dem Genitiv-s, außer bei Eigennamen die auf s, x, z, ce enden (dort als Auslassungszeichen).

Häufige Indikatoren:
- "Martin's Profil" statt "Martins Profil"
- "Peter's Projekt" statt "Peters Projekt"
- "das Team's Ergebnis" statt "das Teamergebnis" / "das Ergebnis des Teams"
- Korrektes Apostroph bei: "Hans' Auto", "Marx' Theorie" (Auslassung bei s/x/z-Endung)

**Warum LLMs das tun:** Englisches Possessiv-Apostroph-Muster wird auf deutsche Texte übertragen.

**Lösung:** Genitiv-Apostroph entfernen, außer bei s/x/z/ce-Endungen. Korrektes Zeichen verwenden: ’ (U+2019, typografisches Apostroph), nicht ' (U+0027, gerades Apostroph).

#### 50. Interpunktion bei Stichpunkt-Aufzählungen [LOW]

**Kategorie:** Typografie

**Problem:** KI setzt Punkte ans Ende reiner Stichwort-Aufzählungen und beginnt Stichwörter mit Großbuchstaben, auch wenn es keine vollständigen Sätze sind.

Häufige Indikatoren:
- Punkte am Ende jedes Stichpunkts bei reinen Stichworten
- Großbuchstabe am Anfang, obwohl kein vollständiger Satz
- Inkonsistente Mischung: manche Stichpunkte mit Punkt, manche ohne

Deutsche Konvention:
- Vollständige Sätze: Großbuchstabe + Punkt am Ende
- Stichwörter/Fragmente: Kleinbuchstabe (es sei denn Substantiv), kein Punkt
- Konsistenz innerhalb einer Liste ist wichtiger als die Regel selbst

**Warum LLMs das tun:** Englische Konventionen und inkonsistentes Trainingsmaterial.

**Lösung:** Innerhalb einer Liste konsistent bleiben. Bei reinen Stichworten: kein Punkt am Ende. Nur bei vollständigen Sätzen: Punkt.

#### 51. Obsessive Parataxe [MEDIUM]

**Kategorie:** Stil

**Problem:** KI produziert lange Passagen mit ausschließlich Hauptsätzen gleicher Struktur. Kein Nebensatz, keine Subordination, kein Satzgefüge. Der Text wirkt monoton und roboterhaft, obwohl jeder einzelne Satz korrekt ist.

Häufige Indikatoren:
- 4+ aufeinanderfolgende Hauptsätze ohne Nebensatz
- Alle Sätze beginnen mit Subjekt-Verb
- Gleiche Satzlänge über mehrere Sätze
- Fehlende Konnektoren wie "weil", "obwohl", "damit", "sodass", "nachdem"

**Warum LLMs das tun:** Kurze, klare Hauptsätze erzielen bei Evaluations hohe Lesbarkeits-Scores. Das Modell optimiert auf Verständlichkeit, nicht auf Rhythmus.

**Lösung:** Mindestens jeden dritten Satz als Satzgefüge umbauen (Haupt- + Nebensatz). Variation in Satzlänge und -anfang einführen. Nicht alle Sätze gleich lang machen. **Stilwahl-Carve-out:** Wenn der Autor bewusst kurze, stakkatohafte Hauptsätze als Stilmittel einsetzt (z.B. in Werbe- oder Manifesto-Texten), greift die "Nicht anfassen"-Regel (weiche Musterhäufung, 3+ Mal konsistent).

**Beispiel:**

❌ Schlecht: "Das Team analysierte die Daten. Die Ergebnisse waren eindeutig. Die Conversion stieg um 25 Prozent. Das Projekt wurde im Budget abgeschlossen."

✓ Besser: "Das Team analysierte die Daten und kam zu einem eindeutigen Ergebnis: Die Conversion stieg um 25 Prozent, obwohl das Projekt im Budget blieb."

#### 57. Markdown-Struktur-Artefakte [MEDIUM]

**Problem:** KI-Chatbots setzen Markdown-Strukturelemente dekorativ statt semantisch ein. Drei wiederkehrende Fälle:

- **Fall A – Tabelle, wo Prosa hingehört:** Eine Tabelle mit nur einer Datenzeile, eine Spalte, die einen Wert wiederholt, oder "Aspekt/Beschreibung"-Paare, die in Wahrheit ein Satz sind.
- **Fall B – Übersprungene Überschriften-Ebenen:** Eine H2 folgt direkt eine H4 (`##` dann `####`). Die Überschriftengröße wird als optisches Gewicht missbraucht, nicht als Hierarchie. Überschriften sollten eine Ebene nach der anderen absteigen.
- **Fall C – Thematische Trennlinie vor Überschrift:** Eine dekorative horizontale Linie (`---`) steht direkt über einer Überschrift. Die Überschrift beginnt bereits einen neuen Abschnitt; die Linie ist redundantes Rauschen.

**Warum LLMs das tun:** Modelle optimieren auf optisch "aufgeräumte" Ausgaben und greifen zu Tabellen, Größensprüngen und Trennlinien als visuellen Markern, ohne die zugrunde liegende Dokumentstruktur zu prüfen.

**Kein Problem, wenn:** Eine Tabelle echte mehrdimensionale Daten zeigt; eine `---`-Linie bewusst als Szenen- oder Themenwechsel *zwischen* gleichrangigen Abschnitten steht (nicht direkt vor einer Überschrift); ein CMS, Theme oder Markdown-Template die Struktur erzeugt. Konsistente, korrekte Formatierung allein ist kein KI-Tell.

**Abgrenzung:** Muster 16 = Dash-Satzzeichen und Gedankenstrich-Cluster im Fließtext, nicht die horizontale Linie `---`. Muster 13 = übermäßige Fettschrift, Muster 14 = falsche Listenzeichen. Muster 23 = Markdown statt Wikitext (Syntax-Wahl im Wiki-Kontext). Muster 57 = dekorativer Struktur-Missbrauch in Markdown selbst.

**Beispiel:**

❌ Schlecht (Fall A – Tabelle statt Satz):
> | Funktion | Beschreibung |
> | --- | --- |
> | Geschwindigkeit | Der Dienst antwortet unter normaler Last schnell. |

✓ Besser: "Unter normaler Last antwortet der Dienst schnell."

❌ Schlecht (Fall B – Ebene übersprungen): `## Installation` direkt gefolgt von `#### Voraussetzungen`

✓ Besser: `## Installation` gefolgt von `### Voraussetzungen`

❌ Schlecht (Fall C – Linie vor Überschrift): ein Absatz, dann `---`, dann `## Nächster Abschnitt`

✓ Besser: der Absatz, dann direkt `## Nächster Abschnitt`

### Titel- und Satzbau (2 Muster)

#### 54. Doppelpunkt-Titel-Schema [MEDIUM]

**Problem:** LLMs bauen Titel und Überschriften bevorzugt nach dem Schema "griffige Phrase: erklärender Nachsatz" – links ein Schlagwort oder eine Bedingung, rechts eine "Was/Warum/Wie"-Auflösung (englisch das berüchtigte "X: How Y Changes Z"). Ein einzelner solcher Titel ist unauffällig und oft legitim. Verdächtig wird die Häufung: Wenn H1, Bildunterschrift und mehrere H2 im selben Dokument demselben Doppelpunkt-Schema folgen, entsteht ein mechanischer Rhythmus, den auch statistische Detektoren als "Robotic Formality" markieren.

**Häufige Indikatoren:**
- Doppelpunkt in Titel/H1/H2: links Schlagwort/Bedingung, rechts "Was/Warum/Wie ..."-Erklärung
- 2+ Überschriften im selben Dokument nach demselben Schema
- Der Nachsatz wiederholt teils nur die linke Seite in Langform

**Warum LLMs das tun:** Doppelpunkt-Titel maximieren Klarheit und Klick-Anmutung und sind in SEO- und Blog-Trainingsdaten stark überrepräsentiert.

**Kein Problem, wenn:** Es bei einem einzelnen Doppelpunkt-Titel bleibt; bei etablierter Konvention (wissenschaftlicher Paper-Titel "Hauptthema: Untertitel"); wenn der Nachsatz echte, nicht-redundante Information trägt.

**Abgrenzung:** Muster 34 = generischer Einzeiler *nach* einer Überschrift. Muster 47 = englische Titel-Großschreibung. Muster 54 = die gehäufte Doppelpunkt-*Konstruktion* selbst.

**Fix-Aktion (Minimalintervention, ab 2+ Doppelpunkt-Titeln im Dokument):** Erst ab dem zweiten gleichartig gebauten Titel eingreifen – ein einzelner Doppelpunkt-Titel bleibt unangetastet. Strategie: im Cluster *variieren*, nicht alle gleich umbauen. Optionen: Überschrift als Aussage formulieren, auf die Kernaussage kürzen, Untertitel in Klammern setzen oder Titel ohne zweiteilige Schablone neu bauen, sofern dabei keine Information verloren geht. Nie alle Doppelpunkte mechanisch gegen Gedankenstriche tauschen – das erzeugt nur ein neues, monotones Schema.

Den Subtitel/Nachsatz *nicht* entfernen, solange er echte, nicht-redundante Information trägt. Entfernen nur, wenn der Nachsatz die linke Seite nur in Langform wiederholt (z. B. „Datenschutz: Datenschutz richtig gemacht") oder eine leere Formel ist (z. B. „Alles, was du wissen musst" ohne konkreten Bezug).

**Nicht anfassen:** wissenschaftliche Haupttitel mit Untertitel, Serien-/Rubriktitel, FAQ-/Glossar-/Definitionstitel, juristische oder technische Labels, echte Zitattitel, Interview-/Q&A-Labels, UI-/Formularlabels, Quellen-/Bildnachweise, Zeit-/Ortslabels.

**Beispiel:**

❌ Schlecht (drei Überschriften desselben Texts, alle gleich gebaut):
- "Wenn KI mitliest: Warum regulierte Branchen umdenken müssen"
- "Die zweite Zeitbombe: veraltete Archive als Weltwissen"
- "Interpretationsstabilität: Was KI-Kompression aus Fachtexten macht"

✓ Besser (Schema aufbrechen, Varianz zulassen – ein Doppelpunkt unter dreien ist unkritisch):
- "Warum regulierte Branchen ihre Inhalte für KI umdenken müssen"
- "Veraltete Archive: die zweite Zeitbombe"
- "Wie KI-Kompression Warnhinweise aus Fachtexten entfernt"

#### 55. Gleichförmiger Satzrhythmus [MEDIUM]

**Kategorie:** Stil

**Problem:** Die Sätze schwanken kaum in Länge und Bau. Die meisten liegen im selben Wortfenster (oft 10–18 Wörter), beginnen mit dem Subjekt und folgen Subjekt-Verb-Objekt. Es fehlt der Wechsel zwischen einem sehr kurzen Satz und einem langen, gegliederten. Der Text ist dadurch korrekt und gut lesbar, aber metrisch monoton. Statistische Detektoren (GPTZero u. a.) messen diese fehlende Varianz als niedrige "Burstiness" und werten sie als KI-Signal – gemeldet als "Lacks Creative Grammar" oder "Mechanical Writing".

**Abgrenzung zu Muster 51 (Obsessive Parataxe):** Muster 51 trifft Texte aus ausschließlich kurzen Hauptsätzen ohne Subordination. Muster 55 ist breiter und greift auch bei syntaktisch komplexen Texten: Die Sätze sind unterschiedlich gebaut, aber alle ungefähr gleich lang und gleich eingeleitet. Ein Text kann Muster 55 zeigen, ohne Muster 51 zu zeigen.

**Häufige Indikatoren:**
- Mehrere aufeinanderfolgende Sätze im engen Längenfenster (Differenz selten > 5 Wörter)
- Überwiegend gleicher Satzanfang (Subjekt zuerst)
- Kein bewusst kurzer Pointe-Satz neben einem langen Schachtelsatz

**Warum LLMs das tun:** Das Sampling tendiert zur mittleren Satzlänge; das Modell reguliert sich auf eine gleichmäßige Kadenz, weil mittellange Sätze die statistisch sichere Wahl sind.

**Lösung:** Satzlänge bewusst spreizen – gelegentlich ein sehr kurzer Satz (3–5 Wörter) neben einem langen, gegliederten. Satzanfänge variieren (Adverbiale, vorangestellter Nebensatz, Subjekt). Es geht um Varianz, nicht um Fehler: keine Grammatik brechen, keine Substanz ändern, nur die Kadenz auflockern.

**Wichtig – nicht übersteuern:** Sachliche Gleichförmigkeit ist in Fachtexten oft korrekt und gewollt. Behandle dieses Muster nur, wenn (a) der Nutzer ausdrücklich Detektor-Resilienz wünscht oder (b) die Monotonie die Lesbarkeit spürbar beeinträchtigt. Im Formal-Modus überspringen, wenn die Gleichförmigkeit fachkonventionell ist. Nie Substanz, Register oder Präzision opfern, nur um einen Detektor-Score zu senken.

**Beispiel:**

❌ Schlecht (vier Sätze, alle 8–12 Wörter, Subjekt zuerst):
"Viele Fachtexte sind korrekt, solange man sie vollständig liest. Ein Nebensatz schränkt die Aussage ein. Eine Fußnote ordnet den Befund ein. Der Kontext trennt Prävention von Therapie."

✓ Besser (Längen gespreizt, Anfänge variiert):
"Viele Fachtexte sind korrekt – solange man sie ganz liest. Ein Nebensatz hier, eine Fußnote dort, und plötzlich trennt der Kontext Prävention von Therapie. Lässt man ihn weg, kippt die Aussage."
