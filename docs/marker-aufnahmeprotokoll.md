# Marker-Aufnahmeprotokoll

Dieses Protokoll ist für neue und materiell erweiterte Regeln der deterministischen Linter
verbindlich. Ein Muster im Katalog ist noch keine Lint-Regel: Erst wenn Erkennungslogik,
Schwelle, Grenzen und erlaubte Aktion dokumentiert und getestet sind, darf ein Marker in
einen Linter aufgenommen werden.

## Pflichtangaben

Jede Aufnahme oder materielle Regeländerung dokumentiert:

1. Muster-ID, Kandidatenname und Zweck
2. unterstützte Texttypen und Modi sowie ausgeschlossene Spans, insbesondere Code, URLs,
   Zitate und Markdown-/HTML-Syntax
3. Regex oder sonstige Erkennungslogik
4. Dokument-Schwelle: Einzelfund, Cluster oder Häufigkeit
5. mindestens drei Positiv-, drei Negativ- und zwei Grenz-Fixtures; für jeden Grenzfall
   steht das erwartete Verhalten ausdrücklich dabei
6. bekannte Fehlalarmfamilien und die qualitative Fehlalarm-Erwartung
7. Severity, Meldungstext und erlaubte Aktion: advisory oder Auto-Hinweis, niemals
   Auto-Rewrite
8. das ausdrückliche Verbot, aus Treffern Autorschaft abzuleiten
9. Versionsdatum und Begründung bei jeder Regeländerung

Fixtures müssen die öffentliche Regeloberfläche prüfen, nicht nur Hilfsfunktionen. Änderungen
an Regex, Schwelle, Severity, Meldung oder Scope gelten als materielle Regeländerung und
erfordern einen neuen datierten Begründungseintrag.

## Aufgenommen: M43-Homoglyph-Check mixed_script (2026-09-02)

1. **Muster-ID, Kandidatenname und Zweck:** Muster 43, `mixed_script`. Der Befund macht
   technische Homoglyph-Artefakte sichtbar: Ein einzelnes Wort enthält Buchstaben aus
   mehreren Schriftsystemen, typischerweise einen kyrillischen oder griechischen
   Doppelgänger in einem lateinischen Wort.
2. **Texttypen, Modi und ausgeschlossene Spans:** Aktiv in allen Texttypen und Modi. Wie
   `hidden_unicode` prüft der Befund den gesamten Text ohne Scope-Ausschluss, also auch
   Code, URLs, Zitate sowie Markdown- und HTML-Syntax. Das ist nötig, weil Homoglyphen
   gerade in technischen Bezeichnern und URL-Domains sicherheitsrelevant sein können.
3. **Erkennungslogik:** `\w+` zerlegt den Text in Tokens; Bindestriche und Satzzeichen
   trennen sie. Für jeden alphabetischen Codepoint wird das Präfix des von
   `unicodedata.name` gelieferten Namens ausgewertet. Berücksichtigt werden `LATIN`,
   `CYRILLIC` und `GREEK`. Ziffern, Satzzeichen, Unterstriche und Kombinationszeichen
   tragen kein Schriftsystem und werden ignoriert. Ein Finding entsteht nur, wenn ein
   Token Buchstaben aus mindestens zwei berücksichtigten Systemen enthält. Als fremd
   meldet der Linter die Zeichen außerhalb des häufigsten Systems; bei Gleichstand hat
   Latein Vorrang. Die Meldung nennt jedes unterschiedliche fremde Zeichen samt
   Codepoint, der Span umfasst das vollständige Token.
4. **Dokument-Schwelle:** Einzelfund. Ein einziges gemischtes Token genügt; rein
   kyrillische oder rein griechische Wörter bleiben ohne Befund.
5. **Fixtures:**

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | `Anаlyse` mit kyrillischem `а` U+0430 | ein `mixed_script`-Finding auf dem ganzen Wort |
   | Positiv | `Mοdell` mit griechischem `ο` U+03BF | ein `mixed_script`-Finding auf dem ganzen Wort |
   | Positiv | `https://exаmple.org/pfad` mit kyrillischem `а` in der Domain | ein `mixed_script`-Finding auf `exаmple` trotz URL-Scope |
   | Negativ | `Fußgänger` | kein Befund; Umlaute und `ß` sind lateinisch |
   | Negativ | `Полностью` | kein Befund; das Wort ist vollständig kyrillisch |
   | Negativ | `Café` | kein Befund; `é` ist lateinisch |
   | Grenzfall | `H2O` | kein Befund; die Ziffer wird ignoriert, beide Buchstaben sind lateinisch |
   | Grenzfall | `Café` mit U+0301 | kein Befund; das Kombinationszeichen wird ignoriert |

6. **Fehlalarmfamilien und Fehlalarm-Erwartung:** Echte gemischte Fachbezeichner,
   mathematische Notation, Marken und technische Identifikatoren können absichtlich
   griechische, kyrillische und lateinische Buchstaben in einem Token verbinden. In
   gewöhnlicher deutscher Prosa ist die Fehlalarm-Erwartung niedrig, in mathematischen,
   multilingualen und technischen Texten höher. Die rekursive FP-Messung über alle 59
   Markdown-Dateien in `research/base-rates/human/` ergab 0 `mixed_script`-Treffer in
   0 Dateien; es waren daher keine Funddateien zu nennen.
7. **Severity, Meldung und erlaubte Aktion:** Im Sammelcheck `warning`, wie die übrigen
   Befunde aus `unicode_lint.py`. Die Meldung folgt dem Schema `Mixed scripts in word
   „Wort“; foreign characters: Zeichen (U+XXXX). Review manually.` Erlaubt sind Prüfung
   und manueller Hinweis. `--fix` verändert diesen Kind nicht, weil nur der Autor das
   beabsichtigte Zeichen kennt; ein Auto-Rewrite ist verboten.
