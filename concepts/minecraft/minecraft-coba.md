---
title: "coba kamu cek github ini https://github.com/itzg/docker-minecraft-server, cari w"
date: 2026-07-16
category: minecraft
tags: []
source: "sessions/hermes/coba-kamu-cek-github-ini.md"
---

# coba kamu cek github ini https://github.com/itzg/docker-minecraft-server, cari w

## Commands
- `cd creative && ./start.sh start`
- `cd mc-server`
- `cd modded   && ./start.sh config set server-port 25567 && cd ..`
- `cd modded   && ./start.sh config set server-port 25567 && cd .. Iya, tetap bisa. `multi.sh` cuma wrapper — fitur multi-s`
- `cd paper-server`
- `cd survival && ./start.sh config set server-port 25565 && cd ..`
- `cd survival && ./start.sh start`
- `cd ~/paper-server`

## Code
```bash
# List semua versi
curl -H "User-Agent: your-app/1.0 (contact@url)" \
  https://fill.papermc.io/v3/projects/paper

# List build untuk versi tertentu
curl -H "User-Agent: your-app/1.0 (contact@url)" \
  https://fill.papermc.io/v3/projects/paper/versions/{MC_VERSION}/builds

# Download dari response JSON: .downloads."server:default".url
```

```bash
# List versi
curl https://api.purpurmc.org/v2/purpur

# List build
curl https://api.purpurmc.org/v2/purpur/{VERSION}

# Download latest build
curl -o purpur.jar https://api.purpurmc.org/v2/purpur/{VERSION}/latest/download
```

```bash
mc-server/
├── setup.sh   # Multi-type setup (paper/purpur/fabric)
└── README.md
```

## Sumber
- [sessions/hermes/coba-kamu-cek-github-ini.md](sessions/hermes/coba-kamu-cek-github-ini.md)

## Related
