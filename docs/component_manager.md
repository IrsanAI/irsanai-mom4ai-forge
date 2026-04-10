# Component Manager

Der `component_manager` erweitert MomAI um eine strukturierte Komponentenverwaltung:

- **Katalogisierung** aller `BIO_COMPONENTS`
- **Auto-Kategorisierung** (z. B. `tier_schwarm`, `oekosystem`, `human_system`)
- **Auto-Lokalisierung** (DE/EN Labels)
- **Vorschläge** für neue, sinnvolle Komponenten für zukünftige Evolutionsrunden

## CLI

```bash
python src/component_manager.py --output docs/component_registry.json --suggest 8 --print-roadmap-snippet
```

oder nach `pip install -e .`:

```bash
momai-components --output docs/component_registry.json --suggest 8
```

## Output

`docs/component_registry.json` enthält:

- `summary`: Anzahl, Kategorien, Mittelwerte
- `underrepresented_categories`: Kategorien mit Ausbaupotenzial (für priorisierte Erweiterung)
- `components`: vollständige registrierte Komponentenliste
- `suggestions`: noch nicht integrierte Kandidaten
