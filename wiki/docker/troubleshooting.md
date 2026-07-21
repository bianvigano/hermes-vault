# Docker Troubleshooting

Masalah umum dan cara debug.

## "Container exited immediately"

```bash
# Cek log
docker logs <name>

# Cek exit code
docker inspect <name> --format='{{.State.ExitCode}}'

# Jalanin ulang dengan shell untuk debug
docker run -it --rm --entrypoint /bin/sh myapp

# Pastikan CMD/ENTRYPOINT tidak exit
# CMD ["tail", "-f", "/dev/null"]  # untuk testing
```

## "Port already in use"

```bash
# Cari proses yang pakai port
sudo lsof -i :8080
sudo ss -tlnp | grep 8080

# Solusi: ganti host port
docker run -p 8081:80 nginx
```

## "Cannot connect to Docker daemon"

```bash
# Cek daemon jalan
sudo systemctl status docker

# Permission issue — tambah user ke docker group
sudo usermod -aG docker $USER
newgrp docker

# Atau cek DOCKER_HOST
echo $DOCKER_HOST
unset DOCKER_HOST  # jika tidak perlu remote

# Restart daemon
sudo systemctl restart docker
```

## Build Lambat / Cache Tidak Jalan

```bash
# Lihat cache
docker buildx du

# Purge cache
docker builder prune

# Build tanpa cache (force)
docker build --no-cache -t myapp .

# Pastikan .dockerignore ada
cat .dockerignore   # node_modules, .git, dll harus di-ignore

# Cek urutan Dockerfile — layer mahal di atas
docker history myapp
```

## Disk Penuh

```bash
# Cek penggunaan
docker system df

# Bersihkan
docker system prune          # container stopped + unused images
docker system prune -a       # + all unused images
docker system prune -a --volumes  # + unused volumes

# Per-komponen
docker container prune
docker image prune -a
docker volume prune
docker network prune
docker builder prune   # build cache
```

## "No space left on device"

```bash
# Cek docker storage
sudo du -sh /var/lib/docker/

# Log piling up?
du -sh /var/lib/docker/containers/*/*.log
truncate -s 0 /var/lib/docker/containers/*/*.log

# Set log rotation di daemon.json:
# { "log-driver": "local", "log-opts": { "max-size": "10m", "max-file": "3" } }
```

## Container Tidak Bisa Akses Internet

```bash
# Cek DNS
docker exec <name> nslookup google.com

# Cek network
docker network inspect bridge

# Restart network
sudo systemctl restart docker

# Custom DNS
docker run --dns 8.8.8.8 --dns 1.1.1.1 nginx
```

## Container Tidak Bisa Komunikasi Antar Satu Sama Lain

```bash
# Harus di user-defined bridge network!
docker network create mynet
docker run --network mynet --name app1 ...
docker run --network mynet --name app2 ...

# Cek DNS internal
docker exec app1 ping app2    # hostname = container name
docker exec app1 nslookup app2
```

## Debug Dalam Container

```bash
docker exec -it <name> /bin/sh          # Alpine
docker exec -it <name> /bin/bash        # Debian/Ubuntu
docker exec -it <name> sh               # generic fallback

# Kalau container langsung exit, pakai entrypoint override:
docker run -it --rm --entrypoint /bin/sh myapp

# Inspect filesystem
docker diff <name>        # lihat perubahan file

# Copy file dari container
docker cp <name>:/app/logs ./logs
# Copy file ke container
docker cp ./config.json <name>:/app/
```

## OOM (Out of Memory)

```bash
# Cek memory usage
docker stats --no-stream

# Set memory limit
docker update --memory=512m <name>

# Cek siapa yang kena OOM kill
docker inspect <name> --format='{{.State.OOMKilled}}'
dmesg | grep -i oom
```

## Debug Pattern — Interactive Session

```bash
# 1. Simpan image running container
docker commit <name> debug-image

# 2. Jalanin dengan shell
docker run -it --rm debug-image /bin/sh

# 3. Investigasi lalu hapus
docker rmi debug-image
```

## Sumber

- [Docker troubleshooting](https://docs.docker.com/config/daemon/troubleshoot/)
