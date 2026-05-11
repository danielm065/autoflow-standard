---
type: project-vision
project: TaskTracker
status: production
created: 2026-02-01
---

# VISION — TaskTracker

## 👤 Customer / user
- **Pays:** myself (internal tool)
- **End-user:** myself
- **Sub-audience:** none (single-user)

## 🎯 Problem being solved
I have tasks scattered across Notes app, sticky notes, Slack DMs to myself, and "remember to..." mental loops. Things slip. Need a single inbox + due-date tracking that I'll actually use because friction is low.

## 💡 Solution in one line
A minimal Node.js + Postgres CLI + web app for capturing tasks in < 2 seconds, with due dates, tags, and a daily digest at 8 AM.

## 📏 Success metric
- **Time to capture:** < 2 seconds from "I should do X" to task in DB (CLI command)
- **Adoption:** I use it for 30 consecutive days
- **Recall accuracy:** 0 missed deadlines in a month

## ⚠️ Out of Scope
- ❌ **No team collaboration** — single user only. If I need a second user, this becomes a different project.
- ❌ **No mobile app** — CLI + web is enough. Mobile = bloat.
- ❌ **No integrations with external services** (Slack, Trello, Asana). This is a standalone tool.
- ❌ **No gamification / streaks / habit tracking.** Just tasks.
- ❌ **No AI-suggested tasks.** Manual input only — I know what I need.
- ❌ **No file attachments.** Text + URLs are enough.

## 👥 Stakeholders
- **Owner + user:** me
- **No external dependencies on team / client**

## 🔒 Constraints
- **Budget:** $0/mo hosting (self-hosted on existing server)
- **Stack:** Node.js (I know it) + Postgres (have running) + Redis (for queue)
- **Time-to-MVP:** 2 weekends
- **Maintenance:** < 1h/month after launch

## 📜 Vision changes (datestamped)
- 2026-02-01 — initial vision (CLI + web, single user)
- 2026-03-15 — added "no AI features" to Out-of-Scope after being tempted to integrate GPT for task estimates (out of scope = preserves focus)
