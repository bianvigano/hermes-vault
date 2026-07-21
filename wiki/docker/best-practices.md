# Docker Best Practices & Security

## Dockerfile Best Practices

### 1. Pilih Base Image yang Tepat

```dockerfile
# BURUK — 600MB+
FROM ubuntu:latest
RUN apt update && apt install -y python3 python3-pip

# BAIK — pakai official slim/alpine image
FROM python:3.12-slim     # ~50MB
FROM node:22-alpine        # ~50MB
FROM golang:1.23-alpine    # ~70MB
```

### 2. Optimalkan Layer Caching

Letakkan instruksi dari yang **paling jarang berubah** ke **sering berubah**.

```dockerfile
# BAIK
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./      # jarang berubah → cache
RUN npm ci                  # jarang berubah → cache
COPY . .                   # sering berubah → di paling bawah

# BURUK
COPY . .
RUN npm ci                 # cache pecah tiap code change
```

### 3. Multi-Stage Build

Pisahkan build & runtime → image lebih kecil + lebih aman.

```dockerfile
# Build stage
FROM golang:1.23 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app

# Run stage — TIDAK ada Go SDK, hanya binary
FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
```

### 4. Jangan Run sebagai Root

```dockerfile
FROM node:22-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD ["node", "server.js"]
```

### 5. Kurangi Jumlah Layer

```dockerfile
# BURUK — 3 layer
RUN apt update
RUN apt install -y curl
RUN apt clean

# BAIK — 1 layer
RUN apt update && apt install -y curl && apt clean && rm -rf /var/lib/apt/lists/*
```

### 6. .dockerignore

```
node_modules
.git
.env
*.log
Dockerfile
docker-compose.yml
dist/
coverage/
```

### 7. Gunakan COPY, Bukan ADD

```dockerfile
COPY . /app        # selalu pakai COPY
# ADD hanya untuk auto-extract tar atau URL remote
```

## Security Best Practices

### 1. Scan Vulnerabilities

```bash
docker scout quickview myapp
docker scout recommendations myapp
docker scan myapp           # Snyk integration
```

### 2. Jangan Hardcode Secrets

```dockerfile
# BURUK
ENV DATABASE_PASSWORD=supersecret

# BAIK — pakai secrets / env file
# docker run -e DATABASE_PASSWORD=$(cat /run/secrets/db_pass)
```

Gunakan Docker Secrets (Swarm) atau external secrets manager.

### 3. Read-Only Root Filesystem

```bash
docker run --read-only --tmpfs /tmp myapp
```

### 4. Limit Capabilities

```bash
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx
```

### 5. Resource Limits

```bash
docker run --memory="256m" --cpus="1" myapp  # cegah 1 container monopolize host
```

### 6. Gunakan Trusted Base Images

- Official images dari Docker Hub (`_/nginx`, `_/python`)
- Verified Publisher images
- Docker Scout untuk cek supply chain

## Production Checklist

- [ ] Gunakan multi-stage build
- [ ] Non-root user (`USER`)
- [ ] Pin base image ke digest (bukan tag `latest`)
- [ ] Scan vulnerabilities
- [ ] Read-only rootfs (`--read-only`)
- [ ] Resource limits (`--memory`, `--cpus`)
- [ ] Healthcheck di container
- [ ] Logs ke stdout/stderr (jangan ke file)
- [ ] Restart policy (`--restart unless-stopped`)
- [ ] Jangan expose Docker daemon ke network

## Dockerfile untuk Production

```dockerfile
FROM python:3.12-slim@sha256:abc123...
WORKDIR /app

# Create non-root user
RUN groupadd -r app && useradd -r -g app app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Security hardening
RUN chown -R app:app /app
USER app

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Sumber

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
