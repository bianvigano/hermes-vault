# Docker Registry & Docker Hub

Registry = tempat menyimpan dan mendistribusikan Docker images. Docker Hub adalah registry publik default.

## Docker Hub

### Buat Akun & Repository

1. Daftar di [hub.docker.com](https://hub.docker.com)
2. Buat **Access Token** (Settings → Security → New Access Token)
   - Simpan tokennya — ini pengganti password untuk CLI
3. Login dari CLI:
   ```bash
   docker login -u USERNAME
   # Masukkan access token (bukan password)
   ```

### Push Image

```bash
# 1. Build image
docker build -t myapp:1.0 .

# 2. Tag dengan format: USERNAME/REPO:TAG
docker tag myapp:1.0 bianvigano/myapp:1.0
docker tag myapp:1.0 bianvigano/myapp:latest

# 3. Push
docker push bianvigano/myapp:1.0
docker push bianvigano/myapp:latest
```

### Pull Image

```bash
docker pull python:3.12-slim           # official image
docker pull bianvigano/myapp:latest    # user image
docker pull ubuntu:noble               # specific tag
```

### Repository Types

| Type | Visibility | Free Limit |
|---|---|---|
| Public | Siapa saja bisa pull | Unlimited |
| Private | Hanya yang di-invite | 1 private repo (free) |

### Best Practices

- Tag dengan **version** (`1.0.0`), bukan hanya `latest`
- Push multi-arch image (`linux/amd64` + `linux/arm64`)
- Set description & README di Docker Hub
- Scan vulnerability dengan Docker Scout

```bash
docker scout quickview bianvigano/myapp:latest
```

## Private Registry

### Jalankan Registry Sendiri

```bash
# Run local registry di port 5000
docker run -d -p 5000:5000 --name registry registry:2

# Tag image ke local registry
docker tag myapp localhost:5000/myapp:1.0

# Push
docker push localhost:5000/myapp:1.0

# Pull
docker pull localhost:5000/myapp:1.0
```

### Registry dengan Auth + HTTPS

```yaml
# docker-compose.yml
services:
  registry:
    image: registry:2
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_HTTP_TLS_CERTIFICATE: /certs/registry.crt
      REGISTRY_HTTP_TLS_KEY: /certs/registry.key
    volumes:
      - ./auth:/auth
      - ./certs:/certs
      - registry-data:/var/lib/registry
    ports:
      - "443:443"
```

### Cloud Registries

| Provider | Service | URL Format |
|---|---|---|
| AWS | ECR | `ACCOUNT.dkr.ecr.REGION.amazonaws.com/NAME` |
| GCP | Artifact Registry | `REGION-docker.pkg.dev/PROJECT/NAME` |
| Azure | ACR | `NAME.azurecr.io` |
| GitHub | GHCR | `ghcr.io/USERNAME/NAME` |

```bash
# AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# GitHub GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

## Image Tags — Convention

```bash
bianvigano/myapp:1.2.3              # exact semver
bianvigano/myapp:1.2                 # minor version (floating)
bianvigano/myapp:latest              # latest stable (floating)
bianvigano/myapp:sha-abc123          # commit hash
bianvigano/myapp:dev                 # development
bianvigano/myapp:1.2.3-alpine        # variant
```

## Sumber

- [Docker Hub](https://hub.docker.com)
- [Docker Registry](https://docs.docker.com/registry/)
- [AWS ECR](https://aws.amazon.com/ecr/)
