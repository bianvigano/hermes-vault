# Arsitektur LXC

LXC menggunakan arsitektur **berlapis (layered)** yang memisahkan UI, orchestration, subsistem, dan kernel interface.

## 5 Layer Arsitektur

```
┌─────────────────────────────────────────┐
│ Layer 4: Communication & Control        │  ← CLI tools, REST API (LXD), monitor daemon
├─────────────────────────────────────────┤
│ Layer 3: Subsystems                     │  ← Network, Storage, Security, Cgroups
├─────────────────────────────────────────┤
│ Layer 2: Core Orchestration             │  ← lxc_handler, lxc_conf, confile parser, state
├─────────────────────────────────────────┤
│ Layer 1: User Interface                 │  ← lxc_container API, CLI tools, templates
├─────────────────────────────────────────┤
│ Layer 5: Utilities                      │  ← utils.c, file_utils.c, memory_utils.h
└─────────────────────────────────────────┘
```

## 3 Struktur Data Inti

### `lxc_container` — Public API Interface

Entry point publik untuk liblxc. Semua operasi container lewat struct ini:

- `c->create()` — buat container
- `c->start()` — jalankan container
- `c->stop()` — hentikan container
- `c->shutdown()` — graceful shutdown
- `c->destroy()` — hapus container
- `c->state()` — status container
- `c->init_pid()` — PID init proses dalam container

Didefinisikan di `src/lxc/lxccontainer.h`

### `lxc_handler` — Container Lifecycle Manager

Struct internal yang mengelola **runtime state** container:

- Proses init container
- Signal handling
- Console/TTY management
- Monitor proses (lxc-monitord)
- Checkpoint/Restore (CRIU)

Didefinisikan di `src/lxc/start.h`

### `lxc_conf` — Configuration System

Menyimpan seluruh konfigurasi container:

- Network config
- Storage/mount config
- Cgroup limits
- Security profiles (AppArmor, SELinux, Seccomp)
- Capabilities
- Namespace settings

Didefinisikan di `src/lxc/conf.h`

## Fitur Kernel yang Dipakai LXC

| Kernel Feature | Fungsi |
|---|---|
| **Namespaces** | Isolasi: pid, net, mnt, uts, ipc, user, cgroup |
| **Cgroups (v1/v2)** | Resource control: CPU, RAM, blkio, devices |
| **AppArmor / SELinux** | Mandatory Access Control (MAC) |
| **Seccomp** | System call filtering |
| **Capabilities** | Privilege granular (drop `CAP_SYS_ADMIN`, `CAP_NET_RAW`, dll.) |
| **pivot_root** | Ganti root filesystem container |
| **User Namespaces** | Map UID/GID container ke non-root host (unprivileged containers) |

## Flow: Create → Start → Attach

1. **Create**: `lxc_container_new()` → `c->create()` → download template → extract rootfs → tulis config
2. **Start**: `c->start()` → setup namespaces → apply cgroup → mount rootfs → jalankan `/sbin/init`
3. **Attach**: `lxc_attach()` → masuk namespaces container → jalankan shell/proses

## Command & State System

- **lxc-monitord** — daemon monitor yang track state container (RUNNING, STOPPED, FROZEN)
- **State machine** — transisi antar state via command IPC
- **Command socket** — komunikasi antar `lxc` tools dan `lxc-monitord`

## Sumber

- [deepwiki.com/lxc/lxc/2-core-architecture](https://deepwiki.com/lxc/lxc/2-core-architecture)
- [linuxcontainers.org/lxc/introduction](https://linuxcontainers.org/lxc/introduction/)

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/containers]] — Lifecycle container
- [[wiki/lxc/networking]] — Konfigurasi network
- [[wiki/lxc/storage]] — Storage backend
