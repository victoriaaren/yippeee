# yippeee
online porfolio for yippeeetea for my UGC videos, and manage pitches + find  businesses to work with :)

## How this site works

This is now a small static-site generator, not hand-written HTML:

- `data/videos.json` — one entry per featured video (brand, reel link, collab type, bullets, etc.)
- `templates/` — Jinja2 templates (`base.html`, `index.html`, `about.html`, `brand.html`, `_card.html`)
- `static/style.css` — all styling
- `build.py` — reads the data + templates and renders everything into `public/` (git-ignored, rebuilt every time)
- `.github/workflows/deploy.yml` — on every push to `main`, GitHub Actions runs `build.py` and deploys `public/` straight to GitHub Pages

**Brands with more than one video automatically become a hover "stack" card** (deck-of-cards animation, capped at 4 leaves) that links to an auto-generated `<brand-slug>.html` page listing every video for that brand. A brand with exactly one video just renders as a normal card. This means Superboba today and itea world (or anyone else) tomorrow, as soon as a second video is added, get the same stack treatment with zero manual HTML.

### Adding a new video
1. Open `data/videos.json`
2. Copy an existing entry, update `id`, `brand`, `brand_slug`, `reel_url`, `collab_type` (`gifted`/`paid`), `thumb_class`/`thumb_emoji`, and `bullets`
3. Commit + push to `main` — Actions rebuilds and deploys automatically (usually live within ~1-2 minutes)

To preview locally before pushing:
```
pip install -r requirements.txt
python build.py
cd public && python3 -m http.server 8000
```

### On auto-polling Instagram directly
Instagram does not allow public scraping (login wall + Terms of Service), so this
site can't silently "watch" the account and pull in new reels on its own. The
sanctioned path is Meta's **Instagram Graph API**, which requires converting to an
Instagram **Business/Creator** account linked to a Facebook Page, creating a Meta
app, completing app review for the needed permissions, and maintaining a
long-lived access token (stored as a GitHub Actions secret, refreshed periodically).
If that's ever set up, a scheduled Actions job could call the Graph API, append new
posts to `data/videos.json`, and let the existing build/deploy pipeline take it from
there — but that's a separate, account-level step outside of what this generator can
do by itself. For now, the manual `data/videos.json` edit above is the fast,
reliable path and takes under a minute per video.
 
