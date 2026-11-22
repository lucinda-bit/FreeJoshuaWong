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
- Social posts: `assets/socials.js` (the "On social media" section of the Voices page; socials.html redirects there). Copy post text exactly; add the post's own link as `url` when you have it.

- Asked and answered tracker (home page and Newsroom): edit `TRACKER` in `tools/build.py`. When an answer comes in, change its status and wording.
- Chinese page: `zh()` in `tools/build.py` (zh.html). Reviewed by Danny; public and linked from the menu (中文).

- Write to Joshua page (write.html): live, linked from Take action. Messages are sent by Web3Forms (same access key as the Contact form, `FORM_KEY` in `tools/build.py`) to the campaign inbox, subject "Message for Joshua: please read and approve". Nothing appears on the site until approved.
- Approved messages for Joshua: add them to `assets/messages.js` (first name, town, date, text). They appear on the wall (write.html) and, once there are any, in a strip on the home page.
- Print page for his friends: messages-print.html (unlisted). Pick a month and press Print.

- Visitor counting: set `GOATCOUNTER` in `tools/build.py` to the site code from goatcounter.com, then rebuild. No cookies; counts page visits and plays of each video (shown in GoatCounter as `play/<video name>`). Leave it empty to switch counting off.
