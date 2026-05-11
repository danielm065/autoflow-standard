---
type: dashboard
purpose: documentation-health
auto_updates: true
tags: [dashboard, autoflow-standard, documentation]
---

# 📊 Documentation Health — AutoFlow Standard

> Cross-project compliance check. Powered by Dataview. **Auto-refreshes** when Obsidian opens.
>
> Convention: every project under `02-Projects/<N>/` needs 11 files. See [HOW-TO-USE-VAULT.md](../HOW-TO-USE-VAULT.md) (or repo `docs/architecture.md`).

---

## 🎯 Active projects

```dataview
TABLE WITHOUT ID
  link(file.link, project) AS "Project",
  client AS "Client",
  status AS "Status",
  last_context_reviewed AS "Last reviewed"
FROM "02-Projects"
WHERE type = "project-home" AND status != "archived"
SORT last_context_reviewed DESC
```

---

## 📋 11-Files Standard Coverage

> Each row = one project. `❌` = file missing. **Goal: all green.**

```dataviewjs
try {
  const required = ["CLAUDE", "VISION", "CONSTITUTION", "ONBOARDING",
                    "SYSTEM", "RUNBOOK", "PROCESS-MAP",
                    "STATUS", "handoff", "decisions", "mistakes"];

  const folders = app.vault.getAllLoadedFiles()
    .filter(f => f.path.startsWith("02-Projects/") && f.children !== undefined)
    .filter(f => f.path.split("/").length === 2)
    .filter(f => !f.name.startsWith("_") && !f.name.startsWith("."));

  if (folders.length === 0) {
    dv.paragraph("⚠️ No projects found under `02-Projects/`.");
  } else {
    const projects = [];
    for (const folder of folders) {
      const row = { Project: folder.name, _score: 0 };
      for (const f of required) {
        const exists = app.vault.getAbstractFileByPath(`${folder.path}/${f}.md`);
        row[f] = exists ? "✅" : "❌";
        if (exists) row._score++;
      }
      projects.push(row);
    }

    projects.sort((a, b) => b._score - a._score || a.Project.localeCompare(b.Project));

    dv.table(
      ["Project", "Score", ...required],
      projects.map(p => [p.Project, `${p._score}/11`, ...required.map(f => p[f])])
    );

    const fullyMigrated = projects.filter(p => p._score === required.length).length;
    dv.paragraph(`**Coverage:** ${fullyMigrated}/${projects.length} projects fully migrated.`);
  }
} catch (e) {
  dv.paragraph(`⚠️ Dashboard error: ${e.message}\n\nRequires Dataview plugin with **JS queries enabled** (Settings → Dataview → Enable JavaScript Queries).`);
}
```

---

## 🆕 Recent decisions (all projects)

```dataview
TABLE WITHOUT ID
  file.link AS "Project",
  file.mtime AS "Last updated"
FROM "02-Projects"
WHERE file.name = "decisions"
SORT file.mtime DESC
LIMIT 10
```

---

## ⏰ STATUS not updated recently (>14 days)

```dataview
TABLE WITHOUT ID
  file.link AS "STATUS",
  file.mtime AS "Last updated",
  (date(today) - file.mtime).days AS "Days stale"
FROM "02-Projects"
WHERE file.name = "STATUS"
  AND (date(today) - file.mtime).days > 14
SORT file.mtime ASC
```

---

## 🔥 Active handoffs

```dataview
TABLE WITHOUT ID
  file.link AS "Project handoff",
  file.mtime AS "Last session",
  (date(today) - file.mtime).days AS "Days ago"
FROM "02-Projects"
WHERE file.name = "handoff"
SORT file.mtime DESC
LIMIT 15
```

---

## 🚀 Quick actions

### New project
1. `Cmd+P` → "Templater: Create new note from template"
2. Choose `Project-Init`
3. Answer 7 questions
4. **Result:** 11 files at `02-Projects/<Name>/`

### Existing project migration
Manual: copy `Templates/_ProjectStandard/*.md` to project folder and fill.

### Refresh auto docs
Terminal: `vault refresh` (or LaunchAgent does it every 5 min automatically)
