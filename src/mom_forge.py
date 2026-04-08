import random
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import uuid
import hashlib
from datetime import datetime
from bio_components import BIO_COMPONENTS
from child_generator import generate_child_mixture, crossover_mixtures, mutate_mixture
from resonance_protocol import score_interactions, classify_resonance

SURVIVORS_DIR = "survivors"
os.makedirs(SURVIVORS_DIR, exist_ok=True)
VISUALS_DIR = "survivors/visuals"
os.makedirs(VISUALS_DIR, exist_ok=True)
USER_FILE = ".user.json"
RESONANCE_EVENTS_FILE = "resonance_events.jsonl"


class MomForge:
    def __init__(self):
        self.children = []
        self.generation = 0
        self.user_id = self.get_or_create_user_id()
        print(f"🤱 Mom4AI erwacht... (User: {self.user_id})")

    def get_or_create_user_id(self):
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data["user_id"]

        while True:
            user_id = input(
                "Gib deinen einzigartigen GitHub-Namen oder Identifier ein (z.B. 'IrsanAI', 'CoolDev42'): ").strip()
            if not user_id:
                user_id = f"User-{uuid.uuid4()[:6]}"

            # Prüfen, ob Name schon zentral existiert
            if self.is_user_id_taken(user_id):
                print(f"Name '{user_id}' ist leider schon vergeben. Wähle bitte einen anderen.")
                continue

            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump({"user_id": user_id}, f)
            print(f"Name '{user_id}' erfolgreich registriert!")
            return user_id

    def is_user_id_taken(self, user_id):
        users_path = "users.json"
        if not os.path.exists(users_path):
            return False

        with open(users_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
        return user_id in [u["name"] for u in users]

    def compute_dna_hash(self, mixture, graph):
        data = str(sorted(mixture.items())) + str(nx.node_link_data(graph))
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def load_survivors(self):
        if not os.path.exists(SURVIVORS_DIR):
            print("Keine Überlebenden gefunden.")
            return

        loaded_count = 0
        for file in os.listdir(SURVIVORS_DIR):
            if file.endswith(".json"):
                path = os.path.join(SURVIVORS_DIR, file)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                G = nx.node_link_graph(data["graph_data"])
                print(f"🔄 Geladen: {data['name']} (Fitness {data['fitness']:.3f})")
                self.children.append({
                    "graph": G,
                    "fitness": data["fitness"],
                    "mixture": data["mixture"],
                    "name": data["name"]
                })
                loaded_count += 1

        self.generation = max([c["fitness"] for c in self.children] or [0]) + 1 if self.children else 0
        print(f"✅ {loaded_count} Skelette geladen. Nächste Generation: {self.generation}")

    @staticmethod
    def dominant_component(mixture: dict) -> str:
        if not mixture:
            return "unknown"
        return max(mixture, key=mixture.get)

    def select_parent_candidates(self, limit: int = 12):
        """
        Lineage-aware Parent Selection:
        - priorisiert Fitness
        - hält Diversität über dominante DNA-Komponenten
        """
        ranked = sorted(self.children, key=lambda c: c.get("fitness", 0), reverse=True)
        if not ranked:
            return []

        selected = []
        seen_dominants = set()
        for candidate in ranked:
            dominant = self.dominant_component(candidate.get("mixture", {}))
            if dominant not in seen_dominants or len(selected) < max(3, limit // 3):
                selected.append(candidate)
                seen_dominants.add(dominant)
            if len(selected) >= limit:
                break

        # falls durch Diversitätsregel noch nicht genug Eltern da sind
        if len(selected) < min(limit, len(ranked)):
            for candidate in ranked:
                if candidate in selected:
                    continue
                selected.append(candidate)
                if len(selected) >= limit:
                    break
        return selected

    def birth_new_skeleton(
        self,
        num_components: int = 3,
        strategy: str = "random",
        parent_pool=None,
        mutation_strength: float = 0.08,
        crossover_noise: float = 0.07
    ):
        parent_pool = parent_pool or []
        if strategy == "crossover" and len(parent_pool) >= 2:
            p1, p2 = random.sample(parent_pool, 2)
            mixture = crossover_mixtures(p1["mixture"], p2["mixture"], mutation_noise=crossover_noise)
            parent_names = [p1["name"], p2["name"]]
        elif strategy == "mutation" and len(parent_pool) >= 1:
            p = random.choice(parent_pool)
            mixture = mutate_mixture(p["mixture"], mutation_strength=mutation_strength)
            parent_names = [p["name"]]
        else:
            mixture = generate_child_mixture(num_components)
            parent_names = []

        unique_id = str(uuid.uuid4())[:8]
        dominant_components = sorted(mixture.items(), key=lambda x: x[1], reverse=True)[:2]
        name_parts = [comp.split('_')[0].capitalize() for comp, _ in dominant_components]
        name = f"{''.join(name_parts)}-G{self.generation}-{len(self.children) + 1}-{unique_id}"

        factsheet = {
            "id": unique_id,
            "name": name,
            "generation": self.generation,
            "mixture": mixture,
            "produced_by": self.user_id,
            "timestamp": datetime.now().isoformat(),
            "facts": {
                "nodes": 0,
                "edges": 0,
                "density": 0.0,
                "modularity": 0.0,
                "feedback_loops": 0,
                "dominant_type": max(mixture, key=mixture.get) if mixture else "unknown"
            },
            "creation_mode": strategy,
            "parents": parent_names
        }

        total_plast = sum(
            (mixture.get(k, 0) / 100.0) * BIO_COMPONENTS.get(k, {}).get("plastizitaet", 0.5)
            for k in mixture
        )

        total_dezentral = sum(
            (mixture.get(k, 0) / 100.0) * BIO_COMPONENTS.get(k, {}).get("dezentral", 0.5)
            for k in mixture
        )

        print(f"DEBUG: total_plast = {total_plast:.4f} | total_dezentral = {total_dezentral:.4f}")

        num_nodes = min(40, int(10 + 30 * total_plast))
        edge_prob = min(0.30, 0.05 + 0.25 * total_dezentral)

        G = nx.DiGraph()

        layer_types = ["AttentionHead", "MyzelRouter", "SwarmFFN", "StandardMLP", "PlasticityGate"]
        type_weights = [
            mixture.get("mensch_gehirn", 0) / 100 + mixture.get("quorum_sensing", 0) / 100,
            mixture.get("myzel_netz", 0) / 100,
            mixture.get("ameisen_schwarm", 0) / 100 + mixture.get("bienen_schwarm", 0) / 100,
            0.5,
            total_plast
        ]
        type_weights = [w / sum(type_weights) for w in type_weights] if sum(type_weights) > 0 else [0.2] * 5

        for i in range(num_nodes):
            layer_type = random.choices(layer_types, weights=type_weights, k=1)[0]
            G.add_node(i, type=layer_type, bio_influence=mixture)

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < edge_prob:
                    G.add_edge(i, j, weight=random.uniform(0.5, 1.5), type="forward")
            if random.random() < 0.15 * total_dezentral:
                G.add_edge(random.randint(0, i), i, weight=random.uniform(0.3, 0.8), type="feedback")

        factsheet["facts"]["nodes"] = G.number_of_nodes()
        factsheet["facts"]["edges"] = G.number_of_edges()
        factsheet["facts"]["density"] = G.number_of_edges() / (G.number_of_nodes() * (G.number_of_nodes() - 1)) if G.number_of_nodes() > 1 else 0
        factsheet["facts"]["modularity"] = nx.community.modularity(G, nx.community.greedy_modularity_communities(G)) if G.number_of_nodes() > 10 else 0.3
        factsheet["facts"]["feedback_loops"] = sum(1 for u, v, d in G.edges(data=True) if d.get('type') == 'feedback')

        dna_hash = self.compute_dna_hash(mixture, G)

        print(f"✅ Skelett geboren: {name} | Knoten: {num_nodes} | Kanten: {G.number_of_edges()} | DNA-Hash: {dna_hash}")
        return G, mixture, name, factsheet, dna_hash

    def visualize_skeleton(self, G, name):
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(10, 8))
        node_colors = [hash(G.nodes[n]['type']) % 10 for n in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.tab10,
                node_size=800, font_size=10, arrows=True, arrowstyle='->', arrowsize=15)
        plt.title(f"Skelett {name}")
        vis_path = os.path.join(VISUALS_DIR, f"{name}.png")
        plt.savefig(vis_path)
        plt.close()
        print(f"📊 Visualisierung gespeichert: {vis_path}")

    def calculate_auto_fitness(self, G, mixture):
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        if num_nodes < 5:
            return 0.1

        density = num_edges / (num_nodes * (num_nodes - 1))
        modularity = nx.community.modularity(G, nx.community.greedy_modularity_communities(G)) if num_nodes > 10 else 0.3
        feedback_loops = sum(1 for u, v, d in G.edges(data=True) if d.get('type') == 'feedback')

        bio_score = sum((mixture.get(k, 0) / 100) * BIO_COMPONENTS.get(k, {}).get("plastizitaet", 0.5) for k in mixture)

        fitness = (
            0.25 * density +
            0.35 * modularity +
            0.25 * (feedback_loops / max(1, num_nodes)) +
            0.15 * bio_score
        )
        fitness = min(1.0, max(0.0, fitness * 1.2))

        print(f"  → Auto-Fitness: {fitness:.3f} (Density: {density:.3f}, Modularity: {modularity:.3f})")
        return fitness

    def load_resonance_scores(self):
        if not os.path.exists(RESONANCE_EVENTS_FILE):
            return {}

        per_skeleton_events = {}
        with open(RESONANCE_EVENTS_FILE, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                skeleton_name = event.get("skeleton_name")
                if not skeleton_name:
                    continue
                per_skeleton_events.setdefault(skeleton_name, []).append(event)

        scores = {}
        for skeleton_name, events in per_skeleton_events.items():
            result = score_interactions(events)
            scores[skeleton_name] = {
                "score": result.score,
                "connection": result.connection,
                "coordination": result.coordination,
                "interaction_count": result.interaction_count,
                "classification": result.classification
            }
        return scores

    def calculate_combined_fitness(self, auto_fitness: float, resonance_score: float, interaction_count: int):
        if interaction_count <= 0:
            return auto_fitness

        if interaction_count >= 5:
            resonance_weight = 0.70
        else:
            resonance_weight = 0.20 + (interaction_count / 5.0) * 0.50

        auto_weight = 1.0 - resonance_weight
        combined = (auto_weight * auto_fitness) + (resonance_weight * resonance_score)
        return max(0.0, min(1.0, combined))

    @staticmethod
    def mixture_distance(m1: dict, m2: dict) -> float:
        keys = set(m1.keys()) | set(m2.keys())
        if not keys:
            return 0.0
        l1 = sum(abs(float(m1.get(k, 0.0)) - float(m2.get(k, 0.0))) for k in keys)
        return max(0.0, min(1.0, l1 / 200.0))

    def calculate_multi_objective_score(
        self,
        auto_fitness: float,
        resonance_score: float,
        interaction_count: int,
        child_mixture: dict,
        parent_pool: list
    ):
        base = self.calculate_combined_fitness(auto_fitness, resonance_score, interaction_count)
        if not parent_pool:
            return base, 0.0

        distances = [self.mixture_distance(child_mixture, p.get("mixture", {})) for p in parent_pool[:8]]
        diversity_score = sum(distances) / len(distances) if distances else 0.0
        final = (0.75 * base) + (0.25 * diversity_score)
        return max(0.0, min(1.0, final)), diversity_score

    def simulate_feedback(self, fitness: float, resonance_classification: str = "no_data"):
        if fitness > 0.50 and resonance_classification in ("resonant", "emerging", "insufficient_data", "no_data"):
            verdict = f"🌟 Stark – überlebt ({resonance_classification})"
        elif fitness > 0.35:
            verdict = f"🟢 Gut – überlebt ({resonance_classification})"
        elif fitness > 0.20 and resonance_classification in ("neutral", "insufficient_data", "no_data"):
            verdict = f"🟡 Mittel – bleibt neutral ({resonance_classification})"
        else:
            verdict = f"💀 Schwach – stirbt aus ({resonance_classification})"
        print(verdict)
        return fitness > 0.20

    def save_survivor_skeleton(self, G, fitness, mixture, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "name": name,
            "generation": self.generation - 1,
            "mixture": mixture,
            "fitness": fitness,
            "timestamp": timestamp,
            "graph_data": nx.node_link_data(G)
        }
        path = os.path.join(SURVIVORS_DIR, f"{name}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Skelett gespeichert: {name} (Fitness {fitness:.3f})")


if __name__ == "__main__":
    mom = MomForge()

    if os.path.exists(SURVIVORS_DIR) and any(f.endswith('.json') for f in os.listdir(SURVIVORS_DIR)):
        print("Alte Skelette gefunden – lade automatisch...")
        mom.load_survivors()

    ancestry_path = "ancestry.json"
    ancestry = []
    if os.path.exists(ancestry_path):
        with open(ancestry_path, 'r', encoding='utf-8') as f:
            ancestry = json.load(f)
        print(f"Ancestry geladen: {len(ancestry)} Einträge")

    resonance_scores = mom.load_resonance_scores()
    if resonance_scores:
        print(f"Resonance-Events geladen: {len(resonance_scores)} Skelette mit Live-Interaktion")
    else:
        print("Keine Resonance-Events gefunden – Auto-Fitness als Vorfilter aktiv.")

    survivors = []
    anzahl = int(input("Wie viele neue Skelette sollen gebaut werden? ") or "8")
    for _ in range(anzahl):
        parent_candidates = mom.select_parent_candidates(limit=12)
        diversity = len({mom.dominant_component(c.get("mixture", {})) for c in parent_candidates}) / max(1, len(parent_candidates))
        adaptive_mutation = 0.06 if diversity > 0.6 else 0.11
        adaptive_crossover_noise = 0.05 if diversity > 0.6 else 0.10
        rnd = random.random()
        strategy = "random"
        if len(parent_candidates) >= 2 and rnd < 0.45:
            strategy = "crossover"
        elif len(parent_candidates) >= 1 and rnd < 0.75:
            strategy = "mutation"

        G, mixture, name, factsheet, dna_hash = mom.birth_new_skeleton(
            num_components=random.randint(2, 6),
            strategy=strategy,
            parent_pool=parent_candidates,
            mutation_strength=adaptive_mutation,
            crossover_noise=adaptive_crossover_noise
        )
        mom.visualize_skeleton(G, name)

        auto_fitness = mom.calculate_auto_fitness(G, mixture)
        resonance_entry = resonance_scores.get(name, {})
        resonance_fitness = float(resonance_entry.get("score", 0.0))
        interaction_count = int(resonance_entry.get("interaction_count", 0))
        objective_ar = mom.calculate_combined_fitness(auto_fitness, resonance_fitness, interaction_count)
        combined_fitness, diversity_objective = mom.calculate_multi_objective_score(
            auto_fitness=auto_fitness,
            resonance_score=resonance_fitness,
            interaction_count=interaction_count,
            child_mixture=mixture,
            parent_pool=parent_candidates
        )
        resonance_classification = resonance_entry.get(
            "classification",
            classify_resonance(resonance_fitness, interaction_count)
        )

        print(
            f"  → Resonance: {resonance_fitness:.3f} | Interaktionen: {interaction_count} | "
            f"Klassifikation: {resonance_classification}"
        )
        print(f"  → Objective(Auto+Resonance): {objective_ar:.3f}")
        print(f"  → Objective(Diversity): {diversity_objective:.3f}")
        print(f"  → Combined Fitness (multi-objective): {combined_fitness:.3f}")
        survives = mom.simulate_feedback(combined_fitness, resonance_classification)

        if survives:
            mom.save_survivor_skeleton(G, combined_fitness, mixture, name)
            factsheet["fitness"] = combined_fitness
            factsheet["auto_fitness"] = auto_fitness
            factsheet["resonance_fitness"] = resonance_fitness
            factsheet["resonance_interactions"] = interaction_count
            factsheet["resonance_classification"] = resonance_classification
            factsheet["objective_auto_resonance"] = objective_ar
            factsheet["objective_diversity"] = diversity_objective
            factsheet["image_path"] = f"images/{name}.png"
            ancestry.append(factsheet)
            survivors.append(name)
            print(f"💾 Skelett {name} zur ancestry.json hinzugefügt")

    with open(ancestry_path, 'w', encoding='utf-8') as f:
        json.dump(ancestry, f, indent=2, ensure_ascii=False)
    # GitHub Pages liest aus docs/; daher ancestry auch dort spiegeln.
    docs_ancestry_path = os.path.join("docs", "ancestry.json")
    with open(docs_ancestry_path, 'w', encoding='utf-8') as f:
        json.dump(ancestry, f, indent=2, ensure_ascii=False)
    print(f"Ancestry aktualisiert: {len(ancestry)} Skelette insgesamt (root + docs)")
    # Nach dem ancestry-Speichern: User in users.json eintragen (nur beim ersten Mal oder wenn neu)
    users_path = "users.json"
    users = []
    if os.path.exists(users_path):
        try:
            with open(users_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    users = json.loads(content)
                else:
                    users = []
        except json.JSONDecodeError:
            print("users.json war kaputt oder leer – neu initialisiert")
            users = []

    if not any(u["name"] == mom.user_id for u in users):
        users.append({
            "name": mom.user_id,
            "first_seen": datetime.now().isoformat(),
            "skelette_count": len(survivors)
        })
        with open(users_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
        print(f"Dein Name '{mom.user_id}' wurde zentral registriert!")

    import subprocess
    import os

    # PAT aus Datei laden (sicherer als hardcode)
    pat_file = os.path.expanduser("~/.github_pat")
    if os.path.exists(pat_file):
        with open(pat_file, 'r') as f:
            pat = f.read().strip()
        repo_url = f"https://{pat}@github.com/IrsanAI/irsanai-mom4ai-forge.git"
    else:
        repo_url = "origin"

    print("Versuche automatisch zu pushen...")

    def _extract_error_text(err: subprocess.CalledProcessError) -> str:
        stderr = getattr(err, "stderr", None)
        stdout = getattr(err, "stdout", None)
        if isinstance(stderr, bytes):
            return stderr.decode(errors="ignore")
        if isinstance(stderr, str) and stderr.strip():
            return stderr
        if isinstance(stdout, bytes):
            return stdout.decode(errors="ignore")
        if isinstance(stdout, str) and stdout.strip():
            return stdout
        return str(err)

    try:
        # PAT sauber laden
        pat_file = os.path.expanduser("~/.github_pat")
        if os.path.exists(pat_file):
            with open(pat_file, 'r', encoding='utf-8-sig') as f:
                pat = f.read().strip()
            repo_url = f"https://{pat}@github.com/IrsanAI/irsanai-mom4ai-forge.git"
        else:
            repo_url = "origin"

        # 1. Alles temporär verstecken (Stash)
        print("   → Stash (verstecke Änderungen)...")
        subprocess.run(
            ["git", "stash", "push", "-m", "Auto-Push Stash"],
            check=True,
            capture_output=True,
            text=True
        )

        # 2. Pull mit Rebase
        print("   → Pull + Rebase...")
        subprocess.run(["git", "pull", repo_url, "main", "--rebase"], check=True, capture_output=True, text=True)

        # 3. Stash zurückholen
        print("   → Pop Stash...")
        subprocess.run(["git", "stash", "pop"], check=True, capture_output=True, text=True)

        # 4. Add + Commit + Push
        print("   → Add + Commit + Push...")
        subprocess.run(["git", "add", "ancestry.json", "docs/ancestry.json", "docs/images/", "users.json", ".user.json", "survivors/"],
                       check=True)
        commit_result = subprocess.run(
            ["git", "commit", "-m", f"Automatischer Upload: {len(survivors)} neue Skelette von {mom.user_id}"],
            capture_output=True,
            text=True
        )
        if commit_result.returncode != 0 and "nothing to commit" not in (commit_result.stdout + commit_result.stderr).lower():
            raise subprocess.CalledProcessError(
                commit_result.returncode,
                commit_result.args,
                output=commit_result.stdout,
                stderr=commit_result.stderr
            )

        subprocess.run(["git", "push", repo_url, "main"], check=True, capture_output=True, text=True)

        print("✅ Automatisch & konflikt-sicher gepusht! Pages aktualisiert sich in 1–2 Min.")

    except subprocess.CalledProcessError as e:
        print("Auto-Push fehlgeschlagen – mach manuell:")
        print("git add .")
        print("git commit -m 'Manueller Upload'")
        print("git pull --rebase")
        print("git push")
        details = _extract_error_text(e)
        if "refusing to allow a personal access token to create or update workflow" in details.lower():
            print("Hinweis: Dein PAT braucht zusätzlich den Scope 'workflow' oder nutze den origin-Remote mit lokalem Git-Login.")
        print("Fehler-Details:", details)
    except Exception as e:
        print("Unerwarteter Fehler:", str(e))

    # Dann push (wie vorher)
    print(f"\n🎉 {len(survivors)} Skelette überlebt: {', '.join(survivors) or 'keine'}")
    print("Mom4AI lebt – nächste Generation kann auf alten Skeletten aufbauen.")
