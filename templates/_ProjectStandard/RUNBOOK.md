---
type: project-runbook
project: {{project_name}}
created: {{date}}
---

# RUNBOOK — {{project_name}}

> מה לעשות כש-X. מבוסס על mistakes.md + buglog + production incidents.
> חלק auto-generated מ-`.wolf/buglog.json`.

---

## 🚨 Incident Response

### תרחיש: <!-- e.g., "Workflow X stopped firing" -->
**Symptoms:** <!-- מה המשתמש/לקוח רואה -->

**Quick check (60 sec):**
1. <!-- בדיקה ראשונה -->
2. 
3. 

**Root causes seen:**
- <!-- סיבה → תיקון -->

**Recovery steps:**
1. 
2. 
3. 

**How to verify recovery:**
- 

---

## 🔄 Routine ops

### Deploy a change
1. 

### Rollback last deploy
1. 

### Restart services
1. 

### Rotate credentials
1. 

---

## 📊 Monitoring & alerts
<!-- איפה לבדוק שהמערכת חיה? -->

- **Dashboard:** 
- **Alert channels:** <!-- Discord channel? email? -->
- **Health check endpoint:** 

### מה צריך להיות ירוק
- [ ] 
- [ ] 

---

## 🔥 Known fires (active workarounds)
<!-- בעיות פתוחות שיש להן workaround עד שיתוקנו. -->

- <!-- "X לא עובד אם Y → workaround: Z" -->

---

<!-- vault-runbook-refresh ימלא את החלק הזה ממקרים שכבר נפתרו.
     לא לערוך בין markers — נכתב מחדש בכל refresh.
     הרץ: `vault refresh` (או ישיר: python3 04-OpenClaw/Skills/vault-runbook-refresh/run.py --project {{project_name}}) -->

<!-- AUTO-START: vault-runbook-refresh -->
_Auto-section לא הופעל עדיין. הרץ `vault refresh` למלא._
<!-- AUTO-END: vault-runbook-refresh -->
