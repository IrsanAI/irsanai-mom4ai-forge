---
layout: default
title: Mom4AI Forge
---

<div style="text-align: center; margin: 2em 0;">
  <h1 style="color: #0f0; font-family: 'Courier New', monospace;">Mom4AI Forge</h1>
  <p style="font-size: 1.3em; color: #0f0;">Die evolutive KI-Mutter, die neue neuronale Netze gebiert.</p>
</div>

<p align="center">
  <a href="https://irsanai.github.io/irsanai-mom4ai-forge/">
    <img src="https://img.shields.io/badge/Live%20Demo-live-00ff00?style=for-the-badge&logo=githubpages&logoColor=white" alt="Live Demo">
  </a>
</p>

## Vision

Eine KI, die **nicht kopiert** – sondern **neu erfindet**.  
Aus Myzel-Netzen, Ameisen-Schwärmen, Oktopus-Nervensystemen, Korallenriffen & Vogelzügen entstehen Graph-Skelette.  
Nur die mit starker Auto-Fitness (Dichte, Modularität, Feedback-Loops) überleben.

## Hall of Fame – Moms Ancestry (Top 10)

Hier die aktuell besten 10 Skelette (sortiert nach Fitness – aktualisiert bei jedem Push):

<div id="hall-of-fame" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 2em 0;"></div>

<script>
console.log('Versuche ancestry.json zu laden...');
fetch('ancestry.json')
  .then(response => {
    console.log('Status:', response.status);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.text();  // erst als Text laden
  })
  .then(text => {
    console.log('Roh-Text:', text.substring(0, 200));  // ersten 200 Zeichen loggen
    if (!text.trim()) throw new Error('Datei ist leer');
    return JSON.parse(text);
  })
  .then(data => {
    console.log('Daten geladen – Anzahl:', data.length);
    const top10 = data.sort((a, b) => b.fitness - a.fitness).slice(0, 10);
    const container = document.getElementById('hall-of-fame');
    container.innerHTML = '';
    if (top10.length === 0) {
      container.innerHTML = '<p>Noch keine Skelette in Top 10.</p>';
      return;
    }
    top10.forEach(s => {
      const div = document.createElement('div');
      div.style.textAlign = 'center';
      div.innerHTML = `
        <img src="images/${s.name}.png" width="280" style="border-radius: 8px; border: 2px solid #0f0;" onerror="this.src='https://via.placeholder.com/280?text=No+Image';">
        <h3>${s.name}</h3>
        <p><strong>Produced by:</strong> ${s.produced_by || 'unbekannt'}</p>
        <p><strong>Fitness:</strong> ${s.fitness ? s.fitness.toFixed(3) : 'N/A'}</p>
        <p><strong>Born count:</strong> ${s.born_count || 1}x</p>
        <small>Dominant: ${s.facts?.dominant_type || 'N/A'}</small>
      `;
      container.appendChild(div);
    });
  })
  .catch(err => {
    console.error('Ladefehler:', err);
    document.getElementById('hall-of-fame').innerHTML = '<p>Fehler beim Laden der Hall of Fame: ' + err.message + '</p>';
  });
</script>

<small>Mehr Details in <a href="ancestry.json">ancestry.json</a> – bald interaktive Filter & Suche!</small>

## Wie es funktioniert

1. Mom mischt Bio-DNA (0–100 %)
2. Erzeugt Graph-Skelett (Knoten = Layer-Typen, Kanten = Verbindungen)
3. Bewertet automatisch (Fitness-Score)
4. Überlebende werden gespeichert & können mutiert werden

## Aktueller Stand & Roadmap

- Graph-Generierung mit networkx
- Auto-Fitness (Dichte, Modularity, Feedback)
- Speichern/Laden & PNG-Visuals
- User-Registrierung (unique Namen)
- DNA-Hash + born_count-Tracking

- Mutation & Crossover von Skeletten
- Aus Graph → echtes Mini-Transformer-Chat-Modell
- Echte User-Resonance durch Chatten
- Skalierung auf Server

Made with ❤️ by [IrsanAI](https://github.com/IrsanAI)  
[Live Demo](https://irsanai.github.io/irsanai-mom4ai-forge/) • [Repo](https://github.com/IrsanAI/irsanai-mom4ai-forge) • [X/Twitter] • [Discord?]
