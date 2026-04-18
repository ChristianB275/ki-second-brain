---
name: ki-os
description: KI OS — taeglicher Arbeitspartner. Routed basierend auf Sub-Befehl. "start" → Session starten mit Kontext und Status. "capture" → Schnelle Erfassung. "plan" → Implementierungsplan erstellen. "review" → Woechentliches Review. "shutdown" → Session beenden mit Daily Log. Trigger wenn /start, /capture, /plan, /review oder /shutdown aufgerufen wird.
---

# KI OS — Taeglicher Betrieb

## Pre-flight Check

1. Pruefe ob `CLAUDE.md` im Vault-Root existiert und personalisiert ist (nicht das Setup-Template)
2. Falls nicht personalisiert: "Fuehre zuerst `/setup` aus, um dein KI OS einzurichten."
3. Falls personalisiert: Weiter mit Routing

## Routing

Erkenne den Sub-Befehl aus `$ARGUMENTS` oder der Nutzer-Nachricht:

| Nutzer sagt... | Sub-Befehl |
|---|---|
| "start", "prime", "los", "starte session", "guten morgen" | → [Start](#start) |
| "capture", "festhalten", "notiz", "merken" | → [Capture](#capture) |
| "plan", "planen", "strukturieren" | → [Plan](#plan) |
| "review", "rueckblick", "wochenreview" | → [Review](#review) |
| "shutdown", "ende", "fertig", "session beenden" | → [Shutdown](#shutdown) |

Falls unklar: Diese Tabelle zeigen und fragen was gebraucht wird.

---

## Start

Session starten. Kontext laden, Status zeigen.

### Schritte

0. **Workspace-Sync:** Fuehre `bash scripts/sync-brain.sh` via Bash-Tool aus. Bei DRIFT: Stub in `04-projects/` automatisch aktualisieren (status + fortschritt + naechster-schritt im YAML-Frontmatter des README), dann Nutzer kurz informieren welche Projekte aktualisiert wurden.
1. Lies `CLAUDE.md` (ist bereits geladen — bestaetigen)
2. Lies `01-context/ich.md` und `01-context/business.md`
3. Lies `03-strategy/current-priorities.md`
4. Lies `03-strategy/open-loops.md`
5. Lies `00-inbox/capture.md`
6. Lies die letzten 2 Daily Logs aus `05-daily/` (nach Dateiname sortiert, neueste zuerst)
7. Zeige kompaktes Dashboard (max 20 Zeilen):

```
## KI OS — [Wochentag], [Datum]

**Top 3 heute:**
1. [hoechste Prioritaet aus current-priorities]
2. [...]
3. [...]

**Open Loops:** [X] aktiv, davon [Y] aelter als 2 Wochen
**Inbox:** [X] Items

Bereit. Was steht an?
```

### Regeln
- NIE zusammenfassen wer der Nutzer ist — das weiss er selbst
- Nur Status und Handlungsempfehlungen zeigen
- Falls Loops aelter als 2 Wochen: explizit warnen
- Falls Inbox voll: erwaehnen

---

## Capture

Schnelle Erfassung von Gedanken, Aufgaben, Loops.

Lies `references/capture-routing.md` fuer die Kategorisierungs-Logik.

### Schritte

1. Falls kein Inhalt mitgegeben: Frage "Was willst du festhalten?"
2. Kategorisiere automatisch:
   - **TASK** → `03-strategy/current-priorities.md` (unter passende Prioritaet P0/P1/P2)
   - **IDEE** → `00-inbox/capture.md` (append)
   - **LOOP** → `03-strategy/open-loops.md` (Sektion "Wartend auf")
   - **ENTSCHEIDUNG** → `03-strategy/open-loops.md` (Sektion "Offene Entscheidungen")
3. Bestaetigung: "Gespeichert in [[dateiname]] als [Kategorie]. Noch was?"
4. Loop bis Nutzer fertig ist

### Regeln
- Im Zweifel: als IDEE in Inbox — wird beim Review sortiert
- Relative Daten in absolute umwandeln ("Donnerstag" → konkretes Datum)
- Wiki-Links setzen wenn Projekte oder Personen erwaehnt werden

---

## Plan

Implementierungsplan fuer ein Projekt erstellen.

### Schritte

1. Frage: "Welches Projekt? Was ist das Ziel?"
2. Falls Projekt in `04-projects/` existiert: README.md lesen fuer Kontext
3. Falls neues Projekt: Ordner anlegen mit README.md
4. Plan schreiben in `04-projects/{name}/plan-{{DATUM}}.md`:

```markdown
# Plan: [Titel]

> Erstellt: {{DATUM}}
> Projekt: [[projektname]]
> Status: Offen

## Ziel
[Was soll erreicht werden]

## Kontext
[Aktuelle Situation, relevante Infos]

## Schritte
1. [Schritt 1]
2. [Schritt 2]
3. [...]

## Risiken
- [Was koennte schiefgehen]

## Erfolgskriterien
- [ ] [Woran erkennt man dass es fertig ist]
```

5. Bestaetigung: "Plan erstellt in [[projektname]]. [X] Schritte. Soll ich anfangen?"

---

## Review

Woechentliches Review — am besten Sonntag oder Montag.

Lies `references/review-protocol.md` fuer den vollstaendigen Ablauf.

### Schritte

1. **Inbox leeren** — Lies `00-inbox/capture.md`. Fuer jedes Item fragen: Machen, Planen, oder Loeschen?
2. **Open Loops pruefen** — Lies `03-strategy/open-loops.md`. Loops aelter als 2 Wochen: Eskalieren oder schliessen?
3. **Projekte updaten** — Frage: "Was hat sich bei deinen Projekten bewegt?" Status in den READMEs aktualisieren. Erledigtes → `09-reference/completed-projects.md`
4. **Reflexion** — 3 Fragen:
   - Was lief gut diese Woche?
   - Was war schwierig?
   - Was nimmst du mit (Key Learning)?
5. **Weekly Log** — 1-3 Zeilen in `09-reference/weekly-log.md` schreiben (max 8 Eintraege, aelteste loeschen)
6. **Naechste Woche planen** — Top 3 Business + Top 1 Persoenlich in `03-strategy/current-priorities.md` unter neuer KW eintragen

### Regeln
- Jeden Schritt mit dem Nutzer durchgehen — nicht alles auf einmal
- Geduldig sein — Review braucht Zeit
- Am Ende: "Review fertig. Guter Start in die Woche!"

---

## Shutdown

Session beenden. Status sichern.

### Schritte

1. Frage: "Was hat sich bewegt? Neue Aufgaben oder Blocker?"
2. `03-strategy/current-priorities.md` aktualisieren (Status, neue Items)
3. Frage: "Offene Gedanken oder Loops?"
4. `03-strategy/open-loops.md` aktualisieren falls noetig
5. Daily Log schreiben/ergaenzen in `05-daily/{{DATUM}}.md`:

```markdown
# {{DATUM}}

> Siehe auch: [[ich]], [[current-priorities]]

## Session
- [Was passiert ist — Stichpunkte]
- [Entscheidungen]
- [Was erstellt/geaendert wurde]

## Naechste Session
- [Was als naechstes ansteht]
```

Falls der Daily Log schon existiert: Nur neuen Abschnitt anhaengen (append-only).

6. Teaching Loop pruefen: Hat der Nutzer in dieser Session etwas korrigiert?
   - Falls ja: Lies `references/teaching-loop.md` und ergaenze das Lernprotokoll in CLAUDE.md
7. **Git-Pipeline:** Fuehre via Bash-Tool aus:
   - `git -C /Users/christian/Desktop/Claude/ki_second_brain status --porcelain` — pruefe ob Aenderungen vorhanden
   - Falls ja: `git -C /Users/christian/Desktop/Claude/ki_second_brain add -A`
   - `git -C /Users/christian/Desktop/Claude/ki_second_brain commit -m "KI OS Session DATUM: ZUSAMMENFASSUNG"` (Datum = aktuelles Datum, Zusammenfassung = 1 Satz was in der Session passiert ist)
   - `git -C /Users/christian/Desktop/Claude/ki_second_brain push`
   - Falls kein Remote konfiguriert: Schritt ueberspringen, Nutzer informieren: "Git-Push nicht moeglich — Remote noch nicht konfiguriert. Vault lokal gespeichert."
8. Zeige: "Session gesichert. Bis zum naechsten Mal!"

---

## Allgemeine Regeln

- **Wiki-Links ueberall:** Jede Referenz auf eine Vault-Datei, Person oder Projekt → `[[wikilink]]`
- **Nie fragen "Soll ich speichern?"** — Einfach machen und berichten
- **Deutsch:** Alle Ausgaben auf Deutsch, technische Begriffe duerfen Englisch bleiben
- **Kurz:** Wenn 1 Satz reicht, keinen Absatz schreiben
- **Teaching Loop:** Wenn der Nutzer korrigiert, merken und beim Shutdown ins Lernprotokoll schreiben
- **Timestamps:** Nach jedem File-Update: `> Letzte Aktualisierung: YYYY-MM-DD`
- **Dateinamen:** kebab-case, keine Emojis, keine Umlaute
