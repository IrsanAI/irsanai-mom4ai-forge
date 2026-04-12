# T01 — Assembly Compiler Contract

## Status
✅ Done

## Ziel
Definiere den formalen DAG->Model Contract (Knoten-/Kantenanforderungen, Merge-Regeln, Dimensionsschema).

## In-Scope
- Contract-Dokument + Basisschnittstellen
- Fehlerklassen für invalide DAGs

## Out-of-Scope
- Vollständige Trainingsintegration

## Akzeptanzkriterien
- [x] Contract ist dokumentiert und testbar
- [x] Mindestens 5 Invalid-Case-Fehler klar benannt

## Tests
- [ ] `python -m py_compile src/*.py tests/smoke_test.py`
- [ ] `python tests/smoke_test.py`
