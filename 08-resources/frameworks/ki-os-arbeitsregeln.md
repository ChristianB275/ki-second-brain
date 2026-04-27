# KI OS Arbeitsregeln

> Letzte Aktualisierung: 2026-04-27

## Session-Management

### Wann gleiche Session weiternutzen
- Thema bleibt gleich
- Session unter ~30 Minuten
- Bisheriger Kontext wird noch gebraucht

### `/compact` als Zwischenlösung
- Session wird lang, aber Kontext bleibt relevant
- Komprimiert ohne Reset — Kontinuität bleibt erhalten

### Wann neue Session starten
- Neues Thema oder neue Aufgabe
- Session dauert bereits >1 Stunde
- Claude wiederholt sich oder wird inkonsistent
- Frischer Blick auf ein Zwischenergebnis gewünscht

---

## Kontext-Management

KI-Modelle haben ein Aufmerksamkeitslimit — je größer der Kontext, desto stärker die Abweichung vom Ausgangsziel. Dagegen helfen:

- **Daily Logs** als Anker am Sessionende (`/shutdown`)
- **Vault-Dateien** als persistenter Speicher außerhalb des Kontexts
- **`/start`** lädt gezielt nur den relevanten Kontext neu
- **`/compact`** komprimiert den laufenden Kontext ohne Neustart

Das `/shutdown` → `/start` Ritual ist ein kontrollierter Kontext-Reset mit Anker.

---

## Plan-Modus

| Aufgabe | Vorgehen |
|---|---|
| Einzelfrage, ein Schritt | Direkt loslegen |
| Mehrere Dateien, komplexes Ziel | Plan-Modus zuerst |
| Große Evaluierung / Recherche | Plan-Modus zuerst |

**Warum:** Ein guter Plan vorne spart teure Korrekturrunden und Token. Erst abstimmen, dann ausführen.

---

## Grundprinzipien

- **Iterieren** — kein Ergebnis ist beim ersten Durchgang perfekt
- **Hände am Steuer** — Pläne lesen, eigene Gedanken einbringen, nicht blind abnicken
- **KI = Werkzeug, kein Autopilot** — du bringst Urteilsvermögen, ich bringe Geschwindigkeit
- **Pareto-Prinzip** — 80% übernimmt die KI, 20% Feinschliff erfolgt manuell. Ein 100%-Ergebnis, das exakt trifft, entsteht nicht allein durch die KI.
