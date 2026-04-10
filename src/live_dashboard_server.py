"""Lokaler Hybrid-Server für die Mom4AI-Dashboard-Experience.

Primär ohne Docker nutzbar (python src/live_dashboard_server.py),
optional kann dasselbe `docs/` Verzeichnis in Docker/Nginx gemountet werden.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
ANCESTRY_FILE = ROOT / "ancestry.json"
USERS_FILE = ROOT / "users.json"
RESONANCE_EVENTS_FILE = ROOT / "resonance_events.jsonl"
RESONANCE_SESSIONS_FILE = ROOT / "resonance_sessions.json"


def _safe_load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback


def _collect_local_stats():
    ancestry = _safe_load_json(ANCESTRY_FILE, [])
    users = _safe_load_json(USERS_FILE, [])
    top5 = sorted(ancestry, key=lambda x: x.get("fitness", 0), reverse=True)[:5]
    resonance_counts = {
        "resonant": 0,
        "emerging": 0,
        "neutral": 0,
        "non_resonant": 0,
        "insufficient_data": 0,
        "no_data": 0,
    }

    for entry in ancestry:
        cls = entry.get("resonance_classification", "no_data")
        resonance_counts[cls] = resonance_counts.get(cls, 0) + 1

    return {
        "total_skeletons": len(ancestry),
        "total_users": len(users),
        "top5": [
            {
                "name": x.get("name"),
                "fitness": x.get("fitness", 0.0),
                "resonance_classification": x.get("resonance_classification", "no_data"),
            }
            for x in top5
        ],
        "resonance_counts": resonance_counts,
    }


def _git_sync_status():
    def run(cmd):
        try:
            return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()
        except Exception:
            return None

    head = run(["git", "rev-parse", "HEAD"])
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    remote = run(["git", "config", "--get", f"branch.{branch}.remote"]) if branch else None
    tracking = run(["git", "rev-parse", "--abbrev-ref", "@{u}"])
    dirty = bool(run(["git", "status", "--porcelain"]))
    return {
        "branch": branch,
        "head": head,
        "remote": remote,
        "tracking": tracking,
        "dirty_worktree": dirty,
    }


def _validate_resonance_event(event: dict):
    required = ["skeleton_name", "intent_match", "context_match", "tone_match", "reliability", "coordination"]
    missing = [k for k in required if k not in event]
    if missing:
        return False, f"missing fields: {', '.join(missing)}"
    metric_fields = ["intent_match", "context_match", "tone_match", "reliability", "coordination"]
    for field in metric_fields:
        try:
            value = float(event.get(field))
        except (TypeError, ValueError):
            return False, f"invalid metric '{field}': expected float in [0, 1]"
        if not math.isfinite(value):
            return False, f"invalid metric '{field}': must be finite"
        if value < 0.0 or value > 1.0:
            return False, f"invalid metric '{field}': expected float in [0, 1]"

    skeleton_name = str(event.get("skeleton_name", "")).strip()
    if not skeleton_name:
        return False, "invalid field 'skeleton_name': must be non-empty"
    return True, "ok"


def _append_resonance_event(event: dict):
    payload = dict(event)
    payload["skeleton_name"] = str(payload.get("skeleton_name", "")).strip()
    payload["session_id"] = str(payload.get("session_id") or "default-session").strip() or "default-session"
    payload["actor_type"] = str(payload.get("actor_type") or "agent").strip() or "agent"
    for key in ["intent_match", "context_match", "tone_match", "reliability", "coordination"]:
        payload[key] = float(payload.get(key, 0.0))
    payload.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
    with RESONANCE_EVENTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload


def _load_sessions():
    return _safe_load_json(RESONANCE_SESSIONS_FILE, {})


def _save_sessions(sessions: dict):
    with RESONANCE_SESSIONS_FILE.open("w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def _update_session_aggregate(event: dict):
    sessions = _load_sessions()
    session_id = str(event.get("session_id") or "default-session")
    skeleton_name = str(event.get("skeleton_name") or "unknown-skeleton")

    metrics = ["intent_match", "context_match", "tone_match", "reliability", "coordination"]
    record = sessions.get(
        session_id,
        {
            "session_id": session_id,
            "event_count": 0,
            "first_seen": event.get("timestamp"),
            "last_seen": event.get("timestamp"),
            "avg_intent_match": 0.0,
            "avg_context_match": 0.0,
            "avg_tone_match": 0.0,
            "avg_reliability": 0.0,
            "avg_coordination": 0.0,
            "last_skeleton_name": skeleton_name,
            "last_actor_type": event.get("actor_type", "unknown"),
        },
    )

    n = int(record.get("event_count", 0))
    for metric in metrics:
        key = f"avg_{metric}"
        prev_avg = float(record.get(key, 0.0))
        current = float(event.get(metric, 0.0))
        record[key] = ((prev_avg * n) + current) / (n + 1)

    record["event_count"] = n + 1
    record["last_seen"] = event.get("timestamp")
    record["last_skeleton_name"] = skeleton_name
    record["last_actor_type"] = event.get("actor_type", "unknown")

    # Session-level resonance (gleich gewichtet)
    record["session_resonance"] = (
        record["avg_intent_match"]
        + record["avg_context_match"]
        + record["avg_tone_match"]
        + record["avg_reliability"]
        + record["avg_coordination"]
    ) / 5.0

    sessions[session_id] = record
    _save_sessions(sessions)
    return record


def _session_snapshot():
    sessions = list(_load_sessions().values())
    sessions.sort(key=lambda x: x.get("session_resonance", 0.0), reverse=True)
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_count": len(sessions),
        "top_session": sessions[0] if sessions else None,
    }


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.md"):
            self.path = "/index.html"
            super().do_GET()
            return
        if parsed.path == "/api/local_stats":
            self._send_json(_collect_local_stats())
            return
        if parsed.path == "/api/sync_status":
            self._send_json(_git_sync_status())
            return
        if parsed.path == "/api/session_summary":
            query = parse_qs(parsed.query)
            sessions = _load_sessions()
            session_id = query.get("session_id", [None])[0]
            if session_id:
                self._send_json(sessions.get(session_id, {"error": "session_not_found"}))
            else:
                self._send_json({"sessions": list(sessions.values())})
            return
        if parsed.path == "/api/session_stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            try:
                # einfacher SSE stream, liefert kontinuierliche Session-Snapshots
                for _ in range(180):  # ca. 6 Minuten bei 2s Intervall
                    payload = json.dumps(_session_snapshot(), ensure_ascii=False)
                    self.wfile.write(f"event: session\n".encode("utf-8"))
                    self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(2.0)
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/resonance_event":
            self._send_json({"error": "not found"}, status=404)
            return

        try:
            content_len = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(content_len) if content_len > 0 else b"{}"
            event = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            self._send_json({"error": f"invalid_json: {exc}"}, status=400)
            return

        ok, msg = _validate_resonance_event(event)
        if not ok:
            self._send_json({"error": msg}, status=400)
            return

        stored = _append_resonance_event(event)
        session = _update_session_aggregate(stored)
        self._send_json({"status": "ok", "stored": stored, "session": session}, status=201)


def main():
    host = os.getenv("MOM_DASHBOARD_HOST", "127.0.0.1")
    port = int(os.getenv("MOM_DASHBOARD_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"🚀 Mom4AI Dashboard läuft auf http://{host}:{port}")
    print("   Endpoints: /api/local_stats, /api/sync_status, /api/session_summary, /api/session_stream, POST /api/resonance_event")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server gestoppt.")


if __name__ == "__main__":
    main()
