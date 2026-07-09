# Humanizer-de Regressionsszenarien

Diese Datei sammelt Regressionsszenarien für das URTEILSVERHALTEN des Skills `Humanizer (Deutsch)` (LLM-im-Loop). Sie ergänzt den deterministischen Golden Corpus in `tests/corpus/` und die maschinenlesbaren Contract-Fixtures in `tests/scenarios/`.

## Ausführung

Starte für ein Szenario einen Subagenten mit geladenem Skill `SKILL.md`. Übergib den jeweiligen Nutzer-Prompt und den Input unverändert. Gleiche die Antwort anschließend manuell gegen die Pass/Fail-Kriterien ab.

Die Methodik entspricht dem Golden Corpus: Der Input ist der Testfall, die erwarteten Befunde stehen explizit daneben. Anders als `tests/test_corpus.py` laufen diese Fließtext-Fälle nicht per Python, sondern per Agent, weil sie Pass-Reihenfolge, Carve-outs, Output-Disziplin und Modellurteil prüfen.

Maschinenlesbare Invarianten liegen zusätzlich in `tests/scenarios/` und laufen über:

```bash
python3 scripts/run_review_eval.py tests/scenarios --check-invariants
```

## Coverage-Matrix

| Nr | Modus | getesteter Failure-Mode |
|---:|---|---|
| 1 | Sachlich | Dichte KI-Cluster werden nicht erkannt, zu breit umgeschrieben oder als Volltext neu ausgegeben. |
| 2 | Locker | Rhythmusarbeit wird mit Lexikpolitur, erfundener Nähe oder übersehenem Doppelpunkt-Titel-Cluster vermischt. |
| 3 | Sachlich | Subtile Struktur-Tells werden übersehen, weil die Linter keine Oberfläche melden. |
| 4 | Sachlich | Präziser technischer Fachtext wird wegen vermeintlicher "Mechanical Precision" verschlechtert. |
| 5 | Formal | Wissenschaftliches Register wird fälschlich gelockert oder gegen Fachkonventionen geglättet. |
| 6 | Formal | Behörden- oder Rechtssprache wird stilistisch umgeschrieben und dadurch unpräziser. |
| 7 | Sachlich | Ein einzelnes Oberflächensignal löst trotz Cluster-Regel einen Eingriff aus. |
| 8 | Locker | "Menschlicher machen" erfindet, verstärkt oder löscht persönliche Erfahrung falsch. |
| 9 | Sachlich | Vage Autoritäten werden mit erfundenen Quellen oder Zahlen kaschiert. |
| 10 | Sachlich | Eine konkrete Quelle mit Scope-Mismatch wird als tragender Beleg behandelt. |
| 11 | Sachlich | Ein lokaler KI-polierter Absatz führt zu globaler Politur menschlicher Absätze. |
| 12 | Locker | Eine Schreibprobe wird ignoriert oder in generische Lockerheit übersetzt. |
| 13 | Sachlich | Output-Disziplin und Fabrikationsschutz werden bei ankerlosem Text verletzt. |
| 19 | Formal | Ein tell-freier förmlicher Text wird in flapsiges Du-Register gekippt. |
| 20 | Sachlich | Ein tell-freier Text behält nach der Überarbeitung seinen monotonen Satzrhythmus. |
| 21 | Sachlich | Die Branding-Prelude landet trotz Raw-JSON/Maschinen-Output im Ergebnis. |
| 22 | Formal | Juristische Wiederholungen und Paragraphenanker werden aus falschem Glättungsdrang entfernt. |
| 23 | Locker | Bewusste Marketing-Repetition wird in generische Werbesprache geglättet. |
| 24 | Formal | Akademische Abstrakta, Passiv und Aussagevorsicht werden als vermeintliche KI-Tells überarbeitet. |

Die Szenarien 14 bis 18 (QGIR-Contracts) existieren nur als maschinenlesbare Fixtures in `tests/scenarios/` und laufen ausschließlich über den Runner; sie haben bewusst keinen Eintrag in dieser Datei.

## Szenario 1: Flagranter KI-Cluster (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe diesen Website-Text auf KI-Tells und überarbeite nur die Stellen, die wirklich auffallen."

**Input:**
```
In der heutigen schnelllebigen Zeit steht nachhaltige digitale Transformation als Zeugnis für den Anspruch unseres Unternehmens, Verantwortung und Innovation nahtlos zu verbinden. Unsere Plattform fungiert als zentraler Begleiter für Organisationen, die ihre Prozesse optimieren, ihre Datenlandschaft beleuchten und zukunftsfähige Lösungen umsetzen möchten. Darüber hinaus stellen unsere Beratungsleistungen einen wichtigen Bestandteil einer ganzheitlichen Strategie dar, die verschiedene Maßnahmen, relevante Aspekte und robuste Faktoren sinnvoll bündelt.

Zudem verfügt unser Team über ein einzigartiges Verständnis für die vielschichtige digitale Landschaft und zeigt spannende Möglichkeiten auf, Effizienz, Transparenz und Nachhaltigkeit miteinander zu verzahnen. Die modularen Services zeichnen sich durch hohe Flexibilität aus und schaffen für Kundinnen und Kunden ein faszinierendes Fundament für skalierbare Entscheidungen. Insgesamt unterstreicht dieser Ansatz, dass Technologie mehr ist als ein Werkzeug: Sie symbolisiert den nächsten Schritt verantwortungsvoller Unternehmensentwicklung. Zusammenfassend lässt sich sagen, dass wir den Wandel aktiv gestalten.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Der Audit benennt mehrere unabhängige Cluster, darunter 1/2/5/58/64/65, und stützt sie mit kurzen Zitaten statt mit Einzelsignalen.
- [ ] Pass 1-3 entfernen oder entschärfen Floskel-Opener, mechanische Übergänge, Symbolik, Werbewörter, Abstrakta-Stapel, KI-Marker-Vokabular und Kopula-Vermeidung; die Aussagen zu Plattform, Beratung, Effizienz, Transparenz und Nachhaltigkeit bleiben erhalten.
- [ ] Die Ausgabe zeigt nur geänderte Stellen mit Kurzaudit und gibt nicht den vollständigen Text aus.

**Relevante Muster:** 37 feuert als "In der heutigen..."-Framing; 4 feuert durch "Darüber hinaus"/"Zudem"/"Insgesamt"; 1 feuert durch "steht ... als Zeugnis"/"symbolisiert"; 2 feuert durch "einzigartig"/"faszinierend"; 5 feuert durch "Insgesamt"/"Zusammenfassend"; 58 feuert durch "Maßnahmen", "Aspekte", "Faktoren"; 64 feuert durch "nahtlos", "beleuchten", "digitale Landschaft", "vielschichtig", "spannend", "ganzheitlich"; 65 feuert durch "fungiert als", "stellt ... dar", "verfügt über", "zeichnet sich ... aus".

**Warum dieses Szenario zählt:** Es prüft den Grundfall eines dichten KI-Clusters, bei dem mehrere Muster gleichzeitig auftreten. Der Test fängt ab, ob das Skill konservativ, aber entschieden eingreift, ohne Substanz zu erfinden oder den Volltext neu auszugeben.

## Szenario 2: Monotoner Satzrhythmus (Locker)

**Skill-Modus:** Locker
**Nutzer-Prompt:** "Mach diesen Blogabschnitt bitte weniger gleichförmig, aber ohne neue Inhalte oder künstliche Lockerheit."

**Input:**
```
## Meal Prep am Sonntag: Wie ich die Woche sortiere

