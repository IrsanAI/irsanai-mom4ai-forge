# Resonance Lifecycle (Survival Engine MVP)

Dieses Modul modelliert den von dir beschriebenen evolutionären Zustand:

- User ↔ Produkt Resonanz entsteht
- daraus ergibt sich Überleben / Dormanz / Aussterben / Re-Connection

## Zustände

- `thriving`: hohe Resonanz + aktive Nutzung
- `alive`: stabile Resonanz, noch aktiv
- `dormant`: mittlere Resonanz, wenig aktuelle Aktivität
- `reconnecting`: historisch gut, aktuell inaktiv
- `extinct`: zu wenig Resonanz oder zu lange inaktiv

## CLI

```bash
python src/resonance_lifecycle.py \
  --events-file resonance_events.jsonl \
  --output docs/resonance_lifecycle_report.json
```

Der Report ist eine Population-Sicht inkl. `state_counts` und Liste je Skeleton.
