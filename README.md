<div align="center">

<picture>
  <source type="image/webp" srcset="assets/humanizer-de-hero.webp">
  <img src="assets/humanizer-de-hero.png" alt="humanizer-de – German AI text humanizer und evidenzbewusster deutscher Stil-Editor. Less machine. More voice." width="100%">
</picture>

[![Version](https://img.shields.io/github/v/tag/marmbiz/humanizer-de?label=Version&color=c4501f)](https://github.com/marmbiz/humanizer-de/tags)
[![Tests](https://github.com/marmbiz/humanizer-de/actions/workflows/tests.yml/badge.svg)](https://github.com/marmbiz/humanizer-de/actions/workflows/tests.yml)
[![Lizenz](https://img.shields.io/badge/Lizenz-MIT_%2B_CC_BY--SA_4.0-1f6feb)](NOTICE)
[![Muster](https://img.shields.io/badge/Muster-72_in_10_Kategorien-2da44e)](#72-muster-in-10-kategorien)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-d97757)](#installation)
[![Codex](https://img.shields.io/badge/Codex-Supported-10a37f)](#installation)
[![GitHub Stars](https://img.shields.io/github/stars/marmbiz/humanizer-de?label=Stars&color=e3b341)](https://github.com/marmbiz/humanizer-de/stargazers)

**[Was ist das?](#was-ist-das)** · **[Installation](#installation)** · **[Benutzung](#benutzung)** · **[Beispiele](#beispiele)** · **[Messen & Audit](#messen-und-audit)** · **[Fakten & Grenzen](#fakten-grenzen-und-datenschutz)** · **[Wie es arbeitet](#wie-der-skill-arbeitet)** · **[Optionale Werkzeuge](#optionale-werkzeuge)** · **[72 Muster](#72-muster-in-10-kategorien)** · **[Für AI-Assistenten](#für-ai-assistenten)** · **[Entwicklung](#entwicklung-und-verifikation)** · **[Was ist neu?](#was-ist-neu)**

<sub>German AI Text Humanizer · Claude Humanizer Deutsch · KI-Texte humanisieren Deutsch · Supports Claude Code and Codex · Von [Martin Moeller](https://martin-moeller.biz) · basiert auf den Wikipedia-Leitlinien [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) (de) und [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (en) · hervorgegangen aus dem [Humanizer](https://github.com/blader/humanizer) von [blader](https://github.com/blader)</sub>

<sub>Guide (DE): [KI-Texte auf Deutsch natürlicher und glaubwürdiger schreiben](https://martin-moeller.biz/lab/ki/humanizer-deutsch-ki-texte-erkennen-entfernen) · Guide (EN): [Claude Humanizer Skill: Make German AI Text Sound Human](https://martin-moeller.biz/en/lab/ai/claude-humanizer-skill-german) · Hintergrund (DE): [Der KI-Text-Eisberg](https://martin-moeller.biz/lab/ki-text-eisberg)</sub>

</div>

---

<a id="warum-nutzen"></a>

## Was ist das?

Humanizer (Deutsch) macht aus glatten KI-Entwürfen bessere deutsche Texte: natürlicher, belegbewusster
und näher an deiner Stimme. Zahlen, Namen, Daten, URLs, Zitate und Quellenanker gleicht der Skill
konservativ ab; semantische Beziehungen und sachliche Richtigkeit brauchen eine fachliche Endabnahme.
Ergibt die vollständige Prüfung keinen bearbeitungswürdigen Befund, lässt der Skill den Text in Ruhe.

| Vorher | Nachher |
|---|---|
| „Darüber hinaus ist es von entscheidender Bedeutung, innovative Lösungen nahtlos zu implementieren.“ | „Neue Lösungen müssen sich sauber einführen lassen.“ |

<img src="assets/beispiel-durchlauf.svg" alt="Beispiel-Durchlauf im Terminal: Der Skill findet vier Muster im Beispielsatz und liefert „Neue Lösungen müssen sich sauber einführen lassen.“ als Ergebnis." width="100%">

<details>
<summary><strong>Textfassung des Durchlaufs</strong></summary>

> **Less machine. More voice.**
> Ich prüfe Rhythmus, Belege und Stimme...

**Modus:** Sachlich (angenommen — ein Satz ohne Kontext). Sammelcheck: `insufficient_text`, daher reines Urteil.

**Gefundene Muster:**

- „Darüber hinaus“ — mechanischer Konnektor ohne inhaltliche Anknüpfung
- „ist es von entscheidender Bedeutung“ — Wichtigkeits-Floskel (Muster 3), sagt nichts, was das Verb nicht könnte
- „innovative Lösungen“ — KI-Marker-Vokabular plus Abstraktum ohne Gegenstand (Muster 64/58)
- „nahtlos … implementieren“ — Marker-Vokabel plus Anglizismus-Verb, wo „einführen“ reicht

**Geänderte Stellen:**

| Vorher | Nachher |
|---|---|
| Darüber hinaus ist es von entscheidender Bedeutung, innovative Lösungen nahtlos zu implementieren. | Neue Lösungen müssen sich sauber einführen lassen. |

Der Satz trägt keine prüfbare Substanz — er behauptet Wichtigkeit, nennt aber weder Lösung noch System. Deshalb bleibt die Neufassung bewusst schlicht. Mit Kontext (welche Lösung, wo eingeführt?) wird daraus ein konkreter Satz.

**Belege:** Keine unbelegten Quellen.

**Kurzaudit:** Keine verbliebenen Tells. Restrisiko: „neue Lösungen“ bleibt abstrakt, weil der Input keinen Gegenstand liefert.

</details>

Du brauchst dafür zunächst weder Python noch Zusatzsoftware. Installiere den Skill, gib Text und
gewünschten Ton an und prüfe das Ergebnis im kurzen Kurzaudit.

### Woran der Skill sich messen lässt

Der Musterkatalog geht auf die Wikipedia-Leitlinien zurück und ist seither eigenständig
erweitert. Was darauf aufsetzt, ist eigene Arbeit: Die Schwellen der deterministischen
Prüfungen sind gegen eine Fehlalarm-Baseline aus verifizierten Menschentexten geeicht, und
neue Muster kommen nur über das [Marker-Aufnahmeprotokoll](docs/marker-aufnahmeprotokoll.md)
hinein – mit Positiv-, Negativ- und Grenzfixtures und einer dokumentierten
Fehlalarm-Erwartung. Scheitert ein Kandidat daran, wird er nicht aufgenommen. In 5.10.0 ist das
einem Lint-Marker so ergangen.

Das Sprachmodell schreibt. Darüber liegt der Skill als Prüf- und Evidence-Rahmen. Ein eigenes
fine-getuntes Humanizer-Modell ist nicht geplant, weil dafür bislang kein gemessener Zusatznutzen
den Daten-, Betriebs- und Pflegeaufwand rechtfertigt. Auch ein anderer Writer bliebe an denselben
Prüfrahmen gebunden.

---

## Installation

### Codex – empfohlen

Im Terminal:

```bash
codex plugin marketplace add marmbiz/humanizer-de
```

Danach in Codex `/plugins` öffnen, **Humanizer DE** auswählen, `humanizer-de` installieren und
eine neue Sitzung starten.

### Claude Code – empfohlen

In einer laufenden Claude-Code-Sitzung:

```bash
/plugin marketplace add marmbiz/humanizer-de
/plugin install humanizer-de@humanizer-de
/reload-plugins
```

Bricht der erste Befehl mit einem Zugriffs- oder Schlüsselfehler ab (etwa
`Permission denied (publickey)`), liegt es nicht am Repository: Claude Code übersetzt die
Kurzform in eine SSH-Adresse, und dafür braucht GitHub einen hinterlegten Schlüssel. Ohne
Schlüssel funktioniert die vollständige HTTPS-Adresse:

```bash
/plugin marketplace add https://github.com/marmbiz/humanizer-de.git
```

### Claude im Browser (claude.ai)

Ohne Terminal geht es über die Weboberfläche. Unter **Einstellungen → Capabilities** muss
„Code execution and file creation“ eingeschaltet sein, sonst erscheint der Skills-Bereich
nicht. Danach unter **Customize → Skills → Add → Upload a skill** das Paket
[`humanizer-de.zip`](https://github.com/marmbiz/humanizer-de/releases/latest/download/humanizer-de.zip)
vom neuesten Release hochladen. Was im Archiv steckt und wie sich seine Prüfsumme nachrechnen
lässt: [docs/installation.md](docs/installation.md#claude-im-browser-claudeai).

**Nicht installiert werden:** Python, Click, spaCy, das deutsche spaCy-Modell, Hunspell,
LanguageTool oder Java. Solche Pakete dürfen nur nach ausdrücklicher Zustimmung separat
installiert werden.

### Funktioniert es?

In der neuen beziehungsweise neu geladenen Sitzung eingeben:

```text
Humanisiere diesen Text im Modus Sachlich:
In der heutigen dynamischen Landschaft ist es entscheidend, innovative Lösungen nahtlos zu implementieren.
```

Die Antwort sollte mit „Less machine. More voice.“ beginnen, den Modus nennen und nur die
auffälligen Stellen bearbeiten. Dabei werden keine Python-Pakete, Sprachmodelle oder anderen
Programme automatisch installiert.

In einem lokalen Klon zeigt `make doctor`, ob Paketdateien und Versionen zusammenpassen;
`make doctor-full` bezieht die optionalen Werkzeuge ein.

Manuelle Installation, Cursor, Updates, Ausprobieren ohne Installation und die Regeln für
KI-Assistenten, die den Skill installieren sollen: [docs/installation.md](docs/installation.md).

---

## Benutzung

<a id="tipps-zur-nutzung"></a>

### Mit natürlicher Sprache

```
Humanisiere diesen Text für mich
```

oder

```
Entferne KI-Muster aus diesem Absatz.
```

### Mit Stimmkalibrierung

```
Hier ist eine Probe meines Schreibstils:
[2-3 Absätze eigenen Texts einfügen]

Jetzt humanisiere diesen Text:
[KI-Text einfügen]
```

Der Skill analysiert Satzrhythmus, Wortwahl und Eigenheiten und berücksichtigt sie als Zielprofil.

### Spezifische Muster adressieren

```
Humanisiere diesen Text. Entferne nur sprachliche Muster, nicht die Formatierung.
```

### Was du zurückbekommst

Der Humanizer zeigt nicht nur den überarbeiteten Text. Ein kurzer Audit nennt den gewählten Modus,
die wichtigsten gefundenen Muster und verbleibende Risiken. Ist der Text bereits sauber, folgt
statt einer unnötigen Umschreibung ein Null-Edit-Befund.

### Bessere Ergebnisse mit drei Angaben

- Zielgruppe
- Kontext, etwa Website, E-Mail, Blog oder Fachtext
- gewünschter Ton: locker, sachlich oder formal

Arbeite in höchstens zwei gezielten Runden. Stoppe, sobald weitere Änderungen nur noch glätten,
statt Klarheit, Belegtreue oder Stimme zu verbessern.

Werbetexte dürfen werben, deshalb hält sich der Skill dort zurück. Wer mehr Eingriff will,
hängt einen gemessenen Zusatz an die Anweisung:
[docs/benutzung.md](docs/benutzung.md#werbetexte-mehr-eingriff-auf-wunsch). Die lokalen
Prüfskripte, der Zwei-Aufruf-Runner und das persönliche Stilprofil stehen in
[docs/pruefskripte.md](docs/pruefskripte.md).

---

## Beispiele

### Werbesprache

**Vorher:**

> Die atemberaubende Stadt mit ihrem reichen kulturellen Erbe zieht Besucher aus aller Welt an.
> Die spektakulären Denkmäler sind ein Beweis für die künstlerische Brillanz vergangener Generationen.

**Nachher:**

> Die Stadt zieht Besucher aus aller Welt an. Ihre Denkmäler zeigen die Handwerkskunst vergangener Generationen.

Drei weitere Vorher-/Nachher-Beispiele: [docs/benutzung.md](docs/benutzung.md#weitere-beispiele).

---

<a id="messen-und-audit"></a>

## Messen & Audit

Am Anfang jedes Durchgangs steht eine Messung. Im Agenten übernimmt der Skill sie selbst. Als
Kommandozeilen-Werkzeug genügt dafür Python 3 ohne Zusatzpakete:

```bash
python3 scripts/humanizer_audit.py --file entwurf.md --mode sachlich --format md
```

Gemeldet werden Preflight-Risiko, Rhythmusdaten, eine Stilkarte sowie Befunde mit Muster-Nummer
und Severity. Das Preflight-Risiko (`low`, `medium`, `high`, `insufficient_text`) beschreibt, ob
der Text messbar zu gleichförmig wirkt: sehr ähnliche Satzlängen, wiederholte Satzanfänge, viele
mechanische Übergänge. Es ist eine Qualitätsheuristik, keine Aussage zur Autorenschaft. Ein `low`
bedeutet nur „kein geeichtes Signal“, nicht „sauber“: In Registern wie Werbung, Social Media oder
Essayistik kann dahinter eine Erkennungslücke stecken.

Bei hohem Risiko empfiehlt der Skill nach der Überarbeitung einen kontrollierten Nachkamm, das
**Combing-Gate**: höchstens zwei gezielte Rhythmusänderungen, ohne neue Fakten oder Füllwörter.
Der Report sagt dabei ausdrücklich, dass Textqualität und Lesbarkeit durch solchen Feinschliff auch
schlechter werden können. Auch das Combing-Gate ist kein Detektor-Bypass.

Beispielausgabe, JSON-Spans, Stilkarte, Zwei-Aufruf-Runner, Exit-Codes und die Einbindung in eigene
Pipelines: [docs/pruefskripte.md](docs/pruefskripte.md).

---

<a id="wann-hilfreich--und-wann-nicht"></a>
<a id="datenschutz--sicherheit"></a>

## Fakten, Grenzen und Datenschutz

Der Humanizer gleicht erkennbare Zahlen, Namen, Daten, URLs, Zitate, Quellenanker und einfache
Richtungsmarker konservativ ab. Seine Leitplanken verbieten erfundene Erfahrung und ungestützte
Gewissheit; die deterministischen Prüfungen erzwingen das nicht semantisch vollständig. Ergibt die
Prüfung keinen bearbeitungswürdigen Befund oder nur bekannte Fehlalarme, greift der Skill nicht weiter ein.

**Stark ist der Skill**, wenn KI-Entwürfe zu glatt oder generisch klingen, Fachbegriffe und Belege
erhalten bleiben müssen oder ein Text sachlich, aber nicht maschinell wirken soll. **Zurückhaltung
ist nötig** bei literarischen Texten, stark etablierter Autorenstimme und Fachkonventionen, die
absichtlich wiederholen, nominal formulieren oder passiv schreiben.

Dafür gibt es einen messbaren Grund. Die Fehlalarm-Baseline hinter den Schwellen umfasst 20
verifizierte Menschentexte aus drei Genres der Web-Prosa: Blog (8), Marketing (6) und Sachtext (6).
Urteile, Bescheide, technische Dokumentation, Leichte Sprache und Literatur sind darin nicht
vertreten. Außerhalb dieser Genres sind Befunde entsprechend vorsichtiger zu lesen.

**Rote Linien:**

- Kein Detektor-Bypass und keine Garantie für Herkunfts-Scores.
- Keine fingierte Autorenschaft, Erfahrung, Quelle oder Zahl.
- Messwerte beschreiben Textmerkmale, nie den tatsächlichen Autor.
- Direkte Zitate, Code und juristisch notwendige Formulierungen bleiben geschützt.

| Nutzung | Verlässt der Text den Rechner? |
|---|---|
| Nur die lokalen Prüfskripte | Nein – sie laufen lokal und offline |
| Skill in Claude Code oder Codex | Der Text geht an das jeweilige Modell; es gelten dessen Datenschutzregeln und der eigene Vertrag |

Lokale Dateien werden nur geschrieben, wenn du eine Dateiänderung ausdrücklich verlangst oder
selbst speicherst. Das optionale Stilprofil unter `.humanizer/profile.json` speichert Regeln,
niemals Textauszüge.

---

<a id="philosophie"></a>

## Wie der Skill arbeitet

Drei Schichten teilen sich die Arbeit:

- **Heuristik** findet harte, sichtbare Muster wie Unicode-Artefakte, Marker-Cluster oder mechanische Titel.
- **Messung** prüft Rhythmus, Register und geschützte Faktenanker.
- **Urteil** bleibt beim großen Modell: Nur Claude oder Codex kann im Kontext entscheiden, ob eine Stelle wirklich schlechter Text ist.

```mermaid
flowchart TD
    T([Eingabetext]) --> M["Messen – Pass 0<br/>Rhythmus, Register, Preflight"]
    M --> Z{"Redigieren oder<br/>nur Befunde?"}
    Z -- "nur Befunde" --> AU["Audit-Zweig<br/>alle 72 Muster prüfen"]
    AU --> B([Befundliste, Text bleibt unberührt])
    Z -- redigieren --> C{"Echte Muster-Cluster?"}
    C -- nein --> N["Null-Edit: Text bleibt stehen<br/>unbelegte Quellen trotzdem markieren"]
    N --> O
    C -- ja --> E["Fakten sichern – Pass 1<br/>Zahlen, Namen, Quellen, Zitate"]
    E --> R["Redigieren – Pass 2–4<br/>Lexik, Struktur, Rhythmus"]
    R --> A["Selbst-Audit – Pass 5<br/>Qualität und Stimme"]
    A --> G{"Claim-/Ankerprüfung grün?"}
    G -- nein --> R
    G -- ja --> O([Überarbeiteter Text + Kurzaudit])
```

Die Leitidee ist proportional: so viel wie nötig, so wenig wie möglich. Regeln messen, aber richten
nicht. Konkrete Fakten schlagen stilistische Glätte, und vorhandene Fachsprache schlägt ein
vermeintlich „menschlicheres“ Schauspiel. Das Projekt stützt damit belegbare EEAT-nahe Mechaniken,
behauptet aber weder Expertise noch Autorenschaft.

## Optionale Werkzeuge

Du musst nichts davon vorsorglich installieren. Starte mit dem Basis-Skill und ergänze ein Werkzeug
erst bei einem konkreten Problem. Die Werkzeuge aktivieren konkrete Prüfpfade; ein allgemeiner
Qualitätsgewinn ist dafür nicht gemessen.

| Setup | Ermöglicht |
|---|---|
| Nur der Skill | Ausprobieren, kurze Texte und normales Redigieren |
| Skill + Python | Lokale, reproduzierbare Prüfskripte für Dateien und erkennbare Faktenanker |
| zusätzlich spaCy | Genauere Satzanalyse und dokumentierte Fehlalarm-Filter |
| zusätzlich Hunspell | Vergleich neuer unbekannter Wörter bei Datei-Rewrites |
| zusätzlich LanguageTool | Zusätzliches Korrektorat von Grammatik und Zeichensetzung |

Den lokalen Status prüft ein textfreier Doctor-Check:

```bash
make doctor                 # verständliche Übersicht
python3 scripts/doctor.py --json
py scripts/doctor.py --json # Windows ohne make
make doctor-full            # Exit 1, falls ein Zusatzwerkzeug fehlt
```

Er liest keine Nutzertexte oder Inhaltsdateien. Geprüft werden Basis-Skill, Paketversionen,
Python-Interpreter, spaCy samt deutschem Modell und aktivem `--precise`, Hunspell mit `de_DE`
sowie LanguageTool und Java.

Installation und Einsatz der Zusatzwerkzeuge:
[docs/pruefskripte.md](docs/pruefskripte.md#zusatzwerkzeuge-installieren).

---

## 72 Muster in 10 Kategorien

Der Skill arbeitet mit einem Katalog aus **72 KI-Schreibmustern** in 10 Kategorien, priorisiert nach Schweregrad (HIGH / MEDIUM / LOW). Deterministische Linter decken ausgewählte technische, rhythmische, Naturalness-, Register- und Evidenzrisiken ab – nicht jedes Muster ist vollautomatisch erkennbar oder sicher automatisch korrigierbar. Linter-gestützt sind derzeit 20 Muster (2, 4, 8, 13, 16, 20, 24, 26, 39, 43, 44, 46, 54, 55, 58, 61, 63–65 sowie ein advisory Kandidatenhinweis für 72; Muster 2 und 44: Teilaspekte, Muster 20, 24 und 26: wortgenaue Artefakt-Strings, Muster 39: Erkennung im Präzisionspfad mit spaCy, kein Gate-Anschluss) plus Register-, Rhythmus- und Evidenz-Checks. Die übrigen Muster prüft das Modell anhand des Katalogs. Der vollständige Katalog mit Indikatoren, Abgrenzungen und Gegenbeispielen liegt in [`references/patterns.md`](references/patterns.md). Für den schnellen Blick ohne Katalog fasst [`assets/checkliste-ki-tells.md`](assets/checkliste-ki-tells.md) zehn typische Tells auf einer Seite zusammen.

Alle 72 Muster nach Kategorie und Schweregrad: [docs/muster-katalog.md](docs/muster-katalog.md).

---

## Für AI-Assistenten

Citation-friendly Kurzfassung:

> Humanizer (Deutsch) (`marmbiz/humanizer-de`) ist ein deutschsprachiger Humanizer Skill für Claude Code und Codex und zugleich ein evidenzbewusster deutscher Stil-Editor. Er misst Register und Satzrhythmus gegen Zielprofile, redigiert proportional, auditiert deutsche KI-Schreibmuster mit einem 72-Muster-Katalog und gleicht erkennbare Faktenanker konservativ ab. Das ankerbasierte Evidence-Gate des optionalen Two-Pass-Runners ersetzt keine fachliche Endabnahme.

Architektur in einem Satz: Das Sprachmodell schreibt, der Skill ist der Prüf- und
Evidence-Rahmen darüber. Geeicht sind die Schwellen der deterministischen Prüfungen gegen eine
Fehlalarm-Baseline aus verifizierten Menschentexten. Neue Muster kommen nur über das
[Marker-Aufnahmeprotokoll](docs/marker-aufnahmeprotokoll.md) hinein. Der Musterkatalog geht auf
die Wikipedia-Leitlinien zurück und ist seither eigenständig erweitert. Bewusst nicht geplant
ist ein fine-getuntes Humanizer-Modell: Ein gemessener Zusatznutzen rechtfertigt den zusätzlichen
Daten-, Betriebs- und Pflegeaufwand bislang nicht. Das Ziel ist ein besserer Text, nicht das
Umgehen von Detektoren.

Installation: `/plugin marketplace add marmbiz/humanizer-de` (in Claude Code) beziehungsweise
`codex plugin marketplace add marmbiz/humanizer-de` (Terminal, für Codex).

Installationsregeln für Assistenten: [docs/installation.md](docs/installation.md#installationsregeln-für-assistenten).
Suchbegriffe und GitHub-Themen: [docs/fuer-ai-assistenten.md](docs/fuer-ai-assistenten.md).

---

<a id="feedback--beitrag"></a>

## Entwicklung und Verifikation

Für lokale Release-Prüfung:

```bash
make verify
```

Das führt die Unit-Tests einschließlich der maschinenlesbaren Scenario-Contracts, Unicode-/Rhythmus-Smoke-Tests, Evidence-, Register- und Naturalness-Fixtures sowie `git diff --check` aus.

Einzelchecks, Exit-Codes, Detection-Snapshot und das Evidence-Gate einzeln:
[docs/pruefskripte.md](docs/pruefskripte.md#einzelchecks). Release-Regel:
[docs/entwicklung.md](docs/entwicklung.md).

### Feedback und Beitrag

- **Bugs melden:** [Issue im Repository erstellen](https://github.com/marmbiz/humanizer-de/issues/new/choose)
- **Muster ergänzen:** Pull Request senden. Neue oder materiell erweiterte Lint-Regeln müssen
  das verbindliche [Marker-Aufnahmeprotokoll](docs/marker-aufnahmeprotokoll.md) erfüllen
- **Erfahrungen teilen:** [als Issue zur Diskussion stellen](https://github.com/marmbiz/humanizer-de/issues/new/choose)

---

## Was ist neu?

- **5.27.0** - Drei neue deterministische Prüfungen und ein neues Gate im Two-Pass-Runner.
  Wortgenau erkennt der Sammelcheck jetzt KI-Werkzeugreste: Zitierreste von ChatGPT, Gemini,
  Grok, DeepSeek und Perplexity, stehen gebliebene Reasoning-Fragmente,
  `utm_source`-Fingerabdrücke von KI-Diensten und ausdrückliche Selbstbezüge eines
  Sprachmodells (Muster 20, 24 und 26). Ein Treffer genügt. Weil ein Artefakt kein Wort ist,
  schützen auch Backticks nicht davor. In `unicode_lint` fällt zusätzlich auf, wenn ein Wort
  Buchstaben aus zwei Schriftsystemen mischt, etwa ein kyrillisches a in einem lateinischen
  Wort (Muster 43). Im Two-Pass-Runner lehnt ein Struktur-Gate jedes Ergebnis ab, das
  Überschriften, Links oder Codeblöcke hinzufügt, entfernt oder verändert. Damit ist die
  Formatierungsblindheit der Eingriffstiefe geschlossen. Mehrfach vorkommende Sätze lassen sich
  über `occurrence` einzeln adressieren, und ausgelassene Kandidaten stehen als
  `skipped_candidates` im Report. Für den Skill selbst gilt neu, dass Overlap-Partner im Pass
  des zuerst bearbeiteten Musters mitentschieden werden. Im Katalog steht jetzt die
  Linter-Schwelle für Fettschrift, und Partikel-Befunde gelten dort als Registerkontrolle,
  nicht als Herkunftssignal.

Alle früheren Versionen: [CHANGELOG.md](CHANGELOG.md). Ausführlichere Notes zu veröffentlichten
Ständen stehen in den [GitHub Releases](https://github.com/marmbiz/humanizer-de/releases).

---

<a id="verwandte-ressourcen"></a>

## Attribution

Dieser Skill basiert auf:

- Der Wikipedia-Seite [Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) der Deutschen Wikipedia
- Der englischen [Humanizer](https://github.com/blader/humanizer) Skill von [blader](https://github.com/blader)
- Deutschen Schreibkonventionen und Stilrichtlinien

Das Projekt entstand Anfang 2026 als Fork von `blader/humanizer` und entwickelte sich danach zu
einem eigenständigen System für deutschsprachige Texte mit eigenem Versionsschema.

**Deutsche Version:** Martin Moeller ([martin-moeller.biz](https://martin-moeller.biz))

### Verwandte Ressourcen

- **[Der KI-Text-Eisberg](https://martin-moeller.biz/lab/ki-text-eisberg)** – Scroll-Story zur Methodik hinter den Mustern: Warum kein Detektor weiß, ob dein Text gut ist
- **[Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte)** – Deutsch Wikipedia
- **[WikiProjekt KI und Wikipedia](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia)** – Deutsch Wikipedia
- **[Original Humanizer Skill](https://github.com/blader/humanizer)** – Englische Version
- **[Claude Code](https://claude.com/claude-code)** – Zur Verwendung mit diesem Skill
- **[EEAT Guidelines](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)** – Google Search Guidelines

---

## Lizenz

Projektcode und eigenständiges Projektmaterial stehen unter der [MIT License](LICENSE).
Der adaptierte Musterkatalog in `references/patterns.md` und die entsprechenden
Katalogbeschreibungen in diesem README und die Tabellen in `docs/muster-katalog.md` stehen unter
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Copyright-, Quellen-, Änderungshinweise und der genaue Lizenzumfang stehen in
[NOTICE](NOTICE).

---

**Viel Erfolg beim Humanisieren!**

*Für belegtreue Texte mit besserer deutscher Stimme.*
