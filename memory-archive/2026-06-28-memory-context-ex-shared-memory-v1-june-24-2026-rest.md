# memory-context/ (ex shared-memory/) v1 (June 24, 2026): Restructured into two su

- **Source:** memory
- **Archived:** 2026-06-28T14:58:48+07:00
- **Tags:** memory-context,servers,memory-bank,restructure

---

memory-context/ (ex shared-memory/) v1 (June 24, 2026): Restructured into two subsystems:
- servers/servers.yaml — server config (IP, port, user, tags, notes). Single source of truth for all SSH/sync scripts.
- memory/ — memory bank (SQLite + Python scripts). context_snippets for server info via server.py add-to-memory.
Scripts: server.py (manager), memory.py (CRUD), memory-sync.py (rsync sync), ssh-key-copy.py, push_server_data.py, run_verify.py.
All paths: ~/.hermes/memory-context/ (local), /root/.hermes/memory-context/ (server).
Key design decision: server.py add does NOT auto-save to memory bank — must be explicit via add-to-memory.
