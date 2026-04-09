# OpenAI/Agents Hook (MVP)

Der Hook übersetzt einen Chat-Turn (`user_text`, `assistant_text`) in heuristische
Resonanz-Metriken und sendet den Event an den lokalen MomAI-Server.

## CLI

```bash
momai-hook \
  --server http://localhost:8080 \
  --skeleton MyzelAmeisen-G2-11-ab12cd34 \
  --session chat-42 \
  --user-text "Ich brauche einen Plan für diese Woche." \
  --assistant-text "Gerne! Hier ist ein 7-Tage-Plan mit Prioritäten." \
  --tool-calls-total 3 \
  --tool-calls-success 2 \
  --recovery-success 0.8 \
  --followup-consistency 0.85 \
  --actor agent
```

## Was der MVP-Hook macht

- berechnet einfache Proxy-Metriken (`intent_match`, `context_match`, `tone_match`, `reliability`, `coordination`)
- berechnet Runtime-Semantik (`tool_success_rate`, `recovery_success`, `followup_consistency`, `semantic_quality`)
- baut daraus ein Resonanz-Event
- sendet den Event an `POST /api/resonance_event`

## Nächster Schritt

Direkte Hooks in Agents/SDKs statt CLI-Parameter.
