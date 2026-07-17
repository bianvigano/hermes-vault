# Hermes Setup

## Info Server
- Remote: 109.111.53.58:55225 (user: root)
- Hermes v0.15.1 (outdated)
- RAM 3.9GB, Disk 61%, Node.js belum install
- 153 sessions, 7.5M tokens

## Local
- VS Code 1.124.0
- Hermes profile: default
- Skills: 27+ installed

## Sistem Aktif
- [[vault-system]] — Vault ingest tiap 2h, cleanup tiap 24h
- [[shared-memory]] — SQLite + rsync antara local dan server
- Memory flush — auto-archive kalau memory >80%
- Cron: vault-session-ingest (2h), vault-cleanup-old-sessions (24h), memory-flush-check (2h)

## Skill System
- Auto-detect + auto-fetch dari GitHub (Approach C)
- Symlink-based skill management
- skill_manage TIDAK bisa edit symlinked skills → edit langsung via write_file

## Konfigurasi Penting
- memory_char_limit=5000
- user_char_limit=3000
- Timezone: WIB (UTC+7)
- Language: Indonesian
