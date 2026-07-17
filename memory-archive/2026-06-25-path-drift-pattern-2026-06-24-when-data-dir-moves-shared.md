# Path drift pattern (2026-06-24): when data dir moves (shared-memory/ → memory-

- **Source:** memory
- **Archived:** 2026-06-25T03:35:29+07:00
- **Tags:** path-drift,migration,memory-context

---

Path drift pattern (2026-06-24): when data dir moves (shared-memory/ → memory-context/memory/), must update ALL path refs: LOCAL_DB, schema_path in memory-sync.py, SERVER_DB_PATH, cron prompts. Grep -r oldpath in skills dir to find stale refs.
