# Hermes Workspace TanStack Start routing: File api/auth-logout.ts creates route /

- **Source:** memory
- **Archived:** 2026-06-29T21:29:39+07:00
- **Tags:** hermes,workspace,tanstack,routing,serverx

---

Hermes Workspace TanStack Start routing: File api/auth-logout.ts creates route /api/auth-logout (hyphen), NOT /api/auth/logout (nested). For nested routes, use folder structure: api/auth/index.ts + api/auth/logout.ts. Production mode (pnpm build + node server-entry.js) more stable than pnpm dev on remote (HMR causes exit 137). Always set -a && source .env && set +a before node server-entry.js or HERMES_PASSWORD wont load. VPS NAT only SSH port forwarded.
