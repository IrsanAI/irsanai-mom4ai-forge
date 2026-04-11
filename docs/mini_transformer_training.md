# Mini-Transformer Training (MVP)

Mit `mini_transformer_trainer.py` kann aus einem Skeleton-Blueprint ein kleines
trainierbares Transformer-LM trainiert werden.

## Was passiert?

1. Skeleton aus `ancestry.json` wählen (top fitness oder `--skeleton-name`)
2. Blueprint aus `mini_transformer_adapter` ableiten
3. Char-Level Korpus laden (Datei oder fallback synthetic corpus)
4. Next-token Training (cross entropy) für definierte Steps
5. Checkpoint + `train_metrics.json` speichern

## CLI

```bash
momai-mini-train \
  --ancestry-json ./ancestry.json \
  --output-dir ./outputs/mini_transformer \
  --steps 60 \
  --batch-size 8 \
  --seq-len 64
```

Optional:

```bash
--skeleton-name "MySkeleton-123"
--corpus ./my_corpus.txt
--lr 0.0003
```

## Output

- `outputs/mini_transformer/mini_transformer.pt`
- `outputs/mini_transformer/train_metrics.json`
