---
description: Show active project STATUS + handoff + compliance check
---

```bash
__SYSTEM_DIR__/bin/vault where-am-i
```

Prints STATUS.md + handoff.md + 11-file Standard compliance for active project (auto-detected from CWD).

After running, summarize for user in 3-5 lines:
1. Project name
2. Current state
3. Next step from handoff
4. Compliance score (X/11) — flag if below 11