Der Sonntag beginnt bei mir mit einem leeren Tisch und einer einfachen Einkaufsliste. Ich prüfe zuerst die Vorräte im Schrank und notiere nur fehlende Zutaten. Der Einkauf bleibt dadurch überschaubar und passt meistens in eine kleine Fahrradtasche. Die Gerichte folgen einem festen Muster, weil ich oft dieselben Grundzutaten nutze. Ich koche außerdem am Abend Reis, Linsen und eine einfache Tomatensoße vor. Ich schneide zudem Gemüse klein und lagere es in flachen Glasboxen griffbereit. Die Boxen stehen danach vorne im Kühlschrank und erinnern mich jeden Morgen ans Mitnehmen. Mein Mittagessen entsteht morgens schneller, weil fast alles bereits zu Hause vorbereitet ist.

## Feierabend: Warum der Plan locker bleibt

Der Plan lässt trotzdem Raum für Hunger, Termine und spontane Einladungen nach der Arbeit. Ich tausche einzelne Zutaten aus und halte die Portionen unter der Woche einfach. Das Essen wirkt dadurch nicht besonders kreativ, aber es rettet bei mir volle Arbeitstage. Ich spare gleichzeitig Geld, weil weniger halbe Packungen am Ende im Kühlschrank landen.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] `rhythm_lint` meldet die Verdachtsmuster 4, 54 und 55; `unicode_lint` meldet keine Unicode- oder Quote-Befunde.
- [ ] Pass 3 darf zusätzlich den gehäuften Doppelpunkt-Titel nach Muster 54 entschärfen, etwa indem eine der beiden H2 in eine Aussage-Überschrift umgeformt wird.
- [ ] Pass 4 spreizt Satzlängen und rotiert das Vorfeld, sodass nicht fast jeder Satz subjektinitial und mittellang bleibt.
- [ ] Inhalt, Ich-Perspektive und alltagsnaher Ton bleiben erhalten; keine erfundene Anekdote, keine zusätzlichen Tipps, kein Volltext-Output.

**Relevante Muster:** 55 feuert primär durch niedrige Satzlängenvarianz und fast durchgehend subjektinitiale Sätze; 4 feuert durch die dichte Platzierung von "außerdem", "zudem" und "gleichzeitig"; 54 feuert durch zwei Überschriften im Doppelpunkt-Schema; 58/64 feuern bewusst nicht, weil die Lexik sauber und konkret bleibt; 59 feuert bewusst nicht, weil die Ich-Perspektive im Input bereits angelegt ist.

**Warum dieses Szenario zählt:** Es trennt Rhythmusarbeit von Lexikpolitur. Der Test fängt ab, ob Pass 4 einen brauchbaren, unauffälligen Text nur rhythmisch öffnet, ohne neue Inhalte oder forcierte Nähe einzubauen.

## Szenario 3: Subtile Struktur ohne Oberflächen-Tells (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe diesen Abschnitt auf KI-Tells; wenn nur die Struktur auffällt, ändere auch nur die Struktur."

