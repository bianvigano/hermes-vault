# Minecraft Docker Server — itzg/minecraft-server

Image Docker paling populer untuk hosting Minecraft server. Otomatis download versi terbaru, support Paper/Fabric/Forge/NeoForge/Vanilla.

**Image**: `itzg/minecraft-server:latest`
**Docker Hub**: https://hub.docker.com/r/itzg/minecraft-server
**Docs**: https://docker-minecraft-server.readthedocs.io/
**GitHub**: https://github.com/itzg/docker-minecraft-server

---

## Docker Compose Dasar (Vanilla)

```yaml
version: "3.8"
services:
  minecraft:
    image: itzg/minecraft-server:latest
    container_name: minecraft-vanilla
    restart: unless-stopped
    stdin_open: true
    tty: true
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      TYPE: VANILLA
      VERSION: "LATEST"
      MEMORY: "4G"
      MOTD: "Vanilla Server"
      MAX_PLAYERS: 20
      VIEW_DISTANCE: 10
    volumes:
      - ./data:/data
```

## Docker Compose Paper (Rekomendasi)

```yaml
environment:
  EULA: "TRUE"
  TYPE: PAPER
  VERSION: "LATEST"
  MEMORY: "8G"
  ONLINE_MODE: "true"
  VIEW_DISTANCE: 10
  SIMULATION_DISTANCE: 8
  MAX_PLAYERS: 20
```

## Docker Compose Fabric

```yaml
environment:
  EULA: "TRUE"
  TYPE: FABRIC
  VERSION: "1.21.4"
  FABRIC_LOADER_VERSION: "latest"
  MEMORY: "8G"
```

Untuk mod Inundated dan modpack Fabric lainnya, tambahkan folder `mods/`:

```yaml
volumes:
  - ./data:/data
  - ./mods:/data/mods
```

## Docker Compose dengan Network Kustom

```yaml
networks:
  mcnet:
    external: true
    name: minecraft_mcnet
services:
  mc-event:
    image: itzg/minecraft-server:latest
    container_name: mc-event
    restart: unless-stopped
    stdin_open: true
    tty: true
    ports:
      - "25861:25861"
    environment:
      EULA: "TRUE"
      SERVER_NAME: "event"
      SERVER_PORT: 25861
      TYPE: FABRIC
      VERSION: "1.21.4"
      FABRIC_LOADER_VERSION: "latest"
      MEMORY: "8G"
      DIFFICULTY: "normal"
      MODE: "survival"
      MAX_PLAYERS: 10
      VIEW_DISTANCE: 10
    volumes:
      - ./event:/data
    networks: [mcnet]
```

## Dimensi: World / Nether / End

Minecraft otomatis buat 3 folder:
```
data/
├── world/          # Overworld
├── world_nether/   # Nether (otomatis saat pertama masuk)
├── world_the_end/  # End (otomatis saat pertama masuk)
```

⚠️ **Nether dan End tidak akan muncul sampai pemain masuk ke dimensi tersebut.** Ini normal.

Force generate dengan command:
```bash
docker exec -it minecraft-server rcon-cli
execute in minecraft:the_nether run tp @p 0 80 0
```

Pastikan di `server.properties`:
```properties
allow-nether=true
```

## Solusi Multi-User Console

❌ **`docker attach` tidak bisa untuk multi-user** — semua lihat input yang sama.

✅ **RCON (recommended)**:
```properties
enable-rcon=true
rcon.port=25575
rcon.password=PASSWORDKUAT
```
```bash
mcrcon -H 127.0.0.1 -P 25575 -p PASSWORDKUAT
```

✅ **`docker exec` (alternatif)**:
```bash
docker exec -it mc-event bash
```

| Cara | Multi-user | Rekomendasi |
|------|-----------|-------------|
| docker attach | ❌ | ❌ |
| docker exec | ⚠️ | ❌ |
| RCON | ✅ | ⭐⭐⭐ |
| Panel (Pterodactyl) | ✅ | ⭐⭐⭐⭐ |

## Minecraft Bot (Mineflayer)

Bot pakai Docker — bukan server, tapi pemain otomatis:
```js
const mineflayer = require('mineflayer')
const bot = mineflayer.createBot({
  host: 'localhost',
  port: 25565,
  username: 'BotDocker',
  version: false
})
```

Dockerfile:
```Dockerfile
FROM node:18
WORKDIR /bot
COPY . .
RUN npm install mineflayer
CMD ["node", "bot.js"]
```

## Velocity + Paper (Multi-Server Proxy)

Vanilla ❌ Velocity (tidak support modern forwarding)
Paper ✅ Velocity (pakai `paper-global.yml`)

```yaml
# velocity.toml
player-info-forwarding-mode = "modern"
```

```yaml
# paper-global.yml
proxies:
  velocity:
    enabled: true
    online-mode: true
    secret: "PASTE_SECRET_DARI_VELOCITY"
```

```properties
# server.properties (backend)
online-mode=false
```

## Pitfall

- `version` di docker-compose sekarang deprecated (tidak perlu)
- Cardboard (hybrid Bukkit+Fabric) cuma ada versi alpha — set `MODRINTH_VERSION_TYPE: alpha`
- Crack server: `ONLINE_MODE: "FALSE"` — tidak aman
- Level type `flat` bisa bikin End ga generate
- `FABRIC_LOADER_VERSION: "latest"` aman, tapi `VERSION` harus spesifik (e.g. "1.21.4")

## Related

- [[minecraft/tools/chunky]] — Pre-generate chunk
- [[minecraft/tools/geyser-velocity]] — Bedrock-Java crossplay
- [[minecraft/plugin/fawe-troubleshooting]] — FAWE error fix
- [[minecraft/server/inundated-setup]] — Server mod Inundated
- [[minecraft/plugin/denizen]] — Denizen scripting
- [[minecraft/plugin/luckperms]] — Permission management
