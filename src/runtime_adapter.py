from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime


def build_event(
    skeleton_name: str,
    session_id: str,
    intent_match: float,
    context_match: float,
    tone_match: float,
    reliability: float,
    coordination: float,
    actor_type: str = "agent",
):
    return {
        "skeleton_name": skeleton_name,
        "session_id": session_id,
        "intent_match": float(intent_match),
        "context_match": float(context_match),
        "tone_match": float(tone_match),
        "reliability": float(reliability),
        "coordination": float(coordination),
        "actor_type": actor_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def send_event(server_url: str, event: dict):
    payload = json.dumps(event).encode("utf-8")
    req = urllib.request.Request(
        server_url.rstrip("/") + "/api/resonance_event",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="MomAI runtime adapter: send resonance events to local server.")
    parser.add_argument("--server", default="http://localhost:8080")
    parser.add_argument("--skeleton", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--intent", type=float, required=True)
    parser.add_argument("--context", type=float, required=True)
    parser.add_argument("--tone", type=float, required=True)
    parser.add_argument("--reliability", type=float, required=True)
    parser.add_argument("--coordination", type=float, required=True)
    parser.add_argument("--actor", default="agent")
    args = parser.parse_args()

    event = build_event(
        skeleton_name=args.skeleton,
        session_id=args.session,
        intent_match=args.intent,
        context_match=args.context,
        tone_match=args.tone,
        reliability=args.reliability,
        coordination=args.coordination,
        actor_type=args.actor,
    )
    status, body = send_event(args.server, event)
    print(f"status={status}")
    print(json.dumps(body, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
