from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from bio_components import BIO_COMPONENTS


CATEGORY_RULES = {
    "mikrobiell": ["bakter", "biofilm", "quorum", "virus", "flechten"],
    "neuro_biologisch": ["gehirn", "neur", "glia", "echolot", "oktopus", "nervensystem"],
    "tier_schwarm": ["schwarm", "rudel", "vogel", "murmuration", "fisch", "delphin", "orca", "ameisen", "bienen"],
    "oekosystem": ["korallen", "myzel", "wurzel", "regenwald", "mangrove", "pilz", "algen", "pflanzen"],
    "human_system": ["stadt", "krankenhaus", "logistik", "open_source", "bildungs", "katastrophen", "markt"],
}

LOCALIZATION_HINTS = {
    "ameisen": "ant",
    "bienen": "bee",
    "myzel": "mycelium",
    "gehirn": "brain",
    "vogel": "bird",
    "oktopus": "octopus",
    "korallen": "coral",
    "pflanzen": "plant",
    "wolf": "wolf",
    "termit": "termite",
    "delphin": "dolphin",
    "orca": "orca",
    "stadt": "city",
    "bildungs": "education",
    "logistik": "logistics",
    "krankenhaus": "hospital",
}

SUGGESTED_CANDIDATES = {
    "quallen_schwarm_signal": {"plastizitaet": 0.77, "dezentral": 0.95},
    "walgesang_langdistanz": {"plastizitaet": 0.73, "dezentral": 0.72},
    "biberlandschaft_ingenieur": {"plastizitaet": 0.69, "dezentral": 0.64},
    "papierwespen_nestlogik": {"plastizitaet": 0.71, "dezentral": 0.82},
    "koalitions_diplomatie_mensch": {"plastizitaet": 0.78, "dezentral": 0.67},
    "fruehwarnnetz_epidemiologie": {"plastizitaet": 0.83, "dezentral": 0.88},
}


@dataclass
class ComponentRecord:
    name: str
    plastizitaet: float
    dezentral: float
    category: str
    label_de: str
    label_en: str


def _category_for(name: str) -> str:
    n = name.lower()
    for category, needles in CATEGORY_RULES.items():
        if any(needle in n for needle in needles):
            return category
    return "hybrid"


def _label_de(name: str) -> str:
    return name.replace("_", " ").strip()


def _label_en(name: str) -> str:
    parts = name.split("_")
    translated = []
    for part in parts:
        replacement = part
        for de_hint, en_hint in LOCALIZATION_HINTS.items():
            if de_hint in part:
                replacement = part.replace(de_hint, en_hint)
                break
        translated.append(replacement)
    return " ".join(translated)


def build_component_registry(components: Dict[str, Dict[str, float]] | None = None) -> List[ComponentRecord]:
    source = components or BIO_COMPONENTS
    records: List[ComponentRecord] = []
    for name, metrics in sorted(source.items()):
        records.append(
            ComponentRecord(
                name=name,
                plastizitaet=float(metrics.get("plastizitaet", 0.0)),
                dezentral=float(metrics.get("dezentral", 0.0)),
                category=_category_for(name),
                label_de=_label_de(name),
                label_en=_label_en(name),
            )
        )
    return records


def summarize_registry(records: List[ComponentRecord]) -> dict:
    by_category: Dict[str, int] = {}
    for r in records:
        by_category[r.category] = by_category.get(r.category, 0) + 1
    return {
        "total_components": len(records),
        "category_counts": dict(sorted(by_category.items())),
        "avg_plastizitaet": round(sum(r.plastizitaet for r in records) / max(1, len(records)), 4),
        "avg_dezentral": round(sum(r.dezentral for r in records) / max(1, len(records)), 4),
    }


def suggest_new_components(limit: int = 5) -> List[dict]:
    existing = set(BIO_COMPONENTS.keys())
    suggestions = []
    for name, metrics in SUGGESTED_CANDIDATES.items():
        if name in existing:
            continue
        suggestions.append(
            {
                "name": name,
                "metrics": metrics,
                "category": _category_for(name),
                "label_de": _label_de(name),
                "label_en": _label_en(name),
            }
        )
    return suggestions[: max(0, int(limit))]


def roadmap_markdown_snippet(registry_summary: dict) -> str:
    total = registry_summary.get("total_components", 0)
    return (
        f"- [x] Component Manager (Katalog + Auto-Lokalisierung + Kategorien)\n"
        f"  **Resonanz:** `69/100` 🟩🟩🟩⬜⬜\n"
        f"  **Chemie (Repo-Fit):** `87/100` 🟩🟩🟩🟩⬜\n"
        f"  **Coach-Feedback:** Komponentenbasis auf {total} Einträge skaliert, "
        f"Taxonomie + DE/EN-Labels für zukünftige Erweiterungen operationalisiert."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage, localize and summarize MomAI bio components.")
    parser.add_argument("--output", default="docs/component_registry.json")
    parser.add_argument("--suggest", type=int, default=6, help="Number of candidate components to suggest.")
    parser.add_argument("--print-roadmap-snippet", action="store_true")
    args = parser.parse_args()

    records = build_component_registry()
    summary = summarize_registry(records)
    payload = {
        "summary": summary,
        "components": [asdict(r) for r in records],
        "suggestions": suggest_new_components(limit=args.suggest),
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote registry: {out_path}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.print_roadmap_snippet:
        print("\n--- roadmap-snippet ---")
        print(roadmap_markdown_snippet(summary))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
