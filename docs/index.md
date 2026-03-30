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

<div id="hall-stats" style="text-align:center; margin:1em; color:#0f0;">
  <h2>Live Evolution – Mom's Ancestry</h2>
  <p id="stats-total">Gesamt Skelette: <span id="total-count">...</span> • User: <span id="user-count">...</span> • Seltenste: <span id="rare-count">...</span>× geboren</p>
  <p id="stats-resonance">Resonant: <span id="resonant-count">...</span> • Emerging: <span id="emerging-count">...</span> • Non-resonant: <span id="non-resonant-count">...</span></p>
</div>

<div style="margin:1em; text-align:center;">
  <input type="text" id="search" placeholder="Suche nach Name, User oder Dominant..." style="padding:8px; width:300px; background:#111; color:#0f0; border:1px solid #0f0;">
  <select id="sort" style="padding:8px; background:#111; color:#0f0; border:1px solid #0f0;">
    <option value="fitness-desc">Fitness ↓</option>
    <option value="fitness-asc">Fitness ↑</option>
    <option value="born-desc">Born count ↓</option>
    <option value="born-asc">Born count ↑</option>
  </select>
  <button onclick="loadHall()" style="padding:8px 16px; background:#0f0; color:#000; border:none; cursor:pointer;">Aktualisieren</button>
</div>

<div id="top-5" style="margin: 1.5em 0;">
  <h3 style="color:#0f0; text-align:center;">Top 5 Gesamt (Online Snapshot)</h3>
  <ol id="top-5-list" style="max-width: 780px; margin: 0 auto; color:#0f0; background:#111; border:1px solid #0f0; border-radius:8px; padding:16px 24px;"></ol>
</div>

<div id="local-runtime" style="margin:1.5em auto; max-width:780px; color:#0f0; background:#111; border:1px solid #0f0; border-radius:8px; padding:16px;">
  <h3 style="margin-top:0;">Local Runtime / Sync Monitor</h3>
  <p id="local-runtime-stats">Warte auf lokalen Server...</p>
  <p id="local-runtime-git">Git Sync: -</p>
  <p id="local-runtime-session">Session: -</p>
  <p id="local-runtime-stream">Stream: -</p>
</div>

<script>
let allSkeletons = [];

async function loadHall() {
  try {
    const resp = await fetch('ancestry.json');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    allSkeletons = await resp.json();
    
    // Stats oben
    document.getElementById('total-count').textContent = allSkeletons.length;
    const users = new Set(allSkeletons.map(s => s.produced_by || 'unbekannt'));
    document.getElementById('user-count').textContent = users.size;
    const minBorn = Math.min(...allSkeletons.map(s => s.born_count || 1));
    document.getElementById('rare-count').textContent = minBorn;
    const resonant = allSkeletons.filter(s => s.resonance_classification === 'resonant').length;
    const emerging = allSkeletons.filter(s => s.resonance_classification === 'emerging').length;
    const nonResonant = allSkeletons.filter(s => s.resonance_classification === 'non_resonant').length;
    document.getElementById('resonant-count').textContent = resonant;
    document.getElementById('emerging-count').textContent = emerging;
    document.getElementById('non-resonant-count').textContent = nonResonant;

    renderSkeletons(allSkeletons);
    renderTop5(allSkeletons);
  } catch (err) {
    document.getElementById('hall-of-fame').innerHTML = '<p style="color:red;">Fehler: ' + err.message + '</p>';
  }
}

async function loadLocalRuntime() {
  const isLocalHost = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  if (!isLocalHost) {
    document.getElementById('local-runtime-stats').textContent =
      'Online Mode aktiv (GitHub Pages). Lokale Runtime-API ist hier bewusst deaktiviert.';
    document.getElementById('local-runtime-git').textContent =
      'Für Local Runtime/Sync: python src/live_dashboard_server.py und dann http://localhost:8080 öffnen.';
    return;
  }

  try {
    const [statsResp, syncResp, sessionResp] = await Promise.all([
      fetch('/api/local_stats'),
      fetch('/api/sync_status'),
      fetch('/api/session_summary')
    ]);
    if (!statsResp.ok || !syncResp.ok || !sessionResp.ok) throw new Error('local api unavailable');

    const stats = await statsResp.json();
    const sync = await syncResp.json();
    const sessions = await sessionResp.json();
    document.getElementById('local-runtime-stats').textContent =
      `Local skeletons: ${stats.total_skeletons} | Local users: ${stats.total_users} | Local top1: ${stats.top5?.[0]?.name || 'n/a'}`;
    document.getElementById('local-runtime-git').textContent =
      `Git Sync: branch=${sync.branch || 'n/a'} | dirty=${sync.dirty_worktree ? 'yes' : 'no'} | tracking=${sync.tracking || 'n/a'}`;
    const list = Array.isArray(sessions.sessions) ? sessions.sessions : [];
    const bestSession = list.sort((a,b) => (b.session_resonance || 0) - (a.session_resonance || 0))[0];
    document.getElementById('local-runtime-session').textContent =
      bestSession
        ? `Best Session: ${bestSession.session_id} | Resonance ${(bestSession.session_resonance || 0).toFixed(3)} | Events ${bestSession.event_count || 0}`
        : 'Session: noch keine Live-Events.';
  } catch (_err) {
    document.getElementById('local-runtime-stats').textContent =
      'Lokaler Runtime-Server nicht verbunden. Starte: python src/live_dashboard_server.py';
    document.getElementById('local-runtime-git').textContent =
      'Tipp: lokale API-Endpunkte (/api/local_stats, /api/sync_status) sind nur lokal verfügbar.';
    document.getElementById('local-runtime-session').textContent =
      'Session-Summary benötigt den lokalen Runtime-Server.';
  }
}

