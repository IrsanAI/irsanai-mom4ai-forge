```markdown
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

3. Ersten Run starten
```bash
python src/mom_forge.py
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
3. Wähle Scope: **repo** (full control of private repositories)
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
- [x] Interaktive Hall of Fame (Suche, Filter, Stats)
- [x] Automatisches Pushen mit PAT
- [ ] Mutation & Crossover (Skelette paaren)
- [x] Erste Resonanz-Messung (JSONL-basierter Interaction-Score)
- [ ] Live-Resonanz-Messung direkt aus Chat/Agent-Runtime
- [ ] Community-Rangliste & Seltenheits-Badges
- [ ] Vis.js Evolution-Tree in der Hall of Fame
- [ ] Mini-Transformer aus Graph-Skeletten

## Resonance Protocol (neu)

Mom4AI bewertet nicht mehr nur Struktur, sondern kann auch **echte Interaktion** als Fitnesssignal einbeziehen:

- Datei: `resonance_events.jsonl` (eine JSON-Zeile pro Dialog-Event)
- Kernkriterien: `intent_match`, `context_match`, `tone_match`, `reliability`, `coordination`
- Klassifikation: `resonant`, `emerging`, `neutral`, `non_resonant`

Details und Beispiel-Format: `docs/resonance_protocol.md`.

## Mitmachen & Community

Jeder neue Skelett-Upload landet in der globalen Ancestry und kann in der Hall of Fame auftauchen. Je mehr Leute mitmachen, desto vielfältiger und spannender wird das Ökosystem.

Falls du Lust hast, einfach clonen, PAT setzen, laufen lassen – und zuschauen, wie deine Kreationen in der Hall of Fame erscheinen.

**Fragen / Ideen / Bugs?**  
→ Issues auf GitHub oder einfach einen PR mit neuen Bio-Komponenten.

Made with ❤️ & many late-night runs by IrsanAI

---

## English

# Mom4AI Forge
**The evolutionary AI mother giving birth to new neural network architectures**

[... englische Version analog zur deutschen, kürzer gehalten wenn du willst ...]

```
