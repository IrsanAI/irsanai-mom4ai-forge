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
from sdk_hooks import ResonanceSDKHook
from mini_transformer_adapter import blueprint_from_skeleton
from vendor_wiring import (
    auto_wire_turn,
    extract_anthropic_tool_stats,
    extract_anthropic_trace_metrics,
    extract_openai_trace_metrics,
    extract_tool_stats,
)


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


def test_sdk_hook_init():
    hook = ResonanceSDKHook(
        server_url="http://localhost:8080",
        skeleton_name="demo-skeleton",
        actor_type="agent",
    )
    assert hook.server_url.startswith("http")
    assert hook.skeleton_name == "demo-skeleton"


def test_vendor_wiring_extract_tool_stats():
    payload = {
        "choices": [
            {
                "message": {
                    "tool_calls": [
                        {"name": "search", "status": "success"},
                        {"name": "calc", "status": "failed"},
                    ]
                }
            }
        ]
    }
    total, success = extract_tool_stats(payload)
    assert total == 2
    assert success == 1


def test_vendor_wiring_trace_metrics():
    payload = {
        "usage": {"prompt_tokens": 50, "completion_tokens": 40},
        "choices": [{"finish_reason": "stop"}],
        "response_ms": 900,
    }
    metrics = extract_openai_trace_metrics(payload)
    assert metrics["prompt_tokens"] == 50
    assert metrics["completion_tokens"] == 40
    assert 0.0 <= metrics["recovery_success_inferred"] <= 1.0
    assert 0.0 <= metrics["followup_consistency_inferred"] <= 1.0


def test_vendor_wiring_anthropic_metrics():
    payload = {
        "content": [
            {"type": "text", "text": "Ich prüfe das."},
            {"type": "tool_use", "name": "search", "status": "success"},
            {"type": "tool_use", "name": "calc", "status": "failed"},
        ],
        "usage": {"input_tokens": 70, "output_tokens": 35},
        "stop_reason": "end_turn",
    }
    total, success = extract_anthropic_tool_stats(payload)
    assert total == 2
    assert success == 1

    metrics = extract_anthropic_trace_metrics(payload)
    assert metrics["prompt_tokens"] == 70
    assert metrics["completion_tokens"] == 35
    assert 0.0 <= metrics["recovery_success_inferred"] <= 1.0
    assert 0.0 <= metrics["followup_consistency_inferred"] <= 1.0


def test_vendor_wiring_auto_provider_detects_anthropic():
    class DummyHook:
        def on_turn(self, **kwargs):
            return 200, kwargs

    payload = {
        "content": [{"type": "tool_use", "name": "search", "status": "success"}],
        "usage": {"input_tokens": 100, "output_tokens": 20},
        "stop_reason": "end_turn",
    }
    _status, body = auto_wire_turn(
        hook=DummyHook(),
        session_id="s-1",
        user_text="u",
        assistant_text="a",
        response_payload=payload,
        provider="auto",
    )
    assert body["tool_calls_total"] == 1
    assert body["tool_calls_success"] == 1


def test_dashboard_index_html_present():
    index_html = ROOT / "docs" / "index.html"
    assert index_html.exists()
    content = index_html.read_text(encoding="utf-8")
    assert "Live Evolution" in content
    assert "loadHall()" in content
    assert "vis-network.min.js" in content
    assert "buildEvolutionTree" in content


def test_mini_transformer_blueprint_ranges():
    skeleton = {
        "name": "demo-mini-transformer",
        "generation": 2.5,
        "fitness": 0.41,
        "facts": {
            "nodes": 42,
            "density": 0.18,
            "modularity": 0.27,
            "feedback_loops": 4,
        },
    }
    bp = blueprint_from_skeleton(skeleton)
    assert bp.d_model % 32 == 0
    assert 2 <= bp.num_layers <= 12
    assert bp.d_model % bp.num_heads == 0
    assert 256 <= bp.max_seq_len <= 2048
    assert 0.05 <= bp.dropout <= 0.25


if __name__ == "__main__":
    test_validate_resonance_event()
    test_resonance_scoring_bounds()
    test_session_aggregation()
    test_runtime_adapter_event_builder()
    test_openai_hook_metric_bounds()
    test_openai_hook_runtime_semantics()
    test_sdk_hook_init()
    test_vendor_wiring_extract_tool_stats()
    test_vendor_wiring_trace_metrics()
    test_vendor_wiring_anthropic_metrics()
    test_vendor_wiring_auto_provider_detects_anthropic()
    test_dashboard_index_html_present()
    test_mini_transformer_blueprint_ranges()
    print("smoke tests passed")
