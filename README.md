# Happy Teacher's Day Banner

Pure HTML/CSS fullscreen banner for smart board / projector,
with animated gold-on-black celebration visuals and JPG downloads.
**No background music / audio** — the page is fully silent.

## Live

- Display: https://banner.blazenxt.in/
- Downloads: https://banner.blazenxt.in/api/downloads

## UI

Premium ceremonial gold-and-black theme with:

- **Fit-to-screen scaling** — every content size is expressed in a single CSS
  unit `--u = min(vw, vh)` derived from a 1120×720 design. Pure CSS (no JS),
  so the whole banner uniformly scales to perfectly fit ANY screen: smart
  boards (16:9, 4:3, ultrawide), projectors and phones, portrait or landscape,
  windowed or fullscreen. Text never clips and stays as large as possible.
- Ambient aurora glow + slowly rotating light rays
- Twinkling sparkles and rising golden dust particles
- Gradient title, floating laurel, spinning jewel divider
- Dashed halo rings around the icons, breathing date badge
- **Auto-rotating scenes (~8s)**: hero title → Hindi/English Teacher's Day
  quotes (Noto Devanagari, with progress dots) → a generic "Thank You
  Teachers" finale (no personal names)
- **Golden confetti** burst on tap and periodically (GPU-friendly)
- **Live date/time clock** at the top
- Fullscreen toggle button (bottom-right)
- **Performance-tuned for low-end devices (2018 Android etc.)**: every looping
  animation uses only `transform` + `opacity` (GPU-composited). No
  `mix-blend-mode`, no per-frame `box-shadow` / `filter: blur` /
  `background-position` repaints; fewer particles on small screens.
- Respects `prefers-reduced-motion`

Candidate builds are previewed before going live under `/preview/<n>/`
(banner) and `/preview/<n>/devices` (all-devices sheet); the root `/` is only
updated after approval. The live build is v4 (`/preview/4/`): 9 Hindi/English
quotes rotating every 6s, confetti salvo every ~6.5s, scenes every 8s.

All visuals are self-contained in `index.html` (CSS + a tiny vanilla-JS
particle generator, scene rotator, clock and confetti). No build step, no
external media.

## Routes

| Path | What |
|------|------|
| `/` | Fullscreen animated CSS banner with scenes + background music |
| `/preview/5/` | Candidate build with JioSaavn music + mute/unmute button |
| `/api/music` | JioSaavn search/play proxy used by the music player |
| `/api/downloads` | Download horizontal + vertical JPG banners |

## Hosting (Railway / Node)

The same `server.js` serves static files **and** the music API, so it works on
Railway (and any Node host):

```bash
npm install        # installs crypto-js
npm start          # node server.js  (uses process.env.PORT)
```

- Railway: deploy this repo; the start command is `npm start`
  (a Node ≥ 18 service). The `/api/music` proxy needs outbound internet.
- Vercel is also still supported (the static site + `api/music.js` function).

The static `serve` script was replaced by `node server.js` because the JioSaavn
music proxy needs a server-side runtime.

## Contributors

- [blazenxt](https://github.com/blazenxt)
- [m11galaxym581](https://github.com/m11galaxym581)
