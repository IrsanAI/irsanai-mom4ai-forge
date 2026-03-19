import random
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import uuid
from datetime import datetime
from bio_components import BIO_COMPONENTS
from child_generator import generate_child_mixture
from tqdm import tqdm

SURVIVORS_DIR = "survivors"
os.makedirs(SURVIVORS_DIR, exist_ok=True)
VISUALS_DIR = "survivors/visuals"
os.makedirs(VISUALS_DIR, exist_ok=True)


class MomForge:
    def __init__(self):
        self.children = []
        self.generation = 0
        print("🤱 Mom4AI erwacht... bereit, architektonische Skelette zu gebären.")

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

    def birth_new_skeleton(self, num_components: int = 3):
        mixture = generate_child_mixture(num_components)

        # Unique ID & sprechender Name
        unique_id = str(uuid.uuid4())[:8]
        dominant_components = sorted(mixture.items(), key=lambda x: x[1], reverse=True)[:2]
        name_parts = [comp.split('_')[0].capitalize() for comp, _ in dominant_components]
        name = f"{''.join(name_parts)}-G{self.generation}-{len(self.children) + 1}-{unique_id}"

        # Factsheet
        factsheet = {
            "id": unique_id,
            "name": name,
            "generation": self.generation,
            "mixture": mixture,
            "timestamp": datetime.now().isoformat(),
            "facts": {
                "nodes": 0,
                "edges": 0,
                "density": 0.0,
                "modularity": 0.0,
                "feedback_loops": 0,
                "dominant_type": max(mixture, key=mixture.get) if mixture else "unknown"
            }
        }

        # Bio-DNA Parameter
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

        # Factsheet füllen
        factsheet["facts"]["nodes"] = G.number_of_nodes()
        factsheet["facts"]["edges"] = G.number_of_edges()
        factsheet["facts"]["density"] = G.number_of_edges() / (G.number_of_nodes() * (G.number_of_nodes() - 1)) if G.number_of_nodes() > 1 else 0
        factsheet["facts"]["modularity"] = nx.community.modularity(G, nx.community.greedy_modularity_communities(G)) if G.number_of_nodes() > 10 else 0.3
        factsheet["facts"]["feedback_loops"] = sum(1 for u, v, d in G.edges(data=True) if d.get('type') == 'feedback')

        print(f"✅ Skelett geboren: {name} | Knoten: {num_nodes} | Kanten: {G.number_of_edges()} | DNA: {mixture}")
        return G, mixture, name, factsheet

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
        fitness = min(1.0, max(0.0, fitness * 1.2))  # kleiner Boost

        print(f"  → Auto-Fitness: {fitness:.3f} (Density: {density:.3f}, Modularity: {modularity:.3f})")
        return fitness

    def simulate_feedback(self, fitness: float):
        if fitness > 0.50:
            verdict = "🌟 Starke Architektur – überlebt & wird Basis!"
        elif fitness > 0.35:
            verdict = "🟢 Gute Architektur – überlebt"
        elif fitness > 0.20:
            verdict = "🟡 Mittel – bleibt neutral"
        else:
            verdict = "💀 Schwache Architektur – stirbt aus"
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

    survivors = []
    for _ in range(3):
        G, mixture, name, factsheet = mom.birth_new_skeleton(num_components=random.randint(2, 6))
        mom.visualize_skeleton(G, name)

        combined_fitness = mom.calculate_auto_fitness(G, mixture)
        survives = mom.simulate_feedback(combined_fitness)

        if survives:
            mom.save_survivor_skeleton(G, combined_fitness, mixture, name)
            factsheet["fitness"] = combined_fitness
            factsheet["image_path"] = f"images/{name}.png"
            ancestry.append(factsheet)
            survivors.append(name)
            print(f"💾 Skelett {name} zur ancestry.json hinzugefügt")

    with open(ancestry_path, 'w', encoding='utf-8') as f:
        json.dump(ancestry, f, indent=2, ensure_ascii=False)
    print(f"Ancestry aktualisiert: {len(ancestry)} Skelette insgesamt")

    print(f"\n🎉 {len(survivors)} Skelette überlebt: {', '.join(survivors) or 'keine'}")
    print("Mom4AI lebt – nächste Generation kann auf alten Skeletten aufbauen.")