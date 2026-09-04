# Benutzung im Detail

Die Grundprompts stehen in der [README](../README.md#benutzung). Hier stehen der Zusatz für Werbetexte und weitere Vorher-/Nachher-Beispiele. Die lokalen Prüfskripte, der Zwei-Aufruf-Runner und das Stilprofil sind in [pruefskripte.md](pruefskripte.md) beschrieben.

## Werbetexte: mehr Eingriff auf Wunsch

Seit 5.17.0 erkennt der Skill Werbeschablonen-Figuren deterministisch: Sozialbeweis,
Standard-Werbesektionen und gestapelte Handlungsaufforderungen. Der Preflight gewichtet
solche Befunde. Am Prüfstein-Werbetext mit sieben eingebauten Schablonen entfernt der
aktuelle Stand ohne jeden Zusatz sechs von sieben, während die Fakten erhalten bleiben.

Der Detektor erkennt allerdings Formulierungen, keine Bauformen. Bei Werbetexten mit
unbekannten Schablonen, etwa frisch erzeugter KI-Werbung, feuert er deshalb oft nicht. Dann
hält sich der Skill weiter zurück, weil Werbesprache werben darf und seine Schutzregeln den
bewusst gesetzten Dreiklang nicht von der austauschbaren Schablone unterscheiden können.
Für genau diese Fälle lässt sich der folgende Absatz an die Anweisung hängen:

```text
Für persuasive Abschnitte gilt: Branchenüblichkeit und Label-Konvention schützen
Werbefloskeln nicht. Trenne bei jeder Werbefigur den prüfbaren Kern von der
Schablone. Prüfbar sind Zahlen, benannte Systeme und Schnittstellen, Normen,
Verfahren, Abläufe, Angebotsbedingungen und konkret bezeichnete Produktfunktionen
— sie bleiben erhalten, notfalls umformuliert. Wertadjektive wie schnell, einfach
oder sicher sind ohne benannte Funktion, Norm oder Messgröße kein prüfbarer Kern.
Die Schablone darum herum entfernst du, wenn ihre Struktur sich auf beliebige
andere Produkte übertragen ließe. Eine mehrgliedrige Figur bleibt jedoch stehen,
sobald eines ihrer Glieder eine Aussage macht, die nachprüfbar falsch sein könnte.
```

Gemessen wurde dieser Zusatz vor Einführung des Detektors. Damals verschwand vom Prüfstein
ohne ihn eine von sieben Schablonen, mit ihm im Schnitt fünfeinhalb. In der menschlichen
Gegenprobe blieben alle acht Substanzanker unberührt. Der Preis ist eine höhere
Eingriffstiefe von rund zwanzig statt rund neun Prozent. Wer viel ändert, ändert manchmal
zu viel. Lies das Ergebnis darum gegen.

## Weitere Beispiele

## Redaktioneller Kommentar

**Vorher:** „Es ist wichtig zu bemerken, dass die Bevölkerung zwischen 1950 und 2000 um 40 Prozent gewachsen ist. Darüber hinaus ist die Stadtfläche um 60 Prozent erweitert worden.“

**Nachher:** „Die Bevölkerung wuchs zwischen 1950 und 2000 um 40 Prozent. Die Stadtfläche wurde um 60 Prozent erweitert.“

## Maschinelle Konjunktionen

**Vorher:** „Das Unternehmen wurde 1980 gegründet. Darüber hinaus beschäftigt es heute 200 Mitarbeiter. Ferner ist es in 8 Ländern tätig. Außerdem hat es einen Umsatz von 50 Millionen Euro.“

**Nachher:** „Das Unternehmen wurde 1980 gegründet. Es beschäftigt heute 200 Mitarbeiter in 8 Ländern und hat einen Umsatz von 50 Millionen Euro.“

## Kollaborative Kommunikation

**Vorher:** „Wie Sie sehen können, war die Produktivität beeindruckend. Der Umsatz verdreifachte sich. Lassen Sie mich wissen, wenn Sie weitere Informationen benötigen!“

**Nachher:** „Die Produktivität fiel positiv auf. Der Umsatz verdreifachte sich.“
