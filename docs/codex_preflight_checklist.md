# Codex Preflight Checklist (für dieses Repo)

Vor jedem größeren Prompt/Task kurz abhaken:

- [ ] Ist der Task atomar und in <1 PR sinnvoll reviewbar?
- [ ] Ist klar gesagt, **was nicht** geändert werden darf?
- [ ] Sind Ziel-Dateien explizit genannt?
- [ ] Sind Test-Commands explizit genannt?
- [ ] Ist der Repo-Intent im Prompt sichtbar?
- [ ] Werden DE/EN-Doku-Sync-Anforderungen beachtet (falls README betroffen)?
- [ ] Ist klar, ob nur lokales Repo-Wissen reicht oder Cross-Repo-Kontext nötig ist?

## Prompt-Mini-Pattern

1. **Intent:** Warum dieser Schritt wichtig ist.
2. **Change:** Genau welche Datei/Funktion.
3. **Constraints:** Was nicht anfassen, keine neuen deps usw.
4. **Validation:** Welche Tests/Befehle müssen laufen.
5. **Output:** Erwartetes Ergebnis (z. B. JSON-Key, CLI-Command, Testfall).
