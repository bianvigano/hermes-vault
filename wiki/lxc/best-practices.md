# LXC Best Practices

## 1. Selalu Pakai Unprivileged Containers

Ini praktik **terpenting**. Root di container unprivileged dipetakan ke UID non-root di host.

```bash
# Setup subuid/subgid
echo "$USER:100000:65536" | sudo tee -a /etc/subuid
echo "$USER:100000:65536" | sudo tee -a /etc/subgid
```

Jangan pernah pakai `sudo lxc-create` atau run container sebagai root kecuali benar-benar perlu.

## 2. Template Download, Bukan Template Lokal

Template `download` lebih cepat, selalu up-to-date, dan support lebih banyak distro.

```bash
# ✅ Baik
lxc-create -t download -n myct -- --dist ubuntu --release jammy --arch amd64

# ❌ Kurang baik (template lama, lambat bootstraping)
lxc-create -t ubuntu -n myct
```

## 3. Resource Limits Wajib

Jangan pernah bikin container tanpa batas resource:

```ini
lxc.cgroup2.memory.max = 512M
lxc.cgroup2.cpu.max = 200000 100000
lxc.cgroup2.pids.max = 200
```

Tanpa limit memory → 1 container bisa OOM host.

## 4. Buat Config Base / Profile

Biar konsisten, jangan copy-paste config manual setiap container.

```bash
# Base config
cat > ~/.config/lxc/default.conf << 'EOF'
lxc.idmap = u 0 100000 65536
lxc.idmap = g 0 100000 65536
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.cgroup2.memory.max = 512M
lxc.cgroup2.cpu.max = 200000 100000
lxc.cgroup2.pids.max = 200
EOF
```

## 5. Naming Convention

```
<env>-<service>-<number>
prod-web-01
dev-db-01
staging-app-02
```

## 6. Update OS di Dalam Container

Container bukan "immutable" kayak Docker image. OS di dalamnya tetap harus di-update.

```bash
lxc-attach -n <name> -- apt update && apt upgrade -y
```

Pertimbangkan cron job atau `unattended-upgrades`.

## 7. Logging

Pasang logging untuk semua container:

```ini
lxc.log.file = /var/log/lxc/<name>.log
lxc.log.level = INFO
```

Rotate log: `logrotate` config di `/etc/logrotate.d/lxc`.

## 8. Storage: Pilih yang Sesuai

| Kebutuhan | Backend |
|---|---|
| Simpel, development | `dir` |
| Snapshot, backup | `ZFS` |
| No extra setup, CoW | `Btrfs` |
| Thin provisioning | `LVM` |

Jangan taruh rootfs container di `/tmp` atau filesystem sementara.

## 9. Backup Rutin

Minimal backup config + data:

```bash
#!/bin/bash
# /usr/local/bin/lxc-backup.sh
BACKUP_DIR=/backup/lxc
DATE=$(date +%Y%m%d)
for ct in $(lxc-ls -1); do
    tar czf "$BACKUP_DIR/${ct}-${DATE}.tar.gz" -C /var/lib/lxc "$ct/"
done
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
```

Jalankan via cron.

## 10. Monitoring

Pantau resource container:

```bash
# Cek dari host
lxc-info -n <name> -r

# Top container
lxc-top

# Cek kernel log
dmesg | grep lxc
```

## 11. Firewall

Jangan lupa firewall untuk bridge:

```bash
# Allow dari container ke luar
sudo iptables -A FORWARD -i lxcbr0 -j ACCEPT

# Allow established
sudo iptables -A FORWARD -o lxcbr0 -m state --state ESTABLISHED,RELATED -j ACCEPT
```

## 12. Jangan Mount /var/run/docker.sock

Mount `docker.sock` ke container LXC = container itu bisa kontrol Docker host. Escape vector besar.

Kalau butuh Docker di dalam LXC → install Docker daemon dalam container, bukan mount socket host.

## 13. Test Recovery

Rutin test backup:

```bash
# Restore ke nama temporary
lxc-copy -n myct-backup --newname myct-restore-test
lxc-start -n myct-restore-test -d
lxc-attach -n myct-restore-test -- systemctl status
lxc-destroy -n myct-restore-test
```

## 14. Debugging

Selalu simpan log saat ada masalah:

```bash
# Log ke file
lxc-start -n <name> -F -l DEBUG -o /tmp/lxc-debug.log

# Cek config yang sebenarnya berlaku
lxc-config -n <name>
```

## Ringkasan Checklist

- [ ] Unprivileged containers
- [ ] Resource limits (CPU, RAM, PIDs)
- [ ] Capability whitelist (drop all, add needed)
- [ ] Backup rutin + test restore
- [ ] Update OS container rutin
- [ ] Logging + logrotate
- [ ] Firewall rules
- [ ] No sensitive host mounts

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/security]] — Security detail
- [[wiki/lxc/storage]] — Storage backend
- [[wiki/lxc/commands]] — Cheatsheet
