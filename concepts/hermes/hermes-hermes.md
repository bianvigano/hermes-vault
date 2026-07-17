---
title: "di kamu hermes kamu tidak bisa bikin RTK.md untuk RTK - Rust Token Killer , kamu"
date: 2026-07-16
category: hermes
tags: []
source: "sessions/hermes/kamu-hermes-kamu-tidak-bisa.md"
---

# di kamu hermes kamu tidak bisa bikin RTK.md untuk RTK - Rust Token Killer , kamu

## Masalah
- di kamu hermes kamu tidak bisa bikin RTK.md untuk RTK - Rust Token Killer , kamu bisa cek dari /home
- es_logging.py     # setup_logging() — agent.log / errors.log / gateway.log (profile-aware)
├── batch_runner.py       # Parallel batch processing

## Commands
- `hermes plugins disable rtk-rewrite : 45.0K input · 1.5K output · 3 req | 46.5K`
- `hermes plugins enable rtk-rewrite`
- `hermes plugins enable rtk-rewrite : 63.8K input · 425 output · 4 req | 64.2K` ```bash`
- `hermes-agent/`

## Code
```bash
hermes-agent/
├── run_agent.py          # AIAgent class — core conversation loop (~12k LOC)
├── model_tools.py        # Tool orchestration, discover_builtin_tools(), handle_function_call()
├── toolsets.py           # Toolset definitions, _HERMES_CORE_TOOLS list
├── cli.py                # HermesCLI class — interactive CLI orchestrator (~11k LOC)
├── hermes_state.py       # SessionDB — SQLite session store (FTS5 search)
├── hermes_constants.py   # get_hermes_home(), display_hermes_home() — profil
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
- [sessions/hermes/kamu-hermes-kamu-tidak-bisa.md](sessions/hermes/kamu-hermes-kamu-tidak-bisa.md)

## Related
