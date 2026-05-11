# Obsidian Setup (AutoFlow Standard)

> Required Obsidian community plugins + setup steps for Templater + Dataview + (optional) QuickAdd.

## Required plugins

Install via **Settings → Community Plugins → Browse**:

| Plugin | Purpose | Required? |
|---|---|---|
| **Templater** | Project-Init scaffolder (7 questions → 11 files) | ✅ Required |
| **Dataview** | Documentation-Health dashboard queries | ✅ Required |
| **QuickAdd** | Hotkey-driven capture (Cmd+D decision, Cmd+M mistake, etc.) | 🟡 Recommended |
| **Calendar** | Daily Notes integration | 🟢 Optional |

## After installing plugins

### Templater

1. Settings → Templater
2. **Template folder location:** `Templates`
3. **Enable user scripts folder:** `Templates/scripts`
4. **Enabled templates hotkeys:** Add `Templates/Project-Init.md`
5. Settings → Hotkeys → search "Templater: Project-Init" → bind to `Cmd+Shift+N` (or any)

### Dataview

1. Settings → Dataview
2. **Enable JavaScript Queries:** ON (required for `Documentation-Health.md`)
3. **Enable Inline JavaScript Queries:** ON

### QuickAdd (optional, recommended)

See [QuickAdd-setup.md](../../templates/QuickAdd-setup.md) (TODO) for 5 hotkey macros:
- `Cmd+D` → Decision
- `Cmd+M` → Mistake
- `Cmd+N` → Quick note
- `Cmd+S` → Status update
- `Cmd+H` → Handoff write

## Verify setup

1. Open `00-Dashboard/Documentation-Health.md` → Dataview tables should render
2. `Cmd+P` → "Templater: Create new note from template" → see `Project-Init` in list
3. Run Project-Init on a test project → verify 11 files created

## Mobile sync

If using Obsidian on iPad/iPhone:
- Daniel's setup: vault lives on local Mac + GoogleDrive mirror for mobile sync
- Mobile clients read from GoogleDrive mirror
- Edits flow back to Mac master via GoogleDrive client sync
- **Caveat:** `vault` CLI and daemon run on Mac only. Mobile edits propagate up via GDrive, then daemon refreshes on Mac.

Alternative: Obsidian Sync ($8/mo) — first-party, no GDrive needed.

## Templater syntax used

`projectInit.js` uses:
- `tp.system.prompt(question, default)` — modal input dialogs
- `tp.date.now("YYYY-MM-DD")` — date stamps
- `app.vault.createFolder(path)` — folder creation
- `app.vault.create(path, content)` — file creation
- `app.vault.delete(file)` — rollback on partial failure

Standard Obsidian API — no extra dependencies.
