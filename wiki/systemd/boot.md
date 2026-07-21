# Systemd Boot Process

Systemd sebagai PID 1 mengontrol seluruh boot process. Ini flow dari kernel sampai user login.

## Boot Flow

```
Firmware (UEFI/BIOS)
  └─ Bootloader (GRUB/systemd-boot)
      └─ Kernel Linux
          └─ systemd (PID 1)
              ├─ default.target
              │   ├─ sysinit.target
              │   │   ├─ mount filesystem
              │   │   ├─ udev (device detection)
              │   │   ├─ swap
              │   │   └─ journald
              │   ├─ basic.target
              │   │   ├─ sockets.target
              │   │   ├─ timers.target
              │   │   └─ paths.target
              │   ├─ multi-user.target
              │   │   ├─ network.target
              │   │   ├─ services (sshd, nginx, postgresql)
              │   │   └─ getty (TTY login)
              │   └─ graphical.target (optional)
              │       └─ Display Manager (GDM, SDDM)
```

## Target Boot

| Target | Purpose | Equivalent Runlevel |
|---|---|---|
| `emergency.target` | Emergency shell (root, minimal) | - |
| `rescue.target` | Single-user rescue | 1 |
| `multi-user.target` | Multi-user, no GUI | 3 |
| `graphical.target` | Multi-user + GUI | 5 |
| `reboot.target` | Reboot | 6 |
| `poweroff.target` | Shutdown | 0 |

## Lihat Boot Info

```bash
# Total boot time
systemd-analyze

# Contoh output: Startup finished in 2.345s (kernel) + 8.912s (userspace) = 11.257s

# Per-unit boot time (sorted slowest first)
systemd-analyze blame

# Critical chain (bottleneck)
systemd-analyze critical-chain

# Plot boot SVG
systemd-analyze plot > boot.svg

# List kernel command line
systemd-analyze cat-config

# Cek security unit
systemd-analyze security sshd.service
```

## Modify Boot Target

```bash
# Default boot target
systemctl get-default
systemctl set-default multi-user.target
systemctl set-default graphical.target

# Boot to specific target (one-time via GRUB)
# Tambah di kernel cmdline: systemd.unit=rescue.target
# Atau: systemd.unit=emergency.target
```

## Kernel Command Line

Lihat: `cat /proc/cmdline`

Parameter systemd penting:
```
quiet                        # Less verbose boot
systemd.unit=rescue.target   # Boot ke rescue
systemd.show_status=yes      # Show service status
systemd.log_level=debug      # Debug logging
systemd.journald.forward_to_console
```

## Parallel Boot

Systemd boot secara **parallel** — dependency graph, bukan urutan manual. Unit yang gak saling tergantung start bareng.

```bash
# Lihat service yang delayed
systemd-analyze blame | head -10

# Lihat dependency problem
systemd-analyze critical-chain
```

## Debug Slow Boot

```bash
# Unit paling lambat
systemd-analyze blame

# Cek timestamp tiap unit
systemd-analyze plot > boot.svg   # Buka di browser

# Log boot
journalctl -b

# Log boot sebelumnya
journalctl -b -1

# Cek unit yang failed saat boot
systemctl --failed
systemctl list-units --state=failed
```

## systemd-boot (Bootloader)

Systemd punya bootloader sendiri: `systemd-boot` (sebelumnya gummiboot). Simpel untuk UEFI.

```bash
# Install
bootctl install

# Status
bootctl status

# Config entries di /boot/loader/entries/
# Default config di /boot/loader/loader.conf
```

Contoh entry:
```
title   Arch Linux
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options root=/dev/sda2 rw quiet
```

## Emergency Recovery

**Rescue mode:**
```bash
# Tambah di GRUB cmdline:
systemd.unit=rescue.target

# Atau via systemctl
systemctl rescue
```

**Emergency shell** (root shell minimal tanpa mount apapun):
```bash
systemctl emergency
# ATAU di GRUB: systemd.unit=emergency.target
```

## Shutdown Process

```
systemctl poweroff
  └─ systemd stop semua service (reverse dependency order)
      └─ kill semua proses
          └─ unmount filesystem
              └─ kernel power off
```

## Sumber

- `man bootup` — diagram boot
- `man systemd.special` — special units
- [freedesktop.org/wiki/Software/systemd](https://freedesktop.org/wiki/Software/systemd/)

## Lanjut Baca

- [[wiki/systemd/overview]] — Overview
- [[wiki/systemd/units]] — Unit types
- [[wiki/systemd/service-files]] — Custom service
- [[wiki/systemd/commands]] — Cheatsheet
