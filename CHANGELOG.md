# Changelog

Alle relevanten Änderungen an Mom4AI Forge werden hier dokumentiert.

## [0.1.0-alpha] - 2026-03-21

### Added
- Resonance Protocol v0.1 mit Interaktions-Scoring und Klassifikation (`resonant`, `emerging`, `neutral`, `non_resonant`, `insufficient_data`).
- Resonanz-Integration in die Selektion (`mom_forge.py`) inkl. kombinierter Fitness aus Auto-Fitness + Resonance-Signal.
- Lokaler Hybrid-Dashboard-Server (`src/live_dashboard_server.py`) mit:
  - `GET /api/local_stats`
  - `GET /api/sync_status`
- Ein-Kommando-CLI über `MomAI`/`momai` (via `pyproject.toml` + `src/momai_cli.py`).
- Neue Dokumentation:
  - `docs/resonance_protocol.md`
  - `docs/factory_blueprint.md`
  - `docs/release_readiness.md`
- Baseline CI-Workflow (`.github/workflows/build.yml`) für Python-Syntaxcheck.
- MIT-Lizenz (`LICENSE`).

### Changed
- README: Rendering-Fix im Headerbereich, aktualisierte Quickstart-Sektion, Hybrid-Betrieb und Roadmap-Erweiterungen.
- Docs-Hall-of-Fame UI: Resonanz-Kennzahlen, Top-5-Snapshot und lokale Runtime/Sync-Info.
- `bio_components.py`: stabile Initialisierung von `BIO_COMPONENTS` und erweiterter Komponenten-Katalog.

### Notes
- Diese Version ist als **Pre-release (alpha)** gedacht.
- Fokus: Fundament & Architektur für den nächsten Schritt (Assembly-Line zu Child-GPT + echtes Portal).

