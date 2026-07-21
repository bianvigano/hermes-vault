# Docker Volumes — Persistent Data

Data di dalam container **ephemeral**: hilang saat container dihapus. Docker menyediakan 3 mekanisme untuk persistent data.

## Storage Types

| Type | Lokasi | Dikelola Docker? | Use Case |
|---|---|---|---|
| **Volume** | `/var/lib/docker/volumes/` | Ya | Production data, DB, uploads |
| **Bind Mount** | Path mana pun di host | Tidak | Development, config file |
| **tmpfs** | RAM | N/A | Temporary/sensitive data |

```
┌──────────────────────────────────┐
│         HOST FILESYSTEM          │
│  ┌────────────┐  ┌──────────────┐│
│  │   Volume   │  │  Bind Mount  ││
│  │ (managed)  │  │ (any path)   ││
│  └──────┬─────┘  └──────┬───────┘│
└─────────┼───────────────┼────────┘
          │               │
     ┌────▼───────────────▼────┐
     │       CONTAINER         │
     │  /data     /app/config  │
     └─────────────────────────┘
         
  ┌──────────────┐
  │     RAM      │
  │  tmpfs mount │
  └──────┬───────┘
         │
    ┌────▼───────────┐
    │   CONTAINER    │
    │     /tmp       │
    └────────────────┘
```

## Volume (Recommended)

Volume disimpan di `/var/lib/docker/volumes/`, dikelola penuh oleh Docker. Bisa di-share antar container.

```bash
# Buat volume
docker volume create mydata

# Gunakan volume
docker run -v mydata:/app/data myapp

# Atau dengan --mount (lebih eksplisit, recommended)
docker run --mount source=mydata,target=/app/data myapp

docker volume ls          # list volume
docker volume inspect mydata  # lihat detail
docker volume rm mydata   # hapus volume
docker volume prune       # hapus semua unused
```

### Dalam docker-compose.yml

```yaml
services:
  db:
    image: postgres:17
    volumes:
      - pgdata:/var/lib/postgresql/data

  app:
    volumes:
      - uploads:/app/uploads

volumes:
  pgdata:     # volume akan dibuat otomatis
  uploads:
```

## Bind Mount

Mount path spesifik dari host ke container. **Tidak dikelola Docker** — isinya sesuai dengan filesystem host.

```bash
# Development — sync code changes real-time
docker run -v $(pwd):/app myapp

# Dengan --mount
docker run --mount type=bind,source=$(pwd),target=/app myapp

# Read-only
docker run -v $(pwd)/config:/etc/app:ro myapp
```

```yaml
services:
  app:
    volumes:
      - ./src:/app          # bind mount development
      - ./nginx.conf:/etc/nginx/nginx.conf:ro  # config read-only
```

## tmpfs Mount

Data disimpan di **RAM** — hilang saat container stop. Cocok untuk data sementara/sensitif.

```bash
docker run --tmpfs /tmp:rw,noexec,nosuid myapp
docker run --mount type=tmpfs,destination=/tmp,tmpfs-size=64m myapp
```

## Volume vs Bind Mount — Kapan Pakai?

| Volume | Bind Mount |
|---|---|
| Database / persistent app data | Development code sync |
| Data yang perlu di-backup | Config files |
| Share data antar container | File host yang perlu diakses container |
| Di-manage Docker | Path spesifik user |

## Backup & Restore Volume

```bash
# Backup
docker run --rm -v mydata:/data -v $(pwd):/backup alpine \
  tar czf /backup/mydata-backup.tar.gz -C /data .

# Restore
docker run --rm -v mydata:/data -v $(pwd):/backup alpine \
  tar xzf /backup/mydata-backup.tar.gz -C /data
```

## Tips

- JANGAN simpan data di writable container layer — gunakan volume/bind mount
- Named volume lebih mudah dikelola daripada anonymous volume
- Named volume aman dari `docker system prune`
- Bind mount `.` untuk hot-reload development

## Sumber

- [Docker Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Bind Mounts](https://docs.docker.com/engine/storage/bind-mounts/)
