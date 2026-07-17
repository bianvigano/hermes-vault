# Pola Node.js Backend

Pola dan teknik backend Node.js/Express umum dari proyek ChatMVI, Discord Clone, dan scraper.

## Arsitektur Express Standar

Struktur proyek Node.js/Express dengan pola MVC:

```
project/
├── server.js          # Entry point, bootstrap Express
├── db.js              # Koneksi database
├── controllers/       # Logika bisnis
├── models/            # Mongoose / akses data
├── routes/            # Definisi rute Express
├── middleware/         # Auth, validasi, handler
├── views/             # Template EJS
├── public/            # Aset statis (CSS/JS/ikon)
├── uploads/           # Penyimpanan berkas unggahan
└── scripts/           # Utilitas
```

## Setup Express Dasar

```js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');

const app = express();
app.disable('x-powered-by');
app.use(cors());
app.use(helmet({ contentSecurityPolicy: false }));
app.use(compression());
app.use(express.json({ limit: '2mb' }));
app.use(express.urlencoded({ extended: true, limit: '2mb' }));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
```

## Middleware Auth

```js
// middleware/auth.js
function isAuthed(req) {
  return !!(req.session && req.session.user);
}
function ensureGuest(req, res, next) {
  if (isAuthed(req)) return res.redirect('/app');
  next();
}
function ensureAuthed(req, res, next) {
  if (!isAuthed(req)) return res.redirect('/');
  next();
}
function requireAdmin(req, res, next) {
  if (req.user && (req.user.isAdmin || req.user.role === 'admin')) return next();
  return res.status(403).json({ error: 'Akses ditolak. Admin saja.' });
}
function requireVerified(req, res, next) {
  if (req.user?.isVerified) return next();
  return res.status(403).json({ error: 'Akun belum diverifikasi.' });
}
module.exports = { isAuthed, ensureGuest, ensureAuthed, requireAdmin, requireVerified };
```

## Pemisahan Rute Auth

Rute auth dipisah ke file `/routes/auth.js`, dipasang via `router.use('/auth', authRoutes)`.
Middleware `ensureGuest` mencegah user login akses `/auth/login` atau `/auth/register`.

## Mongoose Schema Patterns

### UserSchema

```js
const UserSchema = new mongoose.Schema({
  name:     { type: String, trim: true, required: true, minlength: 2, maxlength: 80 },
  username: { type: String, required: true, lowercase: true, trim: true, minlength: 3, maxlength: 32, match: /^[a-z0-9_]+$/ },
  email:    { type: String, required: true, lowercase: true, trim: true, maxlength: 120, validate: { validator: v => emailRegex.test(v), message: 'Email tidak valid' } },
  passwordHash: { type: String, required: true, select: false },
  bio:      { type: String, maxlength: 280, trim: true, default: '' },
  birthdate: { type: Date },
  avatar_type: { type: String, enum: ['default', 'upload'], default: 'default' },
  avatar_url: { type: String, default: null },
  cover_url: { type: String, default: null },
  isAdmin:    { type: Boolean, default: false },
  isVerified: { type: Boolean, default: false },
  role: { type: String, enum: ['user', 'mod', 'admin'], default: 'user' },
}, { timestamps: true });
```

### RoomSchema - RoomId Unik, Nama Duplikat

```js
const RoomSchema = new mongoose.Schema({
  roomId: { type: String, unique: true, index: true, required: true }, // ID unik (URL)
  name:   { type: String, default: '', trim: true },                    // Nama tampilan (boleh sama)
  ownerId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  passwordHash: { type: String, default: null },
  topic: { type: String, default: '' },
  slowModeSec: { type: Number, default: 0 },
  pinnedMessageIds: { type: [String], default: [] },
}, { timestamps: true });

// roomId auto-generate via pre-validate
RoomSchema.pre('validate', function(next) {
  if (!this.roomId) this.roomId = Date.now().toString(36) + Math.random().toString(36).substr(2, 4);
  next();
});
```

## Socket.io Pola

### Handshake dengan Cookie

```js
io.use(async (socket, next) => {
  const cookies = parseCookies(socket.request.headers.cookie || '');
  const sid = cookies.sid || null;
  const rid = cookies.rid || 'global';
  let user = null;
  if (sid) {
    const sess = await Session.findOne({ token: sid }).lean();
    if (sess?.userId) user = await User.findById(sess.userId).lean();
  }
  socket.data.user = user || null;
  socket.data.username = user?.username || 'guest';
  socket.data.roomId = rid;
  next();
});
```

### joinRoom dan Presence in-memory

```js
const presences = new Map(); // roomId -> { users, nameToSockets, lastMsgAtByUser, tokenBuckets }

async function joinRoom(roomId, username) {
  // leave old room
  if (current.roomId) { /* cleanup */ }
  // banned check
  const r = await ensureRoomDoc(roomId, null);
  if (r.bannedUsers?.includes(username)) return;
  // join new
  current = { roomId, username };
  const p = ensurePresence(roomId);
  p.users.set(socket.id, username);
  socket.join(roomId);
  // send history + roomInfo
  socket.emit('history', { items, nextCursor });
  socket.emit('roomInfo', { topic, rules, slowModeSec, theme, pins, announcements });
  broadcastPresence(roomId);
}
```

### Bug Socket.io - Username Tertukar

Masalah: Browser kedua login sebagai "bian", kirim pesan, tapi pesan muncul sebagai "Bianvigano" (user browser pertama).

