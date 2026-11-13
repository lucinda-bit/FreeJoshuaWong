# Free Joshua Wong

Campaign website for freejoshuawong.org.

- `index.html` — the site
- `images/` — photos (Joshua photo: clear with Andrew before launch)
- Press articles are listed in the `PRESS` block near the bottom of `index.html`

Hosted on Netlify: every change pushed to `main` goes live automatically.

## Updating the site
- Coverage: add a line to `assets/press.js`. Voices/quotes: `assets/voices.js`. Parliament record and videos: `RECORD` / `VIDEOS` in `tools/build.py`.
- Then run `python3 tools/build.py` — it rebuilds every page, refreshes the day counts and regenerates `images/share-card.jpg` (the picture shown when the site is shared).
- Push to `main`; GitHub Pages publishes automatically.
- Each quote in `assets/voices.js` automatically gets its own share page (`voices/<name>-<date>.html`) and share picture (`images/quotes/`). If two quotes share a speaker and date, give one an `id:"..."`.