8. **Keine Autorschaft:** Aus einem Treffer darf nicht abgeleitet werden, ob ein Mensch
   oder ein Sprachmodell den Text verfasst hat. Der Befund beschreibt ausschließlich ein
   technisches Zeichenartefakt.
9. **Version und Begründung:** 2026-09-02, Zielversion 5.27.0. Die bisherige
   `hidden_unicode`-Prüfung erkennt unsichtbare Codepoints, aber keine sichtbaren
   Doppelgänger aus fremden Schriftsystemen. Der neue `kind` schließt diese Lücke als
   manuell zu prüfende Erweiterung der Muster-43-Familie ohne automatische Korrektur.

## Aufgenommen: M20/M24/M26-Artefakt-Detektor (2026-09-02)

1. **Muster-ID, Name, Zweck:** Die Muster 20, 24 und 26 liefern den gemeinsamen Befund
   `ai_artifact`. M20 erfasst enge Prompt-Ablehnungs- und Chatbot-Floskeln, M24 technische
   Tool-, Zitier-, Export- und Reasoning-Reste, M26 direkte `utm_source`-Fingerabdrücke von
   KI-Diensten. Der Detektor findet unverarbeitete Fremdkörper, bevor der Stilpass beginnt.
2. **Texttypen, Modi, ausgeschlossene Spans:** Aktiv in Locker, Sachlich und Formal sowie in
   allen Texttypen. Es gibt absichtlich keine ausgeschlossenen Spans: Geprüft wird der
   Rohtext einschließlich Frontmatter, Codeblöcken, Inline-Code, URLs, Blockquotes,
   Anführungszeichen sowie Markdown- und HTML-Syntax. Der vorhandene Mention-Mechanismus
   greift nicht. Artefakte sind Fremdkörper, keine Wörter; `oaicite` bleibt auch in
   Backticks oder in einem erklärenden Satz ein Fund. Dadurch feuert die Regel bewusst auf
   Dokumentation der Artefakte.
3. **Regex:** Die drei Python-Regexe laufen case-insensitiv; M24 nutzt für den
   Thinking-Block zusätzlich einen lokalen Mehrzeilenanker.

   M24:

   ```regex
   contentReference(?:\s*\[\s*oaicite(?::[^\]\s]+)?\s*\])?|oaicite(?::[\w.-]+)?|oai_(?:cite|citation)|citeturn\d+(?:(?:search|image|news|file)\d+)?|turn\d+(?:search|image|news)\d+|iturn\d+image\d+|(?-i:\b[A-ZÄÖÜ][\wÄÖÜäöüß.-]{2,63}\+\d+\b)|attributableIndex|\[cite:\s?\d+(?:\s*,\s*\d+)*\]?|\[citation:\s*\d+(?:\s*,\s*\d+)*\]?|\[span_\d+\]\[(?:start|end)_span\]|\((?:start|end)_span\)|grok_render_citation_card_json|\bgrok_card\b|<grok-card\b|<grok:render\b|【\d+†L\d+(?:-\d+)?】?|\[(?:attached_file|web):\d+\]|ppl-ai-file-upload|:::writing\{|(?m:^[ \t]*>[ \t]*\*\*Thinking\*\*)|\[\^\d+\^\]|_\[unsupported block:\s*(?:think|search)\]_|</?think\b[^>]*>|\[\[\d+\]\](?:[ \t]*\[\[\d+\]\])+|ich\s+muss\s+das\s+Schritt\s+für\s+Schritt\s+durchdenken|zuerst\s+prüfe\s+ich,\s+was\s+der\s+Nutzer\s+wirklich\s+will
   ```

   M26:

   ```regex
   utm_source=(?:chatgpt(?:\.com)?|openai|claude\.ai|gemini\.google\.com|perplexity\.ai|copilot\.com)(?=&|$|[^\w.])
   ```

   M20:

   ```regex
   als\s+KI-Sprachmodell\b|als\s+KI-Modell\b|als\s+KI\s+kann\s+ich\s+nicht\b|ich\s+kann\s+keine\s+aktuelle[n]?\s+Information(?:en)?\s+bereitstellen\b|das\s+liegt\s+außerhalb\s+meiner\s+Fähigkeiten\b
   ```

4. **Dokument-Schwelle:** Ein einzelner Regex-Treffer genügt. Pro getroffenem
   Katalogmuster entsteht ein `ai_artifact`-Befund; bei mehreren Kategorien entstehen
   getrennte Befunde mit `pattern` 20, 24 oder 26. `evidence` enthält jeden gefundenen
   String in Textreihenfolge, `spans` die parallelen Python-Codepoint-Offsets im Rohtext.
5. **Fixtures:**

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | ChatGPT-Zitierrest `(turn0search0)` | `ai_artifact`, M24 |
   | Positiv | Gemini-Rest `[cite: 3]` | `ai_artifact`, M24 |
   | Positiv | URL mit `utm_source=chatgpt.com` | `ai_artifact`, M26 |
   | Negativ | URL mit `utm_source=newsletter` | kein Befund |
   | Negativ | „cite“ als normales Wort | kein Befund |
   | Negativ | Menschliche Rede „Ich hoffe, das hilft dir weiter“ | kein Befund; Schluss- und Entschuldigungsfloskeln bleiben judgment-only |
   | Grenzfall | Erklärender Satz mit Inline-Code `oaicite` | Befund; Use-Mention schützt Artefakte nicht |
   | Grenzfall | `utm_source=chatgpt.computer` | kein Befund; die Hostgrenze verhindert den Präfixtreffer |

