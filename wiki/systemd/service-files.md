# Systemd Service Files

Bikin custom service untuk aplikasi sendiri. Supaya app auto-start dan systemd yang manage lifecycle-nya.

## Template Service Minimal

```ini
[Unit]
Description=My Python App
After=network.target

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/main.py
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

## Contoh: Node.js App

```ini
[Unit]
Description=Next.js Production App
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/myapp
ExecStart=/usr/bin/node /var/www/myapp/.next/standalone/server.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production
Environment=PORT=3000
EnvironmentFile=/etc/myapp/env
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```

## Contoh: Python + Gunicorn

```ini
[Unit]
Description=Flask Gunicorn App
After=network.target

[Service]
Type=notify
User=flaskuser
Group=flaskuser
WorkingDirectory=/opt/flaskapp
ExecStart=/opt/flaskapp/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Contoh: Go Binary

```ini
[Unit]
Description=Go API Server
After=network.target

[Service]
Type=simple
User=gouser
ExecStart=/usr/local/bin/go-api-server
Restart=always
RestartSec=5
LimitNOFILE=65536
ProtectSystem=full
ProtectHome=yes
NoNewPrivileges=yes

[Install]
WantedBy=multi-user.target
```

## Contoh: Timer + Service (Backup Harian)

backup.service:
```ini
[Unit]
Description=Daily Backup Task

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=root
```

backup.timer:
```ini
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

## Lifecycle Commands

```bash
# Buat file service
sudo vim /etc/systemd/system/myapp.service

# Reload systemd (setelah create/edit file)
sudo systemctl daemon-reload

# Enable (auto-start at boot)
sudo systemctl enable myapp.service

# Start
sudo systemctl start myapp.service

# Status
sudo systemctl status myapp.service

# Stop
sudo systemctl stop myapp.service

# Disable
sudo systemctl disable myapp.service

# Restart
sudo systemctl restart myapp.service

# Reload (tanpa restart penuh)
sudo systemctl reload myapp.service

# Lihat log
journalctl -u myapp.service -f

# Lihat log sejak boot terakhir
journalctl -u myapp.service -b
```

## Best Practices

1. **Gunakan user non-root** — `User=` dan `Group=`
2. **Restart policy** — `Restart=on-failure` minimal
3. **Environment di EnvironmentFile** — bukan hardcode di unit file
4. **Type=simple** default — biasanya paling cocok buat app modern
5. **daemon-reload** setiap selesai edit unit
6. **Testing**: `systemctl start` → `systemctl status` → `journalctl -u`
7. **Hardening**: tambah `ProtectSystem=full`, `ProtectHome=yes`, `NoNewPrivileges=yes` kalau bisa

## Troubleshooting

```bash
# Cek apakah unit file valid
systemd-analyze verify /etc/systemd/system/myapp.service

# Cek dependency tree
systemd-analyze critical-chain myapp.service

# Cek semua log dari unit
journalctl -u myapp.service --no-pager -l

# Cek error spesifik
systemctl status myapp.service -l
```

## Sumber

- `man systemd.service`
- `man systemctl`
- `man systemd.exec` — environment, sandboxing directives

## Lanjut Baca

- [[wiki/systemd/overview]] — Overview systemd
- [[wiki/systemd/units]] — Unit types
- [[wiki/systemd/timers]] — Timer units
- [[wiki/systemd/journalctl]] — Log query
- [[wiki/systemd/commands]] — Cheatsheet
