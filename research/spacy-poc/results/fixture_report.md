# spaCy PoC Fixture Report

| Messung | Precision | Recall | F1 | Success |
| --- | --- | --- | --- | --- |
| Passiv + subjektlose Fragmente | 0.952 | 1.000 | 0.976 | no |
| Nomen-Verb-Verhältnis | 1.000 | 1.000 | 1.000 | yes |
| Lemma-Floskeln | 0.917 | 0.786 | 0.846 | no |
| NER-Anker Drift (Regex baseline) | 0.733 | 1.000 | 0.846 | baseline |
| NER-Anker Drift (spaCy names) | 0.818 | 0.818 | 0.818 | no |

## Pattern 39 Cases

| ID | Expected | Actual | Passive | Fragment | Protected |
| --- | --- | --- | --- | --- | --- |
| p39_pos_01 | yes | yes | yes | no | no |
| p39_pos_02 | yes | yes | yes | no | no |
| p39_pos_03 | yes | yes | yes | no | no |
| p39_pos_04 | yes | yes | yes | no | no |
| p39_pos_05 | yes | yes | yes | no | no |
| p39_pos_06 | yes | yes | yes | no | no |
| p39_pos_07 | yes | yes | yes | no | no |
| p39_pos_08 | yes | yes | yes | no | no |
| p39_pos_09 | yes | yes | yes | no | no |
| p39_pos_10 | yes | yes | yes | no | no |
| p39_pos_11 | yes | yes | no | yes | no |
| p39_pos_12 | yes | yes | no | yes | no |
| p39_pos_13 | yes | yes | no | yes | no |
| p39_pos_14 | yes | yes | no | yes | no |
| p39_pos_15 | yes | yes | no | yes | no |
| p39_pos_16 | yes | yes | yes | yes | no |
| p39_pos_17 | yes | yes | no | yes | no |
| p39_pos_18 | yes | yes | no | yes | no |
| p39_pos_19 | yes | yes | no | yes | no |
| p39_pos_20 | yes | yes | no | yes | no |
| p39_neg_01 | no | no | no | no | yes |
| p39_neg_02 | no | no | no | no | yes |
| p39_neg_03 | no | no | no | no | yes |
| p39_neg_04 | no | no | no | no | yes |
| p39_neg_05 | no | yes | no | yes | yes |
| p39_neg_06 | no | no | no | no | yes |
| p39_neg_07 | no | no | no | no | yes |
| p39_neg_08 | no | no | no | no | yes |
| p39_neg_09 | no | no | no | no | yes |
| p39_neg_10 | no | no | no | no | yes |
| p39_neg_11 | no | no | no | no | yes |
| p39_neg_12 | no | no | no | no | yes |
| p39_neg_13 | no | no | no | no | yes |
| p39_neg_14 | no | no | no | no | yes |
| p39_neg_15 | no | no | no | no | yes |
| p39_neg_16 | no | no | no | no | yes |
| p39_neg_17 | no | no | no | no | yes |
| p39_neg_18 | no | no | no | no | yes |
| p39_neg_19 | no | no | no | no | yes |
| p39_neg_20 | no | no | no | no | yes |

## Nominal Style Cases

| ID | Label | Predicted Nominal | Nouns | Verbs | Ratio |
| --- | --- | --- | --- | --- | --- |
| nom_01 | nominal | yes | 5 | 1 | 5.000 |
| nom_02 | nominal | yes | 5 | 1 | 5.000 |
| nom_03 | nominal | yes | 5 | 1 | 5.000 |
| nom_04 | nominal | yes | 4 | 1 | 4.000 |
| nom_05 | nominal | yes | 5 | 1 | 5.000 |
| nom_06 | nominal | yes | 5 | 1 | 5.000 |
| nom_07 | nominal | yes | 5 | 1 | 5.000 |
| nom_08 | nominal | yes | 5 | 1 | 5.000 |
| nom_09 | nominal | yes | 5 | 1 | 5.000 |
| nom_10 | nominal | yes | 5 | 1 | 5.000 |
| verb_01 | verb | no | 4 | 3 | 1.333 |
| verb_02 | verb | no | 4 | 4 | 1.000 |
| verb_03 | verb | no | 4 | 4 | 1.000 |
| verb_04 | verb | no | 4 | 3 | 1.333 |
| verb_05 | verb | no | 4 | 3 | 1.333 |
| verb_06 | verb | no | 4 | 2 | 2.000 |
| verb_07 | verb | no | 3 | 3 | 1.000 |
| verb_08 | verb | no | 3 | 3 | 1.000 |
| verb_09 | verb | no | 4 | 3 | 1.333 |
| verb_10 | verb | no | 4 | 3 | 1.333 |

## Lemma Phrase Cases

