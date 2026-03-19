import random
import numpy as np
from bio_components import BIO_COMPONENTS

def generate_child_mixture(num_components: int = 3) -> dict:
    """Erzeugt eine zufällige prozentuale Mischung (0–100 %)"""
    components = list(BIO_COMPONENTS.keys())  # aus bio_components importiert
    selected = random.sample(components, min(num_components, len(components)))

    weights = np.random.dirichlet(np.ones(len(selected))) * 100  # summe = 100%
    mixture = {comp: round(float(w), 2) for comp, w in zip(selected, weights)}

    return mixture