6. **Fehlalarmfamilien und FP-Messung:** Technische Dokumentation, Testdaten und
   sicherheitsbezogene Erklärtexte nennen Artefakte absichtlich und werden dennoch
   gemeldet. Echte Support- oder Dialogtexte verwenden „Es tut mir leid, aber“ und „Ich
   hoffe, das hilft“ menschlich; beide Formen stehen deshalb nicht im Regex, sondern bleiben
   judgment-only im Katalog. M20 meldet nur ausdrückliche KI-Selbstbezüge. Die Syntax- und
   UTM-Formen haben eine sehr niedrige, M20 eine niedrige qualitative Fehlalarm-Erwartung. Die
   rekursive Messung vom 2026-09-02 über `research/base-rates/human/**/*.md` ergab **4
   Stringtreffer in 1 von 59 Dateien**, zusammengefasst in zwei Befunden. Alle vier stehen
   als dokumentierende Use-Mentions im eigenen Humanizer-Artikel: `oaicite`,
   `contentReference`, `turn0search0` und „Als KI-Modell“. Der
   bestehende FP-Korpus blieb ohne neuen Befund; seine Baseline wurde nicht verändert.
7. **Severity, Meldung, Aktion:** `warning`; der gefundene String steht in `evidence`, sein
   Originalspan in `spans`. Erlaubt sind Prüfung und vollständiges Entfernen eines echten
   Exportrests oder die bewusste Bestätigung einer dokumentierenden Erwähnung. Es gibt
   keinen Auto-Rewrite.
8. **Autorschaft:** Ein Treffer belegt einen Textfremdkörper oder eine katalogisierte
   Floskel, aber nicht die Verfasserschaft. Aus `ai_artifact` darf ausdrücklich nicht
   abgeleitet werden, ob ein Mensch oder ein Sprachmodell den Text verfasst hat.
9. **Versionsdatum und Begründung:** Aufgenommen am 2026-09-02 als Roadmap-Etappe 7. Die
   Formen standen bereits in den Katalogmustern 20, 24 und 26, fehlten aber vollständig im
   deterministischen Pfad. Einzelfunde sind hier günstiger und trennschärfer als weitere
   Stilheuristiken. Die materielle Regelaufnahme verlangt beim Release einen Minor-Bump;
   dieser begrenzte Parallellauf ändert keine Versionsdateien.

## Auslieferung: Patch-Bump-Pflicht

Installierte Plugins sind auf die Versionsnummer aus `plugin.json` gepinnt. Claude Code und
Codex vergleichen nur diese Zeichenkette; solange sie gleich bleibt, behalten sie ihre
zwischengespeicherte Kopie und liefern neue Commits nicht aus. Neuinstallationen ziehen
dagegen den Default-Branch und sehen jede Änderung sofort. Ohne Bump laufen beide Gruppen
also auseinander.

Deshalb gilt: Jede inhaltliche Änderung an ausgelieferten Dateien — Linter-Regeln,
`SKILL.md`, `references/`, `assets/`, `agents/` — bekommt im selben Commit-Zug mindestens
einen Patch-Bump. Reine Reparaturen an Tests, Entwicklerdoku oder interner Steuerung
brauchen keinen.

