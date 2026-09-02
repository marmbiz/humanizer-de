# Register Profiles

Pass 0 erzeugt eine kleine Stilkarte. Sie ist kein Schreibauftrag, sondern ein Schutz gegen generische Lockerheit.

## Profilfelder

| Feld | Beispiele | Zweck |
|---|---|---|
| `mode` | locker, sachlich, formal | Aggressivität der Eingriffe |
| `deictic_center` | ich, wir, man, neutral, institutionell | Sprecherposition stabil halten; keine neue Ich-/Wir-Perspektive erfinden |
| `address` | du, Sie, wir, man, neutral | Anrede stabil halten |
| `distance` | nah, neutral, institutionell | Keine falsche Nähe einbauen |
| `sentence_shape` | kurz, gemischt, lang/fachlich | Rhythmus am Texttyp messen |
| `word_level` | einfach, gemischt, fachlich | Wortniveau nicht pauschal glätten |
| `paragraph_openers` | knapp, variabel, ausformuliert | Typische Absatzanfänge erhalten |
| `paragraph_shape` | knapp, normal, dicht | Struktur nicht normieren |
| `terms` | Fachwörter, Produktnamen | Terminologie stabil halten |
| `particles` | keine, sparsam, prägend | Modalpartikeln nur im passenden Register |
| `punctuation` | Doppelpunkt, Gedankenstrich, Klammern | Lieblingszeichen nicht mechanisch austreiben |
| `quality_exceptions` | Tippfehler, echte Grammatikfehler | Schlechte Eigenheiten nicht konservieren |

## Konfliktordnung

Quelle und belegte Aussage haben Vorrang vor Stil. Danach folgen Recht/Technik, Modus, Zielprofil, Rhythmus und erst zuletzt Lexik.

## Formal-Modus

Im Formal-Modus wird keine Stimme eingebracht. Passiv, Nominalstil und gleichmäßiger Rhythmus bleiben stehen, wenn sie fach-, rechts- oder wissenschaftskonventionell sind.

## Locker-Modus

Locker bedeutet nicht erfunden persönlich. Stimme darf nur aus Schreibprobe, Nutzerangabe oder vorhandenem Textmaterial kommen. Modalpartikeln sind erlaubt, aber nur sparsam und nicht mechanisch.

## Maschinenlesbare Zielkorridore

`references/style-targets.json` hält pro Modus (`locker`, `sachlich`, `formal`) messbare
Sollkorridore für die Metriken aus `scripts/style_profile.py`. Schema pro Profil:
`{"<metric>": {"min": x}}`, `{"max": x}` oder beides; Grenzen sind inklusiv. Die Werte sind
konservativ aus den kalibrierten Schwellen in `scripts/rhythm_lint.py` und
`scripts/register_lint.py` abgeleitet: Unbelegte Korridore fehlen bewusst.
`style_profile.py --target <profil>` ergänzt den Report um einen `delta`-Block
(`value`, `range`, `in_range` je Korridor-Metrik), ohne Aggregat-Score oder Note.

## QGIR-Profilschutz

Iterative Revision darf das Profil nicht in generisches, glattes Standarddeutsch ziehen.

- Anrede bleibt stabil: du, Sie, wir, man oder neutral.
- Sprecherposition bleibt stabil: Ich-/Wir-Stimme nur nutzen, wenn sie im Input, Zielprofil oder Kontext angelegt ist.
- Fachbegriffe, Produktnamen und lokale Lieblingszeichen bleiben erhalten, wenn sie nicht selbst Artefakt sind.
- Schreibproben liefern Richtung, aber keine Pflicht zur maximalen Imitation.
- Eine einzelne Schreibprobe zeigt ein situatives Register, nicht die ganze Stimme. Fehlende Registeranteile weder verneinen noch erfinden; aus fehlender Ich-Form folgt etwa kein generelles Ich-Verbot. Mehrere Proben helfen, Konstanten und Bandbreite zu trennen.
- Formal-Modus schlägt Schreibprobe, Rhythmus und Naturalness.
- Wenn ein weiterer Pass nur Stimme verstärken würde, stoppt QGIR.
