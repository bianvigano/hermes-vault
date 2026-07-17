# Chunk Minecraft — Ukuran dan Perhitungan Blok

Spesifikasi teknis chunk Minecraft: ukuran, jumlah blok, dan perhitungan terkait.

## Ukuran Dasar 1 Chunk

- Lebar: **16 blok**
- Panjang: **16 blok**
- Tinggi: tergantung versi

## Jumlah Blok per Chunk

### Minecraft 1.18+ (Caves & Cliffs)

- Tinggi: **Y -64 sampai Y 319** = **384 blok**
- Total: `16 × 16 × 384` = **98.304 blok**

### Sebelum 1.18

- Tinggi: **Y 0 sampai Y 256** = **256 blok**
- Total: `16 × 16 × 256` = **65.536 blok**

## Perhitungan Bytes/Storage

1 chunk ≈ 98.304 blok. Setiap blok butuh beberapa byte storage:
- Block ID: ~1-2 byte
- Block state data: 2-4 byte
- Block entity (chest, furnace, dll): bervariasi
- Lighting data: 0.5 byte per blok rata-rata

Estimasi kasar per chunk: **4-8 KB** (tanpa block entity). Dunia 10.000×10.000 blok = ~390.625 chunk = **1.5-3 GB** storage.

## Konversi Ukuran (JavaScript → Bash)

```js
const oldChunkSize = 8 * 1024 ** 2;   // JS: 8 * (1024^2) = 8388608 byte = 8 MB
```

Di bash:
```bash
oldChunkSize=$((8 * 1024 * 1024))     # hasil: 8388608
```

Atau dengan variabel:
```bash
MB=$((1024 * 1024))
oldChunkSize=$((8 * MB))
```

Bash tidak punya operator `**`. Gunakan perkalian manual di dalam `$(( ))`.

## Pre-Generation dengan Chunky

Untuk pre-generate chunk (hindari lag eksplorasi), lihat [[tools/chunky]].

Radius Chunky = setengah dari `max-world-size`:
```
max-world-size=50000   →  /chunky radius 25000
max-world-size=10000   →  /chunky radius 5000
```

## Related

- [[tools/chunky]] — Pre-generate chunk
- [[server/server-properties]] — max-world-size
- [[server/docker-compose-8gb]] — Setup 8GB RAM
