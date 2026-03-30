import random
import numpy as np
from bio_components import BIO_COMPONENTS


def _normalize(mixture: dict) -> dict:
    total = sum(max(0.0, float(v)) for v in mixture.values())
    if total <= 0:
        return {}
    return {k: round((max(0.0, float(v)) / total) * 100.0, 2) for k, v in mixture.items()}


def generate_child_mixture(num_components: int = 3) -> dict:
    """Erzeugt eine zufällige prozentuale Mischung (0–100 %)"""
    components = list(BIO_COMPONENTS.keys())  # aus bio_components importiert
    selected = random.sample(components, min(num_components, len(components)))

    weights = np.random.dirichlet(np.ones(len(selected))) * 100  # summe = 100%
    mixture = {comp: round(float(w), 2) for comp, w in zip(selected, weights)}

    return _normalize(mixture)


def crossover_mixtures(parent_a: dict, parent_b: dict, mutation_noise: float = 0.07) -> dict:
    """Kombiniert zwei Eltern-DNA-Mischungen zu einem Kind."""
    all_keys = set(parent_a.keys()) | set(parent_b.keys())
    child = {}
    for key in all_keys:
        a = float(parent_a.get(key, 0.0))
        b = float(parent_b.get(key, 0.0))
        alpha = random.uniform(0.35, 0.65)
        base = alpha * a + (1.0 - alpha) * b
        noise = random.uniform(-mutation_noise * 100.0, mutation_noise * 100.0)
        child[key] = max(0.0, base + noise)
    return _normalize(child)


def mutate_mixture(mixture: dict, mutation_strength: float = 0.08) -> dict:
    """Leichte Mutation einer Mischung (drift + mögliche neue Komponente)."""
    if not mixture:
        return generate_child_mixture(num_components=3)

    mutated = {k: float(v) for k, v in mixture.items()}
    for key in list(mutated.keys()):
        delta = random.uniform(-mutation_strength * 100.0, mutation_strength * 100.0)
        mutated[key] = max(0.0, mutated[key] + delta)

    # gelegentlich neue Komponente injizieren
    if random.random() < 0.25:
        candidate = random.choice(list(BIO_COMPONENTS.keys()))
        mutated[candidate] = mutated.get(candidate, 0.0) + random.uniform(1.0, 8.0)

    return _normalize(mutated)
