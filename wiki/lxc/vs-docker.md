# LXC vs Docker vs VM

## Ringkasan

| | LXC | Docker | Virtual Machine |
|---|---|---|---|
| **Tipe** | System container | Application container | Hypervisor VM |
| **Boot time** | ~1-2 detik | ~1-2 detik | 30-60 detik |
| **Kernel** | Sharing host | Sharing host | Kernel sendiri |
| **Init system** | systemd/init/upstart | Tidak ada (entrypoint) | systemd/init |
| **Proses per container** | Banyak (multi-service) | 1 proses utama (ideal) | Banyak |
| **Overhead** | ~0-2% | ~0-2% | ~5-15% |
| **Isolasi** | Namespaces + cgroups | Namespaces + cgroups | Penuh (hypervisor) |
| **Portabel** | Linux host doang | Linux, Windows, macOS | Semua OS |
| **Ecosystem** | lxc, LXD, Incus | Docker Hub, K8s, Compose | VMware, KVM, VirtualBox |

## Kapan Pakai LXC?

- Butuh **multi-service** jalan bareng (Apache + MySQL + cron + ssh)
- **Development environment** yang mirip production server
- **Self-hosting**: Nextcloud, Plex, Home Assistant, WireGuard VPN
- Testing **upgrade OS** (Ubuntu 22.04 → 24.04)
- **Legacy app** yang butuh init system spesifik
- **Belajar Linux** tanpa install ulang

## Kapan Pakai Docker?

- **1 container = 1 proses** (microservice)
- **CI/CD pipeline** (build → test → deploy)
- **Stateless apps** (12-factor app)
- **Orkestrasi** (Kubernetes, Docker Swarm)
- **Porting antar environment** (dev → staging → prod identik)
- **Ecosystem image** (10M+ image di Docker Hub)

## Kapan Pakai VM?

- **Kernel beda** dari host (Windows di Linux, FreeBSD)
- **Isolasi keamanan maksimum** (tenant berbeda di bare metal yang sama)
- **Hardware emulation** spesifik
- **Snapshot full-machine** + live migration
- **Compliance** yang mewajibkan virtualisasi penuh

## Kombo: Docker Dalam LXC

Bisa — tapi ada caveat:

```bash
# Install Docker di dalam LXC container
lxc-attach -n mycontainer -- apt install docker.io

# Atau mount docker socket dari host:
lxc.mount.entry = /var/run/docker.sock var/run/docker.sock none bind,ro 0 0
```

⚠️ Mount `docker.sock` = container bisa kontrol host Docker — risiko keamanan tinggi.

## Perspektif: LXC vs LXD vs Incus

| | LXC | LXD | Incus |
|---|---|---|---|
| **Apa** | Teknologi low-level | Manager daemon | Fork komunitas LXD |
| **CLI** | `lxc-create`, `lxc-start` | `lxc launch`, `lxc exec` | `incus launch`, `incus exec` |
| **Remote** | ❌ | ✅ REST API | ✅ REST API |
| **Cluster** | ❌ | ✅ | ✅ |
| **Maintainer** | linuxcontainers.org | Canonical | linuxcontainers.org |

> Setelah 2023: LXD resmi proyek Canonical. Incus = fork oleh komunitas Linux Containers yang original.

## Overhead Comparison

```
Physical Server
├── VM: 5-15% overhead (hypervisor + guest kernel)
│   └── Virtual Hardware → Guest Kernel → App
│
├── LXC: ~1-2% overhead (cgroups + namespaces)
│   └── Host Kernel → Container Userland → App
│
└── Docker: ~1-3% overhead (cgroups + namespaces + overlayfs)
    └── Host Kernel → Container → App (satu proses)
```

## Sumber

- [kodekloud.com — LXC vs Docker vs LXD](https://kodekloud.com/blog/what-is-the-difference-between-docker-lxc-and-lxd-containers/)
- [ubuntu.com/blog/lxd-vs-docker](https://ubuntu.com/blog/lxd-vs-docker)
- [unix.stackexchange.com — Docker vs LXD vs LXC](https://unix.stackexchange.com/questions/254956/what-is-the-difference-between-docker-lxd-and-lxc)

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/docker/overview]] — Docker overview (perbandingan dari sisi Docker)
- [[wiki/docker/vs-vm]] — Docker vs VM
