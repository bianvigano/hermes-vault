# Integrasi API (MAL, OAuth, CORS, SSE)

Teknik integrasi API eksternal, autentikasi, CORS, dan Server-Sent Events.

## MyAnimeList (MAL) API

### Cara Resmi: MAL API v2

Butuh Client ID (`X-MAL-CLIENT-ID` header), OAuth untuk data user.

```js
const CLIENT_ID = process.env.MAL_CLIENT_ID;

async function searchAnime(query, limit = 5) {
  const params = new URLSearchParams({ q: query, limit: String(limit), fields: 'id,title,main_picture,mean,rank,media_type,episodes,status,start_date' });
  const res = await fetch(`https://api.myanimelist.net/v2/anime?${params}`, { headers: { 'X-MAL-CLIENT-ID': CLIENT_ID } });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data.data.map(d => d.node);
}

async function getAnime(id) {
  const params = new URLSearchParams({ fields: 'id,title,main_picture,mean,rank,media_type,episodes,genres,synopsis,studios' });
  const res = await fetch(`https://api.myanimelist.net/v2/anime/${id}?${params}`, { headers: { 'X-MAL-CLIENT-ID': CLIENT_ID } });
  return res.json();
}

async function getRanking(type = 'all', limit = 10) {
  const params = new URLSearchParams({ ranking_type: type, limit: String(limit), fields: 'id,title,main_picture,mean,rank' });
  const res = await fetch(`https://api.myanimelist.net/v2/anime/ranking?${params}`, { headers: { 'X-MAL-CLIENT-ID': CLIENT_ID } });
  const data = await res.json();
  return data.data.map(d => d.node);
}
```

### Tidak Resmi: Jikan API v4

Gratis, tanpa API key, rate limit 30 req/menit/IP.

```js
async function jikanSearch(query, limit = 5) {
  const res = await fetch(`https://api.jikan.moe/v4/anime?q=${encodeURIComponent(query)}&limit=${limit}`);
  const data = await res.json();
  return data.data.map(a => ({ id: a.mal_id, title: a.title, image: a.images?.jpg?.image_url, score: a.score, type: a.type, episodes: a.episodes }));
}

async function jikanAnime(id) {
  const res = await fetch(`https://api.jikan.moe/v4/anime/${id}/full`);
  const { data } = await res.json();
  return { id: data.mal_id, title: data.title, synopsis: data.synopsis, score: data.score, rank: data.rank, genres: data.genres?.map(g => g.name), studios: data.studios?.map(s => s.name) };
}
```

### Scraping MAL Sendiri (Proxy API)

Bikin REST API sendiri yang scrape halaman publik MAL, expose sebagai JSON.

```js
// src/fetch.js — Rate limit dengan Bottleneck (750ms)
import Bottleneck from 'bottleneck';
const limiter = new Bottleneck({ minTime: 750, maxConcurrent: 1 });
const client = axios.create({ headers: { 'User-Agent': 'MyMALProxy/1.0 (contact: your-email@example.com)' }, timeout: 15000 });

export async function httpGet(url) {
  return limiter.schedule(async () => {
    const res = await client.get(url, { responseType: 'text' });
    return res.data;
  });
}

// src/parse.js
export function parseSearch(html) {
  const $ = cheerio.load(html);
  const items = [];
  $('.js-categories-seasonal .seasonal-anime, .hoverinfo_trigger').each((_, el) => {
    const a = block.find('a[href*="/anime/"]').first();
    const href = a.attr('href') || '';
    const m = href.match(/\/anime\/(\d+)/);
    const id = m ? Number(m[1]) : null;
    const title = a.attr('title') || a.text().trim() || null;
    const image = imgEl.attr('data-src') || imgEl.attr('src') || null;
    if (id && title) items.push({ id, title, image, score });
  });
  return { count: items.length, results: items };
}

export function parseAnimeDetail(html) {
  const $ = cheerio.load(html);
  const title = og($, 'title') || $('h1').first().text().trim();
  const image = og($, 'image');
  const synopsis = $('p[itemprop="description"]').text().trim() || $('#content p').first().text().trim();
  const score = Number($('.score-label').first().text().trim());
  const genres = []; $('a[href*="/anime/genre/"]').each((_, el) => genres.push($(el).text().trim()));
  const studios = []; $('a[href*="/anime/producer/"]').each((_, el) => studios.push($(el).text().trim()));
  return { title, image, synopsis, score, genres, studios };
}
```

## Google OAuth Error: origin_mismatch (400)

### Penyebab
- Origin aplikasi (`http://localhost:3002`) tidak terdaftar di Google Cloud Console → Authorized JavaScript origins.
- Client type salah (harus "Web application", bukan Android/iOS).
- Trailing slash di origin (`http://localhost:3002/` ❌ → `http://localhost:3002` ✅).

### Solusi

1. Buka Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client IDs.
2. Pastikan Client type = Web application.
3. Di Authorized JavaScript origins, tambahkan `http://localhost:3002`.
4. Restart dev server setelah edit `.env`.
5. Coba hard refresh / incognito.

### Setup React (CRA)

