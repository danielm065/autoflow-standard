---
type: project-processmap
project: TaskTracker
created: 2026-02-01
---

# PROCESS-MAP — TaskTracker

<!-- AUTO-START: vault-process-map -->
_Auto-section not populated yet. Run `vault refresh` to fill._
<!-- AUTO-END: vault-process-map -->

---

## ✏️ Manual — flow diagram

```mermaid
flowchart TD
    User[User: tt add 'X'] --> CLI[tt CLI]
    CLI -->|POST /api/tasks| API[Express API]
    API -->|INSERT| PG[Postgres]
    API -->|LPUSH event| Redis[Redis queue]
    API -->|response| CLI
    CLI --> UserAck[User sees ✓]

    Web[Browser: tasks.localhost] --> API

    Cron[cron 0 8 * * *] --> Digest[digest service]
    Digest -->|SELECT due tasks| PG
    Digest -->|send email| Resend[Resend API]
    Resend --> Inbox[User inbox]

    Events[Event poller] -->|BRPOP| Redis
    Events -->|UPDATE flags| PG
    Events -.->|on error| Sentry
```

## 🔗 Cross-process dependencies
- **API** + **CLI** + **Web** all share same Postgres + Redis
- **Digest** is independent — runs once daily
- **Event poller** is independent — drains Redis queue continuously

## 📋 Schedule
- `0 8 * * *` — Daily digest (Resend send)
- `*/15 * * * *` — Redis queue health check (Sentry breadcrumb)
- `0 3 * * 0` — Weekly archive (move `archived: true` rows to `tasks_archive` table)

## 📂 Files
- `src/api/` — Express server
- `src/cli/` — `tt` binary source
- `src/web/` — Next.js pages
- `src/digest/` — daily email service
- `cron/` — crontab entries + scripts
