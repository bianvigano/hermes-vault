# Docker Compose 8GB — Minecraft Server dengan Nether & End

Konfigurasi `docker-compose.yml` untuk server Minecraft `itzg/minecraft-server` dengan 8GB RAM, satu world lengkap dengan Nether dan The End.

## Compose Dasar (8GB RAM)

```yaml
version: "3.8"
services:
  minecraft:
    image: itzg/minecraft-server:latest
    container_name: minecraft-server
    restart: unless-stopped
    ports:
      - "25861:25565"
      - "25511:25511/udp"     # Voice chat (Simple Voice Chat)
    environment:
      EULA: "TRUE"
      TYPE: PAPER
      VERSION: "LATEST"

      # World
      LEVEL_NAME: "world"
      ENABLE_NETHER: "true"
      ENABLE_END: "true"

      # Resource
      MEMORY: "8G"

      # Performance
      VIEW_DISTANCE: 10
      SIMULATION_DISTANCE: 8
      MAX_PLAYERS: 20
      ONLINE_MODE: "true"

    volumes:
      - ./data:/data
```

## Struktur Data

Setelah server berjalan DAN player masuk Nether + End:

```
data/
├── world/           # Overworld
├── world_nether/    # Muncul setelah masuk Nether
├── world_the_end/   # Muncul setelah masuk End
```

Folder `world_nether` dan `world_the_end` **tidak dibuat saat startup** — hanya saat pertama kali diakses. Ini normal, bukan error.

## Cara Memunculkan Nether + End

### Via Game
- Nether: buat portal → masuk
- The End: cari Stronghold → aktifkan End Portal

### Via Console (RCON)
```bash
docker exec -it minecraft-server rcon-cli
```
```
execute in minecraft:the_nether run tp @p 0 80 0
execute in minecraft:the_end run tp @p 0 80 0
```

### Via Command In-Game (OP)
```
/execute in minecraft:the_nether run tp @p 0 80 0
/execute in minecraft:the_end run tp @p 0 80 0
```

## Tidak Bisa Gabung Dimensi

Minecraft secara internal selalu pisahkan 3 dimensi — tidak bisa disatukan ke satu folder `world/`. Ini desain fundamental Minecraft, bukan keterbatasan Docker/Paper.

| Dimensi | Folder |
|---------|--------|
| Overworld | `world/` |
| Nether | `world_nether/` |
| The End | `world_the_end/` |

Menghapus folder = dibuat ulang otomatis.

## Voice Chat (Simple Voice Chat)

Tambahan untuk Fabric server dengan Simple Voice Chat:

```yaml
ports:
  - "25861:25565"
  - "24454:24454/udp"
environment:
  VOICECHAT_PORT: 24454
```

Port default Simple Voice Chat = 24454/udp. Client juga HARUS install mod ini.

## MAX_WORLD_SIZE di Docker

Gunakan environment variable UPPERCASE:

```yaml
MAX_WORLD_SIZE: 50000
```

Otomatis dikonversi ke `max-world-size=50000` di `server.properties`. Nilai dalam blok (radius).

## Pre-Generate dengan Chunky

Setelah server nyala untuk menghindari lag eksplorasi:

```
/chunky radius 25000
/chunky start
```

Radius = setengah dari MAX_WORLD_SIZE.

## Vanilla vs Paper untuk Velocity

| Setup | Bisa? |
|-------|-------|
| Vanilla → Velocity | ❌ Tidak |
| Paper → Velocity | ✅ Ya |

Vanilla tidak mendukung modern proxy handshake Velocity. Paper wajib untuk setup proxy.

Paper 100% kompatibel dengan world vanilla, tidak merusak data.

## Verifikasi

```bash
docker compose up -d
docker logs -f minecraft-server
```

Harus muncul: "Done" / "RCON running" / tanpa error.

## Related

- [[server/minecraft-docker]] — Panduan utama Docker Minecraft
- [[server/docker-compose-fabric]] — Compose untuk Fabric + mods
- [[server/rcron-multi-user]] — Multi-user console
- [[server/velocity-proxy]] — Setup Velocity proxy
- [[tools/chunky]] — Pre-generate chunk
- [[modding/fabric-mods]] — Mod Fabric untuk server
