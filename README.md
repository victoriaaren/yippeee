# yippeee
online porfolio for yippeeetea for my UGC videos, and manage pitches + find  businesses to work with :)

## How this site works

A small static-site generator:

- `data/videos.json`: one entry per featured video (brand, reel link, collab type, bullets, thumbnail)
- `templates/`: Jinja2 templates
- `static/style.css` and `static/img/`: styling and pixel art thumbnails
- `tools/make_pixel_art.py`: draws the pixel art thumbnails (`python tools/make_pixel_art.py`)
- `sync_instagram.py`: pulls new reels from Instagram into `data/videos.json`
- `build.py`: renders everything into `docs/` (committed; GitHub Pages serves `main` / `docs`)

Brands with more than one video automatically become a hover "stack" card (max 4 leaves) linking to an auto-generated brand page.

## Adding a video by hand
1. Add an entry to `data/videos.json` (copy an existing one; `thumb_img` can be any file in `static/img/`)
2. `python build.py`, then commit and push

Preview locally: `python build.py && cd docs && python3 -m http.server 8000`

## Auto-sync from Instagram
`sync_instagram.py` uses the official Instagram Graph API. One-time setup:
1. Switch @yippeeetea to a Professional (Creator or Business) account in the Instagram app
2. Create a Meta developer app, add the "Instagram API with Instagram Login" product, and add yourself as a tester
3. Generate a long-lived access token and `export IG_ACCESS_TOKEN=...` (tokens last 60 days and can be refreshed)

Then, when you post a collab reel, put one of these hashtags in the caption and @ the brand:
- `#gifted` for gifted collab, `#paid` for paid collab, `#paidugc` for paid UGC

Run `python sync_instagram.py && python build.py`, then push. New reels with those hashtags are added automatically (brand = first @mention, caption's first line = description). Tweak the text or thumbnail in `data/videos.json` after if you like.

Running it on a schedule needs a GitHub Actions workflow, which requires the CLI token to have the `workflow` scope (`gh auth refresh -h github.com -s workflow`).
