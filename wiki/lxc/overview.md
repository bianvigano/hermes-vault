# LXC Overview

LXC (Linux Containers) adalah **userspace interface** untuk fitur kernel Linux yang menyediakan **OS-level virtualization** — container yang menjalankan sistem Linux lengkap tanpa perlu kernel terpisah.

## Apa Itu LXC?

LXC menciptakan environment yang **sedekat mungkin dengan instalasi Linux standar** — dengan init system, multiple proses, dan service — tapi tanpa overhead menjalankan kernel sendiri seperti VM.

Bayangkan: setengah jalan antara `chroot` (isolasi minimal) dan Virtual Machine (isolasi penuh dengan kernel sendiri).

## Kenapa LXC?

| Kapan Pakai LXC | Kapan Jangan |
|---|---|
| Butuh full Linux environment (init system, cron, ssh) | Cuma butuh 1 aplikasi per container → pakai Docker |
| Testing multi-service app di environment bersih | Microservices stateless → Docker/Kubernetes |
| Isolasi ringan untuk development/production | Perlu kernel berbeda dari host |
| Self-hosting service (LAMP, mail server, VPN) | Butuh orkestrasi kompleks → Kubernetes |
| Belajar Linux/DevOps tanpa install ulang OS | |

## Konsep Inti

- **Container** — instance Linux terisolasi, sharing kernel host
- **Template** — blueprint/image untuk membuat container (Ubuntu, Debian, Alpine, dll.)
- **Namespace** — isolasi resource kernel (PID, network, mount, user, IPC, UTS)
- **Cgroups** — pembatasan resource (CPU, RAM, disk I/O)
- **Rootfs** — filesystem root container (bisa directory, ZFS, Btrfs, LVM)

## LXC vs Istilah Lain

| Istilah | Deskripsi |
|---|---|
| **LXC** | Teknologi container level rendah (liblxc + tools CLI: `lxc-create`, `lxc-start`) |
| **LXD** | Daemon/manager di atas LXC — REST API, clustering, remote management, lebih user-friendly |
| **Incus** | Fork LXD oleh komunitas Linux Containers (setelah LXD pindah ke Canonical 2023) |
| **Docker** | Application container — 1 proses per container, image layer, Dockerfile |

> **LXC/LXD = system container** (full OS). **Docker = application container** (1 app per container).

## Komponen LXC

- **liblxc** — library C untuk API container management
- **Language bindings** — Python 3, Lua, Go, Ruby, Haskell
- **CLI tools** — `lxc-create`, `lxc-start`, `lxc-stop`, `lxc-attach`, `lxc-destroy`, dll.
- **Templates** — skrip untuk membuat rootfs distro berbeda (`lxc-download`, `lxc-oci`)

## Lisensi

LGPLv2.1+ — free software, dikelola oleh komunitas **linuxcontainers.org**.

## Dukungan Jangka Panjang

- **LXC 6.0** — supported sampai June 2029
- **LXC 5.0** — supported sampai June 2027

## Sumber

- [linuxcontainers.org/lxc/introduction](https://linuxcontainers.org/lxc/introduction/)
- [linuxcontainers.org/lxc/documentation](https://linuxcontainers.org/lxc/documentation/)
- [deepwiki.com/lxc/lxc/2-core-architecture](https://deepwiki.com/lxc/lxc/2-core-architecture)

## Lanjut Baca

- [[wiki/lxc/architecture]] — Cara kerja internal LXC
- [[wiki/lxc/installation]] — Install LXC di Ubuntu/Debian
- [[wiki/lxc/containers]] — Lifecycle container: create, start, stop, destroy
- [[wiki/lxc/vs-docker]] — Perbandingan detail LXC vs Docker
- [[wiki/lxc/best-practices]] — Best practices + checklist
