# Background music (24×7 bhajans)

The banner plays Teacher's Day / guru bhajans in the background with a single
corner mute/unmute button.

## Songs come from JioSaavn automatically (no files needed)

`/preview/5/` and the shipped player resolve tracks through our own Vercel
proxy **`/api/music`**, which calls JioSaavn's unofficial `api.php`, decrypts
the media URL server-side, and redirects to the playable CDN MP3. So you do
**not** need to add any MP3 files for it to work.

- Tracks are chosen by the search queries in the `SONGS` list
  (`preview/5/index.html`): edit the `q` strings / `title` to change songs.
- Playback requires internet access and works once the site is deployed on
  Vercel (the proxy needs a serverless function — it won't run inside the
  static `serve` dev preview).

## Optional: local MP3 fallback

If you also have your own MP3 files, drop them here and the player uses them
only if the online lookup fails:

| File name | Song |
|-----------|------|
| `guruvar-tere-sar-par-haath.mp3` | Guruvar tere sar par hath rahe |
| `guru-vachno-ko-rakhna.mp3`       | Guru vachno ko rakhna sambhal ke |
| `guru-meri-pooja.mp3`             | Guru Meri Pooja |
| `guru-meri-drishti.mp3`           | Guru Meri Drishti Mein |
| `shukriya-tera-aye-guru.mp3`      | Shukriya Tera Aye Guru |
| `guru-brahma-gurur-vishnu.mp3`    | Guru Brahma Gurur Vishnu |

MP3s are git-ignored (copyrighted/large). The `fallback` paths in `SONGS`
can also be full `https://...mp3` URLs.

> Browsers block audio before interaction: playback starts on the first
> tap/click anywhere; the corner button then mutes/unmutes.
>
> Note: JioSaavn access here uses an unofficial internal API and is intended
> for private/internal celebration use; their terms apply.
