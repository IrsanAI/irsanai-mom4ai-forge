---
layout: default
title: Mom4AI Forge
---

<style>
:root {
  --bg: #05080d;
  --panel: #0e1420;
  --panel-2: #101a28;
  --text: #d8ffe8;
  --muted: #8fc9ad;
  --accent: #35f2a1;
  --accent-2: #59a8ff;
  --danger: #ff6b8a;
}

body {
  background: radial-gradient(circle at 10% 10%, #0a1c1f 0%, var(--bg) 35%), var(--bg);
  color: var(--text);
}

.forge-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1rem 3rem;
}

.hero {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 1rem;
  align-items: stretch;
  margin: 1rem 0 1.4rem;
}

.hero-card,
.panel {
  background: linear-gradient(160deg, rgba(20, 40, 59, 0.95), rgba(9, 17, 28, 0.98));
  border: 1px solid rgba(83, 241, 176, 0.28);
  border-radius: 14px;
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.35);
}

.hero-card {
  padding: 1rem;
}

.hero-card h1 {
  margin: 0 0 0.4rem;
  font-size: clamp(1.6rem, 2.7vw, 2.4rem);
}

.hero-card p {
  color: var(--muted);
  margin: 0.3rem 0;
}

.hero-img {
  width: 100%;
  border-radius: 10px;
  border: 1px solid rgba(89, 168, 255, 0.5);
}