**Input:**
```
Mittwochs ist der Stadtteiltreff ab 15 Uhr offen. Vor dem ersten Termin legt die Koordinatorin Kaffee, Namensschilder, Spielkarten und die Liste mit freien Beratungszeiten auf den großen Tisch. Neue Besucher bekommen eine kurze Führung durch Küche, Gruppenraum und Büro, bevor sie sich dazusetzen. Der Ort wirkt verlässlich.

Bei Formularen hilft der Raum neben der Küche. Vor dem Gespräch sammelt die Koordinatorin Briefe, Fristen, Ausweise und offene Rückfragen in einer blauen Mappe für die Beratung. Neue Besucher bekommen eine Erklärung zu Bescheiden, Anträgen und Terminen, bevor ein Folgetermin entsteht. Die Hilfe bleibt überschaubar.

Nach 18 Uhr wird gemeinsam aufgeräumt. Vor dem Abschließen notiert die Koordinatorin Aufgaben, fehlende Materialien, Rückrufe und Namen für die nächste Woche im Heft. Neue Besucher bekommen am Ausgang einen Hinweis auf Öffnungszeiten, Sprachgruppen und Ansprechpartner, bevor sie gehen. Der nächste Mittwoch ist vorbereitet.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] `rhythm_lint` meldet hier bewusst keine Verdachtsmuster: Der `uniform_paragraphs`-Detektor greift erst ab vier Absätzen, der Input hat drei. Die Erkennung von 61/62 ist deshalb eine Modell-Urteilsleistung in Pass 3.
- [ ] Pass 3 erkennt Muster 61 und 62 als Strukturcluster: drei fast gleich lange Absätze, paralleler Satzbau und je ein bewertender Schlusssatz ohne neue Information.
- [ ] Die Überarbeitung löst die isometrische Struktur gezielt auf, etwa durch Zusammenziehen oder Umgewichten vorhandener Sätze; sie ergänzt keine neuen Details.
- [ ] Pass 2 bleibt aus: keine Lexik-Korrektur für 58/64/65, keine Floskeljagd, keine Ausgabe des vollständigen Textes.

**Relevante Muster:** 61 feuert durch drei isometrische Absätze mit parallelem Aufbau; 62 feuert durch "Der Ort wirkt verlässlich", "Die Hilfe bleibt überschaubar" und "Der nächste Mittwoch ist vorbereitet"; 4, 54, 58, 64 und 65 feuern bewusst nicht, weil weder mechanische Konnektoren, Doppelpunkt-Überschriften, Abstrakta-Stapel, KI-Marker-Vokabular noch Kopula-Vermeidung vorliegen.

**Warum dieses Szenario zählt:** Es prüft den härtesten Positivfall: Der Text klingt sauber, trägt aber eine künstlich symmetrische Struktur. Der Test fängt ab, ob das Skill strukturelle Tells erkennt, ohne die Oberfläche unnötig zu glätten.

## Szenario 4: Sauberer technischer Fachtext (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe diese technische Dokumentation im Sachlich-Modus auf KI-Tells und ändere nur Stellen, bei denen wirklich ein Muster greift."

**Input:**
```
Der Suchdienst legt für Bestellungen zwei Indizes an. Der zusammengesetzte B-Tree-Index auf `tenant_id` und `created_at` deckt die Standardabfrage im Dashboard ab, weil die Daten immer mandantenweise und innerhalb eines Zeitfensters gelesen werden. Für die Volltextsuche in Kommentaren nutzt der Dienst einen separaten GIN-Index auf dem normalisierten Suchvektor. Diese Trennung verhindert, dass Schreibvorgänge unnötig viele Indexseiten anfassen.

Die API liefert bei leeren Ergebnislisten den Status 200 und ein leeres Array. Ein Status 404 wird nur zurückgegeben, wenn die angefragte Ressource selbst nicht existiert. Dieses Verhalten folgt der internen API-Richtlinie vom 14. März 2025 und entspricht der Beschreibung in der PostgreSQL-Dokumentation zu B-Tree- und GIN-Indizes. Clients müssen deshalb nicht zwischen „keine Treffer“ und „Endpunkt nicht gefunden“ raten, sondern prüfen nur das Feld `items`.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Der Skill meldet den Text als sauber oder gibt höchstens unkritische Hinweise aus; es werden keine Vorher/Nachher-Paare erzeugt.
- [ ] Fachbegriffe, Codefragmente, Statuscodes und Quellenhinweise bleiben unverändert; „Mechanical Precision“ oder „Impersonal Tone“ werden nicht als KI-Tell behandelt.
- [ ] Falls Lint-/Audit-Flags vorlagen, darf optional ein Block „Verworfene Kandidaten“ erscheinen, der jede erwogene Änderung an ein konkretes Flag oder eine Textstelle bindet und begründet, warum sie unterbleibt; ohne geprüfte Stelle erfundene Kandidaten sind ein Fail.

**Relevante Muster:** Keine Eingriffe; bewusst nicht feuern: Muster 39 (legitime sachliche Passivnähe), Muster 55 (kein behandlungsbedürftiger monotoner Rhythmus), Muster 65 (keine gehäufte Kopula-Vermeidung).

**Warum dieses Szenario zählt:** Das Szenario prüft, ob der Skill präzise technische Sachlichkeit vor Stilglättung schützt. Ein False Positive würde die Dokumentation weniger eindeutig machen.

## Szenario 5: Wissenschaftlicher Abstract (Formal)

**Skill-Modus:** Formal
**Nutzer-Prompt:** "Bitte prüfe diesen Abstract im Formal-Modus auf KI-Tells. Stilistische Glättung ist nur erwünscht, wenn ein echtes Artefakt vorliegt."

**Input:**
```
Ziel der Studie war die Prüfung, ob ein strukturiertes Übergabeprotokoll die Vollständigkeit pflegerischer Schichtübergaben erhöht. In die prospektive Beobachtungsstudie wurden 18 Stationen eines kommunalen Klinikverbunds eingeschlossen. Vor und nach der Einführung des Protokolls wurden jeweils 240 Übergaben anhand eines standardisierten Erhebungsbogens ausgewertet. Primärer Endpunkt war der Anteil vollständig dokumentierter Angaben zu Medikation, Mobilität und offenen Diagnostikterminen.

Nach Einführung des Protokolls stieg die Vollständigkeit der Übergaben von 71,4 Prozent auf 84,9 Prozent. Der adjustierte Unterschied betrug 13,1 Prozentpunkte bei einem 95-Prozent-Konfidenzintervall von 8,2 bis 18,0 Prozentpunkten. Ausgehend von den Stationsclustern wurden robuste Standardfehler berechnet; ergänzend erfolgte eine Sensitivitätsanalyse ohne Nachtdienste. Die Datenerhebung wurde durch zwei geschulte Pflegewissenschaftlerinnen stichprobenartig geprüft. Die Ergebnisse sprechen für einen messbaren Nutzen des Protokolls, erlauben jedoch keine Aussage zur langfristigen Patientensicherheit.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Im Formal-Modus wird keine persönliche Stimme eingebracht und der Abstract wird nicht in ein lockereres Register umgeschrieben.
- [ ] Muster 10 und Muster 39 werden wegen fachkonventioneller Formulierungen übersprungen oder höchstens markiert; es erfolgt kein stilistischer Eingriff.

**Relevante Muster:** Keine echten Eingriffe; bewusst nicht feuern: Muster 10 (Partizip-I-/Formalregister nicht behandeln), Muster 39 (Passiv im Wissenschaftsregister legitim), Muster 55 (fachübliche Gleichmäßigkeit nicht für Detektor-Score verschlechtern).

**Warum dieses Szenario zählt:** Der Test schützt wissenschaftliches Register vor falscher Humanisierung. Formaler Nominalstil und Passiv sind hier keine KI-Tells, sondern Teil der Textsorte.

## Szenario 6: Behörden-/Rechtstext (Formal)

**Skill-Modus:** Formal
**Nutzer-Prompt:** "Bitte prüfe diesen behördlichen Auszug im Formal-Modus auf KI-Artefakte, ohne die juristischen Formulierungen stilistisch umzuschreiben."

**Input:**
```
Für die Sondernutzung öffentlicher Verkehrsflächen wird gemäß § 12 Abs. 3 der Sondernutzungssatzung eine Gebühr erhoben. Die Gebühr entsteht mit Erteilung der Erlaubnis und wird mit Bekanntgabe dieses Bescheids fällig. Zahlungspflichtig ist die Person, der die Sondernutzungserlaubnis erteilt wurde; bei mehreren Berechtigten haften diese als Gesamtschuldner.

