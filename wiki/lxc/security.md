# LXC Security

## Level Keamanan

| Lapisan | Mekanisme |
|---|---|
| **User Namespaces** | UID/GID container ≠ UID/GID host |
| **Capabilities** | Strip privilege kernel granular |
| **Seccomp** | Filter system call yang boleh dipakai |
| **AppArmor / SELinux** | Mandatory Access Control |
| **Cgroups** | Batasi resource (CPU/RAM/blkio) |
| **Read-only rootfs** | Filesystem tidak bisa ditulis |

## Privileged vs Unprivileged

**Privileged container:** root di container = root di host. Kalau container di-escape → akses penuh ke host.

**Unprivileged container:** root di container dipetakan ke UID non-root di host via user namespaces. Escape container = akses user biasa doang.

```bash
# Cek mapping UID
grep $USER /etc/subuid
# Output: bian:100000:65536
# Berarti: UID 0 di container = UID 100000 di host
#          UID 65535 di container = UID 165535 di host
```

## User Namespace Mapping

Konfig di `~/.config/lxc/default.conf`:

```ini
lxc.idmap = u 0 100000 65536
lxc.idmap = g 0 100000 65536
```

System-wide setup:

```bash
# /etc/subuid — per user
bian:100000:65536

# /etc/subgid — per user
bian:100000:65536
```

## Capabilities

Drop semua capability, tambah yang perlu saja:

```ini
# Drop semua
lxc.cap.drop =

# Tambah beberapa yang perlu
lxc.cap.keep = net_bind_service
lxc.cap.keep = sys_nice
# Jangan: lxc.cap.keep = sys_admin  ← ini bahaya!
```

Capabilities umum yang sering di-drop:

- `sys_admin` — terlalu banyak power
- `net_admin` — manipulasi network
- `sys_module` — load/unload kernel module
- `sys_time` — set system time
- `mac_admin` / `mac_override` — MAC policy

## Seccomp (System Call Filter)

Default profile: `/usr/share/lxc/config/common.seccomp`

Custom profile:

```bash
# Buat profile whitelist
cat > /usr/share/lxc/config/my.seccomp << 'EOF'
2
blacklist
[all]
# Allow specific syscalls
open
openat
read
write
close
EOF

# Pakai di config container
lxc.seccomp.profile = /usr/share/lxc/config/my.seccomp
```

## AppArmor

Profile default: `lxc-container-default-cgns`

Custom:

```ini
lxc.apparmor.profile = lxc-container-default-cgns
lxc.apparmor.profile = unconfined  # disable (tidak direkomendasi)
```

## SELinux

```ini
lxc.selinux.context = system_u:system_r:lxc_t:s0:c22
```

## Resource Limits (Cgroups)

### Cgroup v2

```ini
# CPU
lxc.cgroup2.cpu.max = 200000 100000    # max 2 core
lxc.cgroup2.cpu.weight = 100            # priority (default 100)

# Memory
lxc.cgroup2.memory.max = 512M
lxc.cgroup2.memory.swap.max = 0         # disable swap

# I/O
lxc.cgroup2.io.max = "8:0 rbps=10485760 wbps=10485760"

# PIDs
lxc.cgroup2.pids.max = 200
```

### Cgroup v1 (untuk kernel lama)

```ini
lxc.cgroup.cpu.shares = 512
lxc.cgroup.memory.limit_in_bytes = 512M
lxc.cgroup.blkio.throttle.read_bps_device = "8:0 10485760"
```

## Read-Only Rootfs

```ini
# Rootfs read-only — tulis hanya ke tmpfs
lxc.rootfs.options = ro
lxc.mount.entry = tmpfs tmp tmpfs defaults 0 0
lxc.mount.entry = tmpfs run tmpfs defaults 0 0
```

## Device Control

```ini
# Whitelist device
lxc.cgroup2.devices.allow = c 4:0 rwm    # /dev/tty0
lxc.cgroup2.devices.deny = a              # deny all
```

## Best Practices

1. **Selalu pakai unprivileged containers** — fundamental, bukan opsional
2. **Drop semua capabilities** — tambah satu-satu sesuai kebutuhan
3. **Pakai seccomp profile** — filter syscall yang tidak perlu
4. **Batasi resource** — CPU/Memory/PID limit
5. **Read-only rootfs kalau bisa** — container immutable
6. **Jangan mount `/var/run/docker.sock`** — escape vector
7. **Update container OS rutin** — sama seperti server biasa

## Cek Keamanan Container

```bash
# Cek capabilities container
lxc-attach -n nama-container -- capsh --print

# Cek syscall yang bisa dipanggil
lxc-attach -n nama-container -- strace -c sleep 1

# Cek mount
lxc-attach -n nama-container -- mount

# Cek namespace UID
lxc-attach -n nama-container -- cat /proc/self/uid_map
```

## Sumber

- [linuxcontainers.org/lxc/security](https://linuxcontainers.org/lxc/security/)
- [github.com/icta-tecaji/linux-containers — Security](https://github.com/icta-tecaji/linux-containers)

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/architecture]] — Arsitektur
- [[wiki/lxc/containers]] — Lifecycle container
- [[wiki/lxc/networking]] — Networking
- [[wiki/lxc/storage]] — Storage
- [[wiki/lxc/best-practices]] — Best practices
