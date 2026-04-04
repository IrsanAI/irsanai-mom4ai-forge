# Mom4AI Forge
<!-- README_SYNC_STATUS_START -->
🟢 **Readme Language Sync:** `up_to_date`  
🌐 **Context Delta:** `0`  
🕒 **Last Sync Check (UTC):** `2026-04-04T00:26:03Z`
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
- [x] Interactive Hall of Fame (search, filters, stats)
- [x] Automatic Push via PAT
- [x] Base Mutation & Crossover
- [x] Advanced Evolution (lineage-aware parent selection)
- [x] Multi-objective Selection (fitness + resonance + diversity)
- [x] Initial Resonance Scoring (JSONL interaction score)
- [x] Live Resonance Ingestion (`POST /api/resonance_event`)
- [x] Session Continuity (`resonance_sessions.json` aggregation)
- [x] Live Resonance Streaming (SSE)
- [x] Native Runtime Adapter (`momai-adapter`)
- [x] OpenAI/Agents/Custom Hook Integration (`momai-hook`)
- [x] Native Runtime Semantics (tool-calls/recovery/follow-up)
- [x] Direct SDK Hooks (Agents/OpenAI/Custom)
- [x] Vendor-native Auto Wiring (OpenAI-like)
- [x] Provider-specific depth (OpenAI-like tracing)
- [x] Multi-provider backends (OpenAI-like + Anthropic-like normalization)
- [x] Community ranking & rarity badges
- [x] Vis.js Evolution Tree in Hall of Fame
- [ ] Mini-transformer from graph skeletons
- [x] IrsanAI Chemie Manager (KPI interpretation + portfolio optimization)
- [x] IrsanAI Readme Auto Sync Manager (DE/EN delta + status indicator)

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
- IrsanAI Chemie Manager: `docs/chemie_manager.md`
