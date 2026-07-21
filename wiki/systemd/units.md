# Systemd Units

Unit adalah **resource yang dikelola systemd**. Semua yang dihandle systemd — service, socket, timer, mount, device — direpresentasikan sebagai unit.

## Tipe Unit

| Unit Type | Extension | Deskripsi |
|---|---|---|
| **Service** | `.service` | Proses/daemon (nginx, sshd, docker) |
| **Socket** | `.socket` | IPC/network socket (socket activation) |
| **Timer** | `.timer` | Scheduled task (cron replacement) |
| **Mount** | `.mount` | Mount point filesystem |
| **Automount** | `.automount` | Auto-mount on access |
| **Target** | `.target` | Grouping unit (mirip runlevel) |
| **Path** | `.path` | Watch path for file changes |
| **Device** | `.device` | Hardware device |
| **Slice** | `.slice` | Resource grouping (cgroup hierarchy) |
| **Scope** | `.scope` | External process grouping |
| **Snapshot** | `.snapshot` | System state snapshot |

## Lokasi Unit Files

| Path | Purpose | Priority |
|---|---|---|
| `/etc/systemd/system/` | Admin custom units | **HIGHEST** |
| `/run/systemd/system/` | Runtime units | Medium |
| `/usr/lib/systemd/system/` | Package default units | Lowest |

> Edit unit: jangan edit di `/usr/lib/`. Copy ke `/etc/` dulu dengan `systemctl edit --full <unit>`.

## Anatomi Unit File

```ini
[Unit]
Description=My Custom Service
Documentation=https://example.com/docs
After=network.target
Wants=postgresql.service
Requires=redis.service

[Service]
Type=simple
ExecStart=/usr/bin/myapp --config /etc/myapp/config.yml
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
User=myapp
Group=myapp
Environment="DATABASE_URL=postgres://..."
EnvironmentFile=/etc/myapp/env

[Install]
WantedBy=multi-user.target
```

### [Unit] Section

| Directive | Fungsi |
|---|---|
| `Description=` | Human-readable description |
| `After=` | Start setelah unit ini |
| `Before=` | Start sebelum unit ini |
| `Requires=` | Unit ini HARUS ada (kalau mati, unit mati) |
| `Wants=` | Unit direkomendasikan (kalau mati, unit lanjut) |
| `Conflicts=` | Tidak bisa jalan bareng unit ini |

### [Service] Section

| Directive | Fungsi |
|---|---|
| `Type=` | simple / forking / oneshot / notify / dbus / idle |
| `ExecStart=` | Command untuk start |
| `ExecStop=` | Command untuk stop |
| `ExecReload=` | Command untuk reload |
| `Restart=` | no / on-success / on-failure / on-abnormal / always |
| `RestartSec=` | Delay sebelum restart |
| `User=` / `Group=` | Run as user ini |
| `Environment=` | Set env variable |
| `EnvironmentFile=` | Load env dari file |

### [Install] Section

| Directive | Fungsi |
|---|---|
| `WantedBy=` | Target yang membutuhkan unit ini |
| `RequiredBy=` | Target yang wajib punya unit ini |
| `Alias=` | Nama alternatif |

## Service Type

| Type | Behavior |
|---|---|
| **simple** (default) | ExecStart = proses utama. Systemd anggap service langsung running. |
| **forking** | ExecStart fork child, parent exit. Child = service. Perlu `PIDFile=`. |
| **oneshot** | ExecStart selesai → service considered started. Pakai `RemainAfterExit=yes`. |
| **notify** | Service kirim `sd_notify()` signal ke systemd saat siap. |
| **dbus** | Service register D-Bus name. Siap saat name acquired. |
| **idle** | Tunda start sampai semua job selesai. |

## Dependency: Wants vs Requires

```ini
# Wants: unit start TANPA dia, tetap jalan (soft dependency)
Wants=postgresql.service

# Requires: unit start TANPA dia → GAGAL (hard dependency)
Requires=redis.service

# After: ordering doang, bukan dependency
After=network.target
```

## Override Unit

```bash
# Edit unit (buat override file di /etc/systemd/system/<unit>.d/)
systemctl edit nginx.service

# Edit full unit (copy ke /etc/systemd/system/)
systemctl edit --full nginx.service

# Lihat file yang berlaku
systemctl cat nginx.service
```

## Unit Status

```bash
# Status unit
systemctl status nginx.service

# List semua unit
systemctl list-units

# List semua unit (termasuk inactive)
systemctl list-units --all

# List unit yang failed
systemctl --failed

# Cek apakah unit enabled
systemctl is-enabled nginx.service
systemctl is-active nginx.service
```

## Sumber

- `man systemd.unit`
- `man systemd.service`
- [digitalocean.com — Understanding Systemd Units](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)

## Lanjut Baca

- [[wiki/systemd/overview]] — Overview systemd
- [[wiki/systemd/service-files]] — Custom service detail
- [[wiki/systemd/timers]] — Timer units
- [[wiki/systemd/commands]] — Cheatsheet
- [[wiki/systemd/journalctl]] — Logging
