#!/usr/bin/env python3
"""
Static site build script for yippeeetea's UGC portfolio.

Reads data/videos.json (one entry per featured video) and renders:
  - index.html        (home page; brands with >1 video become a hover "stack" card)
  - about.html         (static about-me page)
  - <brand-slug>.html  (one subpage per brand that has more than one video)

To add a new video: add an entry to data/videos.json, run this script,
then commit + push the regenerated docs/ folder. GitHub Pages is configured
to serve straight from main's /docs folder, so pushing is the only deploy step.
"""
import json
import shutil
from collections import OrderedDict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "videos.json"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"

MAX_STACK_LEAVES = 4  # cap the hover "deck of cards" animation at 3-4 leaves


def load_videos():
    with open(DATA_FILE) as f:
        return json.load(f)


def group_by_brand(videos):
    groups = OrderedDict()
    for v in videos:
        groups.setdefault(v["brand_slug"], {"brand": v["brand"], "videos": []})
        groups[v["brand_slug"]]["videos"].append(v)
    return [
        {"brand_slug": slug, "brand": g["brand"], "videos": g["videos"]}
        for slug, g in groups.items()
    ]


def build():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)

    videos = load_videos()
    groups = group_by_brand(videos)

    # home page
    index_tpl = env.get_template("index.html")
    (OUTPUT_DIR / "index.html").write_text(
        index_tpl.render(active="home", groups=groups)
    )

    # about page
    about_tpl = env.get_template("about.html")
    (OUTPUT_DIR / "about.html").write_text(about_tpl.render(active="about"))

    # one subpage per brand with multiple videos
    brand_tpl = env.get_template("brand.html")
    for group in groups:
        if len(group["videos"]) <= 1:
            continue
        tagline = group["videos"][0].get(
            "brand_tagline",
            f"{len(group['videos'])} videos, one brand, a few different vibes",
        )
        (OUTPUT_DIR / f"{group['brand_slug']}.html").write_text(
            brand_tpl.render(
                active=None,
                brand=group["brand"],
                videos=group["videos"],
                tagline=tagline,
            )
        )

    # static assets
    shutil.copy(STATIC_DIR / "style.css", OUTPUT_DIR / "style.css")
    if (STATIC_DIR / "img").exists():
        shutil.copytree(STATIC_DIR / "img", OUTPUT_DIR / "img")
    (OUTPUT_DIR / ".nojekyll").touch()

    print(f"Built {len(list(OUTPUT_DIR.glob('*.html')))} pages into {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
