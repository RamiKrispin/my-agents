#!/usr/bin/env python3
"""Insert a new post entry at the top of an aggregated posts file.

Usage:
    python3 append_post.py <posts-file> <meta.json> <body.md>

`<meta.json>` schema:
    {
      "title":  "Stanford CS25: Transformers",   # required
      "slug":   "stanford-cs25-transformers",    # required
      "date":   "2026-06-04",                    # required (YYYY-MM-DD)
      "source": "https://...",                   # optional
      "pillar": "Learning Radar",                # optional
      "format": "linkedin" | "reels",            # optional, used for header copy
      "status": "draft" | "posted",              # optional, default "draft"
      "notes":  "...markdown..."                 # optional, embedded in a
                                                 # collapsible <details> block
    }

`<body.md>` is the literal post text (verbatim, what would be pasted to
LinkedIn or read aloud for a Reels script).

Behavior:
  - Creates the parent directory of <posts-file> if absent.
  - Creates <posts-file> with a default H1 header on first run.
  - New entries are inserted at the TOP (just below the H1 + intro). Existing
    entries shift down.
  - Entries are separated by `\\n\\n---\\n\\n` markers.
  - If the same slug already exists in the file, exits 2 — caller should ask
    the user how to resolve (overwrite, skip, rename).

Exit codes:
  0 — wrote successfully
  2 — usage error, missing fields, or slug conflict
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SEPARATOR = "\n\n---\n\n"

# Slug guard. Lowercase kebab-case, must start with [a-z0-9], up to 80 chars.
# Used as a path component for sidecar files (posts/assets/<slug>.drawio,
# posts/assets/<slug>.infographic.md), so anything containing '/', '..', or
# whitespace is rejected up front.
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{0,79}$")


def _default_header(file_stem: str, fmt_hint: str | None) -> str:
    # "learning-resource-post" → "Learning resource"
    base = file_stem
    for suffix in ("-post", "-reels"):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    title = base.replace("-", " ").strip().capitalize() or "Posts"
    fmt_label = {
        "linkedin": "LinkedIn",
        "reels": "Reels / TikTok",
    }.get(fmt_hint or "", "LinkedIn" if "-reels" not in file_stem else "Reels / TikTok")
    return (
        f"# {title} posts ({fmt_label})\n"
        "\n"
        "Drafts compiled by the social-content skill. Newest at the top.\n"
        "Each entry starts with metadata; the post body follows.\n"
    )


def _make_entry(meta: dict, body: str) -> str:
    parts: list[str] = []
    parts.append(f"## {meta['date']} — {meta['title']}")
    parts.append("")
    bullets: list[str] = []
    if meta.get("source"):
        bullets.append(f"- **Source:** {meta['source']}")
    bullets.append(f"- **Slug:** {meta['slug']}")
    if meta.get("pillar"):
        bullets.append(f"- **Pillar:** {meta['pillar']}")
    bullets.append(f"- **Status:** {meta.get('status', 'draft')}")
    parts.extend(bullets)
    parts.append("")
    if meta.get("notes"):
        parts.append("<details><summary>Source notes</summary>")
        parts.append("")
        parts.append(meta["notes"].strip())
        parts.append("")
        parts.append("</details>")
        parts.append("")
    parts.append(body.strip())
    return "\n".join(parts)


def _slug_exists(existing: str, slug: str) -> bool:
    pattern = rf"^- \*\*Slug:\*\*\s+{re.escape(slug)}\s*$"
    return bool(re.search(pattern, existing, re.MULTILINE))


def _split_header_and_body(existing: str) -> tuple[str, str]:
    """Split file at the first separator. If none, treat whole file as header."""
    idx = existing.find(SEPARATOR)
    if idx == -1:
        return existing.rstrip() + "\n", ""
    header = existing[:idx].rstrip() + "\n"
    body = existing[idx + len(SEPARATOR):]
    return header, body


def append_post(posts_path: Path, meta: dict, body: str) -> int:
    posts_path.parent.mkdir(parents=True, exist_ok=True)

    if posts_path.exists():
        existing = posts_path.read_text()
        if _slug_exists(existing, meta["slug"]):
            print(
                f"error: slug '{meta['slug']}' already exists in {posts_path}; "
                "ask the user whether to overwrite, skip, or rename",
                file=sys.stderr,
            )
            return 2
        header, tail = _split_header_and_body(existing)
    else:
        header = _default_header(posts_path.stem, meta.get("format"))
        tail = ""

    entry = _make_entry(meta, body)
    new_content = header + SEPARATOR + entry
    if tail.strip():
        new_content += SEPARATOR + tail.lstrip("\n")
    if not new_content.endswith("\n"):
        new_content += "\n"

    # Atomic write: a sibling temp file then os.replace, so a concurrent
    # invocation can't truncate the file mid-write.
    tmp = posts_path.with_suffix(posts_path.suffix + ".tmp")
    tmp.write_text(new_content)
    os.replace(tmp, posts_path)
    print(f"wrote entry '{meta['slug']}' to {posts_path}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    posts_path = Path(argv[1])
    meta_path = Path(argv[2])
    body_path = Path(argv[3])

    if not meta_path.exists():
        print(f"error: meta file not found: {meta_path}", file=sys.stderr)
        return 2
    if not body_path.exists():
        print(f"error: body file not found: {body_path}", file=sys.stderr)
        return 2

    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {meta_path}: {exc}", file=sys.stderr)
        return 2

    for required in ("title", "slug", "date"):
        if not meta.get(required):
            print(
                f"error: meta.{required} is required",
                file=sys.stderr,
            )
            return 2
    if not _SLUG_RE.match(meta["slug"]):
        print(
            f"error: meta.slug must be lowercase kebab-case (a-z, 0-9, hyphens; "
            f"max 80 chars; must start with a letter or digit). got '{meta['slug']}'",
            file=sys.stderr,
        )
        return 2
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", meta["date"]):
        print(
            f"error: meta.date must be YYYY-MM-DD, got '{meta['date']}'",
            file=sys.stderr,
        )
        return 2

    body = body_path.read_text()
    return append_post(posts_path, meta, body)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
