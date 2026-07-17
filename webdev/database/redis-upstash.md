# Redis dan Upstash

Redis sebagai penyimpanan key-value dalam memori, dengan Upstash sebagai layanan Redis cloud via REST API. Mencakup environment variable Upstash dan troubleshooting Docker Redis.

---

## Upstash Redis: Environment Variable

`UPSTASH_REDIS_REST_URL` dan `UPSTASH_REDIS_REST_TOKEN` adalah environment variable untuk akses Redis Upstash via REST API (bukan koneksi TCP tradisional).

- `UPSTASH_REDIS_REST_URL`: endpoint REST, format `https://<instance-id>.upstash.io`
- `UPSTASH_REDIS_REST_TOKEN`: token autentikasi Bearer

### Contoh Penggunaan (REST API)

```js
const redisUrl = process.env.UPSTASH_REDIS_REST_URL;
const redisToken = process.env.UPSTASH_REDIS_REST_TOKEN;

async function getRedisValue(key) {
  const res = await fetch(`${redisUrl}/get/${key}`, {
    headers: {
      Authorization: `Bearer ${redisToken}`,
    },
  });
  const data = await res.json();
  return data.result;
}
```

### Digunakan Untuk

- Next.js (middleware/session/cache/token)
- Serverless functions (edge-compatible via HTTP)
- Edge functions (Vercel, Cloudflare Workers)

---

## Fix Docker Redis Error: `manifest not found`

Error:

```
manifest for bitnami/redis:latest not found: manifest unknown
```

Penyebab: Bitnami tidak menyediakan tag `latest` untuk image Redis.

### Docker Compose Sebelum (Error)

```yaml
redis:
  image: 'bitnami/redis:latest'
  container_name: redis_chat
  volumes:
    - ./redisdata:/bitnami/redis/data
  ports:
    - 6379:6379
  environment:
    - REDIS_AOF_ENABLED=no
    - ALLOW_EMPTY_PASSWORD=yes
  networks:
    - chat
```

### Solusi: Gunakan Versi Spesifik

Ganti `bitnami/redis:latest` dengan versi spesifik:

```yaml
redis:
  image: 'bitnami/redis:7.2.4-debian-11-r3'
  container_name: redis_chat
  volumes:
    - ./redisdata:/bitnami/redis/data
  ports:
    - 6379:6379
  environment:
    - REDIS_AOF_ENABLED=no
    - ALLOW_EMPTY_PASSWORD=yes
  networks:
    - chat
```

Lihat tag tersedia: <https://hub.docker.com/r/bitnami/redis/tags>

### Tips

- Hindari tag `:latest` di production — tidak stabil dan bisa berubah sewaktu-waktu.
- Selalu tentukan versi spesifik untuk CI/CD dan konsistensi.

---


## Related

- [[mongodb-setup]]
- [[supabase]]
- [[index]]
