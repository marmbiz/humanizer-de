# Die 10 häufigsten deutschen KI-Tells

Kompakte Checkliste zum schnellen Gegenlesen, auch ohne installierten Skill nutzbar. Der
vollständige Katalog mit 69 Mustern, Beispielen und Abgrenzungen steht in
[references/patterns.md](../references/patterns.md).

**Grundregel: Cluster zählen, nicht Einzelsignale.** Ein einzelner Gedankenstrich, ein
`zudem` oder saubere Typografie beweist gar nichts. Verdächtig wird ein Text erst, wenn
mehrere unabhängige Muster zusammenkommen.

1. **Gedankenstrich-Cluster (Muster 16):** mehrere `–` oder `—` pro Absatz, gepaarte
   Einschübe (`Der Bericht – der drei Kontinente abdeckte – kam …`) oder die Punchline
   `Es geht nicht um X – es geht um Y`. Ein einzelner Gedankenstrich ist legitim.
2. **Werbesprache und Superlative (Muster 2):** `atemberaubend`, `einzigartig`,
   `spektakulär`, dazu übersetzte Hype-Idiome wie `das ändert alles`. Marketingsprache an
   Stellen, die neutrale Beschreibung verlangen.
3. **KI-Marker-Vokabular (Muster 64):** `beleuchten`, `eintauchen`, `nahtlos`,
   `spannend`, `entscheidend`, `die digitale Landschaft`, `das Zusammenspiel`. Einzeln
   unauffällig; ab drei Markern im selben Text ein Cluster.
4. **Mechanische Konjunktionen (Muster 4):** jeder zweite Absatz beginnt mit
   `darüber hinaus`, `zudem`, `des Weiteren` oder `außerdem`. Die Übergänge kommen aus
   dem Baukasten statt aus dem Inhalt.
5. **Vage Autoritäten (Muster 11):** `Studien zeigen`, `Experten sind sich einig`,
   `Branchenberichte belegen`, und nirgends steht eine konkrete, prüfbare Quelle.
6. **Abschnitts-Zusammenfassungen (Muster 5 und 6):** Absätze enden mit
   `zusammenfassend`, `insgesamt` oder `kurz gesagt`, und am Textende steht ein Fazit,
   das niemand bestellt hat.
7. **Negative Parallelismen (Muster 8):** `nicht nur … sondern auch`, symmetrische
   Gegenüberstellungen, abgehackte Verneinungen wie `kein Raten.` am Satzende.
8. **Regel der Drei (Muster 9):** auffällig oft genau drei parallele Adjektive oder
   Beispiele (`vielfältig, kreativ und widerstandsfähig`), Listen mit glatten 5, 7 oder
   10 Punkten ohne sachlichen Grund.
9. **Asymmetrische Anführungszeichen (Muster 46):** deutsches öffnendes `„` mit falschem
   Schlusszeichen, also `„Text”` oder `„Text"`. Durchgängig gerade Anführungszeichen sind
   dagegen meist ein CMS-Artefakt und kein KI-Signal.
10. **Gleichförmiger Satzrhythmus (Muster 55):** fast alle Sätze gleich lang, fast alle
    beginnen mit dem Subjekt. Der Text ist korrekt und lesbar, aber metrisch monoton.

**Vorsicht vor Fehlalarmen.** Saubere Grammatik, korrekte Quellen und sachliche Klarheit
sind keine KI-Tells. Wer nur ein einzelnes Signal findet, hat nichts gefunden.

Automatisch prüfen lässt sich das im geklonten Repository mit dem Sammelcheck:

```bash
python3 scripts/humanizer_audit.py --file text.md --mode sachlich
```

Teil von [humanizer-de](https://github.com/marmbiz/humanizer-de), dem deutschen
Stil-Editor für Claude Code und Codex.
