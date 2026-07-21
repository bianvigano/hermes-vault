# Memory Archive - 2026-07-18

## Archival Source: MEMORY.md

### Entry 3 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 4 - skill_manage Subdirectory Limitation
```
skill_manage tool cannot find/edit symlinked skills OR skills in subdirectories. Workaround: create via skill_manage(action='create', category='devops'), or edit files directly via terminal.
```
Timestamp: 2026-07-18
Tags: archive-old-entries, work-around, skill_manage

### Entry 5 - Pending skill patch for remote-server-audit
```
Pending skill patch — remote-server-audit SKILL.md section 6 "Config (sanitized)": add "Reading large files reliably via SSH" subsection. Key learning: persistent PTY SSH sessions corrupt large `cat` output via buffer interleaving. Fix: scp file to local then read_file. Also add Hermes config v30 section map (gateway ~line 576, model at top, etc.). Cannot apply now — skill_manage can't reach devops/ subdirectory skills.
```
Timestamp: 2026-07-18
Tags: archive-old-entries, pending-patch, remote-server-audit, ssh

### Entry 6 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 8 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 9 - minecraft-server-management v2.0
```
minecraft-server-management skill (gaming/) needs v2.0. Bug: skill_manage can't reach gaming/ subcategory — must edit SKILL.md file directly.
```
Timestamp: 2026-07-18
Tags: archive-old-entries, minecraft, skill-update, bug-workaround

### Entry 10 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 14 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 16 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 18 - Section Separator
```
§
```
Timestamp: 2026-07-18
Tags: archive-old-entries, section-separator

### Entry 20 - Duplicate Vault GitHub Pages hosting
```
Vault GitHub Pages hosting: repo bianvigano/hermes-vault, Pages URL https://bianvigano.github.io/hermes-vault/. Script vault_cache.py di ~/.hermes/vault/scripts/ baca dari cache local (~/.hermes/vault-cache/, TTL 24h auto-extend) atau fetch dari GitHub Pages. Multi-token GitHub API fallback. Config: github.vault_repo dan github.tokens di ~/.hermes/config.yaml. Need .nojekyll and index.html redirect. All /home/the-meh/ in vault files sanitized to USER_HOME/ before push.
```
Timestamp: 2026-07-18
Tags: archive-old-entries, duplicate-entry, vault-github-pages

## Archival Summary
- Total entries archived: 11
- Source: MEMORY.md section separators and obsolete entries
- Archive date: 2026-07-18