Zu bumpen sind: `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `CITATION.cff`, das
`SKILL.md`-Frontmatter, die Kopfzeilen von `references/patterns.md` und
`references/decision-tables.md`, `docs/coverage-matrix.md`, `WARP.md` sowie die Pins in
`tests/`. `test_release_metadata_stays_in_sync` erzwingt diese vollständige Liste;
`scripts/doctor.py` prüft separat den Versions-Sync von `SKILL.md` und den beiden
Plugin-Manifesten.
Beim Veröffentlichen gehört das hochladbare Skill-Paket an das Release. GitHub versiegelt
veröffentlichte Releases, deshalb muss das Archiv **beim Anlegen** dabei sein — nachträglich
nimmt das Release keine Datei mehr an, und der Tag-Name lässt sich danach für kein zweites
Release mehr verwenden:

```bash
make skill-bundle
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notes> --target main dist/humanizer-de.zip
```

`.claude-plugin/marketplace.json` führt bewusst keine Version: Steht sie an beiden Stellen,
gewinnt `plugin.json` ohne Warnung, und ein vergessener Wert dort verdeckt den gepflegten
im Marktplatz-Eintrag.

## Präzisiert: M64-Verbstämme gegen Fremd-Derivate

1. **Name und Zweck:** Bestehender M64-Befund `ai_marker_cluster`. Vier Verbmarker sollen
   ihre bisherigen Flexionsformen weiter erfassen, aber gleichlautende Substantiv-Derivate
   fremder Lexeme nicht mehr als das jeweilige Verb ausweisen.
2. **Scope:** Alle Modi und Texttypen des bestehenden Befunds. Geändert werden nur
   `beleuchten`, `eintauchen`, `unterstreichen` und `aufzeigen`; alle anderen AI_MARKERS,
   ABSTRACTA, COPULA_AVOIDANCE und die geschützten Spans bleiben unverändert.
3. **Logik:** Die vorhandene Override-Mechanik nutzt nun die case-insensitiven Muster
   `\bbeleucht(?!ung|er)\w*\b`, `\beintauch(?!ung)\w*\b`,
   `\bunterstreich(?!ung)\w*\b` und `\baufzeig(?!ung)\w*\b`. Die negativen Lookaheads
   verengen ausschließlich die bisherige Stamm-Matchmenge. Präteritum, Partizip mit
   `ge` und getrennte Partikeln werden bewusst nicht neu erschlossen.
4. **Schwelle:** Unverändert mindestens drei AI_MARKER-Treffer pro Text. Zwei echte
   Verbformen plus ein ausgeschlossenes Derivat erzeugen keinen Cluster.
5. **Fixtures:**

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | `beleuchtet` + `eintauchen` + `aufzeigt` | `ai_marker_cluster` |
   | Positiv | bisher erfasste Flexionsformen aller vier Verben | jeweils ein Markertreffer |
   | Positiv | substantiviertes „das Beleuchten des Themas“ | ein Treffer für `beleuchten` |
   | Negativ | dreimal `Beleuchtung` im Fototext | kein Befund |
   | Negativ | `Beleuchtung`, `Beleuchtungen`, `Beleuchter` | kein Treffer für `beleuchten` |
   | Negativ | `Eintauchung`, `Unterstreichung(en)`, `Aufzeigung` | kein Treffer für die Verben |
   | Grenzfall | zwei Verbformen plus einmal `Beleuchtung` | kein Cluster |
   | Grenzfall | `unterstrich`, `aufgezeigt`, `taucht ... ein` | wie bisher nicht erfasst |

6. **Fehlalarmfamilie:** Themengebundene Sach- und Fachprosa über Beleuchtung sowie
   sprachliche oder typografische Unterstreichungen. Die ausgeschlossenen Nomen bezeichneten
   bislang reale Gegenstände oder Verfahren, während die Evidenz fälschlich das Verb nannte.
7. **Severity, Meldung, Aktion:** `warning`, Evidenzstruktur und manueller Prüfauftrag
   bleiben unverändert. Es gibt keinen Auto-Rewrite.
8. **Autorschaft:** Der Befund erlaubt weiterhin keine Aussage darüber, ob ein Mensch oder
   ein Sprachmodell den Text verfasst hat.
9. **Version und Begründung:** 2026-08-28, Zielversion 5.24.1. Anlass ist ein reproduzierter
   Fehlalarm auf themengebundener Sachprosa außerhalb der FP-Baseline-Genres: In einem
   Beleuchtungs-Fachtext erzeugten drei Nomen einen M64-Cluster, dessen Evidenz das falsche
   Lexem `beleuchten` nannte.

## Erweitert: M8-Negationsantithese als Dichtebefund

1. **Muster-ID, Name, Zweck:** Muster 8, `negation_antithesis_cluster`. Der Befund ergänzt
   die bestehende lokale `negation_parallelism`-Prüfung um gehäufte Formen „nicht A,
   sondern B“, „A und nicht B“ und den satzfinalen Kontrast-Schwanz „A, nicht B.“,
   ohne deren Kind oder Schwelle zu ändern.
2. **Texttypen, Modi, ausgeschlossene Spans:** Aktiv in allen Texttypen und Modi. Code,
   Inline-Code, Frontmatter, URLs, Markdown-/HTML-Syntax, Inline-Zitate und
   Markdown-Hervorhebungen werden über die vorhandenen Scope- und Use-Mention-Mechanismen
   ausgeblendet. Auch Treffer, die einen solchen Span nur teilweise überlappen, zählen nicht.
3. **Erkennungslogik:** Drei case-insensitive Regexe erfassen die Formen „nicht A,
   sondern B“, „A und nicht B“ und den nachgestellten Kontrast-Schwanz „A, nicht B.“
   mit höchstens 80 Zeichen je Antithesenarm. Der Schwanz zählt nur satzfinal: Das
   Schlusszeichen `[.!?]` braucht folgenden Leerraum oder Textende und darf nicht auf
   ein Einzelzeichen-Token folgen — Dezimal-, Tausender-, Domain-, Abkürzungs-
   („z. B.“) und Ordinalpunkte („am 3. Mai“) gelten nicht als Satzende. Überlappende
   Treffer der Regexe zählen einmal. „Nicht nur … sondern auch“ bleibt ausgeschlossen;
   beim Schwanz gilt derselbe Ausschluss für „, nicht nur/allein/bloß/ausschließlich“.
   Offensichtliche beidseitige Zeit-, Datums- und Zahlkorrekturen einschließlich geläufiger
   Einheiten sowie Monat-Jahr-Angaben zählen nicht.
4. **Schwelle:** Warnung erst ab mindestens vier Treffern und mindestens 3,0 Treffern pro
   1.000 Wörter. Im Repo-Korpus lag das Maximum bei einem Rohkandidaten pro Dokument. Fünf
   Fachartikel von onlinemarketing.de ergaben 0/0/0/0/1 Kandidaten; das Maximum betrug 0,45
   pro 1.000 Wörter. Der auslösende Praxistext lag bei 7/1.318 Wörtern = 5,31 pro 1.000.
5. **Fixtures:**

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | gemischter Cluster aus beiden Formen | neuer Dichtebefund |
   | Positiv | vier pointierte „nicht A, sondern B“-Sätze | neuer Dichtebefund |
   | Positiv | vier pointierte „A und nicht B“-Sätze | neuer Dichtebefund |
   | Negativ | einzelne inhaltlich begründete Antithese | kein Befund |
   | Negativ | vier eindeutige Wochentags-/Monatskorrekturen | kein Befund |
   | Negativ | vier Zahlkorrekturen mit Einheiten oder Monat-Jahr-Angaben | kein Befund |
   | Negativ | vier Treffer unterhalb der Dokumentdichte | kein Befund |
   | Grenzfall | Cluster nur in Zitaten, Code und Hervorhebungen | kein Befund |
   | Grenzfall | Schutzspan nur in einem Antithesenarm | kein Befund |
   | Grenzfall | zwei Sätze mit je zwei überlappenden Formen | zwei statt vier Treffer, kein Befund |
   | Grenzfall | vier „nicht nur … sondern auch“-Korrelationen | kein Befund |
   | Positiv | vier satzfinale Schwanz-Formen „A, nicht B.“ | neuer Dichtebefund |
   | Positiv | gemischter Cluster aus Schwanz- und klassischen Formen | neuer Dichtebefund |
   | Negativ | vier beidseitige Wert-Korrekturen in Schwanz-Form („am Dienstag, nicht am Mittwoch.“) | kein Befund |
   | Negativ | vier „, nicht nur“-Korrelationen | kein Befund |
   | Grenzfall | Schwanz-Form ohne Satzschlusszeichen dahinter | kein Treffer, kein Befund |
   | Grenzfall | Schwanz überlappt klassische „nicht A, sondern B“-Form | zählt einmal, kein Befund |

6. **Fehlalarmfamilien:** Inhaltliche Abgrenzungen und sachliche Korrekturen sind
   syntaktisch nicht allgemein von Pointen zu trennen. Automatisch ausgeschlossen wird nur
   die sichere Teilmenge; das hohe Doppeltor lässt einzelne und dünn verteilte zulässige
   Antithesen passieren. Dichte fachliche Abgrenzungen bleiben ein manueller Prüffall.
7. **Severity, Meldung, Aktion:** `warning`; Evidenz enthält Zahl, Dichte, Textstellen und
   Spans. Erlaubt ist die manuelle Funktionsprüfung, kein Auto-Rewrite.
8. **Autorschaft:** Der Befund beschreibt eine Wiederholung im Text und erlaubt keine
   Aussage darüber, ob ein Mensch oder ein Sprachmodell ihn verfasst hat.
9. **Version und Begründung:** 2026-07-31, Version 5.11.0. Ein echter Fachbeitrag
   enthielt sieben Vorkommen, vier davon im Schlussabschnitt; der bisherige Linter erfasste
   ausschließlich direkt benachbarte Verneinungsanaphern.
   Präzisierung vom 2026-08-11: Der erste Regex akzeptiert neben dem Komma auch die
   katalogisierten Dash-Trenner. Die Schwellen bleiben unverändert. Damit kann Muster 16
   überlappende „nicht X – sondern Y“-Spans zuverlässig Muster 8 überlassen.
   Erweiterung vom 2026-08-20, Version 5.21.3: dritter Regex für den nachgestellten
   Kontrast-Schwanz „A, nicht B.“ (satzfinal). Anlass war eine externe Meldung aus der
   Praxis (Kurztext-Set mit unsichtbaren Kontrastfiguren). Messung am 50-Texte-Korpus:
   GPT 0/10, Claude 8 Rohtreffer in 5/10, echte Menschen (pre2022) 4 in 3/20, own 4 in
   4/10 — Claude-Marker-Charakter. Cluster-Wirkung im vollen Pipeline-Lauf: vorher 0/50
   Texte mit Dichtebefund, nachher genau 1 (claude-09, count 4, Dichte 5,1/1000); 0 neue
   Fehlalarme auf beiden Menschen-Bedingungen. `left` deckt bewusst nur den Operanden
   direkt vor dem Komma, damit der Fakten-Carve-out beidseitige Wert-Korrekturen weiter
   ausschließt. Schwellen unverändert (4 + 3,0/1.000). Die im selben Befund gemeldete
   Satzgrenzen-Form („kein X. Sondern Y.“) und ein ODER-Pfad für Kurztexte unter 500
   Wörtern sind bewusst nicht aufgenommen: 0 Korpus-Belege bzw. keine FP-Baseline für
   das Zielregister — beide warten auf das Werbe-/Social-Korpus
   (research/base-rates/NEXT.md, Abschnitt Kurztext-Befund).
   Nachtrag nach Review vom selben Tag: Der Satzend-Anker bekam zwei Guards (Leerraum-
   Lookahead gegen Dezimal-/Tausender-/Domain-Punkte, Lookbehind gegen Einzelzeichen-
   Token für Abkürzungs- und Ordinalpunkte), das Wert-Präfix des Fakten-Carve-outs
   wurde um „ab“ und „seit“ erweitert (schließt „ab Mai, nicht ab Juni.“ beidseitig
   als Korrektur aus). Bekannte, bewusst offene Grenzfälle: dichte juristische
   Abgrenzungsprosa („zuständig ist X, nicht Y.“) kann bei vier Treffern in kurzer
   Strecke clustern — Register liegt außerhalb der FP-Baseline, bleibt manueller
   Prüffall nach Punkt 6; ein Roh-Schwanz-Treffer nimmt seine Spanne wie alle
   Antithesen-Kandidaten aus der M16-Dash-Zählung (Entscheid vom 2026-08-11), im
   Repo-Bestand verliert dadurch kein Dokument einen Dash-Befund.

## Erweitert: M43 um Tags-Block und Variation Selectors

1. **Muster-ID, Name, Zweck:** Muster 43, `hidden_unicode`. Die bestehende Zeichenliste
   deckte sechs Klassen ab und ließ die beiden Trägerklassen aus, mit denen sich heute
   beliebiger Text unsichtbar einbetten lässt. Gemessen am 2026-08-14: Von acht geprüften
   Klassen rutschten sieben durch, gefunden wurde nur das bereits abgedeckte U+200B.
2. **Texttypen, Modi, ausgeschlossene Spans:** Aktiv in allen Texttypen und Modi. Versteckte
   Zeichen gelten wie bisher auch in Code und URLs als unsicher, deshalb greift hier
   ausdrücklich **kein** Scope-Ausschluss.
3. **Erkennungslogik:** Drei neue Bereiche in `HIDDEN_RANGES` — U+E0000–U+E007F (Tags-Block),
   U+FE00–U+FE0F (Variation Selectors) und U+E0100–U+E01EF (Supplement). Zwei
   Ausnahmefunktionen: `is_emoji_variation_selector` lässt U+FE0E/U+FE0F stehen, wenn davor
   ein Emoji-Codepoint oder eine Keycap-Basis (`0-9`, `#`, `*`) steht.
   `is_flag_tag_member` lässt Tag-Zeichen stehen, wenn sie in einer zusammenhängenden Kette
   liegen, die unmittelbar auf U+1F3F4 folgt, mit U+E007F endet **und** genau `gbeng`,
   `gbsct` oder `gbwls` buchstabiert. Die geschlossene Liste ist Absicht: Der Codex-Review
   vor dem Commit fand, dass die reine Strukturprüfung umgehbar ist — `🏴` plus beliebige
   Tag-Zeichen plus `U+E007F` schmuggelt sonst jeden Text an der Ausnahme vorbei. Der Fall
   steht als Fixture in der Suite.