```jsx
// index.js
import { GoogleOAuthProvider } from '@react-oauth/google';
root.render(
  <GoogleOAuthProvider clientId={process.env.REACT_APP_CLIENTID}>
    <App />
  </GoogleOAuthProvider>
);

// Login.jsx
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import { useRef } from 'react';

export default function Login({ setLogin, setUser }) {
  const socketRef = useRef(null);
  useEffect(() => { socketRef.current = io(process.env.REACT_APP_SERVER); return () => socketRef.current?.disconnect(); }, []);

  const handleSuccess = (response) => {
    const data = jwtDecode(response.credential);
    setLogin(true);
    socketRef.current?.emit('login', data);
    setUser({ name: data.name, email: data.email, imageUrl: data.picture });
  };

  return <GoogleLogin theme="filled_blue" shape="circle" onSuccess={handleSuccess} onError={() => console.error('Login Failed')} />;
}
```

## CORS Error: file:// Protocol

Error: `Access to fetch at 'file:///api/...' from origin 'null' has been blocked by CORS policy`

### Penyebab
- Membuka `index.html` langsung dari file system (`file://`) bukan dari HTTP server.
- Browser memblokir fetch lintas origin jika bukan http/https.

### Solusi

1. **Gunakan live server** (VS Code extension "Live Server", atau Python `python3 -m http.server 8080`).
2. **Aktifkan CORS middleware di backend Express**:
   ```js
   const cors = require('cors');
   app.use(cors());
   ```
3. **Jangan buka `index.html` dengan `file://`**.

## Server-Sent Events (SSE)

Error: `SSE is not enabled` — biasanya muncul di log viewer atau monitoring tool.

### Setup SSE di Express

```js
app.get('/logs', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.write('data: SSE connection established\n\n');

  const interval = setInterval(() => {
    res.write(`data: ${new Date().toISOString()}\n\n`);
  }, 1000);

  req.on('close', () => { clearInterval(interval); res.end(); });
});
```

### Fallback ke Polling Jika SSE Tidak Didukung

```js
setInterval(async () => {
  const logs = await fetch('/api/logs');
  updateUI(logs);
}, 5000);
```

## Git Authentication: Hugging Face

Error: `Password authentication in git is no longer supported. You must use a user access token or an SSH key instead.`

### Solusi

**Opsi A: `huggingface-cli login`**
```bash
pip install -U huggingface_hub
huggingface-cli login --token <HF_TOKEN> --add-to-git-credential
git remote set-url origin https://huggingface.co/spaces/username/space
git push -u origin main
```

**Opsi B: Token di URL remote**
```bash
git remote set-url origin https://username:<HF_TOKEN>@huggingface.co/spaces/username/space
```

**Opsi C: SSH Key**
```bash
ssh-keygen -t ed25519 -C "email"
cat ~/.ssh/id_ed25519.pub  # Upload ke Settings → SSH keys
git remote set-url origin git@hf.co:spaces/username/space
```

## Ambil Cookies Manual

### Browser DevTools
1. Buka tab Application → Cookies → pilih domain.
2. Atau jalankan di Console: `copy(document.cookie)` (hanya cookie non-HttpOnly).

### Python (browser_cookie3)
```python
import browser_cookie3
cj = browser_cookie3.chrome(domain_name='example.com')
```

### Python (requests Session)
```python
session = requests.Session()
session.post('https://example.com/login', data={...})
cookies = session.cookies.get_dict()
```

## Base64 Decode (btoa / atob)

```js
// JavaScript
let decoded = decodeURIComponent(atob(encoded));

// Python
import base64, urllib.parse
decoded = base64.b64decode(encoded).decode('utf-8')
original = urllib.parse.unquote(decoded)
```

## Tools Cari Subdomain

- **Sublist3r**: `sublist3r -d domain.com`
- **Amass**: `amass enum -d domain.com`
- **Assetfinder**: `assetfinder --subs-only domain.com`
- **crt.sh**: `%.domain.com` di web
- **dnsdumpster.com**: Web-based DNS recon
- **Bash automation**: gabungkan hasil tool, `sort -u` untuk dedup

## Cari Username Sosial Media (Node.js)

```js
const axios = require('axios');
async function checkUsername(username) {
  const platforms = {
    Instagram: `https://www.instagram.com/${username}`,
    Twitter: `https://x.com/${username}`,
    TikTok: `https://www.tiktok.com/@${username}`,
    Threads: `https://www.threads.net/@${username}`,
    Facebook: `https://facebook.com/${username}`,
  };
  for (const [name, url] of Object.entries(platforms)) {
    try {
      const res = await axios.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 ...' }, timeout: 5000 });
      console.log(res.status === 200 ? `✅ ${name}: DITEMUKAN` : `❌ ${name}: TIDAK DITEMUKAN`);
    } catch (err) {
      console.log(err.response?.status === 404 ? `❌ ${name}: TIDAK DITEMUKAN` : `⚠️ ${name}: Error`);
    }
  }
}
```

## Related

- [[nodejs-api]] - Express backend patterns
- [[scraper-patterns]] - Cheerio scraping, anti-bot
