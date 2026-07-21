# Docker Compose

Docker Compose = tool untuk mendefinisikan dan menjalankan **multi-container** Docker apps. Semua konfigurasi di satu file `docker-compose.yml`.

## Kenapa Compose?

Tanpa Compose (ribet):
```bash
docker network create mynet
docker run -d --name db --network mynet -e POSTGRES_PASSWORD=xxx postgres
docker run -d --name app --network mynet -e DB_HOST=db -p 3000:3000 myapp
docker run -d --name redis --network mynet redis
# ... satu-satu, rentan salah
```

Dengan Compose (simpel):
```bash
docker compose up -d
```

## docker-compose.yml — Struktur Dasar

```yaml
# version sudah deprecated (Docker Compose v2)
services:        # definisi container
  web:           # nama service
    build: .     # build dari Dockerfile lokal
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
  
  db:
    image: postgres:17
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: s3cret

volumes:         # named volumes (persistent)
  pgdata:

networks:        # custom network
  appnet:
    driver: bridge
```

## Command Penting

```bash
docker compose up              # start semua service (foreground)
docker compose up -d           # background
docker compose up -d --build   # rebuild image sebelum start
docker compose down            # stop + hapus container & network
docker compose down -v         # stop + hapus juga volumes
docker compose ps              # status semua service di project
docker compose logs -f app     # follow log service tertentu
docker compose restart api     # restart satu service
docker compose exec app bash   # masuk shell ke service
docker compose build           # build (tanpa start)
docker compose pull            # pull semua image dari registry
```

## Fitur Compose

### Networks — Otomatis

Compose otomatis membuat **satu network** untuk semua service. Antar service bisa komunikasi dengan **nama service sebagai hostname**.

```yaml
services:
  api:
    environment:
      DB_HOST: postgres    # ← hostname = nama service!
  postgres:
    image: postgres:17
```

### depends_on

Menentukan urutan start. Tapi **tidak menjamin** service siap (e.g., postgres belum accept connection saat api start).

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy   # tunggu healthy check
  db:
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 5s
```

### Environment Variables

```yaml
services:
  app:
    environment:              # inline
      DEBUG: "true"
    env_file: .env            # dari file
```

File `.env`:
```
DEBUG=true
DATABASE_URL=postgres://...
```

### Volumes

Lihat [[docker/volumes]] untuk detail.

```yaml
services:
  app:
    volumes:
      - ./app:/app              # bind mount
      - uploads:/var/uploads    # named volume
      - /tmp/cache:/cache:ro    # bind mount read-only

volumes:
  uploads:                     # named volume definition
```

### Profiles — Conditional Start

```yaml
services:
  app:
    profiles: ["prod"]
  debug-tools:
    profiles: ["debug"]    # hanya start dengan profile debug
```

```bash
docker compose --profile debug up
```

### Extends & Overrides

```bash
# Base config: docker-compose.yml
# Override dev: docker-compose.override.yml  (auto-loaded)
# Override prod: docker-compose.prod.yml
```

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Compose vs Kubernetes

| | Docker Compose | Kubernetes |
|---|---|---|
| **Scope** | 1 host | Multi-host cluster |
| **Complexity** | Simpel | Kompleks |
| **Use case** | Dev, testing, single-server | Production, scaling |
| **File** | docker-compose.yml | manifests/deployment YAML |

## Tips

- Gunakan `docker compose` (v2 plugin, tanpa strip) bukan `docker-compose` (v1 standalone)
- Simpan `.env` di `.gitignore`
- `docker compose up -d --build` saat development
- `docker compose config` untuk debug parsing config

## Sumber

- [Docker Compose Overview](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/reference/compose-file/)
