---
type: project-handoff
project: TaskTracker
session_date: 2026-05-08
---

# HANDOFF — TaskTracker

## 🎯 What was done last session (2026-05-08)
- Investigated CLI slow-on-wake bug (Open bug #1)
- Confirmed root cause: macOS DNS resolver caches negative lookups for `localhost` after sleep
- Local workaround: changed CLI default API URL from `http://localhost:3000` to `http://127.0.0.1:3000`
- Pushed to main, deployed
- Verified: 5 sleep-wake cycles, all captures < 1s

## 📍 Where I stopped
- Workaround deployed. Bug closed in [STATUS.md](STATUS.md).
- Did NOT yet address "permanent fix" (caching resolved address). Workaround is good enough.

## ➡️ Next step (immediate)
1. Decide whether to keep `127.0.0.1` or add proper DNS cache logic
2. Start work on `tt search` command (open task #2)

## 🪤 Open (not blocking)
- Backup retention bump (30→90d) — trivial, do anytime
- `--mute-today` digest flag — nice-to-have

## 📝 Files touched last session
- `src/cli/config.ts` — changed default API URL
- `STATUS.md` — moved bug from Open to Closed
- `decisions.md` — logged: "Use 127.0.0.1 over localhost to avoid macOS DNS sleep issues"

## ⚠️ Blockers
- None

---
_End of handoff. Next session: pick up from "Next step" above._
