# Quality Gates

Prüft Benchmark-KPIs gegen Mindestkriterien (Repo-Hardening).

## CLI

```bash
python src/quality_gates.py \
  --report docs/benchmark_report.json \
  --output docs/quality_gates_report.json
```

## Aktuelle Gates

- `total_skeletons_min >= 30`
- `avg_fitness_min >= 0.20`
- `readme_sync_up_to_date`
- `context_delta_zero`
