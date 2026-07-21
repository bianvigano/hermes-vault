# LXC Storage

## Storage Backend

| Backend | Fitur | Kelebihan | Kekurangan |
|---|---|---|---|
| **dir** | Directory biasa | Paling simpel, no dependency | Lambat, no snapshot, no quota |
| **ZFS** | Dataset, snapshot, clone, send/receive | Snapshot instan, dedup, compression | Butuh kernel module, RAM hungry |
| **Btrfs** | Subvolume, snapshot, send/receive | Built-in kernel, CoW, compression | Kurang mature dari ZFS |
| **LVM** | Logical volume per container | Thin provisioning, snapshot | No dedup, no compression built-in |
| **Ceph** | Distributed storage | Cluster, HA, scale-out | Kompleks, butuh 3+ node |
| **loop** | File loopback + filesystem (ext4/xfs) | Portable, no partition needed | Performance overhead |

## Directory Backend (Default, Paling Simpel)

Storage di path filesystem biasa.

```bash
# Buat container dengan dir backend
lxc-create -t download -n myct -B dir --dir /path/to/storage

# Atau default ke /var/lib/lxc/
lxc-create -t download -n myct
```

Rootfs: `/var/lib/lxc/myct/rootfs/`

Pro: Zero setup, jalan di semua distro
Con: No snapshot, no quota

## ZFS Backend

```bash
# Setup ZFS pool
sudo zpool create lxcpool /dev/sdb

# Buat dataset
sudo zfs create lxcpool/lxc

# Buat container di ZFS
lxc-create -t download -n myct -B zfs --zfsroot=lxcpool/lxc

# Snapshot
zfs snapshot lxcpool/lxc/myct@before-upgrade

# Rollback
zfs rollback lxcpool/lxc/myct@before-upgrade
```

Keunggulan: Snapshot instan, send/receive untuk backup/migrasi, compression (`zfs set compression=lz4 lxcpool/lxc`).

## Btrfs Backend

```bash
# Buat Btrfs filesystem
sudo mkfs.btrfs /dev/sdb

# Mount
sudo mount /dev/sdb /var/lib/lxc

# Buat container di Btrfs
lxc-create -t download -n myct -B btrfs

# Snapshot
btrfs subvolume snapshot /var/lib/lxc/myct/rootfs /var/lib/lxc/myct-snap
```

## LVM Backend

```bash
# Buat volume group
sudo vgcreate lxcvg /dev/sdb

# Buat thin pool
sudo lvcreate -L 50G -T lxcvg/thinpool

# Buat container di LVM
lxc-create -t download -n myct -B lvm --vgname lxcvg --thinpool thinpool

# Snapshot LVM
sudo lvcreate -s -n myct-snap lxcvg/myct
```

## Migrasi / Backup Container

### Whole Container Backup

```bash
# Tar rootfs + config
cd /var/lib/lxc
sudo tar czf myct-backup.tar.gz myct/

# Restore
sudo tar xzf myct-backup.tar.gz -C /var/lib/lxc/
```

### ZFS Send / Receive

```bash
# Snapshot dulu
sudo zfs snapshot lxcpool/lxc/myct@backup

# Kirim ke file
sudo zfs send lxcpool/lxc/myct@backup > myct.zfs

# Restore di host lain
sudo zfs receive lxcpool/lxc/myct < myct.zfs
```

### Live Migration (dengan CRIU)

Butuh CRIU (Checkpoint/Restore In Userspace):

```bash
# Checkpoint
lxc-checkpoint -n myct -D /tmp/myct-checkpoint -s

# Restore
lxc-checkpoint -n myct -D /tmp/myct-checkpoint -r
```

## Mount Bind

Share direktori host ke container:

```ini
# Di config container
lxc.mount.entry = /host/path container/path none bind 0 0
lxc.mount.entry = /data/apps var/www none bind,rw 0 0
```

## Quota / Limit

```bash
# ZFS quota
zfs set quota=10G lxcpool/lxc/myct

# LVM thin size
lvcreate -V 10G -T lxcvg/thinpool -n myct

# Cgroup blkio
lxc.cgroup2.io.max = "8:0 rbps=10485760 wbps=10485760"
```

## Sumber

- [linuxcontainers.org](https://linuxcontainers.org/)
- [ubuntu.com/lxd/docs — storage](https://documentation.ubuntu.com/lxd/)

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/containers]] — Lifecycle container
- [[wiki/lxc/networking]] — Networking
- [[wiki/lxc/commands]] — Cheatsheet
- [[wiki/lxc/best-practices]] — Best practices
