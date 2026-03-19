from bio_components import BIO_COMPONENTS, get_component
from child_generator import generate_child_mixture
import torch
import torch.nn as nn
import random


class ChildAI(nn.Module):
    """Ein KI-Kind – einfaches neuronales Netz mit Bio-DNA"""

    def __init__(self, bio_mixture: dict, name: str):
        super().__init__()
        self.name = name
        self.bio_mixture = bio_mixture
        self.layers = nn.Sequential(
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
        )
        print(f"✅ Kind geboren: {name} | DNA: {bio_mixture}")

    def forward(self, x):
        return self.layers(x)


class MomForge:
    """Die Mutter-KI – die Forge"""

    def __init__(self):
        self.children = []
        self.generation = 0
        print("🤱 Mom4AI erwacht... bereit, Kinder zu gebären.")

    def birth_child(self, num_components: int = 3):
        mixture = generate_child_mixture(num_components)
        name = f"Child-G{self.generation}-{len(self.children) + 1}"
        child = ChildAI(mixture, name)
        self.children.append(child)
        self.generation += 1
        return child

    def simulate_feedback(self, child, rating: float):
        """Reinforcement: User/Agent-Bewertung (0.0–1.0)"""
        if rating > 0.7:
            print(f"❤️ {child.name} überlebt & wird stärker!")
        elif rating < 0.3:
            print(f"💀 {child.name} stirbt aus...")
            self.children.remove(child)
        else:
            print(f"🟡 {child.name} bleibt neutral.")


if __name__ == "__main__":
    mom = MomForge()

    # Erste 5 Kinder gebären
    for _ in range(5):
        child = mom.birth_child(num_components=random.randint(2, 4))

        # Simuliertes Feedback
        rating = random.uniform(0.1, 0.95)
        mom.simulate_feedback(child, rating)

    print(f"\n🎉 {len(mom.children)} Kinder überlebt! Mom4AI lebt.")