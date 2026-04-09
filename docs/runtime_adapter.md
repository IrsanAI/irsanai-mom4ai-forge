# Native Runtime Adapter (MVP)

Mit dem Adapter kannst du Resonanz-Events direkt aus einem Chat-/Agent-Lauf an MomAI senden.

## CLI

```bash
momai-adapter \
  --server http://localhost:8080 \
  --skeleton MyzelAmeisen-G2-11-ab12cd34 \
  --session chat-42 \
  --intent 0.91 \
  --context 0.84 \
  --tone 0.79 \
  --reliability 0.86 \
  --coordination 0.88 \
  --actor agent
```

## Output

Der Adapter gibt HTTP-Status + JSON-Antwort aus und schreibt den Event über den
lokalen Server in:
- `resonance_events.jsonl`
- `resonance_sessions.json` (aggregiert)

## Nächster Schritt

Direkte Integrationen für OpenAI/Agents-Framework (Auto-Hooks pro Turn).

