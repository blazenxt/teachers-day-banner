# Background music (24×7 bhajans)

The banner plays Teacher's Day / guru bhajans on loop with a corner
mute/unmute button (see `preview/5`).

These songs are copyrighted, so the MP3 files are **not** included — add your
own legally-obtained audio files here with the following names (or edit the
`SONGS` list in the HTML `src`/title to match your files / direct links):

| File name | Song |
|-----------|------|
| `guruvar-tere-sar-par-haath.mp3` | Guruvar tere sar par hath rahe |
| `guru-vachno-ko-rakhna.mp3`       | Guru vachno ko rakhna sambhal ke |
| `guru-brahma-gurur-vishnu.mp3`    | Guru Brahma Gurur Vishnu (Guru Vandana) |
| `guru-meri-pooja.mp3`             | Guru Meri Pooja |
| `shukriya-tera-aye-guru.mp3`      | Shukriya Tera Aye Guru |

Notes:
- Any file that is missing/fails is **auto-skipped** to the next track, so
  the page never errors — just drop in the MP3s you have.
- You can also use full `https://...mp3` URLs directly in the `SONGS` list.
- Browsers block audio before interaction: music starts on the first
  tap/click anywhere; the corner button then toggles mute/unmute.
- Keep audio out of git if files are large (it is already git-ignored).