Die Erlaubnis gilt ausschließlich für den im Antrag bezeichneten Standort und den dort angegebenen Zeitraum. Änderungen des Aufbaus, eine Verlegung der Fläche oder eine Überlassung an Dritte bedürfen der vorherigen schriftlichen Zustimmung der zuständigen Behörde. Wird die Fläche ohne Zustimmung erweitert oder nach Ablauf der Erlaubnis weiter genutzt, kann die Erlaubnis widerrufen und die Entfernung der Anlagen angeordnet werden. Bereits gezahlte Gebühren werden in diesem Fall nur erstattet, soweit die Satzung dies vorsieht. Der Rechtsbehelf richtet sich nach der diesem Bescheid beigefügten Belehrung.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Der Skill nimmt keine stilistische Umschreibung juristischer oder regulatorischer Wendungen vor.
- [ ] Formal-Modus bleibt strikt: höchstens echte Artefakte werden markiert; Passiv, Nominalstil, Satzungssprache und feste Behördenformeln bleiben unangetastet.

**Relevante Muster:** Keine Eingriffe; bewusst nicht feuern: Muster 39 (juristisch legitimes Passiv), Muster 58 (Nominalstil hier textsortentypisch), Muster 65 (keine gehäufte leere Ersatzkonstruktion mit Änderungsbedarf).

**Warum dieses Szenario zählt:** Das Szenario fängt Überarbeitungen ab, die rechtliche Genauigkeit zugunsten vermeintlich menschlicher Sprache beschädigen würden. Regulatorische Formulierungen sind laut Leitplanke nicht stilistisch zu glätten.

## Szenario 7: Einzelsignal (Cluster-Regel) (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe diesen kurzen Sachtext im Sachlich-Modus auf KI-Tells und beachte dabei ausdrücklich die Cluster-Regel."

**Input:**
```
Im Teamreview wurde vereinbart, dass die offenen Rückfragen künftig direkt am jeweiligen Ticket stehen. Bisher lagen einige Hinweise in separaten Notizen, wodurch bei der Übergabe zwischen Entwicklung und Support gelegentlich Kontext verloren ging. Die neue Regel ist einfach – jede Rückfrage bekommt einen Kommentar mit Datum, zuständiger Person und dem nächsten erwarteten Schritt.

Für ältere Tickets wird die Änderung nicht rückwirkend erzwungen. Der Support ergänzt nur dort Angaben, wo ohnehin eine Antwort aussteht oder eine Kundin nach dem Bearbeitungsstand fragt. Die Entwicklung prüft am Ende der Woche, ob die offenen Punkte eindeutig genug beschrieben sind. Wenn ein Ticket danach noch unklar bleibt, wird es im Montagsabgleich kurz besprochen. Mehr ist für den Prozess nicht nötig, weil die bestehenden Statusfelder unverändert weiterverwendet werden.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Der Skill greift nicht ein und sagt explizit, dass ein einzelnes Oberflächensignal ohne Häufung kein KI-Tell ist.
- [ ] Der einzelne Gedankenstrich wird weder entfernt noch als Muster 16 behandelt; es werden keine weiteren Muster konstruiert.

**Relevante Muster:** Keine Eingriffe; bewusst nicht feuern: Muster 16 (genau ein legitimer Gedankenstrich), Muster 4 (keine mechanische Konnektor-Häufung), Muster 55 (ausreichende Satzlängenvarianz).

**Warum dieses Szenario zählt:** Der Test prüft die zentrale Leitplanke „Cluster statt Einzelsignal“. Ein einzelnes Satzzeichen darf keinen Humanizer-Durchlauf auslösen.

## Szenario 8: Ich-Anekdote ohne Autorenkontext (Locker)

**Skill-Modus:** Locker
**Nutzer-Prompt:** "Bitte mach den Text lockerer und persönlicher, er soll weniger nach KI klingen."

**Input:**
```
Ich merke immer wieder, dass gute Routinen nicht am perfekten Plan hängen, sondern an dem Moment, in dem sie in den Alltag passen. Als ich letztes Jahr nach einem Umzug wieder mit Sport anfangen wollte, hatte ich mir erst einen ziemlich strengen Wochenplan gebaut. Der sah auf dem Papier vernünftig aus, hielt aber genau vier Tage. Danach lag die Matte wieder in der Ecke, und ich war genervt, weil ich schon wieder zu groß gedacht hatte.

Geholfen hat am Ende eine kleinere Regel: zehn Minuten, direkt nach dem Kaffee, ohne Umziehen und ohne App. Das war unspektakulär, aber machbar. Nach zwei Wochen war daraus nicht plötzlich ein neues Leben geworden, nur ein Termin, den ich nicht mehr jedes Mal neu verhandeln musste. Genau darum geht es bei Gewohnheiten: Sie müssen nicht beeindrucken. Sie müssen wiederholbar sein.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Die Antwort erfindet oder verstärkt keine Ich-Erfahrung: keine zusätzlichen Orte, Kunden, Gefühle, Zeiträume, Erfolge oder Details zur Anekdote.
- [ ] Falls humanisiert wird, beschränken sich Änderungen auf vorhandene Fakten, Wortwahl oder Rhythmus; die Anekdote bleibt im Zweifel unangetastet oder wird wegen fehlenden Autorenkontexts markiert.
- [ ] Es wird kein vollständiger umgeschriebener Text ausgegeben, sondern nur betroffene Stellen oder ein kurzer Audit-Hinweis.
- [ ] Die vom Nutzer eingereichte Ich-Anekdote wird nicht als Muster-59-Verstoß entfernt; sie ist die eigene Materialgrundlage des Autors. Löschen statt Belassen/Markieren = FAIL.

