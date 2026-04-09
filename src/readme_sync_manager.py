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


def _extract_roadmap_block(md: str) -> tuple[int, int, list[str]] | None:
    lines = md.splitlines()
    start = None
    end = None
    for idx, line in enumerate(lines):
        if line.startswith("## Roadmap") or line.startswith("## Roadmap &"):
            start = idx
            continue
        if start is not None and idx > start and line.startswith("## "):
            end = idx
            break
    if start is None:
        return None
    if end is None:
        end = len(lines)
    return start, end, lines


def _extract_de_visual_triplets(md: str) -> List[tuple[str, str, str]]:
    block = _extract_roadmap_block(md)
    if not block:
        return []
    start, end, lines = block
    visuals: List[tuple[str, str, str]] = []
    i = start + 1
    while i < end:
        if lines[i].strip().startswith("- ["):
            resonanz = ""
            chemie = ""
            feedback = ""
            for j in range(i + 1, min(i + 8, end)):
                probe = lines[j].strip()
                if probe.startswith("- ["):
                    break
                if probe.startswith("**Resonanz:**"):
                    resonanz = probe.replace("**Resonanz:**", "**Resonance:**", 1)
                elif probe.startswith("**Chemie"):
                    chemie = probe.replace("**Chemie (Repo-Fit):**", "**Chemistry (Repo-Fit):**", 1)
                elif probe.startswith("**Coach-Feedback:**"):
                    feedback = probe.replace("**Coach-Feedback:**", "**Coach Feedback:**", 1)
            visuals.append((resonanz, chemie, feedback))
        i += 1
    return visuals


def _sync_en_roadmap_visuals(de_md: str, en_md: str) -> str:
    de_visuals = _extract_de_visual_triplets(de_md)
    block = _extract_roadmap_block(en_md)
    if not block or not de_visuals:
        return en_md

    start, end, lines = block
    out = lines[: start + 1]
    body = lines[start + 1 : end]
    item_idx = -1
    i = 0
    while i < len(body):
        line = body[i]
        if line.strip().startswith("- ["):
            item_idx += 1
            out.append(line)
            # skip existing detail lines and blank lines until next roadmap item/heading
            j = i + 1
            while j < len(body):
                probe = body[j].strip()
                if probe.startswith("- ["):
                    break
                j += 1

            if 0 <= item_idx < len(de_visuals):
                resonanz, chemie, feedback = de_visuals[item_idx]
                if resonanz:
                    out.append(f"  {resonanz}")
                if chemie:
                    out.append(f"  {chemie}")
                if feedback:
                    out.append(f"  {feedback}")
                out.append("")
            i = j
            continue
        i += 1

    out.extend(lines[end:])
    return "\n".join(out).rstrip() + "\n"


def _extract_visual_line_count(md: str) -> int:
    block = _extract_roadmap_block(md)
    if not block:
        return 0
    start, end, lines = block
    count = 0
    for line in lines[start:end]:
        s = line.strip()
        if s.startswith("**Resonanz:**") or s.startswith("**Resonance:**"):
            count += 1
        if s.startswith("**Chemie") or s.startswith("**Chemistry"):
            count += 1
        if s.startswith("**Coach-Feedback:**") or s.startswith("**Coach Feedback:**"):
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

    de_visual_lines = _extract_visual_line_count(de_text)
    en_visual_lines = _extract_visual_line_count(en_text)
    visual_delta = abs(de_visual_lines - en_visual_lines)

    context_delta = len(missing_in_en) + len(missing_in_de) + roadmap_delta + visual_delta
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

    de_text = de_path.read_text(encoding="utf-8")
    en_text = en_path.read_text(encoding="utf-8")
    synced_en_text = _sync_en_roadmap_visuals(de_text, en_text)
    if synced_en_text != en_text:
        en_path.write_text(synced_en_text, encoding="utf-8")
        en_text = synced_en_text

    report = build_sync_report(de_path, en_path)
    block = _build_sync_block(report)
    de_path.write_text(_upsert_sync_block(de_text, block), encoding="utf-8")
    en_path.write_text(_upsert_sync_block(en_text, block), encoding="utf-8")

    Path(args.report_json).write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))

    if args.check and report.status != "up_to_date":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
