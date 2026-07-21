# Container Lifecycle

## Lifecycle Container

```
CREATED → STARTING → RUNNING → STOPPED
                    ↘ FREEZING → FROZEN → THAWED
                    ↘ KILLING
```

## Command Dasar

### Create

```bash
# Buat dari template download (online)
lxc-create -t download -n nama-container -- --dist ubuntu --release jammy --arch amd64

# List distro yang tersedia
lxc-create -t download -n test -- --list

# Buat dengan storage backend tertentu
lxc-create -t download -n nama-container -B zfs -- --dist debian --release bookworm
```

### Start / Stop

```bash
# Start (daemon mode, background)
lxc-start -n nama-container -d

# Start (foreground, debug)
lxc-start -n nama-container -F

# Graceful shutdown — kirim SIGPWR ke init
lxc-stop -n nama-container

# Force kill — SIGKILL
lxc-stop -n nama-container -k

# Reboot
lxc-stop -n nama-container -r
```

### Status

```bash
# Info detail container
lxc-info -n nama-container

# Cek state (RUNNING/STOPPED/FROZEN)
lxc-info -n nama-container -s

# Lihat PID init
lxc-info -n nama-container -p

# Lihat IP address
lxc-info -n nama-container -i

# List semua container
lxc-ls

# List + status
lxc-ls -f
```

### Attach / Execute

```bash
# Masuk shell ke container (butuh login)
lxc-attach -n nama-container

# Execute command langsung
lxc-attach -n nama-container -- apt update

# Execute dengan environment bersih
lxc-attach -n nama-container --clear-env -- /bin/bash

# Execute dengan user tertentu
lxc-attach -n nama-container -- su - username
```

### Console / TTY

```bash
# Attach ke console container (Ctrl+A Q untuk keluar)
lxc-console -n nama-container

# Force attach
lxc-console -n nama-container -f
```

### Freeze / Unfreeze

```bash
# Freeze (SIGSTOP semua proses)
lxc-freeze -n nama-container

# Unfreeze (SIGCONT semua proses)
lxc-unfreeze -n nama-container
```

### Clone

```bash
# Clone container
lxc-copy -n source -N clone-name

# Clone + rename
lxc-copy -n old-name -N new-name
```

### Snapshot

```bash
# Buat snapshot (butuh storage backend yang support: ZFS/Btrfs/LVM)
lxc-snapshot -n nama-container

# List snapshot
lxc-snapshot -n nama-container -L -C

# Restore snapshot
lxc-snapshot -n nama-container -r snap0
```

### Destroy

```bash
# Hapus container (harus STOPPED dulu)
lxc-destroy -n nama-container

# Force destroy (meskipun running)
lxc-destroy -n nama-container -f
```

## Autostart

Di `/var/lib/lxc/nama-container/config` (atau `~/.local/share/lxc/nama-container/config`):

```
lxc.start.auto = 1
lxc.start.delay = 5
lxc.start.order = 10
lxc.group = web
```

## Monitor / Watch

```bash
# Monitor state changes
lxc-monitor -n nama-container

# Top/htop dalam container
lxc-top
```

## Perbedaan Privileged vs Unprivileged

| | Privileged | Unprivileged |
|---|---|---|
| **UID 0 di container** | Root host | User biasa di host (subuid) |
| **Path storage** | `/var/lib/lxc/` | `~/.local/share/lxc/` |
| **Keamanan** | Kurang aman | Lebih aman (rekomendasi) |
| **Network tambahan** | Bisa langsung | Butuh `lxc-user-nic` (setuid) |
| **Command** | `sudo lxc-*` | `lxc-*` (tanpa sudo) |

## File Konfigurasi

Lokasi config:

```
# Privileged
/var/lib/lxc/<nama>/config

# Unprivileged
~/.local/share/lxc/<nama>/config
```

Contoh minimal:

```ini
lxc.uts.name = mycontainer
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.rootfs.path = dir:/var/lib/lxc/mycontainer/rootfs
```

## Sumber

- [linuxcontainers.org/lxc/documentation](https://linuxcontainers.org/lxc/documentation/)
- `man lxc-create`, `man lxc-start`, `man lxc-attach`

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/architecture]] — Arsitektur internal
- [[wiki/lxc/installation]] — Installasi
- [[wiki/lxc/networking]] — Konfigurasi network
- [[wiki/lxc/storage]] — Storage backend
- [[wiki/lxc/commands]] — Cheatsheet lengkap
