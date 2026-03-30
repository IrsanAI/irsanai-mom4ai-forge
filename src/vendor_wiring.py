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


def auto_wire_openai_turn(
    hook: ResonanceSDKHook,
    session_id: str,
    user_text: str,
    assistant_text: str,
    openai_like_response: Any,
    recovery_success: float = 0.5,
    followup_consistency: float = 0.5,
):
    total, success = extract_tool_stats(openai_like_response)
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
    )
    print(f"status={status}")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
