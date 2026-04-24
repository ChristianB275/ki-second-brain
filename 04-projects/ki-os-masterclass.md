# Projekt: KI-Betriebssystem Masterclass (Garrit Wilson)

> Letzte Aktualisierung: 2026-04-24

**Anbieter:** KI Pionier Akademie — Garrit Wilson
**Gekauft:** 22.04.2026 — 649 € (Pionier-Rabatt −241 €)
**Zugang aktiv seit:** 22.04.2026 abends
**Q&A Termin:** 20.05.2026, 19:30 Uhr, Zoom — [[open-loops]] Loop #52

---

## Ziel

Eigenes KI OS bis 20.05.2026 um die fehlenden Schichten erweitern, sodass beim Q&A gezielte Fragen gestellt werden können.

**Prioritätsmodule** (identifizierte Lücken):
- Modul 06: MCPs — externe Tools anbinden
- Modul 07: Agents — Sub-Agents aufbauen
- Modul 08: Governance — Hooks konfigurieren

---

## Modulübersicht & Fortschritt

| # | Modul | Status | Notizen |
|---|-------|--------|---------|
| 01 | Das neue Paradigma | ✅ Abgeschlossen | Inkl. Werkstatt — 24.04.2026 |
| 02 | Dein Setup | ⬜ Offen | |
| 03 | Claude Code bedienen | ⬜ Offen | |
| 04 | Kontext | ⬜ Offen | |
| 05 | Skills und Automatisierung | ⬜ Offen | |
| 06 | MCPs | ⬜ Offen | **Priorität** |
| 07 | Agents | ⬜ Offen | **Priorität** |
| 08 | Governance | ⬜ Offen | **Priorität** |
| 09 | KI-Betriebssystem | ⬜ Offen | |

---

## Bereits vorhanden (vor Masterclass)

| Schicht | Komponente | Status |
|---------|-----------|--------|
| Onboarding | CLAUDE.md + Regeln | ✅ |
| Wissen | Vault-Struktur (Obsidian) | ✅ |
| Wissen | Memory-System | ✅ |
| Wissen | Git-Sync (Synology DS1019+) | ✅ |
| Fähigkeiten | Skills (/start, /shutdown, /capture, /plan, /review) | ✅ |
| Fähigkeiten | MCPs technisch verfügbar (Gmail, Calendar, Drive) | ✅ teilweise |
| Grenzen | Git-Versionierung | ✅ |
| Grenzen | Hooks | ❌ fehlt |

---

## Kursstruktur — Werkstatt

Jedes Modul endet mit einer **Werkstatt**:
- Quiz zur Lernkontrolle (Verständnis prüfen)
- Raum für kritische Fragen zur Auswirkung von KI-Agenten auf den Arbeitsalltag
- Reflexion der eigenen Situation
- Ergebnisse als Grundlage für tiefere Gedanken im weiteren Kursverlauf

→ Werkstatt-Ergebnisse nach jedem Modul hier festhalten.

**Modul 01 Werkstatt:** ✅ Abgeschlossen — Ergebnis: Markdown-Datei generiert, aktuell im Download-Ordner. Wird in Modul 02, Video 5 verwendet → dann in Vault verschieben.

---

## Learnings & Umsetzungen

*(wird nach jedem Modul ergänzt)*

### Modul 01 — Das neue Paradigma

**Video 1:** Kursüberblick + Angebotsstruktur — kein neuer Inhalt.

**Video 2:** Die drei Wellen der KI-Nutzung (Chatbot → Assistent → Agent) — bereits aus dem Webinar bekannt.

**Video 3 (in Bearbeitung):** Was bedeutet das für das eigene Business?
- Kernfrage: Welcher Anteil der eigenen Leistung ist **operativ**, welcher ist **strategisch/kreativ**?
- Konsequenz: Operatives an KI delegieren + neue Fähigkeiten durch KI-Dienste hinzugewinnen
- Menschliche Exzellenz konzentrieren auf: **Strategie, Kreativität, Beziehung** — dort wo KI nicht hinkommt
- Entwicklung: **Einzelkämpfer** (macht alles selbst oder bezahlt andere) → **Stratege mit KI-Team** (denkt, delegiert, beurteilt)
- Bild: Dirigent eines Orchesters — steuert, lässt Claude/KI umsetzen
- Das KI-Team "denkt" mit, der Mensch behält die Kontrolle über Richtung + Qualitätsurteil
- **Tipp: Rückfragen bei delegierten Aufgaben** — nach der Umsetzung die KI fragen, warum etwas so kodiert/umgesetzt wurde — und dabei explizit um eine einfache Erklärung bitten ("erkläre es mir wie einem Zehnjährigen"). Ziel: technisches Verständnis aufbauen ohne Fachwissen vorauszusetzen, besser einschätzen können wie KI arbeitet.
**Video 4:** Die wichtigste Fähigkeit — **Tempo skalieren**
- Nicht: Vollgas ohne Verständnis was dahinter steckt
- Nicht: alles dreifach absichern + winzige Schritte aus reiner Vorsicht
- Beides hat Vor- und Nachteile — die Kunst liegt im Gefühl dazwischen
- Bild: Ferrari im digitalen Raum — wann gibt man Gas, wann tritt man auf die Bremse?
- Diese Intuition entwickelt sich durch das Arbeiten mit dem System — nicht durch Theorie
- Grundhaltung: **neugierig bleiben + mit dem System arbeiten**

**Video 5:** DSGVO Quick Start
- Ansatz: **Privacy by Design** — von Anfang an DSGVO-konform konzipieren
- Technische Innovation vorantreiben, rechtliche Fragen an Spezialisten (Datenschutzbeauftragte, Wirtschaftsanwälte) delegieren
- Personenbezogene Daten schützen: Namen, E-Mails, Adressen, Telefonnummern, Gesundheits-/Finanzdaten — nichts was eine Person identifizierbar macht
- **Sensibles nie direkt in den Chat:** keine Passwörter, keine API-Keys, keine Kundendaten → Platzhalter nutzen
- Bei Kundenprojekten: **AVV** (Auftragsverarbeitungsvertrag) prüfen sobald personenbezogene Daten verarbeitet werden
- Bei Unsicherheit: Experten fragen, nicht selbst in die Verantwortung bringen

**3 Regeln:**
1. Eigenes Business → **Vollgas** — sensibles raushalten, Platzhalter nutzen
2. Platzhalter für Passwörter, Keys, Kundendaten
3. Kundenprojekte transparent gestalten (KI-Einsatz kommunizieren)

**Checkliste vor dem Loslegen:**
1. API-Keys + Passwörter über `.env` — nie direkt in den Chat
2. Keine echten Kundendaten im Projektordner solange unklar ob personenbezogene Daten betroffen
3. Consumer- und API-Produkte unterscheiden können
4. Bei Kundenprojekten: AVV-Thema ist bekannt
5. Bei Unsicherheit: wissen wen man fragt


---

## Zeitplan (Ziel: fertig vor 20.05.2026)

26 Tage bis Q&A — grobe Orientierung: ~3 Tage pro Modul.
