from __future__ import annotations

import argparse
from typing import Optional

from openai_agents_hook import emit_turn_event


class ResonanceSDKHook:
    """
    Lightweight SDK hook bridge:
    - accepts runtime turn data
    - derives resonance metrics automatically
    - emits event to local MomAI server
    """

    def __init__(self, server_url: str, skeleton_name: str, actor_type: str = "agent"):
        self.server_url = server_url
        self.skeleton_name = skeleton_name
        self.actor_type = actor_type

    def on_turn(
        self,
        session_id: str,
        user_text: str,
        assistant_text: str,
        tool_calls_total: int = 0,
        tool_calls_success: int = 0,
        recovery_success: float = 0.5,
        followup_consistency: float = 0.5,
    ):
        return emit_turn_event(
            server_url=self.server_url,
            skeleton_name=self.skeleton_name,
            session_id=session_id,
            user_text=user_text,
            assistant_text=assistant_text,
            actor_type=self.actor_type,
            tool_calls_total=tool_calls_total,
            tool_calls_success=tool_calls_success,
            recovery_success=recovery_success,
            followup_consistency=followup_consistency,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="SDK-style hook demo (no manual resonance metrics).")
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

    hook = ResonanceSDKHook(args.server, args.skeleton, actor_type=args.actor)
    status, body = hook.on_turn(
        session_id=args.session,
        user_text=args.user_text,
        assistant_text=args.assistant_text,
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
