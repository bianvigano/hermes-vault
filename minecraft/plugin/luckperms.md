# LuckPerms — Permission Management

Plugin permission paling populer untuk Minecraft Java Edition. Support Bukkit/Spigot/Paper/Fabric/Forge/Velocity/BungeeCord.

**Website**: https://luckperms.net/
**Docs**: https://luckperms.net/wiki
**GitHub**: https://github.com/LuckPerms/LuckPerms

---

## Struktur Group Dasar

```
default
  ↳ admin
  ↳ moderator
  ↳ vip
```

## Command Penting

| Command | Fungsi |
|---------|--------|
| `/lp user <player> info` | Cek group & permission player |
| `/lp user <player> parent set <group>` | Ganti group utama |
| `/lp user <player> parent add <group>` | Tambah group tambahan |
| `/lp user <player> parent remove <group>` | Hapus group tertentu |
| `/lp group <group> parent add <parent>` | Set inheritance group |
| `/lp group <group> permission set <perm> true` | Tambah permission ke group |
| `/lp sync` | Sync antar server (bungee/network) |
| `/lp editor` | Buka web editor |

## Admin Balik ke Default

Pindah player dari admin ke default (hapus semua group lain):
```
/lp user NAMA_PLAYER parent set default
```

Hapus admin tapi tetap keep default:
```
/lp user NAMA_PLAYER parent remove admin
```

## Inheritance (Best Practice)

Biar admin otomatis inherit permission default:
```
/lp group admin parent add default
```

Struktur jadi:
```
default
  ↳ admin
```

Kalau admin dihapus, player otomatis balik ke default tanpa error.

## Pitfall

- `parent set` = hapus semua group lama, ganti dengan satu group
- `parent add` = tambah group tanpa menghapus yang lain
- `parent remove` = hapus group tertentu
- Selalu cek dengan `/lp user <player> info` sebelum dan sesudah ubah
- Web editor lebih aman untuk edit massal

## Related

- [[minecraft/server/minecraft-docker]] — Docker server setup
- [[minecraft/plugin/fawe-troubleshooting]] — FAWE error fix
- [[minecraft/tools/scoreboard]] — Scoreboard integration
