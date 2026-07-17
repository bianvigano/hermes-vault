# Pending skill patch — remote-server-audit SKILL.md section 6: add "Reading lar

- **Source:** memory
- **Archived:** 2026-07-17T10:13:45+07:00
- **Tags:** archive, skill-patch-pending, remote-server-audit

---

Pending skill patch — remote-server-audit SKILL.md section 6: add "Reading large files reliably via SSH" subsection. Key learning: persistent PTY SSH sessions corrupt large cat output via buffer interleaving. Fix: scp file to local then read_file. Also add Hermes config v30 section map (gateway ~line 576, model at top, etc.). Cannot apply now — skill_manage can't reach devops/ subdirectory skills.
