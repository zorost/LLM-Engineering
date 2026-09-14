#!/usr/bin/env python3
"""Export diagram HTML SVGs to PNG (diagram only, transparent)."""

from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / "assets" / "diagrams"
SCALE = int(sys.argv[1]) if len(sys.argv) > 1 else 2


def main():
    htmls = sorted(ROOT.glob("*.html"))
    if not htmls:
        raise SystemExit("no diagrams")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=SCALE)
        for src in htmls:
            out = src.with_suffix(".png")
            page.goto(src.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            page.locator("svg").first.screenshot(path=str(out), omit_background=True)
            print(out)
        browser.close()


if __name__ == "__main__":
    main()
