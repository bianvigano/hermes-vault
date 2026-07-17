# shared-memory-bank sync: scripts live in ~/.hermes/skills/shared-memory-bank/scr

- **Source:** memory
- **Archived:** 2026-06-25T03:36:38+07:00
- **Tags:** sync,shared-memory-bank,rsync

---

shared-memory-bank sync: scripts live in ~/.hermes/skills/shared-memory-bank/scripts/ NOT ~/.hermes/shared-memory/. Cron must point to skill scripts dir. memory.db and schema.sql must be real files (not symlinks) or rsync copies broken symlinks to server. Server /tmp may be unwritable — use /root/.hermes/shared-memory/ for temp files on server.
