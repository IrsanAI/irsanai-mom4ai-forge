from __future__ import annotations

import argparse
from typing import Dict

from runtime_adapter import build_event, send_event


def _token_set(text: str):
    return {t.strip(".,!?;:()[]{}\"'").lower() for t in text.split() if t.strip()}


def derive_turn_metrics(user_text: str, assistant_text: str) -> Dict[str, float]:
    """
    Heuristische Metriken für einen Turn (MVP),
    bis native Model-/Agent-Hooks strukturierte Scores liefern.
    """
    u = _token_set(user_text)
    a = _token_set(assistant_text)
    overlap = len(u & a) / max(1, len(u))

    # sehr einfache Proxy-Metriken im 0..1 Bereich
    intent_match = min(1.0, 0.45 + 0.55 * overlap)
    context_match = min(1.0, 0.40 + 0.60 * overlap)
    tone_match = 0.75 if assistant_text.strip().endswith((".", "!", "?")) else 0.6
    reliability = 0.8 if len(assistant_text.split()) >= 6 else 0.6
    coordination = min(1.0, (intent_match + context_match + reliability) / 3.0)

    return {
        "intent_match": float(max(0.0, intent_match)),
        "context_match": float(max(0.0, context_match)),
        "tone_match": float(max(0.0, tone_match)),
        "reliability": float(max(0.0, reliability)),
        "coordination": float(max(0.0, coordination)),
    }


def derive_runtime_semantics(
    tool_calls_total: int = 0,
    tool_calls_success: int = 0,
    recovery_success: float = 0.5,
    followup_consistency: float = 0.5,
) -> Dict[str, float]:
    tool_calls_total = max(0, int(tool_calls_total))
    tool_calls_success = max(0, int(tool_calls_success))
    if tool_calls_total == 0:
        tool_success_rate = 0.5
    else:
        tool_success_rate = min(1.0, tool_calls_success / max(1, tool_calls_total))

    recovery = max(0.0, min(1.0, float(recovery_success)))
    followup = max(0.0, min(1.0, float(followup_consistency)))
    semantic_quality = (tool_success_rate + recovery + followup) / 3.0
    return {
        "tool_success_rate": tool_success_rate,
        "recovery_success": recovery,
        "followup_consistency": followup,
        "semantic_quality": semantic_quality,
    }


def emit_turn_event(
    server_url: str,
    skeleton_name: str,
    session_id: str,
    user_text: str,
    assistant_text: str,
    actor_type: str = "agent",
    tool_calls_total: int = 0,
    tool_calls_success: int = 0,
    recovery_success: float = 0.5,
    followup_consistency: float = 0.5,
):
    metrics = derive_turn_metrics(user_text, assistant_text)
    semantics = derive_runtime_semantics(
        tool_calls_total=tool_calls_total,
        tool_calls_success=tool_calls_success,
        recovery_success=recovery_success,
        followup_consistency=followup_consistency,
    )
    # leichte Korrektur für Reliability/Coordination auf Basis Runtime-Semantik
    metrics["reliability"] = min(1.0, max(0.0, 0.7 * metrics["reliability"] + 0.3 * semantics["semantic_quality"]))
    metrics["coordination"] = min(1.0, max(0.0, 0.7 * metrics["coordination"] + 0.3 * semantics["followup_consistency"]))
    event = build_event(
        skeleton_name=skeleton_name,
        session_id=session_id,
        actor_type=actor_type,
        **metrics,
    )
    event.update(semantics)
    return send_event(server_url, event)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one heuristic OpenAI/Agent turn as resonance event.")
    parser.add_argument("--server", default="http://localhost:8080")
    parser.add_argument("--skeleton", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--user-text", required=True)
    parser.add_argument("--assistant-text", required=True)
    parser.add_argument("--actor", default="agent")
    parser.add_argument("--tool-calls-total", type=int, default=0)
    parser.add_argument("--tool-calls-success", type=int, default=0)
    parser.add_argument("--recovery-success", type=float, default=0.5)
    parser.add_argument("--followup-consistency", type=float, default=0.5)
    args = parser.parse_args()

    status, body = emit_turn_event(
        server_url=args.server,
        skeleton_name=args.skeleton,
        session_id=args.session,
        user_text=args.user_text,
        assistant_text=args.assistant_text,
        actor_type=args.actor,
        tool_calls_total=args.tool_calls_total,
        tool_calls_success=args.tool_calls_success,
        recovery_success=args.recovery_success,
        followup_consistency=args.followup_consistency,
    )
    print(f"status={status}")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
