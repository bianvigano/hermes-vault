# Docker Containers

Container = **instance berjalan** dari Docker image. Container menambah **thin writable layer** di atas image layers. Semua perubahan file hilang saat container dihapus — kecuali pakai **volumes**.

## Container Lifecycle

```
  create → start → running → stop → (start) → kill → remove
     │                          │
     └──────────────────────────┘
              di-restart
```

## Command Dasar

### Run Container

```bash
# Basic run
docker run nginx

# Background (-d), port mapping (-p), named (-name)
docker run -d --name webserver -p 8080:80 nginx

# Interactive terminal
docker run -it ubuntu bash

# Remove container when stop (--rm)
docker run --rm -it alpine sh

# Environment variables
docker run -e DATABASE_URL=postgres://... -e DEBUG=true myapp

# Restart policy
docker run --restart always nginx          # selalu restart
docker run --restart unless-stopped nginx  # kecuali manual stop
docker run --restart on-failure:3 nginx    # restart max 3x
```

### Melihat Container

```bash
docker ps                 # container running
docker ps -a              # semua container (termasuk stopped)
docker ps -a -q           # hanya ID
docker stats              # live CPU/memory usage
```

### Start / Stop / Restart

```bash
docker stop webserver     # graceful shutdown (SIGTERM → SIGKILL)
docker kill webserver     # paksa kill (SIGKILL langsung)
docker start webserver    # start container stopped
docker restart webserver  # stop lalu start
docker pause webserver    # freeze (SIGSTOP)
docker unpause webserver  # thaw (SIGCONT)
```

### Exec — Masuk Container

```bash
# Interactive shell
docker exec -it webserver bash

# Run single command
docker exec webserver ls /app
docker exec webserver cat /etc/os-release

# Run as different user
docker exec -u root webserver whoami
```

### Logs & Inspect

```bash
docker logs webserver                 # semua log
docker logs -f webserver              # follow (tail -f)
docker logs --tail 50 webserver       # 50 baris terakhir
docker logs --since 10m webserver     # 10 menit terakhir

docker inspect webserver              # semua detail JSON
docker inspect -f '{{.NetworkSettings.IPAddress}}' webserver  # ambil field spesifik

docker top webserver                  # proses dalam container
docker port webserver                 # port mapping
```

### Remove Container

```bash
docker rm webserver                   # hapus container stopped
docker rm -f webserver                # force remove (running)
docker container prune                # hapus semua container stopped
docker rm $(docker ps -a -q)          # hapus SEMUA container
```

## Container vs Image vs Dockerfile

| | Apa | Bisa diubah? | Persistent? |
|---|---|---|---|
| **Dockerfile** | Teks instruksi | Ya | N/A (file teks) |
| **Image** | Template hasil build | Tidak (read-only) | Ya, sampai dihapus |
| **Container** | Instance berjalan | Ya (thin writable layer) | Perubahan hilang saat container dihapus |

```
Dockerfile  ── docker build ──▶  Image  ── docker run ──▶  Container
   (teks)                         (binary)                   (process)
```

## Port Mapping

```bash
# Format: -p HOST_PORT:CONTAINER_PORT
docker run -p 8080:80 nginx       # akses via localhost:8080
docker run -p 3000:3000 myapp     # 1:1 mapping
docker run -p 127.0.0.1:5432:5432 postgres  # hanya localhost
```

## Resource Limits

```bash
docker run --memory="256m" --cpus="1.5" myapp
docker run --memory="512m" --memory-swap="1g" myapp  # 512MB RAM, 1GB termasuk swap
docker update --memory="512m" webserver                # update container running
```

## Container Lifetime

Container mati otomatis saat **main process (PID 1) exit**. CMD/ENTRYPOINT yang exit → container stop.

```bash
docker run ubuntu echo "hello"  # container jalan → echo → exit → mati
docker run -d nginx              # nginx daemon tetap jalan → container tetap hidup
```

## Tips

- Gunakan `docker exec` untuk debugging, bukan `docker attach`
- `--rm` untuk container sementara (testing)
- `--restart` untuk production service
- Jangan simpan data penting di writable layer — pakai [[docker/volumes]]

## Sumber

- [Docker CLI — Container](https://docs.docker.com/reference/cli/docker/container/)
- [Docker run reference](https://docs.docker.com/reference/cli/docker/container/run/)
