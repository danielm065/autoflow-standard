#!/usr/bin/env python3
"""
vault-process-map — refresh PROCESS-MAP.md auto-section.

Reads:
  - 02-Projects/<Name>/automations/*.json (n8n exports)
  - 02-Projects/<Name>/n8n/*.json (drafts/legacy)
  - 02-Projects/<Name>/automations-index.md (purpose enrichment)

Writes:
  - Replaces content between AUTO-START / AUTO-END markers in PROCESS-MAP.md

Stdlib only.
Usage:
  python3 run.py --project <Name> [--vault <path>]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

DEFAULT_VAULT = os.path.expanduser("~/vault")
AUTO_START = "<!-- AUTO-START: vault-process-map -->"
AUTO_END = "<!-- AUTO-END: vault-process-map -->"

TRIGGER_NODE_TYPES = {
    "n8n-nodes-base.webhook": "Webhook",
    "n8n-nodes-base.scheduleTrigger": "Cron",
    "n8n-nodes-base.cron": "Cron",
    "n8n-nodes-base.executeWorkflowTrigger": "Execute Workflow (sub-flow)",
    "n8n-nodes-base.manualTrigger": "Manual",
    "n8n-nodes-base.formTrigger": "Form",
    "n8n-nodes-base.emailTrigger": "Email",
    "@n8n/n8n-nodes-langchain.chatTrigger": "Chat (langchain)",
}


def detect_trigger(nodes: list[dict]) -> str:
    if not nodes:
        return "Unknown (no nodes)"
    # Heuristic: a node with no incoming connections is a trigger.
    # Without connections graph, fall back to position-based + type-based.
    candidates = []
    for node in nodes:
        ntype = node.get("type", "")
        if "Trigger" in ntype or ntype == "n8n-nodes-base.webhook" or ntype == "n8n-nodes-base.cron":
            candidates.append(ntype)
    if not candidates:
        # Often the first node by position is the trigger
        first = nodes[0].get("type", "Unknown")
        return TRIGGER_NODE_TYPES.get(first, first.split(".")[-1] if "." in first else first)
    chosen = candidates[0]
    return TRIGGER_NODE_TYPES.get(chosen, chosen.split(".")[-1] if "." in chosen else chosen)


def parse_workflow_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    nodes = data.get("nodes")
    # Heuristic: real n8n workflow has a non-empty nodes array.
    # Skip product outputs / config JSONs / other non-workflow files.
    if not isinstance(nodes, list) or len(nodes) == 0:
        return None
    name = data.get("name", path.stem)
    wid = data.get("id", "")
    active = data.get("active", None)
    trigger = detect_trigger(nodes)
    return {
        "name": name,
        "id": wid,
        "trigger": trigger,
        "node_count": len(nodes),
        "active": active,
        "file": str(path.relative_to(path.parent.parent)),
    }


def collect_workflows(project_dir: Path) -> list[dict]:
    workflows = []
    seen_ids: set[str] = set()
    # Check both `automations` (plural) and `automation` (singular) — projects vary
    for sub in ("automations", "automation", "n8n"):
        d = project_dir / sub
        if not d.is_dir():
            continue
        for json_file in sorted(d.glob("*.json")):
            wf = parse_workflow_json(json_file)
            if not wf:
                continue
            # Dedupe by ID (some projects have same workflow in multiple folders)
            wid = wf.get("id", "")
            if wid and wid in seen_ids:
                continue
            if wid:
                seen_ids.add(wid)
            workflows.append(wf)
    return workflows


def render_auto_section(workflows: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    out = [AUTO_START, f"## 🤖 Auto-generated (last refresh: {today})", ""]

    if not workflows:
        out.append("_No workflows found in `automations/` or `n8n/`._")
        out.append("")
        out.append(AUTO_END)
        return "\n".join(out)

    # Workflows index table
    out.append("### Workflows index")
    out.append("")
    out.append("| # | Name | Trigger | n8n ID | Nodes | Active | File |")
    out.append("|---|------|---------|--------|-------|--------|------|")
    for i, wf in enumerate(workflows, 1):
        active_str = "✅" if wf["active"] is True else ("❌" if wf["active"] is False else "?")
        wid = wf["id"][:8] + "…" if len(wf["id"]) > 10 else wf["id"]
        wname = wf["name"][:60]
        out.append(
            f"| {i} | {wname} | {wf['trigger']} | `{wid}` | {wf['node_count']} | {active_str} | `{wf['file']}` |"
        )
    out.append("")

    # Triggers breakdown
    out.append("### Triggers breakdown")
    counts = Counter(wf["trigger"] for wf in workflows)
    for trig, n in counts.most_common():
        out.append(f"- **{trig}:** {n}")
    out.append("")

    # Active state breakdown
    active_count = sum(1 for wf in workflows if wf["active"] is True)
    inactive_count = sum(1 for wf in workflows if wf["active"] is False)
    unknown_count = len(workflows) - active_count - inactive_count
    out.append("### Active state")
    out.append(f"- Active: {active_count}")
    out.append(f"- Inactive: {inactive_count}")
    if unknown_count:
        out.append(f"- Unknown: {unknown_count}")
    out.append("")

    out.append(f"_Generated by vault-process-map on {today}._")
    out.append(AUTO_END)
    return "\n".join(out)


def update_process_map(pm_path: Path, new_block: str) -> tuple[bool, str]:
    """Replace AUTO-START..AUTO-END block. Dedupe if multiple. Append if missing."""
    if not pm_path.exists():
        return False, f"PROCESS-MAP.md not found at {pm_path}"

    content = pm_path.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END),
        re.DOTALL,
    )
    matches = list(pattern.finditer(content))

    if matches:
        # Replace FIRST match, REMOVE all duplicates (idempotent across runs)
        parts: list[str] = []
        last_end = 0
        for i, m in enumerate(matches):
            parts.append(content[last_end:m.start()])
            if i == 0:
                parts.append(new_block)
            last_end = m.end()
        parts.append(content[last_end:])
        new_content = "".join(parts)
        dup_n = len(matches) - 1
        action = (
            f"replaced existing block, removed {dup_n} duplicate(s)"
            if dup_n
            else "replaced existing block"
        )
    else:
        sep = "\n\n---\n\n" if not content.endswith("\n") else "\n---\n\n"
        new_content = content.rstrip() + sep + new_block + "\n"
        action = "appended new block (markers were absent)"

    pm_path.write_text(new_content, encoding="utf-8")
    return True, action


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh PROCESS-MAP.md auto-section")
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--vault",
        default=os.environ.get("AUTOFLOW_VAULT", DEFAULT_VAULT),
    )
    args = parser.parse_args()

    vault = Path(args.vault)
    project_dir = vault / "02-Projects" / args.project

    if not project_dir.is_dir():
        print(f"❌ Project not found: {project_dir}", file=sys.stderr)
        return 1

    pm = project_dir / "PROCESS-MAP.md"
    if not pm.exists():
        print(
            f"❌ {args.project} has no PROCESS-MAP.md (not migrated to AutoFlow Standard)",
            file=sys.stderr,
        )
        return 2

    workflows = collect_workflows(project_dir)
    block = render_auto_section(workflows)
    ok, msg = update_process_map(pm, block)
    if not ok:
        print(f"❌ {msg}", file=sys.stderr)
        return 3

    print(f"✅ {args.project}/PROCESS-MAP.md — {msg} ({len(workflows)} workflows indexed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
