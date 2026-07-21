# Docker Overview

Docker adalah platform open-source untuk **mengembangkan, mengirim, dan menjalankan aplikasi** di dalam container — ruang isolasi ringan yang mengemas aplikasi beserta semua dependensinya.

## Kenapa Docker?

| Masalah Tanpa Docker | Solusi Dengan Docker |
|---|---|
| "Di laptopku jalan, di server error" | Container jalan identik di mana saja |
| Install dependensi manual tiap server | Semua dependensi dikemas dalam image |
| Konflik versi antar aplikasi | Tiap container terisolasi |
| Setup environment lama | `docker run` — langsung jalan |
| Boros resource (VM) | Container sharing kernel, ringan |

## Konsep Inti

- **Container** — instance berjalan dari image, seperti "proses terisolasi"
- **Image** — template/blueprint read-only untuk membuat container
- **Dockerfile** — file teks berisi instruksi membangun image
- **Docker Hub** — registry publik untuk menyimpan & berbagi image
- **Volume** — penyimpanan persisten di luar lifecycle container
- **Network** — komunikasi antar container dan ke luar
- **Docker Compose** — menjalankan multi-container app dengan satu file YAML

## Analogi

> Docker itu seperti **container pengiriman barang**:
> - Barang dikemas rapi di dalam kontainer standar
> - Kontainer bisa dipindah antar kapal, truk, kereta — isinya tetap aman
> - Tidak peduli lingkungan luar — kontainer melindungi isinya

## Cakupan Wiki Ini

### Core Concepts
- [[docker/architecture]] — Arsitektur: Client, Daemon, Registry
- [[docker/installation]] — Install Docker di Linux/macOS/Windows
- [[docker/images]] — Image, Dockerfile, build & push
- [[docker/containers]] — Container lifecycle, run, stop, exec, logs
- [[docker/vs-vm]] — Docker vs Virtual Machine

### Multi-Container & Orchestration
- [[docker/compose]] — Multi-container app dengan docker-compose.yml
- [[docker/networking]] — Bridge, Host, Overlay network
- [[docker/volumes]] — Persistent data: Volume, Bind Mount, tmpfs

### Production & DevOps
- [[docker/registry]] — Docker Hub, push/pull, private registry
- [[docker/healthcheck]] — HEALTHCHECK & graceful shutdown
- [[docker/logging]] — Log drivers, centralized logging, monitoring (ELK, Prometheus)
- [[docker/cicd]] — CI/CD pipeline: GitHub Actions, auto-deploy
- [[docker/buildkit]] — BuildKit, buildx, cache mounts, multi-platform

### Reference
- [[docker/commands]] — Cheatsheet 60+ command
- [[docker/best-practices]] — Best practices & security hardening
- [[docker/troubleshooting]] — Masalah umum & debugging

## Alur Kerja Dasar

```
  Dockerfile  ──build──▶  Image  ──run──▶  Container
                              │
                              └──push──▶  Registry (Docker Hub)
```

```bash
# 1. Tulis aplikasi
# 2. Bikin Dockerfile
# 3. Build menjadi image
docker build -t namaku/app:1.0 .

# 4. Jalanin container
docker run -d -p 8080:80 namaku/app:1.0

# 5. Push ke registry (opsional)
docker push namaku/app:1.0
```

## Sumber

- [Docker Docs — Overview](https://docs.docker.com/get-started/docker-overview/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
