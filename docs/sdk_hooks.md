# SDK Hooks (Agents/OpenAI/Custom) – MVP

Mit `ResonanceSDKHook` kannst du Resonanz-Telemetrie pro Turn senden, ohne manuell
alle Resonanz-Metriken zu setzen.

## Python Integration

```python
from sdk_hooks import ResonanceSDKHook

hook = ResonanceSDKHook(
    server_url="http://localhost:8080",
    skeleton_name="MyzelAmeisen-G2-11-ab12cd34",
    actor_type="agent",
)

status, body = hook.on_turn(
    session_id="chat-42",
    user_text="Ich brauche einen Plan für diese Woche.",
    assistant_text="Gerne! Hier ist ein 7-Tage-Plan mit Prioritäten.",
    tool_calls_total=2,
    tool_calls_success=2,
    recovery_success=0.9,
    followup_consistency=0.85,
)
```

## CLI Demo

```bash
momai-sdk-hook \
  --server http://localhost:8080 \
  --skeleton MyzelAmeisen-G2-11-ab12cd34 \
  --session chat-42 \
  --user-text "Ich brauche einen Plan für diese Woche." \
  --assistant-text "Gerne! Hier ist ein 7-Tage-Plan mit Prioritäten."
```

