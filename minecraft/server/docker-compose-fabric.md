# Docker Compose Fabric — Minecraft Server dengan Mods

Konfigurasi `docker-compose.yml` untuk server Fabric dengan `itzg/minecraft-server`, termasuk optimasi performa dan mod loading.

## Compose Dasar (Fabric)

```yaml
version: "3.8"
networks:
  mcnet:
    external: true
    name: minecraft_mcnet

services:
  event:
    image: itzg/minecraft-server:latest
    container_name: mc-inundated
    restart: unless-stopped

    ports:
      - "25861:25861"
      - "24454:24454/udp"

    environment:
      EULA: "TRUE"
      SERVER_NAME: "event"
      SERVER_PORT: 25861

      TYPE: "FABRIC"
      VERSION: "1.21"
      FABRIC_LOADER_VERSION: "latest"

      MEMORY: "8G"
      DIFFICULTY: "normal"
      MODE: "survival"
      MAX_PLAYERS: 10
      VIEW_DISTANCE: 10

      MAX_WORLD_SIZE: 50000
      ONLINE_MODE: "TRUE"
      MOTD: "Inundated Event Server"

    volumes:
      - ./event:/data

    stdin_open: true
    tty: true
    networks:
      - mcnet
```

## Environment Variables Format

| Variable | Tujuan | Catatan |
|----------|--------|---------|
| `MAX_WORLD_SIZE` | Batas radius world | UPPERCASE, underscore, otomatis jadi `max-world-size` |
| `SERVER_PORT` | Port server | Harus match dengan port mapping |
| `FABRIC_LOADER_VERSION` | Versi Fabric Loader | "latest" direkomendasikan |

## Version Validation

❌ `VERSION: "1.21.11"` — tidak valid, Minecraft tidak punya versi 1.21.11
✅ `VERSION: "1.21"` — valid
✅ `VERSION: "1.21.1"` — valid

## Instalasi Mods

### Struktur Folder
```
./event/
 ├─ mods/
 │   ├─ fabric-api.jar
 │   ├─ lithium.jar
 │   ├─ spark.jar
 │   ├─ simple-voice-chat.jar
 │   └─ chunky.jar
 ├─ config/
 └─ world/
```

Taruh semua `.jar` di `./event/mods/`. Docker autoload saat start.

### Mods Esensial untuk Fabric Server

| Mod | Fungsi | Modrinth |
|-----|--------|----------|
| Fabric API | Dependency wajib semua mod | https://modrinth.com/mod/fabric-api |
| Lithium | Optimasi performa server | https://modrinth.com/mod/lithium |
| Spark | Profiler TPS/CPU/RAM | https://modrinth.com/mod/spark |
| Simple Voice Chat | Voice proximity | https://modrinth.com/mod/simple-voice-chat |
| Chunky | Pre-generate chunk | https://modrinth.com/plugin/chunky |

Modrinth CDN direct links (contoh — cek versi terbaru):
```
https://cdn.modrinth.com/data/P7dR8mSH/versions/latest/fabric-api.jar
https://cdn.modrinth.com/data/gvQqBUqZ/versions/latest/lithium.jar
https://cdn.modrinth.com/data/l6YH9Als/versions/latest/spark.jar
https://cdn.modrinth.com/data/9eGKb6K1/versions/latest/simple-voice-chat.jar
https://cdn.modrinth.com/data/fALzjamp/versions/latest/chunky.jar
```

### Catatan Penting
- `spark` dan `chunky`: boleh di server saja
- `Simple Voice Chat`: WAJIB di client juga
- `Fabric API`: WAJIB untuk hampir semua mod
- Semua mod HARUS versi yang match dengan Minecraft + Fabric

## Network External

Pastikan network sudah ada:
```bash
docker network ls                      # Cek
docker network create minecraft_mcnet  # Buat kalau belum
```

## Checklist Sebelum Start

- [ ] Versi Minecraft valid & sesuai modpack
- [ ] Mods dimasukkan ke `./event/mods`
- [ ] Network `minecraft_mcnet` sudah ada
- [ ] Port terbuka di firewall
- [ ] Port UDP 24454 untuk voice chat

## Verifikasi

```bash
docker compose up -d
docker logs -f mc-inundated
```

Harus muncul: "Fabric Loader loaded", mods detected, no dependency missing.

## Post-Start: Chunky Pre-Generation

```
/chunky radius 25000
/chunky start
```

Karena `MAX_WORLD_SIZE=50000` (diameter 100K), radius Chunky = setengahnya (25K). Ini kritis untuk TPS stabil saat event.

## Related

- [[server/minecraft-docker]] — Panduan utama Docker
- [[server/docker-compose-8gb]] — Compose 8GB standar
- [[tools/chunky]] — Pre-generate chunk detail
- [[tools/spark-profiler]] — Profiling performa
- [[modding/fabric-mods]] — Koleksi mod Fabric
- [[modding/lithium-optimization]] — Optimasi Lithium
