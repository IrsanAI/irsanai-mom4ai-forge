# Assembly Compiler Contract (T01)

Dieser Contract definiert die minimale JSON-Struktur für den Schritt
**DAG-Skelett -> trainierbares Modellgerüst**.

## Pflichtfelder

- `name`: Name des Contracts
- `nodes`: Liste von Node-Objekten
- `edges`: Liste von Kanten `[from, to]`

### Node-Felder

- `id` (string, eindeutig)
- `in_dim` (int > 0)
- `out_dim` (int > 0)
- optional `op` (default: `linear`)
- optional `merge` (`sum` oder `concat`, default: `sum`)

## Validierungsregeln

- Graph muss DAG sein (keine Zyklen)
- Keine Self-Loops
- Kanten dürfen nur deklarierte Nodes referenzieren
- Mindestens ein Input- und ein Output-Node
- Nicht-Input-Nodes müssen Vorgänger haben

## CLI

```bash
python src/assembly_compiler.py --contract-json contract.json
```

oder nach `pip install -e .`:

```bash
momai-assembly-contract --contract-json contract.json
```
