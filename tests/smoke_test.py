from __future__ import annotations

import json
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
from mini_transformer_adapter import blueprint_from_skeleton, build_pytorch_model
from mini_transformer_trainer import train_once
from resonance_lifecycle import evaluate_skeleton_lifecycle
from benchmark_runner import build_benchmark_report
from quality_gates import evaluate_gates
from chemie_manager import build_portfolio_report, parse_roadmap_from_readme
from readme_sync_manager import build_sync_report
import release_guard as rg
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

    out_of_range_ok, out_of_range_msg = _validate_resonance_event(
        {
            "skeleton_name": "demo",
            "intent_match": 1.1,
            "context_match": 0.8,
            "tone_match": 0.7,
            "reliability": 0.6,
            "coordination": 0.75,
        }
    )
    assert not out_of_range_ok and "expected float in [0, 1]" in out_of_range_msg

    non_finite_ok, non_finite_msg = _validate_resonance_event(
        {
            "skeleton_name": "demo",
            "intent_match": float("nan"),
            "context_match": 0.8,
            "tone_match": 0.7,
            "reliability": 0.6,
            "coordination": 0.75,
        }
    )
    assert not non_finite_ok and "must be finite" in non_finite_msg

    empty_name_ok, empty_name_msg = _validate_resonance_event(
        {
            "skeleton_name": "   ",
            "intent_match": 0.9,
            "context_match": 0.8,
            "tone_match": 0.7,
            "reliability": 0.6,
            "coordination": 0.75,
        }
    )
    assert not empty_name_ok and "non-empty" in empty_name_msg


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


def test_append_event_normalizes_defaults():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        lds.RESONANCE_EVENTS_FILE = tmp_path / "events.jsonl"
        event = {
            "skeleton_name": "  demo-name  ",
            "intent_match": "0.9",
            "context_match": 0.8,
            "tone_match": 0.7,
            "reliability": 0.6,
            "coordination": 0.75,
            "session_id": "   ",
            "actor_type": "   ",
        }
        stored = lds._append_resonance_event(event)
        assert stored["skeleton_name"] == "demo-name"
        assert stored["session_id"] == "default-session"
        assert stored["actor_type"] == "agent"
        assert isinstance(stored["intent_match"], float)


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


def test_mini_transformer_model_forward():
    try:
        import torch
    except Exception:
        return

    bp = blueprint_from_skeleton(
        {
            "name": "forward-test",
            "generation": 1.0,
            "fitness": 0.5,
            "facts": {"nodes": 16, "density": 0.1, "modularity": 0.2, "feedback_loops": 2},
        }
    )
    model = build_pytorch_model(bp)
    x = torch.randint(0, bp.vocab_size, (2, 12), dtype=torch.long)
    y = model(x)
    assert tuple(y.shape) == (2, 12, bp.vocab_size)


def test_mini_transformer_training_mvp_runs():
    try:
        import torch  # noqa: F401
    except Exception:
        return

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "mt"
        metrics = train_once(
            ancestry_json=ROOT / "ancestry.json",
            output_dir=out,
            steps=1,
            batch_size=2,
            seq_len=8,
        )
        assert metrics["steps"] == 1
        assert (out / "mini_transformer.pt").exists()
        assert (out / "train_metrics.json").exists()


def test_chemie_manager_report_generation():
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    items = parse_roadmap_from_readme(readme_text)
    assert len(items) >= 5

    report = build_portfolio_report(items)
    assert report.total_items >= report.completed_items
    assert report.open_items >= 0
    assert 0.0 <= report.completion_rate <= 1.0
    assert isinstance(report.optimization_plan, list) and report.optimization_plan


def test_readme_sync_manager_status():
    report = build_sync_report(ROOT / "README.md", ROOT / "README.en.md")
    assert report.context_delta_score >= 0
    assert report.status == "up_to_date"


def test_resonance_lifecycle_states():
    events = [
        {
            "skeleton_name": "demo-a",
            "session_id": "s1",
            "intent_match": 0.9,
            "context_match": 0.85,
            "tone_match": 0.8,
            "reliability": 0.82,
            "coordination": 0.88,
            "timestamp": "2026-04-03T00:00:00Z",
        }
    ]
    report = evaluate_skeleton_lifecycle(events)
    assert report.state in {"thriving", "alive", "dormant", "reconnecting", "extinct"}
    assert report.event_count == 1


def test_mom_forge_pages_ancestry_sync_present():
    source = (ROOT / "src" / "mom_forge.py").read_text(encoding="utf-8")
    assert "docs/ancestry.json" in source
    assert "git\", \"add\", \"ancestry.json\", \"docs/ancestry.json\"" in source


def test_benchmark_and_quality_gates():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        ancestry_path = tmp_path / "ancestry.json"
        ancestry_path.write_text(
            json.dumps(
                [
                    {"fitness": 0.4, "facts": {"dominant_type": "myzel_netz"}, "resonance_classification": "no_data"},
                    {"fitness": 0.2, "facts": {"dominant_type": "ameisen_schwarm"}, "resonance_classification": "no_data"},
                ]
            ),
            encoding="utf-8",
        )
        readme_sync_path = tmp_path / "readme_sync_report.json"
        readme_sync_path.write_text(json.dumps({"status": "up_to_date", "context_delta_score": 0}), encoding="utf-8")
        lifecycle_path = tmp_path / "lifecycle.json"
        lifecycle_path.write_text(json.dumps({"population_size": 0, "state_counts": {}}), encoding="utf-8")

        report = build_benchmark_report(
            ancestry_path=ancestry_path,
            resonance_events_path=tmp_path / "events.jsonl",
            readme_sync_report_path=readme_sync_path,
            lifecycle_report_path=lifecycle_path,
        )
        gates = evaluate_gates(report)
        assert report["kpis"]["total_skeletons"] == 2
        assert any(g.name == "context_delta_zero" and g.passed for g in gates)


def test_release_guard_report_contracts():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        docs = tmp_root / "docs"
        docs.mkdir(parents=True, exist_ok=True)

        (docs / "readme_sync_report.json").write_text(
            json.dumps({"status": "up_to_date", "context_delta_score": 0}),
            encoding="utf-8",
        )
        (docs / "benchmark_report.json").write_text(
            json.dumps({"kpis": {}, "integrity": {}}),
            encoding="utf-8",
        )
        (docs / "quality_gates_report.json").write_text(
            json.dumps({"passed": True, "gates": []}),
            encoding="utf-8",
        )
        (docs / "resonance_lifecycle_report.json").write_text(
            json.dumps({"population_size": 0, "state_counts": {}, "skeletons": []}),
            encoding="utf-8",
        )

        old_root = rg.ROOT
        rg.ROOT = tmp_root
        try:
            ok, problems = rg.check_report_contracts()
            assert ok, problems

            (docs / "benchmark_report.json").write_text(json.dumps({"kpis": {}}), encoding="utf-8")
            ok2, problems2 = rg.check_report_contracts()
            assert not ok2
            assert any("missing keys" in p for p in problems2)
        finally:
            rg.ROOT = old_root


if __name__ == "__main__":
    test_validate_resonance_event()
    test_resonance_scoring_bounds()
    test_session_aggregation()
    test_append_event_normalizes_defaults()
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
    test_mini_transformer_model_forward()
    test_mini_transformer_training_mvp_runs()
    test_chemie_manager_report_generation()
    test_readme_sync_manager_status()
    test_resonance_lifecycle_states()
    test_mom_forge_pages_ancestry_sync_present()
    test_benchmark_and_quality_gates()
    test_release_guard_report_contracts()
    print("smoke tests passed")
