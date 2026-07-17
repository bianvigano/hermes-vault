# Spawn Commands — Set Spawn Dunia dan Player

Minecraft menyediakan command vanilla untuk mengatur spawn dunia dan spawn per player. Berlaku di semua platform: Bukkit, Spigot, Paper, Purpur, Fabric, Forge, NeoForge, Quilt.

## Set Spawn Dunia

```
/setworldspawn
```

Set spawn dunia di posisi player yang menjalankan command.

```
/setworldspawn <x> <y> <z>
```

Set spawn dunia ke koordinat tertentu.

## Set Spawn Player

```
/spawnpoint <player>
```

Set spawn untuk player tertentu di posisi command sender.

```
/spawnpoint <player> <x> <y> <z>
```

Set spawn player ke koordinat tertentu.

## Alur Default Vanilla

| Kondisi | Hasil Spawn |
|---------|-------------|
| Player baru join | `/setworldspawn` |
| Mati tanpa bed | World spawn |
| Tidur di bed | Bed (khusus player itu) |
| Bed rusak/hilang | Balik ke world spawn |

Ini semua default vanilla. Tidak perlu plugin.

## Spawn Radius

```
/gamerule spawnRadius 0
```

- `0` = spawn tepat di 1 titik
- Default `10` = player spawn di area acak ±10 blok dari spawn point

## Plugin EssentialsX

Kalau pakai EssentialsX:

```
/setspawn    # Set spawn custom (biasanya lobby)
/spawn       # Teleport ke spawn custom
```

`/setspawn` tidak ada di vanilla — hanya dari plugin.

## Catatan Penting

- Butuh OP / permission command
- `/setworldspawn` dijalankan di game; via console harus pakai koordinat
- Beberapa plugin lobby atau hardcore bisa override bed spawn
- `spawn-protection` di `server.properties` hanya proteksi blok, bukan lokasi spawn

## Related

- [[server/server-properties]] — Konfigurasi server.properties
- [[gameplay/daylight-cycle]] — Set siang terus
- [[server/minecraft-docker]] — Setup server via Docker
