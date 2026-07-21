# Docker Architecture

Docker menggunakan arsitektur **client-server**. Client berbicara ke Daemon melalui REST API (UNIX socket atau TCP). Daemon yang melakukan pekerjaan berat: build, run, distribusi container.

```
┌──────────┐     REST API      ┌─────────────┐
│  Client  │ ◄───────────────► │   Daemon     │
│ (docker) │    (UNIX/TCP)     │  (dockerd)   │
└──────────┘                   └──────┬───────┘
                                      │
                          ┌───────────┼───────────┐
                          ▼           ▼           ▼
                      ┌──────┐  ┌──────────┐  ┌──────────┐
                      │Images│  │Containers│  │Networking│
                      └──────┘  └──────────┘  └──────────┘
```

## Komponen Utama

### 1. Docker Client (`docker`)

Primary interface untuk berinteraksi dengan Docker. Perintah CLI:

```bash
docker run nginx        # client kirim perintah ke daemon
docker build -t app .   # client kirim build context
docker pull ubuntu      # client minta image dari registry
```

Client bisa terhubung ke **daemon lokal** (default) atau **daemon remote** via `DOCKER_HOST`.

### 2. Docker Daemon (`dockerd`)

Background process yang:
- Mendengarkan API request dari client
- Mengelola objek Docker: images, containers, networks, volumes
- Bisa berkomunikasi dengan daemon lain (Docker Swarm)

```bash
# Cek status daemon
sudo systemctl status docker

# Konfigurasi daemon di /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m" }
}
```

### 3. Docker Registry

Tempat menyimpan & mendistribusikan Docker images.

- **Docker Hub** — registry publik default (hub.docker.com)
- **Private Registry** — untuk internal perusahaan
- **Cloud Registry** — AWS ECR, GCR, Azure ACR

```bash
docker pull nginx:latest       # download dari Docker Hub
docker tag myapp myrepo/myapp  # tag untuk registry pribadi
docker push myrepo/myapp       # upload ke registry
```

### 4. Docker Objects

#### Images
Template read-only untuk membuat container. Terdiri dari **layer** bertumpuk. Setiap instruksi di Dockerfile = 1 layer.

```
Layer 6: CMD ["python", "app.py"]
Layer 5: EXPOSE 5000
Layer 4: COPY app.py .
Layer 3: RUN pip install -r requirements.txt
Layer 2: WORKDIR /app
Layer 1: FROM python:3.12-slim
```

#### Containers
Instance berjalan dari image. Container menambah **thin writable layer** di atas image layers. Semua perubahan (tulis file, install package) masuk ke layer ini — hilang saat container dihapus.

#### Networks
Driver untuk komunikasi antar container. Lihat [[docker/networking]].

#### Volumes
Penyimpanan persisten yang survive container restart/delete. Lihat [[docker/volumes]].

## Flow: `docker run` (Behind the Scenes)

1. Client jalankan `docker run ubuntu`
2. Client kirim request ke daemon via REST API
3. Daemon cek: image `ubuntu` ada di lokal?
   - Ya → langsung pakai
   - Tidak → pull dari registry
4. Daemon buat container dari image
5. Daemon alokasikan filesystem, network, dll
6. Container jalan, output dikirim balik ke client

## Docker vs Docker Compose

| | Docker CLI | Docker Compose |
|---|---|---|
| **Scope** | 1 container | Multi-container |
| **Config** | Command-line args | `docker-compose.yml` |
| **Use case** | Simple app, testing | Microservices, full stack |
| **Command** | `docker run ...` | `docker compose up` |
| **Networking** | Manual | Auto-network antar service |

## Sumber

- [Docker Docs — Architecture](https://docs.docker.com/get-started/docker-overview/#docker-architecture)
- [Docker Daemon Guide](https://phoenixnap.com/kb/docker-daemon)
