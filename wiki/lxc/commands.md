# LXC Commands Cheatsheet

## Lifecycle

```bash
# Create
lxc-create -t download -n <name> -- --dist ubuntu --release jammy --arch amd64

# Start (daemon)
lxc-start -n <name> -d

# Start (foreground + debug)
lxc-start -n <name> -F -l DEBUG -o /tmp/lxc.log

# Stop gracefully
lxc-stop -n <name>

# Force kill
lxc-stop -n <name> -k

# Reboot
lxc-stop -n <name> -r

# Destroy
lxc-destroy -n <name>

# Force destroy
lxc-destroy -n <name> -f
```

## Info & Status

```bash
# List semua container
lxc-ls

# List + detail (fancy)
lxc-ls -f

# List hanya running
lxc-ls --running

# List hanya stopped
lxc-ls --stopped

# Info detail
lxc-info -n <name>

# State only
lxc-info -n <name> -s

# PID only
lxc-info -n <name> -p

# IP only
lxc-info -n <name> -i

# Cek config
lxc-config -n <name>
```

## Attach & Execute

```bash
# Masuk container
lxc-attach -n <name>

# Execute command
lxc-attach -n <name> -- <command>

# Clear environment
lxc-attach -n <name> --clear-env -- /bin/bash

# As specific user
lxc-attach -n <name> -- su - <user>

# Attach console (Ctrl+A Q to exit)
lxc-console -n <name>
```

## Snapshot & Clone

```bash
# Snapshot
lxc-snapshot -n <name>

# List snapshots
lxc-snapshot -n <name> -L -C

# Restore snapshot
lxc-snapshot -n <name> -r snap0

# Delete snapshot
lxc-snapshot -n <name> -d snap0

# Clone
lxc-copy -n <source> -N <dest>
```

## Freeze / Unfreeze

```bash
# Freeze
lxc-freeze -n <name>

# Unfreeze
lxc-unfreeze -n <name>
```

## Resource Monitoring

```bash
# Monitor container events
lxc-monitor -n <name>

# Top within container
lxc-top

# Resource usage
lxc-info -n <name> -r
```

## Networking

```bash
# Check bridge
brctl show
ip addr show lxcbr0

# IP info dari container
lxc-info -n <name> -iH

# Debug network
lxc-attach -n <name> -- ip addr
lxc-attach -n <name> -- ip route
lxc-attach -n <name> -- cat /etc/resolv.conf
```

## Config Management

```bash
# View config
cat /var/lib/lxc/<name>/config

# Set autostart
echo "lxc.start.auto = 1" >> /var/lib/lxc/<name>/config

# Reload config (restart container supaya apply)
lxc-stop -n <name>
lxc-start -n <name> -d
```

## Templates

```bash
# List available templates local
ls /usr/share/lxc/templates/

# List available distros (online)
lxc-create -t download -n test -- --list

# Show help for specific template
lxc-create -t download -n test -- --help
```

## Backup & Restore

```bash
# Backup (tar)
tar czf /backup/<name>-$(date +%F).tar.gz -C /var/lib/lxc <name>/

# Restore
tar xzf /backup/<name>-date.tar.gz -C /var/lib/lxc/

# Checkpoint (CRIU)
lxc-checkpoint -n <name> -D /tmp/checkpoint -s
lxc-checkpoint -n <name> -D /tmp/checkpoint -r
```

## Troubleshooting

```bash
# Kernel check
lxc-checkconfig

# User namespace check
cat /proc/sys/kernel/unprivileged_userns_clone

# Debug start
lxc-start -n <name> -F -l DEBUG -o /tmp/lxc-debug.log

# Cek log container
cat /var/log/lxc/<name>.log

# Cek capability container
lxc-attach -n <name> -- capsh --print

# Cek UID mapping
lxc-attach -n <name> -- cat /proc/self/uid_map
```

## Config Snippets

### Minimal Config

```ini
lxc.uts.name = <name>
lxc.rootfs.path = dir:/var/lib/lxc/<name>/rootfs
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
```

### Privileged to Unprivileged

```ini
lxc.idmap = u 0 100000 65536
lxc.idmap = g 0 100000 65536
```

### Resource Limits

```ini
lxc.cgroup2.memory.max = 512M
lxc.cgroup2.cpu.max = 200000 100000
lxc.cgroup2.pids.max = 200
```

### Read-Only Rootfs

```ini
lxc.rootfs.options = ro
lxc.mount.entry = tmpfs tmp tmpfs defaults 0 0
```

## Man Pages

```bash
man lxc
man lxc-create
man lxc-start
man lxc-stop
man lxc-attach
man lxc.container.conf  # config reference lengkap
```

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/containers]] — Lifecycle container detail
- [[wiki/lxc/networking]] — Networking detail
- [[wiki/lxc/storage]] — Storage detail
- [[wiki/lxc/security]] — Security detail
