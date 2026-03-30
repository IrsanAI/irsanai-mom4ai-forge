from __future__ import annotations

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import live_dashboard_server as lds
from live_dashboard_server import _validate_resonance_event
from resonance_protocol import score_interactions


def test_validate_resonance_event():
    valid = {
        "skeleton_name": "demo",
        "intent_match": 0.9,
        "context_match": 0.8,
        "tone_match": 0.7,
        "reliability": 0.6,
        "coordination": 0.75,
    }
    ok, msg = _validate_resonance_event(valid)
    assert ok, msg

    missing_ok, missing_msg = _validate_resonance_event({"skeleton_name": "x"})
    assert not missing_ok and "missing fields" in missing_msg


def test_resonance_scoring_bounds():
    result = score_interactions(
        [
            {
                "intent_match": 0.9,
                "context_match": 0.8,
                "tone_match": 0.7,
                "reliability": 0.85,
                "coordination": 0.9,
            },
            {
                "intent_match": 0.8,
                "context_match": 0.7,
                "tone_match": 0.6,
                "reliability": 0.75,
                "coordination": 0.8,
            },
        ]
    )
    assert 0.0 <= result.score <= 1.0
    assert 0.0 <= result.connection <= 1.0
    assert 0.0 <= result.coordination <= 1.0


def test_session_aggregation():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        lds.RESONANCE_SESSIONS_FILE = tmp_path / "sessions.json"
        lds.RESONANCE_EVENTS_FILE = tmp_path / "events.jsonl"
        event = {
            "session_id": "chat-42",
            "skeleton_name": "demo",
            "intent_match": 0.9,
            "context_match": 0.8,
            "tone_match": 0.7,
            "reliability": 0.6,
            "coordination": 0.75,
            "timestamp": "2026-03-29T00:00:00Z",
        }
        lds._append_resonance_event(event)
        s1 = lds._update_session_aggregate(event)
        assert s1["event_count"] == 1
        assert 0.0 <= s1["session_resonance"] <= 1.0

        event2 = dict(event)
        event2["intent_match"] = 0.5
        s2 = lds._update_session_aggregate(event2)
        assert s2["event_count"] == 2
        assert s2["session_resonance"] != s1["session_resonance"]
        snap = lds._session_snapshot()
        assert snap["session_count"] == 1
        assert snap["top_session"]["session_id"] == "chat-42"


if __name__ == "__main__":
    test_validate_resonance_event()
    test_resonance_scoring_bounds()
    test_session_aggregation()
    print("smoke tests passed")