4. **Schwelle:** Einzelfund. Ein einziges verstecktes Zeichen ist ein Befund; eine Dichte
   ergibt hier keinen Sinn, weil eine Nutzlast aus einem Zeichen bestehen kann.
5. **Fixtures** (in `tests/test_unicode_lint.py`):

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | Tag-Zeichen als ASCII-Nutzlast zwischen Wörtern | ein Befund je Zeichen, `fix` entfernt sie |
   | Positiv | U+E0001 Language Tag | Befund |
   | Positiv | U+FE00, U+FE0E, U+FE0F, U+E0100, U+E01EF nach einem Buchstaben | Befund |
   | Negativ | Subdivision-Flaggen gbsct, gbwls, gbeng | kein Befund, `fix` lässt sie unverändert |
   | Negativ | Emoji mit U+FE0F und Keycap-Ziffer | kein Befund |
   | Negativ | Emoji-ZWJ-Sequenzen (bestehender Test) | kein Befund |
   | Positiv | U+1F3F4 plus Tag-Kette plus U+E007F mit fremder Nutzlast (`secret`, `123`, `!`) | Befund — Tarnung, keine Flagge |
   | Grenzfall | dieselben Tag-Zeichen ohne vorangehendes U+1F3F4 | Befund — Nutzlast, keine Flagge |
   | Grenzfall | U+1F3F4 plus Tag-Kette ohne abschließendes U+E007F | Befund, Basis-Emoji bleibt stehen |
   | Grenzfall | U+FE0F als erstes Zeichen des Textes | Befund, kein Absturz beim Blick nach links |