**Relevante Muster:** 59 (feuert als Leitplanke: Ich-Erfahrung ohne gelieferten Autorenkontext nicht ausbauen); 53 (bewusst nicht neu erzeugen: keine spekulativen Motive oder Folgedetails ergänzen)

**Warum dieses Szenario zählt:** Der Fall prüft, ob "menschlicher machen" nicht in Fabrikation kippt. Gerade im Locker-Modus darf Stimme nur aus dem gelieferten Material kommen.

## Szenario 9: Vage Autorität ohne Quelle (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe diesen Abschnitt sachlich auf KI-Tells und Evidenzprobleme."

**Input:**
```
Flexible Arbeitszeiten werden in vielen Dienstleistungsbetrieben inzwischen als wichtiger Baustein der Personalplanung beschrieben. Studien zeigen, dass Beschäftigte dadurch zufriedener sind und seltener kündigen. Experten sind sich einig, dass starre Schichtmodelle vor allem jüngere Bewerber abschrecken. Es ist allgemein bekannt, dass Teams mit mehr Entscheidungsspielraum konzentrierter arbeiten und weniger krankheitsbedingte Ausfälle haben.

Für kleine Betriebe ist die Umsetzung trotzdem nicht trivial. Wenn nur drei Personen eine Filiale öffnen können, lässt sich nicht jeder Wunsch in den Dienstplan schreiben. Sinnvoll ist deshalb ein Rahmen, der feste Kernzeiten mit begrenztem Tauschspielraum verbindet. Die Führungskraft muss dabei transparent erklären, warum bestimmte Zeiten gesetzt sind. Ohne klare Regeln entsteht schnell der Eindruck, einzelne Mitarbeiter würden bevorzugt. Flexible Arbeitszeiten funktionieren also nur, wenn Erwartungen, Zuständigkeiten und Grenzen vorab sauber geklärt sind.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Muster 11 wird konkret an den Formulierungen "Studien zeigen", "Experten sind sich einig" und "Es ist allgemein bekannt" markiert.
- [ ] Die Antwort erfindet keine Studie, Institution, Jahreszahl oder Prozentzahl; sie markiert die Lücke mit `[ECHTE QUELLE NÖTIG]` oder entfernt die vage Zuschreibung.
- [ ] Die sachlichen Sätze ohne Quellenproblem werden nicht pauschal umgeschrieben, nur weil der Text sauber und neutral klingt.

**Relevante Muster:** 11 (feuert: vage Autoritäten ohne konkrete Quelle); 53 (bewusst nicht feuern lassen: keine spekulative Begründung oder Ersatzquelle ergänzen)

**Warum dieses Szenario zählt:** Evidenzlücken dürfen nicht durch glattere Sprache verschwinden. Der Skill muss die fehlende Quelle sichtbar machen, statt den Absatz scheinbar belastbarer zu formulieren.

## Szenario 10: Beleginkongruenz (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe den Abschnitt für eine interne Vorlage auf KI-Tells und belastbare Evidenz."

**Input:**
```
Die Stadt bewertet die neue Online-Terminvergabe als deutlichen Fortschritt für alle Bürgerdienste. Im Entwurf heißt es: „Seit der Einführung des Portals sank die Bearbeitungszeit sämtlicher Bürgeranfragen um 63 Prozent.“ Als Beleg ist im Material folgender Nachweis angegeben: Stadt Köln, Kurzbericht Bürgertelefon 2024, S. 7. Dort steht: „Für das Bürgertelefon lagen 63 Prozent der eingehenden Anrufe im zweiten Quartal unter zwei Minuten Wartezeit; E-Mail-Anfragen, Kfz-Zulassung und Vor-Ort-Termine wurden nicht ausgewertet.“

Die Zahl wird im Text trotzdem als Nachweis für die gesamte Verwaltungskommunikation verwendet. Auch in der Zusammenfassung steht, das Portal habe die Bearbeitung in allen Fachbereichen messbar beschleunigt. Weitere Daten, etwa zu abgeschlossenen Fällen, durchschnittlicher Bearbeitungsdauer oder Rückständen in einzelnen Ämtern, werden nicht genannt. Der Abschnitt soll sachlich bleiben, weil er in eine interne Vorlage für den Hauptausschuss übernommen werden soll.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Muster 42 wird markiert: Die Quelle trägt die Aussage zu "sämtlichen Bürgeranfragen", "Bearbeitungszeit" und "allen Fachbereichen" nicht.
- [ ] Die Antwort behandelt die Quellenangabe nicht ungeprüft als tragenden Beleg und deutet die 63 Prozent nicht zur allgemeinen Bearbeitungszeit um.
- [ ] Zulässig ist nur Kennzeichnung als `[BELEG PRÜFEN]` oder eine engere Formulierung entlang des belegten Bürgertelefon-/Wartezeit-Scope; keine Ersatzquelle wird erfunden.

**Relevante Muster:** 42 (feuert: konkrete Quelle bzw. Quellenpassage belegt die getroffene Aussage nicht)

**Warum dieses Szenario zählt:** Der Fall trennt saubere Quellenoptik von echter Belegkraft. Er verhindert, dass der Skill eine konkrete, aber unpassende Quelle kosmetisch als ausreichend behandelt.

## Szenario 11: Stilwechsel / KI-polierter Mittelabsatz (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe den folgenden Entwurf im Modus Sachlich auf KI-Tells. Mir ist wichtig, dass du nur auffällige Stellen änderst und die persönlichen Beobachtungen stehen lässt."

