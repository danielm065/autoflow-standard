---
description: Refresh auto-generated docs for active project
---

```bash
__SYSTEM_DIR__/bin/vault refresh
```

Invokes:
- `vault-runbook-refresh` — RUNBOOK auto-section from buglog + issues.md
- `vault-process-map` — PROCESS-MAP from automations
- `vault-anatomy-refresh` — per-project file map

After running:
1. Report which skills ran successfully
2. Note any errors
3. Show final compliance score
