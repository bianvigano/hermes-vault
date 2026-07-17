# Linux & DevOps — Server Security & SSH

Referensi keamanan server Linux, konfigurasi SSH, firewall, dan monitoring.

---

## SSH Hardening (Anti Brute Force)

### Ganti ke SSH Key (nonaktifkan password)

```bash
ssh-keygen -t ed25519
ssh-copy-id user@server
```

Edit `/etc/ssh/sshd_config`:
```
PasswordAuthentication no
Port 2222              # ganti dari default 22
MaxStartups 10:30:60   # limit koneksi simultan
```

Restart:
```bash
sudo systemctl restart ssh
```

### Fail2Ban — Auto Block IP Mencurigakan

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

Konfigurasi `/etc/fail2ban/jail.local`:
```ini
[sshd]
enabled = true
port = ssh
maxretry = 5
bantime = 3600
```

Cek status:
```bash
sudo fail2ban-client status sshd
```

Unban IP:
```bash
sudo fail2ban-client set sshd unbanip IP_ADDRESS
```

### Fail2Ban → Discord Webhook (Alert Real-Time)

Script `/etc/fail2ban/discord_notify.sh`:
```bash
#!/bin/bash
WEBHOOK_URL="https://discord.com/api/webhooks/xxxxx/yyyyy"
IP="$1"
JAIL="$2" 
ACTION="$3"
TIME=$(date "+%Y-%m-%d %H:%M:%S")
SERVER=$(hostname)

# GeoIP + Reverse DNS
RDNS=$(dig +short -x $IP | sed 's/\.$//')
COUNTRY=$(geoiplookup $IP | awk -F: '{print $2}' | xargs)
ATTEMPTS=$(grep $IP /var/log/auth.log | wc -l)

# Embed JSON
JSON=$(jq -n \
  --arg server "$SERVER" --arg ip "$IP" --arg jail "$JAIL" \
  --arg action "$ACTION" --arg time "$TIME" --arg country "$COUNTRY" \
  --arg rdns "$RDNS" --arg attempts "$ATTEMPTS" \
'{
  "embeds": [{
    "title": "🚨 Fail2Ban Security Alert",
    "color": 15158332,
    "fields": [
      {"name":"Server","value":$server,"inline":true},
      {"name":"IP","value":$ip,"inline":true},
      {"name":"Country","value":$country,"inline":true},
      {"name":"Jail","value":$jail,"inline":true},
      {"name":"Attempts","value":$attempts,"inline":true},
      {"name":"Time","value":$time,"inline":false}
    ]
  }]
}')

curl -H "Content-Type: application/json" -X POST -d "$JSON" $WEBHOOK_URL
```

Action `/etc/fail2ban/action.d/discord.conf`:
```ini
[Definition]
actionban = /etc/fail2ban/discord_notify.sh <ip> <name> "BANNED"
actionunban = /etc/fail2ban/discord_notify.sh <ip> <name> "UNBANNED"
```

## UFW Firewall

```bash
sudo ufw allow 25565/tcp       # Minecraft
sudo ufw allow 56744/tcp       # SSH custom port
sudo ufw allow port 25569 proto tcp   # explicit syntax
sudo ufw enable
sudo ufw status numbered
sudo ufw reload
```

**Pitfall:** `ufw allow 25569 tcp` → ERROR, harus `ufw allow 25569/tcp`.

## SSH Troubleshooting — "Connection closed by remote host"

Penyebab `kex_exchange_identification: Connection closed by remote host`:

1. **SSH tidak berjalan** — `sudo systemctl status ssh`
2. **Port salah** — `sudo ss -tlnp | grep ssh`
3. **Firewall block** — cek UFW + provider panel
4. **Fail2Ban ban** — `sudo fail2ban-client status sshd`
5. **MaxStartups limit** — terlalu banyak koneksi tertunda
6. **Provider DDoS protection** — coba dari IP/jaringan berbeda

Debug: `ssh -vvv user@host -p PORT`

## Coolify — Self-Hosted PaaS

Coolify = alternatif Vercel/Netlify self-hosted, 100% Docker-based.

### Remote Deploy ke Multiple Server

1. Server A: install Coolify
2. Server B & C: install Docker + SSH key dari Coolify
3. Dashboard → Add Server → isi IP, user, SSH port
4. Deploy: pilih target server

### Spec Minimum

| Server | CPU | RAM | Storage |
|--------|-----|-----|---------|
| Coolify (master) | 1-2 vCPU | 2-4 GB | 20-50 GB |
| Target (deploy) | 1 vCPU | 1-2 GB | 20 GB |

### Uninstall Total

```bash
sudo docker compose -f /data/coolify/source/docker-compose.yml down -v
sudo rm -rf /data/coolify /var/lib/coolify /etc/coolify
sudo docker volume rm $(docker volume ls -q | grep coolify)
sudo docker network rm coolify
```

## Related

- [[linux/docker/index]] — Docker & Container
- [[linux/network/index]] — Network tools
- [[linux/system/index]] — System admin
- [[discord/webhook/webhook-basics]] — Discord webhook
