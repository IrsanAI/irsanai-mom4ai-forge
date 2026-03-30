# Vendor-native Auto-Wiring (Multi-Provider MVP)

`vendor_wiring.py` hilft, OpenAI- und Anthropic-ähnliche Response-Payloads direkt in
Resonanz-Events zu überführen.

## Was wird automatisch gemacht?

- Tool-Call-Infos aus Response extrahieren (`tool_calls` oder `choices[0].message.tool_calls`)
- Tool-Use-Blöcke aus Anthropic-ähnlichen `content`-Payloads extrahieren (`type=tool_use`)
- `tool_calls_total` / `tool_calls_success` berechnen
- Provider-Trace-Merkmale auswerten
  - OpenAI-like: `usage.prompt_tokens`, `usage.completion_tokens`, `finish_reason`
  - Anthropic-like: `usage.input_tokens`, `usage.output_tokens`, `stop_reason`
  - optional: `response_ms`
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
  --response-json ./sample_response.json \
  --provider auto
```

Optional kannst du Inferenzwerte überschreiben:

```bash
--recovery-success 0.9 --followup-consistency 0.8
```

Du kannst den Provider auch explizit setzen:

```bash
--provider openai
--provider anthropic
```
