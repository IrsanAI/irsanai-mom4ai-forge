from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def _safe_load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def _safe_load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def build_benchmark_report(
    ancestry_path: Path,
    resonance_events_path: Path,
    readme_sync_report_path: Path,
    lifecycle_report_path: Path,
) -> Dict[str, Any]:
    ancestry = _safe_load_json(ancestry_path, [])
    events = _safe_load_jsonl(resonance_events_path)
    readme_sync = _safe_load_json(readme_sync_report_path, {"status": "unknown"})
    lifecycle = _safe_load_json(lifecycle_report_path, {"population_size": 0, "state_counts": {}})

    fitness_values = [float(x.get("fitness", 0.0) or 0.0) for x in ancestry]
    top10 = sorted(fitness_values, reverse=True)[:10]
    dominant_types = [
        (x.get("facts", {}) or {}).get("dominant_type", "unknown")
        for x in ancestry
    ]
    dom_counter = Counter(dominant_types)

    resonance_class_counts = Counter(
        [x.get("resonance_classification", "no_data") for x in ancestry]
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "kpis": {
            "total_skeletons": len(ancestry),
            "avg_fitness": round(sum(fitness_values) / len(fitness_values), 4) if fitness_values else 0.0,
            "top10_avg_fitness": round(sum(top10) / len(top10), 4) if top10 else 0.0,
            "resonance_event_count": len(events),
            "resonance_coverage_ratio": round(
                1.0 - (resonance_class_counts.get("no_data", 0) / max(1, len(ancestry))),
                4,
            ),
            "dominant_type_diversity": len({x for x in dominant_types if x != "unknown"}),
        },
        "distribution": {
            "dominant_types": dom_counter,
            "resonance_classes": resonance_class_counts,
        },
        "integrity": {
            "readme_sync_status": readme_sync.get("status", "unknown"),
            "readme_context_delta": readme_sync.get("context_delta_score", None),
            "lifecycle_population": lifecycle.get("population_size", 0),
            "lifecycle_states": lifecycle.get("state_counts", {}),
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build benchmark KPI report for Mom4AI Forge.")
    parser.add_argument("--ancestry", default="ancestry.json")
    parser.add_argument("--events", default="resonance_events.jsonl")
    parser.add_argument("--readme-sync", default="docs/readme_sync_report.json")
    parser.add_argument("--lifecycle", default="docs/resonance_lifecycle_report.json")
    parser.add_argument("--output", default="docs/benchmark_report.json")
    args = parser.parse_args()

    report = build_benchmark_report(
        ancestry_path=Path(args.ancestry),
        resonance_events_path=Path(args.events),
        readme_sync_report_path=Path(args.readme_sync),
        lifecycle_report_path=Path(args.lifecycle),
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
