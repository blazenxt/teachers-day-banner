# Happy Teacher's Day Banner

Pure HTML/CSS fullscreen banner for smart board / projector,
with background celebration music and JPG downloads.

## Live

- Display + song: https://banner.blazenxt.in/
- Downloads: https://banner.blazenxt.in/api/downloads

## Routes

| Path | What |
|------|------|
| `/` | Fullscreen CSS banner + Teacher's Day melody |
| `/api/downloads` | Download horizontal + vertical JPG banners |
| `/assets/banner-horizontal.jpg` | Horizontal image |
| `/assets/banner-vertical.jpg` | Vertical image |
| `/assets/audio/teachers-day-song.mp3` | Background song |

## Music

Royalty-free inspirational ambient track (Pixabay-style free use).
Autoplay tries on load; if the browser blocks it, a gold “Play Song”
prompt appears. Floating control (bottom-right) to play/pause.

## Local preview

```bash
npx serve . -l 3000
```

## Deploy

Static site — Railway / Vercel / any static host.
Push to `main` to redeploy.

## Contributors

- [blazenxt](https://github.com/blazenxt)
- [m11galaxym581](https://github.com/m11galaxym581)
