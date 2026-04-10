from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    v = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(v)
    except ValueError:
        return None


def _avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


@dataclass
class SkeletonLifecycle:
    skeleton_name: str
    event_count: int
    unique_sessions: int
    last_seen: str | None
    avg_resonance: float
    state: str
    rationale: str


def evaluate_skeleton_lifecycle(events: List[Dict[str, Any]], now: datetime | None = None) -> SkeletonLifecycle:
    now = now or datetime.now(timezone.utc)
    name = str(events[0].get("skeleton_name") if events else "unknown")

    scores = []
    sessions = set()
    timestamps = []
    for ev in events:
        scores.append(
            _avg(
                [
                    float(ev.get("intent_match", 0.0)),
                    float(ev.get("context_match", 0.0)),
                    float(ev.get("tone_match", 0.0)),
                    float(ev.get("reliability", 0.0)),
                    float(ev.get("coordination", 0.0)),
                ]
            )
        )
        sessions.add(str(ev.get("session_id", "default")))
        ts = _parse_ts(ev.get("timestamp"))
        if ts:
            timestamps.append(ts.astimezone(timezone.utc))

    avg_resonance = round(_avg(scores), 4)
    last_seen_dt = max(timestamps) if timestamps else None
    last_seen = last_seen_dt.isoformat().replace("+00:00", "Z") if last_seen_dt else None

    if not events:
        state = "extinct"
        rationale = "No resonance events yet."
    else:
        days_since_seen = (now - last_seen_dt).days if last_seen_dt else 999
        if avg_resonance >= 0.78 and days_since_seen <= 7:
            state = "thriving"
            rationale = "High resonance + recent activity."
        elif avg_resonance >= 0.62 and days_since_seen <= 21:
            state = "alive"
            rationale = "Stable resonance and still active."
        elif avg_resonance >= 0.5 and days_since_seen <= 45:
            state = "dormant"
            rationale = "Moderate resonance, low recent activity."
        elif avg_resonance >= 0.62 and days_since_seen > 45:
            state = "reconnecting"
            rationale = "Good historical resonance but currently inactive."
        else:
            state = "extinct"
            rationale = "Low resonance and/or long inactivity."

    return SkeletonLifecycle(
        skeleton_name=name,
        event_count=len(events),
        unique_sessions=len(sessions),
        last_seen=last_seen,
        avg_resonance=avg_resonance,
        state=state,
        rationale=rationale,
    )


def build_population_lifecycle(events_file: Path) -> Dict[str, Any]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    if events_file.exists():
        for line in events_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = str(ev.get("skeleton_name", "unknown"))
            grouped.setdefault(key, []).append(ev)

    reports = [evaluate_skeleton_lifecycle(events) for _name, events in grouped.items()]
    reports.sort(key=lambda x: (x.state, x.avg_resonance), reverse=True)

    state_counts: Dict[str, int] = {}
    for rep in reports:
        state_counts[rep.state] = state_counts.get(rep.state, 0) + 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "population_size": len(reports),
        "state_counts": state_counts,
        "skeletons": [asdict(x) for x in reports],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate resonance lifecycle states for skeleton survival.")
    parser.add_argument("--events-file", default="resonance_events.jsonl")
    parser.add_argument("--output", default="docs/resonance_lifecycle_report.json")
    args = parser.parse_args()

    payload = build_population_lifecycle(Path(args.events_file))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
