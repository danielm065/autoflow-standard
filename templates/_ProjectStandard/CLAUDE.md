---
type: project-routing
project: {{project_name}}
client: {{client_name}}
created: {{date}}
---

# {{project_name}} — Project Routing

> טוען בתחילת סשן. routing מהיר ל-AI agents (Claude / Codex / Hermes).

## Load order — תחילת סשן (חובה)
1. [VISION.md](VISION.md) — למה הפרויקט קיים
2. [CONSTITUTION.md](CONSTITUTION.md) — חוקים לא לעבור
3. [STATUS.md](STATUS.md) — איפה עצרנו
4. [handoff.md](handoff.md) — next step

## On demand
| תרחיש | קובץ |
|---|---|
| שאלת ארכיטקטורה | [SYSTEM.md](SYSTEM.md) |
| באג / קריסה | [RUNBOOK.md](RUNBOOK.md) |
| setup ראשוני / credentials | [ONBOARDING.md](ONBOARDING.md) |
| "למה החלטנו X?" | [decisions.md](decisions.md) |
| "מה לא לחזור עליו?" | [mistakes.md](mistakes.md) |
| automations / n8n | [PROCESS-MAP.md](PROCESS-MAP.md) |

## חוקי vault גלובליים (תזכורת)
- Hebrew UI, English code, full absolute paths
- `decisions.md` + `mistakes.md` = **append-only**
- Auto-generated (`SYSTEM` partial, `RUNBOOK` partial, `PROCESS-MAP`) — אל תערוך ידנית
- Master = `/Users/danielworkspace/AutoFlow-Vault/`. Mirror (GoogleDrive) read-only.
