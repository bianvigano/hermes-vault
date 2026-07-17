# Memory-context system v1 (June 24, 2026): Folder ~/.hermes/memory-context/ beris

- **Source:** memory
- **Archived:** 2026-06-29T03:06:04+07:00
- **Tags:** memory-context,servers,ssh,system-architecture

---

Memory-context system v1 (June 24, 2026): Folder ~/.hermes/memory-context/ berisi dua subfolder: servers/ (config server: servers.yaml) dan memory/ (memory bank: memory.db, memory.py, memory-sync.py, schema.sql). Script: server.py, ssh-key-copy.py, push_server_data.py, run_verify.py, add_server_data.py, verify_server.py, sshpass_mini.py, migrate.py. servers.yaml = single source of truth untuk koneksi SSH. Memory bank (SQLite) = shared memory untuk facts/scenarios/context_snippets/decisions. User prefer Indonesian, langsung action.
