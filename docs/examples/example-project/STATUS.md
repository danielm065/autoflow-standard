---
type: project-status
project: TaskTracker
last_updated: 2026-05-08
---

# STATUS — TaskTracker

## 🟢 Current state
**Production** — daily digest delivered for 87 consecutive days. ~12 captures/day average.

## ✅ Working
- CLI capture in p95 = 0.8s (R1 honored)
- Web UI for browsing
- Daily digest at 8 AM
- Archive flow (R6)
- Redis queue + event poller

## 🐛 Open bugs
- 🟡 **CLI takes 3-5s on first call after laptop sleep** — DNS resolution delay on `localhost`. Worked around with `127.0.0.1`. Permanent fix: cache resolved address.

## ✓ Recently closed (2026-04 / 2026-05)
- ~~Digest stripped emojis on Resend send~~ — fixed: Resend HTML template uses UTF-8 explicitly
- ~~Postgres pool exhaustion under burst load~~ — bumped pool 10→20 + connection timeout 5s

## 📋 Open tasks
- [ ] Cache DNS for `localhost` to fix sleep-recovery slow first-call
- [ ] Add `tt search` command (full-text Postgres `ts_vector`)
- [ ] Backup retention bumped 30d → 90d (it's cheap)
- [ ] Add `--mute-today` for digest

## 📌 Where to pick up if you're new
1. Read [VISION.md](VISION.md) — single-user, simple
2. Read [CONSTITUTION.md](CONSTITUTION.md) — 7 rules, all with Why
3. Read [SYSTEM.md](SYSTEM.md) — Node + Postgres + Redis
4. Try `tt add "test"` to verify capture
5. Check `pm2 status` for running processes

## 🔗 Quick links
- [VISION](VISION.md)
- [CONSTITUTION](CONSTITUTION.md)
- [SYSTEM](SYSTEM.md)
- [RUNBOOK](RUNBOOK.md)
- [decisions](decisions.md)
