from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent.parent


REQUIRED_FILES = [
    ".github/workflows/build.yml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "docs/release_readiness.md",
    "docs/releases/v0.1.0-alpha.md",
    "src/mom_forge.py",
]


def check_files():
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    return missing


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_ancestry_valid():
    path = ROOT / "ancestry.json"
    if not path.exists():
        return False, "ancestry.json fehlt"
    try:
        data = _load_json(path)
        if not isinstance(data, list):
            return False, "ancestry.json ist keine Liste"
        return True, f"{len(data)} Einträge"
    except Exception as exc:
        return False, f"JSON-Fehler: {exc}"


def check_report_contracts():
    report_specs = [
        {
            "path": ROOT / "docs" / "readme_sync_report.json",
            "required_keys": ["status", "context_delta_score"],
        },
        {
            "path": ROOT / "docs" / "benchmark_report.json",
            "required_keys": ["kpis", "integrity"],
        },
        {
            "path": ROOT / "docs" / "quality_gates_report.json",
            "required_keys": ["passed", "gates"],
        },
        {
            "path": ROOT / "docs" / "resonance_lifecycle_report.json",
            "required_keys": ["population_size", "state_counts", "skeletons"],
        },
    ]

    problems = []
    for spec in report_specs:
        path = spec["path"]
        if not path.exists():
            problems.append(f"{path.relative_to(ROOT)} fehlt")
            continue
        try:
            data = _load_json(path)
        except Exception as exc:
            problems.append(f"{path.relative_to(ROOT)} JSON-Fehler: {exc}")
            continue
        if not isinstance(data, dict):
            problems.append(f"{path.relative_to(ROOT)} hat kein Objekt-Top-Level")
            continue
        missing = [k for k in spec["required_keys"] if k not in data]
        if missing:
            problems.append(f"{path.relative_to(ROOT)} missing keys: {', '.join(missing)}")

    return len(problems) == 0, problems


def main() -> int:
    missing = check_files()
    ancestry_ok, ancestry_msg = check_ancestry_valid()
    contracts_ok, contract_problems = check_report_contracts()

    print("=== MomAI Release Guard ===")
    if missing:
        print("❌ Fehlende Dateien:")
        for item in missing:
            print(f"  - {item}")
    else:
        print("✅ Pflichtdateien vorhanden")

    print(("✅" if ancestry_ok else "❌") + f" ancestry.json: {ancestry_msg}")
    if contracts_ok:
        print("✅ report contracts: ok")
    else:
        print("❌ report contracts:")
        for problem in contract_problems:
            print(f"  - {problem}")

    if missing or not ancestry_ok or not contracts_ok:
        print("\nRelease-Guard: BLOCKED")
        return 1

    print("\nRelease-Guard: READY_FOR_ALPHA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
