from __future__ import annotations

import argparse
import json
from typing import Any, Dict, Tuple

from sdk_hooks import ResonanceSDKHook


def _safe_get(obj: Any, key: str, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def extract_tool_stats(openai_like_response: Any) -> Tuple[int, int]:
    """
    Extrahiert Tool-Call-Stats aus dict-/objektähnlichen OpenAI-Responses.
    Unterstützt MVP-Formate.
    """
    tool_calls = _safe_get(openai_like_response, "tool_calls", None)
    if tool_calls is None:
        # manche payloads legen es unter choices[0].message.tool_calls ab
        choices = _safe_get(openai_like_response, "choices", [])
        if choices:
            first = choices[0]
            message = _safe_get(first, "message", {})
            tool_calls = _safe_get(message, "tool_calls", [])
    tool_calls = tool_calls or []

    total = len(tool_calls)
    success = 0
    for tc in tool_calls:
        status = _safe_get(tc, "status", "success")
        if str(status).lower() in ("success", "ok", "done"):
            success += 1
    return total, success


def extract_openai_trace_metrics(openai_like_response: Any) -> Dict[str, float]:
    usage = _safe_get(openai_like_response, "usage", {}) or {}
    prompt_tokens = float(_safe_get(usage, "prompt_tokens", 0) or 0)
    completion_tokens = float(_safe_get(usage, "completion_tokens", 0) or 0)

    choices = _safe_get(openai_like_response, "choices", []) or []
    finish_reason = "stop"
    if choices:
        finish_reason = str(_safe_get(choices[0], "finish_reason", "stop"))

    # optionale Laufzeitdaten, falls vorhanden
    response_ms = float(_safe_get(openai_like_response, "response_ms", 0) or 0)

    # heuristische Ableitung für Recovery/Follow-up
    recovery_success = 0.9 if finish_reason in ("stop", "tool_calls") else 0.55
    if completion_tokens <= 0:
        followup_consistency = 0.45
    else:
        ratio = completion_tokens / max(1.0, prompt_tokens)
        followup_consistency = max(0.4, min(0.95, 0.6 + 0.25 * min(1.0, ratio)))

    if response_ms > 0 and response_ms > 12000:
        followup_consistency = max(0.35, followup_consistency - 0.1)

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "finish_reason_score": 1.0 if finish_reason in ("stop", "tool_calls") else 0.55,
        "response_ms": response_ms,
        "recovery_success_inferred": recovery_success,
        "followup_consistency_inferred": followup_consistency,
    }


def auto_wire_openai_turn(
    hook: ResonanceSDKHook,
    session_id: str,
    user_text: str,
    assistant_text: str,
    openai_like_response: Any,
    recovery_success: float | None = None,
    followup_consistency: float | None = None,
):
    total, success = extract_tool_stats(openai_like_response)
    trace = extract_openai_trace_metrics(openai_like_response)
    if recovery_success is None:
        recovery_success = trace["recovery_success_inferred"]
    if followup_consistency is None:
        followup_consistency = trace["followup_consistency_inferred"]
    return hook.on_turn(
        session_id=session_id,
        user_text=user_text,
        assistant_text=assistant_text,
        tool_calls_total=total,
        tool_calls_success=success,
        recovery_success=recovery_success,
        followup_consistency=followup_consistency,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Vendor wiring demo for OpenAI-like response payloads.")
    parser.add_argument("--server", default="http://localhost:8080")
    parser.add_argument("--skeleton", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--user-text", required=True)
    parser.add_argument("--assistant-text", required=True)
    parser.add_argument("--response-json", required=True, help="Path to OpenAI-like response JSON")
    parser.add_argument("--recovery-success", type=float, default=None)
    parser.add_argument("--followup-consistency", type=float, default=None)
    args = parser.parse_args()

    with open(args.response_json, "r", encoding="utf-8") as f:
        payload = json.load(f)

    hook = ResonanceSDKHook(args.server, args.skeleton)
    status, body = auto_wire_openai_turn(
        hook=hook,
        session_id=args.session,
        user_text=args.user_text,
        assistant_text=args.assistant_text,
        openai_like_response=payload,
        recovery_success=args.recovery_success,
        followup_consistency=args.followup_consistency,
    )
    print(f"status={status}")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
