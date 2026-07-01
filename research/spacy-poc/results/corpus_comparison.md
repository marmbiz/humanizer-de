# spaCy PoC Corpus Comparison

## Lab-Post Nominal Ratio Distribution

| Count | Min | Median | Mean | Max |
| --- | --- | --- | --- | --- |
| 21 | 1.267 | 2.130 | 2.182 | 3.109 |

## Files

| Group | File | Regex Pattern Kinds | Passive | Fragments | N/V Ratio | Lemma Hits | Regex Names | spaCy Names |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| golden | tests/corpus/case_01_input.md |  | 0 | 2 | 1.419 | 0 | 45 | 4 |
| golden | tests/corpus/case_02_input.md |  | 0 | 0 | 3.250 | 0 | 45 | 2 |
| golden | tests/corpus/case_03_input.md |  | 0 | 0 | 2.429 | 0 | 44 | 2 |
| golden | tests/corpus/case_04_input.md | colon_heading_cluster, particles_outside_locker | 3 | 1 | 1.640 | 1 | 45 | 3 |
| golden | tests/corpus/case_05_input.md |  | 0 | 0 | 1.515 | 0 | 55 | 2 |
| golden | tests/corpus/rhythm/formal_protected_de.md |  | 4 | 0 | 0.500 | 0 | 4 | 0 |
| golden | tests/corpus/rhythm/scope_skill_doc.md |  | 0 | 7 | 4.333 | 0 | 16 | 7 |
| golden | tests/corpus/rhythm/scope_user_text_de.md |  | 0 | 0 | 3.375 | 0 | 21 | 2 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-chatbots-ux-test-verlaesslichkeit.md |  | 2 | 12 | 1.267 | 1 | 103 | 24 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-fortschritt-nicht-alles-mitbekommen-muessen.md | colon_heading_cluster, particles_outside_locker | 2 | 42 | 1.693 | 9 | 293 | 76 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-geo-generative-engine-optimierung-neue-seo.md | particles_outside_locker | 11 | 80 | 2.295 | 3 | 433 | 126 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-hanzi-movie-studio-chinesisch-lernen-mit-ki.md | colon_heading_cluster | 2 | 17 | 2.456 | 1 | 140 | 48 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-humanizer-deutsch-ki-texte-erkennen-entfernen.md | abstraction_cluster, ai_marker_cluster, copula_avoidance_cluster, particles_outside_locker | 11 | 196 | 3.109 | 28 | 786 | 261 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-ki-zeigt-was-produktmanagement-bedeutet.md |  | 0 | 15 | 2.367 | 0 | 101 | 27 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-llms-als-browser.md |  | 1 | 16 | 1.767 | 1 | 123 | 25 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-taxonomie-ki-prompting.md | particles_outside_locker | 1 | 17 | 2.188 | 2 | 98 | 32 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-verbalized-sampling-mehr-vielfalt-ohne-fine-tuning.md | particles_outside_locker | 1 | 27 | 3.024 | 1 | 161 | 40 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-verstaendnis-steuern-schema-llms-txt.md | particles_outside_locker | 2 | 36 | 2.434 | 1 | 244 | 90 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-voice-ai-prototyp-gemini-live.md | colon_heading_cluster, particles_outside_locker | 6 | 88 | 2.814 | 2 | 301 | 86 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ki-woechentlicher-briefing-agent-was-der-filterbau-mich-gelehrt-hat.md | particles_outside_locker | 1 | 72 | 1.925 | 4 | 282 | 81 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/seo-content-governance-ki-suche-regulierte-branchen.md |  | 17 | 66 | 2.192 | 2 | 596 | 130 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/seo-google-ai-overviews-autoritat-vs-expertise.md | colon_heading_cluster, particles_outside_locker | 7 | 37 | 2.000 | 3 | 200 | 59 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/seo-ki-veraendert-seo-chancen-2025.md | particles_outside_locker | 9 | 78 | 2.933 | 1 | 389 | 153 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/seo-warum-google-klicks-verschwinden.md | particles_outside_locker | 1 | 32 | 2.130 | 3 | 226 | 70 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ux-ambivalente-personas-ki-simulieren.md |  | 0 | 15 | 1.560 | 0 | 103 | 25 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ux-content-testing-umsatz-kultur-hebel.md |  | 2 | 22 | 1.592 | 0 | 175 | 44 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ux-dark-pattern-ux-banken.md | particles_outside_locker | 0 | 11 | 2.019 | 1 | 75 | 14 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ux-interpretationsstabilitaet.md | colon_heading_cluster, particles_outside_locker | 9 | 34 | 2.019 | 2 | 354 | 99 |
| lab-posts | /Users/mm/Local Sites/martin-moeller/app/public/lab-posts/de/ux-schlechte-ux-it-sicherheit-inklusion.md | abstraction_cluster, particles_outside_locker | 2 | 47 | 2.047 | 12 | 256 | 80 |
