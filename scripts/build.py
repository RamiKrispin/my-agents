#!/usr/bin/env python3
"""Generate tool-native layouts from the neutral source/ tree.

Source of truth lives in `source/`. Running this script compiles it into:

  - .claude-plugin/marketplace.json   Claude Code marketplace manifest
  - plugins/<name>/...                Claude Code plugins (agents, commands, skills)
  - .opencode/agent/*.md              opencode agents (remapped frontmatter)
  - .opencode/command/*.md            opencode commands
  - opencode.json                     minimal opencode config

Everything it writes is GENERATED — edit `source/`, not the output.

Zero external dependencies: a small parser handles the constrained YAML subset
used in source files (flat scalars + inline `[a, b, c]` lists).

Usage:
    python3 scripts/build.py            # regenerate all outputs
    python3 scripts/build.py --check    # fail if outputs are stale (CI)
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
SRC_PLUGINS = SOURCE / "plugins"

# Output locations (regenerated wholesale on every run).
CLAUDE_PLUGIN_DIR = ROOT / ".claude-plugin"
CLAUDE_PLUGINS_OUT = ROOT / "plugins"
OPENCODE_DIR = ROOT / ".opencode"
OPENCODE_CONFIG = ROOT / "opencode.json"

# Neutral (lowercase) tool name -> Claude Code tool name.
NEUTRAL_TO_CC = {
    "read": "Read",
    "write": "Write",
    "edit": "Edit",
    "bash": "Bash",
    "grep": "Grep",
    "glob": "Glob",
    "list": "LS",
    "webfetch": "WebFetch",
    "websearch": "WebSearch",
    "task": "Task",
    "todowrite": "TodoWrite",
}

# The universe of opencode tools. A neutral allow-list is emulated in opencode by
# enabling listed tools and disabling the rest.
OPENCODE_TOOLS = [
    "read", "write", "edit", "bash", "grep", "glob",
    "list", "patch", "webfetch", "todowrite", "todoread", "task",
]


# --------------------------------------------------------------------------- #
# Minimal YAML-subset parser
# --------------------------------------------------------------------------- #
def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _parse_scalar(value: str):
    """Parse a single source value: inline list `[a, b]` or a scalar string."""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_unquote(item) for item in inner.split(",") if item.strip()]
    return _unquote(value)


def parse_block(text: str) -> dict:
    """Parse a flat `key: value` block (one pair per line, # comments allowed)."""
    data: dict = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = _parse_scalar(value)
    return data


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a markdown file into (frontmatter dict, body)."""
    text = text.lstrip("﻿")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta = parse_block("\n".join(lines[1:end]))
    body = "\n".join(lines[end + 1:]).lstrip("\n")
    return meta, body


# --------------------------------------------------------------------------- #
# Rendering helpers
# --------------------------------------------------------------------------- #
def _dq(value: str) -> str:
    """Double-quote a scalar for safe YAML frontmatter output."""
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_frontmatter(pairs: list[tuple[str, str]], body: str) -> str:
    lines = ["---"]
    lines.extend(f"{key}: {value}" for key, value in pairs)
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Emitters: neutral frontmatter -> per-tool files
# --------------------------------------------------------------------------- #
def emit_claude_agent(meta: dict, body: str) -> str:
    pairs = [("name", meta["name"]), ("description", _dq(meta["description"]))]
    tools = meta.get("tools") or []
    if tools:
        cc = [NEUTRAL_TO_CC.get(t, t) for t in tools]
        pairs.append(("tools", ", ".join(cc)))
    if meta.get("model"):
        pairs.append(("model", meta["model"]))
    return render_frontmatter(pairs, body)


def emit_opencode_agent(meta: dict, body: str) -> str:
    pairs = [
        ("description", _dq(meta["description"])),
        ("mode", meta.get("mode", "subagent")),
    ]
    if meta.get("model"):
        pairs.append(("model", meta["model"]))
    lines = ["---"]
    lines.extend(f"{key}: {value}" for key, value in pairs)
    tools = meta.get("tools") or []
    if tools:
        allow = set(tools)
        lines.append("tools:")
        for tool in OPENCODE_TOOLS:
            lines.append(f"  {tool}: {'true' if tool in allow else 'false'}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def emit_claude_command(meta: dict, body: str) -> str:
    pairs = [("description", _dq(meta["description"]))]
    if meta.get("argument-hint"):
        # argument-hint is a display string. Authors naturally write it as
        # `[base-branch]`, which the parser reads as an inline list — re-serialize
        # the bracket form so it round-trips to a literal string for Claude Code.
        hint = meta["argument-hint"]
        if isinstance(hint, list):
            hint = "[" + ", ".join(hint) + "]"
        pairs.append(("argument-hint", hint))
    tools = meta.get("tools") or []
    if tools:
        cc = [NEUTRAL_TO_CC.get(t, t) for t in tools]
        pairs.append(("allowed-tools", ", ".join(cc)))
    if meta.get("model"):
        pairs.append(("model", meta["model"]))
    return render_frontmatter(pairs, body)


def emit_opencode_command(meta: dict, body: str) -> str:
    pairs = [("description", _dq(meta["description"]))]
    if meta.get("agent"):
        pairs.append(("agent", meta["agent"]))
    if meta.get("model"):
        pairs.append(("model", meta["model"]))
    return render_frontmatter(pairs, body)


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def clean_outputs() -> None:
    for path in (CLAUDE_PLUGIN_DIR, CLAUDE_PLUGINS_OUT, OPENCODE_DIR):
        shutil.rmtree(path, ignore_errors=True)
    OPENCODE_CONFIG.unlink(missing_ok=True)


def build_owner(mp: dict) -> dict:
    owner = {"name": mp.get("owner_name", "")}
    if mp.get("owner_email"):
        owner["email"] = mp["owner_email"]
    if mp.get("owner_url"):
        owner["url"] = mp["owner_url"]
    return owner


def build_author(meta: dict) -> dict | None:
    if not meta.get("author_name"):
        return None
    author = {"name": meta["author_name"]}
    if meta.get("author_email"):
        author["email"] = meta["author_email"]
    if meta.get("author_url"):
        author["url"] = meta["author_url"]
    return author


def process_plugin(plugin_dir: Path) -> dict:
    """Generate one plugin's outputs; return its marketplace.json entry."""
    meta = parse_block((plugin_dir / "plugin.yaml").read_text(encoding="utf-8"))
    name = meta["name"]
    cc_root = CLAUDE_PLUGINS_OUT / name

    # Claude Code plugin manifest.
    manifest = {"name": name, "version": meta.get("version", "0.0.0")}
    if meta.get("description"):
        manifest["description"] = meta["description"]
    author = build_author(meta)
    if author:
        manifest["author"] = author
    if meta.get("homepage"):
        manifest["homepage"] = meta["homepage"]
    if meta.get("license"):
        manifest["license"] = meta["license"]
    if meta.get("keywords"):
        manifest["keywords"] = meta["keywords"]
    _write(cc_root / ".claude-plugin" / "plugin.json",
           json.dumps(manifest, indent=2) + "\n")

    # Plugin README (optional) -> shipped with the Claude Code plugin.
    readme = plugin_dir / "README.md"
    if readme.is_file():
        shutil.copy2(readme, cc_root / "README.md")

    # Agents -> Claude Code + opencode.
    for agent_file in sorted((plugin_dir / "agents").glob("*.md")):
        fm, body = split_frontmatter(agent_file.read_text(encoding="utf-8"))
        _write(cc_root / "agents" / agent_file.name, emit_claude_agent(fm, body))
        _write(OPENCODE_DIR / "agent" / agent_file.name, emit_opencode_agent(fm, body))

    # Commands -> Claude Code + opencode.
    for cmd_file in sorted((plugin_dir / "commands").glob("*.md")):
        fm, body = split_frontmatter(cmd_file.read_text(encoding="utf-8"))
        _write(cc_root / "commands" / cmd_file.name, emit_claude_command(fm, body))
        _write(OPENCODE_DIR / "command" / cmd_file.name, emit_opencode_command(fm, body))

    # Skills -> Claude Code only (opencode has no skill concept).
    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        shutil.copytree(skills_dir, cc_root / "skills")

    # Optional pass-through assets for Claude Code: hooks/ and .mcp.json.
    hooks_dir = plugin_dir / "hooks"
    if hooks_dir.is_dir():
        shutil.copytree(hooks_dir, cc_root / "hooks")
    mcp_file = plugin_dir / ".mcp.json"
    if mcp_file.is_file():
        shutil.copy2(mcp_file, cc_root / ".mcp.json")

    # Marketplace entry.
    entry = {
        "name": name,
        "source": f"./plugins/{name}",
        "description": meta.get("description", ""),
        "version": meta.get("version", "0.0.0"),
    }
    if author:
        entry["author"] = author
    if meta.get("homepage"):
        entry["homepage"] = meta["homepage"]
    if meta.get("license"):
        entry["license"] = meta["license"]
    if meta.get("category"):
        entry["category"] = meta["category"]
    if meta.get("keywords"):
        entry["keywords"] = meta["keywords"]
    return entry


def build() -> None:
    if not SRC_PLUGINS.is_dir():
        sys.exit(f"error: no source plugins directory at {SRC_PLUGINS}")

    mp = parse_block((SOURCE / "marketplace.yaml").read_text(encoding="utf-8"))
    clean_outputs()

    plugin_dirs = sorted(p for p in SRC_PLUGINS.iterdir()
                         if (p / "plugin.yaml").is_file())
    entries = [process_plugin(p) for p in plugin_dirs]

    # Claude Code marketplace manifest.
    marketplace = {"name": mp["name"], "owner": build_owner(mp)}
    metadata = {}
    if mp.get("description"):
        metadata["description"] = mp["description"]
    if mp.get("version"):
        metadata["version"] = mp["version"]
    if metadata:
        marketplace["metadata"] = metadata
    marketplace["plugins"] = entries
    _write(CLAUDE_PLUGIN_DIR / "marketplace.json",
           json.dumps(marketplace, indent=2) + "\n")

    # Minimal opencode config (agents/commands are auto-discovered from .opencode/).
    _write(OPENCODE_CONFIG,
           json.dumps({"$schema": "https://opencode.ai/config.json"}, indent=2) + "\n")

    print(f"Built {len(entries)} plugin(s): {', '.join(e['name'] for e in entries)}")
    print("  -> .claude-plugin/marketplace.json + plugins/")
    print("  -> .opencode/ + opencode.json")


def check() -> None:
    """Verify generated outputs are up to date with source (for CI)."""
    import tempfile

    snapshot = {}
    for base in (CLAUDE_PLUGIN_DIR, CLAUDE_PLUGINS_OUT, OPENCODE_DIR, OPENCODE_CONFIG):
        if base.is_file():
            snapshot[base] = base.read_bytes()
        elif base.is_dir():
            for f in base.rglob("*"):
                if f.is_file():
                    snapshot[f] = f.read_bytes()

    build()

    stale = []
    current = set()
    for base in (CLAUDE_PLUGIN_DIR, CLAUDE_PLUGINS_OUT, OPENCODE_DIR, OPENCODE_CONFIG):
        if base.is_file():
            current.add(base)
            if snapshot.get(base) != base.read_bytes():
                stale.append(base)
        elif base.is_dir():
            for f in base.rglob("*"):
                if f.is_file():
                    current.add(f)
                    if snapshot.get(f) != f.read_bytes():
                        stale.append(f)
    removed = set(snapshot) - current
    if stale or removed:
        for f in sorted(stale) + sorted(removed):
            print(f"stale: {f.relative_to(ROOT)}")
        sys.exit("error: generated outputs are out of date — run scripts/build.py")
    print("Outputs are up to date.")


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        check()
    else:
        build()
