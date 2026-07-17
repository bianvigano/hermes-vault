# Shared Memory System

## Konsep
SQLite + rsync antara local dan server. Shared facts/entities yang bisa diakses dari mana saja.

## Lokasi DB
- Local: `~/.hermes/shared-memory/memory.db`
- Server: `/root/.hermes/shared-memory/memory.db` (109.111.53.58:55225)

## Scripts
- `memory.py` — add/search/list/delete/export/stats
- `memory-sync.py` — bidirectional/pull/push via SSH rsync

## Schema
- `facts` — fakta/teks
- `entities` — entitas (orang, project, dll)
- `fact_entities` — relasi many-to-many
- `facts_fts` — full-text search index

## Penggunaan
```bash
python memory.py add "Fakta baru"
python memory.py search "keyword"
python memory-sync.py push
python memory-sync.py pull
```

## Status
- Auto-sync belum di-cron (manual saja)
