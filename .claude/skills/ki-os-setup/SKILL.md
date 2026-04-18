---
name: ki-os-setup
description: KI OS Setup — Erstellt die Vault-Struktur, fuehrt ein 3-Fragen-Onboarding durch und personalisiert alle Dateien. Verwende wenn der Nutzer /setup ausfuehrt, "einrichten", "setup", "bootstrap" oder "initialisieren" sagt.
---

# KI OS — Setup + Onboarding

## Pre-flight Check

1. Pruefe ob `03-strategy/current-priorities.md` im aktuellen Verzeichnis existiert
2. Falls ja: "Dieses Vault ist bereits eingerichtet. Moechtest du das Onboarding nochmal durchlaufen (bestehende Struktur bleibt) oder alles zuruecksetzen?"
3. Falls nein: Weiter mit Phase A

---

## Phase A: Onboarding (3 Fragen)

Lies `references/onboarding-questions.md` fuer die exakten Fragen und Anweisungen.

**Wichtig:**
- Stelle jede Frage einzeln. Warte auf die Antwort bevor du weitergehst.
- Akzeptiere jedes Format: kurzer Satz, Wall of Text, LinkedIn-Profil, "skip"
- Keine Nachfragen. Extrahiere was du kannst.
- Nach jeder Antwort: kurze Bestaetigung (1 Satz), dann naechste Frage

Speichere die Antworten intern als:
- `{{NAME}}` — Name des Nutzers
- `{{KURZBESCHREIBUNG}}` — Was er/sie macht, fuer wen
- `{{ANGEBOT}}` — Produkte/Dienstleistungen
- `{{ZIELGRUPPE}}` — Fuer wen
- `{{HERAUSFORDERUNG}}` — Groesste aktuelle Herausforderung
- `{{PROJEKTE}}` — Liste aktiver Projekte (Name + Ziel)
- `{{DATUM}}` — Heutiges Datum (YYYY-MM-DD)
- `{{KW}}` — Aktuelle Kalenderwoche

---

## Phase B: Vault erstellen

Lies `references/vault-structure.md` fuer die vollstaendige Ordner- und Dateistruktur.

### Schritt 1: Ordner erstellen

Erstelle alle 10 nummerierten Ordner und Unterordner wie in `vault-structure.md` definiert.

### Schritt 2: Folder-Guides schreiben

Lies jeden Guide aus `references/folder-guides/` und schreibe ihn als `_guide.md` in den entsprechenden Ordner:
- `references/folder-guides/00-inbox.md` → `00-inbox/_guide.md`
- `references/folder-guides/01-context.md` → `01-context/_guide.md`
- `references/folder-guides/02-brand.md` → `02-brand/_guide.md`
- `references/folder-guides/03-strategy.md` → `03-strategy/_guide.md`
- `references/folder-guides/04-projects.md` → `04-projects/_guide.md`
- `references/folder-guides/05-daily.md` → `05-daily/_guide.md`
- `references/folder-guides/06-team.md` → `06-team/_guide.md`
- `references/folder-guides/07-intelligence.md` → `07-intelligence/_guide.md`
- `references/folder-guides/08-resources.md` → `08-resources/_guide.md`
- `references/folder-guides/09-reference.md` → `09-reference/_guide.md`

### Schritt 3: Context-Dateien erstellen

Lies die Templates aus `references/context-templates/` und ersetze die Platzhalter mit den Onboarding-Antworten:

- `references/context-templates/ich.md` → `01-context/ich.md` (mit {{NAME}}, {{KURZBESCHREIBUNG}})
- `references/context-templates/business.md` → `01-context/business.md` (mit {{ANGEBOT}}, {{ZIELGRUPPE}}, {{HERAUSFORDERUNG}})
- `references/context-templates/strategie.md` → `03-strategy/current-priorities.md` (mit {{KW}}, {{DATUM}})
- `references/context-templates/open-loops.md` → `03-strategy/open-loops.md` (mit {{DATUM}})
- `references/context-templates/projekte.md` → `04-projects/README.md` (mit {{PROJEKTE}})

Erstelle zusaetzlich fuer jedes genannte Projekt einen Unterordner mit `README.md`:
- `04-projects/{projektname-kebab}/README.md` mit Ziel und Status "Aktiv"
- Verlinke das Projekt mit `[[ich]]` und ggf. `[[business]]`

### Schritt 4: Weitere Seed-Dateien

- `00-inbox/capture.md` — Leere Inbox mit Header
- `02-brand/brand-voice.md` — Minimales Template (Ton, Stil, Regeln)
- `09-reference/weekly-log.md` — Leerer Weekly Log mit Tabellenheader
- `09-reference/completed-projects.md` — Leeres Archiv mit Header

### Schritt 5: CLAUDE.md personalisieren

Lies `references/claude-md-template.md` und ersetze alle Platzhalter. Ueberschreibe die bestehende `CLAUDE.md` im Vault-Root mit der personalisierten Version.

### Schritt 6: Erster Daily Log

Erstelle `05-daily/{{DATUM}}.md`:
```markdown
# {{DATUM}}

> Siehe auch: [[ich]], [[current-priorities]]

## Setup
- KI OS eingerichtet
- Vault-Struktur erstellt
- Kontext personalisiert

## Naechste Schritte
[Basierend auf den genannten Projekten die wichtigsten 2-3 naechsten Schritte auflisten]
```

---

## Phase C: Abschluss

Zeige eine kompakte Zusammenfassung:

```
KI OS eingerichtet fuer [Name].

Erstellt:
- 10 Vault-Ordner mit Guides
- [X] Kontext-Dateien (ich, business, strategie, open-loops)
- [X] Projekt-Ordner ([Projektnamen])
- Personalisierte CLAUDE.md

Naechste Schritte:
1. Oeffne diesen Ordner in Obsidian als Vault
2. Starte jede Claude Code Session mit /start
3. Beende jede Session mit /shutdown

Alle Commands: /start | /capture | /plan | /review | /shutdown
```

---

## Regeln

- Nie den Nutzer fragen "Soll ich das speichern?" — einfach machen
- Alle Dateien auf Deutsch, technische Begriffe (kebab-case, wiki-links) auf Englisch
- Wiki-Links ([[dateiname]]) in JEDER erstellten Datei
- Dateinamen: kebab-case, keine Emojis, keine Umlaute
- Keine leeren Placeholder-Dateien — jede Datei hat mindestens einen sinnvollen Header
