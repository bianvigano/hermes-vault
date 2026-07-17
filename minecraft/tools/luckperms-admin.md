# LuckPerms — Admin ke Default Group

Cara mengatur group di LuckPerms: pindah player dari group admin ke default, menghapus group, dan inheritance.

## Perintah Dasar

### Pindah Player ke Default Saja

```
/lp user NAMA_PLAYER parent set default
```

Efek: menghapus semua group lain, player hanya punya `default`.

### Hapus Group Admin Saja (Default Tetap Ada)

```
/lp user NAMA_PLAYER parent remove admin
```

Efek: group `admin` dihapus, group lain termasuk `default` tetap ada.

### Cek Group Player

```
/lp user NAMA_PLAYER info
```

## Inheritance: Default sebagai Parent Admin

Best practice: buat `default` jadi parent dari `admin`.

```
/lp group admin parent add default
```

Struktur:
```
default
  ↳ admin
```

Kalau `admin` dihapus, player otomatis balik ke `default` tanpa error.

## Setup Group Lengkap

### Buat Group
```
/lp group admin create
```

### Beri Permission ke Group
```
/lp group admin permission set minecraft.command.gamemode true
```

### Set Default Group
```
/lp group default setdisplayname &7Player
```

### Set Track/Promotion
```
/lp user NAMA_PLAYER promote track-staff
```

## Perintah Berguna Lainnya

| Perintah | Fungsi |
|----------|--------|
| `/lp user <player> parent info` | Lihat group player |
| `/lp user <player> parent add admin` | Tambah group |
| `/lp user <player> parent set admin` | Ganti ke satu group |
| `/lp group <group> listmembers` | Lihat anggota group |
| `/lp sync` | Sync database |

## Related

- [[tools/luckperms-build-error]] — Fix build error LuckPerms
- [[tools/luckperms-branch-fix]] — Fix remote name LuckPerms
- [[server/server-properties]] — Konfigurasi server
- [[plugin/essentialsx]] — Plugin EssentialsX permissions