**Input:**
```
Am Dienstag stand ich um halb acht mit Lisa im kleinen Besprechungsraum, weil der Beamer im großen Raum wieder kein Bild zeigte. Auf dem Ausdruck lag noch ihr Kaffeefleck vom Vortag. Wir sind die Liste trotzdem Punkt für Punkt durchgegangen und haben drei Tickets gestrichen, die längst erledigt waren. Bei zwei Punkten wussten wir beide nicht, wer sie eigentlich aufgeschrieben hatte.

In der heutigen Arbeitswelt stellt die Abstimmung zwischen Fachbereich und IT einen entscheidenden Erfolgsfaktor dar. Darüber hinaus ermöglicht ein ganzheitlicher Blick auf Prozesse, Anforderungen und Stakeholder eine nahtlose Priorisierung relevanter Maßnahmen. Im Kern geht es darum, das Zusammenspiel der Beteiligten zu beleuchten und robuste Lösungen für eine dynamische Projektlandschaft zu schaffen. So entsteht eine tragfähige Grundlage für nachhaltige Umsetzung.

Nach der Runde habe ich die offenen Punkte direkt neben die alten Screenshots gesetzt. Das sah nicht schön aus, war aber lesbar. Jan hat später noch angerufen und gesagt, dass der Export vom Freitag fehlt. Den Satz über die neue Rollenverteilung lasse ich erst einmal draußen, bis wir wissen, ob Katrin die Freigabe wirklich übernimmt.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Erkennt Muster 30 als Stilbruch: Nur der Mittelabsatz wird markiert oder überarbeitet; Absatz 1 und 3 bleiben in Inhalt, Rhythmus und konkreten Beobachtungen unangetastet.
- [ ] Bearbeitet die Tells im Mittelabsatz lokal, ohne die menschlichen Absätze sachlicher, glatter oder generischer zu machen.
- [ ] Erfindet keine zusätzlichen Projektdetails und ersetzt Abstrakta nur dort, wo der Input selbst eine konkrete Grundlage liefert.

**Relevante Muster:** 30 feuert als Stilwechsel; 4, 32, 37, 58, 62, 64 und 65 feuern im Mittelabsatz. 55/51 dürfen nicht als globaler Glättungsauftrag auf den ganzen Text ausgeweitet werden.

**Warum dieses Szenario zählt:** Es prüft, ob der Skill gemischte Autorschaft erkennt und lokal eingreift. Der Failure-Mode wäre, die zwei menschlichen Absätze aus Vorsicht ebenfalls zu polieren.

## Szenario 12: Schreibprobe + Rewrite (Zielprofil) (Locker)

**Skill-Modus:** Locker
**Nutzer-Prompt:** "Ich habe erst eine Schreibprobe eingefügt und darunter den Text, der humanisiert werden soll. Bitte nutze meine Stimme als Ziel und überarbeite nur den zweiten Teil."

**Input:**
```
Schreibprobe:
Der alte Export nervt. Nicht dramatisch. Aber er frisst Zeit. Ich mache dann erst Kaffee, öffne die CSV und suche die drei Spalten, die wirklich zählen. Meist ist es dieselbe Baustelle: eine ID fehlt, ein Datum rutscht, und jemand nennt die Datei final_final. Kurz: läuft nicht schön. Geht aber.

Text zum Überarbeiten:
In der heutigen Datenarbeit stellt ein sauberer Export einen entscheidenden Erfolgsfaktor dar. Darüber hinaus ermöglicht eine strukturierte Prüfung der relevanten Informationen eine nahtlose Qualitätssicherung über verschiedene Prozessschritte hinweg. Im Kern geht es darum, die vorhandenen Datenflüsse ganzheitlich zu beleuchten und robuste Lösungen für eine effiziente Zusammenarbeit zu schaffen. So entsteht eine Grundlage, die Teams nachhaltig unterstützt und Orientierung in einer dynamischen Arbeitsumgebung bietet.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Pass 0 hält ein Zielprofil aus der Schreibprobe fest: kurze Sätze und Fragmente, einfaches Wortniveau, knappe Absatzanfänge, Doppelpunkt als Lieblingszeichen, keine geschmeidige Default-Stimme.
- [ ] Der Rewrite des zweiten Teils folgt diesem Profil, bleibt aber bei den gelieferten Fakten; die Schreibprobe selbst wird nicht korrigiert oder umgeschrieben.
- [ ] Es entstehen keine erfundene Ich-Erfahrung, keine Pseudo-Anekdote und keine forcierte Lockerheit.

**Relevante Muster:** Pass-0-Zielprofil steuert das Ergebnis; im Rewrite-Teil feuern 4, 32, 37, 58, 64 und 65. 59 darf bewusst nicht neu entstehen.

**Warum dieses Szenario zählt:** Es prüft, ob eine gelieferte Schreibprobe tatsächlich die Stimme vorgibt. Der Failure-Mode wäre ein generischer lockerer Ton, der zwar weniger KI-glatt wirkt, aber nicht zur Probe passt.

## Szenario 13: Output-Disziplin + Null-Anker (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte prüfe diesen Sachtext im Modus Sachlich. Gib nur die geänderten Stellen aus und markiere Lücken, statt Details zu erfinden."

