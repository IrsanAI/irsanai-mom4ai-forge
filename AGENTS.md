# AGENTS.md — Mom4AI Forge Operating Contract

## Repo Intent
Mom4AI Forge entwickelt bio-inspirierte DAG-Skelette zu einer evolutiven KI-Fabrik, in der reale Resonanz (Mensch/Agent) als Selektionssignal zurück in die Evolution fließt.

## Task-Strategie (Pflicht)
- Arbeite in **atomaren Tasks**: eine klar testbare Änderung pro Task.
- Vor jeder Umsetzung: kurz die Zielwirkung auf den Repo-Intent benennen.
- Keine Scope-Explosion: lieber kleine, abschließbare Schritte mit Tests.

## Sprache & Stil
- Dokumentation/Erklärtexte: Deutsch (optional EN-Spiegel in README.en.md).
- Code: englische Bezeichner.
- Kommentare: kurz, technisch, nur wenn nötig.

## Guardrails
- Keine neuen Dependencies ohne explizite Begründung.
- Keine großflächigen Refactors ohne vorherige Teilziele.
- Keine generierten Build-Artefakte committen (`__pycache__`, `*.egg-info`, lokale IDE-Dateien).

## Qualitätsregeln
- Nach Codeänderungen mindestens:
  - `python -m py_compile src/*.py tests/smoke_test.py`
  - `python tests/smoke_test.py`
- Bei README-Änderungen zusätzlich:
  - `python src/readme_sync_manager.py --check`

## Roadmap-Disziplin
- Roadmap-Items müssen den Intent widerspiegeln.
- "Resonanz/Chemie/Coach" nur vergeben, wenn die Änderung im Repo real nachvollziehbar ist.
- Große Vision in kleine nachprüfbare Milestones übersetzen (Assembly, Training, Resonanzklassenlernen).

## Empfohlene Reihenfolge für v0.2
1) DAG→PyTorch Assembly Compiler
2) Child-GPT Training Pipeline
3) Resonanz-Klassenlernen (Human vs Agent) + Anti-Gaming
