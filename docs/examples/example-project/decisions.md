---
type: project-decisions
project: TaskTracker
created: 2026-02-01
append_only: true
---

# Decisions Log — TaskTracker

> Append-only. Never delete entries. Order: oldest first (FIFO).

## 2026-02-01 — Initial stack: Node + Postgres + Redis
**Decision:** Build with Node.js + Express + Postgres + Redis + Resend.
**Why:** I know Node best (R1 — fast iteration matters). Postgres already running. Redis is cheap.
**Alternatives considered:**
- Go/Rust → slower iteration, no real perf need
- SQLite → blocked by concurrent CLI + web access pattern
- BullMQ → overkill for ~12 tasks/day
**Consequences:** Single-node Postgres = bottleneck if I ever go multi-user (out of scope per VISION).
**Outcome (retrospective):** ✅ Solid choice. 87 days production, zero stack-related incidents.

## 2026-02-05 — No required fields beyond `text`
**Decision:** Task schema: only `text` is NOT NULL.
**Why:** R2 in CONSTITUTION — friction kills adoption.
**Alternatives considered:** Require `due_date` or `tag` for "discipline" — rejected, would just slow me down.
**Consequences:** Need sensible defaults everywhere (`due_date = NULL = "someday"`).
**Outcome (retrospective):** ✅ Use rate confirms — I never skip captures.

## 2026-02-10 — Daily digest is the only push
**Decision:** Email at 8 AM. No SMS, no push, no in-app banners.
**Why:** R3 — notification fatigue.
**Alternatives considered:** Slack DM, mobile push — all rejected.
**Consequences:** If I miss the email, I miss the reminders. Acceptable.
**Outcome (retrospective):** ✅ I've muted it 0 times in 87 days.

## 2026-03-15 — Reject AI-suggested tasks idea
**Decision:** No GPT integration for task generation / estimation.
**Why:** Was tempted to add "let GPT estimate task duration" — pushed back to Out-of-Scope. I know my own tasks better than an LLM.
**Alternatives considered:** A "smart" mode using GPT-4o — rejected.
**Consequences:** Won't ever auto-categorize or auto-tag.
**Outcome (retrospective):** ✅ Still happy. Saved feature complexity.

## 2026-05-08 — Use `127.0.0.1` instead of `localhost` in CLI default
**Decision:** CLI default API URL = `http://127.0.0.1:3000` (was `http://localhost:3000`).
**Why:** macOS DNS resolver caches negative `localhost` lookups after sleep, causing 3-5s delays on first capture post-wake. Violates R1 (< 2s).
**Alternatives considered:**
- DNS cache logic in CLI — too much code for an OS quirk
- Run `dscacheutil -flushcache` after wake — manual, easy to forget
**Consequences:** All future CLI configs default to numeric IP. Users on Linux unaffected.
**Outcome (retrospective):** TBD — verify over next 30 days.

<!-- ⬇️ INSERT NEW DECISIONS ABOVE THIS LINE — newest at bottom (chronological FIFO) ⬇️ -->
