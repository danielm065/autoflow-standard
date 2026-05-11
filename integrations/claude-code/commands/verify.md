---
description: Verify AutoFlow Standard compliance + secrets scan
argument-hint: [project name — optional, default: all]
---

```bash
__SYSTEM_DIR__/bin/vault verify "$ARGUMENTS"
```

If empty → scans all projects. With name → that project + heuristic secrets scan.

After running:
1. Top-line "X/N projects fully migrated"
2. List projects below 11/11 with what's missing
3. If secrets scan flags → CRITICAL: rotate immediately + show specific lines
