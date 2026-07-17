# HTML Canvas: Game, Countdown, Bubble Glow

Kumpulan contoh HTML Canvas, game 2 player, countdown ulang tahun, dan efek bubble glow.

## Bubble Glow Pill

Pill kapsul dengan gradien ungu-pink-kuning dan efek neon glow.

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neon Glow Pill</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background-color: #000;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      font-family: Arial, sans-serif;
    }
    .glow-pill {
      width: 800px;
      height: 120px;
      border-radius: 999px;
      background: linear-gradient(to right, #b400f5, #8d2cae, #1f0c3b, #e9e58b);
      box-shadow:
        0 0 40px 10px rgba(208, 98, 248, 0.6),
        0 0 80px 20px rgba(255, 255, 255, 0.05) inset;
      filter: blur(0.3px);
      position: relative;
    }
    .glow-pill::after {
      content: '';
      position: absolute;
      inset: 0;
      border-radius: inherit;
      background-image: url("https://www.transparenttextures.com/patterns/dark-mosaic.png");
      opacity: 0.05;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div class="glow-pill"></div>
</body>
</html>
```

**Penjelasan efek:**
- `border-radius: 999px` → bentuk kapsul.
- `linear-gradient(to right, ...)` → gradien horizontal.
- `box-shadow` → efek neon glow luar dan dalam.
- `filter: blur(0.3px)` → efek lembut.

## Bubble Nama Neon

Pill dengan teks nama di dalamnya:

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Bubble Nama Neon</title>
  <style>
    body {
      background-color: #000;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      font-family: Arial, sans-serif;
    }
    .bubble-nama {
      padding: 30px 80px;
      border-radius: 999px;
      background: linear-gradient(to right, #ff00ff, #6b0080, #1a001a, #e9e58b);
      color: white;
      font-size: 28px;
      font-weight: bold;
      position: relative;
      box-shadow:
        0 0 60px 20px rgba(255, 0, 255, 0.4),
        0 0 100px 40px rgba(255, 0, 255, 0.1);
      text-align: center;
      overflow: hidden;
    }
    .bubble-nama::before {
      content: '';
      position: absolute;
      inset: -10px;
      border-radius: inherit;
      background: inherit;
      filter: blur(20px);
      opacity: 0.5;
      z-index: -1;
    }
  </style>
</head>
<body>
  <div class="bubble-nama">Bian Haryanto</div>
</body>
</html>
```

## Game 2 Player dengan HTML + CSS + JavaScript

Konsep game 2 player turn-based bisa dibuat dengan HTML/CSS/JS. Untuk online multiplayer gunakan Node.js + Socket.io.

**Fitur utama:**
- 2 player (local multiplayer di 1 device).
- Turn-based system: Player 1 → Player 2 → ulang.
- Game board digital dengan token/pion.
- Interaksi klik/tap.
- Penentuan pemenang berdasarkan skor/target.

**Teknologi:**
- Frontend: HTML, CSS, JavaScript (Canvas atau DOM).
- Backend (opsional online): Node.js + Socket.io.

## Countdown Ulang Tahun HTML

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Hitung Mundur Ulang Tahun</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .countdown {
      text-align: center;
      background: #1e293b;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .time { font-size: 24px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="countdown">
    <h1>Hitung Mundur Ulang Tahun</h1>
    <p class="time" id="timer">Memuat...</p>
  </div>

  <script>
    function updateCountdown() {
      const now = new Date();
      let target = new Date(now.getFullYear(), 0, 18); // 18 Januari

      if (now >= target) {
        target = new Date(now.getFullYear() + 1, 0, 18);
      }

      const diff = target - now;
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);

      document.getElementById("timer").innerHTML =
        `${days} hari ${hours} jam ${minutes} menit ${seconds} detik`;
    }

    setInterval(updateCountdown, 1000);
    updateCountdown();
  </script>
</body>
</html>
```

**Logika:**
- Target = 18 Januari tahun ini.
- Jika hari ini sudah lewat/tanggal target, hitung ke tahun depan.
- Update setiap detik dengan `setInterval`.

## CLI ke Website

Mengubah program CLI menjadi website:

1. Bungkus logika program ke dalam fungsi.
2. Buat web server dengan Flask (Python) atau Express (Node.js).
3. Buat halaman HTML untuk input/output.

Contoh Flask:
```python
from flask import Flask, request, render_template
from your_program import proses_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = ""
    if request.method == "POST":
        data = request.form["input_user"]
        hasil = proses_data(data)
    return render_template("index.html", hasil=hasil)

app.run(debug=True)
```

## Related

- [[css-patterns]] — Pola CSS, gradien, SVG, layout
- [[hosting-options]] — Deploy website ke Vercel, Netlify, Cloudflare
