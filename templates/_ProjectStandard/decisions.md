---
type: project-decisions
project: {{project_name}}
created: {{date}}
append_only: true
---

# DECISIONS — {{project_name}}

> **Append-only.** לעולם לא למחוק entries. רק להוסיף `Outcome (retrospective):` בעוד שבוע-חודש.
> entries חדשות **בראש** הקובץ (LIFO).

---

## 📋 Template (העתק לכל decision חדשה)

```markdown
## YYYY-MM-DD — <שם קצר של ההחלטה>
**Decision:** <מה הוחלט>
**Why:** <הסיבה / trade-off>
**Alternatives considered:** <מה דחינו ולמה>
**Consequences:** <מה זה גורר>
**Outcome (retrospective):** <נמלא בעוד שבוע-חודש>
```

---

## ✍️ Decisions

<!-- ⬇️ INSERT NEW DECISIONS ABOVE THIS LINE — newest at top (LIFO) ⬇️ -->

## {{date}} — Project initialized
**Decision:** Project structure created using AutoFlow Standard (11-file convention)
**Why:** Standardize documentation across all projects for handoff readiness
**Alternatives considered:** Ad-hoc per-project structure (rejected — drift)
**Consequences:** Every new project follows same pattern; AI agents have predictable context
**Outcome (retrospective):** TBD
