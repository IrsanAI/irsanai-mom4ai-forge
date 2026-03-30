# Vendor-native Auto-Wiring (MVP)

`vendor_wiring.py` hilft, OpenAI-ähnliche Response-Payloads direkt in
Resonanz-Events zu überführen.

## Was wird automatisch gemacht?

- Tool-Call-Infos aus Response extrahieren (`tool_calls` oder `choices[0].message.tool_calls`)
- `tool_calls_total` / `tool_calls_success` berechnen
- OpenAI-Trace-Merkmale auswerten (`usage`, `finish_reason`, optional `response_ms`)
- daraus `recovery_success` und `followup_consistency` inferieren
- via `ResonanceSDKHook` automatisch an MomAI senden

## CLI

```bash
momai-vendor-wire \
  --server http://localhost:8080 \
  --skeleton MyzelAmeisen-G2-11-ab12cd34 \
  --session chat-42 \
  --user-text "Bitte plane meinen Tag." \
  --assistant-text "Gerne, hier ist dein Tagesplan." \
  --response-json ./sample_openai_response.json
```

Optional kannst du Inferenzwerte überschreiben:

```bash
--recovery-success 0.9 --followup-consistency 0.8
```
