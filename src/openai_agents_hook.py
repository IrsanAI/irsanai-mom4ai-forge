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


def emit_turn_event(
    server_url: str,
    skeleton_name: str,
    session_id: str,
    user_text: str,
    assistant_text: str,
    actor_type: str = "agent",
):
    metrics = derive_turn_metrics(user_text, assistant_text)
    event = build_event(
        skeleton_name=skeleton_name,
        session_id=session_id,
        actor_type=actor_type,
        **metrics,
    )
    return send_event(server_url, event)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one heuristic OpenAI/Agent turn as resonance event.")
    parser.add_argument("--server", default="http://localhost:8080")
    parser.add_argument("--skeleton", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--user-text", required=True)
    parser.add_argument("--assistant-text", required=True)
    parser.add_argument("--actor", default="agent")
    args = parser.parse_args()

    status, body = emit_turn_event(
        server_url=args.server,
        skeleton_name=args.skeleton,
        session_id=args.session,
        user_text=args.user_text,
        assistant_text=args.assistant_text,
        actor_type=args.actor,
    )
    print(f"status={status}")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