.cta-box {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.cta-button {
  margin-top: 0.8rem;
  display: inline-block;
  text-decoration: none;
  color: #031016;
  background: linear-gradient(90deg, var(--accent), #7effc4);
  font-weight: 700;
  border-radius: 9px;
  padding: 0.6rem 0.85rem;
}

.stats-grid {
  margin: 1rem 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.7rem;
}

.stat-tile {
  background: var(--panel-2);
  border: 1px solid rgba(83, 241, 176, 0.2);
  border-radius: 10px;
  padding: 0.8rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin: 0.6rem 0 1rem;
}

.controls input,
.controls select,
.controls button {
  background: #0b121d;
  color: var(--text);
  border: 1px solid rgba(83, 241, 176, 0.35);
  border-radius: 8px;
  padding: 0.5rem 0.65rem;
}

.controls button {
  cursor: pointer;
}

.hall-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}

.skeleton-card {
  background: linear-gradient(180deg, #101825, #0a111b);
  border: 1px solid rgba(83, 241, 176, 0.2);
  border-radius: 12px;
  padding: 0.7rem;
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.skeleton-card:hover {
  transform: translateY(-4px);
  border-color: rgba(83, 241, 176, 0.55);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.skeleton-card img {
  width: 100%;
  border-radius: 8px;
  border: 1px solid rgba(89, 168, 255, 0.3);
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
  margin: 1.2rem 0;
}

.meta-grid ul {
  margin: 0.4rem 0 0;
  padding-left: 1.2rem;
}

.tree-panel {
  margin: 1rem 0;
}

#evolution-tree {
  width: 100%;
  height: 420px;
  border-radius: 10px;
  border: 1px solid rgba(83, 241, 176, 0.25);
  background: radial-gradient(circle at 30% 10%, #122338 0%, #0b121d 60%);
}

small,
.muted {
  color: var(--muted);
}

.modal-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(2, 8, 12, 0.8);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}

.modal {
  width: min(740px, 96vw);
  max-height: 88vh;
  overflow: auto;
  background: #0c1320;
  border: 1px solid rgba(83, 241, 176, 0.35);
  border-radius: 12px;
  padding: 1rem;
}

.badge { font-weight: 700; }
.badge.resonant { color: #57ffba; }
.badge.emerging { color: #befd6f; }
.badge.neutral { color: #ffd166; }
.badge.non_resonant { color: #ff7b7b; }
.badge.no_data { color: #98a6aa; }

.rarity-badge {
  display: inline-block;
  padding: 0.18rem 0.48rem;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  margin-left: 0.4rem;
}

.rarity-legend {
  margin: 0.45rem 0 0;
  font-size: 0.82rem;
  color: var(--muted);
}

@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; }
}
</style>

<div class="forge-shell">
  <div class="hero">
    <section class="hero-card">
      <h1>Mom4AI Forge — Live Evolution Lab</h1>
      <p>Keine statische Modell-Liste, sondern ein lebendiges Ökosystem aus bio-inspirierten Netz-Skeletten mit kontinuierlicher Selektion.</p>
      <p class="muted">Die Grafik zeigt den Kern-Claim: klassisches Feedforward-Netz vs. evolutive MomAI-Topologie.</p>
      <img class="hero-img" src="images/momai-forge-vs-typical-nn.jpg" alt="Typisches NN vs MomAI Forge Topologie">
    </section>

    <aside class="hero-card cta-box">
      <div>
        <h2 style="margin-top:0;">Join the Forge</h2>
        <p>Generiere eigene Skelette, pushe sie ins Repo und sieh zu, wie sie in der Hall of Fame auftauchen.</p>
        <p class="muted">Online läuft die öffentliche Hall of Fame. Für Runtime-APIs/Sessions lokal starten:</p>
        <code>python src/live_dashboard_server.py</code>
      </div>
      <a class="cta-button" href="https://github.com/IrsanAI/irsanai-mom4ai-forge">Mitbauen auf GitHub</a>
    </aside>
  </div>

  <section class="panel" style="padding:0.9rem;">
    <h2 style="margin:0.2rem 0 0.6rem;">Live Evolution – Hall of Fame</h2>
    <div class="stats-grid" id="stats-grid">
      <div class="stat-tile"><div class="muted">Gesamt Skelette</div><div id="total-count" class="stat-value">…</div></div>
      <div class="stat-tile"><div class="muted">Contributor</div><div id="user-count" class="stat-value">…</div></div>
      <div class="stat-tile"><div class="muted">Resonant</div><div id="resonant-count" class="stat-value">…</div></div>
      <div class="stat-tile"><div class="muted">Emerging</div><div id="emerging-count" class="stat-value">…</div></div>
      <div class="stat-tile"><div class="muted">Non-resonant</div><div id="non-resonant-count" class="stat-value">…</div></div>
      <div class="stat-tile"><div class="muted">Seltenste Geburt</div><div id="rare-count" class="stat-value">…</div></div>
    </div>

    <div class="controls">
      <input type="text" id="search" placeholder="Suche Name, User, Dominant Type…">
      <select id="sort">
        <option value="fitness-desc">Fitness ↓</option>
        <option value="fitness-asc">Fitness ↑</option>
        <option value="born-desc">Born count ↓</option>
        <option value="born-asc">Born count ↑</option>
      </select>
      <button id="refresh-btn">Aktualisieren</button>
    </div>

    <div class="hall-grid" id="hall-of-fame"></div>
  </section>

  <section class="meta-grid">
    <article class="panel" style="padding:0.9rem;">
      <h3 style="margin:0;">Top 5 Gesamt (Fitness)</h3>
      <ol id="top-5-list"></ol>
    </article>
    <article class="panel" style="padding:0.9rem;">
      <h3 style="margin:0;">Seltenste Skelette (born_count ≤ 1)</h3>
      <ul id="rare-list"></ul>
    </article>
    <article class="panel" style="padding:0.9rem;">
      <h3 style="margin:0;">Top Contributor Ranking</h3>
      <ul id="contributors-list"></ul>
      <p class="rarity-legend">🏆 Legendär = Top1 • 🥈 Aufstrebend = Top2/3 • 🌱 Newcomer = alle weiteren</p>
    </article>
    <article class="panel" style="padding:0.9rem;">
      <h3 style="margin:0;">Dominante Bio-Typen</h3>
      <ul id="dominant-list"></ul>
    </article>
  </section>

  <section class="panel tree-panel" style="padding:0.9rem;">
    <h3 style="margin-top:0;">Vis.js Evolution-Tree (Hall of Fame)</h3>
    <p class="muted" style="margin-top:0;">
      Visualisiert die Evolution der Top-Skelette als interaktiven Graphen.
      Linien verbinden einen Eintrag mit einem plausiblen Vorgänger (gleicher Contributor, niedrigere Generation) als Lineage-Proxy.
    </p>
    <div id="evolution-tree"></div>
  </section>

  <section class="panel" style="padding:0.9rem; margin-top:0.4rem;">
    <h3 style="margin-top:0;">Local Runtime / Sync Monitor</h3>
    <p id="local-runtime-stats">Warte auf lokalen Server…</p>
    <p id="local-runtime-git">Git Sync: -</p>
    <p id="local-runtime-session">Session: -</p>
    <p id="local-runtime-stream">Stream: -</p>
  </section>

  <p style="margin-top:1rem;"><small>Hinweis: Auf GitHub Pages ist nur der Online-Modus aktiv; lokale Runtime-APIs sind absichtlich deaktiviert.</small></p>
</div>

<div class="modal-backdrop" id="detail-backdrop">
  <div class="modal">
    <button id="close-modal" style="float:right;">Schließen</button>
    <h3 id="detail-title">Skeleton Detail</h3>
    <pre id="detail-json" style="white-space:pre-wrap; font-size:0.86rem;"></pre>
  </div>
</div>

<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script>
let allSkeletons = [];
let evolutionNetwork = null;

function badgeForResonance(cls) {
  const safe = cls || 'no_data';
  return `<span class="badge ${safe}">${safe}</span>`;
}

function rarityBadgeForBornCount(bornCount) {
  const born = bornCount || 1;
  if (born <= 1) return '<span class="rarity-badge" style="background:#7b2cff22; color:#c8a6ff; border:1px solid #a46eff55;">🦄 Mythic (1x)</span>';
  if (born <= 2) return '<span class="rarity-badge" style="background:#3a6aff22; color:#9dc8ff; border:1px solid #7fa9ff55;">💎 Rare (2x)</span>';
  if (born <= 4) return '<span class="rarity-badge" style="background:#2e9f6a22; color:#9ff7c7; border:1px solid #7de2b055;">✨ Uncommon (3-4x)</span>';
  return '<span class="rarity-badge" style="background:#6a7a8822; color:#c5d1da; border:1px solid #a8bac955;">📦 Common (5x+)</span>';
}

function number(v, digits = 3) {
  if (typeof v !== 'number' || Number.isNaN(v)) return 'n/a';
  return v.toFixed(digits);
}

function aggregateBy(arr, fn) {
  const map = new Map();
  arr.forEach((item) => {
    const key = fn(item) || 'unknown';
    map.set(key, (map.get(key) || 0) + 1);
  });
  return [...map.entries()].sort((a, b) => b[1] - a[1]);
}

function updateStats(data) {
  document.getElementById('total-count').textContent = data.length;
  const users = new Set(data.map(s => s.produced_by || 'unbekannt'));
  document.getElementById('user-count').textContent = users.size;
  const minBorn = data.length ? Math.min(...data.map(s => s.born_count || 1)) : 0;
  document.getElementById('rare-count').textContent = `${minBorn}x`;

  const resonant = data.filter(s => s.resonance_classification === 'resonant').length;
  const emerging = data.filter(s => s.resonance_classification === 'emerging').length;
  const nonResonant = data.filter(s => s.resonance_classification === 'non_resonant').length;

  document.getElementById('resonant-count').textContent = resonant;
  document.getElementById('emerging-count').textContent = emerging;
  document.getElementById('non-resonant-count').textContent = nonResonant;
}

function renderTop5(data) {
  const top5 = [...data].sort((a,b) => (b.fitness || 0) - (a.fitness || 0)).slice(0, 5);
  const list = document.getElementById('top-5-list');
  list.innerHTML = '';
  top5.forEach((s, idx) => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>#${idx + 1}</strong> ${s.name} — Fitness ${number(s.fitness)} — ${badgeForResonance(s.resonance_classification)}`;
    list.appendChild(li);
  });
}

function renderRare(data) {
  const rare = data.filter(s => (s.born_count || 1) <= 1).slice(0, 8);
  const list = document.getElementById('rare-list');
  list.innerHTML = '';
  if (!rare.length) {
    list.innerHTML = '<li>Keine seltenen Einträge gefunden.</li>';
    return;
  }
  rare.forEach((s) => {
    const li = document.createElement('li');
    li.textContent = `${s.name} (${s.produced_by || 'unbekannt'})`;
    list.appendChild(li);
  });
}

function renderContributors(data) {
  const ranking = aggregateBy(data, s => s.produced_by || 'unbekannt').slice(0, 8);
  const list = document.getElementById('contributors-list');
  list.innerHTML = '';
  ranking.forEach(([name, count], idx) => {
    const li = document.createElement('li');
    let tier = '🌱 Newcomer';
    if (idx === 0) tier = '🏆 Legendär';
    else if (idx <= 2) tier = '🥈 Aufstrebend';
    li.textContent = `#${idx + 1} ${name}: ${count} skeletons (${tier})`;
    list.appendChild(li);
  });
}

function renderDominants(data) {
  const ranking = aggregateBy(data, s => s.facts?.dominant_type || 'n/a').slice(0, 8);
  const list = document.getElementById('dominant-list');
  list.innerHTML = '';
  ranking.forEach(([dominant, count]) => {
    const li = document.createElement('li');
    li.textContent = `${dominant}: ${count}`;
    list.appendChild(li);
  });
}

function renderSkeletons(data) {
  const container = document.getElementById('hall-of-fame');
  container.innerHTML = '';

  const sortVal = document.getElementById('sort').value;
  const search = document.getElementById('search').value.toLowerCase();

  let filtered = data.filter((s) => {
    if (!search) return true;
    return (
      (s.name || '').toLowerCase().includes(search) ||
      (s.produced_by || '').toLowerCase().includes(search) ||
      (s.facts?.dominant_type || '').toLowerCase().includes(search)
    );
  });

  if (sortVal === 'fitness-desc') filtered.sort((a,b) => (b.fitness || 0) - (a.fitness || 0));
  if (sortVal === 'fitness-asc') filtered.sort((a,b) => (a.fitness || 0) - (b.fitness || 0));
  if (sortVal === 'born-desc') filtered.sort((a,b) => (b.born_count || 1) - (a.born_count || 1));
  if (sortVal === 'born-asc') filtered.sort((a,b) => (a.born_count || 1) - (b.born_count || 1));

  filtered.slice(0, 24).forEach((s) => {
    const div = document.createElement('article');
    div.className = 'skeleton-card';
    const fallback = encodeURIComponent((s.name || 'skeleton').slice(0, 12));
    div.innerHTML = `
      <img src="images/${s.name}.png" alt="${s.name}" onerror="this.src='https://via.placeholder.com/560x330/0f1720/57ffba?text=${fallback}'">
      <h4>${s.name}</h4>
      <p><strong>Produced by:</strong> ${s.produced_by || 'unbekannt'}</p>
      <p><strong>Fitness:</strong> ${number(s.fitness)}</p>
      <p><strong>Resonance:</strong> ${badgeForResonance(s.resonance_classification)}</p>
      <p><strong>Born count:</strong> ${s.born_count || 1}x ${rarityBadgeForBornCount(s.born_count)}</p>
      <p><strong>Dominant:</strong> ${s.facts?.dominant_type || 'N/A'}</p>
      <button class="details-btn">Details</button>
    `;
    div.querySelector('.details-btn').addEventListener('click', () => openDetails(s));
    container.appendChild(div);
  });
}

function buildEvolutionTree(data) {
  const container = document.getElementById('evolution-tree');
  if (!container || !window.vis) return;

  const selected = [...data]
    .sort((a, b) => (b.fitness || 0) - (a.fitness || 0))
    .slice(0, 50);

  const nodes = selected.map((s) => ({
    id: s.id || s.name,
    label: `${s.name}`.slice(0, 28),
    title: `${s.name}\nFitness: ${number(s.fitness)}\nGen: ${number(s.generation, 2)}\nUser: ${s.produced_by || 'n/a'}`,
    shape: 'dot',
    size: 10 + Math.min(18, Math.max(0, (s.fitness || 0) * 35)),
    color: s.resonance_classification === 'resonant' ? '#57ffba'
      : s.resonance_classification === 'emerging' ? '#c1ff74'
      : s.resonance_classification === 'non_resonant' ? '#ff7b7b'
      : '#9fb4c7',
  }));

  const byUser = new Map();
  selected.forEach((s) => {
    const key = s.produced_by || 'unbekannt';
    const arr = byUser.get(key) || [];
    arr.push(s);
    byUser.set(key, arr);
  });
  byUser.forEach((arr) => arr.sort((a, b) => (a.generation || 0) - (b.generation || 0)));

  const edges = [];
  selected.forEach((s) => {
    const group = byUser.get(s.produced_by || 'unbekannt') || [];
    const idx = group.findIndex((x) => (x.id || x.name) === (s.id || s.name));
    if (idx > 0) {
      const parent = group[idx - 1];
      edges.push({
        from: parent.id || parent.name,
        to: s.id || s.name,
        color: { color: 'rgba(123, 167, 215, 0.45)' },
        arrows: 'to'
      });
    }
  });

  const networkData = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
  const options = {
    physics: { stabilization: true, barnesHut: { springLength: 90 } },
    interaction: { hover: true, tooltipDelay: 100 },
    nodes: { font: { color: '#d6fce8', size: 12 } },
    edges: { smooth: { type: 'dynamic' } },
  };

  if (evolutionNetwork) {
    evolutionNetwork.destroy();
  }
  evolutionNetwork = new vis.Network(container, networkData, options);
}

async function loadHall() {
  try {
    const resp = await fetch('ancestry.json');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    allSkeletons = await resp.json();

    updateStats(allSkeletons);
    renderTop5(allSkeletons);
    renderRare(allSkeletons);
    renderContributors(allSkeletons);
    renderDominants(allSkeletons);
    renderSkeletons(allSkeletons);
    buildEvolutionTree(allSkeletons);
  } catch (err) {
    document.getElementById('hall-of-fame').innerHTML = `<p style="color:#ff7b7b;">Fehler: ${err.message}</p>`;
  }
}

async function loadLocalRuntime() {
  const isLocalHost = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  if (!isLocalHost) {
    document.getElementById('local-runtime-stats').textContent = 'Online Mode aktiv (GitHub Pages). Lokale Runtime-API ist hier bewusst deaktiviert.';
    document.getElementById('local-runtime-git').textContent = 'Für Local Runtime/Sync: python src/live_dashboard_server.py und dann http://localhost:8080 öffnen.';
    document.getElementById('local-runtime-session').textContent = 'Session: Online Snapshot ohne lokale Session-Daten.';
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
    const list = Array.isArray(sessions.sessions) ? sessions.sessions : [];
    const bestSession = list.sort((a,b) => (b.session_resonance || 0) - (a.session_resonance || 0))[0];

    document.getElementById('local-runtime-stats').textContent = `Local skeletons: ${stats.total_skeletons} | Local users: ${stats.total_users} | Local top1: ${stats.top5?.[0]?.name || 'n/a'}`;
    document.getElementById('local-runtime-git').textContent = `Git Sync: branch=${sync.branch || 'n/a'} | dirty=${sync.dirty_worktree ? 'yes' : 'no'} | tracking=${sync.tracking || 'n/a'}`;
    document.getElementById('local-runtime-session').textContent = bestSession
      ? `Best Session: ${bestSession.session_id} | Resonance ${(bestSession.session_resonance || 0).toFixed(3)} | Events ${bestSession.event_count || 0}`
      : 'Session: noch keine Live-Events.';
  } catch (_err) {
    document.getElementById('local-runtime-stats').textContent = 'Lokaler Runtime-Server nicht verbunden. Starte: python src/live_dashboard_server.py';
    document.getElementById('local-runtime-git').textContent = 'Tipp: lokale API-Endpunkte sind nur lokal verfügbar.';
    document.getElementById('local-runtime-session').textContent = 'Session-Summary benötigt den lokalen Runtime-Server.';
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
        document.getElementById('local-runtime-stream').textContent = `Stream aktiv | Sessions ${data.session_count || 0}`;
      }
    } catch (_e) {
      document.getElementById('local-runtime-stream').textContent = 'Stream aktiv (decode fallback).';
    }
  });
  stream.onerror = () => {
    document.getElementById('local-runtime-stream').textContent = 'Stream getrennt – reconnect läuft...';
  };
}

function openDetails(item) {
  document.getElementById('detail-title').textContent = item.name || 'Skeleton Detail';
  document.getElementById('detail-json').textContent = JSON.stringify(item, null, 2);
  document.getElementById('detail-backdrop').style.display = 'flex';
}

function closeDetails() {
  document.getElementById('detail-backdrop').style.display = 'none';
}

document.getElementById('search').addEventListener('input', () => renderSkeletons(allSkeletons));
document.getElementById('sort').addEventListener('change', () => renderSkeletons(allSkeletons));
document.getElementById('refresh-btn').addEventListener('click', () => loadHall());
document.getElementById('close-modal').addEventListener('click', closeDetails);
document.getElementById('detail-backdrop').addEventListener('click', (e) => {
  if (e.target.id === 'detail-backdrop') closeDetails();
});

setInterval(loadHall, 30000);
setInterval(loadLocalRuntime, 8000);
loadHall();
loadLocalRuntime();
connectSessionStream();
</script>
