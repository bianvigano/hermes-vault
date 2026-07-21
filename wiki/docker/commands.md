# Docker Commands — Cheatsheet

Ringkasan command Docker yang paling sering dipakai.

## Container Lifecycle

```bash
docker run -d --name web -p 8080:80 nginx   # run background, named, port map
docker run -it ubuntu bash                   # interactive terminal
docker run --rm alpine sh                    # auto-remove after stop
docker create --name temp nginx              # create only, don't start
docker start web                             # start stopped container
docker stop web                              # graceful stop (SIGTERM)
docker kill web                              # force kill (SIGKILL)
docker restart web                           # stop + start
docker pause web                             # freeze container
docker unpause web                           # unfreeze
docker rm web                                # remove stopped container
docker rm -f web                             # force remove
```

## Info & Monitoring

```bash
docker ps                           # running containers
docker ps -a                        # all containers
docker ps -a -q                     # all container IDs only
docker stats                        # live resource usage
docker top web                      # processes inside container
docker port web                     # port mappings
docker logs web                     # logs
docker logs -f web                  # follow logs
docker logs --tail 50 web           # last 50 lines
docker logs --since 1h web          # logs since 1 hour ago
docker diff web                     # changes to filesystem
docker inspect web                  # detailed JSON info
docker inspect -f '{{.State.Status}}' web  # specific field
```

## Exec (Masuk Container)

```bash
docker exec -it web bash            # interactive shell
docker exec web ls /app             # one-off command
docker exec -u root web whoami      # run as specific user
docker exec web cat /etc/hosts      # read file inside container
docker attach web                   # attach to PID 1 (jarang dipakai)
```

## Images

```bash
docker images                       # list images
docker images -a                    # termasuk intermediate layers
docker pull nginx:latest            # download from registry
docker build -t myapp .             # build from Dockerfile
docker build -t myapp:v2 --no-cache .  # force rebuild
docker tag myapp user/myapp:v1      # tag for registry
docker push user/myapp:v1           # push to registry
docker rmi myapp:v1                 # remove image
docker rmi $(docker images -q)      # remove ALL images
docker image prune                  # remove dangling images
docker image prune -a               # remove all unused
docker save -o myapp.tar myapp      # export to tar
docker load -i myapp.tar            # import from tar
docker history myapp                # layer history
```

## Networks

```bash
docker network ls                   # list networks
docker network create mynet         # create bridge network
docker network inspect mynet        # network details
docker network connect mynet web    # add container to network
docker network disconnect mynet web # remove from network
docker network rm mynet             # remove network
docker network prune                # remove unused
```

## Volumes

```bash
docker volume ls                    # list volumes
docker volume create mydata         # create named volume
docker volume inspect mydata        # volume details
docker volume rm mydata             # remove volume
docker volume prune                 # remove unused
```

## System & Cleanup

```bash
docker info                         # system-wide info
docker system df                    # disk usage
docker system prune                 # remove unused containers/networks/images
docker system prune -a --volumes    # remove EVERYTHING unused
docker events                       # live events stream
docker version                      # version info
docker login                        # login to registry
docker logout                       # logout
```

## Compose

```bash
docker compose up                   # start services (foreground)
docker compose up -d                # start background
docker compose up -d --build        # rebuild then start
docker compose down                 # stop + remove
docker compose down -v              # stop + remove + delete volumes
docker compose ps                   # service status
docker compose logs -f api          # follow service logs
docker compose restart api          # restart service
docker compose exec api bash        # shell into service
docker compose build                # build only
docker compose pull                 # pull latest images
docker compose config               # validate + view parsed config
```

## One-Liner Tools

```bash
# Hapus semua container stopped
docker rm $(docker ps -a -q)

# Hapus semua container running
docker rm -f $(docker ps -q)

# Hapus semua dangling images
docker rmi $(docker images -f "dangling=true" -q)

# Stop + remove all containers
docker stop $(docker ps -q) && docker rm $(docker ps -a -q)

# Masuk container terakhir
docker exec -it $(docker ps -lq) bash

# Lihat IP container
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web
```

## Sumber

- [Docker CLI Reference](https://docs.docker.com/reference/cli/docker/)