6. **Fehlalarmfamilien:** Variation Selectors kennzeichnen zwei legitime Dinge, die dieser
   Linter trotzdem meldet. Erstens Schriftvarianten von CJK-Ideographen (`一` plus U+E0100).
   Zweitens die standardisierten Mathematik-Varianten aus `StandardizedVariants.txt`, etwa
   `∪` plus U+FE00 für die Serifenform. Beides ist in deutscher Gebrauchsprosa praktisch
   ausgeschlossen, und `--fix` lässt das Basiszeichen unversehrt — aus `∪` wird `∪`, nicht
   nichts. Wer mathematischen oder CJK-Satz bearbeitet, prüft den Befund von Hand. Bewusst so
   entschieden, gefunden im Codex-Review.
   Der Emoji-Carve-out folgt der Basiszeichen-Liste von `is_emoji_codepoint` und erbt deren
   Grenzen. Gemessene Baseline: 55 Dateien aus `tests/fp_corpus`, `tests/corpus`,
   `tests/scenarios`, den 20 echten Menschentexten und allen ausgelieferten Dokumenten —
   **null neue Treffer**, der einzige Fund ist das absichtliche U+200B in
   `tests/corpus/case_01_input.md`.
7. **Severity, Meldung, Aktion:** unverändert `hidden_unicode` mit der bestehenden Meldung;
   `--fix` entfernt ersatzlos. Kein Auto-Rewrite.
8. **Keine Autorschaft:** Aus einem Fund folgt keine Herkunftsaussage. Die real ausgerollten
   Text-Wasserzeichen arbeiten statistisch über die Token-Auswahl und sind über Zeichen
   weder nachweisbar noch entfernbar. Der Befund begründet Textreinigung, sonst nichts.
9. **Version und Begründung:** 2026-08-14, aufgenommen mit 5.19.0. Neues
   Erkennungsverhalten, deshalb Minor statt Patch.

**Bewusst nicht aufgenommen**, weil in mehrsprachigem oder fachlichem Text legitim:
U+200E/U+200F (Bidi-Marken), U+061C, U+180E, die Hangul-Füllzeichen U+115F/U+1160/U+3164 und
U+2800 (Braille-Blank). Sie rutschen weiterhin durch; das ist eine offene Entscheidung, kein
Versehen.

## Aufgenommen: M16-Gedankenstrich-Cluster

1. **Muster-ID, Name, Zweck:** Muster 16, `dash_cluster`. Der Befund macht gehäufte
   Gedankenstriche und Dash-Ersatzzeichen als Satzzeichen deterministisch erreichbar, ohne
   einzelne Gedankenstriche oder legitime Trenner zu melden.
2. **Texttypen, Modi, ausgeschlossene Spans:** Aktiv in Locker, Sachlich und Formal. Code,
   URLs, Frontmatter und technische Markdown-/HTML-Spans werden längentreu maskiert.
   `foreign_voice_ranges` plus `overlaps_mention` schließen Zitate, Blockquotes und
   Hervorhebungen aus. Markdown-Überschriften zählen nie. Wort-Bindestriche und
   Zahlenbereiche bleiben ebenfalls ausgeschlossen.
3. **Erkennungslogik:** `–` und `—` sowie horizontal umgebene ` -- ` und ` - ` sind
   Kandidaten. `\d[^\S\r\n]*(?:[–—]|--?)[^\S\r\n]*\d` schützt auch Bereiche mit
   Leerraum. Treffer, die mit vorhandenen `NEGATION_PARALLELISM_RES`- oder
   `ANTITHESIS_RES`-Spans überlappen, bleiben Muster 8 vorbehalten. Gewertet wird je
   Absatz; Evidenz und Spans verweisen auf den Originaltext.
4. **Schwelle, zwei Tore:** Ein Finding entsteht bei Konzentration ODER Verteilung.
   *Konzentration:* fünf Kandidaten in einem Absatz und mindestens 15,0 Treffer pro 1.000
   Absatzwörter. Drei reichten nicht: Der saubere Spiegelungs-Text hat nach allen
   Ausschlüssen vier Kandidaten aus zwei legitimen Einschüben. Unter den 39 geprüften
   Menschentexten erreicht nur die lange Plenarrede mindestens fünf Kandidaten in einem
   Absatz; ihre Dichte liegt bei 11,03. Der Positivfall liegt bei 5 und 116,28.
   *Verteilung:* mindestens vier Absätze mit je mindestens drei Kandidaten. Dieses Tor fängt
   den häufigeren KI-Fall — gepaarte Em-Dashes über viele Absätze verstreut, je Absatz
   wenige. Drei qualifizierende Absätze reichen nicht: Der Nietzsche-Text erreicht genau
   drei (je drei ` - `), das lange Urteil zwei. Vier hält die 39 Menschentexte geschlossen
   stumm und lässt den verteilten Testfall mit sechs Absätzen feuern.
