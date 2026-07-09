# Quality-Guided Iterative Revision

QGIR ist ein begrenzter Revisionsmodus fuer Faelle, in denen ein einzelner Audit-Pass echte KI-Muster findet, aber die erste Korrektur noch nicht review-ready ist.

## Qualitätsziel

- Detector-Bezug ist Kontext.
- Ziel ist ein Text, der fuer Menschen klar, proportional geaendert und belegtreu wirkt.
- Volltext-Rewrite ist nur dann sinnvoll, wenn der Nutzer ihn ausdruecklich will.
- Beispiele, Quellen, Ich-Erfahrung oder Produktdetails muessen aus Input oder Kontext kommen.
- Register bleibt am Zielprofil orientiert statt auf glattes Standarddeutsch normalisiert zu werden.

## Loop

1. Diagnose: hoechstens die wichtigsten HIGH/MEDIUM-Cluster waehlen.
2. Lokale Revision: nur betroffene Passagen aendern.
3. Gates: Claim-Delta, Registerprofil, Naturalness und Rhythmus pruefen.
4. Edit-Budget: Anteil substanziell geaenderter Saetze pruefen.
5. Stoppen: wenn Restbefunde niedrig sind oder ein weiterer Pass Drift riskieren wuerde.

Fuer Claim-Delta reicht der direkte Vorpass-Diff nicht aus. Vor Pass 1 ein Original-Ledger mit
`scripts/evidence_lint.py --write-ledger` schreiben und nach jedem QGIR-Pass zusaetzlich mit
`--ledger` gegen dieses Original-Ledger pruefen; so faellt auch schrittweiser Ankerverlust auf.

## Harte Grenzen

| Grenze | Regel |
|---|---|
| Passzahl | 2 normal, 3 nur bei dokumentiertem schweren Restcluster |
| Edit-Budget | Warnen ab ca. 25-35 Prozent substanziell geaenderter, entfernter oder hinzugefuegter Saetze |
| Claim-Delta | Null Toleranz fuer neue ungestuetzte Faktenanker |
| Register-Drift | Null Toleranz fuer Anrede-, Modus- oder Profilbruch |
| Naturalness | Ziel ist review-ready, nicht maximal menschlich klingend |
| Detector-Metrik | Nicht allein Akzeptanzkriterium |

## Moduswahl

| Situation | Modus |
|---|---|
| Text ist sauber oder hat nur Einzelsignale | Audit-only |
| Klare Cluster, aber geringe Drift-Gefahr | Minimal revise |
| Erste Revision laesst noch echte HIGH/MEDIUM-Cluster stehen | QGIR |
| Quelle, Recht, Technik oder Formalregister wuerde durch weitere Revision leiden | Stop |

## Stop-Regeln

Stoppe sofort, wenn eine der folgenden Bedingungen eintritt:

- Ein Faktenanker fehlt, entsteht neu oder wird staerker bewertet.
- Anrede, Distanz, Fachterminologie oder Autorenprofil kippt.
- Die Revision muss Volltext ausgeben, um weiterzukommen.
- Der naechste Eingriff wuerde nur noch Score, Glattheit oder Detektorwirkung ohne Qualitaetsgewinn verbessern.
- Uebriges Holpern ist akzeptable Textur des Registers.

## Erfolgskriterium

Ein QGIR-Ergebnis ist gut, wenn ein kritischer menschlicher Leser es als klarer, belegtreu, registerpassend und proportional geaendert beurteilen wuerde.
