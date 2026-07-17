# Gamerules — Daftar dan Penggunaan Game Rules Minecraft

Panduan lengkap `/gamerule` untuk mengontrol perilaku dunia Minecraft. Mencakup daftar gamerule penting, perubahan di versi 1.21+, dan penggunaan di server.

## Apa Itu Gamerule?

Gamerule adalah pengaturan yang mengontrol **perilaku dunia Minecraft secara dinamis** — bisa diubah saat server berjalan, tidak perlu restart. Berbeda dengan `server.properties` yang hanya bisa diubah saat server mati.

Semua gamerule diset dan dibaca via command:

```minecraft
/gamerule <nama>            # Lihat nilai saat ini
/gamerule <nama> <nilai>    # Set nilai baru
/gamerule                   # Lihat daftar semua gamerule yang tersedia
```

## Gamerule Paling Penting

### Waktu & Siklus

```minecraft
/gamerule doDaylightCycle false   # Hentikan siklus siang-malam
/gamerule doDaylightCycle true    # Kembalikan siklus normal
/gamerule doWeatherCycle false    # Hentikan siklus cuaca
/gamerule doWeatherCycle true     # Kembalikan siklus cuaca normal
```

**Penting 1.21+**: `doDaylightCycle` masih ada dan berfungsi. Case-sensitive — D dan C harus huruf besar.

```minecraft
/gamerule doDaylightCycle false   # ✓ Benar
/gamerule dodaylightcycle false   # ✗ Salah — "Unknown gamerule"
```

### Spawn

```minecraft
/gamerule spawnRadius 0           # Spawn tepat di 1 titik
/gamerule spawnRadius 10          # Default: spawn menyebar ±10 blok
```

### Survival & Inventory

```minecraft
/gamerule keepInventory true      # Inventory tetap saat mati
/gamerule naturalRegeneration true # Regenerasi darah alami (default)
/gamerule naturalRegeneration false # Matikan regen (UHC/hardcore style)
/gamerule doImmediateRespawn true  # Langsung respawn tanpa layar kematian
```

### Mob & Lingkungan

```minecraft
/gamerule doMobSpawning false     # Matikan spawn mob
/gamerule doMobSpawning true      # Default
/gamerule mobGriefing false       # Creeper/TNT tidak merusak blok
/gamerule doFireTick false        # Api tidak menyebar
/gamerule doTileDrops false       # Blok tidak drop item saat dirusak
```

### Player & PvP

```minecraft
/gamerule pvp false               # Matikan PvP (damage antar pemain)
/gamerule keepInventory true      # Simpan inventory saat mati
/gamerule showDeathMessages false # Sembunyikan pesan kematian
```

### Command & Teknis

```minecraft
/gamerule commandBlockOutput false  # Matikan output command block di chat
/gamerule sendCommandFeedback false # Matikan feedback command di chat
/gamerule logAdminCommands false    # Jangan log command admin
/gamerule maxCommandChainLength 65536 # Panjang maksimum rantai command block
```

## Perubahan di Minecraft 1.21+

Minecraft 1.21.11 melakukan **rename gamerule ke format snake_case** untuk konsistensi. Gamerule lama masih berfungsi tapi mungkin deprecated di versi mendatang.

| Nama Lama (Pre-1.21) | Nama Baru (1.21.11+) | Fungsi |
|-----------------------|----------------------|--------|
| `doDaylightCycle` | `do_daylight_cycle` | Siklus siang-malam |
| `doWeatherCycle` | `do_weather_cycle` | Siklus cuaca |
| `doMobSpawning` | `do_mob_spawning` | Spawn mob |
| `mobGriefing` | `mob_griefing` | Mob merusak blok |
| `keepInventory` | `keep_inventory` | Simpan inventory saat mati |
| `doFireTick` | `do_fire_tick` | Api menyebar |
| `doTileDrops` | `do_tile_drops` | Blok drop item |
| `naturalRegeneration` | `natural_regeneration` | Regen darah alami |
| `commandBlockOutput` | `command_block_output` | Output command block |
| `sendCommandFeedback` | `send_command_feedback` | Feedback command |
| `spawnRadius` | `spawn_radius` | Radius spawn |
| `doImmediateRespawn` | `do_immediate_respawn` | Respawn instan |

**Tips**: Ketik `/gamerule` di game untuk melihat daftar lengkap nama yang valid di versimu.

## Cara Membuat Siang Terus (Permanent Day)

### Metode 1: Gamerule (Rekomendasi)

```minecraft
/gamerule doDaylightCycle false
/time set day
```

- `doDaylightCycle false` → menghentikan waktu (matahari berhenti)
- `time set day` → set ke siang (1000 ticks)

Kembali normal:
```minecraft
/gamerule doDaylightCycle true
```

### Metode 2: Command Block (Fallback)

Kalau gamerule tidak tersedia (server dibatasi):

1. `/give @p command_block`
2. Taruh command block
3. Isi: `/time set day`
4. Mode: **Repeat** + **Always Active**

Command block akan memaksa waktu selalu kembali ke siang setiap tick. Boros CPU untuk penggunaan jangka panjang.

### Metode 3: Plugin (Untuk Server Production)

Denizen Script:
```yaml
on server start:
    - set_gamerule doDaylightCycle false
    - set_time day
```

Java Bukkit API:
```java
world.setGameRule(GameRule.DO_DAYLIGHT_CYCLE, false);
world.setTime(1000);
```

## Setup Server Selalu Siang

1. Pastikan cheat/command aktif (server harus enable command)
2. Jalankan `/gamerule doDaylightCycle false`
3. Jalankan `/time set day`
4. Untuk permanen: tambahkan command ke script startup server atau plugin

## Troubleshooting

### "Unknown gamerule"

- Cek case sensitivity: `doDaylightCycle` bukan `dodaylightcycle`
- Coba nama baru (1.21+): `/gamerule do_daylight_cycle false`
- Ketik `/gamerule` untuk daftar yang tersedia di versimu

### Gamerule Reset Setelah Restart

- Gamerule **disimpan di world**, bukan di `server.properties`. Harusnya persisten.
- Beberapa plugin mungkin override gamerule di event start
- Cek `level.dat` — gamerule tersimpan di dalam file world

### Gamerule Berbeda per World

Gamerule tersimpan per-world. Pakai `/minecraft:gamerule` di world yang dituju, atau plugin seperti Multiverse untuk set per-world.

## Related

- [[minecraft/server/server-properties]] — Konfigurasi server.properties (beda: perlu restart)
- [[minecraft/gameplay/daylight-cycle]] — Fokus spesifik cara set siang terus
- [[minecraft/server/set-spawn]] — Set spawn dan spawnRadius
- [[minecraft/tools/custom-seed]] — Seed kustom untuk world baru
- [[minecraft/server/minecraft-docker]] — Setup server via Docker
