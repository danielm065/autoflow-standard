---
type: project-system
project: TaskTracker
status: hybrid-doc
created: 2026-02-01
---

# SYSTEM — TaskTracker

## 🤖 Auto-generated section
<!-- vault-arch-refresh would populate this. Skipped in example. -->

---

## ✏️ Manual section

### Why this architecture?

**Stack:** Node.js + Express + Postgres + Redis + Resend + Sentry

**Trade-offs:**
- **Node.js, not Go/Rust** — I know Node best. Sub-2s capture (R1) doesn't need ultra-low latency.
- **Postgres, not SQLite** — already have Postgres running; need concurrent access from CLI + web.
- **Redis for queue, not BullMQ/RabbitMQ** — overkill. Redis lists + simple poller is enough at this scale.
- **Resend, not SES** — simpler setup, free tier covers personal use.
- **Sentry, not Datadog** — free tier sufficient.

### High-level data flow

```
CLI: `tt add "Buy milk"`
    │
    ▼
┌────────────────┐
│ tt CLI binary  │
│ (Node.js)      │
└────────┬───────┘
         │ HTTP POST /api/tasks
         ▼
┌────────────────┐         ┌───────────┐
│ Express API    │────────►│ Postgres  │  (R4: only persistent store)
│                │         │  tasks    │
└────────┬───────┘         └───────────┘
         │
         │ LPUSH redis queue
         ▼
┌────────────────┐
│ Redis          │  (R4: ephemeral only, TTL ≤ 1h)
│ task-events    │
└────────────────┘

Web UI: http://localhost:3000
    │
    ▼
Express API → Postgres

Daily digest (8 AM):
Cron → digest service → Postgres SELECT → Resend send
                                          │
                                          └─ (on fail) → Sentry + retry queue
```

### Critical invariants
- **R1 < 2s capture** — measured end-to-end
- **R2 only `text` required** — schema enforced (other cols nullable)
- **R4 Postgres = SOT** — Redis data is reproducible
- **R5 offline capture** — hot path uses no external services
- **R6 no delete** — schema has no `DELETE` privilege for app user

### Known limits
- **Single user** — multi-user would require auth + RLS rewrite
- **Postgres single-node** — no read replicas. Acceptable at this load.
- **Resend free tier** — 3,000 emails/month (digest = ~30/month, fine)
- **CLI requires server running** — could be improved with local SQLite fallback (out of scope per R5 spirit)

### Failure modes
- **API down** → CLI fails. Manual SQL or wait.
- **Postgres down** → everything fails. Service crashes loud.
- **Redis down** → API still works, queue drops (next migration: persistent queue)
- **Resend down** → digest queued + retried with backoff
- **Sentry down** → errors logged locally (best-effort)

### Open questions
- Should CLI have local SQLite fallback when API offline? (Currently violates "Postgres SOT" but improves R5 offline-capture.)
- Add a TUI (terminal UI) for browsing tasks? Maybe, low priority.
