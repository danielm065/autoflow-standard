#!/usr/bin/env python3
"""
vault-anatomy-refresh — auto-scan project folder, generate file-level map.

Output: 02-Projects/<Name>/.anatomy.md
  - One line per file with: name, ~tokens, first non-empty line as description
  - Excluded: .DS_Store, .git, _legacy, secrets/, very large binaries
  - Idempotent — overwrites existing .anatomy.md

Borrowed from OpenWolf's anatomy.md concept but per-project + faster.

Usage:
  python3 run.py --project <Name> [--vault <path>]
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_VAULT = os.path.expanduser("~/vault")
EXCLUDE_DIRS = {".git", ".DS_Store", "_legacy", "secrets", "node_modules", "__pycache__", ".venv", "venv"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".log", ".lock"}
BINARY_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".docx", ".xlsx", ".zip", ".tar", ".gz", ".mp4", ".webp"}
MAX_FILE_BYTES_FOR_DESC = 1024 * 1024  # 1MB cap on description extraction


def estimate_tokens(text_bytes: int) -> int:
    """Very rough estimate: 1 token ≈ 3 bytes (Hebrew/UTF-8 heavy).
    For pure English use ≈4 bytes/token. We err toward more tokens (safer for budget).
    """
    return text_bytes // 3


def get_description(path: Path) -> str:
    """Extract first meaningful line as description. Skips frontmatter blocks."""
    if path.suffix.lower() in BINARY_EXTS:
        return f"(binary, {path.suffix})"
    try:
        size = path.stat().st_size
    except OSError:
        return "(unreadable)"
    if size == 0:
        return "(empty)"
    if size > MAX_FILE_BYTES_FOR_DESC:
        return f"(large file, {size // 1024}KB)"
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            in_frontmatter = False
            frontmatter_seen = False
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                # Frontmatter handling: --- ... --- block at top
                if stripped == "---":
                    if not frontmatter_seen:
                        in_frontmatter = True
                        frontmatter_seen = True
                        continue
                    elif in_frontmatter:
                        in_frontmatter = False
                        continue
                if in_frontmatter:
                    continue
                # Skip shebangs
                if stripped.startswith("#!"):
                    continue
                # Strip leading markdown heading marks
                if stripped.startswith("#"):
                    stripped = stripped.lstrip("# ").strip()
                # Skip blockquote markers
                if stripped.startswith(">"):
                    stripped = stripped.lstrip("> ").strip()
                # Strip leading comment markers
                for comment in ("//", "/*", "*", "<!--"):
                    if stripped.startswith(comment):
                        stripped = stripped[len(comment):].strip()
                        # Strip trailing comment closer
                        for closer in ("-->", "*/"):
                            if stripped.endswith(closer):
                                stripped = stripped[:-len(closer)].strip()
                        break
                if stripped and len(stripped) > 2:
                    return stripped[:80]
    except (UnicodeDecodeError, PermissionError):
        return "(binary or unreadable)"
    return "(no description)"


def walk_project(project_dir: Path) -> list[dict]:
    """Walk project dir, return file metadata sorted by relative path."""
    entries = []
    for root, dirs, files in os.walk(project_dir):
        # Filter excluded dirs in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        root_path = Path(root)
        rel_root = root_path.relative_to(project_dir)
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            ext = Path(fname).suffix.lower()
            if ext in EXCLUDE_EXTS:
                continue
            fpath = root_path / fname
            try:
                size = fpath.stat().st_size
            except OSError:
                continue
            rel_path = rel_root / fname if str(rel_root) != "." else Path(fname)
            entries.append(
                {
                    "rel_path": str(rel_path),
                    "size": size,
                    "tokens": estimate_tokens(size),
                    "description": get_description(fpath),
                    "ext": ext,
                }
            )
    return entries


def render_anatomy(project: str, entries: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_tokens = sum(e["tokens"] for e in entries)
    out = [
        "---",
        "type: project-anatomy",
        f"project: {project}",
        f"last_scanned: {today}",
        f"file_count: {len(entries)}",
        f"rough_token_estimate: {total_tokens}",
        "auto_generated: true",
        "---",
        "",
        f"# Anatomy — {project}",
        "",
        "> **Auto-maintained** by `vault-anatomy-refresh`. אל תערוך ידנית.",
        f"> Last scanned: {today}. Files: {len(entries)}. Rough token estimate: ~{total_tokens:,} (bytes/3, UTF-8/Hebrew aware).",
        "",
        "Use this map to **decide which files to read** without opening them all.",
        "",
        "## Files",
        "",
    ]

    # Group by directory for readability
    current_dir = None
    for e in entries:
        rel = Path(e["rel_path"])
        d = str(rel.parent) if str(rel.parent) != "." else "(root)"
        if d != current_dir:
            out.append(f"\n### {d}/")
            current_dir = d
        size_kb = e["size"] / 1024
        size_str = f"{size_kb:.1f}KB" if size_kb >= 1 else f"{e['size']}B"
        out.append(
            f"- `{rel.name}` ({size_str}, ~{e['tokens']} tok est) — {e['description']}"
        )

    out.append("")
    out.append(f"_Generated by vault-anatomy-refresh on {today}._")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-generate per-project anatomy.md")
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

    entries = walk_project(project_dir)
    content = render_anatomy(args.project, entries)
    out_path = project_dir / ".anatomy.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"✅ {args.project}/.anatomy.md — {len(entries)} files scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
