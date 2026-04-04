# Mom4AI Forge
<!-- README_SYNC_STATUS_START -->
🟢 **Readme Language Sync:** `up_to_date`  
🌐 **Context Delta:** `0`  
🕒 **Last Sync Check (UTC):** `2026-04-04T12:36:48Z`
<!-- README_SYNC_STATUS_END -->

**English** | [Deutsch](./README.md)

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-View%20Hall%20of%20Fame-brightgreen?style=for-the-badge&logo=githubpages)](https://irsanai.github.io/irsanai-mom4ai-forge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

## What is Mom4AI Forge?

Mom4AI Forge is an evolutionary pipeline that generates graph-based neural skeletons
from bio-inspired patterns (mycelium, ant swarms, octopus nervous systems, coral reefs,
bird migration, etc.), evaluates them, and keeps the strongest candidates.

## Quickstart

1. Clone repository
```bash
git clone https://github.com/IrsanAI/irsanai-mom4ai-forge.git
cd irsanai-mom4ai-forge
```

2. Install dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

3. Run
```bash
python src/mom_forge.py
# or
MomAI
```

## Roadmap
- [x] Auto-Fitness & Ancestry Tracking
  **Resonance:** `88/100` 🟩🟩🟩🟩⬜
  **Chemistry (Repo-Fit):** `90/100` 🟩🟩🟩🟩🟩
  **Coach Feedback:** Starkes Fundament, stabil mit Datenhaltung verzahnt.

- [x] Interactive Hall of Fame (search, filters, stats)
  **Resonance:** `84/100` 🟩🟩🟩🟩⬜
  **Chemistry (Repo-Fit):** `86/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Gute Sichtbarkeit von Fortschritt, motiviert Contributor.

- [x] Automatic Push via PAT
  **Resonance:** `72/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `78/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Nützlich, aber bleibt sicherheits- und token-sensitiv.

- [x] Base Mutation & Crossover
  **Resonance:** `81/100` 🟩🟩🟩🟩⬜
  **Chemistry (Repo-Fit):** `85/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Klarer Evolutionssprung gegenüber rein zufälligen Geburten.

- [x] Advanced Evolution (lineage-aware parent selection)
  **Resonance:** `83/100` 🟩🟩🟩🟩⬜
  **Chemistry (Repo-Fit):** `88/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Bessere Balance aus Leistung und Vielfalt im Genpool.

- [x] Multi-objective Selection (fitness + resonance + diversity)
  **Resonance:** `79/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `84/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Ab jetzt wird Diversität explizit als Ziel mitoptimiert.

- [x] Initial Resonance Scoring (JSONL interaction score)
  **Resonance:** `76/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `82/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Gute Brücke zwischen Theorie und implementierbarer Praxis.

- [x] Live Resonance Ingestion (`POST /api/resonance_event`)
  **Resonance:** `62/100` 🟨🟨🟨⬜⬜
  **Chemistry (Repo-Fit):** `74/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Runtime-Eingang steht; als Nächstes Session-Memory + Streaming.

- [x] Session Continuity (`resonance_sessions.json` aggregation)
  **Resonance:** `68/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `77/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Kontinuität ist da; nächster Schritt ist Streaming + memory-aware weighting.

- [x] Live Resonance Streaming (SSE)
  **Resonance:** `73/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `79/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Kontinuierlicher Session-Flow steht; nächster Schritt sind native Chat/Agent-Adapter.

- [x] Native Runtime Adapter (`momai-adapter`)
  **Resonance:** `64/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `76/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Adapter-Basis steht; jetzt direkte Framework-Hooks pro Turn.

- [x] OpenAI/Agents/Custom Hook Integration (`momai-hook`)
  **Resonance:** `61/100` 🟨🟨🟨⬜⬜
  **Chemistry (Repo-Fit):** `74/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Hook ist da; jetzt von Heuristik zu echten Runtime-Signalen gehen.

- [x] Native Runtime Semantics (tool-calls/recovery/follow-up)
  **Resonance:** `66/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `78/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Semantik ist integriert; jetzt echte SDK-Hooks automatisieren.

- [x] Direct SDK Hooks (Agents/OpenAI/Custom)
  **Resonance:** `69/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `80/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Hook-Layer steht; nächster Schritt ist echte Vendor-spezifische Auto-Wiring-Integration.

- [x] Vendor-native Auto Wiring (OpenAI-like)
  **Resonance:** `71/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `82/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Wire-up steht; nächster Schritt ist provider-spezifische Tiefe (SDK-native Objekte/Tracing).

- [x] Provider-specific depth (OpenAI-like tracing)
  **Resonance:** `74/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `83/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Der Hook liest jetzt echte Provider-Spuren, nicht nur statische Felder.

- [x] Multi-provider backends (OpenAI-like + Anthropic-like normalization)
  **Resonance:** `66/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `79/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Adapter spricht jetzt mehrere Payload-Stile und normalisiert Semantik konsistent.

- [x] Community ranking & rarity badges
  **Resonance:** `61/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `77/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Contributor-Ranking + Rarity-Badges stärken den Community-Loop sichtbar.

- [x] Vis.js Evolution Tree in Hall of Fame
  **Resonance:** `63/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `78/100` 🟩🟩🟩⬜⬜
  **Coach Feedback:** Interaktive Graph-Ansicht macht Evolution und Contributor-Linien direkt greifbar.

- [x] Mini-transformer from graph skeletons (MVP training + checkpointing)
  **Resonance:** `58/100` 🟨🟨🟨⬜⬜
  **Chemistry (Repo-Fit):** `81/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Von Blueprint zu trainierbarem Artefakt ist jetzt im Repo-End-to-End abbildbar.

- [x] IrsanAI Chemie Manager (KPI interpretation + portfolio optimization)
  **Resonance:** `67/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `85/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** KPI-getriebene Priorisierung macht Roadmap-Steuerung reproduzierbar und mastermind-fähig.

- [x] IrsanAI Readme Auto Sync Manager (DE/EN delta + status indicator)
  **Resonance:** `64/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `88/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Mehrsprachigkeit bleibt nachhaltig konsistent statt über Zeit auseinanderzulaufen.

- [x] Resonance Lifecycle Survival Engine (thriving/alive/dormant/reconnecting/extinct)
  **Resonance:** `70/100` 🟩🟩🟩⬜⬜
  **Chemistry (Repo-Fit):** `86/100` 🟩🟩🟩🟩⬜
  **Coach Feedback:** Modelliert produktnah, dass Überleben erst über echte User-Produkt-Resonanz entschieden wird.

## Resonance Protocol

Mom4AI uses real interaction events as an additional fitness signal:
`intent_match`, `context_match`, `tone_match`, `reliability`, `coordination`.

See `docs/resonance_protocol.md`.

## Local Live Dashboard

Run locally:
```bash
python src/live_dashboard_server.py
```
Open: `http://localhost:8080`

## Next logical step

1. Realtime evolution stream (SSE/WebSocket)
2. Lineage explorer
3. Dual ranking (local vs global)
4. Human + agent feedback layer

## Factory Blueprint

The production-line view remains:
Design → Assembly → Quality → Registry → Feedback.

See `docs/factory_blueprint.md`.

## Contribute & Community

Open issues/PRs, run local generation, and push skeletons to extend the global Hall of Fame.

Guides:
- Runtime Adapter: `docs/runtime_adapter.md`
- OpenAI/Agents Hook: `docs/openai_agents_hook.md`
- SDK Hooks: `docs/sdk_hooks.md`
- Vendor Wiring: `docs/vendor_wiring.md`
- Mini-Transformer Adapter: `docs/mini_transformer_adapter.md`
- Mini-Transformer Training: `docs/mini_transformer_training.md`
- IrsanAI Chemie Manager: `docs/chemie_manager.md`
- Resonance Lifecycle: `docs/resonance_lifecycle.md`
