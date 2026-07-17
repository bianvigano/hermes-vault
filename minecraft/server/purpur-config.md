# Purpur Config — Konfigurasi dan Kustomisasi Pesan Purpur Server

Panduan konfigurasi Purpur: file `purpur.yml`, kustomisasi pesan server, connection throttle, dan integrasi dengan config Paper/Spigot.

## Apa Itu Purpur?

Purpur adalah fork dari Paper (yang fork dari Spigot) — server Minecraft Java Edition dengan performa tinggi dan opsi konfigurasi paling lengkap. Purpur menambahkan **1000+ opsi konfigurasi** di file `purpur.yml`.

**File konfigurasi Purpur**:
| File | Fungsi |
|------|--------|
| `server.properties` | Konfigurasi dasar (sama dengan vanilla) |
| `bukkit.yml` | Konfigurasi Bukkit API |
| `spigot.yml` | Konfigurasi Spigot (throttle, messages) |
| `paper-global.yml` | Konfigurasi Paper global |
| `paper-world-defaults.yml` | Konfigurasi Paper per-world |
| `purpur.yml` | Konfigurasi Purpur (entity, gameplay, messages) |

## Mengganti Pesan "Connection Throttled"

Pesan ini muncul saat player reconnect terlalu cepat. Dikendalikan di `spigot.yml`:

### Edit di `spigot.yml`

```yaml
settings:
  connection-throttle: 4000    # Delay antar reconnect (ms)

messages:
  throttle: &cTunggu sebentar sebelum masuk lagi ya!
```

### Kode Warna Format `&`

| Kode | Warna/Efek |
|------|------------|
| `&0` | Hitam |
| `&1` | Biru tua |
| `&2` | Hijau tua |
| `&3` | Cyan tua |
| `&4` | Merah tua |
| `&5` | Ungu |
| `&6` | Emas |
| `&7` | Abu-abu |
| `&8` | Abu-abu tua |
| `&9` | Biru |
| `&a` | Hijau |
| `&b` | Cyan |
| `&c` | Merah |
| `&d` | Pink |
| `&e` | Kuning |
| `&f` | Putih |
| `&l` | **Bold** |
| `&n` | <u>Underline</u> |
| `&o` | *Italic* |
| `&k` | Random (obfuscated) |
| `&m` | ~~Strikethrough~~ |
| `&r` | Reset |

### Mematikan Connection Throttle

```yaml
settings:
  connection-throttle: -1
```

**WARNING**: Mematikan throttle = server rentan spam bot dan serangan reconnect. Hanya gunakan untuk server private/testing.

## Pesan Kustom di `purpur.yml`

Purpur menyediakan bagian `messages` untuk kustomisasi berbagai pesan server:

```yaml
messages:
  ping:
    motd: "&aSelamat Datang di Server Kami!"
    outdated-server: "&cServer versi lama, update dulu!"
    outdated-client: "&cClient kamu versi lama, update dulu!"
  afk:
    idle-timeout: "&eKamu di-kick karena idle terlalu lama"
  disable-chat: "&cChat dinonaktifkan!"
  enable-chat: "&aChat diaktifkankan kembali!"
  cannot-ride-mob: "&cKamu tidak bisa menaiki mob ini!"
```

## Pesan Kustom di `paper-global.yml`

Paper (induk Purpur) juga menyediakan pesan kustom:

```yaml
messages:
  no-permission: "&cKamu tidak punya izin untuk command ini!"
  kick:
    flying-player: "&cFlying is not enabled on this server"
    flying-vehicle: "&cFlying is not enabled on this server"
```

## Kustomisasi Entity & Gameplay di `purpur.yml`

Purpur punya kontrol granular atas perilaku entity dan gameplay:

```yaml
world-settings:
  default:
    blocks:
      crying-obsidian:
        valid-for-portal-frame: false
    mobs:
      villager:
        lobotomize:
          enabled: false           # Matikan AI villager yang jauh
        bypass-mob-griefing: false # Villager tidak bisa farming
      zombie:
        jockey:
          only-babies: true
        aggressive-towards-villager: true
```

Lebih dari 1000 opsi tersedia — lihat dokumentasi resmi untuk daftar lengkap.

## Pesan "Failed to connect to the server"

Pesan ini **tidak bisa diganti dari config server** karena merupakan pesan client-side Minecraft. Muncul saat:
- Server mati / tidak bisa dijangkau
- Koneksi ditolak
- Timeout

Untuk custom full message, diperlukan:
- Plugin **AdvancedBan** atau **CustomKick**
- Atau modifikasi JAR server (tidak disarankan)

## Best Practices 2024-2025

- **Format warna**: Gunakan `&` format (bukan MiniMessage) di `spigot.yml` dan `purpur.yml`
- **MiniMessage**: Paper 1.19+ mendukung MiniMessage untuk beberapa pesan — cek dokumentasi per versi, formatnya berbeda (`<red>Teks</red>`)
- **Backup**: Selalu backup config sebelum edit — salah format YAML bisa bikin server gagal start
- **Test lokal**: Uji perubahan di server lokal sebelum deploy ke production
- **Reload vs Restart**: Beberapa setting `purpur.yml` hanya berlaku setelah restart penuh, bukan `/reload`
- **Format YAML**: Indentasi harus pakai spasi (bukan tab) — 2 spasi per level

## Troubleshooting

### Server gagal start setelah edit purpur.yml

- Cek format YAML — pakai [YAML Lint](https://www.yamllint.com/)
- Pastikan indentasi pakai spasi, bukan tab
- Pastikan tidak ada karakter spesial yang conflict
- Kembalikan ke backup, edit satu per satu untuk identifikasi masalah

### Pesan tidak berubah setelah edit

- Restart server penuh (bukan `/reload`)
- Pastikan kamu mengedit file yang benar (beberapa host memakai symlink)
- Cek apakah plugin lain meng-override pesan yang sama

## Related

- [[minecraft/troubleshooting/connection-throttled]] — Fokus troubleshooting connection throttle
- [[minecraft/server/server-properties]] — Konfigurasi server.properties
- [[minecraft/server/gamerules]] — Gamerule / aturan dunia
- [[minecraft/server/minecraft-docker]] — Setup Purpur via Docker
- [[minecraft/tools/chunky]] — Pre-generate chunk (performa)
