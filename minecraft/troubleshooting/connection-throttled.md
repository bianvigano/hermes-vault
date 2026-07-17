# Ganti Pesan Purpur/Spigot — Custom Server Messages

Cara mengganti pesan bawaan server Purpur/Paper/Spigot, termasuk pesan "Connection throttled" dan konfigurasi throttle.

## Pesan "Connection throttled! Please wait before reconnecting."

Muncul saat player reconnect terlalu cepat. Dikenakan oleh mekanisme connection throttle Spigot/Paper/Purpur.

### Cara Mengganti di `spigot.yml`

```yaml
messages:
  throttle: &cTunggu sebentar sebelum masuk lagi ya!
```

Kode warna Minecraft (format `&`):
- `&c` — merah
- `&a` — hijau
- `&e` — kuning
- `&l` — bold
- `&n` — underline

### Cara Mematikan Throttle

```yaml
settings:
  connection-throttle: -1
```

Nilai `-1` = throttle dimatikan. WARNING: server lebih rentan spam bot.

Nilai default `4000` = 4 detik delay antar reconnect.

## Pesan "Failed to connect to the server"

Ini pesan client-side, **tidak bisa diganti dari config server**. Muncul saat:
- Server mati/tidak bisa dijangkau
- Koneksi ditolak
- Timeout

Untuk custom full message, perlu:
- Plugin seperti **AdvancedBan**, **CustomKick**
- Atau modifikasi jar server (tidak disarankan)

## Konfigurasi Purpur Messages

Purpur (`purpur.yml`) juga menyediakan custom messages:

```yaml
messages:
  ping:
    motd: "&aSelamat Datang di Server Kami!"
    outdated-server: "&cServer versi lama, update dulu!"
    outdated-client: "&cClient kamu versi lama!"
```

## Konfigurasi Paper Messages

Paper global config (`paper-global.yml` atau `config/paper-global.yml`):

```yaml
messages:
  no-permission: "&cKamu tidak punya izin untuk command ini!"
  kick:
    flying-player: "&cFlying is not enabled on this server"
    flying-vehicle: "&cFlying is not enabled on this server"
```

## Best Practices 2024-2025

- Gunakan `&` format (bukan MiniMessage) di `spigot.yml` dan `purpur.yml`
- Paper 1.19+ mendukung MiniMessage untuk beberapa pesan — cek dokumentasi per versi
- Simpan backup config sebelum edit
- Test di local dulu sebelum deploy ke production

## Related

- [[server/server-properties]] — Konfigurasi dasar server
- [[server/purpur-config]] — Konfigurasi lengkap Purpur
- [[plugin/minimessage-format]] — Format MiniMessage untuk Paper modern
- [[troubleshooting/minecraft-crash-189]] — Troubleshooting crash
