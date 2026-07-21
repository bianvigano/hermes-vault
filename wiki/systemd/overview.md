# Systemd Overview

Systemd adalah **init system dan service manager** untuk Linux. PID 1 — proses pertama yang dijalankan kernel saat boot. Menggantikan SysV init dan Upstart di mayoritas distro modern (Ubuntu 15.04+, Debian 8+, Fedora 15+, RHEL 7+, Arch 2012+).

## Apa Itu Systemd?

Bukan cuma init system. Systemd adalah **suite tools** untuk mengelola:
- **Services** — start/stop/reload service (daemon)
- **Sockets** — socket activation
- **Timers** — cron replacement
- **Mounts** — auto-mount filesystem
- **Logs** — journald (centralized logging)
- **Network** — networkd (network configuration)
- **Boot** — parallel boot, dependency-based start

## Kenapa Systemd?

| Sebelum Systemd | Dengan Systemd |
|---|---|
| Boot lambat (serial) | Parallel boot via dependency graph |
| Bash script service management | Declarative unit files |
| Log di file teks terpisah | journald — binary log, queryable |
| cron syntax cryptic | Timer units — deklaratif |
| Init script custom per distro | Unit files standar di semua distro |
| No socket activation | Service start saat socket kena traffic |

## Konsep Inti

- **Unit** — resource yang dikelola systemd (service, socket, timer, dll.)
- **Unit file** — file konfigurasi deklaratif (`*.service`, `*.socket`, `*.timer`)
- **Target** — grouping unit (mirip SysV runlevel)
- **PID 1** — systemd berjalan sebagai proses pertama
- **journald** — logging daemon systemd
- **D-Bus** — IPC yang dipakai systemd untuk komunikasi
- **cgroups** — isolasi resource per service (otomatis)

## Systemd vs SysV Init vs OpenRC

| | Systemd | SysV Init | OpenRC |
|---|---|---|---|
| Boot | Parallel | Serial | Parallel |
| Config | Unit files (.ini) | Bash script | Shell script |
| Logging | journald | syslog | syslog |
| Socket activation | ✅ | ❌ | ❌ |
| cgroups integrated | ✅ | ❌ | Opsional |
| Dependency | Declarative | Manual ordering | Declarative |
| Distro | Modern semua | Legacy | Alpine, Gentoo |

## Komponen Systemd

- **systemd** — PID 1, init system
- **journald** — centralized logging (`journalctl`)
- **networkd** — network management
- **resolved** — DNS resolver
- **timedated** — date/time sync
- **logind** — session/login management
- **udevd** — device management

## Lisensi

LGPLv2.1+ — dikembangkan oleh Lennart Poettering, Kay Sievers, dan kontributor.

## Sumber

- [freedesktop.org/wiki/Software/systemd](https://freedesktop.org/wiki/Software/systemd/)
- `man systemd`
- [digitalocean.com — Understanding Systemd Units](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)

## Lanjut Baca

- [[wiki/systemd/units]] — Unit types: service, socket, timer, mount, target
- [[wiki/systemd/service-files]] — Bikin custom service
- [[wiki/systemd/timers]] — Cron replacement
- [[wiki/systemd/journalctl]] — Query log
- [[wiki/systemd/commands]] — Cheatsheet
- [[wiki/systemd/boot]] — Boot process
