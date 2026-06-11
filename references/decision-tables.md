# Humanizer-de Decision Tables

Nutze diese Tabellen vor `references/patterns.md`, wenn Befunde ueberlappen. Sie sind die verbindliche Kurzlogik fuer v3.8.0-de.1.

## Evidenz: 11 / 26 / 42 / 53

| Situation | Muster | Aktion |
|---|---:|---|
| Keine konkrete Quelle, nur "Studien zeigen", "Beobachter sagen", "Experten meinen" | 11 | Zuschreibung entfernen oder `[ECHTE QUELLE NOETIG]` markieren |
| Quelle sieht konkret aus, ist aber formal ungueltig, erfunden oder mit KI-Tracking-Artefakt versehen | 26 | Entfernen oder `[QUELLE NICHT VERIFIZIERT]`; keine Ersatzquelle erfinden |
| Quelle existiert und wurde geprueft, belegt die konkrete Aussage aber nicht | 42 | Aussage an Quelle anpassen, Quelle ersetzen oder `[BELEG PRUEFEN]` |
| Quelle fehlt oder schweigt, Text ergaenzt Motive, Herkunft, Privatleben oder Plausibilitaet | 53 | Spekulation entfernen oder "keine Angaben im Material" schreiben |
| Quelle ist nicht pruefbar | nicht 42 | Keine Beleginkongruenz behaupten; 26/53 nur bei eigenen Indikatoren |

## Struktur: 5 / 6 / 34 / 44 / 61 / 62

| Situation | Muster | Aktion |
|---|---:|---|
| Schluss- oder Zusammenfassungsphrase im Absatz | 5 | Satz umformulieren oder entfernen, Substanz erhalten |
| Explizite `Fazit`-/`Zusammenfassung`-Sektion im falschen Kontext | 6 | Sektion integrieren oder entfernen, wenn sie artefaktisch ist |
| Generischer Einzeiler direkt nach einer Ueberschrift | 34 | Entfernen oder in den naechsten Absatz integrieren |
| Ganzer Standardabschnitt mit Allgemeinplaetzen ohne konkrete Substanz | 44 | Konkretisieren, integrieren, umwidmen oder `[SUBSTANZ PRUEFEN]` |
| Absaetze/Sektionen/Listen durchgehend gleich lang und symmetrisch | 61 | Gewichtung an Substanz koppeln; umverteilen, nichts erfinden |
| Bewertender Abschlusssatz ohne neue Information am Absatzende | 62 | Streichen; Absatz darf offen enden |
| Schlusssatz zieht echte neue Folgerung | nicht 62 | Stehen lassen |
| Kurzer Einstieg enthaelt konkrete Zahl, Datum oder These | nicht 34 | Stehen lassen |
| Standard-Ueberschrift mit belegtem, konkretem Inhalt | nicht 44 | Stehen lassen oder nur Ueberschrift praezisieren |

## Floskeln und Schablonen: 1 / 2 / 32 / 56 / 58 / 60

| Situation | Muster | Aktion |
|---|---:|---|
| Symbolisierende Aufladung ("steht als Zeugnis", "symbolisiert") | 1 | Umformulieren auf die konkrete Aussage |
| Werbesprache oder Superlative ("atemberaubend", "einzigartig") | 2 | Entfernen oder sachlich ersetzen |
| Persuasive Einschub-Floskel ("Im Kern", "In Wirklichkeit") | 32 | Floskel streichen, Aussage direkt stellen |
| Aphoristische Schablone ersetzt eine konkrete Behauptung ("X ist die Sprache des Y", "X wird zur Falle") | 56 | Durch die gemeinte konkrete Behauptung ersetzen |
| Hypernym/Nominalstil ersetzt eine im Text belegte Konkretion | 58 | Konkretisieren aus Text/Kontext oder `[KONKRETION NOETIG]`; nichts erfinden |
| Rotierende Bezeichnungen fuer denselben Referenten | 60 | Grundwort + Pronomen; max. eine Beiname-Variante mit Mehrwert |
| Gekennzeichnetes Zitat oder belegte konkrete Aussage | nicht 56 | Stehen lassen |

## Evidenz zweiter Ordnung: 59

| Situation | Muster | Aktion |
|---|---:|---|
| Anekdote/Ich-Erfahrung ohne Traeger im Autorenkontext | 59 | Entfernen oder durch belegbare Beobachtung ersetzen |
| Erfahrung plausibel vom realen Autor (Schreibprobe/Nutzerangabe) | nicht 59 | Stehen lassen |

## Format und Markdown: 13 / 14 / 16 / 23 / 57

| Situation | Muster | Aktion |
|---|---:|---|
| Gedankenstriche (— / –) im Fließtext | 16 | Reduzieren, gepaarte Einschübe aufloesen |
| Übermäßige Fettschrift / falsche Listenzeichen | 13 / 14 | Fett sparsam; korrekte Listensyntax |
| Markdown-Syntax statt Wikitext im Wiki-Kontext | 23 | In Wikitext umsetzen |
| Dekorative Tabelle, übersprungene Heading-Ebene oder `---` direkt vor Überschrift | 57 | In Prosa/korrekte Hierarchie aufloesen; Linie vor Überschrift entfernen |
| Echte mehrdimensionale Daten, bewusster `---`-Szenenwechsel, CMS/Theme-Struktur | nicht 57 | Stehen lassen |

## Modusmatrix

| Musterklasse | Locker | Sachlich | Formal |
|---|---|---|---|
| HIGH Artefakt, Chatbot, Technik | aendern/entfernen | aendern/entfernen | aendern/entfernen |
| HIGH Evidenz/Quelle | markieren oder korrigieren | markieren oder korrigieren | markieren oder korrigieren |
| HIGH Stil | aendern | aendern | nur wenn nicht fachkonventionell; Muster 10 ueberspringen |
| MEDIUM technische/strukturelle Befunde | aendern | aendern | markieren oder vorsichtig aendern |
| MEDIUM weiche Stilbefunde | bei Haeufung/Cluster aendern | bei Haeufung/klarer Mechanik aendern | meist nur markieren |
| LOW Format/Interpunktion | aendern, wenn stoerend | aendern, wenn klarer Regelverstoss | meist ueberspringen oder markieren |
| Stimme einbringen | voll | dezent | nie |

Muster 45: False Friends immer korrigieren. Calques und syntaktische Transfers im Formal-Modus korrigieren; in Sachlich/Locker nur bei Haeufung oder auffaelliger Woertlichkeit.
