# Systemd Timers

Timer = cron replacement di systemd. Lebih powerful, declarative, dan integrated dengan logging.

## Kenapa Timer?

| Cron | Systemd Timer |
|---|---|
| Syntax cryptic (`*/5 * * * *`) | `OnCalendar=*-*-* *:00/5` atau `OnUnitActiveSec=5min` |
| Log di email/syslog | journalctl otomatis |
| Gak bisa retry | `Persistent=true` catch-up missed runs |
| Gak bisa random delay | `RandomizedDelaySec=` |
| No dependency | `Requires=`, `After=` unit lain |
| Manual anacron | Persistent otomatis |

## Jenis Timer

### 1. Realtime (OnCalendar)

```ini
[Timer]
OnCalendar=*-*-* 02:30:00
OnCalendar=daily
OnCalendar=Mon,Fri 18:00
Persistent=true
```

Format: `DayOfWeek Year-Month-Day Hour:Minute:Second`

Calendar shortcuts: `hourly`, `daily`, `weekly`, `monthly`, `yearly`

### 2. Monotonic (Relative)

```ini
[Timer]
OnActiveSec=1h
OnUnitActiveSec=30min
OnBootSec=5min
```

Jalan relatif dari event spesifik, bukan jam dinding.

## Structure: Service + Timer

Timer selalu paired dengan service dengan nama SAMA.

```
# /etc/systemd/system/backup.service
[Unit]
Description=Daily Backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

```
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily at 2:30 AM
Requires=backup.service

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

## Calendar Syntax

```
OnCalendar=DayOfWeek Year-Month-Day Hour:Minute:Second
               *           *            *-*-*     02:00
               *         2026           *-*-*     00:00
            Mon,Fri         *           *-*-*     09:00
               *           *            5-*       00:00
```

| Shortcut | Ekuivalen |
|---|---|
| `hourly` | `*-*-* *:00:00` |
| `daily` | `*-*-* 00:00:00` |
| `weekly` | `Mon *-*-* 00:00:00` |
| `monthly` | `*-*-01 00:00:00` |
| `yearly` | `*-01-01 00:00:00` |

## Timer Options

```ini
[Timer]
# Calendar trigger
OnCalendar=*-*-* 02:00

# Relative trigger
OnBootSec=5min
OnActiveSec=1h

# Catch-up missed runs
Persistent=true

# Random delay (± detik)
RandomizedDelaySec=300

# Accuracy (default: 1min)
AccuracySec=1s

# Wake system from sleep
WakeSystem=false

# Run after unit X
Unit=my-service.service
```

## Timer Commands

```bash
# Enable timer
systemctl enable backup.timer
systemctl start backup.timer

# List all timers
systemctl list-timers
systemctl list-timers --all

# Cek next run
systemctl status backup.timer

# Lihat log dari timer trigger
journalctl -u backup.service

# Test manual trigger
systemctl start backup.service

# Cek timer config
systemctl cat backup.timer
```

## Contoh: Maintenance Timer

```ini
# cleanup.service
[Unit]
Description=Weekly Cleanup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/cleanup.sh
```

```ini
# cleanup.timer
[Unit]
Description=Weekly Cleanup Timer

[Timer]
OnCalendar=Sun 04:00
RandomizedDelaySec=600
Persistent=true

[Install]
WantedBy=timers.target
```

## Contoh: Every 5 Minutes

```ini
[Timer]
OnCalendar=*-*-* *:00/5
# atau
OnUnitActiveSec=5min
```

## Persistent Mode

`Persistent=true` — kalau timer missed (server mati), dijalankan langsung saat boot berikutnya. Ini = built-in anacron.

## Sumber

- `man systemd.timer`
- [wiki.archlinux.org/title/Systemd/Timers](https://wiki.archlinux.org/title/Systemd/Timers)

## Lanjut Baca

- [[wiki/systemd/overview]] — Overview systemd
- [[wiki/systemd/units]] — Unit types
- [[wiki/systemd/service-files]] — Custom service
- [[wiki/systemd/journalctl]] — Logging
- [[wiki/systemd/commands]] — Cheatsheet