**Input:**
```
In der heutigen digitalen Verwaltung stellt ein klarer Umgang mit internen Informationen einen entscheidenden Erfolgsfaktor dar. Der Ansatz beleuchtet verschiedene Aspekte der Zusammenarbeit und schafft ein nahtloses Zusammenspiel zwischen Prozessen, Rollen und Erwartungen. Im Kern geht es darum, eine robuste Grundlage für bessere Entscheidungen zu entwickeln, ohne dabei die Flexibilität der Beteiligten einzuschränken.

Darüber hinaus ist davon auszugehen, dass die Maßnahme aus einer besonderen Bedarfslage entstanden ist und langfristig zu mehr Vertrauen führt. Welche Auslöser genau beteiligt waren, wird nicht benannt; vermutlich spielte eine veränderte Arbeitsweise eine wichtige Rolle. Die Umsetzung eröffnet vielseitige Möglichkeiten und zeigt, wie dynamisch sich organisatorische Landschaften verändern können. Insgesamt entsteht so ein zukunftsfähiger Rahmen, der Orientierung bietet und weitere Potenziale sichtbar macht.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Gibt niemals den vollständigen Text aus; erlaubt sind nur Gefundene Muster, Vorher/Nachher-Paare für geänderte Stellen und ein kurzes Audit.
- [ ] Entfernt oder markiert Floskeln und Spekulationen, ergänzt aber keine Namen, Zahlen, Daten, Beispiele, Ursachen oder Träger.
- [ ] Markiert fehlende Substanz mit Hinweisen wie `[KONKRETION NÖTIG]` oder `[SUBSTANZ PRÜFEN]`, statt aus dem leeren Kontext konkrete Verwaltungsvorgänge zu erfinden.

**Relevante Muster:** 53 feuert bei unbelegter Lückenfüllung; 5, 32, 37, 58, 64 und 65 feuern als ankerlose Floskel-Cluster. 42 feuert nicht, weil keine konkrete Quelle geprüft werden kann.

**Warum dieses Szenario zählt:** Es prüft gleichzeitig die Output-Regel und den Fabrikationsschutz. Der Failure-Mode wäre, den ganzen Text neu auszugeben oder fehlende Konkretion mit plausibel klingenden Details zu füllen.

## Szenario 19: Registerbruch ohne KI-Tells (Formal)

**Skill-Modus:** Formal
**Nutzer-Prompt:** "Bitte prüfe diese Anfrage im Modus Formal und ändere nur, was wirklich nötig ist."

**Input:**
```
Sehr geehrte Frau Berger, für die Schlussabrechnung des Projekts fehlt uns noch Ihre unterschriebene Stundenübersicht. Bitte senden Sie das Dokument bis Donnerstag an das Sekretariat. Für Rückfragen erreichen Sie mich vormittags telefonisch.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Der Input wird als tell-freier menschlicher Text erkannt; es gibt keine erfundenen Muster-Befunde und keine unnötige Umschreibung.
- [ ] Sie-Anrede, förmlicher Ton und die Anker (Frau Berger, Stundenübersicht, Donnerstag, Sekretariat) bleiben unangetastet.
- [ ] Eine Antwort im flapsigen Du-Register (halt, doch, einfach) wird als Registerbruch behandelt, auch wenn sie inhaltlich korrekt und tell-frei ist.

**Relevante Muster:** bewusst keine — der Text enthält kein einziges KI-Tell. Das Urteil kommt allein aus Registertreue (`register_shift`, `formal_register_break`) und Profil-Contract (`particle_count`, Rhythmus-Korridor).

**Warum dieses Szenario zählt:** Es ist der Existenzbeweis für die Nach-Tell-Ära: menschlicher Text, null Katalog-Treffer, trotzdem ein hartes Urteil. Der Failure-Mode wäre ein Harness, das ohne Tells nichts mehr zu sagen hat. Das Contract-File erzwingt beides exakt: der Du-Umbau feuert Register- und Profil-Verletzungen, die registertreue Minimalkorrektur bleibt bei exakt null Verletzungen.

## Szenario 20: Monotonie ohne KI-Tells (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Bitte öffne den Satzrhythmus dieses Abschnitts, ohne Inhalte zu ändern."

**Input:**
```
Die Werkstatt öffnet unter der Woche am frühen Morgen. Die Kunden geben ihre Räder direkt am Tresen ab. Die Mechaniker prüfen zuerst Bremsen, Schaltung und Beleuchtung. Die Reparaturen dauern meistens nur wenige Tage. Die Abholung klappt danach auch ohne festen Termin.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Der Text wird als fehlerfrei und tell-frei erkannt; das einzige Problem ist der gleichförmige Satzrhythmus (fünf Sätze nahezu gleicher Länge).
- [ ] Eine Überarbeitung, die die Monotonie beibehält, gilt als gescheitert — auch wenn sie sprachlich sauber bleibt.
- [ ] Die rhythmisch geöffnete Fassung variiert Satzlängen und Satzanfänge, ohne neue Inhalte, Partikeln oder Volltext-Echo.

**Relevante Muster:** bewusst keine Katalog-Treffer. Das Urteil kommt allein aus dem Stilprofil: der `stddev_mean_ratio`-Korridor des Zielprofils `sachlich` (min 0.4) schlägt bei der monotonen Fassung an (`profile_out_of_range`), die geöffnete Fassung liegt im Korridor.

**Warum dieses Szenario zählt:** Es prüft, ob das Harness ein reines Rhythmusurteil ohne jede Tell-Oberfläche tragen kann. Der Failure-Mode wäre, Monotonie nur dann zu erkennen, wenn zugleich Katalogmuster feuern. Beide Contract-Samples laufen exakt: die monotone Umschreibung erwartet genau `profile_out_of_range`, die geöffnete Fassung genau null Verletzungen.

## Szenario 21: Prelude-Suppression bei Raw-JSON (Sachlich)

**Skill-Modus:** Sachlich
**Nutzer-Prompt:** "Gib das Ergebnis als Raw-JSON aus."

**Input:**
```
Die API liefert Status 200 und ein leeres Array.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Raw-JSON und anderer Maschinen-Output enthalten keine Branding-Prelude und keine Zusatzprosa.
- [ ] Eine Ausgabe mit `Less machine. More voice.` vor dem JSON gilt als harter Contract-Verstoß.
- [ ] Sauberes JSON ohne Prelude bleibt bei exakt null Invariant-Verletzungen.

**Relevante Muster:** bewusst keine Katalog-Treffer. Das Urteil kommt allein aus der Output-Regel: Die Prelude ist für normale user-facing Runs erlaubt, muss bei Raw-JSON, ausdrücklich knapper Ausgabe und stillen Dateiänderungen aber wegfallen.

**Warum dieses Szenario zählt:** Es schützt maschinenlesbare Ausgaben vor menschlichem Branding. Der Failure-Mode wäre, dass eine hilfreiche Standard-Prelude in Raw-JSON rutscht und nachgelagerte Automatisierung bricht.

## Szenario 22: Red-Team Rechtstext Do-nothing (Formal)

