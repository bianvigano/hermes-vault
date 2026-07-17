# Discord Webhook

Webhook Discord = endpoint HTTP untuk kirim pesan ke channel tanpa bot. Satu arah (kirim doang, tidak bisa baca chat).

---

## Kemampuan Webhook

| Fitur | Status | Catatan |
|-------|--------|---------|
| Kirim pesan teks | ✅ | POST ke webhook URL |
| Upload file | ✅ | Attachment pesan, max 25MB |
| Edit pesan sendiri | ✅ | PATCH + message_id, HARUS simpan message_id |
| Custom username/avatar | ✅ | Set di body request |
| Embed message | ✅ | Warna, field, thumbnail, image |
| Baca chat/event | ❌ | Tidak subscribe gateway |
| Edit pesan orang lain | ❌ | Cek ownership Discord |
| Interaksi/command | ❌ | Webhook tidak punya state |

## Storage via Webhook

Webhook bisa dipakai sebagai "database cheap" — store file, edit, append:

```js
const WEBHOOK_URL = process.env.WEBHOOK_URL;
const MAX_CHUNK_BYTES = 5 * 1024 * 1024; // 5MB limit Discord

// Create file
async function createFile(filename, buffer) {
    const form = new FormData();
    form.append("payload_json", JSON.stringify({}));
    form.append("files[0]", new Blob([buffer]), filename);
    
    const res = await fetch(`${WEBHOOK_URL}?wait=true`, { method: 'POST', body: form });
    const msg = await res.json();
    return { messageId: msg.id, size: buffer.length };
}

// Edit file (replace)
async function editFile(messageId, filename, buffer) {
    const form = new FormData();
    form.append("payload_json", JSON.stringify({}));
    form.append("files[0]", new Blob([buffer]), filename);
    
    await fetch(`${WEBHOOK_URL}/messages/${messageId}?wait=true`, { method: 'PATCH', body: form });
}

// Read file
async function readFile(messageId) {
    const msg = await fetch(`${WEBHOOK_URL}/messages/${messageId}`).then(r => r.json());
    const att = msg.attachments[0];
    if (!att) return Buffer.alloc(0);
    
    const res = await fetch(att.url);
    return Buffer.from(await res.arrayBuffer());
}

// Append data
async function appendToFile(messageId, filename, data) {
    const old = await readFile(messageId);
    const next = Buffer.concat([old, Buffer.from(data)]);
    if (next.length > MAX_CHUNK_BYTES) throw new Error("Append exceeds MAX_CHUNK_BYTES");
    await editFile(messageId, filename, next);
}
```

**Alur edit pesan:**
1. Kirim pesan dengan `?wait=true` → Discord balikin `message_id`
2. SIMPAN `message_id` (database, file, cache)
3. Edit: PATCH ke `{WEBHOOK_URL}/messages/{message_id}`
4. Tanpa `message_id` → tidak bisa edit

## Webhook vs Bot

| | Webhook | Bot |
|---|---------|-----|
| Arah | Satu arah (kirim) | Dua arah (baca + respon) |
| Install | Buat di channel settings | Invite via OAuth2 |
| Baca chat | ❌ | ✅ |
| Command | ❌ | ✅ |
| Edit pesan | Hanya milik sendiri | Hanya milik sendiri |
| Kompleksitas | Rendah | Tinggi |

**Analogi**: Webhook = pengeras suara otomatis (bisa ngomong, ga bisa dengar). Bot = orang di ruangan (bisa dengar + jawab).

## Use Case

- Notifikasi otomatis (order baru, server down, CI/CD)
- Integrasi GitHub, Stripe, trading bot
- Daily report / summary
- Logging error aplikasi
- Mini database (state, cache, progress)
- Zapier/Make/IFTTT workflow

## Pitfall

- Tidak ada way untuk baca chat sama sekali
- `?wait=true` WAJIB kalau mau dapat `message_id` untuk edit nanti
- Max upload 25MB (attachment), 5MB untuk storage pattern per chunk
- Webhook tidak punya role/permission — hanya bisa kirim sebatas channel permission

## Related

- [[discord/bot/discordjs-bot]] — Bot development dengan discord.js
- [[discord/bot/permissions]] — Setting role & permission Discord
