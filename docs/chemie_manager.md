# IrsanAI Chemie Manager

Der **IrsanAI Chemie Manager** analysiert die KPI-Roadmap in `README.md` und erzeugt
einen priorisierten Optimierungsplan.

## Ziel

- IST-Status der Roadmap maschinell auslesen
- Resonanz-/Chemie-Werte interpretieren
- offene Items priorisieren
- konkrete „Mastermind“-Next-Steps vorschlagen

## CLI

```bash
momai-chemie-manager
```

JSON-Ausgabe (für Automatisierung/CI):

```bash
momai-chemie-manager --json
```

## Was wird berechnet?

- Anzahl Roadmap-Items, abgeschlossen/offen
- Completion Rate
- Durchschnittliche Resonanz/Chemie der offenen Items
- Top Next Priority
- Ranking aller offenen Items mit Priority-Score

## Nutzen im Repo

Das Tool verbindet strategische Roadmap-KPIs mit dem operativen Engineering-Backlog
und schafft damit eine wiederholbare Entscheidungslogik im IrsanAI-Style.