5. **Fixtures:**

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | fünf gehäufte Spaced-Em-Dashes | `dash_cluster` |
   | Positiv | fünf gehäufte Halbgeviertstriche | `dash_cluster` |
   | Positiv | fünf gehäufte ` -- ` oder ` - ` | `dash_cluster` |
   | Negativ | Überschriften, `KI-Tell`, `2D-Spiegelung`, `E-Mail` | kein Befund |
   | Negativ | `2019–2021`, `S. 12–15`, `10–20 %`, `10 – 20` | kein Befund |
   | Negativ | Zitat, Blockquote, Inline-Code und Hervorhebung | kein Befund |
   | Grenzfall | zwei legitime gepaarte Einschübe, vier Kandidaten | kein Befund |
   | Grenzfall | fünf Kandidaten unter 15,0 pro 1.000 Absatzwörter | kein Befund |
   | Grenzfall | fünf „nicht X – sondern Y“-Antithesen | nur Muster 8 |

6. **Fehlalarmfamilien:** Literarische und historische Prosa, Plenarreden, Rechtstexte,
   Definitionslisten und legitime Einschübe nutzen Gedankenstriche ebenfalls häufig. Das
   Doppeltor lässt die gemessenen Fälle stumm; ungewöhnlich dichte menschliche Prosa bleibt
   ein manueller Prüffall. Erwartet wird eine niedrige, nicht aus Autorschaft abgeleitete
   Fehlalarmrate.
7. **Severity, Meldung, Aktion:** `warning`; Evidenz enthält Zahl, maximale Absatzdichte,
   Glyphen und Originalspans. Erlaubt ist die manuelle Satzbauprüfung, niemals ein
   automatischer Glyph-Tausch oder Auto-Rewrite.
8. **Autorschaft:** Der Befund beschreibt nur ein Interpunktionscluster. Er erlaubt keine
   Aussage darüber, ob ein Mensch oder ein Sprachmodell den Text verfasst hat.
