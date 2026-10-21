#!/usr/bin/env python3
"""
Pulls new reels from @yippeeetea via the Instagram Graph API and appends them
to data/videos.json.

Needs a Creator or Business account (yours already is) and a long-lived token:
    export IG_ACCESS_TOKEN=...      # see README for one-time setup

A reel is only added when its caption has a portfolio hashtag:
    #gifted  -> "gifted collab"
    #paid    -> "paid collab"
    #paidugc -> "paid UGC"
The brand is the first @mention in the caption.

It also refreshes each video's "views" so the site sorts by most viewed.

Usage: python sync_instagram.py [--dry-run]  then  python build.py
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "videos.json"
API = "https://graph.instagram.com/me/media"
FIELDS = "id,caption,media_type,media_product_type,permalink,timestamp"

HASHTAG_TO_COLLAB = {"paidugc": "paid ugc", "paid": "paid", "gifted": "gifted"}
IMG_KEYWORDS = [("boba", "generic-boba"), ("bubble", "generic-boba"), ("matcha", "generic-matcha")]


def fetch_media(token):
    url = f"{API}?{urllib.parse.urlencode({'fields': FIELDS, 'limit': 50, 'access_token': token})}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r).get("data", [])


def fetch_views(media_id, token):
    url = f"https://graph.instagram.com/{media_id}/insights?{urllib.parse.urlencode({'metric': 'views', 'access_token': token})}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.load(r).get("data", [])
        return data[0]["values"][0]["value"] if data else None
    except Exception:
        return None


def update_views(videos, media, token):
    by_code = {shortcode(m.get("permalink")): m for m in media}
    for v in videos:
        item = by_code.get(shortcode(v["reel_url"]))
        views = fetch_views(item["id"], token) if item else None
        if views is not None:
            v["views"] = views


def shortcode(permalink):
    m = re.search(r"/(?:reel|p)/([\w-]+)", permalink or "")
    return m.group(1) if m else None


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_media(item):
    """Returns a video record for a reel with a collab hashtag, else None."""
    if item.get("media_product_type") != "REELS" and item.get("media_type") != "VIDEO":
        return None
    caption = item.get("caption") or ""
    tags = {t.lower() for t in re.findall(r"#(\w+)", caption)}
    collab = next((HASHTAG_TO_COLLAB[t] for t in ("paidugc", "paid", "gifted") if t in tags), None)
    if not collab:
        return None
    mention = re.search(r"@([\w.]+)", caption)
    brand = f"@{mention.group(1)}" if mention else "new collab"
    first_line = re.sub(r"[#@][\w.]+", "", caption.splitlines()[0] if caption else "").strip()
    lowered = caption.lower()
    thumb = next((img for kw, img in IMG_KEYWORDS if kw in lowered), "generic-tea")
    slug = slugify(brand)
    record = {
        "id": f"{slug}-{shortcode(item['permalink'])}",
        "brand": brand,
        "brand_slug": slug,
        "accent": "✨",
        "thumb_class": "thumb-matcha",
        "thumb_emoji": "🍵",
        "thumb_img": f"img/{thumb}.png",
        "reel_url": item["permalink"],
        "collab_type": collab,
        "bullets": [first_line[:80] or "new video!"],
    }
    if collab == "paid ugc":
        record["group_tags"] = ["paid UGC"]
    return record


def merge(existing, media):
    known = {shortcode(v["reel_url"]) for v in existing}
    added = []
    for item in sorted(media, key=lambda m: m.get("timestamp", "")):
        if shortcode(item.get("permalink")) in known:
            continue
        rec = parse_media(item)
        if rec:
            existing.append(rec)
            known.add(shortcode(item["permalink"]))
            added.append(rec)
    return added


def main():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        sys.exit("Set IG_ACCESS_TOKEN first (see README).")
    videos = json.loads(DATA_FILE.read_text())
    media = fetch_media(token)
    added = merge(videos, media)
    update_views(videos, media, token)
    for rec in added:
        print(f"+ {rec['brand']} ({rec['collab_type']}) {rec['reel_url']}")
    if not added:
        print("nothing new")
    if "--dry-run" not in sys.argv:
        DATA_FILE.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n")
        print("updated data/videos.json (new reels + view counts), now run: python build.py")


if __name__ == "__main__":
    main()
