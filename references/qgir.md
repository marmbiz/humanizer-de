# Quality-Guided Iterative Revision

QGIR ist ein begrenzter Revisionsmodus für Fälle, in denen ein einzelner Audit-Pass echte KI-Muster findet, aber die erste Korrektur noch nicht review-ready ist.

## Qualitätsziel

- Detector-Bezug ist Kontext.
- Ziel ist ein Text, der für Menschen klar, proportional geändert und belegtreu wirkt.
- Volltext-Rewrite ist nur dann sinnvoll, wenn der Nutzer ihn ausdrücklich will.
- Beispiele, Quellen, Ich-Erfahrung oder Produktdetails müssen aus Input oder Kontext kommen.
- Register bleibt am Zielprofil orientiert statt auf glattes Standarddeutsch normalisiert zu werden.

## Loop

1. Diagnose: höchstens die wichtigsten HIGH/MEDIUM-Cluster wählen.
2. Lokale Revision: nur betroffene Passagen ändern.
3. Gates: Claim-Delta, Registerprofil, Naturalness und Rhythmus prüfen.
4. Edit-Budget: Anteil substanziell geänderter Sätze prüfen.
5. Stoppen: wenn Restbefunde niedrig sind oder ein weiterer Pass Drift riskieren würde.

Für Claim-Delta reicht der direkte Vorpass-Diff nicht aus. Vor Pass 1 ein Original-Ledger mit
`scripts/evidence_lint.py --write-ledger` schreiben und nach jedem QGIR-Pass zusätzlich mit
`--ledger` gegen dieses Original-Ledger prüfen; so fällt auch schrittweiser Ankerverlust auf.

## Harte Grenzen

| Grenze | Regel |
|---|---|
| Passzahl | 2 normal, 3 nur bei dokumentiertem schweren Restcluster |
| Edit-Budget | Warnen ab ca. 25-35 Prozent substanziell geänderter, entfernter oder hinzugefügter Sätze |
| Claim-Delta | Null Toleranz für neue ungestützte Faktenanker |
| Register-Drift | Null Toleranz für Anrede-, Modus- oder Profilbruch |
| Naturalness | Ziel ist review-ready, nicht maximal menschlich klingend |
| Detector-Metrik | Nicht allein Akzeptanzkriterium |

## Moduswahl

| Situation | Modus |
|---|---|
| Kein bearbeitungswürdiger Cluster oder nur Einzelsignale | Audit-only |
| Klare Cluster, aber geringe Drift-Gefahr | Minimal revise |
| Erste Revision lässt noch echte HIGH/MEDIUM-Cluster stehen | QGIR |
| Quelle, Recht, Technik, Formalregister oder Zielprofil würde durch weitere Revision leiden | Stop |

## Stop-Regeln

Stoppe sofort, wenn eine der folgenden Bedingungen eintritt:

- Ein Faktenanker fehlt, entsteht neu oder wird stärker bewertet.
- Anrede, Distanz, Fachterminologie oder Autorenprofil kippt.
- Die Revision muss Volltext ausgeben, um weiterzukommen.
- Der nächste Eingriff würde nur noch Score, Glattheit oder Detektorwirkung ohne Qualitätsgewinn verbessern.
- Übriges Holpern ist akzeptable Textur des Registers.

## Erfolgskriterium

Ein QGIR-Ergebnis ist gut, wenn ein kritischer menschlicher Leser es als klarer, belegtreu, registerpassend und proportional geändert beurteilen würde.