9. **Empirische Grundlage, an eigenen deutschen Daten:** Muster 16 wurde zuerst aus
   Fremdquellen übernommen (englische `exmergo`-Messung, Gibbs-Artikel „P16
   Claude-spezifisch"). Am 2026-08-11 erstmals an eigenen deutschen Ausgangstexten gemessen:
   Claude setzt im Schnitt **1,56 Gedankenstriche**, GPT **0,56** — fast dreimal so viele.
   Das ist der Beleg, dass der Detektor ein reales deutsches Signal fasst, kein aus dem
   Englischen entliehenes. Bemerkenswert die Gegenrichtung: GPT verrät sich stattdessen an
   geringerer Satzlängen-Streuung (Muster 55). Die beiden Modelle haben verschiedene
   Fingerabdrücke — Rohdaten in `research/base-rates/NEXT.md`.
10. **Version und Begründung:** 2026-08-11, aufgenommen mit 5.18.0. Neues Erkennungsverhalten,
    wo Muster 16 zuvor judgment-only war — Minor-Bump, Präzedenz v5.8.0 (Muster 8/13).
    Aufnahme nach byte-identischer FP-Baseline und einer Nullmessung über 20 Basisraten- plus
    19 Registertexte.

## Präzisiert: `mixed_address` bei Inline-Zitaten

1. **Name und Zweck:** Bestehender Registerbefund `mixed_address`, kein Katalogmuster.
   Eindeutig gepaarte Inline-Zitate sollen im aktiven `--precise`-Pfad wie Blockquotes als
   fremde Stimme gelten.
2. **Scope:** Alle Modi; im Stilprofil und bei aktivem spaCy-Präzisionspfad. Code,
   Frontmatter, Tabellen, HTML-Syntax und Blockquotes bleiben wie bisher geschützt.
3. **Logik:** Die validen Quote-Patterns des Evidence-Gates maskieren gepaarte deutsche,
   Schweizer, englische und gerade Inline-Zitate längentreu vor der
   Registerzählung. Der kompatible Default bleibt unverändert.
4. **Schwelle:** Der Registerbefund entsteht weiterhin erst, wenn ungeschützte `du`- und
   `Sie`-Formen gemeinsam vorkommen.
5. **Fixtures:**

   | Typ | Textfamilie | Erwartung |
   |---|---|---|
   | Positiv | Du-Stimme + deutsches Inline-Zitat mit `Sie` | kein `mixed_address` in `--precise` |
   | Positiv | Du-Stimme + gerades Inline-Zitat mit `Sie` | kein `mixed_address` in `--precise` |
   | Positiv | Sie-Stimme + Schweizer Inline-Zitat mit `Du` | kein `mixed_address` in `--precise` |
   | Negativ | unzitierter echter Wechsel von `Du` zu `Sie` | `mixed_address` |
   | Negativ | nur ein Sachwort zitiert, echte `Sie`-Anrede unzitiert | `mixed_address` |
   | Negativ | Zitat plus weitere echte `Sie`-Anrede außerhalb | `mixed_address` |
   | Grenzfall | ungepaarte Anführungszeichen | konservativ nicht maskieren |
   | Grenzfall | mögliche Plural-Anapher (`Die Teams ... Sie ...`) | manueller Kandidat bleibt |

6. **Fehlalarmfamilien:** Zitate, UI-Wortlaut, Interview- und Dialogbeispiele. Die sichere
   gepaarte Teilmenge fällt im Präzisionspfad weg; Plural-Coreference bleibt qualitativ
   zu prüfen, weil `Sie` grammatisch nicht sicher von der Höflichkeitsform trennbar ist.
7. **Severity, Meldung, Aktion:** `warning` bleibt. Die Meldung nennt jetzt einen möglichen
   Anredewechsel und verlangt die Prüfung auf Anapher oder Zitat. Kein Auto-Rewrite.
8. **Autorschaft:** Der Befund erlaubt weiterhin keine Aussage zur Verfasserschaft.
9. **Version und Begründung:** 2026-07-30, Version 5.10.5. Der Audit von 20 eigenen Posts
   zeigte zitierte Fremdstimme und anaphorisches `Sie` als wiederkehrende Fehlalarmfamilien.
   Automatisiert wird nur die eindeutig trennbare Zitatfamilie.

## Aufgenommen: M72-Kandidatenhinweis

1. **Muster-ID, Name, Zweck:** Muster 72, `address_validation_candidate`. Der Hinweis findet
   enge Formulierungen, die Gefühle, Selbstbild oder Vorgeschichte des Adressaten ungefragt
   als Tatsache behandeln. Er ist ein Kandidat, kein bestätigter Befund.
2. **Texttypen, Modi, ausgeschlossene Spans:** Aktiv in Locker, Sachlich und Formal.
   Geschützte Codeblöcke, Inline-Code, URLs, Frontmatter, Markdown-/HTML-Syntax und Zitate
   werden vor der Prüfung ausgeblendet oder als Use-Mention übersprungen.
3. **Erkennungslogik:** Case-insensitive Python-Regex:

   ```regex
   \b(?:du\s+bist\s+nicht\s+(?:zu\s+|einfach\s+nur\s+)?(?:sensibel|empfindlich|emotional|bedürftig|anspruchsvoll|schwierig|schwach|faul|anstrengend)|du\s+(?:überreagierst\s+nicht|reagierst\s+nicht\s+über|fühlst\s+nicht\s+falsch)|deine\s+gefühle\s+sind\s+(?:völlig\s+)?(?:berechtigt|valide|verständlich)|deine\s+reaktion(?:en)?\s+(?:ist|sind)\s+(?:völlig\s+)?(?:berechtigt|valide|verständlich)|du\s+wurdest\s+(?:nur\s+)?(?:zu\s+lange\s+)?(?:nicht\s+ernst\s+genommen|kleingehalten|emotional\s+vernachlässigt))\b
   ```

   Bewusst ausgeschlossen sind „Es liegt nicht an dir“, offenes „Du wurdest nur ...“ und
   „Du bist nicht zu spät“.
4. **Schwelle:** Ein Regex-Treffer erzeugt einen advisory Kandidatenhinweis. Die Schwelle
   bestätigt Muster 72 nicht; der Kontext entscheidet.
5. **Fixtures:**

   | Typ | Text | Erwartung |
   |---|---|---|
   | Positiv | „Du bist nicht zu sensibel. Die anderen haben dir das nur eingeredet.“ | Kandidatenhinweis |
   | Positiv | „Deine Gefühle sind völlig valide, auch wenn du ihren Ursprung noch nicht kennst.“ | Kandidatenhinweis |
   | Positiv | „Du wurdest nur zu lange nicht ernst genommen.“ | Kandidatenhinweis |
   | Negativ | „Du bist nicht zu spät; die Besprechung beginnt um zehn.“ | kein Treffer |
   | Negativ | „Es liegt nicht an dir. Der Server weist derzeit alle Konten ab.“ | kein Treffer |
   | Negativ | „Der Sensor ist nicht zu empfindlich, sondern falsch kalibriert.“ | kein Treffer |
   | Grenzfall | „Du bist nicht zu empfindlich; der Sensor ist falsch kalibriert.“ | Regex matcht; Meldung bleibt Kandidat, wörtlich-technischer Kontext kann den Befund verwerfen |
   | Grenzfall | „Deine Reaktion ist verständlich, nachdem du den Ablauf geschildert hast.“ | Regex matcht; Meldung bleibt Kandidat, bei Beratungsauftrag und belegtem Gesprächskontext zulässig |

6. **Fehlalarmfamilien:** Wörtlich-technische Vergleiche mit „du“, ausdrücklich beauftragte
   Beratung oder Coaching, das Aufgreifen bereits genannter Gefühle sowie Zitat, Interview
   und literarischer Dialog. Fehlalarme sind bei den beiden ungeschützten Kontextfamilien
   technisch und Beratung qualitativ zu erwarten; deshalb nur `info`, nie `warning`.
7. **Severity, Meldung, Aktion:** `info`, zusätzlich `advisory: true`. Meldung:
   „Kandidat für unbelegte Adressaten-Validierung: Kontext prüfen (Beratungsauftrag? Zitat?
   Sachklärung?)“. Erlaubt ist nur die manuelle Kontextprüfung. Kein Auto-Rewrite.
8. **Autorschaft:** Ein Treffer erlaubt keine Aussage darüber, ob ein Mensch oder ein
   Sprachmodell den Text verfasst hat.
9. **Version und Begründung:** 2026-07-23, Version 5.10.0. Aufnahme als enger Hinweis, weil
   die vorhandene `info`-Severity Kandidaten klar von Warnungen und Blockern trennt und die
   bekannten Grenzfälle ausdrücklich zur manuellen Prüfung zwingt.

## Abgelehnt: M71-Marker-Lint

- **Muster-ID, Kandidatenname, Zweck:** Muster 71, Marker-Lint für retroaktive
  Scheinnuance.
- **Geprüfte Erkennungslogik:** Regex auf
  `Genauer gesagt|Fairerweise|Eigentlich ist es komplizierter`.
- **Entscheidung:** abgelehnt. Die Marker leiten häufig echte Präzisierung ein. Ob der
  Nachsatz nur weicher wiederholt oder eine Bedingung, Ausnahme, Kennzahl, Ursache oder
  Gegenposition ergänzt, entscheidet erst der Neuigkeits- und Löschtest. Diese Entscheidung
  kann die Regex nicht leisten.
- **Folge:** Muster 71 bleibt judgment-only. Es gibt keine Severity, keinen automatischen
  Hinweis und keinen Auto-Rewrite.
- **Version und Begründung:** 2026-07-23, Version 5.10.0. Der Kandidat scheitert an
  Positiv-/Negativ-Trennbarkeit und der zu erwartenden Fehlalarmrate.
