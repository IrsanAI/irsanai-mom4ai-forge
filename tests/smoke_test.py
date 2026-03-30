from __future__ import annotations

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import live_dashboard_server as lds
from live_dashboard_server import _validate_resonance_event
from resonance_protocol import score_interactions
from runtime_adapter import build_event
from openai_agents_hook import derive_turn_metrics, derive_runtime_semantics


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


def test_runtime_adapter_event_builder():
    event = build_event(
        skeleton_name="demo-skeleton",
        session_id="demo-session",
        intent_match=0.9,
        context_match=0.8,
        tone_match=0.7,
        reliability=0.6,
        coordination=0.75,
        actor_type="agent",
    )
    assert event["skeleton_name"] == "demo-skeleton"
    assert event["session_id"] == "demo-session"
    assert 0.0 <= event["intent_match"] <= 1.0
    assert "timestamp" in event


def test_openai_hook_metric_bounds():
    m = derive_turn_metrics(
        user_text="Bitte gib mir einen Plan für diese Woche.",
        assistant_text="Gerne! Hier ist ein strukturierter Wochenplan mit Prioritäten."
    )
    for key in ["intent_match", "context_match", "tone_match", "reliability", "coordination"]:
        assert 0.0 <= m[key] <= 1.0


def test_openai_hook_runtime_semantics():
    s = derive_runtime_semantics(
        tool_calls_total=4,
        tool_calls_success=3,
        recovery_success=0.9,
        followup_consistency=0.8,
    )
    for key in ["tool_success_rate", "recovery_success", "followup_consistency", "semantic_quality"]:
        assert 0.0 <= s[key] <= 1.0


if __name__ == "__main__":
    test_validate_resonance_event()
    test_resonance_scoring_bounds()
    test_session_aggregation()
    test_runtime_adapter_event_builder()
    test_openai_hook_metric_bounds()
    test_openai_hook_runtime_semantics()
    print("smoke tests passed")
