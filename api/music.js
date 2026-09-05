/**
 * JioSaavn proxy for the Teacher's Day banner background music.
 *
 *   GET /api/music?action=search&q=<query>   -> { songs: [{ id, title, artist }] }
 *   GET /api/music?action=play&id=<songId>   -> 302 redirect to a playable MP3
 *
 * JioSaavn's api.php returns encrypted media URLs (DES-ECB with the known
 * key 38346591). We decrypt server-side and redirect to the CDN MP3, so the
 * browser only needs a same-origin URL (no CORS issues for <audio>).
 *
 * NOTE: this uses JioSaavn's unofficial internal API. It is intended for
 * private / internal use (e.g., a school celebration). JioSaavn's terms
 * apply; use responsibly.
 */

// Pure-JS DES (crypto-js) so it works on Node 18+ where OpenSSL 3 disables
// legacy DES-ECB and on every Vercel runtime without env/OpenSSL tweaks.
let CryptoJS = null;
try { CryptoJS = require('crypto-js'); } catch (e) { CryptoJS = null; }

function decryptMediaUrl(encrypted) {
  try {
    if (!CryptoJS) return null;
    const keyWA = CryptoJS.enc.Utf8.parse('38346591'); // 8-byte DES key
    const cfg = { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 };
    const cipherParams = CryptoJS.lib.CipherParams.create({
      ciphertext: CryptoJS.enc.Base64.parse(encrypted),
    });
    let dec = CryptoJS.DES.decrypt(cipherParams, keyWA, cfg).toString(CryptoJS.enc.Utf8);
    if (!dec) return null;
    return dec.replace(/^http:\/\//, 'https://');
  } catch (e) {
    return null;
  }
}

// Decrypted URL points to a 96kbps AAC file (.../_96.mp4). Offer MP3 variants.
function toQuality(url, quality) {
  if (!url) return null;
  if (quality === '320') return url.replace('_96.mp4', '_320.mp3');
  if (quality === '160') return url.replace('_96.mp4', '_160.mp3');
  return url; // _96.mp4 (AAC, plays in browsers)
}

async function saavnApi(params) {
  const u = new URL('https://www.jiosaavn.com/api.php');
  const base = { _format: 'json', _marker: '0', api_version: '4', ctx: 'web6dot0' };
  u.search = new URLSearchParams(Object.assign({}, base, params)).toString();

  const r = await fetch(u.toString(), {
    headers: {
      'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
        '(KHTML, like Gecko) Chrome/120.0 Safari/537.36',
      Accept: 'application/json',
      Referer: 'https://www.jiosaavn.com/',
    },
  });
  if (!r.ok) throw new Error('JioSaavn HTTP ' + r.status);
  return r.json();
}

// Find the first song object in a song.getDetails response (shape varies).
function pickSong(data, id) {
  if (!data) return null;
  if (Array.isArray(data.songs) && data.songs[0]) return data.songs[0];
  if (id && data[id]) return data[id];
  const found = Object.keys(data)
    .map((k) => data[k])
    .find((v) => v && typeof v === 'object' && v.encrypted_media_url);
  return found || null;
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    const action = (req.query && req.query.action) || 'search';

    if (action === 'search') {
      const q = req.query.q || '';
      if (!q) return res.status(400).json({ error: 'missing q' });

      const data = await saavnApi({ __call: 'search.getResults', q: q, n: '8', p: '1' });
      const list = (data && data.results && data.results.data) || [];
      const songs = list
        .filter((s) => s && (s.type === 'song' || s.id))
        .slice(0, 6)
        .map((s) => ({
          id: s.id,
          title: s.title || s.song,
          artist:
            s.subtitle ||
            (s.more_info &&
              s.more_info.artistMap &&
              s.more_info.artistMap.primary_artists &&
              s.more_info.artistMap.primary_artists.map((a) => a.name).join(', ')) ||
            '',
        }));

      res.setHeader('Cache-Control', 'public, max-age=86400');
      return res.status(200).json({ songs });
    }

    if (action === 'play') {
      const id = req.query.id;
      const quality = req.query.quality === '96' ? '96' : '320';
      if (!id) return res.status(400).json({ error: 'missing id' });

      const data = await saavnApi({ __call: 'song.getDetails', pids: String(id) });
      const song = pickSong(data, String(id));
      const enc =
        song &&
        (song.encrypted_media_url ||
          (song.more_info && song.more_info.encrypted_media_url));
      const decrypted = enc ? decryptMediaUrl(enc) : null;
      const target = toQuality(decrypted, quality);
      if (!target) return res.status(404).json({ error: 'media url not found' });

      res.setHeader('Cache-Control', 'public, max-age=3600');
      return res.redirect(302, target);
    }

    return res.status(400).json({ error: 'unknown action' });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
};
