# Pola Scraper (Manga, Komikcast, XBato)

Teknik web scraping dengan Node.js (Express + Axios + Cheerio) untuk situs manga/komik.

## Arsitektur Scraper API

```
scraper/
├── index.js         # Server Express + routes
├── cache/           # Direktori file cache
└── package.json
```

Library: `express` `axios` `cheerio` `morgan` `fs-extra`

## Komikcast Scraper

Scraper untuk `https://komikcast.li` — daftar manga, search, detail, chapter images.

### Konfigurasi HTTP Client

```js
const http = axios.create({
  baseURL: 'https://komikcast.li',
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://komikcast.li/',
  },
  httpAgent, httpsAgent,
  timeout: 15000,
  decompress: true,
  maxRedirects: 5,
  validateStatus: (s) => (s >= 200 && s < 300) || s === 304,
});
```

### Parser: Daftar Manga

```js
function parseListPage(html) {
  const $ = cheerio.load(html);
  const items = [];
  $('.list-update_item').each((_i, el) => {
    const $a = $(el).find('a').first();
    const href = $a.attr('href') || '';
    const img = $a.find('img').attr('src') || $a.find('img').attr('data-src') || '';
    const title = $a.find('h3.title').text().trim();
    const ratingText = ($a.find('.numscore').text().trim() || '').replace(',', '.');
    let slug = '';
    try {
      const u = new URL(href, BASE_URL);
      const segs = u.pathname.replace(/^\/|\/$/g, '').split('/');
      if (segs[0] === 'komik' && segs[1]) slug = segs[1].toLowerCase();
    } catch {
      const segs = href.replace(/^\/|\/$/g, '').split('/');
      if (segs[0] === 'komik' && segs[1]) slug = segs[1].toLowerCase();
    }
    if (slug && title) {
      items.push({
        slug, judul: title, href,
        image: cleanImageUrl(img),
        rating: ratingText && ratingText !== '?' ? parseFloat(ratingText) : null,
        chapter: $a.find('.other .chapter').text().trim() || null,
        type: $a.find('.type').text().trim() || null,
      });
    }
  });
  return items;
}
```

### Route: /manga dengan sort, type, status + filter

```js
app.get('/manga', async (req, res) => {
  const page = Number(req.query.page || 1) || 1;
  const sort = (req.query.sort || '').toLowerCase(); // "popular", "update", "title", "titlereverse"
  const typeQ = (req.query.type || '').toLowerCase();   // "manga", "manhwa", "manhua"
  const statusQ = (req.query.status || '').toLowerCase(); // "ongoing", "completed"

  let url;
  switch (sort) {
    case 'popular': url = page === 1 ? '/popular-komik/' : `/popular-komik/page/${page}/`; break;
    default:        url = page === 1 ? '/daftar-komik/' : `/daftar-komik/page/${page}/`;
  }

  // Filter type
  if (typeQ) list = list.filter(x => (x.type || '').toLowerCase().includes(typeQ));

  // Filter status → fetch detail page untuk setiap item (concurrency=6)
  if (statusQ) {
    const tasks = list.map(item => async () => {
      const detailKey = `detail_${item.slug}`;
      const detail = await fetchWithCache(detailKey, TTL.detail, req, async (ch) => {
        const r = await http.get(`/komik/${item.slug}/`, { headers: ch });
        if (r.status === 304) return { status: 304 };
        return { data: parseDetailPage(r.data), httpMeta: { etag: r.headers.etag || null, lastModified: r.headers['last-modified'] || null } };
      });
      return (detail?.status || '').toLowerCase().startsWith(statusQ) ? item : null;
    });
    list = (await runLimited(tasks, 6)).filter(Boolean);
  }
});
```

### Parser: Detail Page

```js
function parseDetailPage(html) {
  const $ = cheerio.load(html);
  const title = $('h1.entry-title').text().trim() || $('h1.title').text().trim() || $('.komik_info-title').text().trim() || $('h1').first().text().trim();
  const cover = $('.thumb img').attr('src') || $('.komik_info-cover img').attr('src') || $('meta[property="og:image"]').attr('content') || '';

  // Pick text dengan fallback selector
  function pickText(selList) { for (const s of selList) { const t = $(s).text().trim(); if (t) return t; } return ''; }

  const status = pickText(['.komik_info-content:contains(\'Status\') .komik_info-content-value', '.col-info-manga-box > span:contains(\'Status\')']).replace(/Status:\s*/i, '').trim() || null;
  const author = pickText(['.komik_info-content:contains(\'Author\') .komik_info-content-value', '.col-info-manga-box > span:contains(\'Author\')']).replace(/Author:\s*/i, '').trim() || null;

  // Chapters
  const chapters = [];
  $('.box-list-chapter ul li').each((_i, el) => {
    const $a = $(el).find('a').first();
    const url = $a.attr('href') || '';
    const nama = $a.text().replace(/\s+/g, ' ').trim();
    if (!url || !nama) return;
    let slug = '';
    try { const u = new URL(url, BASE_URL); const segs = u.pathname.replace(/^\/|\/$/g, '').split('/'); slug = segs[0] === 'chapter' && segs[1] ? segs[1] : segs.pop(); } catch {}
    chapters.push({ slug, nama, url });
  });

  return { judul: title || null, gambar: cleanImageUrl(cover), status, author, rilis, genre: Array.from(genres), deskripsi, chapters };
}
```

