---
description: Append project mistake (date-stamped) to active project's mistakes.md
argument-hint: <mistake text — what was tried + what failed>
---

```bash
__SYSTEM_DIR__/bin/vault mistake "$ARGUMENTS"
```

CLI auto-detects active project. After running:
1. Show entry from output
2. Help fill TODO placeholders (Tried/Result/Why-it-failed/Better-approach) from conversation context if obvious
3. Confirm file location
