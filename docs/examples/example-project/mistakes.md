---
type: project-mistakes
project: TaskTracker
created: 2026-02-01
append_only: true
---

# Mistakes Log — TaskTracker

> Append-only. Read this BEFORE trying anything similar.

## 📋 Template

```markdown
## YYYY-MM-DD — short title
**Tried:** what I did
**Result:** what happened
**Why it failed:** root cause
**Better approach:** what works now
**Tags:** [postgres, redis, ...]
```

---

## ❌ Mistakes

<!-- ⬇️ INSERT NEW MISTAKES ABOVE THIS LINE — newest at top (LIFO) ⬇️ -->

## 2026-04-10 — Tried adding GPT for task estimation
**Tried:** Wired in OpenAI API to estimate "how long will this task take?" based on the text.
**Result:** Estimates were laughably wrong (5x off on average). Added 2s latency to capture flow.
**Why it failed:** LLM has no context on my actual work patterns. Even with system prompt, it guessed wildly. Latency violated R1.
**Better approach:** Removed entirely. Logged decision 2026-03-15 (predated this attempt; should have followed the decision).
**Tags:** [llm, latency, r1, r3]

## 2026-03-04 — Sentry SDK cold start killed CLI < 2s budget
**Tried:** Added `import * as Sentry from "@sentry/node"` at top of CLI entry point.
**Result:** CLI cold start jumped from 200ms to 1.1s. Sometimes exceeded 2s end-to-end (R1 fail).
**Why it failed:** Sentry SDK does sync setup work at import time (DSN parsing, transport init).
**Better approach:** Lazy-load Sentry: `if (process.env.SENTRY_DSN) { const { init } = require("@sentry/node"); init({ dsn: ... }) }` inside the error handler only.
**Tags:** [sentry, cold-start, r1]

## 2026-02-20 — Redis used as primary task store
**Tried:** Originally stored tasks in Redis Sorted Sets keyed by due-date timestamp. Skipped Postgres for "speed."
**Result:** Lost 3 days of tasks when Redis crashed (no persistence enabled). Also: querying by tag was painful.
**Why it failed:** Redis is NOT a database. RDB snapshots are async; AOF is heavier. R4 was crystallized post-this-incident.
**Better approach:** Postgres = source of truth (R4). Redis = ephemeral queue + cache only (TTL ≤ 1h).
**Tags:** [redis, postgres, data-loss, r4]
