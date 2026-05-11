---
description: Append project decision (date-stamped) to active project's decisions.md
argument-hint: <decision text — what was decided>
---

Run the vault CLI to log this decision:

```bash
__SYSTEM_DIR__/bin/vault decision "$ARGUMENTS"
```

CLI auto-detects active project from CWD (must be inside `__AUTOFLOW_VAULT__/02-Projects/<Name>/`).

After running:
1. Show the appended entry from output
2. If entry has TODO placeholders for **Why** / **Alternatives**, prompt user to fill or note 24h deadline
3. Confirm file location
