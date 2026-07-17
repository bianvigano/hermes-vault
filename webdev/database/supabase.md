# Supabase

Platform backend-as-a-service berbasis PostgreSQL dengan fitur auth real-time, API otomatis, dan penyimpanan file.

---

## Kesalahan Umum: `.insert()` Harus Berbentuk Array

Error:

```
Expected array, received object
```

Penyebab: `.insert()` menerima array, bukan objek tunggal.

### Salah

```js
const { error, data } = await supabase
  .from('files')
  .insert({
    name: file.formattedName,
    size: file.file.size,
    fileid: fdataid,
    chanid,
    dir: file.directory?.id
  })
  .select()
  .single();
```

### Benar

```js
const { error, data } = await supabase
  .from('files')
  .insert([{
    name: file.formattedName,
    size: file.file.size,
    fileid: fdataid,
    chanid: chanid,
    dir: file.directory?.id || null
  }])
  .select()
  .single();

if (error) {
  console.error("Insert error:", error.message, error.details);
}
```

### Hal yang Perlu Dicek

- Semua variabel terdefinisi (`chanid`, `fdataid`, dll).
- Kolom nullable di database cocok dengan nilai yang dikirim (cek `dir: file.directory?.id`).
- Error log ditambahkan untuk debugging.

---

## Database Migrations

Supabase menggunakan Supabase CLI untuk migrasi berbasis file SQL.

### Instal Supabase CLI

```bash
brew install supabase/tap/supabase  # Mac/Linux
```

### Login dan Link Project

```bash
supabase login
supabase link --project-ref <PROJECT_REF>
```

### Alur Kerja Migrasi

1. **Buat migrasi baru:**

```bash
supabase migration new add_users_table
```

Ini membuat `supabase/migrations/<timestamp>_add_users_table.sql`. File kosong, isi manual:

```sql
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text,
  created_at timestamp DEFAULT now()
);
```

2. **Test di lokal:**

```bash
supabase start
supabase db reset
```

3. **Deploy ke cloud:**

```bash
supabase db push --linked
```

### Diff Otomatis

Untuk membuat migrasi dari perbedaan schema:

```bash
supabase db diff -f auto_migration
```

### Rollback

Supabase tidak punya rollback otomatis. Buat migrasi baru untuk undo:

```sql
DROP TABLE users;
```

### Ringkasan Perintah

| Tujuan | Perintah |
|--------|----------|
| Migrasi otomatis | `supabase db diff -f <nama>` |
| Pull schema dari cloud | `supabase db pull` |
| Migrasi kosong manual | `supabase migration new <nama>` |
| Deploy | `supabase db push` |

---

## Multiple URLs Setup (Dua Proyek Supabase)

Bisa pakai dua proyek Supabase terpisah dalam satu aplikasi, misal proyek A untuk auth dan proyek B untuk data.

### Setup Dua Client

`supabaseAuthClient.js`:

```js
import { createClient } from '@supabase/supabase-js'

export const supabaseAuth = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_AUTH_URL,
  process.env.NEXT_PUBLIC_SUPABASE_AUTH_KEY
)
```

`supabaseDataClient.js`:

```js
import { createClient } from '@supabase/supabase-js'

export const supabaseData = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_DATA_URL,
  process.env.NEXT_PUBLIC_SUPABASE_DATA_KEY
)
```

`.env`:

```
NEXT_PUBLIC_SUPABASE_AUTH_URL=https://gjjkdgwptvmiqmtspcre.supabase.co
NEXT_PUBLIC_SUPABASE_AUTH_KEY=xxxx

NEXT_PUBLIC_SUPABASE_DATA_URL=https://kxjeazwigucdvrcanvzo.supabase.co
NEXT_PUBLIC_SUPABASE_DATA_KEY=xxxx
```

### Masalah: `auth.uid()` Lintas Proyek Tidak Berfungsi

`auth.uid()` hanya bekerja di proyek tempat auth diaktifkan. Jika tabel di proyek B pakai `default auth.uid()`, nilainya akan null.

### Solusi: Kirim user.id Manual

```js
// Ambil user dari proyek Auth
const { data: { user } } = await supabaseAuth.auth.getUser()

// Insert ke proyek Data dengan user.id manual
await supabaseData.from("files").insert({
  name,
  size,
  fileid,
  userid: user.id,  // kirim manual
  chanid
})
```

Ubah kolom `userid` di proyek B menjadi tanpa default:

```sql
userid uuid NOT NULL  -- tanpa default auth.uid()
```

### Arsitektur Aman (2 Proyek)

```
Frontend
   ↓ (Auth via Proyek A)
Supabase Auth (A)
   ↓ (user.id)
API Route Next.js
   ↓ (Insert server-side dengan service key)
Supabase Data (B)
```

Gunakan API route sebagai gateway, jangan expose service key ke frontend.

---

## Related

- [[mongodb-setup]]
- [[redis-upstash]]
- [[index]]
