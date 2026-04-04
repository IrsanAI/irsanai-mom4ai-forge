from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

SYNC_START = "<!-- README_SYNC_STATUS_START -->"
SYNC_END = "<!-- README_SYNC_STATUS_END -->"


@dataclass
class ReadmeSyncReport:
    generated_at_utc: str
    de_path: str
    en_path: str
    de_roadmap_items: int
    en_roadmap_items: int
    missing_sections_in_en: List[str]
    missing_sections_in_de: List[str]
    context_delta_score: int
    status: str


def _extract_h2_titles(md: str) -> List[str]:
    return [line[3:].strip().lower() for line in md.splitlines() if line.startswith("## ")]


def _extract_roadmap_items(md: str) -> int:
    in_roadmap = False
    count = 0
    for line in md.splitlines():
        if line.startswith("## Roadmap") or line.startswith("## Roadmap &"):
            in_roadmap = True
            continue
        if in_roadmap and line.startswith("## "):
            break
        if in_roadmap and line.strip().startswith("- ["):
            count += 1
    return count


def _normalize_title(title: str) -> str:
    t = title.lower().strip()
    replacements = {
        "was ist mom4ai forge?": "what is mom4ai forge?",
        "schnellstart – wie du mitmachst": "quickstart",
        "roadmap & was kommt als nächstes": "roadmap",
        "resonance protocol (neu)": "resonance protocol",
        "lokales live-dashboard (ohne docker & mit docker)": "local live dashboard",
        "nächster logischer schritt (usp-richtung)": "next logical step",
        "factory blueprint (produktionslinien-denken)": "factory blueprint",
        "mitmachen & community": "contribute & community",
    }
    return replacements.get(t, t)


def _remove_sync_block(md: str) -> str:
    if SYNC_START in md and SYNC_END in md:
        start = md.index(SYNC_START)
        end = md.index(SYNC_END) + len(SYNC_END)
        return (md[:start] + md[end:]).strip() + "\n"
    return md


def _upsert_sync_block(md: str, block: str) -> str:
    payload = f"{SYNC_START}\n{block}\n{SYNC_END}"
    if SYNC_START in md and SYNC_END in md:
        start = md.index(SYNC_START)
        end = md.index(SYNC_END) + len(SYNC_END)
        return md[:start] + payload + md[end:]

    lines = md.splitlines()
    insert_at = 0
    if lines and lines[0].startswith("# "):
        insert_at = 1
    lines.insert(insert_at, payload)
    return "\n".join(lines) + ("\n" if not md.endswith("\n") else "")


def build_sync_report(readme_de: Path, readme_en: Path) -> ReadmeSyncReport:
    de_text = _remove_sync_block(readme_de.read_text(encoding="utf-8"))
    en_text = _remove_sync_block(readme_en.read_text(encoding="utf-8"))

    de_titles = {_normalize_title(x) for x in _extract_h2_titles(de_text)}
    en_titles = {_normalize_title(x) for x in _extract_h2_titles(en_text)}

    missing_in_en = sorted(de_titles - en_titles)
    missing_in_de = sorted(en_titles - de_titles)

    de_roadmap = _extract_roadmap_items(de_text)
    en_roadmap = _extract_roadmap_items(en_text)
    roadmap_delta = abs(de_roadmap - en_roadmap)

    context_delta = len(missing_in_en) + len(missing_in_de) + roadmap_delta
    status = "up_to_date" if context_delta == 0 else "out_of_sync"

    return ReadmeSyncReport(
        generated_at_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        de_path=str(readme_de),
        en_path=str(readme_en),
        de_roadmap_items=de_roadmap,
        en_roadmap_items=en_roadmap,
        missing_sections_in_en=missing_in_en,
        missing_sections_in_de=missing_in_de,
        context_delta_score=context_delta,
        status=status,
    )


def _badge_for_status(status: str) -> str:
    if status == "up_to_date":
        return "🟢"
    return "🟠"


def _build_sync_block(report: ReadmeSyncReport) -> str:
    badge = _badge_for_status(report.status)
    return (
        f"{badge} **Readme Language Sync:** `{report.status}`  \n"
        f"🌐 **Context Delta:** `{report.context_delta_score}`  \n"
        f"🕒 **Last Sync Check (UTC):** `{report.generated_at_utc}`"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="IrsanAI Readme Auto Sync Manager")
    parser.add_argument("--de", default="README.md")
    parser.add_argument("--en", default="README.en.md")
    parser.add_argument("--report-json", default="docs/readme_sync_report.json")
    parser.add_argument("--check", action="store_true", help="Exit with non-zero when readmes are out of sync")
    args = parser.parse_args()

    de_path = Path(args.de)
    en_path = Path(args.en)

    report = build_sync_report(de_path, en_path)
    block = _build_sync_block(report)

    de_text = de_path.read_text(encoding="utf-8")
    en_text = en_path.read_text(encoding="utf-8")
    de_path.write_text(_upsert_sync_block(de_text, block), encoding="utf-8")
    en_path.write_text(_upsert_sync_block(en_text, block), encoding="utf-8")

    Path(args.report_json).write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))

    if args.check and report.status != "up_to_date":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
