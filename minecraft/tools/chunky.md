# Chunky — Minecraft Chunk Pre-Generator

Plugin untuk pre-generate chunk di Minecraft server (Spigot/Paper/Fabric/Forge/NeoForge/Sponge).

**Versi terbaru**: 1.4.40
**Author**: pop4959
**Download**: https://www.spigotmc.org/resources/chunky.81534/
**Modrinth**: https://modrinth.com/plugin/chunky
**GitHub**: https://github.com/pop4959/Chunky
**Companion**: ChunkyBorder — worldborder otomatis mengikuti Chunky (https://modrinth.com/plugin/chunkyborder)

---

## Kenapa Pakai Chunky?

Pre-generate chunk = chunk sudah jadi SEBELUM pemain eksplor. Tanpa pre-generate, server generate chunk real-time → TPS turun, lag saat eksplorasi.

## Instalasi

1. Download `.jar` dari SpigotMC atau Modrinth
2. Masukkan ke folder `plugins/`
3. Restart server (`/reload` bisa, restart lebih aman)
4. Verifikasi: `/chunky` — muncul help = aktif

## Command Penting

| Command | Fungsi |
|---------|--------|
| `/chunky world [world]` | Pilih world (world, world_nether, world_the_end) |
| `/chunky radius [N]` | Set radius blok dari center |
| `/chunky shape [circle/square]` | Bentuk area (default: circle) |
| `/chunky center [X] [Z]` | Titik pusat generate |
| `/chunky start` | Mulai pre-generate |
| `/chunky pause` | Jeda |
| `/chunky continue` | Lanjut |
| `/chunky cancel` | Batalkan |
| `/chunky progress` | Cek progress |
| `/chunky info` | Cek setting aktif |
| `/chunky limit [N]` | Batasi chunk per tick (50-100 aman) |
| `/chunky worldborder` | Ikuti worldborder vanilla (auto set center + radius) |
| `/chunky spawn` | Set center ke spawn world |
| `/chunky silent` | Matikan notifikasi selesai task |

## Default Values

| Setting | Default |
|---------|---------|
| Radius | 1000 block |
| Shape | Circle |
| World | World aktif (world pemain berdiri) |
| Center | Spawn |
| Chunk limit | Unlimited |

## WorldBorder + Chunky (Best Practice)

Chunky + WorldBorder = cara paling rapi:

```bash
/worldborder set 10000
/chunky worldborder
/chunky start
```

**Rumus**: `WorldBorder = Radius × 2`
- `worldborder set 8000` = Radius 4000
- `Radius 29.999.984` = Worldborder 59.999.968 (limit maksimal Minecraft)

## Rekomendasi Ukuran per Server

| Tujuan | WorldBorder |
|--------|-------------|
| SMP kecil | 5.000 – 10.000 |
| SMP menengah | 10.000 – 20.000 |
| SMP besar | 30.000 – 50.000 |
| Extreme | 100.000+ (tidak disarankan) |

## Tips Performa

- Jalankan saat server sepi (1 pemain atau kosong)
- SSD wajib — HDD bottleneck parah
- Set limit rendah (50-100) biar pemain online ga keganggu
- Radius 5000 dengan limit 100 ≈ 1-2 jam
- Jangan generate 30M radius kecuali dedicated server kelas berat (ratusan GB storage, berhari-hari)

## ⚠️ Pitfall

- Chunky SELALU butuh batas area — ga bisa generate tanpa radius/worldborder
- `/chunky radius -[N]` = mengKECILkan radius yang sudah diset (bukan set negatif)
- FAWE (FastAsyncWorldEdit) bisa bentrok dengan Chunky jika versi ga cocok atau config rusak
- Jangan generate terlalu agresif saat pemain online — TPS bisa drop

## Related

- [[minecraft/server/worldborder-chunky]] — WorldBorder + Chunky workflow
- [[minecraft/plugin/fawe-troubleshooting]] — FAWE error & bentrok plugin
- [[minecraft/server/minecraft-docker-setup]] — Docker Compose Minecraft
- [[minecraft/server/server-settings]] — server.properties config reference
- [[minecraft/plugin/luckperms]] — Permission management
- [[minecraft/tools/geyser-velocity]] — Bedrock-Java crossplay
