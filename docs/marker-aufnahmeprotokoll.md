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
