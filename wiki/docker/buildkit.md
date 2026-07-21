# Docker BuildKit & Buildx

BuildKit = **modern build engine** Docker. Lebih cepat, concurrent, dan punya fitur yang tidak ada di legacy builder.

## Kenapa BuildKit?

| Legacy Builder | BuildKit |
|---|---|
| Sequential build | Concurrent (parallel stages) |
| No build secrets | Secret mounts |
| No cache mounts | Persistent build cache |
| Single platform | Multi-platform (arm64 + amd64) |
| Basic caching | Advanced layer caching |
| Tightly coupled | Client-server (buildx) |

## Mengaktifkan BuildKit

```bash
# Sejak Docker 23+, BuildKit default. Bisa paksa:
export DOCKER_BUILDKIT=1
docker build -t myapp .

# Atau via buildx (selalu BuildKit):
docker buildx build -t myapp .
```

## Cache Mounts

Cache dependensi antar build — **nggak perlu download ulang tiap kali**.

```dockerfile
# Node.js — cache npm
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Python — cache pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Go — cache modules
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Apt — cache packages
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt update && apt install -y curl
```

## Secret Mounts

Rahasia yang hanya ada saat build — **tidak masuk layer image**.

```dockerfile
# Mount secret saat build
RUN --mount=type=secret,id=npmrc,dst=/root/.npmrc \
    npm install --registry=https://private-registry.com

# Mount SSH key
RUN --mount=type=ssh \
    git clone git@github.com:private/repo.git
```

```bash
# Pass secret via file
docker build --secret id=npmrc,src=./.npmrc -t myapp .

# Pass secret via env
echo "$NPM_TOKEN" > /tmp/npmrc && \
  docker build --secret id=npmrc,src=/tmp/npmrc -t myapp .
```

## Multi-Platform Build

Build image yang jalan di **amd64 DAN arm64** sekaligus.

```bash
# Setup multi-arch builder
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap

# Build multi-platform
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t bianvigano/myapp:latest \
  --push .
```

```dockerfile
# Gunakan build args untuk conditional
FROM --platform=$BUILDPLATFORM node:22-alpine AS builder
ARG TARGETPLATFORM
RUN echo "Building for $TARGETPLATFORM"
```

## Buildx Commands

```bash
docker buildx ls                    # list builders
docker buildx create --name mybuilder  # create new builder
docker buildx use mybuilder          # switch builder
docker buildx inspect --bootstrap    # start builder
docker buildx rm mybuilder           # remove builder

docker buildx build -t myapp .       # build
docker buildx build --push -t repo/app .  # build + push langsung

docker buildx bake                   # build multiple images
docker buildx imagetools inspect repo/app:latest  # inspect manifest

docker buildx du                     # cache disk usage
docker buildx prune                  # clean build cache
```

## Advanced Dockerfile with BuildKit

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS base
WORKDIR /app

# ---- Dependencies ----
FROM base AS deps
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,src=package.json,dst=package.json \
    --mount=type=bind,src=package-lock.json,dst=package-lock.json \
    npm ci

# ---- Build ----
FROM deps AS build
COPY . .
RUN npm run build

# ---- Production ----
FROM node:22-alpine AS prod
RUN addgroup -S app && adduser -S app -G app
COPY --from=build --chown=app:app /app/dist /app
USER app
EXPOSE 3000
CMD ["node", "server.js"]
```

## BuildKit Cache di CI

```bash
# GitHub Actions — cache via gha
docker buildx build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  -t myapp .

# Registry cache
docker buildx build \
  --cache-from type=registry,ref=myrepo/app:cache \
  --cache-to type=registry,ref=myrepo/app:cache,mode=max \
  -t myapp .
```

## Performance Tips

1. Cache mount mengurangi download 90% di rebuild
2. Multi-stage → image final lebih kecil
3. `--parallel` build multi-stage concurrently
4. `.dockerignore` kurangi build context
5. `RUN --mount=type=cache` untuk package managers

## Sumber

- [Docker BuildKit](https://docs.docker.com/build/buildkit/)
- [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
- [BuildKit Cache Mounts](https://docs.docker.com/build/cache/backends/)
