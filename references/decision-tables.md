# Humanizer-de Decision Tables

Nutze diese Tabellen vor `references/patterns.md`, wenn Befunde überlappen. Sie sind die verbindliche Kurzlogik für v5.22.0.

## QGIR: Moduswahl

| Situation | Aktion |
|---|---|
| Text ist sauber oder hat nur Einzelsignale | Audit-only; nicht umschreiben |
| Echte HIGH/MEDIUM-Cluster, geringe Drift-Gefahr | Minimal revise; ein lokaler Pass |
| Nach Minimal-Revision bleiben echte HIGH/MEDIUM-Cluster | QGIR mit max. 2 Pässen |
| Dritter Pass wäre nötig | Nur bei dokumentiertem schweren Restcluster |
| Quelle, Recht, Technik, Formalregister oder Zielprofil wäre gefährdet | Stop; Befund markieren |
| Ziel wäre nur Detektorwirkung, Score oder maximale Glattheit ohne Qualitätsgewinn | Stop; nicht optimieren |

## Evidenz: 11 / 25 / 26 / 42 / 53

| Situation | Muster | Aktion |
|---|---:|---|
| Keine konkrete Quelle, nur "Studien zeigen", "Beobachter sagen", "Experten meinen" | 11 | Zuschreibung entfernen oder `[ECHTE QUELLE NOETIG]` markieren |
| Link sieht konkret aus, ist aber defekt oder im Material nicht prüfbar | 25 | `[LINK NICHT VERIFIZIERT]` markieren; nicht blind löschen, wenn externe Prüfung fehlt |
| Quelle sieht konkret aus, ist aber formal ungültig, erfunden, unverifizierbar oder mit KI-Tracking-Artefakt versehen | 26 | Entfernen oder `[QUELLE NICHT VERIFIZIERT]`; keine Ersatzquelle erfinden |
| Quelle existiert und wurde geprüft, belegt die konkrete Aussage aber nicht | 42 | Aussage an Quelle anpassen, Quelle ersetzen oder `[BELEG PRUEFEN]` |
| Quelle fehlt oder schweigt, Text ergänzt Motive, Herkunft, Privatleben oder Plausibilität | 53 | Spekulation entfernen oder "keine Angaben im Material" schreiben |
| Quelle ist nicht prüfbar | nicht 42 | Keine Beleginkongruenz behaupten; 26/53 nur bei eigenen Indikatoren |

## Claim-Delta: Faktenanker

| Situation | Aktion |
|---|---|
| Zahl, Datum, URL, DOI, Paragraph, Code oder direktes Zitat verschwindet oder ändert sich | Blocken oder explizit mit Quelle/Input begründen |
| Neuer konkreter Name, Ort, Zeitraum, Betrag, Prozentwert oder Erfahrungsanker entsteht | Blocken, wenn nicht im Input/Kontext belegt |
| Satz wird geteilt oder zusammengezogen, alle Faktenanker bleiben erhalten | Erlaubt |
| Floskel wird gestrichen, Aussage und Autoritätsgrad bleiben gleich | Erlaubt |
| "vermutlich/kann/laut" wird zu "zeigt/beweist/muss" | Blocken: Autoritätsgrad nicht stärken |

## Struktur: 5 / 6 / 34 / 44 / 61 / 62

| Situation | Muster | Aktion |
|---|---:|---|
| Schluss- oder Zusammenfassungsphrase im Absatz | 5 | Satz umformulieren oder entfernen, Substanz erhalten |
| Explizite `Fazit`-/`Zusammenfassung`-Sektion im falschen Kontext | 6 | Sektion integrieren oder entfernen, wenn sie artefaktisch ist |
| Generischer Einzeiler direkt nach einer Überschrift | 34 | Entfernen oder in den nächsten Absatz integrieren |
| Ganzer Standardabschnitt mit Allgemeinplätzen ohne konkrete Substanz | 44 | Konkretisieren, integrieren, umwidmen oder `[SUBSTANZ PRUEFEN]` |
| Absätze/Sektionen/Listen durchgehend gleich lang und symmetrisch | 61 | Gewichtung an Substanz koppeln; umverteilen, nichts erfinden |
| Bewertender Abschlusssatz ohne neue Information am Absatzende | 62 | Streichen; Absatz darf offen enden |
| Schlusssatz zieht echte neue Folgerung | nicht 62 | Stehen lassen |
| Kurzer Einstieg enthält konkrete Zahl, Datum oder These | nicht 34 | Stehen lassen |
| Standard-Überschrift mit belegtem, konkretem Inhalt | nicht 44 | Stehen lassen oder nur Überschrift präzisieren |

