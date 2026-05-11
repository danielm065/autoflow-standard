# Architecture — Why 11 Files Per Project?

> Counterintuitive answer to an obvious question: "why not just one big README?"

## TL;DR

**1 file = a document.** Good for résumés or blog posts.
**11 files = a system.** Required for AI-readable knowledge bases that update autonomously, load smartly, and survive concurrent edits across 10+ projects.

This is SOLID software design applied to documentation.

## The 11 files

```
02-Projects/<Name>/
│
├── 📝 MANUAL (you write once, rarely change) ───────────────┐
│   ├── CLAUDE.md           # routing card for AI agents    │
│   ├── VISION.md           # why this exists + Out-of-Scope│
│   ├── CONSTITUTION.md     # rules + Why per rule          │
│   └── ONBOARDING.md       # setup + credentials refs      │
│                                                            │
├── 🤖 AUTO-GENERATED (daemon refreshes — do not edit) ─────┤  4 categories,
│   ├── SYSTEM.md           # architecture                  │  not 11 random files
│   ├── RUNBOOK.md          # incident response             │
│   └── PROCESS-MAP.md      # automations / n8n map         │
│                                                            │
├── 📊 SESSION-DRIVEN (hook updates each session) ──────────┤
│   ├── STATUS.md           # current state                 │
│   └── handoff.md          # next-session context          │
│                                                            │
└── 📚 APPEND-ONLY (never deleted — historical record) ─────┘
    ├── decisions.md        # why X was chosen
    └── mistakes.md         # what failed and why
```

## 7 reasons for the split

### 1. Context budget — load only what's relevant

```
Question: "what's the status?"
   1-file:  load 50KB              → expensive
   11-file: load STATUS.md (1KB)   → 50× cheaper

Question: "is X allowed?"
   1-file:  load 50KB              → expensive
   11-file: load CONSTITUTION (3KB) → 16× cheaper

Question: "how is it built?"
   1-file:  load 50KB              → expensive
   11-file: load SYSTEM.md (5KB)   → 10× cheaper
```

A mature project in practice has 18+ files totaling several hundred K estimated tokens. Sessions load **5 files = ~15KB**, not all 18. Token-aware loading is the whole point.

### 2. Manual vs Auto separation — prevents drift

| Source | Files |
|---|---|
| Human writes | VISION, CONSTITUTION, ONBOARDING |
| Daemon generates | SYSTEM (partial), RUNBOOK (partial), PROCESS-MAP (partial) |
| Hook tracks | STATUS, handoff |
| Append-only log | decisions, mistakes |

If everything's in one file, the daemon overwrites human edits. **Catastrophic.** Separation is structural protection.

### 3. Concurrent edits — no merge hell

```
14:30 — Daniel edits VISION
14:31 — daemon refreshes RUNBOOK auto-section
14:32 — Hermes appends to decisions.md from Discord (!decision command)
14:33 — Claude Code edits CONSTITUTION
```

**11 files = 4 writers concurrently, 0 conflicts.**
1 file = merge hell.

### 4. Audience separation — each reader gets what they need

| Reader | What | Why |
|---|---|---|
| Client | VISION | "what am I getting?" |
| New employee | ONBOARDING | "how do I start?" |
| Claude writing code | CONSTITUTION | "what's forbidden?" |
| Hermes at 2 AM | RUNBOOK | "how do I recover?" |
| Project manager | STATUS | "where are we?" |
| Next-session agent | handoff | "what's the next step?" |

In 1 file — everyone loads 50KB and hunts for their 1KB. Slow + expensive.

### 5. Append-only safety

`decisions.md` and `mistakes.md` are **never deleted**. Convention enforced by INSERT markers + CLI logic.

In 1 file — if Claude edits VISION and accidentally cuts an old decision? History lost. Hard to detect.

### 6. Auto-section markers — idempotent rewrite

RUNBOOK and PROCESS-MAP have `<!-- AUTO-START -->...<!-- AUTO-END -->` markers. Daemon replaces only between markers. Manual section untouched.

In 1 file — where do markers go? What's safe to overwrite? Bug-prone.

### 7. Per-file frontmatter — Dataview queries

Each file has YAML frontmatter (`type: project-vision`, `status: draft`, etc.). Enables queries:

```dataview
TABLE status FROM "02-Projects"
WHERE type = "project-vision" AND status = "draft"
```

"Find every project with a draft VISION" — sub-second answer.

In 1 file — Dataview can't query sections within a file. No structured queries.

## Real-world example — mature CPA office automation project

| File | Size | Why this size |
|---|---|---|
| README.md | 4KB | Hub MOC with navigation |
| VISION.md | 3KB | 6 Out-of-Scope items, 4 stakeholders |
| CONSTITUTION.md | 4KB | 8 rules with Why + How-to-apply |
| ONBOARDING.md | 4KB | Setup steps + 5 credentials refs |
| SYSTEM.md | 5KB | Architecture diagram + 8 trade-offs |
| **RUNBOOK.md** | **18KB** | **76 buglog entries auto-loaded** (this is where the magic shows) |
| PROCESS-MAP.md | 2KB | n8n workflow index |
| STATUS.md | 3KB | Open tasks, blockers |
| handoff.md | 2KB | Last-session context |
| decisions.md | 15KB | History of ~12 decisions with full reasoning |
| mistakes.md | 1KB | Template ready, no historical entries |
| **TOTAL** | **~61KB** | |
| anatomy.md (auto file map) | 30KB | 173 files indexed |

If this were 1 file = 91KB monolith. Claude's 200K context loads it 2× before exhausting budget. Multiple projects in same session = impossible.

11 files = load 5 (15KB) per session, on-demand load others. Stays within budget for 10+ projects in same session.

## The OpenWolf comparison

OpenWolf has a similar concept (anatomy.md + cerebrum.md + memory.md + buglog.json) but **vault-wide**, not per-project. Result:
- One anatomy.md for 14 projects = noisy
- One cerebrum for everyone = collision-prone
- In practice: only anatomy.md actually fills with content. Others stay empty.

AutoFlow Standard learned from this:
- Same concepts (file map, learnings, log, bug log)
- **Per-project scope**
- **Idempotent auto-refresh**
- **Markers protect manual sections**
- **Append-only enforcement**

Result: 7 active projects @ 11/11 compliance, daemon running autonomously, real data in every file.

## When to use this

✅ **Use AutoFlow Standard if:**
- 3+ active projects you maintain in parallel
- Multiple AI agents (Claude/Codex/Hermes) need consistent context
- You want documentation to update without manual effort
- You want to hand off projects to employees without long onboarding

❌ **Skip if:**
- Single short-lived project (a tutorial, a sketch)
- Solo dev with no AI tooling
- Documentation isn't the bottleneck

## When NOT to add a 12th file

The 11 files cover the dimensions: **what / how / why / when / who / scope / state / log of choices / log of failures**. Adding more = scope creep.

If you need something specific (e.g., "billing.md"), put it as a working doc inside the project folder — but don't require it in the Standard.

## Further reading

- [Comparison: AutoFlow Standard vs OpenWolf vs single-file](comparison.md)
- [Getting started](getting-started.md)
- [vault CLI reference](concepts/vault-cli.md)
