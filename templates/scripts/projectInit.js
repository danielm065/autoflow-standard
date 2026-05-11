/**
 * AutoFlow — projectInit.js
 *
 * Templater user script. Scaffolds a new project under 02-Projects/<Name>/
 * by asking 7 questions and instantiating 11 standard files.
 *
 * Invoked by Templates/Project-Init.md (trigger template).
 *
 * Files created:
 *   CLAUDE.md, VISION.md, CONSTITUTION.md, ONBOARDING.md,
 *   SYSTEM.md, RUNBOOK.md, PROCESS-MAP.md,
 *   STATUS.md, handoff.md, decisions.md, mistakes.md
 *
 * Reads skeletons from: Templates/_ProjectStandard/<name>.md
 * Substitutes: {{project_name}}, {{client_name}}, {{date}},
 *              {{description}}, {{stack}}, {{vision_why}},
 *              {{success_metric}}, {{out_of_scope}}
 *
 * Hardening (2026-05-10 rev2):
 *   - try/catch around all I/O
 *   - cancel detection (null from prompt → abort cleanly)
 *   - instanceof TFile check before app.vault.read
 *   - rollback: delete created folder if any file fails midway
 *   - rich error messages with which-step-failed info
 */

async function projectInit(tp) {
  const TEMPLATE_FOLDER = "Templates/_ProjectStandard";
  const PROJECTS_ROOT = "02-Projects";
  const TEMPLATE_FILES = [
    "CLAUDE",
    "VISION",
    "CONSTITUTION",
    "ONBOARDING",
    "SYSTEM",
    "RUNBOOK",
    "PROCESS-MAP",
    "STATUS",
    "handoff",
    "decisions",
    "mistakes",
  ];

  // Helper: detect cancellation (user pressed Esc).
  // Templater returns null/undefined on cancel. Empty string = user typed nothing but pressed Enter.
  const cancelled = (v) => v === null || v === undefined;

  // Helper: detect TFile (vs TFolder). TFolder has .children property.
  const isFile = (f) => f && typeof f.path === "string" && f.children === undefined;

  // 1. Gather inputs
  let inputs;
  try {
    const projectName = await tp.system.prompt("Project name (English, no spaces)?");
    if (cancelled(projectName) || !projectName.trim()) {
      return "❌ Cancelled — no project name provided.";
    }
    const safeName = projectName.trim().replace(/\s+/g, "-");

    const askOrCancel = async (q, def = "") => {
      const v = await tp.system.prompt(q, def);
      if (cancelled(v)) return null;
      return v;
    };

    const clientName = await askOrCancel("Client display name (Hebrew OK)?");
    if (cancelled(clientName)) return `❌ Cancelled at step 2 (client name). Project "${safeName}" not created.`;

    const description = await askOrCancel("One-line description?");
    if (cancelled(description)) return `❌ Cancelled at step 3 (description). Project "${safeName}" not created.`;

    const stack = await askOrCancel("Stack (e.g., n8n + Railway + Supabase)?");
    if (cancelled(stack)) return `❌ Cancelled at step 4 (stack). Project "${safeName}" not created.`;

    const visionWhy = await askOrCancel("Why does this project exist? (1-2 sentences)");
    if (cancelled(visionWhy)) return `❌ Cancelled at step 5 (vision). Project "${safeName}" not created.`;

    const successMetric = await askOrCancel("Success metric? (number if possible)");
    if (cancelled(successMetric)) return `❌ Cancelled at step 6 (metric). Project "${safeName}" not created.`;

    const outOfScope = await askOrCancel("What's OUT of scope? (comma separated)");
    if (cancelled(outOfScope)) return `❌ Cancelled at step 7 (out of scope). Project "${safeName}" not created.`;

    inputs = {
      project_name: safeName,
      client_name: clientName,
      description: description,
      stack: stack,
      vision_why: visionWhy,
      success_metric: successMetric,
      out_of_scope: outOfScope,
      date: tp.date.now("YYYY-MM-DD"),
    };
  } catch (e) {
    return `❌ Error gathering inputs: ${e.message}`;
  }

  const folderPath = `${PROJECTS_ROOT}/${inputs.project_name}`;

  // 2. Folder check
  if (app.vault.getAbstractFileByPath(folderPath)) {
    return `❌ Project "${inputs.project_name}" already exists at ${folderPath}.\n\nFor existing projects, use manual migration (copy files from Templates/_ProjectStandard/).`;
  }

  // 3. Pre-validate all template files exist before creating anything
  const missingTemplates = [];
  for (const name of TEMPLATE_FILES) {
    const tplPath = `${TEMPLATE_FOLDER}/${name}.md`;
    const tplFile = app.vault.getAbstractFileByPath(tplPath);
    if (!tplFile) {
      missingTemplates.push(tplPath);
    } else if (!isFile(tplFile)) {
      missingTemplates.push(`${tplPath} (not a file?)`);
    }
  }
  if (missingTemplates.length > 0) {
    return `❌ Missing/invalid templates:\n${missingTemplates.map((p) => `  - ${p}`).join("\n")}\n\nProject NOT created. Restore templates first.`;
  }

  // 4. Create folder
  try {
    await app.vault.createFolder(folderPath);
  } catch (e) {
    return `❌ Failed to create folder ${folderPath}: ${e.message}`;
  }

  // 5. Substitution helper
  const fillTemplate = (content) => {
    let out = content;
    for (const [k, v] of Object.entries(inputs)) {
      const re = new RegExp(`\\{\\{${k}\\}\\}`, "g");
      out = out.replace(re, v);
    }
    return out;
  };

  // 6. Read each skeleton, fill, write — with rollback on failure
  const created = [];
  let failure = null;
  for (const name of TEMPLATE_FILES) {
    const tplPath = `${TEMPLATE_FOLDER}/${name}.md`;
    const tplFile = app.vault.getAbstractFileByPath(tplPath);
    try {
      const tplContent = await app.vault.read(tplFile);
      const filled = fillTemplate(tplContent);
      const targetPath = `${folderPath}/${name}.md`;
      await app.vault.create(targetPath, filled);
      created.push(name);
    } catch (e) {
      failure = { step: name, error: e.message };
      break;
    }
  }

  // 7. Rollback on failure
  if (failure) {
    const failureLog = [];
    for (const name of created) {
      try {
        const f = app.vault.getAbstractFileByPath(`${folderPath}/${name}.md`);
        if (f) await app.vault.delete(f);
      } catch (e) {
        failureLog.push(`could not delete ${name}.md: ${e.message}`);
      }
    }
    try {
      const folder = app.vault.getAbstractFileByPath(folderPath);
      if (folder) await app.vault.delete(folder, true);
    } catch (e) {
      failureLog.push(`could not delete folder: ${e.message}`);
    }
    return [
      `❌ FAILED at step ${failure.step}.md`,
      `Error: ${failure.error}`,
      "",
      `Rolled back: deleted ${created.length} files + folder ${folderPath}`,
      ...(failureLog.length > 0 ? ["", "⚠️ Rollback issues:", ...failureLog.map((l) => `  - ${l}`)] : []),
    ].join("\n");
  }

  // 8. Success report
  const lines = [
    `# ✅ Project Scaffolded — ${inputs.project_name}`,
    "",
    `Created at: \`${folderPath}/\``,
    `Date: ${inputs.date}`,
    "",
    "## Files created (11/11)",
    ...created.map((f) => `- [x] ${f}.md`),
    "",
    "## Inputs received",
    `- **Client:** ${inputs.client_name || "(empty)"}`,
    `- **Description:** ${inputs.description || "(empty)"}`,
    `- **Stack:** ${inputs.stack || "(empty)"}`,
    `- **Vision Why:** ${inputs.vision_why || "(empty)"}`,
    `- **Success Metric:** ${inputs.success_metric || "(empty)"}`,
    `- **Out of Scope:** ${inputs.out_of_scope || "(empty)"}`,
    "",
    "## Next steps",
    `1. Open [[${folderPath}/CLAUDE]] — project routing`,
    `2. Open [[${folderPath}/VISION]] — verify auto-filled details`,
    `3. Open [[${folderPath}/CONSTITUTION]] — add project-specific rules`,
    `4. Open [[${folderPath}/ONBOARDING]] — fill credentials refs + setup steps`,
    "",
    "> This scratch file (the report you're reading) can be deleted.",
  ];

  return lines.join("\n");
}

module.exports = projectInit;
