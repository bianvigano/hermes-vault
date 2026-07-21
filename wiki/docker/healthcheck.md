# Docker Healthcheck & Graceful Shutdown

## HEALTHCHECK

HEALTHCHECK = cara Docker tahu apakah container **benar-benar sehat**, bukan cuma "prosesnya masih jalan".

### Kenapa Penting?

Tanpa healthcheck, Docker hanya cek **apakah PID 1 masih hidup**. Tapi proses bisa hidup tapi stuck/error (e.g., deadlock, DB connection lost).

### Cara Pakai

```dockerfile
# Exec form (recommended)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Shell form
HEALTHCHECK CMD pg_isready -U postgres || exit 1
```

### Parameter

| Parameter | Default | Keterangan |
|---|---|---|
| `--interval` | 30s | Seberapa sering health check dijalankan |
| `--timeout` | 30s | Max waktu 1x check |
| `--start-period` | 0s | Grace period setelah start (jangan hitung failure) |
| `--retries` | 3 | Berapa kali retry sebelum `unhealthy` |

### Status Container

```bash
docker ps                    # lihat kolom STATUS
# Up 5 minutes (healthy)    ← sehat
# Up 3 minutes (unhealthy)  ← tidak sehat
# Up 10 seconds (starting)  ← masih start-period

docker inspect --format='{{json .State.Health}}' web | python3 -m json.tool
```

### Contoh per Language

**Web app:**
```dockerfile
HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

**PostgreSQL:**
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U postgres || exit 1
```

**Redis:**
```dockerfile
HEALTHCHECK --interval=10s --timeout=3s \
  CMD redis-cli ping || exit 1
```

### Compose `depends_on` dengan Healthcheck

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy  # tunggu db benar-benar sehat
  
  db:
    image: postgres:17
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
```

## Graceful Shutdown — SIGTERM

### Masalah

Saat `docker stop`, Docker kirim **SIGTERM** ke PID 1, tunggu 10 detik, lalu **SIGKILL** (force kill). Kalau app tidak handle SIGTERM → connection drop, data loss.

### Solusi

**Node.js:**
```js
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down...');
  server.close();          // stop accept new requests
  await db.disconnect();   // graceful DB disconnect
  process.exit(0);
});
```

**Python:**
```python
import signal, sys

def shutdown(sig, frame):
    print("SIGTERM received, closing...")
    server.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
```

**Go:**
```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
<-ctx.Done()
server.Shutdown(context.Background())
```

**Bash:**
```bash
#!/bin/bash
cleanup() {
    echo "Shutting down..."
    kill $PID
    exit 0
}
trap cleanup SIGTERM SIGINT
```

### Penting: EXEC form CMD

```dockerfile
# BAIK — app adalah PID 1, terima SIGTERM langsung
CMD ["node", "server.js"]

# BURUK — shell adalah PID 1, SIGTERM tidak diteruskan ke app
CMD node server.js
```

### STOP_TIMEOUT di Compose

```yaml
services:
  api:
    stop_grace_period: 30s   # tunggu 30 detik sebelum SIGKILL
```

## Pola Umum

1. **Health endpoint**: `GET /health` → return 200 kalau DB, cache, external service OK
2. **Readiness endpoint**: `GET /ready` → return 200 kalau siap terima traffic
3. **Grace period**: 5–15 detik start-period untuk app warm-up
4. **Kubernetes**: liveness probe + readiness probe = HEALTHCHECK on steroids

## Sumber

- [Docker HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck)
- [Docker stop](https://docs.docker.com/reference/cli/docker/container/stop/)
