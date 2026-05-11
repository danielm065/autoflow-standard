---
type: project-system
project: {{project_name}}
status: hybrid-doc
created: {{date}}
---

# SYSTEM — {{project_name}}

> ארכיטקטורה ומבנה. **חלק auto-generated מ-Arch-Hub**, חלק ידני.
> ידני = "מה הקוד לא מספר" (trade-offs, invariants, integration boundaries).

---

## 🤖 Auto-generated section (אל תערוך ידנית)
<!-- vault-arch-refresh יעדכן את החלק הזה.
     רק "מצביעים" ל-Arch-Hub — לא משכפלים תוכן. -->

הרץ: `vault-arch-refresh --project {{project_name}}` כדי למלא.

### קישורי Arch-Hub
- <!-- e.g., "[[03-Tech-Knowledge/Arch-Hub/automations/{{project_name}}-flow.arch.md]]" -->

### Anatomy (מ-`.wolf/anatomy.md` אם קיים)
<!-- 5 קבצים מרכזיים -->
- 

---

## ✏️ Manual section — מה הקוד לא מספר

### Why this architecture?
<!-- למה בחרנו את ה-stack הזה? trade-offs?
     דוגמה: "n8n ולא Make כי X. Railway ולא Render כי Y." -->


### High-level data flow
<!-- ASCII או mermaid או הסבר טקסטואלי. -->

```
[Trigger] → [Step 1] → [Step 2] → [Output]
```


### Critical invariants
<!-- מה תמיד חייב להיות נכון במערכת.
     דוגמה: "כל message חייב wamid לפני שליחה" -->
- 


### Known limits
<!-- מגבלות מובנות. שובר את ההנחה הזו = בעיה.
     דוגמה: "Meta rate limit 80msg/sec" / "Supabase free tier = 500MB" -->
- 


### Integration boundaries
<!-- איפה אנחנו מסתיימים ומתחיל external service.
     מה אחריותנו, מה לא. -->
- 


### Failure modes
<!-- איך המערכת נכשלת? graceful degradation?
     מה קורה כש-X לא זמין? -->
- 


### Open architectural questions
<!-- לא החלטנו עדיין. נדון בפעם הבאה. -->
- 
