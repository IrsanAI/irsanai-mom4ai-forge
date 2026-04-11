from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from mini_transformer_adapter import blueprint_from_skeleton, build_pytorch_model


def _load_skeleton(ancestry_path: Path, skeleton_name: str | None):
    ancestry = json.loads(ancestry_path.read_text(encoding="utf-8"))
    if not ancestry:
        raise ValueError("empty ancestry")
    if skeleton_name:
        for row in ancestry:
            if row.get("name") == skeleton_name:
                return row
        raise ValueError(f"skeleton not found: {skeleton_name}")
    return max(ancestry, key=lambda x: float(x.get("fitness", 0) or 0))


def _load_corpus(corpus_path: Path | None, skeleton: dict) -> str:
    if corpus_path and corpus_path.exists():
        return corpus_path.read_text(encoding="utf-8")
    dominant = skeleton.get("facts", {}).get("dominant_type", "bio")
    return (
        f"Mom4AI evolution report for {skeleton.get('name', 'skeleton')}. "
        f"Dominant type: {dominant}. "
        "Resonance and chemistry guide the next generation. "
    ) * 200


def _build_char_vocab(text: str, vocab_size: int):
    chars = sorted(set(text))
    if not chars:
        chars = [" "]
    # reserve 0 for unknown/pad
    chars = chars[: max(1, vocab_size - 1)]
    stoi = {ch: i + 1 for i, ch in enumerate(chars)}
    itos = {i + 1: ch for i, ch in enumerate(chars)}
    return stoi, itos


def _encode(text: str, stoi: dict[int, str] | dict[str, int]):
    return [stoi.get(ch, 0) for ch in text]


def train_once(
    ancestry_json: Path,
    output_dir: Path,
    skeleton_name: str | None = None,
    corpus_path: Path | None = None,
    steps: int = 40,
    batch_size: int = 8,
    seq_len: int = 64,
    lr: float = 3e-4,
):
    try:
        import torch
        import torch.nn.functional as F
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("PyTorch is required for mini-transformer training") from exc

    skeleton = _load_skeleton(ancestry_json, skeleton_name)
    blueprint = blueprint_from_skeleton(skeleton)
    text = _load_corpus(corpus_path, skeleton)
    stoi, _itos = _build_char_vocab(text, blueprint.vocab_size)
    token_ids = _encode(text, stoi)

    if len(token_ids) < seq_len + 2:
        token_ids = token_ids * ((seq_len + 2) // max(1, len(token_ids)) + 1)

    data = torch.tensor(token_ids, dtype=torch.long)
    model = build_pytorch_model(blueprint)
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    losses = []
    for _step in range(steps):
        starts = torch.randint(0, len(data) - seq_len - 1, (batch_size,))
        x = torch.stack([data[s : s + seq_len] for s in starts])
        y = torch.stack([data[s + 1 : s + seq_len + 1] for s in starts])

        logits = model(x)
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.item()))

    output_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = output_dir / "mini_transformer.pt"
    torch.save(model.state_dict(), ckpt_path)

    metrics = {
        "skeleton_name": blueprint.skeleton_name,
        "steps": steps,
        "batch_size": batch_size,
        "seq_len": seq_len,
        "final_loss": losses[-1],
        "min_loss": min(losses),
        "avg_loss": sum(losses) / len(losses),
        "blueprint": asdict(blueprint),
        "checkpoint": str(ckpt_path),
    }
    metrics_path = output_dir / "train_metrics.json"
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Train a mini-transformer from Mom4AI skeleton blueprint (MVP).")
    parser.add_argument("--ancestry-json", default="ancestry.json")
    parser.add_argument("--output-dir", default="outputs/mini_transformer")
    parser.add_argument("--skeleton-name", default=None)
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--seq-len", type=int, default=64)
    parser.add_argument("--lr", type=float, default=3e-4)
    args = parser.parse_args()

    metrics = train_once(
        ancestry_json=Path(args.ancestry_json),
        output_dir=Path(args.output_dir),
        skeleton_name=args.skeleton_name,
        corpus_path=Path(args.corpus) if args.corpus else None,
        steps=args.steps,
        batch_size=args.batch_size,
        seq_len=args.seq_len,
        lr=args.lr,
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
