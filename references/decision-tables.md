# Humanizer-de Decision Tables

Nutze diese Tabellen vor `references/patterns.md`, wenn Befunde ueberlappen. Sie sind die verbindliche Kurzlogik fuer v5.8.0.

## QGIR: Moduswahl

| Situation | Aktion |
|---|---|
| Text ist sauber oder hat nur Einzelsignale | Audit-only; nicht umschreiben |
| Echte HIGH/MEDIUM-Cluster, geringe Drift-Gefahr | Minimal revise; ein lokaler Pass |
| Nach Minimal-Revision bleiben echte HIGH/MEDIUM-Cluster | QGIR mit max. 2 Paessen |
| Dritter Pass waere noetig | Nur bei dokumentiertem schweren Restcluster |
| Quelle, Recht, Technik, Formalregister oder Zielprofil waere gefaehrdet | Stop; Befund markieren |
| Ziel waere nur Detektorwirkung, Score oder maximale Glattheit ohne Qualitaetsgewinn | Stop; nicht optimieren |

## Evidenz: 11 / 25 / 26 / 42 / 53

| Situation | Muster | Aktion |
|---|---:|---|
| Keine konkrete Quelle, nur "Studien zeigen", "Beobachter sagen", "Experten meinen" | 11 | Zuschreibung entfernen oder `[ECHTE QUELLE NOETIG]` markieren |
| Link sieht konkret aus, ist aber defekt oder im Material nicht pruefbar | 25 | `[LINK NICHT VERIFIZIERT]` markieren; nicht blind loeschen, wenn externe Pruefung fehlt |
| Quelle sieht konkret aus, ist aber formal ungueltig, erfunden, unverifizierbar oder mit KI-Tracking-Artefakt versehen | 26 | Entfernen oder `[QUELLE NICHT VERIFIZIERT]`; keine Ersatzquelle erfinden |
| Quelle existiert und wurde geprueft, belegt die konkrete Aussage aber nicht | 42 | Aussage an Quelle anpassen, Quelle ersetzen oder `[BELEG PRUEFEN]` |
| Quelle fehlt oder schweigt, Text ergaenzt Motive, Herkunft, Privatleben oder Plausibilitaet | 53 | Spekulation entfernen oder "keine Angaben im Material" schreiben |
| Quelle ist nicht pruefbar | nicht 42 | Keine Beleginkongruenz behaupten; 26/53 nur bei eigenen Indikatoren |

## Claim-Delta: Faktenanker

| Situation | Aktion |
|---|---|
| Zahl, Datum, URL, DOI, Paragraph, Code oder direktes Zitat verschwindet oder aendert sich | Blocken oder explizit mit Quelle/Input begruenden |
| Neuer konkreter Name, Ort, Zeitraum, Betrag, Prozentwert oder Erfahrungsanker entsteht | Blocken, wenn nicht im Input/Kontext belegt |
| Satz wird geteilt oder zusammengezogen, alle Faktenanker bleiben erhalten | Erlaubt |
| Floskel wird gestrichen, Aussage und Autoritaetsgrad bleiben gleich | Erlaubt |
| "vermutlich/kann/laut" wird zu "zeigt/beweist/muss" | Blocken: Autoritaetsgrad nicht staerken |

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

## Floskeln und Schablonen: 1 / 2 / 32 / 56 / 58 / 60 / 64 / 65

| Situation | Muster | Aktion |
|---|---:|---|
| Symbolisierende Aufladung ("steht als Zeugnis", "symbolisiert") | 1 | Umformulieren auf die konkrete Aussage |
| Werbesprache oder Superlative ("atemberaubend", "einzigartig") | 2 | Entfernen oder sachlich ersetzen |
| Persuasive Einschub-Floskel ("Im Kern", "In Wirklichkeit") | 32 | Floskel streichen, Aussage direkt stellen |
| Aphoristische Schablone ersetzt eine konkrete Behauptung ("X ist die Sprache des Y", "X wird zur Falle") | 56 | Durch die gemeinte konkrete Behauptung ersetzen |
| Hypernym/Nominalstil ersetzt eine im Text belegte Konkretion | 58 | Konkretisieren aus Text/Kontext oder `[KONKRETION NOETIG]`; nichts erfinden |
| Rotierende Bezeichnungen fuer denselben Referenten | 60 | Grundwort + Pronomen; max. eine Beiname-Variante mit Mehrwert |
| Frequenz-Marker-Vokabeln in Haeufung ("beleuchten", "spannend", "nahtlos", "Landschaft" figurativ) | 64 | Durch gewoehnliches Wort ersetzen; fachgebundene Verwendung stehen lassen |
| Ersatzkonstruktion statt "ist"/"hat" ("fungiert als", "verfuegt ueber") in Haeufung | 65 | Auf Kopula zurueckfuehren, wenn keine Information verloren geht |
| Symbolische Aufladung statt nuechterner Ersatzkonstruktion | 1, nicht 65 | Siehe Muster 1 |
| Relativsatz/Anschlusskonstruktion ohne neue Information ("was X unterstreicht/verdeutlicht") | 66 | Loeschtest: Faellt der Anhang weg ohne Informationsverlust? Dann streichen |
| Relativsatz traegt echte, im Hauptsatz nicht enthaltene Information | nicht 66 | Stehen lassen oder als eigenstaendigen Satz formulieren |
| Gekennzeichnetes Zitat oder belegte konkrete Aussage | nicht 56 | Stehen lassen |

