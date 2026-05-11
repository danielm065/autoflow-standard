---
type: project-onboarding
project: TaskTracker
created: 2026-02-01
---

# ONBOARDING — TaskTracker

> "Hello World" in under 30 minutes for a fresh machine.

## ✅ Prerequisites
- [ ] Node.js 20+ (`node --version`)
- [ ] Postgres 14+ running (`pg_isready`)
- [ ] Redis 6+ running (`redis-cli ping` → PONG)
- [ ] Git
- [ ] 1Password or env var manager

## 🔐 Credentials (references — not values)
- **Password manager:** 1Password vault → `TaskTracker`
- **Items needed:**
  - `POSTGRES_URL` — connection string
  - `REDIS_URL` — connection string
  - `RESEND_API_KEY` — for digest email
  - `SESSION_SECRET` — JWT signing key (64 chars random)

## 🔌 External services

| Service | Purpose | URL | Account |
|---|---|---|---|
| Resend | digest email | https://resend.com | personal |
| Sentry | error tracking | https://sentry.io | personal |

## 🚀 Setup
```bash
# Clone
git clone git@github.com:user/tasktracker.git
cd tasktracker

# Install deps
npm ci

# Copy env
cp .env.example .env
# Fill values from 1Password

# Migrate DB
npm run migrate

# Seed (optional)
npm run seed

# Start dev server
npm run dev
# Visit http://localhost:3000
```

## 👋 Hello World — verify it works
```bash
# CLI capture
npm run cli -- add "Test task"
# → "✓ Task #1 created"

# CLI list
npm run cli -- list
# → "1. Test task (no due date)"

# Web check
curl http://localhost:3000/api/tasks
# → [{"id":1,"text":"Test task",...}]

# Digest dry run
npm run digest -- --dry-run
# → "Would send to me@example.com: 1 overdue, 0 today"
```

## 🩹 Common setup issues
- **Postgres `connection refused`** → check `POSTGRES_URL` host (likely `localhost`, not `postgres`)
- **Redis `ECONNREFUSED`** → start with `redis-server` or `brew services start redis`
- **Resend `401`** → token revoked or wrong account; rotate from dashboard
- **Migration fails** → drop schema, re-run: `psql -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"` then `npm run migrate`

## 🗺️ Where to go next
1. [VISION.md](VISION.md) — why this exists
2. [SYSTEM.md](SYSTEM.md) — how it's built
3. [STATUS.md](STATUS.md) — where we are
4. [CONSTITUTION.md](CONSTITUTION.md) — rules
