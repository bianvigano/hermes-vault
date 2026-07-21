# Docker CI/CD

Pola umum untuk build, test, dan deploy Docker images secara otomatis.

## GitHub Actions — Build & Push

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Pipeline Stages

```
┌────────┐    ┌────────┐    ┌────────┐    ┌──────────┐    ┌─────────┐
│  Lint  │───▶│  Test  │───▶│ Build  │───▶│  Push    │───▶│ Deploy  │
│        │    │        │    │ Image  │    │ Registry │    │         │
└────────┘    └────────┘    └────────┘    └──────────┘    └─────────┘
```

### Stage Dockerfile

```dockerfile
FROM node:22-alpine AS base
WORKDIR /app

# ---- Dependencies (cached) ----
FROM base AS deps
COPY package*.json ./
RUN npm ci

# ---- Test ----
FROM deps AS test
COPY . .
RUN npm run lint
RUN npm test

# ---- Production ----
FROM base AS production
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
USER node
CMD ["node", "dist/server.js"]
```

### Build per Stage untuk CI

```bash
# CI: test stage
docker build --target test -t myapp:test .
docker run --rm myapp:test npm test

# CI: production stage
docker build --target production -t myapp:latest .
```

## GitLab CI

```yaml
# .gitlab-ci.yml
build:
  image: docker:27
  services:
    - docker:27-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
```

## Deploy Patterns

### 1. Pull & Run (Simple)

```bash
# Di server
docker pull myapp:latest
docker stop myapp || true
docker rm myapp || true
docker run -d --name myapp -p 8080:80 --restart unless-stopped myapp:latest
```

### 2. Docker Compose Remote

```bash
# CI push image → SSH to server → docker compose pull & up
ssh user@server "cd /opt/app && docker compose pull && docker compose up -d"
```

### 3. Watchtower — Auto-Update

```bash
# Jalankan Watchtower untuk auto-pull + restart
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  myapp --interval 30
```

### 4. Kubernetes (Production)

CI build & push image → K8s rolling update → no downtime.

## Security in CI/CD

```yaml
# Scan sebelum push
- name: Docker Scout
  run: |
    docker scout cves myapp:latest
    docker scout recommendations myapp:latest
```

```bash
# Jangan hardcode credential di CI config
# Pakai GitHub Secrets / GitLab Variables / Vault
docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_TOKEN }}
```

## CI/CD Best Practices

1. **Build sekali, deploy banyak**: jangan rebuild per environment (dev/staging/prod)
2. **Pin base image**: `FROM node:20.10.0-alpine` bukan `node:alpine`
3. **Cache layer**: manfaatkan GitHub Actions cache / BuildKit cache
4. **Multi-platform**: `docker buildx build --platform linux/amd64,linux/arm64`
5. **Image signing**: `docker trust sign` atau cosign
6. **Scout/Snyk/Trivy** scan sebelum push

## Sumber

- [GitHub Actions — Docker](https://docs.docker.com/build/ci/github-actions/)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