## Kontrastformeln: 7 / 8 / 16 / 56

| Situation | Muster | Aktion |
|---|---:|---|
| Wiederholte oder funktionsarme Pointe „nicht (nur) X, sondern Y", „kein X. Sondern Y." | 8 | Kontrastschema auf die konkrete Aussage zurückführen |
| Sachliche Korrektur („nicht Montag, sondern Dienstag") oder einzelne begründete Antithese | nicht 8 | Stehen lassen |
| Dash-Cluster ohne Kontrastschema | 16 | Satzbau nach Ersetzungshierarchie lösen |
| Kontrastformel mit einem einzelnen Dash, sonst kein Dash-Cluster | 8, nicht 16 | Einmal nach dem primären Mechanismus behandeln |
| Konzessive Dichotomie „Trotz X … Y" | 7 | Aussage konkret statt symmetrisch führen |
| Aphoristische Metapher „kein Werkzeug, sondern ein Spiegel" | 56 | Durch die gemeinte konkrete Behauptung ersetzen |

## Explainer-Signposts: 5 / 33 / 34 / 35 / 44 / 54 / 57

| Situation | Muster | Aktion |
|---|---:|---|
| „Warum das wichtig ist:" / „Das große Bild:" als Fließtext-Ankündigung | 33 | Label streichen und Aussage direkt beginnen |
| Generischer Einzeiler direkt nach einer Überschrift oder einem solchen Label | 34 | Entfernen oder in den nächsten Absatz integrieren |
| „Warum ist das wichtig?" mit sofortiger eigener Antwort | 35 | Frage entfernen und Antwort direkt formulieren |
| Konkrete, inhaltstragende Explainer-Sektion | nicht 33/34/35 | Stehen lassen |
| „Kurz gesagt" fasst im Absatz nur Vorheriges zusammen | 5, nicht 33 | Zusammenfassung streichen oder mit neuer Substanz verbinden |
| Substanzlose Standardsektion, Doppelpunkt-Titel oder Inline-Label-Liste | 44 / 54 / 57 | Nach dem jeweiligen Strukturmechanismus behandeln |

## Evidenz zweiter Ordnung: 59

| Situation | Muster | Aktion |
|---|---:|---|
| Anekdote/Ich-Erfahrung ohne Traeger im Autorenkontext | 59 | Entfernen oder durch belegbare Beobachtung ersetzen |
| Erfahrung plausibel vom realen Autor (Schreibprobe/Nutzerangabe) | nicht 59 | Stehen lassen |

## Format und Markdown: 13 / 14 / 16 / 23 / 57

| Situation | Muster | Aktion |
|---|---:|---|
| Gedankenstriche oder Dash-Ersatz als Satzzeichen (`—`, `–`, ` -- `, ` - `) im Cluster | 16 | Nicht Glyph tauschen; Satzbau mit Punkt, Komma, Doppelpunkt, Semikolon, Klammer oder Streichung loesen |
| Einzelner bewusst gesetzter Gedankenstrich ohne weitere Muster | nicht 16 | Stehen lassen |
| Bindestrich in Komposita, Namen, URLs, IDs oder echter Bereichsstrich | nicht 16 | Stehen lassen |
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

## Profil-Konflikte

| Konflikt | Vorrang |
|---|---|
| Quelle vs. schoener Stil | Quelle |
| Recht/Technik vs. Rhythmus | Recht/Technik |
| Formal-Modus vs. Schreibprobe | Formal-Modus |
| Zielprofil vs. generische Lockerheit | Zielprofil |
| Terminologiekonsistenz vs. Synonymvariation | Terminologiekonsistenz |
