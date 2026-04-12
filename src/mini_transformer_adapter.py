from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class MiniTransformerBlueprint:
    skeleton_name: str
    d_model: int
    num_layers: int
    num_heads: int
    ffn_dim: int
    dropout: float
    max_seq_len: int
    vocab_size: int
    source_fitness: float
    source_generation: float


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _nearest_multiple(value: int, step: int) -> int:
    return max(step, int(round(value / step) * step))


def _pick_num_heads(d_model: int) -> int:
    for candidate in (12, 10, 8, 6, 4, 2):
        if d_model % candidate == 0:
            return candidate
    return 1


def blueprint_from_skeleton(skeleton: Dict[str, Any]) -> MiniTransformerBlueprint:
    facts = skeleton.get("facts", {}) or {}
    nodes = int(facts.get("nodes", 24) or 24)
    density = float(facts.get("density", 0.1) or 0.1)
    modularity = float(facts.get("modularity", 0.2) or 0.2)
    feedback_loops = int(facts.get("feedback_loops", 0) or 0)
    fitness = float(skeleton.get("fitness", 0.3) or 0.3)
    generation = float(skeleton.get("generation", 1.0) or 1.0)

    base_model = 192 + nodes * 8 + int(modularity * 128)
    d_model = _nearest_multiple(int(_clamp(base_model, 128, 768)), 32)

    depth = int(_clamp(2 + nodes // 10 + int(density * 4), 2, 12))
    heads = _pick_num_heads(d_model)
    ffn_dim = d_model * 4
    dropout = round(_clamp(0.08 + feedback_loops * 0.01 + (0.35 - fitness) * 0.2, 0.05, 0.25), 3)
    max_seq_len = int(_clamp(256 + nodes * 8, 256, 2048))

    return MiniTransformerBlueprint(
        skeleton_name=str(skeleton.get("name", "unknown-skeleton")),
        d_model=d_model,
        num_layers=depth,
        num_heads=heads,
        ffn_dim=ffn_dim,
        dropout=dropout,
        max_seq_len=max_seq_len,
        vocab_size=32000,
        source_fitness=fitness,
        source_generation=generation,
    )


def build_pytorch_model(blueprint: MiniTransformerBlueprint):
    try:
        import torch
        import torch.nn as nn
    except Exception as exc:  # pragma: no cover - optional runtime path
        raise RuntimeError("PyTorch not available. Install torch to build model instances.") from exc

    class MiniTransformerLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.token_embedding = nn.Embedding(blueprint.vocab_size, blueprint.d_model)
            self.position_embedding = nn.Embedding(blueprint.max_seq_len, blueprint.d_model)
            layer = nn.TransformerEncoderLayer(
                d_model=blueprint.d_model,
                nhead=blueprint.num_heads,
                dim_feedforward=blueprint.ffn_dim,
                dropout=blueprint.dropout,
                batch_first=True,
            )
            self.encoder = nn.TransformerEncoder(layer, num_layers=blueprint.num_layers)
            self.norm = nn.LayerNorm(blueprint.d_model)
            self.lm_head = nn.Linear(blueprint.d_model, blueprint.vocab_size)

        def forward(self, input_ids):
            seq_len = input_ids.shape[1]
            if seq_len > blueprint.max_seq_len:
                raise ValueError(f"sequence length {seq_len} exceeds max_seq_len={blueprint.max_seq_len}")
            pos = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(input_ids.shape[0], seq_len)
            x = self.token_embedding(input_ids) + self.position_embedding(pos)
            x = self.encoder(x)
            x = self.norm(x)
            return self.lm_head(x)

    return MiniTransformerLM()


def _load_skeleton(ancestry_path: Path, skeleton_name: str | None) -> Dict[str, Any]:
    with ancestry_path.open("r", encoding="utf-8") as f:
        ancestry = json.load(f)

    if not isinstance(ancestry, list) or not ancestry:
        raise ValueError("ancestry data is empty or invalid")

    if skeleton_name:
        for item in ancestry:
            if item.get("name") == skeleton_name:
                return item
        raise ValueError(f"skeleton not found: {skeleton_name}")

    return max(ancestry, key=lambda x: float(x.get("fitness", 0.0) or 0.0))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mini-transformer blueprints from Mom4AI ancestry data.")
    parser.add_argument("--ancestry-json", default="ancestry.json")
    parser.add_argument("--skeleton-name", default=None)
    parser.add_argument("--output", default=None, help="Optional output JSON file path")
    parser.add_argument("--with-model-stats", action="store_true", help="Instantiate PyTorch modules and print parameter count")
    args = parser.parse_args()

    skeleton = _load_skeleton(Path(args.ancestry_json), args.skeleton_name)
    blueprint = blueprint_from_skeleton(skeleton)
    payload = asdict(blueprint)

    if args.with_model_stats:
        model = build_pytorch_model(blueprint)
        params = sum(p.numel() for p in model.parameters())
        payload["pytorch_param_count"] = int(params)

    if args.output:
        Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"blueprint_saved={args.output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
