# Set Spawn — Mengatur Titik Spawn Server Minecraft

Panduan lengkap mengatur spawn dunia dan spawn pemain menggunakan command vanilla dan plugin. Mencakup perilaku bed respawn, server.properties, dan troubleshooting.

## Command Vanilla (Berlaku Semua Platform)

Semua command di bawah berlaku untuk: **Vanilla, Bukkit, Spigot, Paper, Purpur, Fabric, Forge, NeoForge, Quilt**.

### `/setworldspawn` — Set Spawn Dunia

```minecraft
/setworldspawn
```

Men-set spawn dunia ke posisi kamu berdiri saat ini.

```minecraft
/setworldspawn <x> <y> <z>
```

Men-set spawn dunia ke koordinat spesifik. Gunakan via console kalau tidak ada player di lokasi.

### `/spawnpoint` — Set Spawn per Pemain

```minecraft
/spawnpoint <player>
```

Set spawn point untuk player tertentu di posisi command sender.

```minecraft
/spawnpoint <player> <x> <y> <z>
```

Set spawn point player ke koordinat tertentu.

## Alur Spawn Default Vanilla

| Kondisi | Hasil Spawn |
|---------|-------------|
| Player baru join | `/setworldspawn` |
| Mati tanpa bed | World spawn |
| Tidur di bed | Bed (khusus player itu saja) |
| Bed dihancurkan/hilang | Balik ke world spawn |

**Semua ini default vanilla — tidak perlu plugin apapun.** Behavior ini hardcoded di Minecraft, tidak bisa dimatikan lewat `server.properties`.

## Plugin EssentialsX

Kalau pakai EssentialsX (`/setspawn` dan `/spawn`):

```minecraft
/setspawn     # Set spawn custom (biasanya lobby)
/spawn        # Teleport ke spawn custom
```

- `/setspawn` **tidak ada di vanilla** — hanya dari plugin
- `/setworldspawn` = spawn dunia default server
- `/setspawn` (plugin) = spawn custom (biasanya lobby/hub)
- `/spawnpoint` = spawn per pemain (overwrite bed)

## Spawn Radius

```minecraft
/gamerule spawnRadius 0
```

- `0` = spawn tepat di 1 titik (tidak menyebar)
- Default `10` = player spawn di area acak ±10 blok dari spawn point

`spawnRadius` di `gamerule` (bukan `server.properties`) untuk Java Edition modern. Di versi lama, `spawn-protection` di `server.properties` mengontrol ini.

## Pengaturan di server.properties

```properties
spawn-protection=0   # Radius proteksi spawn (blok). Hanya OP yang bisa edit area ini. 0 = tidak ada proteksi
```

`spawn-protection` **bukan lokasi spawn** — ini hanya radius blok yang dilindungi. Lokasi spawn tetap diatur dengan `/setworldspawn`.

## Multi-World Setup

Untuk server dengan banyak world (via Multiverse-Core atau plugin serupa):

```minecraft
/mv setspawn           # Set spawn di world yang sedang aktif
/mv spawn              # Teleport ke spawn world itu
/mvtp <player> <world> # Teleport player ke world lain
```

## Best Practices 2024-2025

- **Server survival murni**: Cukup `/setworldspawn` + `/gamerule spawnRadius 0` — biarkan bed respawn default vanilla bekerja
- **Server lobby + survival**: Pakai EssentialsX `/setspawn` untuk lobby, biarkan world survival pakai `/setworldspawn` + bed vanilla
- **Hardcore/semi-hardcore**: Hati-hati dengan plugin yang override bed spawn — cek config masing-masing
- **Spawn tepat 1 blok**: Pastikan `spawnRadius=0` dan posisi spawn di blok solid dengan 2 blok udara di atasnya
- **Spawn protection**: Untuk spawn publik, set `spawn-protection=16` agar area spawn tidak bisa dirusak player biasa

## Troubleshooting

### Player tidak respawn di bed setelah mati

Kemungkinan penyebab:
1. Bed dihancurkan/dirobek — otomatis balik ke world spawn
2. Plugin lobby/hardcore override bed spawn
3. Plugin respawn override (misal plugin minigame)
4. Mod Fabric/Forge tertentu yang mengubah respawn logic

Solusi: cek daftar plugin, nonaktifkan satu per satu untuk identifikasi.

### Spawn menyebar padahal sudah set spawnRadius 0

- Cek apakah `spawnRadius` di set per-world (Multiverse) bukan global
- Beberapa plugin (seperti EssentialsX) punya setting spawn radius sendiri di `config.yml`

### `/setworldspawn` tidak bekerja

- Pastikan kamu OP (level 4) atau punya permission `minecraft.command.setworldspawn`
- Via console harus selalu sertakan koordinat: `/setworldspawn 0 64 0`

## Related

- [[minecraft/server/server-properties]] — Konfigurasi lengkap server.properties
- [[minecraft/gameplay/daylight-cycle]] — Set siang terus (kombinasi dengan spawn untuk server 24/7)
- [[minecraft/tools/custom-seed]] — Seed kustom untuk world baru
- [[minecraft/tools/chunky]] — Pre-generate chunk (chunky bisa center ke spawn)
- [[minecraft/server/minecraft-docker]] — Setup server via Docker
