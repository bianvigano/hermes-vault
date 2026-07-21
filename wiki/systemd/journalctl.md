# journalctl — Systemd Logging

journalctl = query tool untuk **journald** (logging daemon systemd). Semua log service terpusat di binary journal, bukan file teks terpisah.

## Kenapa journalctl?

| Tanpa journald | Dengan journald |
|---|---|
| Log di `/var/log/syslog` — plaintext, no query | Binary log, queryable |
| Gak tau log dari service mana | `-u <unit>` filter langsung |
| Cari error manual grep | `-p err` filter by severity |
| Log hilang pas reboot | Persistent storage option |
| Timezone campur aduk | UTC + local time display |

## Basic Commands

```bash
# Semua log (newest first)
journalctl

# Semua log (oldest first)
journalctl -r

# Follow (tail -f mode)
journalctl -f

# Log dari boot ini
journalctl -b

# Log dari boot sebelumnya
journalctl -b -1

# List boot IDs
journalctl --list-boots

# N recent lines
journalctl -n 50

# No pager, full output
journalctl --no-pager
```

## Filter by Unit (Service)

```bash
# Log dari service spesifik
journalctl -u nginx.service

# Follow log service
journalctl -u nginx.service -f

# Log dari service + boot ini
journalctl -u nginx.service -b

# Multiple units
journalctl -u nginx.service -u postgresql.service

# Log dari user unit
journalctl --user -u myapp.service
```

## Filter by Time

```bash
# Sejak jam tertentu
journalctl --since "2026-07-21 08:00:00"

# Sampai jam tertentu
journalctl --until "2026-07-21 18:00:00"

# Range
journalctl --since "1 hour ago"
journalctl --since "yesterday"
journalctl --since "2026-07-20" --until "2026-07-21"

# Kombinasi filter
journalctl -u nginx.service --since "2 hours ago"
```

## Filter by Priority/Severity

```bash
# Hanya error
journalctl -p err

# Error + worse
journalctl -p err..emerg

# Level dari yang paling rendah ke tertinggi:
# 0: emerg   — System unusable
# 1: alert   — Immediate action
# 2: crit    — Critical
# 3: err     — Error
# 4: warning — Warning
# 5: notice  — Normal but significant
# 6: info    — Informational
# 7: debug   — Debug
```

## Filter by Kernel Messages

```bash
# Kernel messages only
journalctl -k

# Sama dengan
journalctl -b -k
```

## Filter by Executable/Binary

```bash
# Log dari binary spesifik
journalctl /usr/bin/sshd

# Log dari PID
journalctl _PID=1234

# Log dari UID
journalctl _UID=1000

# Log dari GID
journalctl _GID=1000
```

## Output Format

```bash
# Default (cat)
journalctl -o cat

# Short (syslog style)
journalctl -o short

# Short with timezone
journalctl -o short-iso

# Short with precise timestamp
journalctl -o short-precise

# JSON
journalctl -o json

# JSON pretty
journalctl -o json-pretty

# Verbose (all fields)
journalctl -o verbose

# Export binary
journalctl -o export
```

## Disk Usage & Maintenance

```bash
# Cek disk usage journal
journalctl --disk-usage

# Vacuum: retain last 2 days
sudo journalctl --vacuum-time=2d

# Vacuum: max 500MB
sudo journalctl --vacuum-size=500M

# Vacuum: max 1000 files
sudo journalctl --vacuum-files=1000

# Rotate (sekarang)
sudo journalctl --rotate
```

## Persistent Storage

Default: journal di `/run/log/journal/` (volatile — hilang pas reboot).

```bash
# Enable persistent storage
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald

# Config: /etc/systemd/journald.conf
# Storage=persistent
# SystemMaxUse=500M
# MaxRetentionSec=2week
```

## Remote Logging

```bash
# Upload journal ke URL
sudo journalctl --upload=http://log-server:19532
```

## Kombinasi Berguna

```bash
# Error dari nginx dalam 1 jam terakhir
journalctl -u nginx.service -p err --since "1 hour ago"

# Semua error + warning dari boot ini
journalctl -b -p warning

# Log kernel boot
journalctl -b -k

# Semua service yang failed
systemctl --failed | tail +2 | awk '{print $2}' | while read u; do journalctl -u "$u" --since "1 hour ago"; done

# Cek restart service
journalctl -u nginx.service | grep "Stopping\|Starting"
```

## Sumber

- `man journalctl`
- `man journald.conf`
- [wiki.archlinux.org/title/Systemd/Journal](https://wiki.archlinux.org/title/Systemd/Journal)

## Lanjut Baca

- [[wiki/systemd/overview]] — Overview systemd
- [[wiki/systemd/service-files]] — Custom service
- [[wiki/systemd/timers]] — Timer units
- [[wiki/systemd/commands]] — Cheatsheet
