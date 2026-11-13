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
- Social posts: `assets/socials.js` (Socials page). Copy post text exactly; add the post's own link as `url` when you have it.

- Asked and answered tracker (home page and Newsroom): edit `TRACKER` in `tools/build.py`. When an answer comes in, change its status and wording.
- Chinese page: `zh()` in `tools/build.py` (zh.html). Unlisted and hidden from search until Danny has reviewed it; then remove the noindex line and add it to the menu.

- Write to Joshua page (write.html): unlisted for now. Set `WRITE_TO` in `tools/build.py` to the email address messages should go to; then link it from the menu/home page.
- Approved messages for Joshua: add them to `assets/messages.js` (first name, town, date, text). They appear on the wall (write.html) and, once there are any, in a strip on the home page.
- Print page for his friends: messages-print.html (unlisted). Pick a month and press Print.
