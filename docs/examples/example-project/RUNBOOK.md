---
type: project-runbook
project: TaskTracker
created: 2026-02-01
---

# RUNBOOK — TaskTracker

## 🚨 Incident Response

### Scenario: Capture takes > 2 seconds (R1 violation)
**Symptoms:** `time tt add "test"` returns > 2s

**Quick check (60 sec):**
1. Is Postgres slow? `psql -c "SELECT pg_stat_activity.state FROM pg_stat_activity;"`
2. Is the API process loaded? `ps aux | grep node | grep tasktracker`
3. Network? (localhost should never be the issue)

**Root causes seen:**
- Postgres connection pool exhausted (one slow query starved others)
- Sentry SDK adding 800ms to cold start
- Redis LPUSH timeout

**Recovery:**
1. Restart API: `pm2 restart tasktracker-api`
2. Check pool size in config — bump from 10 to 20 if hot
3. Disable Sentry temporarily if it's the cause: `SENTRY_DSN= npm run start`

### Scenario: Daily digest not sent
**Symptoms:** No email at 8 AM

**Quick check:**
1. Cron ran? `grep digest /var/log/cron.log | tail`
2. Last execution: `npm run digest -- --dry-run`
3. Resend dashboard — errors?

**Recovery:**
1. Manual run: `npm run digest`
2. If `--dry-run` shows 0 tasks → maybe nothing was due (verify with SQL)
3. If Resend 401 → rotate `RESEND_API_KEY`

### Scenario: Postgres connection refused
**Symptoms:** API returns 500 + Sentry alerts

**Quick check:**
1. `pg_isready -h localhost` — is Postgres up?
2. `df -h` — disk full?
3. `psql -c "SELECT count(*) FROM tasks;"` — query works directly?

**Recovery:**
1. Restart Postgres: `brew services restart postgresql` or `systemctl restart postgres`
2. If disk full → archive old `pg_wal` or run `VACUUM FULL` (downtime)
3. If pool exhausted → restart API to reset connections

---

## 🔄 Routine ops

### Deploy a change
```bash
git push  # CI runs tests
ssh prod-host
cd /srv/tasktracker
git pull
npm ci --production
npm run migrate  # if schema changes
pm2 reload tasktracker-api
```

### Rollback
```bash
ssh prod-host
cd /srv/tasktracker
git checkout HEAD~1
npm ci --production
pm2 reload tasktracker-api
# If schema changed: run reverse migration manually
```

### DB backup
Daily cron: `pg_dump tasktracker | gzip > /backups/tt-$(date +%Y%m%d).sql.gz`
Retention: 30 days

### Rotate Resend key
1. Resend dashboard → API Keys → Revoke old + Create new
2. Update 1Password
3. `pm2 restart tasktracker-api` (loads new env)

---

## 📊 Monitoring

- **Sentry** — errors + perf
- **Postgres logs** — slow queries
- **PM2** — process status: `pm2 status`
- **Digest receipt** — I get the daily email = health signal

### Should be green
- [ ] API responding to `GET /healthz`
- [ ] Postgres connections < 80% of pool
- [ ] Resend account in good standing
- [ ] Daily digest received at 8:00 AM ± 5 min

---

## 🔥 Known fires
- None currently. Last incident: 2026-03-04 (Sentry cold start latency — fixed by lazy-load).

## 🤖 Auto-section
<!-- AUTO-START: vault-runbook-refresh -->
_Auto-section not populated yet. Run `vault refresh` to fill._
<!-- AUTO-END: vault-runbook-refresh -->
