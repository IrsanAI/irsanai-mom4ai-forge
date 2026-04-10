from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List


ROADMAP_ITEM_RE = re.compile(r"^- \[(?P<done>[ xX])\] (?P<title>.+?)\s*$")
SCORE_RE = re.compile(r"`(?P<value>\d{1,3})/100`")


@dataclass
class RoadmapItem:
    title: str
    done: bool
    resonanz: int
    chemie: int
    coach_feedback: str


@dataclass
class PortfolioReport:
    total_items: int
    completed_items: int
    open_items: int
    completion_rate: float
    average_resonanz_open: float
    average_chemie_open: float
    top_next_priority: str
    optimization_plan: List[str]
    open_items_ranked: List[dict]


def _extract_score(line: str) -> int:
    m = SCORE_RE.search(line)
    if not m:
        return 0
    return int(m.group("value"))


def parse_roadmap_from_readme(readme_text: str) -> List[RoadmapItem]:
    lines = readme_text.splitlines()
    in_roadmap = False
    items: List[RoadmapItem] = []

    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        if line.strip().startswith("## Roadmap"):
            in_roadmap = True
            i += 1
            continue
        if in_roadmap and line.startswith("## "):
            break

        if in_roadmap:
            m = ROADMAP_ITEM_RE.match(line.strip())
            if m:
                done = m.group("done").lower() == "x"
                title = m.group("title").strip()

                resonanz = 0
                chemie = 0
                feedback = ""
                for j in range(i + 1, min(i + 6, len(lines))):
                    probe = lines[j].strip()
                    if probe.startswith("**Resonanz:**"):
                        resonanz = _extract_score(probe)
                    elif probe.startswith("**Chemie"):
                        chemie = _extract_score(probe)
                    elif probe.startswith("**Coach-Feedback:**"):
                        feedback = probe.replace("**Coach-Feedback:**", "").strip()

                items.append(
                    RoadmapItem(
                        title=title,
                        done=done,
                        resonanz=resonanz,
                        chemie=chemie,
                        coach_feedback=feedback,
                    )
                )
        i += 1

    return items


def _priority_score(item: RoadmapItem) -> float:
    # IrsanAI-Style: Repo-fit (Chemie) + Resonanz + strategischer Moonshot-Bonus.
    strategic_bonus = 8.0 if "Mini-Transformer" in item.title else 0.0
    community_bonus = 4.0 if "Community" in item.title else 0.0
    return item.chemie * 0.58 + item.resonanz * 0.42 + strategic_bonus + community_bonus


def build_portfolio_report(items: List[RoadmapItem]) -> PortfolioReport:
    if not items:
        return PortfolioReport(
            total_items=0,
            completed_items=0,
            open_items=0,
            completion_rate=0.0,
            average_resonanz_open=0.0,
            average_chemie_open=0.0,
            top_next_priority="n/a",
            optimization_plan=["Roadmap konnte nicht geparst werden."],
            open_items_ranked=[],
        )

    completed = [it for it in items if it.done]
    open_items = [it for it in items if not it.done]
    ranked = sorted(open_items, key=_priority_score, reverse=True)

    avg_res_open = sum(x.resonanz for x in open_items) / len(open_items) if open_items else 0.0
    avg_chem_open = sum(x.chemie for x in open_items) / len(open_items) if open_items else 0.0

    plan = [
        "1) Stabilisiere zuerst High-Chemie offene Items (schneller Repo-Fit-Gewinn).",
        "2) Kopple Dashboard-Insights direkt an Runtime/Selection, damit Resonanz-Signale operativ werden.",
        "3) Nutze Mini-Transformer-Blueprints als Brücke zwischen Graph-Evolution und trainierbaren Artefakten.",
    ]

    if ranked:
        top = ranked[0].title
    else:
        top = "Alle Roadmap-Items sind abgeschlossen"

    return PortfolioReport(
        total_items=len(items),
        completed_items=len(completed),
        open_items=len(open_items),
        completion_rate=round(len(completed) / len(items), 3),
        average_resonanz_open=round(avg_res_open, 2),
        average_chemie_open=round(avg_chem_open, 2),
        top_next_priority=top,
        optimization_plan=plan,
        open_items_ranked=[
            {
                "title": x.title,
                "resonanz": x.resonanz,
                "chemie": x.chemie,
                "priority_score": round(_priority_score(x), 2),
                "coach_feedback": x.coach_feedback,
            }
            for x in ranked
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="IrsanAI Chemie Manager: Roadmap-KPI Analyse & Optimierungsvorschläge.")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--json", action="store_true", help="JSON Ausgabe statt Text")
    args = parser.parse_args()

    readme_text = Path(args.readme).read_text(encoding="utf-8")
    items = parse_roadmap_from_readme(readme_text)
    report = build_portfolio_report(items)

    if args.json:
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
        return 0

    print("=== IrsanAI Chemie Manager ===")
    print(f"Roadmap items: {report.total_items} | done: {report.completed_items} | open: {report.open_items}")
    print(f"Completion rate: {report.completion_rate:.1%}")
    print(f"Ø offene Resonanz: {report.average_resonanz_open} | Ø offene Chemie: {report.average_chemie_open}")
    print(f"Top Next Priority: {report.top_next_priority}")
    print("\nMastermind Optimization Plan:")
    for step in report.optimization_plan:
        print(f"- {step}")

    if report.open_items_ranked:
        print("\nOpen Items (ranked):")
        for row in report.open_items_ranked:
            print(
                f"- {row['title']} | score={row['priority_score']} "
                f"(R={row['resonanz']}, C={row['chemie']})"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