Penyebab: Socket handshake membaca cookie `sid` dan lookup user dari session. Jika dua browser berbagi cookie session sama (server session-based, bukan per-tab), maka socket.data.username akan sama.

Solusi: Gunakan `socket.data.username` dari nilai cookie `rid` + mekanisme autentikasi per socket connection yang terisolasi, bukan shared cookie session.

## Cursor Pagination (MongoDB)

```js
function packCursor(doc) {
  if (!doc) return null;
  return Buffer.from(`${new Date(doc.createdAt).toISOString()}|${String(doc._id)}`).toString('base64');
}
function unpackCursor(c) {
  if (!c) return null;
  const [iso, id] = Buffer.from(String(c), 'base64').toString('utf8').split('|');
  return { t: new Date(iso), id: new ObjectId(id) };
}

app.get('/messages', async (req, res) => {
  const cursor = unpackCursor(req.query.cursor);
  const q = { roomId };
  if (cursor) q.$or = [
    { createdAt: { $lt: cursor.t } },
    { createdAt: cursor.t, _id: { $lt: cursor.id } }
  ];
  const docs = await Message.find(q).sort({ createdAt: -1, _id: -1 }).limit(50).lean();
  const nextCursor = docs.length ? packCursor(docs[0]) : null;
  res.json({ items: docs.reverse(), nextCursor });
});
```

## File Cache Pola (SHA1 + TTL + Conditional GET)

Cache berbasis file system dengan struktur:

```js
// Key → SHA1 hash → cache/{hash}.json
function keyToFilename(key) {
  const hash = crypto.createHash('sha1').update(key).digest('hex');
  return path.join(CACHE_DIR, `${hash}.json`);
}

// Payload structure
{
  __meta: { key, createdAt, ttl, expireAt, httpMeta: { etag, lastModified } },
  data: {/* actual data */}
}

// TTL per route (ms)
const TTL = {
  manga:   3 * 60 * 1000,        // 3 menit
  search:  2 * 60 * 1000,        // 2 menit
  genre:  12 * 60 * 60 * 1000,   // 12 jam
  detail: 12 * 60 * 60 * 1000,   // 12 jam
  chapter: 3 * 60 * 60 * 1000,   // 3 jam
};

// Conditional GET dengan etag/lastModified
const httpMeta = await getCacheHttpMeta(cacheKey);
if (httpMeta) {
  if (httpMeta.etag) headers['If-None-Match'] = httpMeta.etag;
  if (httpMeta.lastModified) headers['If-Modified-Since'] = httpMeta.lastModified;
}
const resp = await http.get(url, { headers });
if (resp.status === 304) {
  await extendCacheTTL(cacheKey, ttlMs);
  return cached;
}

// Cleanup: hapus expired, LRU eviction berdasarkan mtime
setInterval(cleanupCacheDir, CACHE_CLEAN_INTERVAL).unref();
```

## Rate Limiter + Agent Pool

```js
const httpAgent  = new HttpAgent({ keepAlive: true, maxSockets: 50 });
const httpsAgent = new HttpsAgent({ keepAlive: true, maxSockets: 50 });

const http = axios.create({
  baseURL: BASE_URL,
  headers: {
    'User-Agent': 'Mozilla/5.0 ...',
    'Accept-Language': 'id-ID,id;q=0.9',
    'Referer': BASE_URL + '/'
  },
  httpAgent, httpsAgent,
  timeout: 15000,
  decompress: true,
  maxRedirects: 5,
  validateStatus: (s) => (s >= 200 && s < 300) || s === 304
});
```

## Membaca File JSON di Node.js

```js
const fs = require('fs');
const path = require('path');

// Baca semua file JSON dalam folder
const folderPath = path.join(__dirname, 'datalist');
const files = fs.readdirSync(folderPath).filter(f => f.endsWith('.json'));

files.forEach(file => {
  const raw = fs.readFileSync(path.join(folderPath, file), 'utf8');
  const data = JSON.parse(raw);
  const count = Array.isArray(data) ? data.length : Object.keys(data).length;
  console.log(`${file}: ${count} item`);
});
```

## Full-app.js: Single-file Express + MongoDB

```js
require('dotenv').config();
const express = require('express');
const { MongoClient } = require('mongodb');
const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');

async function connectDB() {
  await client.connect();
  return client.db(process.env.MONGO_DB || 'DiscordClone');
}

// Token auth via headers
async function getUserTokenUUID(conn, token) {
  const row = await conn.collection('userTokens').findOne({ token });
  return row ? row.uuid : null;
}

// Express setup
const app = express();
app.use(cors());
app.use(express.json());

// Route: user CRUD, login/logout, server CRUD, invite, message
app.use('/user', userRouter);
app.use('/server', serverRouter);
```

## PostgreSQL/Supabase: Duplicate Key Error

Error `duplicate key value violates unique constraint "files_pkey"`:

- Penyebab: INSERT dengan `id` yang sudah ada, atau sequence `SERIAL` tidak sinkron.
- Solusi: `SELECT setval('files_id_seq', (SELECT MAX(id) FROM files));`
- Atau gunakan `ON CONFLICT (id) DO UPDATE SET ...`
- Atau biarkan database auto-generate `id`, jangan kirim manual.

## ESM Import Fix

```js
// ❌ Error: Cannot find module './config/connectDB'
import connectDB from './config/connectDB';

// ✅ ESM wajib pakai ekstensi .js dan path relatif benar
import connectDB from '../config/connectDB.js';
```

## Related

- [[scraper-patterns]] - Cheerio scraping, anti-bot
- [[api-integration]] - MAL API, OAuth, CORS, SSE