## Floskeln und Schablonen: 1 / 2 / 32 / 56 / 58 / 60 / 64 / 65

| Situation | Muster | Aktion |
|---|---:|---|
| Symbolisierende Aufladung ("steht als Zeugnis", "symbolisiert") | 1 | Umformulieren auf die konkrete Aussage |
| Werbesprache oder Superlative ("atemberaubend", "einzigartig") | 2 | Entfernen oder sachlich ersetzen |
| Persuasive Einschub-Floskel ("Im Kern", "In Wirklichkeit") | 32 | Floskel streichen, Aussage direkt stellen |
| Aphoristische Schablone ersetzt eine konkrete Behauptung ("X ist die Sprache des Y", "X wird zur Falle") | 56 | Durch die gemeinte konkrete Behauptung ersetzen |
| Hypernym/Nominalstil ersetzt eine im Text belegte Konkretion | 58 | Konkretisieren aus Text/Kontext oder `[KONKRETION NOETIG]`; nichts erfinden |
| Rotierende Bezeichnungen für denselben Referenten | 60 | Grundwort + Pronomen; max. eine Beiname-Variante mit Mehrwert |
| Frequenz-Marker-Vokabeln in Häufung ("beleuchten", "spannend", "nahtlos", "Landschaft" figurativ) | 64 | Durch gewöhnliches Wort ersetzen; fachgebundene Verwendung stehen lassen |
| Ersatzkonstruktion statt "ist"/"hat" ("fungiert als", "verfügt über") in Häufung | 65 | Auf Kopula zurückführen, wenn keine Information verloren geht |
| Symbolische Aufladung statt nüchterner Ersatzkonstruktion | 1, nicht 65 | Siehe Muster 1 |
| Relativsatz/Anschlusskonstruktion ohne neue Information ("was X unterstreicht/verdeutlicht") | 66 | Löschtest: Fällt der Anhang weg ohne Informationsverlust? Dann streichen |
| Relativsatz trägt echte, im Hauptsatz nicht enthaltene Information | nicht 66 | Stehen lassen oder als eigenständigen Satz formulieren |
| Gekennzeichnetes Zitat oder belegte konkrete Aussage | nicht 56 | Stehen lassen |

Der Slot-Test ist eine Diagnose, keine Muster-Zuordnung: Wirkt ein Satz wie eine Schablone, die
Substantive themenfremd ersetzen. Funktioniert der Satz unverändert, anschließend Muster 2, 12,
56, 58 oder 64 prüfen.

## Anglizismus-Strukturen und Korrektorat: 45

| Situation | Aktion |
|---|---|
| False Friend verändert die Bedeutung | Immer als Muster 45 korrigieren |
| Mehrere wörtlich englische Kollokationen oder Syntaximporte im deutschen Fließtext | Als M45-Cluster lokal auf natürliches Deutsch zurückführen |
| Englischer Genitiv verbindet Anbieter und Produkt in einem deutschen Satz | Deutsche Attribution verwenden; offiziellen Produktnamen erhalten |
| Einzelner etablierter Fachanglizismus oder offizieller englischer Produktstring | Kein M45-Befund; stehen lassen |
| Komma-, Genus- oder Flexionsfehler ohne englischen Transfer | Korrektorat, keine neue Muster-ID und keine Autorschaftsaussage |
| Sammelcheck ist grün, der Text enthält aber ein belegtes M45-Cluster | Urteilsbasiert lokal redigieren; Linter-Stille nicht als Naturalness-Beweis behandeln |

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

## Retroaktive Scheinnuance: 32 / 33 / 41 / 66 / 71

