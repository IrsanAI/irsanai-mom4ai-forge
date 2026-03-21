from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    script = root / "mom_forge.py"
    completed = subprocess.run([sys.executable, str(script)])
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
