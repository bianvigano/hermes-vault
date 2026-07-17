# Opsi Hosting: Vercel, Netlify, Cloudflare, Vite, PM2

Panduan deploy website — Vite build tool, PM2 process manager, Vercel, Netlify, Cloudflare, dan hosting gratis.

## Vite — Build Tool Cepat

Vite adalah build tool modern cepat untuk frontend (React, Vue, Vanilla JS). Keunggulan: HMR cepat, konfigurasi minimal.

### Instalasi
```bash
npm create vite@latest
```

Ikuti prompt: nama proyek → framework → varian.

```bash
cd my-app
npm install
```

### Jalankan
```bash
npm run dev
# → http://localhost:5173
```

### Build produksi
```bash
npm run build
# → hasil di folder dist/
```

## PM2 — Process Manager untuk Node.js

Jalankan aplikasi di background dengan auto-restart:

```bash
pm2 start "npm run dev -- --host" --name nama-aplikasi
```

Atau untuk file langsung:
```bash
pm2 start server.js --name nama-aplikasi
```

### Perintah penting:
```bash
pm2 list              # cek semua proses
pm2 logs nama-aplikasi # lihat log
pm2 startup            # auto-start saat boot
pm2 save               # simpan konfigurasi
```

## Vercel — Hosting Frontend Modern

### Kelebihan
- Deploy cepat via integrasi Git (GitHub, GitLab, Bitbucket).
- Optimasi framework modern (Next.js, React, Svelte, Vue).
- Auto-scaling serverless + edge network.
- CDN global — rendah latensi.
- Fitur preview deployment, rollback mudah.
- Plan gratis (Hobby) cukup untuk prototipe.

### Kekurangan
- Biaya naik cepat untuk skala besar.
- Kurang cocok untuk backend stateful/WebSocket intensif.
- Cold start dan batasan durasi fungsi serverless.
- Logging/error tracking kadang kurang memadai.
- Vendor lock-in.

### Kapan pakai Vercel?
- Proyek front-end statis/semi-dinamis.
- Fokus kode tanpa kelola infrastruktur.
- Tim kecil/startup.
- Trafik naik-turun butuh auto-scaling.
- Butuh deployment preview dan kolaborasi.

## Batasan Akun Gratis Vercel

Plan Hobby (gratis):
- CPU aktif: 4 CPU-jam per bulan
- Memori: 360 GB-jam per bulan
- Fungsi serverless: 1.000.000 permintaan per bulan
- Fast Data Transfer: 100 GB per bulan
- Web Analytics: 50.000 event per bulan
- Log runtime disimpan 1 jam

Jika kuota habis: situs mungkin **di-offline** sementara sampai periode reset (~30 hari). Tidak ada penagihan otomatis.

Domain gratis: `*.vercel.app`

## Netlify — Hosting Statis + Serverless

### Fitur gratis:
- Gratis selamanya, tanpa kartu kredit.
- Deploy dari Git, auto build & deploy.
- SSL gratis (HTTPS).
- Subdomain gratis `*.netlify.app`.
- Serverless functions (Node.js).

### Batasan:
- Jika penggunaan melebihi kuota, situs ditangguhkan sampai bulan depan.
- Fitur analytics lengkap, kolaborasi tim, support prioritas — bayar.

### Apakah bisa Node.js full?
**TIDAK** bisa `node server.js` dengan `app.listen(3000)`. Alternatif: **Serverless Functions** — handler backend `.js` dengan batasan.

## Cloudflare — DNS + Redirect

### Redirect domain lama ke baru via Cloudflare:

1. Tambahkan domain lama ke akun Cloudflare.
2. Atur DNS record (A record ke IP dummy `192.0.2.1`, Proxied).
3. Buat Redirect Rule:
   - Kondisi: `jijahaulia1x2-p.hf.space/*`
   - Aksi: Forwarding URL (301) ke `https://x1m.mvi.my.id/$1`
4. Tunggu propagasi, cek di browser.

## Hosting Gratis untuk Domain Sendiri

Untuk domain `mvi.my.id`:

| Platform     | Cocok untuk                       | Custom Domain |
|-------------|-----------------------------------|---------------|
| Netlify     | Situs statis, landing page       | Ya            |
| Vercel      | Frontend framework (Next.js dll) | Ya            |
| GitHub Pages| Website statis                   | Ya            |
| Cloudflare  | DNS, redirect, CDN               | Ya            |

Subdomain dan email tidak mengganggu — domain tetap bisa digunakan untuk website utama.

## Node.js + NVM + Yarn — Instalasi

### Install NVM (Linux/macOS):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Restart terminal, cek: `nvm --version`

### Install Node.js via NVM:
```bash
nvm install --lts
nvm use --lts
node -v
npm -v
```

### Install Yarn:
```bash
npm install -g yarn
yarn --version
```

### Troubleshooting versi Node:
Jika error `EBADENGINE Unsupported engine`:
- Cek `package.json` — dependency butuh versi Node tertentu (`>=21.0.0`).
- Gunakan `FROM node:22-slim` di Dockerfile.
- Atau: `nvm install 22 && nvm use 22`.

## Related

- [[css-patterns]] — CSS patterns, gradien, SVG, layout
- [[html-canvas]] — HTML Canvas, game, countdown
