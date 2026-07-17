# Vault pipeline v3 (old stats): vault_update.py reads request_dump JSON from /hom

- **Source:** memory
- **Archived:** 2026-07-17T10:11:30+07:00
- **Tags:** archive, vault-pipeline, superseded

---

Vault pipeline v3 (old stats): vault_update.py reads request_dump JSON from /home/the-meh/.hermes/sessions/ -> generate session .md in vault/sessions/ -> vault_concepts.py extracts concepts. Cron vault-session-ingest runs every 2h: pipeline + cleanup. Old v1 sessions archived to vault/sessions-archive/. 46 user sessions dumped, 18 processed, 28 skipped.
