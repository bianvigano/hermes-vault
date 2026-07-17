# Daylight Cycle — Cara Set Siang Terus

Menghentikan siklus siang-malam di Minecraft (Versi Java & Bedrock, 1.21+).

## Command Utama

```
/gamerule doDaylightCycle false
/time set day
```

- `doDaylightCycle false` — menghentikan pergerakan waktu (matahari tidak bergerak)
- `time set day` — set waktu ke siang (1000 ticks)

Balik normal:

```
/gamerule doDaylightCycle true
```

## Catatan Penting Versi 1.21+

Gamerule `doDaylightCycle` **MASIH ADA** di 1.21.11. Syntax:

- Case sensitive: `doDaylightCycle` (D dan C besar)
- Cek daftar gamerule yang tersedia: ketik `/gamerule` saja

## Alternatif Kalau Gamerule Tidak Tersedia

Pakai command block:

1. `/give @p command_block`
2. Taruh command block
3. Isi: `/time set day`
4. Set ke **Repeat** + **Always Active**

Ini akan memaksa waktu selalu kembali ke siang setiap tick. Kurang efisien tapi selalu works.

## Cara Aktifkan Cheat

**Singleplayer:**
1. Pause → Open to LAN → Allow Cheats: ON → Start LAN World

**Bedrock:**
1. Settings → Edit World → Activate Cheats

## Troubleshooting

### "Unknown gamerule"

- Cek huruf besar-kecil: harus `doDaylightCycle` (bukan `dodaylightcycle`)
- Pakai `/gamerule` untuk lihat daftar lengkap
- Beberapa server Bedrock mungkin menggunakan nama berbeda — cek dokumentasi versi

### Gamerule tidak muncul di daftar

- Pastikan versi Minecraft mendukung: semua versi modern (1.8+) punya gamerule ini
- Di server tertentu, plugin mungkin membatasi akses gamerule

## Setup Permanent (Server)

Untuk server yang selalu siang:

1. Edit `server.properties` tidak bisa set ini
2. Gunakan plugin atau command block repeat
3. Alternatif: buat script startup yang menjalankan command via console:
```
# Di startup script server
echo "gamerule doDaylightCycle false" >> server-console
echo "time set day" >> server-console
```

## Penggunaan di Plugin/Mod

### Denizen Script
```yaml
on server start:
    - set_gamerule doDaylightCycle false
    - set_time day
```

### Plugin Java (Bukkit API)
```java
world.setGameRule(GameRule.DO_DAYLIGHT_CYCLE, false);
world.setTime(1000);
```

## Related

- [[server/server-properties]] — Konfigurasi server.properties
- [[server/spawn-commands]] — Set spawn dunia
- [[gameplay/denizen-basics]] — Alternatif via Denizen script
