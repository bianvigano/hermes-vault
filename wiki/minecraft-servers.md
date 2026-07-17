# Minecraft Servers

## Server List
| Server | Service Name | Path | Deskripsi |
|--------|-------------|------|-----------|
| arnarki | mc-arnarki | /root/minecraft/arnarki | Server utama |
| lobby | mc-lobby | /root/minecraft/lobby | Lobby server |
| proxy | mc-proxy | /root/minecraft/proxy | Proxy (Bungee/Velocity) |

Semua jalan via Docker.

## Backup
- Jadwal: 2x sehari (12:00 & 00:00 WIB)
- Via crontab + `jadwal-backup.sh` wrapper
- Flow: [1/4]~[4/4] dari file x asli

## Docker Console
- Command: `mc-send-to-console`
- Test: kirim 'list' ke console
- Kalau pipe error → silent skip

## Plugin yang Pernah Dibuat
- [[minecraft-plugins]] — Hunger Games, custom plugins

## Catatan Penting
- Folia API: `dev.folia:folia-api:26.1.2.build.8-stable`
- LuckPerms untuk permission
- Spark untuk profiling (`https://spark.lucko.me/...`)
- Entity drop item — bisa di-config waktu despawn
