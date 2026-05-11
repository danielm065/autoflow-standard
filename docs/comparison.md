# Comparison: AutoFlow Standard vs Alternatives

> Honest comparison. AutoFlow Standard isn't always the right tool.

## Side-by-side

| Capability | Single big README | Notion/Confluence | OpenWolf | AutoFlow Standard |
|---|---|---|---|---|
| **Markdown source** | ✅ | ❌ (proprietary) | ✅ | ✅ |
| **AI agent context** | 50KB blob | API-fetched | per-vault | per-project, smart loading |
| **Multi-agent unified** | N/A | N/A | Claude only | Claude + Codex + Hermes + CLI |
| **Auto-refresh from code** | ❌ | ❌ | partial | ✅ (3 skills + daemon) |
| **Concurrent edit safety** | merge hell | locks | unclear | markers + INSERT logic |
| **Append-only enforcement** | ❌ | manual | ❌ | ✅ |
| **Out-of-scope tracking** | ❌ | manual | ❌ | ✅ (VISION.md required) |
| **Constitution per project** | ❌ | manual | ❌ | ✅ (with Why per rule) |
| **Secrets leak detection** | ❌ | ❌ | ❌ | ✅ (heuristic scan) |
| **Discord remote control** | ❌ | ❌ | ❌ | ✅ via Hermes |
| **Dashboard compliance** | ❌ | manual | ❌ | ✅ Dataview |
| **macOS LaunchAgent** | N/A | N/A | scripted | ✅ |
| **Hebrew + English** | depends | ✅ | English | ✅ first-class |
| **Setup effort** | 0 min | 1 hour | 30 min | 30 min |
| **Vendor lock-in** | none | full | none | none |
| **Cost** | free | $8-30/mo | free | free |

## Detailed: OpenWolf

**OpenWolf** is the closest competitor — same Markdown-in-vault philosophy.

### Where OpenWolf wins

| Feature | OpenWolf | AutoFlow Standard |
|---|---|---|
| **anatomy.md auto-scan** | ✅ vault-wide | ✅ per-project (we adopted this) |
| **Single config file** | ✅ `.wolf/OPENWOLF.md` | ❌ scattered (intentional for SRP) |
| **Cron daemon model** | ✅ designed in | ✅ adopted (LaunchAgent) |

### Where AutoFlow Standard wins

| Feature | OpenWolf | AutoFlow Standard |
|---|---|---|
| **In practice — has content** | 95% empty | 50% projects active |
| **Per-project scope** | ❌ vault-wide | ✅ per-project |
| **Cross-agent (Claude/Codex/Hermes)** | Claude-only | ✅ all 3 + Discord |
| **Out-of-Scope first-class** | ❌ | ✅ VISION required |
| **Why per rule** | ❌ | ✅ CONSTITUTION required |
| **Auto-section markers** | ❌ | ✅ idempotent refresh |
| **Templater scaffolder** | ❌ | ✅ 7-question interactive |
| **Dataview dashboard** | ❌ | ✅ |
| **Token leak detection** | ❌ | ✅ |
| **Hebrew first-class** | ❌ | ✅ |

### The honest take

OpenWolf is **vaporware-operational**: great design, no users filled it. Sample audit:
- `cerebrum.md`: 0 entries
- `memory.md`: 4 lines
- `buglog.json`: 2 entries
- `anatomy.md`: ✅ actually works (576 files indexed)

AutoFlow Standard borrowed the **one thing that works** (anatomy auto-scan) and built around the missing pieces.

## Detailed: Notion/Confluence

### Where Notion wins
- Polished UI, drag-and-drop blocks
- Mobile app first-class
- Permissions per-page
- Embedded media (videos, Figma)

### Where AutoFlow Standard wins
- **Markdown source = git-tracked + grep-able + AI-context-friendly**
- No vendor lock-in
- $0/month
- Works offline
- Daemon-driven autonomy not possible in Notion (no shell access)
- AI agents can directly read/write (no API roundtrip)

### When to use which
- **Notion**: client-facing docs, embedded media-heavy, non-technical team
- **AutoFlow Standard**: technical projects, AI-driven workflow, solo or technical team, cost-sensitive

## Detailed: Single big README.md

### When this works
- Single project
- Short-lived (sprint duration)
- No automation needed
- One reader (you)

### When this breaks
- 3+ projects → which README has the answer?
- Multiple AI agents → all load 50KB on every query
- Long-running project → README grows to 100KB+, becomes unmaintainable
- Team growth → onboarding is "read 50KB and ask questions"
- Audit trail → who decided what, when? Hard to extract.

## Detailed: Linear/Trello/Jira/Asana

Different category — these are **task management**, not documentation.

AutoFlow Standard is **documentation-as-code**. They complement:
- Linear = tracks tasks (what to do next)
- AutoFlow Standard = tracks knowledge (why we did it, what works, what doesn't)

Use both. STATUS.md per project can link to Linear sprint board.

## Decision matrix

```
                    │ AutoFlow Standard │ Notion │ OpenWolf │ Single README │
1 project, solo     │       🟢          │   🟡   │    🟢    │      🟢       │
3-10 projects, solo │       🟢🟢        │   🟢   │    🟡    │      🔴       │
10+ projects        │       🟢🟢🟢      │   🟢   │    🔴    │      🔴       │
Team with mobile UX │       🟡          │   🟢   │    🟡    │      🔴       │
AI-heavy workflow   │       🟢🟢🟢      │   🟡   │    🟡    │      🔴       │
Solo + Hebrew + AI  │       🟢🟢🟢      │   🟡   │    🟡    │      🔴       │
Cost-sensitive      │       🟢          │   🔴   │    🟢    │      🟢       │
```

## Migration paths

### From OpenWolf → AutoFlow Standard
1. Run installer (preserves `.wolf/anatomy.md` if exists)
2. Daemon will read `.wolf/buglog.json` automatically → populates RUNBOOK
3. Move per-project content into 11-file structure manually (or via scaffolder for new projects)
4. Keep `.wolf/anatomy.md` (useful) — disable OpenWolf protocol loader in CLAUDE.md (frees ~7KB per session)

### From single README → AutoFlow Standard
1. Run Project-Init scaffolder
2. Copy README content into VISION.md (vision parts) + SYSTEM.md (technical) + ONBOARDING.md (setup)
3. Move decisions to decisions.md
4. Done.

### From Notion → AutoFlow Standard
1. Export Notion to Markdown
2. Run Project-Init for each project
3. Paste Notion content into appropriate of the 11 files
4. Daemon picks up
