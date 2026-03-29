from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

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


if __name__ == "__main__":
    test_validate_resonance_event()
    test_resonance_scoring_bounds()
    print("smoke tests passed")
