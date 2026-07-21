# Docker Networking

Docker networking memungkinkan container berkomunikasi dengan container lain dan dengan host/outside world. Docker memiliki beberapa **network driver**.

## Network Drivers

| Driver | Use Case | Scope |
|---|---|---|
| **bridge** | Komunikasi antar container di host yang sama (default) | Single host |
| **host** | Performance maksimum, gunakan network host langsung | Single host |
| **overlay** | Komunikasi antar container di host berbeda (Swarm) | Multi-host |
| **none** | Isolasi total, tanpa network | Single container |
| **ipvlan/macvlan** | Container pakai IP fisik (like VM) | Single host |

## Bridge Network (Default)

Setiap container di bridge network dapat berkomunikasi **dengan nama container** via DNS internal Docker.

```bash
# Container di default bridge — pakai --link (legacy, hindari)
docker run --name db -d postgres
docker run --name app --link db -d myapp

# Container di custom bridge — auto DNS!
docker network create mynet
docker run --name db --network mynet -d postgres
docker run --name app --network mynet -d myapp
# app bisa ping db (hostname = container name)
```

### Perbedaan default bridge vs user-defined bridge

| Fitur | Default Bridge | User-defined Bridge |
|---|---|---|
| DNS resolution | Tidak (pakai `--link`) | Ya (auto) |
| Network isolation | 1 network untuk semua | 1 network per project |
| Konfigurasi | Terbatas | Subnet, gateway, dll custom |

## Host Network

Container **sharing network stack** dengan host. Tidak ada isolasi network — container gunakan port host langsung.

```bash
docker run --network host nginx
# nginx langsung listen di port 80 host
# Tidak perlu -p mapping
# Tidak bisa run 2 container di port sama
```

Use case: aplikasi yang perlu performa network maksimum, latency rendah.

## Overlay Network

Untuk komunikasi antar container di **host berbeda** (Docker Swarm). Container di host A bisa komunikasi dengan container di host B via overlay network.

```bash
docker network create -d overlay myoverlay
docker service create --name app --network myoverlay myapp
```

## Network Commands

```bash
docker network ls                     # list networks
docker network create mynet           # buat bridge network
docker network create --driver overlay --subnet 10.1.0.0/24 myoverlay
docker network inspect mynet          # lihat detail
docker network connect mynet app      # attach container ke network
docker network disconnect mynet app   # detach container
docker network rm mynet               # hapus network
docker network prune                  # hapus unused networks
```

## Port Mapping (`-p`)

Expose port container ke host.

```bash
docker run -p 8080:80 nginx         # HOST:CONTAINER
# Akses: http://localhost:8080 → nginx port 80

docker run -p 127.0.0.1:5432:5432 postgres  # hanya localhost

docker run -P myapp                  # publish semua EXPOSE port
```

## Container DNS

Docker menjalankan **embedded DNS server** (127.0.0.11). Container query DNS ini untuk resolve nama container lain.

```bash
docker run --name app --network mynet alpine ping db
# Docker DNS: "db" → 172.18.0.2 (IP container db)
```

## Troubleshooting

```bash
docker network inspect bridge        # lihat semua container di bridge
docker exec app nslookup db          # cek DNS dari dalam container
docker exec app ping db              # test connectivity
docker exec app curl http://api:3000 # test HTTP antar container
```

## Sumber

- [Docker Networking Overview](https://docs.docker.com/engine/network/)
- [Bridge network tutorial](https://docs.docker.com/engine/network/tutorials/standalone/)
