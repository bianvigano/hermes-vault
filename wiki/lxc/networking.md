# LXC Networking

## Tipe Network Device

| Tipe | Deskripsi | Use Case |
|---|---|---|
| **veth** (default) | Virtual Ethernet pair — satu di host, satu di container | Bridge ke lxcbr0, komunikasi host↔container |
| **macvlan** | Container dapat MAC address sendiri, langsung di LAN | Container butuh IP dari router fisik |
| **ipvlan** | Mirip macvlan, sharing MAC host tapi beda IP | Hosting provider yang batasi MAC per port |
| **phys** | Pass-through physical NIC ke container | Butuh dedicated NIC untuk container |
| **vlan** | VLAN tagged interface | Isolasi network per VLAN |

## Bridge Networking (Default)

Arsitektur: container → veth pair → bridge lxcbr0 → NAT ke eth0 host

```ini
# Config container
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx
lxc.net.0.ipv4 = 10.0.3.50/24
lxc.net.0.ipv4.gateway = 10.0.3.1
```

Setup bridge di host:

```bash
# Enable lxc-net service (auto-create lxcbr0 + dnsmasq)
sudo systemctl enable --now lxc-net

# Config: /etc/default/lxc-net
# USE_LXC_BRIDGE="true"
# LXC_BRIDGE="lxcbr0"
# LXC_ADDR="10.0.3.1"
# LXC_NETMASK="255.255.255.0"
# LXC_NETWORK="10.0.3.0/24"
# LXC_DHCP_RANGE="10.0.3.2,10.0.3.254"
# LXC_DHCP_MAX="253"
```

## Macvlan — Container Punya IP Sendiri

Container langsung dapat IP dari subnet router fisik.

```ini
lxc.net.0.type = macvlan
lxc.net.0.link = eth0
lxc.net.0.macvlan.mode = bridge
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:41:11:65
```

Mode macvlan:

| Mode | Behavior |
|---|---|
| `bridge` | Semua container + host bisa komunikasi |
| `vepa` | Traffic antar container lewat switch eksternal |
| `private` | Container tidak bisa komunikasi satu sama lain |
| `passthru` | Dedicated — 1 container per parent interface |

## Multiple Network Interfaces

```ini
# Management (bridge NAT)
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.ipv4 = 10.0.3.100/24

# Data (macvlan — direct LAN)
lxc.net.1.type = macvlan
lxc.net.1.link = eth0
lxc.net.1.macvlan.mode = bridge
lxc.net.1.flags = up
lxc.net.1.hwaddr = 00:16:3e:11:22:33
```

## Set IP Static

```bash
# Di container config
lxc.net.0.ipv4 = 192.168.1.100/24
lxc.net.0.ipv4.gateway = 192.168.1.1

# Set nameserver
# Di host: /etc/resolvconf/resolv.conf.d/base
# Atau di container config:
lxc.mount.entry = /etc/resolv.conf etc/resolv.conf none bind,ro 0 0
```

## Port Forwarding (NAT)

Untuk akses service container dari luar via host:

```bash
# Via iptables
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to 10.0.3.50:80
sudo iptables -A FORWARD -p tcp -d 10.0.3.50 --dport 80 -j ACCEPT

# Persistent: /etc/iptables/rules.v4 (iptables-persistent)
```

## Unprivileged Container Network

User namespace container butuh setuid helper `lxc-user-nic`:

```bash
# Di /etc/lxc/lxc-usernet
# Format: <user> <bridge> <count>
bian    lxcbr0  10
```

## Troubleshooting

```bash
# Cek bridge
ip addr show lxcbr0
brctl show lxcbr0

# Cek iptables NAT
sudo iptables -t nat -L POSTROUTING

# Debug container network
lxc-attach -n nama-container -- ip addr
lxc-attach -n nama-container -- ip route

# Test koneksi
lxc-attach -n nama-container -- ping 8.8.8.8
```

## Sumber

- [deepwiki.com/lxc/lxc/5-networking](https://deepwiki.com/lxc/lxc/5-networking)
- [wiki.gentoo.org/wiki/LXC/Network_examples](https://wiki.gentoo.org/wiki/LXC/Network_examples)
- [flockport.com/lxc-macvlan-networking](https://archives.flockport.com/lxc-macvlan-networking/)

## Lanjut Baca

- [[wiki/lxc/overview]] — Overview LXC
- [[wiki/lxc/containers]] — Lifecycle container
- [[wiki/lxc/storage]] — Storage backend
- [[wiki/lxc/security]] — Keamanan