### Parser: Chapter Images

```js
function parseChapterImages(html) {
  const $ = cheerio.load(html);
  const urls = new Set();
  const scopes = ['#readerarea', '.reading-content', '.reader-area', '.chapter-area', '.main-reading-area', '.entry-content', 'body'];
  for (const s of scopes) {
    $(`${s} img`).each((_i, el) => {
      const src = $(el).attr('src') || $(el).attr('data-src') || $(el).attr('data-lazy-src') || $(el).attr('data-original') || '';
      const u = cleanImageUrl(src);
      if (u && /^https?:\/\//i.test(u)) urls.add(u);
    });
    if (urls.size > 0) break;
  }
  return Array.from(urls).map(u => ({ gambar: u }));
}
```

### Merge + Dedupe by Slug

```js
function mergeUniqueBySlug(newList, oldList, maxSize) {
  const out = [];
  const seen = new Set();
  for (const it of Array.isArray(newList) ? newList : []) {
    const key = (it && it.slug) ? String(it.slug).toLowerCase() : null;
    if (!key || seen.has(key)) continue;
    seen.add(key); out.push(it);
    if (maxSize && out.length >= maxSize) return out;
  }
  for (const it of Array.isArray(oldList) ? oldList : []) {
    const key = (it && it.slug) ? String(it.slug).toLowerCase() : null;
    if (!key || seen.has(key)) continue;
    seen.add(key); out.push(it);
    if (maxSize && out.length >= maxSize) return out;
  }
  return out;
}
```

### Search → Kembalikan Bentuk Penuh

```js
app.get('/search', async (req, res) => {
  const q = (req.query.query || '').toString().trim();
  if (!q) return res.status(400).json({ error: 'query is required' });
  const url = `/?s=${encodeURIComponent(q)}`;
  const data = await fetchWithCache(cacheKey, TTL.search, req, async (condHeaders) => {
    const resp = await http.get(url, { headers: condHeaders });
    if (resp.status === 304) return { status: 304 };
    const list = parseListPage(resp.data); // bentuk penuh: {slug, judul, href, image, rating, chapter, type}
    return { data: list, httpMeta: { etag: resp.headers.etag || null, lastModified: resp.headers['last-modified'] || null } };
  });
  res.json(data);
});
```

## XBato Scraper

Scraper untuk `https://xbato.com` — robots guard, rate-limit 1 req/detik, sticky UA.

### Robots Guard

```js
const ROBOTS_DISALLOW = [
  '/account/', '/publish/', '/editor/', '/my/',
  '/subject-overview/', '/subject-episodes/', '/subject-permissions/',
  '/_tools/', '/_utils/', '/_miscs/', '/editor-'
];
function isDisallowedPath(urlPath) {
  return ROBOTS_DISALLOW.some(p => urlPath.startsWith(p));
}
```

### Rate-limit 1 req/detik

```js
let lastAt = 0;
async function politeDelay() {
  const minMs = 1000;
  const delta = Date.now() - lastAt;
  if (delta < minMs) await new Promise(r => setTimeout(r, minMs - delta));
  lastAt = Date.now();
}
```

### Sticky User-Agent per Host

```js
const UA_POOL = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/16.6 Safari/605.1.15',
  'Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/124.0 Mobile Safari/537.36',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 Version/16.6 Mobile/15E148 Safari/604.1'
];
const stickyUAByHost = new Map();
function getUA(url) {
  const host = new URL(url).host;
  if (!stickyUAByHost.has(host)) stickyUAByHost.set(host, UA_POOL[Math.floor(Math.random() * UA_POOL.length)]);
  return stickyUAByHost.get(host);
}
```

### Parser: List Page (xbato .col.item)

```js
function parseListPage($) {
  const items = [];
  $('.col.item').each((_, el) => {
    const title = safeText($(el).find('.item-text .item-title').first());
    const href = $(el).find('a.item-title').attr('href') || $(el).find('a.item-cover').attr('href') || $(el).find('a').first().attr('href');
    const url = absUrl(href);
    if (!url || isDisallowedPath(new URL(url).pathname)) return;
    const img = $(el).find('.item-cover img').first();
    const thumb = img.attr('data-src') || img.attr('src') || null;
    items.push({ title: title || null, url, thumb });
  });
  // Fallback
  if (items.length === 0) {
    $('.gallery, .card, .item, .post, .entry').each((_, el) => {
      const a = $(el).find('a').first();
      const href = a.attr('href'); const url = absUrl(href);
      if (!url || isDisallowedPath(new URL(url).pathname)) return;
      const t = safeText($(el).find('.item-title').first()) || safeText($(el).find('.title, .caption, h3, h2').first());
      const img = $(el).find('img').first();
      const thumb = img.attr('data-src') || img.attr('src') || null;
      if (t || thumb) items.push({ title: t || null, url, thumb });
    });
  }
  return items;
}
```

