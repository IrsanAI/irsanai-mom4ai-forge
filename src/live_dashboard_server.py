"""Lokaler Hybrid-Server für die Mom4AI-Dashboard-Experience.

Primär ohne Docker nutzbar (python src/live_dashboard_server.py),
optional kann dasselbe `docs/` Verzeichnis in Docker/Nginx gemountet werden.
"""

from __future__ import annotations

import json
import os
import subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
ANCESTRY_FILE = ROOT / "ancestry.json"
USERS_FILE = ROOT / "users.json"
RESONANCE_EVENTS_FILE = ROOT / "resonance_events.jsonl"


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
    return True, "ok"


def _append_resonance_event(event: dict):
    payload = dict(event)
    payload.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
    with RESONANCE_EVENTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload


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
        if parsed.path == "/api/local_stats":
            self._send_json(_collect_local_stats())
            return
        if parsed.path == "/api/sync_status":
            self._send_json(_git_sync_status())
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
        self._send_json({"status": "ok", "stored": stored}, status=201)


def main():
    host = os.getenv("MOM_DASHBOARD_HOST", "127.0.0.1")
    port = int(os.getenv("MOM_DASHBOARD_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"🚀 Mom4AI Dashboard läuft auf http://{host}:{port}")
    print("   Endpoints: /api/local_stats, /api/sync_status, POST /api/resonance_event")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server gestoppt.")


if __name__ == "__main__":
    main()
