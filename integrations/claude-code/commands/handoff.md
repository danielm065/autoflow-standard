---
description: Read project handoff or append a line for next session
argument-hint: [text — append; empty = read]
---

```bash
__SYSTEM_DIR__/bin/vault handoff "$ARGUMENTS"
```

- No args → print handoff.md
- With text → append timestamped section

If reading: summarize in 3-5 lines.
If appending: confirm what was added + timestamp.

Run at end of session to leave context for next session/agent.