function connectSessionStream() {
  const isLocalHost = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  if (!isLocalHost || !window.EventSource) {
    document.getElementById('local-runtime-stream').textContent = 'Stream: im Online Mode deaktiviert.';
    return;
  }

  const stream = new EventSource('/api/session_stream');
  stream.addEventListener('session', (evt) => {
    try {
      const data = JSON.parse(evt.data);
      if (data?.top_session) {
        document.getElementById('local-runtime-stream').textContent =
          `Stream Top: ${data.top_session.session_id} | Resonance ${(data.top_session.session_resonance || 0).toFixed(3)} | Sessions ${data.session_count}`;
      } else {
        document.getElementById('local-runtime-stream').textContent =
          `Stream aktiv | Sessions ${data.session_count || 0}`;
      }
    } catch (_e) {
      document.getElementById('local-runtime-stream').textContent = 'Stream aktiv (decode fallback).';
    }
  });
  stream.onerror = () => {
    document.getElementById('local-runtime-stream').textContent = 'Stream getrennt – reconnect läuft...';
  };
}

function badgeForResonance(cls) {
  if (cls === 'resonant') return '<span style="color:#00ff99;font-weight:bold;">resonant</span>';
  if (cls === 'emerging') return '<span style="color:#7CFC00;font-weight:bold;">emerging</span>';
  if (cls === 'non_resonant') return '<span style="color:#ff5a5a;font-weight:bold;">non_resonant</span>';
  if (cls === 'neutral') return '<span style="color:#ffd166;font-weight:bold;">neutral</span>';
  return '<span style="color:#9e9e9e;font-weight:bold;">no_data</span>';
}

function renderTop5(data) {
  const top5 = [...data]
    .sort((a,b) => (b.fitness || 0) - (a.fitness || 0))
    .slice(0, 5);

  const list = document.getElementById('top-5-list');
  list.innerHTML = '';
  top5.forEach((s, idx) => {
    const li = document.createElement('li');
    li.style.margin = '6px 0';
    li.innerHTML = `<strong>#${idx + 1}</strong> ${s.name} — Fitness ${(s.fitness || 0).toFixed(3)} — ${badgeForResonance(s.resonance_classification)}`;
    list.appendChild(li);
  });
}

function renderSkeletons(data) {
  const container = document.getElementById('hall-of-fame');
  container.innerHTML = '';

  const sortVal = document.getElementById('sort').value;
  const search = document.getElementById('search').value.toLowerCase();

  let filtered = data.filter(s => {
    if (!search) return true;
    return (
      s.name.toLowerCase().includes(search) ||
      (s.produced_by || '').toLowerCase().includes(search) ||
      (s.facts?.dominant_type || '').toLowerCase().includes(search)
    );
  });

  if (sortVal === 'fitness-desc') filtered.sort((a,b) => b.fitness - a.fitness);
  if (sortVal === 'fitness-asc')  filtered.sort((a,b) => a.fitness - b.fitness);
  if (sortVal === 'born-desc')    filtered.sort((a,b) => (b.born_count||1) - (a.born_count||1));
  if (sortVal === 'born-asc')     filtered.sort((a,b) => (a.born_count||1) - (b.born_count||1));

  const top = filtered.slice(0, 20); // erstmal 20 statt 10 – skalierbar

  top.forEach(s => {
    const div = document.createElement('div');
    div.style.background = '#111';
    div.style.padding = '12px';
    div.style.border = '1px solid #0f0';
    div.style.borderRadius = '8px';
    div.innerHTML = `
      <img src="images/${s.name}.png" width="280" style="border-radius:8px;" onerror="this.src='https://via.placeholder.com/280x280/111/0f0?text=${s.name.slice(0,10)}';">
      <h3 style="margin:8px 0;">${s.name}</h3>
      <p><strong>Produced by:</strong> ${s.produced_by || 'unbekannt'}</p>
      <p><strong>Fitness:</strong> ${s.fitness.toFixed(3)}</p>
      <p><strong>Resonance:</strong> ${badgeForResonance(s.resonance_classification)}</p>
      <p><strong>Interactions:</strong> ${s.resonance_interactions || 0}</p>
      <p><strong>Born count:</strong> <strong style="color:#0f0;">${s.born_count || 1}x</strong></p>
      <p><strong>Dominant:</strong> ${s.facts?.dominant_type || 'N/A'}</p>
    `;
    container.appendChild(div);
  });
}

// Auto-Refresh alle 30 Sekunden + initial laden
setInterval(loadHall, 30000);
setInterval(loadLocalRuntime, 8000);
loadHall();
loadLocalRuntime();
connectSessionStream();

// Suche & Sort live reagieren
document.getElementById('search').addEventListener('input', () => renderSkeletons(allSkeletons));
document.getElementById('sort').addEventListener('change', () => renderSkeletons(allSkeletons));
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
