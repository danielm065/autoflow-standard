# Example Project — TaskTracker

This directory contains a **fully filled-out** AutoFlow Standard project for reference. It's not a real client project; it's a fictional "TaskTracker" CLI + web app — small enough to fit in your head, real-looking enough to teach.

## Read in this order

1. **[CLAUDE.md](CLAUDE.md)** — routing card (the entry point)
2. **[VISION.md](VISION.md)** — why this project exists + 6 Out-of-Scope items
3. **[CONSTITUTION.md](CONSTITUTION.md)** — 7 rules, each with Why
4. **[ONBOARDING.md](ONBOARDING.md)** — 30-min setup
5. **[SYSTEM.md](SYSTEM.md)** — architecture, trade-offs, failure modes
6. **[RUNBOOK.md](RUNBOOK.md)** — 3 incident scenarios + routine ops
7. **[PROCESS-MAP.md](PROCESS-MAP.md)** — flow diagram + schedule
8. **[STATUS.md](STATUS.md)** — current state of a 3-month-old production project
9. **[handoff.md](handoff.md)** — what last session said
10. **[decisions.md](decisions.md)** — 5 chronological decisions with reasoning
11. **[mistakes.md](mistakes.md)** — 3 failures with root causes (LIFO order)

## What this example teaches

| Lesson | Where to see it |
|---|---|
| How VISION's "Out of Scope" prevents feature creep | VISION.md (6 items) → decisions.md 2026-03-15 + mistakes.md 2026-04-10 |
| How CONSTITUTION rules with "Why" stay relevant | CONSTITUTION.md R1 (< 2s capture) → enforced in mistakes.md 2026-03-04 (Sentry cold-start) |
| How RUNBOOK scenarios mirror real incidents | RUNBOOK.md "Capture takes > 2s" → matches mistakes.md Sentry incident |
| How handoff.md works as a baton | handoff.md "Where I stopped" + "Next step" structure |
| Decision logs are FIFO (oldest first) with `<!-- INSERT -->` at bottom | decisions.md |
| Mistakes logs are LIFO (newest first) with `<!-- INSERT -->` at top | mistakes.md |
| When AUTO-START/END blocks appear | RUNBOOK.md + PROCESS-MAP.md (markers present, daemon would fill) |

## Use this as a copy-paste reference

When scaffolding your real project (via Templater or manually), reference how the 11 files connect:

- **VISION** declares Out-of-Scope → **CONSTITUTION** enforces rules to keep VISION true → **mistakes.md** records violations and what was learned
- **SYSTEM** describes architecture → **RUNBOOK** describes what to do when it breaks
- **STATUS** is the current state → **handoff** is the bridge to the next session
- **decisions** is the immutable record of "why we chose this"

The 11 files form a **cohesive narrative**, not a random folder of docs.

## Anti-pattern: don't copy this exact project

The point of the example is **structure**, not content. Your project will have different rules, different stack, different Out-of-Scope. Copy the **shape**, write your own substance.
