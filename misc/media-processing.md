# ffmpeg & Media Processing

Referensi pemrosesan media — kompresi video, screenshot, multi-resolusi, audio streaming.

---

## ffmpeg — Video & Audio CLI

### Info Video (ffprobe)

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

### Convert Resolusi (Downscale)

```bash
# Satu resolusi
ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4

# Multi resolusi sekaligus
ffmpeg -i input.mp4 \
  -filter:v:0 scale=1920:1080 -c:v:0 libx264 output_1080p.mp4 \
  -filter:v:1 scale=1280:720 -c:v:1 libx264 output_720p.mp4 \
  -filter:v:2 scale=854:480 -c:v:2 libx264 output_480p.mp4
```

### Screenshot dari Video

```bash
ffmpeg -i video.mp4 -ss 00:00:10 -vframes 1 screenshot.jpg
```

## Resolusi Video — Reference

| Nama | Resolusi | Penggunaan |
|------|----------|-----------|
| 4K (UHD) | 3840×2160 | Upscale AI |
| Full HD | 1920×1080 | Standar |
| HD (720p) | 1280×720 | Ringan |
| SD (480p) | 854×480 | Koneksi lambat |
| 360p | 640×360 | Data minim |

**Pententuan kualitas**: resolusi + bitrate + codec (H.264, H.265, VP9, AV1).

## Website Video dengan Multi-Resolusi

### HTML + JS (Manual Dropdown)

```html
<video id="player" width="640" controls>
  <source id="videoSource" src="video-1080p.mp4" type="video/mp4">
</video>

<select id="qualitySelect">
  <option value="video-1080p.mp4">1080p</option>
  <option value="video-720p.mp4">720p</option>
  <option value="video-480p.mp4">480p</option>
</select>

<script>
  select.addEventListener("change", () => {
    const time = player.currentTime;
    source.src = select.value;
    player.load();
    player.currentTime = time;
    player.play();
  });
</script>
```

### HLS Adaptive Streaming

```html
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<video id="video" controls></video>
<script>
  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource('master.m3u8');
    hls.attachMedia(video);
  }
</script>
```

⚠️ Browser TIDAK otomatis downscale — harus sediakan file terpisah per resolusi.

## Node.js: fluent-ffmpeg

```js
import ffmpeg from "fluent-ffmpeg";

// Screenshot
ffmpeg("video.mp4")
  .screenshots({
    count: 1,
    timestamps: ['10%'],
    folder: './thumbs'
  });

// ffprobe metadata
ffmpeg.ffprobe("video.mp4", (err, metadata) => {
  console.log(metadata.format.duration);
});
```

## DistubeError FFMPEG (Discord Music Bot)

Error ini muncul saat bot Discord pakai `disTube` atau `discord-player` gagal streaming karena ffmpeg tidak ditemukan.

Fix:
```bash
sudo apt install ffmpeg -y
which ffmpeg  # pastikan ada di PATH
```

Atau install `@distube/ytdl-core` + `ffmpeg-static`.

## Kompresi Backup Linux

| Format | Ukuran | Kecepatan | Rekomendasi |
|--------|--------|-----------|-------------|
| zip | Biasa | Cepat | Kompatibel |
| tar.gz | Lebih kecil | Cepat | Standar |
| tar.xz | Sangat kecil | Lambat | Arsip lama |
| **tar.zst** | Kecil + Cepat | Cepat | ⭐ TERBAIK |

```bash
# zstd (recommended)
tar --zstd -cvf backup-$(date +%F).tar.zst folder/

# zip with password
zip -r -e backup.zip folder/

# tar.gz daily
tar -czvf backup-$(date +%Y-%m-%d).tar.gz folder/
```

## Related

- [[webdev/frontend/html-canvas]] — Video player UI
- [[linux/network/server-security]] — Server + cron backup
