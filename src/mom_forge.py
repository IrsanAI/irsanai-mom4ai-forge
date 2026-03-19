import random
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import StratifiedShuffleSplit
from bio_components import BIO_COMPONENTS
from child_generator import generate_child_mixture
from tqdm import tqdm

# Mini-Dataset laden (Fashion-MNIST)
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
train_dataset = torchvision.datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)


class ChildAI(nn.Module):
    """Ein KI-Kind – kleines CNN mit Bio-DNA"""

    def __init__(self, bio_mixture: dict, name: str):
        super().__init__()
        self.name = name
        self.bio_mixture = bio_mixture

        # Einfaches CNN (angepasst an Fashion-MNIST 28x28)
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

        print(f"✅ Kind geboren: {name} | DNA: {bio_mixture}")

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


class MomForge:
    def __init__(self):
        self.children = []
        self.generation = 0
        print("🤱 Mom4AI erwacht... bereit, Kinder zu gebären.")

    def birth_and_train_child(self, num_components: int = 3, subset_size: int = 2000, epochs: int = 2):
        mixture = generate_child_mixture(num_components)
        name = f"Child-G{self.generation}-{len(self.children) + 1}"
        child = ChildAI(mixture, name)

        # Kleines, stratifiziertes Subset (gleiche Klassenverteilung)
        sss = StratifiedShuffleSplit(n_splits=1, train_size=subset_size, random_state=random.randint(0, 9999))
        train_idx, _ = next(sss.split(train_dataset.data, train_dataset.targets))
        mini_dataset = Subset(train_dataset, train_idx)
        loader = DataLoader(mini_dataset, batch_size=64, shuffle=True)

        # Training
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(child.parameters(), lr=0.001)

        child.train()
        total_loss = 0
        for epoch in range(epochs):
            epoch_loss = 0
            for images, labels in tqdm(loader, desc=f"Training {name} Epoche {epoch + 1}/{epochs}", leave=False):
                optimizer.zero_grad()
                outputs = child(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            avg_loss = epoch_loss / len(loader)
            total_loss += avg_loss
            print(f"  Epoche {epoch + 1} → Avg Loss: {avg_loss:.4f}")

        avg_final_loss = total_loss / epochs
        fitness = max(0.0, 1.0 - avg_final_loss / 2.5)  # grobe Fitness: niedriger Loss → hohe Fitness
        print(f"🏁 {name} fertig trainiert | Final Avg Loss: {avg_final_loss:.4f} | Fitness: {fitness:.3f}")

        child.eval()  # für spätere Nutzung
        self.children.append({"model": child, "fitness": fitness, "mixture": mixture})
        self.generation += 1
        return child, fitness

    def simulate_feedback(self, fitness: float):
        """Fitness-basiertes Überleben (kann später mit User/Agent kombiniert werden)"""
        if fitness > 0.65:
            verdict = "❤️ überlebt & wird stärker!"
        elif fitness < 0.35:
            verdict = "💀 stirbt aus..."
        else:
            verdict = "🟡 bleibt neutral."
        print(verdict)
        return fitness > 0.35  # True = überlebt


if __name__ == "__main__":
    mom = MomForge()

    # 4 Kinder gebären & trainieren (mehr dauert zu lange für Test)
    survivors = []
    for _ in range(4):
        child, fitness = mom.birth_and_train_child(num_components=random.randint(2, 5))
        survives = mom.simulate_feedback(fitness)
        if survives:
            survivors.append(child.name)

    print(f"\n🎉 {len(survivors)} Kinder überlebt: {', '.join(survivors)}")
    print("Mom4AI lebt und lernt weiter.")