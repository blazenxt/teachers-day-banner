# Happy Teacher's Day Banner

Pure HTML/CSS fullscreen banner for smart board / projector,
with an **original** Teacher's Day melody (composed for this project — not from YouTube / not a known song) and JPG downloads.

## Live

- Display + song: https://banner.blazenxt.in/
- Downloads: https://banner.blazenxt.in/api/downloads

## Music

**“Gratitude · Teacher's Day”** — original ceremonial piano melody
synthesized in Python (`scripts/compose_melody.py`).

```bash
python3 scripts/compose_melody.py
ffmpeg -y -i assets/audio/teachers-day-song.wav -b:a 192k assets/audio/teachers-day-song.mp3
```

No third-party commercial tracks. No YouTube rips.

## Routes

| Path | What |
|------|------|
| `/` | Fullscreen CSS banner + original melody |
| `/api/downloads` | Download horizontal + vertical JPG banners |
| `/assets/audio/teachers-day-song.mp3` | Original song |

## Contributors

- [blazenxt](https://github.com/blazenxt)
- [m11galaxym581](https://github.com/m11galaxym581)
