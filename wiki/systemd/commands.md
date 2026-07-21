# Systemd Commands Cheatsheet

## systemctl — Service Management

```bash
# Start / Stop / Restart
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx             # Reload config (SIGHUP)
systemctl reload-or-restart nginx # Reload if possible, else restart

# Enable / Disable (boot)
systemctl enable nginx             # Start at boot
systemctl disable nginx            # Don't start at boot
systemctl enable --now nginx       # Enable + start now
systemctl disable --now nginx      # Disable + stop now

# Status
systemctl status nginx
systemctl is-active nginx
systemctl is-enabled nginx
systemctl is-failed nginx

# Mask / Unmask (prevent start)
systemctl mask nginx               # Symlink to /dev/null
systemctl unmask nginx

# List
systemctl list-units               # Active units
systemctl list-units --all         # All units
systemctl list-units --state=failed  # Failed only
systemctl list-unit-files          # All installed units
systemctl --failed                 # Failed units (shortcut)
systemctl --type=service           # Filter type
systemctl --type=service --state=running
```

## Unit File Management

```bash
# Edit unit (override)
systemctl edit nginx.service

# Edit full unit
systemctl edit --full nginx.service

# View unit file
systemctl cat nginx.service

# Show dependencies
systemctl list-dependencies nginx.service
systemctl list-dependencies --reverse nginx.service

# Reload systemd
systemctl daemon-reload

# Verify unit syntax
systemd-analyze verify /etc/systemd/system/myapp.service
```

## journalctl — Logging

```bash
journalctl -f                             # Follow
journalctl -b                             # Boot ini
journalctl -b -1                          # Boot sebelumnya
journalctl -u nginx                       # By unit
journalctl -u nginx -f                    # By unit + follow
journalctl -p err                         # Errors only
journalctl --since "1 hour ago"           # Time filter
journalctl -n 50                          # Last 50 lines
journalctl -o json-pretty                 # JSON output
journalctl --disk-usage                   # Disk usage
journalctl --vacuum-size=500M             # Shrink
```

## systemd-analyze — Performance & Debug

```bash
# Boot time
systemd-analyze

# Boot time detail per unit
systemd-analyze blame

# Critical chain (bottleneck)
systemd-analyze critical-chain

# Plot boot (SVG graph)
systemd-analyze plot > boot.svg

# Verify unit
systemd-analyze verify /etc/systemd/system/myapp.service

# Security analysis
systemd-analyze security nginx.service
```

## hostnamectl — Hostname

```bash
hostnamectl                        # Info
hostnamectl set-hostname newname   # Set hostname
hostnamectl set-icon-name server   # Set icon
```

## timedatectl — Date & Time

```bash
timedatectl                        # Status
timedatectl list-timezones         # List tz
timedatectl set-timezone Asia/Jakarta
timedatectl set-ntp true           # Enable NTP sync
```

## localectl — Locale

```bash
localectl                          # Current
localectl list-locales
localectl set-locale LANG=en_US.UTF-8
```

## loginctl — User Sessions

```bash
loginctl                           # Sessions
loginctl list-users
loginctl list-sessions
loginctl user-status username
loginctl terminate-session <id>
```

## systemctl — Power Management

```bash
systemctl reboot
systemctl poweroff
systemctl suspend
systemctl hibernate
systemctl hybrid-sleep
```

## Target (Runlevel)

```bash
systemctl get-default              # Current target
systemctl set-default multi-user.target  # Set default

# Common targets:
# multi-user.target  — Runlevel 3 (multi-user, no GUI)
# graphical.target   — Runlevel 5 (multi-user + GUI)
# rescue.target      — Runlevel 1 (single-user, rescue)
# emergency.target   — Emergency shell
# reboot.target      — Reboot
# poweroff.target    — Shutdown
```

## cgroup — Resource Info

```bash
# Cek cgroup unit
systemctl show nginx --property=ControlGroup

# Tree processes di service
systemd-cgls -u nginx.service

# Top by cgroup
systemd-cgtop
```

## Debug Service Startup

```bash
# Jalankan service dengan log verbose
SYSTEMD_LOG_LEVEL=debug systemctl start myapp.service

# Cek dependency gagal
systemctl list-dependencies --reverse myapp.service

# Cek environment
systemctl show myapp.service --property=Environment

# Cek status detail
systemctl status myapp.service -l --no-pager
```

## Config Files

```bash
# Journal config
/etc/systemd/journald.conf

# System config
/etc/systemd/system.conf

# Logind config
/etc/systemd/logind.conf

# Resolved config (DNS)
/etc/systemd/resolved.conf

# Timesyncd config (NTP)
/etc/systemd/timesyncd.conf
```

## Man Pages

```bash
man systemctl
man systemd.unit
man systemd.service
man systemd.timer
man systemd.exec
man journalctl
man journald.conf
man systemd-analyze
man systemd-system.conf
```

## Sumber

- `man systemctl`
- [freedesktop.org/wiki/Software/systemd](https://freedesktop.org/wiki/Software/systemd/)

## Lanjut Baca

- [[wiki/systemd/overview]] — Overview
- [[wiki/systemd/units]] — Unit types
- [[wiki/systemd/service-files]] — Custom service
- [[wiki/systemd/timers]] — Timer units
- [[wiki/systemd/journalctl]] — Logging
- [[wiki/systemd/boot]] — Boot process
