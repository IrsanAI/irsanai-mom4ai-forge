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


def check_ancestry_valid():
    path = ROOT / "ancestry.json"
    if not path.exists():
        return False, "ancestry.json fehlt"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return False, "ancestry.json ist keine Liste"
        return True, f"{len(data)} Einträge"
    except Exception as exc:
        return False, f"JSON-Fehler: {exc}"


def main() -> int:
    missing = check_files()
    ancestry_ok, ancestry_msg = check_ancestry_valid()

    print("=== MomAI Release Guard ===")
    if missing:
        print("❌ Fehlende Dateien:")
        for item in missing:
            print(f"  - {item}")
    else:
        print("✅ Pflichtdateien vorhanden")

    print(("✅" if ancestry_ok else "❌") + f" ancestry.json: {ancestry_msg}")

    if missing or not ancestry_ok:
        print("\nRelease-Guard: BLOCKED")
        return 1

    print("\nRelease-Guard: READY_FOR_ALPHA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
