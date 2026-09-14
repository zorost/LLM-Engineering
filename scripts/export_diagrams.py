#!/usr/bin/env python3
"""Export diagram HTML SVGs to PNG (diagram only, transparent)."""

from pathlib import Path
import shutil
import sys

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "assets" / "diagrams"
IMG = REPO / "img"
SCALE = int(sys.argv[1]) if len(sys.argv) > 1 else 2

README_COPIES = {
    "banner.png": "banner.png",
    "social.png": "social.png",
    "roadmap-fundamentals.png": "roadmap_fundamentals.png",
    "roadmap-scientist.png": "roadmap_scientist.png",
    "roadmap-engineer.png": "roadmap_engineer.png",
    "roadmap-operator.png": "roadmap_operator.png",
    "roadmap-leader.png": "roadmap_leader.png",
}


def main():
    htmls = sorted(ROOT.glob("*.html"))
    if not htmls:
        raise SystemExit("no diagrams")
    IMG.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            device_scale_factor=SCALE,
            viewport={"width": 1400, "height": 900},
        )
        for src in htmls:
            out = src.with_suffix(".png")
            page.goto(src.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            page.evaluate("() => document.fonts.ready")
            page.locator("svg").first.screenshot(path=str(out), omit_background=True)
            print(out)
        browser.close()
    for src_name, dest_name in README_COPIES.items():
        src = ROOT / src_name
        if src.is_file():
            dest = IMG / dest_name
            shutil.copy2(src, dest)
            print(dest)


if __name__ == "__main__":
    main()
