#!/usr/bin/env python3
"""Fail if labs or required files are missing, and execute notebook self-checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

REQUIRED = [
    "README.md",
    "START-HERE.md",
    "LICENSE",
    "docs/ASSESSMENT.md",
    "reference/GLOSSARY.md",
    "reference/BOOKS.md",
    "reference/YOUTUBE.md",
    "tracks/00-fundamentals/README.md",
    "tracks/01-scientist/README.md",
    "tracks/02-engineer/README.md",
    "tracks/03-operator/README.md",
    "tracks/04-leader/README.md",
    "assets/diagrams/course-map.png",
    "img/banner.png",
    "img/roadmap_fundamentals.png",
    "img/roadmap_scientist.png",
    "img/roadmap_engineer.png",
    "img/roadmap_operator.png",
    "img/roadmap_leader.png",
]

def fail(msg: str) -> None:
    print("fail:", msg, file=sys.stderr)
    sys.exit(1)


def exec_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    env = {"__name__": "__main__"}
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        try:
            exec(compile(src, str(path), "exec"), env, env)
        except Exception as exc:  # noqa: BLE001
            fail(f"{path.name}: {exc}")


def main() -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing {rel}")
    names = sorted(p.name for p in NOTEBOOKS.glob("*.ipynb"))
    if len(names) < 20:
        fail(f"expected 20 notebooks, found {len(names)}")
    for prefix in [f"{i:02d}" for i in range(20)]:
        if not any(n.startswith(prefix) for n in names):
            fail(f"missing lab {prefix}")
    for path in sorted(NOTEBOOKS.glob("*.ipynb")):
        exec_notebook(path)
    # no em dash in tracked markdown
    for md in ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "\u2014" in text:
            fail(f"em dash in {md.relative_to(ROOT)}")
    print("ok")


if __name__ == "__main__":
    main()
