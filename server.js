/**
 * Universal static + API server.
 *
 * Works on Railway (and any plain Node host) and locally:
 *   npm start  ->  node server.js  (PORT from env, default 3000)
 *
 * - Serves the static site (index.html, assets, preview/...), with clean
 *   extension-less URLs (e.g. /preview/5, /api/downloads).
 * - Runs the JioSaavn music proxy at /api/music.
 *
 * This keeps one codebase for both Vercel (api/music.js serverless) and
 * Railway / other Node hosts (this long-running server).
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;
const ROOT = __dirname;

const musicHandler = require('./api/music.js');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.mp3': 'audio/mpeg',
  '.mp4': 'audio/mp4',
  '.wav': 'audio/wav',
  '.webp': 'image/webp',
  '.webmanifest': 'application/manifest+json',
  '.txt': 'text/plain; charset=utf-8',
  '.md': 'text/plain; charset=utf-8'
};

function sendFile(res, file) {
  fs.readFile(file, function (err, data) {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not found');
      return;
    }
    const ext = path.extname(file).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
}

function isSafePublicFile(file) {
  const rel = path.relative(ROOT, file);
  if (!rel || rel.startsWith('..') || path.isAbsolute(rel)) return false;
  // never serve dotfiles / dotfolders (.git, .vercel, .gitignore, etc.)
  const parts = rel.split(path.sep);
  for (const part of parts) {
    if (part === '' || part.startsWith('.')) return false;
  }
  // never serve server-side code or manifests
  const base = path.basename(file);
  if (base === 'server.js' || base === 'package.json' || base === 'package-lock.json') return false;
  if (rel.split(path.sep).includes('api') && base.endsWith('.js')) return false;
  return true;
}

function resolveStatic(pathname) {
  // Decode and strip leading slash; block any traversal / dotfiles.
  let rel = decodeURIComponent(pathname);
  rel = rel.replace(/^\/+/, '').replace(/\?.*$/, '');
  if (rel.includes('\0')) return null;

  let abs = path.normalize(path.join(ROOT, rel));
  if (!abs.startsWith(ROOT)) return null; // prevent path traversal

  const candidates = [];
  if (rel === '') {
    candidates.push(path.join(ROOT, 'index.html'));
  } else {
    candidates.push(abs);                                  // exact (file or dir)
    candidates.push(abs + '.html');                        // clean url -> .html
    candidates.push(path.join(abs, 'index.html'));         // dir -> index.html
  }

  for (const c of candidates) {
    try {
      const st = fs.statSync(c);
      if (st.isFile() && isSafePublicFile(c)) return c;
    } catch (e) { /* try next */ }
  }
  return null;
}

const server = http.createServer(function (req, res) {
  const parsed = url.parse(req.url, true);
  const pathname = parsed.pathname || '/';

  // CORS for the audio/API
  res.setHeader('Access-Control-Allow-Origin', '*');

  // ---- API: JioSaavn music proxy ----
  if (pathname === '/api/music') {
    const adapters = {
      query: parsed.query,
      setHeader: function (k, v) { res.setHeader(k, v); },
      status: function (code) { res.statusCode = code; return adapters; },
      json: function (obj) {
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify(obj));
      },
      redirect: function (code, to) {
        res.statusCode = code || 302;
        res.setHeader('Location', to);
        res.end();
      }
    };
    Promise.resolve(musicHandler({ query: parsed.query }, adapters)).catch(function (e) {
      if (!res.headersSent) {
        res.statusCode = 500;
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify({ error: String((e && e.message) || e) }));
      }
    });
    return;
  }

  // ---- everything else: static (covers /api/downloads via clean url) ----
  const file = resolveStatic(pathname);
  if (file) {
    sendFile(res, file);
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('404 Not Found');
});

server.listen(PORT, '0.0.0.0', function () {
  console.log('Teacher\'s Day banner running on http://0.0.0.0:' + PORT);
});
