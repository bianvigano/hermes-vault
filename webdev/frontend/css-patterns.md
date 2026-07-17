# Pola CSS: Gradien, SVG, Layout, Clip-path

Kumpulan teknik CSS: gradien, SVG ke CSS, border effects, clip-path, dan tema responsif hijau.

## Gradien Linear

Gradien ungu-ke-pink kompleks dengan multi color-stop. Gunakan `linear-gradient` standar tanpa vendor prefix. Browser modern sudah support penuh.

```css
.gradien-ungu {
  background: linear-gradient(
    90deg,
    rgba(254, 140, 253, 1) 0%,
    rgba(191, 107, 219, 1) 8.93%,
    rgba(142, 81, 191, 1) 17.09%,
    rgba(106, 63, 171, 1) 24.2%,
    rgba(84, 51, 159, 1) 29.98%,
    rgba(76, 47, 155, 1) 33.71%,
    rgba(78, 48, 160, 1) 36.15%,
    rgba(85, 49, 175, 1) 39.08%,
    rgba(96, 52, 199, 1) 42.25%,
    rgba(111, 56, 232, 1) 45.58%,
    rgba(117, 58, 246, 1) 46.76%,
    rgba(153, 78, 248, 1) 52.57%,
    rgba(206, 107, 252, 1) 61.97%,
    rgba(240, 125, 254, 1) 69.03%,
    rgba(252, 132, 255, 1) 72.88%,
    rgba(253, 160, 254, 1) 79.71%,
    rgba(254, 183, 254, 1) 86.98%,
    rgba(255, 196, 253, 1) 93.89%,
    rgba(255, 201, 253, 1) 100%
  );
}
```

**Catatan penting:**
- Hapus `filter: progid:DXImageTransform.Microsoft.gradient(...)` — deprecated, khusus IE lama.
- Hapus vendor prefix `-moz-`, `-webkit-`, `-o-`, `-ms-` untuk `linear-gradient`.
- Browser modern tidak butuh prefix tersebut.

## Border Dashed + Opacity

```css
.border-ungu {
  border-style: dashed;
  border-color: rgba(199, 95, 206, 1);
  border-width: 6px;
  opacity: 0.75;
}
```

Hapus `filter: alpha(opacity=75)` — khusus IE deprecated.

## Background Image SVG sebagai Tiket Chat

Teknik menampilkan SVG sebagai background bubble chat:

```css
#message.yt-live-chat-text-message-renderer {
  display: inline-block;
  background-image: url("http://localhost:5000/Tiket.svg");
  background-repeat: no-repeat;
  background-size: 100% 100%;   /* stretch penuh */
  background-position: center;

  padding: 12px 30px 16px 34px;
  margin: 10px 0 40px 80px;

  width: auto;                  /* ikuti panjang teks */
  max-width: 90vw;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: anywhere;
}
```

**Fix masalah background terpotong:**
1. Pakai `display: inline-block` (bukan `block`) agar lebar mengikuti isi teks.
2. Pakai `background-size: 100% 100%` untuk stretch sempurna.
3. Pakai `width: auto` — jangan fixed width.
4. Tambah `overflow-wrap: anywhere` agar kata panjang tidak keluar frame.

**Integrasi dengan YouTube Live Chat:**
Gunakan selector `#author-name.yt-live-chat-author-chip` untuk badge nama:

```css
#author-name.yt-live-chat-author-chip {
  box-sizing: border-box;
  border-radius: 999px;
  color: white;
  font-weight: 600;
  background-image: url("http://localhost:5000/bm.svg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  height: 36px;
  min-width: 160px;
  padding: 0 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 0 5px #ff00ff;
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
}
```

## SVG ke CSS

Konversi atribut presentasional SVG ke aturan CSS:

```css
.path-1 { fill: #000000; }
.path-2 { fill: #FFFFFF; }
.path-3 { fill: #F4C300; }
```

Gunakan class naming seperti `.path-1`, `.g-1` untuk elemen tanpa id.

## SVG Icon Verifikasi

### Style standar (centang biru):
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="12" fill="#1D9BF0"/>
  <path d="M10.0001 14.586L17.2931 7.293L18.7071 8.707L10.0001 17.414L5.29297 12.707L6.70697 11.293L10.0001 14.586Z" fill="white"/>
</svg>
```

### Style hacker (hijau neon):
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M12 2L15.09 4.26L19.5 4.5L21 9L19.5 13.5L21 18L19.5 19.5L15.09 19.74L12 22L8.91 19.74L4.5 19.5L3 18L4.5 13.5L3 9L4.5 4.5L8.91 4.26L12 2Z" fill="#000000" stroke="#00FF88" stroke-width="1.5"/>
  <path d="M8 12.5L10.5 15L16.5 9" stroke="#00FF88" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter"/>
</svg>
```

Glow effect via CSS:
```css
.verified-hacker svg {
  filter: drop-shadow(0 0 4px #00FF88);
}
```

## Kotak Border Gradasi + Inset Shadow

```css
.fancy-box {
  width: 300px;
  height: 150px;
  padding: 15px;
  background: linear-gradient(to right, #f0c, #90f);
  border-radius: 10px;
  position: relative;
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.3);
  clip-path: polygon(10px 0%, 100% 0%, 100% 100%, 10px 100%, 0% 90%, 0% 10%);
}

.fancy-box::before {
  content: '';
  position: absolute;
  top: 4px; left: 4px; right: 4px; bottom: 4px;
  background: linear-gradient(to right, #fff, #fef9ff);
  border-radius: 6px;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.6);
  z-index: 1;
}
```

## Clip-path Polygon — Format Bersih

Pecah `clip-path: polygon(...)` kompleks ke multi-baris dengan komentar agar mudah diedit:

```css
clip-path: polygon(
  /* Start */
  5.34% 3.00%,
  5.34% 7.00%,
  ...
  93.11% 96.00%
);
```

## AI Design ke HTML/CSS

Gambar UI hasil generate AI (Midjourney, DALL·E) tidak bisa langsung diekstrak ke HTML/CSS. Alternatif:
- Konversi manual.
- Gunakan tools seperti Sketch2Code (Microsoft).
- Minta ChatGPT langsung generate HTML/CSS dari deskripsi.

## Tema Hijau Responsif (CSS Variables)

Tema hijau mobile-friendly dengan CSS custom properties:

```css
:root {
  --brand: #16a34a;
  --brand-700: #15803d;
  --brand-soft: #dcfce7;
  --bg: #f3f4f6;
  --panel: #ffffff;
  --chat-bg: #f8eeee;
  --text: #0f172a;
  --muted: #64748b;
  --border: #e5e7eb;
  --radius: 14px;
  --radius-sm: 10px;
  --shadow: 0 8px 28px rgba(2, 8, 23, .08);
}

:root[data-theme="dark"] {
  --bg: #0b0f14;
  --panel: #0f141b;
  --chat-bg: #151217;
  --text: #e5e7eb;
  --muted: #9aa4b2;
  --border: #273244;
  --shadow: 0 10px 36px rgba(0, 0, 0, .35);
}
```

**Tips responsif:**
- Gunakan `max-width: 90vw` untuk mencegah overflow layar.
- `font-size` pakai satuan relatif (`em`, `rem`).
- `display: flex` + `flex-wrap` untuk layout adaptif.

## Related

- [[html-canvas]] — HTML Canvas, game, countdown
- [[hosting-options]] — Deploy ke Vercel, Netlify, Cloudflare
