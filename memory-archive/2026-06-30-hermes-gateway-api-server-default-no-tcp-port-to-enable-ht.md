# Hermes gateway API server: default NO TCP port. To enable HTTP API on 8642: set 

- **Source:** memory
- **Archived:** 2026-06-30T07:42:11+07:00
- **Tags:** hermes,gateway,api,systemd

---

Hermes gateway API server: default NO TCP port. To enable HTTP API on 8642: set API_SERVER_ENABLED=true and API_SERVER_KEY (64 hex, via openssl rand -hex 32) in gateway env file, restart. hermes-workspace needs HERMES_API_URL and HERMES_API_TOKEN matching that key. Install as systemd user service: hermes gateway install (auto linger). Key pitfall: API_SERVER_KEY required even for loopback, without it refuse start.