### Pagination Heuristik

```js
function findNextUrl($, currentUrl) {
  let next = $('link[rel=next]').attr('href') || $('a[rel=next]').attr('href');
  if (!next) next = $('a.next, .pagination a.next, a:contains("Next")').attr('href');
  if (!next) next = $('.load-more a').attr('href') || $('.load-more [data-url]').attr('data-url');
  if (!next) {
    const u = new URL(currentUrl);
    const p = Number(u.searchParams.get('page') || '1');
    u.searchParams.set('page', String(p + 1));
    next = u.toString();
  }
  return next ? new URL(next, currentUrl).toString() : null;
}
```

### Route: /detail dengan Fallback Search

```js
app.get('/detail/:slug', async (req, res) => {
  const input = req.params.slug.trim();
  const primary = /^\d+$/.test(input) ? `${BASE}/series/${input}` : `${BASE}/series/${encodeURIComponent(input)}`;
  let got = await fetchHtmlTry(primary, { ttl, refresh });
  if (!got.ok) {
    // Fallback: /search?word=...
    const s = await fetchHtmlTry(`${BASE}/search?word=${encodeURIComponent(input)}`);
    if (!s.ok) return res.status(404).json({ error: 'Series not found' });
    const picked = pickSeriesFromSearch(cheerio.load(s.html), input);
    if (!picked) return res.status(404).json({ error: 'Not found in search' });
    got = await fetchHtmlTry(picked.url);
  }
  const $ = cheerio.load(got.html);
  const chapters = [];
  $('.episode-list .main .item a.chapt').each((_, el) => {
    const url = absUrl($(el).attr('href'));
    const chTitle = (safeText($(el).find('b').first()) + ' ' + safeText($(el).find('span').first())).trim();
    if (url) chapters.push({ title: chTitle || null, url });
  });
  res.json({ input, url: target, title, cover, description, chapters, chaptersCount: chapters.length });
});
```

### Parse Durasi Multi-Segmen (Bahasa Indonesia)

```js
function parseDuration(input, fallbackMs) {
  const FACTOR_MS = {
    ms: 1, s: 1000, sec: 1000, detik: 1000,
    m: 60000, min: 60000, menit: 60000,
    h: 3600000, hr: 3600000, jam: 3600000,
    d: 86400000, day: 86400000, hari: 86400000,
  };
  const re = /(\d+(?:\.\d+)?)\s*(ms|milliseconds?|s|secs?|seconds?|detik|m|mins?|minutes?|menit|h|hrs?|hours?|jam|d|days?|hari)\b/g;
  let total = 0, matched = false, m;
  while ((m = re.exec(str)) !== null) {
    matched = true;
    const factor = FACTOR_MS[normalize(m[2])] || FACTOR_MS[m[2]];
    if (factor) total += parseFloat(m[1]) * factor;
  }
  return matched ? Math.round(total) : fallbackMs;
}
```

## API Downloader: yt-dlp via Node.js

```js
const { exec } = require('child_process');
app.get('/aio', (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).json({ error: 'parameter url dibutuhkan!' });
  const command = `yt-dlp -j --no-playlist --no-warnings --simulate "${url}"`;
  exec(command, { maxBuffer: 1024 * 1000 }, (error, stdout, stderr) => {
    if (error) return res.status(500).json({ error: stderr || error.message });
    const data = JSON.parse(stdout);
    const formats = data.formats.map(f => ({
      formatId: f.format_id, label: f.format_note || f.format,
      type: f.vcodec === 'none' ? 'audio' : 'video', ext: f.ext,
      quality: f.format, width: f.width, height: f.height, url: f.url,
      bitrate: f.tbr, fps: f.fps, duration: f.duration, is_audio: f.vcodec === 'none'
    }));
    res.json({ apiCreator: '...', url, source: data.extractor, title: data.title, thumbnail: data.thumbnail, duration: data.duration, medias: formats });
  });
});
```

Optimasi: `--no-playlist --no-warnings --simulate`, tambah `--user-agent`, gunakan `--cookies` jika perlu.

## Etika Scraping

- Hormati `robots.txt` (denylist path)
- Rate limit: 1 request/detik minimum
- Cache hasil (hindari request berulang)
- Identifikasi diri via User-Agent yang jelas
- Jangan scraping konten sensitif
- Jangan host publik tanpa izin

## Related

- [[nodejs-api]] - Pola backend Node.js
- [[api-integration]] - MAL API, OAuth, CORS
