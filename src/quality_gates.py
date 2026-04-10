from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str


def evaluate_gates(report: Dict) -> List[GateResult]:
    kpis = report.get("kpis", {})
    integrity = report.get("integrity", {})
    readme_delta = integrity.get("readme_context_delta", None)
    if readme_delta is None:
        readme_delta = 999

    gates = [
        GateResult(
            name="total_skeletons_min",
            passed=float(kpis.get("total_skeletons", 0)) >= 30,
            detail=f"total_skeletons={kpis.get('total_skeletons', 0)} (min=30)",
        ),
        GateResult(
            name="avg_fitness_min",
            passed=float(kpis.get("avg_fitness", 0.0)) >= 0.20,
            detail=f"avg_fitness={kpis.get('avg_fitness', 0.0)} (min=0.20)",
        ),
        GateResult(
            name="readme_sync_up_to_date",
            passed=str(integrity.get("readme_sync_status", "unknown")) == "up_to_date",
            detail=f"readme_sync_status={integrity.get('readme_sync_status', 'unknown')}",
        ),
        GateResult(
            name="context_delta_zero",
            passed=float(readme_delta) == 0,
            detail=f"readme_context_delta={readme_delta}",
        ),
    ]
    return gates


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate quality gates from benchmark report.")
    parser.add_argument("--report", default="docs/benchmark_report.json")
    parser.add_argument("--output", default="docs/quality_gates_report.json")
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    results = evaluate_gates(report)

    payload = {
        "passed": all(x.passed for x in results),
        "gates": [asdict(x) for x in results],
    }

    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
