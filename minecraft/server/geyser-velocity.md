# Geyser + Velocity — Crossplay Java-Bedrock

Setup GeyserMC di proxy Velocity untuk memungkinkan pemain Bedrock Edition join ke server Java.

## Arsitektur

```
Bedrock Client (port 19132) ─┐
                              ├── Geyser (Velocity plugin) ──┬── Paper Hardcore (25566)
Java Client (port 25565) ────┘                               └── Paper Lobby (25567)
```

Geyser dipasang di **Velocity (proxy)**, bukan di server Paper langsung. Dengan ini, semua subserver bisa diakses pemain Bedrock.

## Instalasi

### 1. Download

Dari https://geysermc.org/download/:
- **Geyser-Velocity.jar** — bridge Bedrock↔Java
- **Floodgate-Velocity.jar** — autentikasi Bedrock tanpa akun Java

Taruh di folder `plugins/` server Velocity.

### 2. Konfigurasi Geyser (`plugins/Geyser-Velocity/config.yml`)

```yaml
bedrock:
  address: 0.0.0.0
  port: 19132
  motd1: "Server Crossplay!"
  motd2: "Powered by GeyserMC"

remote:
  address: 127.0.0.1
  port: 25566                       # port server Paper utama
  auth-type: floodgate
```

### 3. Konfigurasi Floodgate (`plugins/Floodgate/config.yml`)

```yaml
send-floodgate-data: true
player-link:
  enabled: false
```

Floodgate memungkinkan pemain Bedrock login tanpa akun Java premium.

### 4. Buka Port

Pastikan port UDP **19132** terbuka di firewall:
```bash
sudo ufw allow 19132/udp
```

### 5. DNS (Opsional)

```
play.domain.com    → 25565 (Java)
bedrock.domain.com → 19132 (Bedrock)
```

## Testing

- **Java Edition**: `ip-server:25565`
- **Bedrock Edition**: `ip-server`, port `19132`

## Catatan Penting

- Geyser di Velocity = semua subserver bisa diakses Bedrock
- Geyser di Paper langsung = hanya server itu saja
- Floodgate wajib untuk menghindari keharusan akun Java premium
- Bedrock Edition punya batasan fitur dibanding Java (combat berbeda, redstone beda)

## Troubleshooting

### Bedrock tidak bisa connect
- Cek port 19132 UDP terbuka
- Cek `remote.address` di config.yml mengarah ke IP yang benar
- Cek firewall server

### Pemain Bedrock muncul sebagai player tidak dikenal
- Pastikan Floodgate terinstal dengan benar
- Cek `send-floodgate-data: true`

## Related

- [[server/velocity-proxy]] — Setup Velocity lengkap
- [[server/minecraft-docker]] — Docker setup
- [[server/server-types]] — Jenis server
- [[plugin/geyser-bedrock]] — Plugin Bedrock lainnya
