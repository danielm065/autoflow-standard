---
type: project-constitution
project: TaskTracker
created: 2026-02-01
---

# CONSTITUTION — TaskTracker

> Project-specific rules. Each has **Why**. Global vault rules live in vault `CLAUDE.md`.

---

## 📜 Active rules

### R1. < 2 second capture time
**Rule:** Any change that makes task capture take > 2 seconds is rejected.
**Why:** Friction kills adoption. The whole point is "lower than the urge to ignore the task." Measured: target p95 < 2s end-to-end (CLI command → DB row written).
**How to apply:** Every PR touching the capture flow gets benchmarked with `time tt add "test task"`. If > 2s, halt + diagnose.

### R2. No required fields beyond task text
**Rule:** Adding a task requires only the text. Tags, due date, priority are all optional with sensible defaults.
**Why:** Forcing fields = users skip and use sticky notes. Defaults solve 80% of cases.
**How to apply:** API + CLI signatures: only `text` is required. Web form must have skippable fields.

### R3. Daily digest is the only push notification
**Rule:** One email at 8 AM with overdue + today's tasks. No other notifications (no push, no SMS, no in-app banners).
**Why:** Notification fatigue. I check the digest with coffee. Anything more = annoying.
**How to apply:** Cron at 0 8 * * *. Block any PR adding new notification channels.

### R4. Postgres is the only persistent store
**Rule:** All persistent data in Postgres. Redis is allowed only for ephemeral queues + cache (TTL ≤ 1h).
**Why:** Single source of truth. Multi-store = sync hell.
**How to apply:** Any new "store this for X" → goes to Postgres. Redis only for "this is reproducible from Postgres if Redis dies."

### R5. No external service dependencies in critical path
**Rule:** Task capture + listing must work offline (no external API). Email sending can fail gracefully (queue + retry).
**Why:** I want capture to work on a plane. Offline-first.
**How to apply:** All hot-path code (`/add`, `/list`, `/done`) must succeed with no internet. Test in airplane mode.

### R6. No deletion — only archive
**Rule:** Tasks are never deleted. Marked `archived: true` and hidden from default views.
**Why:** Audit trail. Sometimes I want to know "did I do X?" 6 months later.
**How to apply:** No `DELETE FROM tasks` in any code. Only `UPDATE SET archived=true`. Add CI check if needed.

### R7. Daily digest can be muted but never disabled
**Rule:** `--mute-today` skips today's digest. There is no `--disable-digest` flag.
**Why:** Re-enabling friction. If I disable, I'll forget to re-enable.
**How to apply:** Code never exposes a "disabled" state for the digest cron.

---

## 🪦 Removed rules
(none yet)
