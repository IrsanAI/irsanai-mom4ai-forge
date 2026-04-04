# IrsanAI README Auto Sync Manager

`readme_sync_manager.py` hält die mehrsprachigen Readmes inhaltlich synchronisiert
und schreibt eine visuelle Sync-Anzeige direkt in die Dateien.

## Features

- analysiert `README.md` (Deutsch) und `README.en.md` (Englisch)
- vergleicht H2-Sektionsabdeckung + Roadmap-Item-Anzahl
- berechnet einen `context_delta_score`
- schreibt Sync-Status-Block in beide Readmes (`🟢`/`🟠`)
- erzeugt `docs/readme_sync_report.json`
- optionaler CI-Gate via `--check` (fail wenn out-of-sync)

## CLI

```bash
python src/readme_sync_manager.py
python src/readme_sync_manager.py --check
```

## CI Integration

Workflow: `.github/workflows/readme-sync.yml`

Bei jedem Push/PR läuft der Check und lädt den Report als Artefakt hoch.
