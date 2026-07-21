# Docker Installation

## Linux (Ubuntu/Debian)

### Install via apt repository (recommended)

```bash
# 1. Hapus versi lama
sudo apt remove docker docker-engine docker.io containerd runc

# 2. Setup repository
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. Add repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Install via convenience script

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Post-install: Docker tanpa sudo

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
# Logout/login agar efektif

# Test
docker run hello-world
```

## macOS

Download [Docker Desktop](https://www.docker.com/products/docker-desktop/) — sudah include Docker CLI, daemon, Compose, dan GUI.

Alternatif via Homebrew (hanya CLI, tetap perlu Docker Desktop untuk daemon):

```bash
brew install docker docker-compose
```

## Windows

Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/). Pilih:
- **WSL 2 backend** (recommended) — lebih cepat, full Linux kernel
- **Hyper-V backend** — legacy

## Verifikasi Install

```bash
docker --version          # Docker version 26.x.x
docker compose version    # Docker Compose version v2.x
docker run hello-world    # Test container
docker info               # Info sistem Docker
```

## Troubleshooting

### Permission denied saat docker run

```bash
sudo usermod -aG docker $USER
# Logout/login, atau:
newgrp docker
```

### Daemon tidak jalan

```bash
sudo systemctl status docker
sudo systemctl start docker
sudo systemctl enable docker   # auto-start on boot
```

### Port 2375/2376 untuk remote access

```bash
# JANGAN expose port tanpa TLS di production!
# /etc/docker/daemon.json:
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
  "tls": true,
  "tlscacert": "/etc/docker/certs/ca.pem",
  "tlscert": "/etc/docker/certs/server-cert.pem",
  "tlskey": "/etc/docker/certs/server-key.pem"
}
```

## Sumber

- [Docker Docs — Install](https://docs.docker.com/engine/install/)
- [Docker post-install steps](https://docs.docker.com/engine/install/linux-postinstall/)
