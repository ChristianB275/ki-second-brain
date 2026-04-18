# 05-Daily

Tages-Logs im Format `YYYY-MM-DD.md`. Werden automatisch durch `/os shutdown` erstellt.

**Was reinkommt:**
- Was in der Session passiert ist
- Entscheidungen die getroffen wurden
- Offene Punkte fuer die naechste Session

**Regel:** Daily Logs sind append-only — bestehende Eintraege nicht ueberschreiben, nur ergaenzen.

**Tipp:** Claude liest die letzten 2 Daily Logs bei jedem `/os start` fuer Kontinuitaet.
