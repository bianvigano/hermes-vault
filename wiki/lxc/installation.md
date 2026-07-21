# Installasi LXC

## Ubuntu/Debian

```bash
# Install LXC dan dependencies
sudo apt update
sudo apt install lxc lxc-templates

# Verifikasi
lxc-checkconfig
```

Output `lxc-checkconfig` akan menunjukkan kernel feature yang enabled/disabled (namespace, cgroup, dll).

### Setup Unprivileged Containers (Rekomendasi)

Unprivileged container lebih aman — root di container = user biasa di host.

```bash
# Setup subuid/subgid mapping
echo "$USER:100000:65536" | sudo tee -a /etc/subuid
echo "$USER:100000:65536" | sudo tee -a /etc/subgid

# Buat config LXC user
mkdir -p ~/.config/lxc
echo "lxc.idmap = u 0 100000 65536" > ~/.config/lxc/default.conf
echo "lxc.idmap = g 0 100000 65536" >> ~/.config/lxc/default.conf
echo "lxc.net.0.type = veth" >> ~/.config/lxc/default.conf
echo "lxc.net.0.link = lxcbr0" >> ~/.config/lxc/default.conf
echo "lxc.net.0.flags = up" >> ~/.config/lxc/default.conf
```

### Setup LXC Networking (Bridge)

```bash
# Konfigurasi bridge default (lxcbr0) — via /etc/lxc/default.conf
sudo systemctl enable lxc-net
sudo systemctl start lxc-net
```

### Storage Default

Default storage di `/var/lib/lxc/` (unprivileged: `~/.local/share/lxc/`).

## Buat Container Pertama

```bash
# List template yang tersedia
ls /usr/share/lxc/templates/

# Download & buat container Ubuntu
lxc-create -t download -n mycontainer -- --dist ubuntu --release jammy --arch amd64

# Atau pakai template lokal
lxc-create -t ubuntu -n mycontainer
```

## Verifikasi

```bash
# Cek container sudah terdefinisi
lxc-ls

# Cek konfigurasi
lxc-config -n mycontainer

# Lihat file konfigurasi
cat /var/lib/lxc/mycontainer/config
# atau untuk unprivileged:
cat ~/.local/share/lxc/mycontainer/config
```

## Troubleshooting

```bash
# Debug mode saat start
lxc-start -n mycontainer -F -l DEBUG -o /tmp/lxc-debug.log

# Cek kernel support
lxc-checkconfig | grep -i miss

# Cek permission user namespaces
cat /proc/sys/kernel/unprivileged_userns_clone  # harus 1
```

## Sumber

- [linuxcontainers.org/lxc/introduction](https://linuxcontainers.org/lxc/introduction/)
- [dev.to/damilola_oladele/get-started-with-lxc](https://dev.to/damilola_oladele/get-started-with-lxc-explained-with-installation-guide-4efj)

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/containers]] — Lifecycle container
- [[wiki/lxc/networking]] — Setup networking
- [[wiki/lxc/security]] — Keamanan container
