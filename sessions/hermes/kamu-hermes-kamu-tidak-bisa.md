---
title: "di kamu hermes kamu tidak bisa bikin RTK.md untuk RTK - Rust Token Killer , kamu bisa cek dari /home"
date: 2026-07-13T10:37:56
session_id: 20260713_093229_1e03f0_20260713_103756_241676
category: hermes
model: jb/claude-sonnet-5
messages: 48
source_dump: request_dump_20260713_093229_1e03f0_20260713_103756_241676.json
---

# di kamu hermes kamu tidak bisa bikin RTK.md untuk RTK - Rust Token Killer , kamu bisa cek dari /home

## Ringkasan
Model: jb/claude-sonnet-5 | Pesan: 48 | Kategori: hermes

## Percakapan
### Q1: di kamu hermes kamu tidak bisa bikin RTK.md untuk RTK - Rust Token Killer , kamu bisa cek dari USER_HOME/.claude/RTK
### Q2: bukan ke USER_HOME/.claude tapi ke USER_HOME/.hermes/
**A:** File udah ada di `USER_HOME/.claude/RTK.md`, isinya: - RTK - Rust Token Killer, CLI proxy optimized token (60-90% savings) - Meta commands: `rtk gain`, `rtk gain --history`, `rtk discover`, `rtk proxy <cmd>` - Verifikasi install: `rtk --version`, `rtk gain`, `which rtk` - Hook-based: semua comma

### Q3: giman cara testnya ?
### Q4: bisa ga sementara dinonaktifkan system RTK bisa ga sementara dinonaktifkan system RTK entahlah sebuhtanya apa
### Q5: malha jadi tidak hemat token , degan tulisan sama seperti ini "coba aja jalankan terminal("ls -la"), atau yang lebih leb
## Commands
- `hermes plugins disable rtk-rewrite`
- `hermes plugins disable rtk-rewrite : 45.0K input · 1.5K output · 3 req | 46.5K`
- `hermes plugins enable rtk-rewrite`
- `hermes plugins enable rtk-rewrite : 63.8K input · 425 output · 4 req | 64.2K`

## Code
```bash
# Prefer .venv; fall back to venv if that's what your checkout has.
source .venv/bin/activate   # or: source venv/bin/activate
```

```bash
hermes-agent/
├── run_agent.py          # AIAgent class — core conversation loop (~12k LOC)
├── model_tools.py        # Tool orchestration, discover_builtin_tools(), handle_function_call()
├── toolsets.py           # Toolset definitions, _HERMES_CORE_TOOLS list
├── cli.py                # HermesCLI class — interactive CLI orchestrator (~11k LOC)
├── hermes_state.py       # SessionDB — SQLite session store (FTS5 search)
├── hermes_constants.py   # get_hermes_home(), display_hermes_home() — profile-aware paths
├── hermes_logging.py     # setup_logging() — agent.log / errors.log / gateway.log (profile-aware)
├── batch_runner.py       # Parallel batch processing
├── agent/                # Agent internals (provider adapters, memory, caching, compression, etc.)
├── hermes_cli/           # CLI s
```

```bash
tools/registry.py  (no deps — imported by all tool files)
       ↑
tools/*.py  (each calls registry.register() at import time)
       ↑
model_tools.py  (imports tools/registry + triggers tool discovery)
       ↑
run_agent.py, cli.py, batch_runner.py, environments/
```

## Sumber
- Request dump: `request_dump_20260713_093229_1e03f0_20260713_103756_241676.json`
- Session ID: `20260713_093229_1e03f0_20260713_103756_241676`

## Related
