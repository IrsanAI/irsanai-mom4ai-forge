# Resonance Protocol (RP) – v0.1

Mom4AI Forge nutzt jetzt ein zweistufiges Überlebensmodell:

1. **Auto-Fitness** als Vorfilter (Graph-Struktur)
2. **Resonanz-Fitness** aus echten Interaktionen (Mensch oder Agent)

## Event-Format

Lege eine Datei `resonance_events.jsonl` im Repo-Root an. Jede Zeile ist ein JSON-Objekt:

```json
{
  "skeleton_name": "MyzelAmeisen-G2-11-ab12cd34",
  "intent_match": 0.9,
  "context_match": 0.8,
  "tone_match": 0.7,
  "reliability": 0.85,
  "coordination": 0.88,
  "actor_type": "human",
  "session_id": "chat-42"
}
```

Alle Scores sind im Bereich **0.0 bis 1.0**.

## Klassifikation

- `resonant` (>= 0.75, mit mindestens 3 Interaktionen)
- `emerging` (>= 0.55)
- `neutral` (>= 0.35)
- `non_resonant` (< 0.35)
- `insufficient_data` (< 3 Interaktionen)

## Selection-Logik

- Ohne Interaktionsdaten zählt nur Auto-Fitness.
- Mit Interaktionsdaten steigt das Gewicht der Resonanz bis auf 70% (ab 5 Interaktionen).

Damit gilt praktisch:

> **Auto-Fitness ist Geburtshilfe. Resonanz ist Lebensfähigkeit.**

