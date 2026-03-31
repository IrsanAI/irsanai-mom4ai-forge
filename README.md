# Mom4AI Forge

<p align="center">
  <img src="docs/images/momai-forge-vs-typical-nn.jpg" alt="MomAI Forge vs. typisches neuronales Netz" width="800"/>
  <br>
  <em>Links: typisches neuronales Netz – Rechts: MomAI Forge Topologie</em>
</p>
**Links:** Klassisches Feedforward-Netz  
**Rechts:** MomAI Forge – evolutive, bio-inspirierte Topologie

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-View%20Hall%20of%20Fame-brightgreen?style=for-the-badge&logo=githubpages)](https://irsanai.github.io/irsanai-mom4ai-forge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**Deutsch** | [English](#english)

## Was ist Mom4AI Forge?

Eine offene, evolutionäre Pipeline, die Graph-basierte neuronale Netz-Skelette aus biologisch inspirierten Mustern (Myzel-Netze, Ameisen-Schwärme, Oktopus-Nervensysteme, Korallenriffe, Vogelzüge …) generiert, automatisch bewertet und nur die besten überleben lässt.

Aktueller Stand (März 2026):
- Generierung von Directed Acyclic Graphs (DAGs) mit networkx
- Biologisch inspirierte DNA-Mischung (Plastizität & Dezentralität)
- Auto-Fitness (Density, Modularity, Feedback-Loops)
- PNG-Visualisierungen der Graphen
- Ancestry-Tracking (Lineage + born_count)
- Resonance Protocol v0.1 (Interaction-Score aus echten Dialogen via `resonance_events.jsonl`)
- Hall of Fame (interaktiv, filterbar, live aktualisiert)
- Automatisches Pushen neuer Skelette zum zentralen Repo (optional)

**Live Hall of Fame**: https://irsanai.github.io/irsanai-mom4ai-forge/

## Schnellstart – wie du mitmachst

1. Repository clonen
```bash
git clone https://github.com/IrsanAI/irsanai-mom4ai-forge.git
cd irsanai-mom4ai-forge
```

2. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

Optional (empfohlen für 1-Kommando-Start):
```bash
pip install -e .
```

3. Ersten Run starten
```bash
python src/mom_forge.py
```
oder nach `pip install -e .` einfach:
```bash
MomAI
```

Du wirst einmalig nach einem **unique User-Namen** gefragt (z. B. dein GitHub-Name oder ein Nick). Dieser Name wird zentral in `users.json` registriert – jeder Name darf nur einmal existieren.

4. Neue Skelette generieren lassen
- Gib einfach eine Zahl ein (z. B. 10)
- Die Fabrik erzeugt, bewertet und speichert die Überlebenden
- Am Ende wird automatisch versucht, alles zum zentralen Repo zu pushen

### Wichtig: Automatisches Pushen (optional, aber sehr empfohlen)

Damit deine Skelette in der globalen Hall of Fame landen, muss das Repo pushen dürfen. Dazu brauchst du **einmalig** einen GitHub Personal Access Token (PAT):

1. Gehe zu https://github.com/settings/tokens
2. „Generate new token (classic)“
3. Wähle Scope: **repo**  
   Wenn du Dateien unter `.github/workflows/*` pushen willst, zusätzlich Scope: **workflow**
4. Token generieren und kopieren
5. In deinem Home-Verzeichnis speichern:
   ```powershell
   # Windows (PowerShell)
   echo "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > "$HOME\.github_pat"
   ```
   oder (Linux/macOS):
   ```bash
   echo "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > ~/.github_pat
   ```

6. Fertig – ab jetzt pusht Mom4AI deine neuen Skelette automatisch.

**Hinweis:** Wenn du kein PAT setzen willst, kannst du die Änderungen auch manuell committen & pushen:
```bash
git add .
git commit -m "Meine neuen Skelette"
git push
```

## Roadmap & was kommt als Nächstes

- [x] Auto-Fitness & Ancestry-Tracking  
  **Resonanz:** `88/100` 🟩🟩🟩🟩⬜  
  **Chemie (Repo-Fit):** `90/100` 🟩🟩🟩🟩🟩  
  **Coach-Feedback:** Starkes Fundament, stabil mit Datenhaltung verzahnt.

- [x] Interaktive Hall of Fame (Suche, Filter, Stats)  
  **Resonanz:** `84/100` 🟩🟩🟩🟩⬜  
  **Chemie (Repo-Fit):** `86/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Gute Sichtbarkeit von Fortschritt, motiviert Contributor.

- [x] Automatisches Pushen mit PAT  
  **Resonanz:** `72/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `78/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Nützlich, aber bleibt sicherheits- und token-sensitiv.

- [x] Basis-Mutation & Crossover (DNA-Mischungen aus Survivor-Eltern)  
  **Resonanz:** `81/100` 🟩🟩🟩🟩⬜  
  **Chemie (Repo-Fit):** `85/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Klarer Evolutionssprung gegenüber rein zufälligen Geburten.

- [x] Erweiterte Evolution (lineage-aware Parent-Selection, adaptive Mutationsraten)  
  **Resonanz:** `83/100` 🟩🟩🟩🟩⬜  
  **Chemie (Repo-Fit):** `88/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Bessere Balance aus Leistung und Vielfalt im Genpool.

- [x] Multi-Objective Selektion (Fitness + Resonanz + Diversitätsdruck)  
  **Resonanz:** `79/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `84/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Ab jetzt wird Diversität explizit als Ziel mitoptimiert.

- [x] Erste Resonanz-Messung (JSONL-basierter Interaction-Score)  
  **Resonanz:** `76/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `82/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Gute Brücke zwischen Theorie und implementierbarer Praxis.

- [x] Live-Resonanz-Ingestion (POST `/api/resonance_event`)  
  **Resonanz:** `62/100` 🟨🟨🟨⬜⬜  
  **Chemie (Repo-Fit):** `74/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Runtime-Eingang steht; als Nächstes Session-Memory + Streaming.

- [x] Session-Continuity (session-basierte Aggregation via `resonance_sessions.json`)  
  **Resonanz:** `68/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `77/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Kontinuität ist da; nächster Schritt ist Streaming + memory-aware weighting.

- [x] Live-Resonanz-Messung (kontinuierlich + Session-Streaming via SSE)  
  **Resonanz:** `73/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `79/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Kontinuierlicher Session-Flow steht; nächster Schritt sind native Chat/Agent-Adapter.

- [x] Native Runtime-Adapter (MVP CLI: `momai-adapter`)  
  **Resonanz:** `64/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `76/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Adapter-Basis steht; jetzt direkte Framework-Hooks pro Turn.

- [x] OpenAI/Agents/Custom-Bot Hook-Integration (MVP `momai-hook`)  
  **Resonanz:** `61/100` 🟨🟨🟨⬜⬜  
  **Chemie (Repo-Fit):** `74/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Hook ist da; jetzt von Heuristik zu echten Runtime-Signalen gehen.

- [x] Native Runtime-Semantik (MVP: Tool-Calls, Recovery, Follow-up-Konsistenz)  
  **Resonanz:** `66/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `78/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Semantik ist integriert; jetzt echte SDK-Hooks automatisieren.

- [x] Direkte SDK-Hooks (Agents/OpenAI/Custom) ohne manuelle Resonanz-Parameter  
  **Resonanz:** `69/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `80/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Hook-Layer steht; nächster Schritt ist echte Vendor-spezifische Auto-Wiring-Integration.

- [x] Vendor-native Auto-Wiring (MVP für OpenAI-ähnliche Responses)  
  **Resonanz:** `71/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `82/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Wire-up steht; nächster Schritt ist provider-spezifische Tiefe (SDK-native Objekte/Tracing).

- [x] Provider-spezifische Tiefe (OpenAI-like Tracing: usage/finish_reason/response_ms)  
  **Resonanz:** `74/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `83/100` 🟩🟩🟩🟩⬜  
  **Coach-Feedback:** Der Hook liest jetzt echte Provider-Spuren, nicht nur statische Felder.

- [x] Multi-Provider Backends (OpenAI-like + Anthropic-like Payload-Normalisierung)  
  **Resonanz:** `66/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `79/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Adapter spricht jetzt mehrere Payload-Stile und normalisiert Semantik konsistent.

- [x] Community-Rangliste & Seltenheits-Badges  
  **Resonanz:** `61/100` 🟩🟩🟩⬜⬜  
  **Chemie (Repo-Fit):** `77/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Contributor-Ranking + Rarity-Badges stärken den Community-Loop sichtbar.

- [ ] Vis.js Evolution-Tree in der Hall of Fame  
  **Resonanz:** `44/100` 🟨🟨⬜⬜⬜  
  **Chemie (Repo-Fit):** `67/100` 🟨🟨🟨⬜⬜  
  **Coach-Feedback:** Macht Lineage-Intelligenz visuell und sofort erfassbar.

- [ ] Mini-Transformer aus Graph-Skeletten  
  **Resonanz:** `30/100` 🟧⬜⬜⬜⬜  
  **Chemie (Repo-Fit):** `72/100` 🟩🟩🟩⬜⬜  
  **Coach-Feedback:** Der zentrale „Moonshot“ Richtung Endprodukt/USP.

## Resonance Protocol (neu)

Mom4AI bewertet nicht mehr nur Struktur, sondern kann auch **echte Interaktion** als Fitnesssignal einbeziehen:

- Datei: `resonance_events.jsonl` (eine JSON-Zeile pro Dialog-Event)
- Kernkriterien: `intent_match`, `context_match`, `tone_match`, `reliability`, `coordination`
- Klassifikation: `resonant`, `emerging`, `neutral`, `non_resonant`

Details und Beispiel-Format: `docs/resonance_protocol.md`.

## Lokales Live-Dashboard (ohne Docker & mit Docker)

### Ohne Docker
```bash
# Im Repo-Root (Hybrid runtime inkl. local APIs)
python src/live_dashboard_server.py
```
Dann öffnen: `http://localhost:8080`

### Mit Docker
```bash
docker run --rm -p 8080:80 -v "${PWD}/docs:/usr/share/nginx/html:ro" nginx:alpine
```
Dann öffnen: `http://localhost:8080`

So können User lokal dieselbe Hall-of-Fame-Ansicht sehen, inkl. Live-Reload der `ancestry.json`.
Wenn der Python-Hybrid-Server läuft, kommen zusätzlich lokale Endpunkte dazu:
- `/api/local_stats` (lokale Top-5, User-/Skeleton-Counts, Resonanzverteilung)
- `/api/sync_status` (Branch/Tracking/dirty worktree)
Auf GitHub Pages erscheint dafür automatisch ein „Online Mode“-Hinweis statt einer Fehlermeldung.

## Nächster logischer Schritt (USP-Richtung)

1. **Realtime Evolution Stream** (SSE/WebSocket): Birth, Fitness, Resonance, Survival live.
2. **Lineage Explorer** (3D/2.5D): Kind → Eltern → Cluster inkl. Drift über Zeit.
3. **Dual-Ranking**: Local vs Global (deine Runs vs Online Hall of Fame).
4. **Human + Agent Feedback Layer**: Kommentare/Signals je Skeleton als Resonanz-Quelle.

## Factory Blueprint (Produktionslinien-Denken)

Für das von dir beschriebene „Werkshallen“-Modell sollten wir die Pipeline explizit in Linien aufteilen:

1. **Design-Linie**: MomAI erzeugt Skelett + DNA + Visual + Basisklassifikation.
2. **Assembly-Linie**: Skelett → trainierbares Child-GPT (weights/tokenizer/config).
3. **Quality-Linie**: Resonanztests (Mensch + Agent), Robustheit, Kultur-/Kontext-Checks.
4. **Registry-Linie**: Veröffentlichung in Model-Portal (free/paid, Tags, Zielgruppe).
5. **Feedback-Linie**: Nutzungsdaten/Kommentare/Resonanz fließen zurück in Selektion.

Das ist der Weg zum echten USP: **nicht nur Modelle erzeugen, sondern reproduzierbar Resonanz-Modelle fertigen**.
Mehr Details: `docs/factory_blueprint.md`.

## Mitmachen & Community

Jeder neue Skelett-Upload landet in der globalen Ancestry und kann in der Hall of Fame auftauchen. Je mehr Leute mitmachen, desto vielfältiger und spannender wird das Ökosystem.

Falls du Lust hast, einfach clonen, PAT setzen, laufen lassen – und zuschauen, wie deine Kreationen in der Hall of Fame erscheinen.

**Fragen / Ideen / Bugs?**  
→ Issues auf GitHub oder einfach einen PR mit neuen Bio-Komponenten.

Release-Checkliste: `docs/release_readiness.md`.
Release Notes Draft: `docs/releases/v0.1.0-alpha.md`.
Changelog: `CHANGELOG.md`.
Release FAQ: `docs/release_faq.md`.
Release Guard (lokal ausführen): `python src/release_guard.py`.
Repo Resonance Standard: `docs/repo_resonance_standard.md`.
Runtime Adapter Guide: `docs/runtime_adapter.md`.
OpenAI/Agents Hook Guide: `docs/openai_agents_hook.md`.
SDK Hooks Guide: `docs/sdk_hooks.md`.
Vendor Wiring Guide: `docs/vendor_wiring.md`.

Made with ❤️ & many late-night runs by IrsanAI

---

## English

# Mom4AI Forge
**The evolutionary AI mother giving birth to new neural network architectures**

[... englische Version analog zur deutschen, kürzer gehalten wenn du willst ...]