| ID | OK | Expected | Actual |
| --- | --- | --- | --- |
| lemma_01 | yes | ai_marker:beleuchten | ai_marker:beleuchten:beleuchtet |
| lemma_02 | yes | ai_marker:beleuchten | ai_marker:beleuchten:beleuchtete |
| lemma_03 | yes | ai_marker:unterstreichen | ai_marker:unterstreichen:unterstreichen |
| lemma_04 | no | ai_marker:unterstreichen |  |
| lemma_05 | yes | ai_marker:maßgeblich | ai_marker:maßgeblich:maßgebliche |
| lemma_06 | yes | ai_marker:maßgeschneidert, abstractum:lösungen | ai_marker:maßgeschneidert:Maßgeschneiderte, abstractum:lösungen:Lösungen |
| lemma_07 | yes | ai_marker:digitale landschaft | ai_marker:digitale landschaft:digitale Landschaft |
| lemma_08 | yes | ai_marker:zusammenspiel | ai_marker:zusammenspiel:Zusammenspiel |
| lemma_09 | yes | copula_avoidance:fungiert als | copula_avoidance:fungiert als:fungiert als |
| lemma_10 | yes | copula_avoidance:dient als | copula_avoidance:dient als:diente als |
| lemma_11 | yes | abstractum:lösungen, copula_avoidance:stellt dar | abstractum:lösungen:Lösung, copula_avoidance:stellt dar:stellt einen Fortschritt dar |
| lemma_12 | yes | abstractum:lösungen, copula_avoidance:stellt dar | abstractum:lösungen:Lösung, copula_avoidance:stellt dar:stellte einen Fortschritt dar |
| lemma_13 | yes | copula_avoidance:verfügt über | copula_avoidance:verfügt über:verfügt über |
| lemma_14 | no | abstractum:prozesse, copula_avoidance:zeichnet sich | copula_avoidance:zeichnet sich:zeichnet sich |
| lemma_15 | yes | copula_avoidance:erweist sich als | copula_avoidance:erweist sich als:erweist sich als |
| lemma_16 | no | copula_avoidance:repräsentiert | abstractum:maßnahmen:Maßnahme, copula_avoidance:repräsentiert:repräsentiert |
| lemma_17 | no | abstractum:maßnahmen, abstractum:aspekte, abstractum:faktoren | abstractum:maßnahmen:Maßnahmen |
| lemma_18 | no | abstractum:herausforderungen, abstractum:prozesse |  |
| lemma_19 | yes | particle:ja | particle:ja:ja |
| lemma_20 | yes | particle:mal | particle:mal:mal |
| lemma_21 | yes | particle:schon | particle:schon:schon |
| lemma_22 | yes |  |  |
| lemma_23 | yes |  |  |
| lemma_24 | yes |  |  |
| lemma_25 | yes |  |  |
| lemma_26 | no |  | ai_marker:nahtlos:nahtlos |

## NER Entity Cases

| ID | Expected | Regex | spaCy |
| --- | --- | --- | --- |
| ner_ent_01 | David Goggins | David Goggins, Ausdauer | David Goggins |
| ner_ent_02 | Elon Musk, Berlin, Tesla | Berlin, Elon Musk, Tesla | Berlin, Elon Musk, Tesla |
| ner_ent_03 | Dalai Lama | Dalai Lama, Mitgefühl |  |
| ner_ent_04 | Angela Merkel, Olaf Scholz, Berlin | Angela Merkel, Olaf Scholz, Berlin | Angela Merkel, Olaf Scholz, Berlin |
| ner_ent_05 | Martin Möller, OpenAI | Martin Möller, OpenAI | Martin Möller, OpenAI |
| ner_ent_06 | AOK, Techniker Krankenkasse | AOK, Chatbots, Techniker Krankenkasse | AOK |
| ner_ent_07 | Google AI Overviews, SEO | Google AI Overviews, SEO | Google AI Overviews, SEO |
| ner_ent_08 | OpenAI, Berlin | Berlin, OpenAI, Der Bericht | Berlin, OpenAI |

## NER Drift Cases

| ID | Expected | Regex | spaCy |
| --- | --- | --- | --- |
| ner_drift_01 | removed_proper_name, added_proper_name | added_proper_name, removed_proper_name | added_proper_name, removed_proper_name |
| ner_drift_02 | removed_number, added_number | added_number, removed_number | added_number, removed_number |
| ner_drift_03 | removed_proper_name, added_proper_name | added_proper_name, removed_proper_name | removed_proper_name |
| ner_drift_04 | removed_quote, added_quote | added_quote, removed_quote | added_quote, removed_quote |
| ner_drift_05 | removed_paragraph, added_paragraph | added_number, added_paragraph, removed_number, removed_paragraph | added_number, added_paragraph, removed_number, removed_paragraph |
| ner_drift_06 |  |  |  |
| ner_drift_07 |  | removed_proper_name |  |
| ner_drift_08 | removed_proper_name | added_proper_name, removed_proper_name |  |
