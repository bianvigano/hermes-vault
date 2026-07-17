# Vault System

## Apa itu Vault?
Persistent storage untuk session lama + memory archive + knowledge base.

## Lokasi
- Vault: `~/.hermes/vault/`
- Sessions: `~/.hermes/vault/sessions/`
- Wiki: `~/.hermes/vault/wiki/`
- Memory archive: `~/.hermes/vault/memory-archive/`
- Index: `~/.hermes/vault/index.md`

## Flow
1. Session berakhir → disimpan di `~/.hermes/sessions/`
2. Vault ingest (tiap 2h) → pindah session >30 hari ke vault
3. Memory flush (tiap 2h) → archive memory ke vault kalau >80%
4. Wiki → manual/organized knowledge base

## Cara Akses
- `session_search(query="...")` — search session lama
- `read_file("~/.hermes/vault/sessions/...")` — baca session
- `search_files(pattern="...", path="~/.hermes/vault/wiki/")` — search wiki

## Shared Memory
- SQLite DB: `~/.hermes/shared-memory/memory.db`
- Sync ke server via rsync (SSH port 55225)
- Script: `memory.py` (CRUD), `memory-sync.py` (sync)