| Situation | Muster | Aktion |
|---|---:|---|
| Nachsatz kündigt Präzision an, bringt aber keine neue Bedingung, Teilmenge, Ursache, Kennzahl, Ausnahme oder Gegenposition | 71 | Neuigkeits- und Löschtest anwenden; echte Präzision liefern oder Nachsatz streichen |
| Autoritätsfloskel rahmt eine angeblich tiefere Sicht („In Wirklichkeit ...") | 32, nicht 71 | Rahmung streichen und Aussage direkt stellen |
| Ankündigung beschreibt den kommenden Aufbau | 33, nicht 71 | Meta-Ankündigung streichen; Muster 71 blickt auf eine bereits gemachte Aussage zurück |
| Sicherheitsgrad ist falsch kalibriert | 41 | Anspruch verengen oder Unsicherheit konkret benennen; Muster 71 kann korrekt kalibriert und trotzdem leer sein |
| Funktionsleerer Relativsatz-Nachklapp hängt im selben Satz | 66, nicht 71 | Nachklapp per Löschtest entfernen |

## Syntaktische Ankündigung, Komparativ-Rahmung und Locker-Architektur: 67 / 68 / 69

| Situation | Muster | Aktion |
|---|---:|---|
| Spaltsatz kündigt eine einfache Aussage als Erkenntnismoment an („Was auffiel, war ...") | 67 | Aussage direkt formulieren; bei Einzelvorkommen und echter Informationsstruktur stehen lassen |
| Meta-Ankündigung nutzt Signal-Vokabular („Schauen wir uns an", „Hier ist, was Sie wissen müssen") | 33, nicht 67 | Meta-Vorspann streichen und Inhalt direkt beginnen |
| Autoritäts-Floskel rahmt eine vermeintlich tiefere Einsicht („Die eigentliche Frage ist") | 32, nicht 67 | Floskel streichen; Aussage direkt stellen |
| Vergleichs- oder Abstufungsschablone ersetzt die direkte Beschreibung („weniger X als vielmehr Y") | 68 | Versteckte konkrete Aussage direkt formulieren |
| Verneinungs- oder Spiegel-Parallelismus trägt die Pointe | 8, nicht 68 | Kontrastschema auf die konkrete Aussage zurückführen |
| Figurative Spannweite nutzt „von ... bis" | 12, nicht 68 | Spannweite durch konkrete Menge oder Beschreibung ersetzen |
| Lockere Marker liegen über polierter Satz- und Absatzarchitektur | 69 | Schreibprobe und Format prüfen; Architektur nur aus gelieferten Fakten lockern |
| Auffälligkeit liegt auf Wortebene bei Partikelarmut oder -überdosis | 63, nicht 69 | Nach Partikel- und Moduslogik behandeln |
| Lockerheit beruht auf erfundener Erfahrung oder forcierter Mündlichkeit | 59, nicht 69 | Persona-Lock anwenden; erfundene Erfahrung entfernen |
| Register oder Stimme wechseln zwischen Absätzen | 30, nicht 69 | Wechsel angleichen; nicht pauschal die Architektur lockern |

## Register: Anrede

| Situation | Aktion |
|---|---|
| `du` und echte höfliche `Sie`-Anrede in der Autorenstimme | `mixed_address` bestätigen und Anrede vereinheitlichen |
| Großes `Sie` als Singular-Anapher oder in eindeutig gepaartem Inline-Zitat/Blockquote | Mit aktivem `--precise` ausblenden; kein Registerwechsel |
| Großes `Sie` als mögliche Plural-Anapher | Manuell prüfen; nicht automatisch umschreiben |

## Evidenz zweiter Ordnung: 59

| Situation | Muster | Aktion |
|---|---:|---|
| Anekdote/Ich-Erfahrung ohne Träger im Autorenkontext | 59 | Entfernen oder durch belegbare Beobachtung ersetzen |
| Erfahrung plausibel vom realen Autor (Schreibprobe/Nutzerangabe) | nicht 59 | Stehen lassen |

## Zuschreibung und Erleben: 18 / 53 / 59 / 72

| Situation | Muster | Aktion |
|---|---:|---|
| Austauschbare Höflichkeits- oder Hilfsgeste | 18 | Floskel entfernen und beim Inhalt beginnen |
| Unbelegte Spekulation über Dritte | 53 | Spekulation entfernen oder Lücke markieren |
| Erfundene Erfahrung des angeblichen Autors | 59 | Persona-Lock anwenden; Erfahrung entfernen oder belegen |
| Unbelegte Diagnose über Gefühle, Selbstbild oder Vorgeschichte des Adressaten | 72 | Diagnose streichen und belegbaren Sachkern nennen |
| Adressat hat das Gefühl selbst genannt oder Beratung/Coaching ist belegt der Auftrag | nicht 72 | Ohne Verstärkung aufgreifen; Kontext erhalten |

## Akteursrolle: 39 / 70

| Situation | Muster | Aktion |
|---|---:|---|
| Passiv oder fehlendes Subjekt verschleiert den Akteur | 39 | Belegten Akteur einsetzen; im Formal-Modus Fachkonvention beachten |
| Aktiver Satz besetzt eine Entscheidungs- oder Verantwortungsrolle mit einem ungeeigneten Abstraktum | 70 | Belegten Akteur einsetzen und Abstraktum als Grundlage, Anlass oder Maßstab führen |
| Fachübliche Metonymie oder technisches Funktionssubjekt („Die Studie zeigt", „Das System speichert") | kein Befund | Stehen lassen |

## Format und Markdown: 13 / 14 / 16 / 23 / 57

| Situation | Muster | Aktion |
|---|---:|---|
| Gedankenstriche oder Dash-Ersatz als Satzzeichen (`—`, `–`, ` -- `, ` - `) im Cluster | 16 | Nicht Glyph tauschen; Satzbau mit Punkt, Komma, Doppelpunkt, Semikolon, Klammer oder Streichung lösen |
| Einzelner bewusst gesetzter Gedankenstrich ohne weitere Muster | nicht 16 | Stehen lassen |
| Bindestrich in Komposita, Namen, URLs, IDs oder echter Bereichsstrich | nicht 16 | Stehen lassen |
| Übermäßige Fettschrift / falsche Listenzeichen | 13 / 14 | Fett sparsam; korrekte Listensyntax |
| Markdown-Syntax statt Wikitext im Wiki-Kontext | 23 | In Wikitext umsetzen |
| Dekorative Tabelle, übersprungene Heading-Ebene oder `---` direkt vor Überschrift | 57 | In Prosa/korrekte Hierarchie auflösen; Linie vor Überschrift entfernen |
| Echte mehrdimensionale Daten, bewusster `---`-Szenenwechsel, CMS/Theme-Struktur | nicht 57 | Stehen lassen |

## Modusmatrix

Die Matrix steuert die Eingriffsentscheidung des Modells. `german_pattern_lint` meldet
modusunabhängig; `rhythm_lint` unterdrückt bei `--mode formal` die Stilverdachte zu den
Mustern 55 und 61, und `register_lint` schaltet Partikel- und Anrede-Findings je Modus.
Zusätzlich wertet die Preflight-Empfehlung den Modus maschinell aus.

| Musterklasse | Locker | Sachlich | Formal |
|---|---|---|---|
| HIGH Artefakt, Chatbot, Technik | ändern/entfernen | ändern/entfernen | ändern/entfernen |
| HIGH Evidenz/Quelle | markieren oder korrigieren | markieren oder korrigieren | markieren oder korrigieren |
| HIGH Stil | ändern | ändern | nur wenn nicht fachkonventionell; Muster 10 überspringen |
| MEDIUM technische/strukturelle Befunde | ändern | ändern | markieren oder vorsichtig ändern |
| MEDIUM weiche Stilbefunde | bei Häufung/Cluster ändern | bei Häufung/klarer Mechanik ändern | meist nur markieren |
| LOW Format/Interpunktion | ändern, wenn störend | ändern, wenn klarer Regelverstoß | meist überspringen oder markieren |
| Stimme einbringen | voll | dezent | nie |

Muster 45: False Friends immer korrigieren. Calques und syntaktische Transfers im Formal-Modus korrigieren; in Sachlich/Locker nur bei Häufung oder auffälliger Wörtlichkeit.

## Profil-Konflikte

| Konflikt | Vorrang |
|---|---|
| Zurückhaltung vs. unbelegte oder erfundene Quelle | Markierung |
| Quelle vs. schöner Stil | Quelle |
| Recht/Technik vs. Rhythmus | Recht/Technik |
| Formal-Modus vs. Schreibprobe | Formal-Modus |
| Zielprofil vs. generische Lockerheit | Zielprofil |
| Terminologiekonsistenz vs. Synonymvariation | Terminologiekonsistenz |
