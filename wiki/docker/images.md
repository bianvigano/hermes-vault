# Docker Images & Dockerfile

## Apa Itu Image?

Docker image = **template read-only** yang berisi aplikasi + semua dependensinya. Image terdiri dari **layer** yang bertumpuk. Layer di-cache — rebuild hanya memproses layer yang berubah.

```
Layer dibaca:  dari bawah ke atas (base → app)
Layer ditulis: dari atas ke bawah (ubah layer atas, bawah tetap)
```

## Dockerfile

Dockerfile = file teks berisi instruksi untuk membangun image. **WAJIB dimulai dengan `FROM`.**

### Instruksi Penting

| Instruksi | Fungsi | Contoh |
|---|---|---|
| `FROM` | Base image | `FROM python:3.12-slim` |
| `WORKDIR` | Set working dir | `WORKDIR /app` |
| `COPY` | Copy file dari host | `COPY . .` |
| `RUN` | Eksekusi perintah saat build | `RUN pip install -r requirements.txt` |
| `CMD` | Default command saat container start | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Executable utama (tidak bisa override) | `ENTRYPOINT ["gunicorn"]` |
| `EXPOSE` | Port yang dipakai aplikasi | `EXPOSE 5000` |
| `ENV` | Environment variable | `ENV FLASK_ENV=production` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `VOLUME` | Buat mount point | `VOLUME /data` |
| `USER` | User untuk menjalankan container | `USER appuser` |

### Contoh Dockerfile — Python App

```dockerfile
# ---- Build Stage ----
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Run Stage ----
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
USER 1000
CMD ["python", "app.py"]
```

### Contoh Dockerfile — Node.js App

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
USER node
CMD ["node", "server.js"]
```

## Build Image

```bash
# Build dengan tag
docker build -t namaku/app:1.0 .

# Build dengan custom Dockerfile
docker build -f Dockerfile.prod -t namaku/app:prod .

# Build tanpa cache
docker build --no-cache -t namaku/app:latest .

# Build dengan build arg
docker build --build-arg VERSION=2.0 -t namaku/app:2.0 .
```

## Tag & Push

```bash
# Lihat image lokal
docker images

# Tag image
docker tag myapp:latest username/myapp:1.0
docker tag myapp:latest username/myapp:latest

# Push ke Docker Hub
docker login
docker push username/myapp:1.0
docker push username/myapp:latest

# Pull dari registry
docker pull username/myapp:latest
docker pull python:3.12-slim
```

## Layer Caching

Docker cache setiap layer. Urutan instruksi **sangat penting** — letakkan yang **jarang berubah di atas**.

```dockerfile
# BAIK: layer mahal jarang berubah
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./       # ← jarang berubah
RUN npm ci                   # ← jarang berubah, pakai cache
COPY . .                    # ← sering berubah, di bawah

# BURUK: cache pecah tiap kali
FROM node:22-alpine
WORKDIR /app
COPY . .                    # ← berubah tiap code change
RUN npm ci                   # ← REBUILD tiap kali!
```

## Multi-Stage Build

Teknik untuk memisahkan **build environment** dan **runtime environment** → image lebih kecil.

```dockerfile
# Stage 1: Build
FROM golang:1.23 AS builder
WORKDIR /src
COPY . .
RUN go build -o /app

# Stage 2: Run (hanya binary)
FROM alpine:latest
COPY --from=builder /app /app
CMD ["/app"]
```

## Image Management

```bash
docker images                  # list images
docker image history myapp     # lihat layer history
docker image inspect myapp     # detail metadata
docker image prune             # hapus dangling images
docker image prune -a          # hapus semua unused images
docker rmi myapp:old           # hapus image spesifik
docker save -o myapp.tar myapp # export ke file tar
docker load -i myapp.tar       # import dari file tar
```

## .dockerignore

Sama seperti `.gitignore` — file yang TIDAK dikirim ke build context.

```
# .dockerignore
node_modules
.git
Dockerfile
.env
*.log
dist/
```

## Sumber

- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Writing Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
