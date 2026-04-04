# Mini-Transformer Adapter (Roadmap-Vorstufe)

`mini_transformer_adapter.py` erzeugt aus einem Hall-of-Fame Skeleton ein
**trainingsnahes Transformer-Blueprint** (Konfigurationsentwurf), das später für
Assembly-/Training-Pipelines genutzt werden kann.

## Was das Modul macht

- liest ein Skeleton aus `ancestry.json` (optional per Name)
- leitet Modellparameter heuristisch ab:
  - `d_model`
  - `num_layers`
  - `num_heads`
  - `ffn_dim`
  - `dropout`
  - `max_seq_len`
- kann optional ein PyTorch-Modell instanziieren und Parameteranzahl ausgeben

## CLI

```bash
momai-mini-transformer \
  --ancestry-json ./ancestry.json \
  --skeleton-name "MyzelAmeisen-G2-11-ab12cd34" \
  --output ./mini_transformer_blueprint.json
```

Optional mit Modellinstanz:

```bash
momai-mini-transformer --with-model-stats
```

## Hinweis

Das ist bewusst eine **Roadmap-Vorstufe** für den Punkt
„Mini-Transformer aus Graph-Skeletten“:
- heute: Blueprint-Generierung
- später: tatsächliches Training, Tokenizer/Datapipeline, Evaluation
