# Docker Logging & Monitoring

Container menulis log ke **stdout** dan **stderr**. Docker menangkapnya via **logging driver** — default: `json-file`.

## Logging Drivers

| Driver | Output | Use Case |
|---|---|---|
| `json-file` | File JSON di host (default) | Development, simple |
| `local` | File terkompresi + auto-rotate (recommended) | Production single-host |
| `syslog` | Syslog daemon | Central logging |
| `journald` | systemd journal | Systemd-based host |
| `fluentd` | Fluentd collector | Centralized + structured |
| `gelf` | Graylog/GELF endpoint | Graylog stack |
| `awslogs` | AWS CloudWatch | AWS ECS/EC2 |
| `gcplogs` | Google Cloud Logging | GCP/GKE |
| `splunk` | Splunk | Enterprise |
| `none` | Disable logging | Silence |

### Konfigurasi Logging Driver

```bash
# Per-container
docker run --log-driver fluentd --log-opt fluentd-address=localhost:24224 nginx

# Global default (/etc/docker/daemon.json)
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Log Rotation (json-file)

```bash
docker run \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  nginx
```

### Compose

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Viewing Logs

```bash
docker logs web              # semua log
docker logs -f web           # follow (real-time)
docker logs --tail 50 web    # 50 baris terakhir
docker logs --since 1h web   # 1 jam terakhir
docker logs --until 10m web  # sampai 10 menit yang lalu
docker logs -t web           # dengan timestamp
```

## Structured Logging

### Kirim Log JSON ke stdout

**Node.js:**
```js
console.log(JSON.stringify({ level: "info", msg: "user login", userId: 123 }));
```

**Python:**
```python
import json
print(json.dumps({"level": "info", "msg": "order created", "orderId": 456}))
```

Log driver `fluentd` atau `gelf` akan parse otomatis.

## Centralized Logging Stack

### ELK (Elasticsearch + Logstash + Kibana)

```
Container → json-file → Filebeat → Logstash → Elasticsearch → Kibana
```

### EFK (Elasticsearch + Fluentd + Kibana)

```
Container → fluentd driver → Fluentd → Elasticsearch → Kibana
```

```yaml
# docker-compose.yml — EFK stack
services:
  fluentd:
    image: fluent/fluentd:v1.16
    volumes:
      - ./fluentd/conf:/fluentd/etc
    ports:
      - "24224:24224"
  
  elasticsearch:
    image: elasticsearch:8
    environment:
      - discovery.type=single-node
  
  kibana:
    image: kibana:8
    ports:
      - "5601:5601"
```

## Monitoring

### cAdvisor (Container Advisor)

Monitor resource usage semua container — CPU, memory, disk, network.

```bash
docker run -d --name cadvisor \
  -p 8080:8080 \
  -v /:/rootfs:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /sys:/sys:ro \
  -v /var/lib/docker/:/var/lib/docker:ro \
  gcr.io/cadvisor/cadvisor
# Dashboard: http://localhost:8080
```

### Prometheus + Grafana

```
Container → cAdvisor → Prometheus → Grafana Dashboard
```

```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

### Docker CLI Monitoring

```bash
docker stats                          # live CPU/Memory/Net I/O
docker stats --no-stream              # snapshot satu kali
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker events                         # live Docker events
docker system df                      # disk usage
docker system df -v                   # per-object detail
```

### Prometheus Exporter

```yaml
# docker-compose.yml
services:
  app:
    ports:
      - "8080:8080"
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=8080"
```

## Tips

- Production: pakai `local` atau `fluentd` driver, bukan `json-file`
- Selalu set `max-size` + `max-file` untuk rotasi
- Jangan simpan log di file dalam container (tulis ke stdout)
- Gunakan structured logging (JSON) untuk query yang lebih baik
- `docker events` untuk debug container lifecycle

## Sumber

- [Docker Logging Drivers](https://docs.docker.com/engine/logging/configure/)
- [cAdvisor](https://github.com/google/cadvisor)
- [Prometheus Docker](https://docs.docker.com/config/daemon/prometheus/)