**Skill-Modus:** Formal
**Nutzer-Prompt:** "Bitte prüfe diesen Vertragsauszug im Formal-Modus und ändere nur echte KI-Artefakte."

**Input:**
```
Im Sinne dieser Vereinbarung bezeichnet „Vertrauliche Information“ jede Unterlage, die im Datenraum bereitgestellt wird. Die Mieterin darf Unterlagen nach § 5 Abs. 2 nur für die Prüfung verwenden. § 5 Abs. 2 gilt auch für Kopien, Auszüge und Notizen. Vertrauliche Information bleibt Vertrauliche Information, selbst wenn sie mündlich erläutert wird. Einwendungen sind binnen 14 Tagen in Textform mitzuteilen.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Die wiederholten Verweise auf § 5 Abs. 2 bleiben stehen; sie sind juristische Präzision, kein Stilproblem.
- [ ] Die Definitionswiederholung „Vertrauliche Information“ wird nicht durch Synonyme ersetzt.
- [ ] Eine minimale Umstellung ist zulässig, wenn Mieterin, Frist, Textform und alle Paragraphenanker erhalten bleiben.

**Relevante Muster:** bewusst keine Katalog-Tells. Das Urteil kommt aus Anker- und Registertreue: Ein Over-Edit, der Paragraphen, Definition oder Formanforderung glättet, verletzt den Contract.

**Warum dieses Szenario zählt:** Der Fall schützt Rechtssprache vor falscher Varianz. Der Failure-Mode wäre, Wiederholung als KI-Signal zu behandeln und dadurch Rechtsbezüge unpräziser zu machen.

## Szenario 23: Red-Team Marketing-Repetition (Locker)

**Skill-Modus:** Locker
**Nutzer-Prompt:** "Bitte prüfe diesen Kampagnenabschnitt auf KI-Tells. Die Wiederholung im Claim ist beabsichtigt."

**Input:**
```
Wir starten klein. Wir testen schnell. Wir lernen offen. Das ist kein Zufall, sondern unser Arbeitsversprechen für die Frühjahrskampagne 2026: weniger Reibung im Shop, klare Preise im Warenkorb und Antworten binnen 24 Stunden. Wieder schneller finden. Wieder leichter kaufen. Wieder sicherer entscheiden. Genau diese Wiederholung soll im Claim stehen.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Parallelismus und „Wieder“-Repetition bleiben als Stilmittel erhalten.
- [ ] Kampagnenjahr, Antwortzeit und die drei Claim-Zeilen werden nicht zusammengezogen oder verallgemeinert.
- [ ] Zulässig ist nur eine kleine syntaktische Straffung außerhalb des Claims.

**Relevante Muster:** bewusst keine Eingriffe wegen Repetition allein. Der Contract schützt die beabsichtigte Wiederholung und die Kampagnenanker vor generischer Werbeglättung.

**Warum dieses Szenario zählt:** Marketingtexte nutzen Wiederholung oft absichtlich. Der Test fängt ab, ob das Skill Repetition nur dann behandelt, wenn sie tatsächlich künstlich wirkt und nicht, wenn sie als Claim-Mechanik markiert ist.

## Szenario 24: Red-Team Akademisches Register (Formal)

**Skill-Modus:** Formal
**Nutzer-Prompt:** "Bitte prüfe diesen Methodikabschnitt im Formal-Modus. Fachregister und Aussagevorsicht sollen erhalten bleiben."

**Input:**
```
Die Auswertung wurde auf Ebene der Kursgruppen vorgenommen. Im Mittelpunkt standen die Vergleichbarkeit der Erhebungszeitpunkte, die Nachvollziehbarkeit der Kodierung und die Begrenzung möglicher Verzerrungen. Abweichungen wurden dokumentiert; eine kausale Wirkung wurde ausdrücklich nicht behauptet. Diese Zurückhaltung ist Teil der Argumentation, nicht ein Mangel an Stimme.
```

**Erwartetes Verhalten (Pass/Fail):**
- [ ] Abstrakta wie Vergleichbarkeit, Nachvollziehbarkeit und Verzerrungen bleiben erhalten, weil sie die Methode präzise benennen.
- [ ] Das Passiv wird nicht pauschal in ein lockeres „Wir“-Register umgeschrieben.
- [ ] Die Aussage „kausale Wirkung wurde ausdrücklich nicht behauptet“ darf nicht in eine stärkere Ergebnisbehauptung kippen.

**Relevante Muster:** bewusst keine Eingriffe wegen akademischem Passiv oder Nominalstil. Der Contract misst Ankererhalt und verhindert Register- sowie Claim-Drift.

**Warum dieses Szenario zählt:** Der Fall hält die Grenze zwischen berechtigter Humanisierung und fachlicher Verwässerung. Akademische Vorsicht ist hier Substanz, kein Artefakt.

## Neue Szenarien hinzufügen

Neue Szenarien sollten einen klaren Failure-Mode isolieren und die betroffenen Muster-IDs nennen. Der Input sollte klein genug bleiben, dass ein Mensch die Antwort gegen die Pass/Fail-Kriterien prüfen kann, aber groß genug, um echte Cluster oder Carve-outs sichtbar zu machen.

Füge neue Fälle fortlaufend nummeriert hinzu und ergänze die Coverage-Matrix. Wenn ein Szenario deterministisch durch `unicode_lint.py`, `rhythm_lint.py`, `evidence_lint.py`, `register_lint.py` oder `german_pattern_lint.py` prüfbar ist, gehört der reine Linter-Anteil zusätzlich in `tests/corpus/`. Wenn Output-Invarianten maschinenlesbar sind, lege zusätzlich ein Contract-File in `tests/scenarios/` an. QGIR-Fälle müssen dort `qgir_contract` mit Pass-Limit, Edit-Budget und belegtreuen Ankern enthalten; Detector-Bezug bleibt außerhalb der Contract-Checks. Sample-Outputs mit Pass-Limit brauchen eine `passes`-Liste, sonst gilt die Pass-Spur als fehlend. `SCENARIOS.md` bleibt für Urteil, Pass-Reihenfolge und Output-Verhalten.
