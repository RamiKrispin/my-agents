#!/usr/bin/env python3
"""Atomically materialize a campaign directory skeleton.

Usage:
    python3 init_campaign.py <campaigns-root> <slug>

Creates:
    <campaigns-root>/<slug>/campaign.md     # skeleton with Status: PROPOSED
    <campaigns-root>/<slug>/topics/         # empty; populated at fan-out
    <campaigns-root>/<slug>/blog/           # empty; populated at fan-out
    <campaigns-root>/<slug>/assets/         # empty; sidecars land here

If the campaign directory already exists, the script does NOT overwrite it
(so resuming a campaign mid-flight is safe). Exits 1 in that case so the
caller can decide whether to read the existing campaign.md or stop.

The skeleton campaign.md is copied from `templates/campaign.md` (relative to
the skill folder) — the orchestrator populates the actual content fields after
this script runs.

Slug guard: lowercase kebab-case, max 80 chars, must start with [a-z0-9].
Same regex as social-content's append_post.py — slugs become path components,
so '..', '/', whitespace, and leading hyphens are rejected up front.

Exit codes:
    0   created successfully
    1   campaign directory already exists (caller decides what to do)
    2   usage error / invalid slug / template missing
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{0,79}$")


def _atomic_write(path: Path, content: str) -> None:
    """Write to a sibling .tmp and os.replace into place."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content)
    os.replace(tmp, path)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    campaigns_root = Path(argv[1])
    slug = argv[2]

    if not _SLUG_RE.match(slug):
        print(
            f"error: slug must be lowercase kebab-case (a-z, 0-9, hyphens; "
            f"max 80 chars; must start with a letter or digit). got '{slug}'",
            file=sys.stderr,
        )
        return 2

    # Guard the campaigns root: must be an existing directory, and we resolve
    # it to defeat `..` traversal in the input. The orchestrator should pass
    # an explicit working-directory path; refusing nonexistent roots prevents
    # silent phantom-directory creation on a typo.
    if not campaigns_root.exists():
        print(
            f"error: campaigns root does not exist: {campaigns_root}\n"
            "  pass an existing directory (e.g. the user's working directory).",
            file=sys.stderr,
        )
        return 2
    if not campaigns_root.is_dir():
        print(
            f"error: campaigns root is not a directory: {campaigns_root}",
            file=sys.stderr,
        )
        return 2
    campaigns_root = campaigns_root.resolve()

    campaign_dir = campaigns_root / slug
    if campaign_dir.exists():
        print(
            f"error: campaign directory already exists: {campaign_dir}",
            file=sys.stderr,
        )
        return 1

    # Locate the template (relative to this script: ../templates/campaign.md)
    template_path = Path(__file__).resolve().parent.parent / "templates" / "campaign.md"
    if not template_path.exists():
        print(f"error: template not found: {template_path}", file=sys.stderr)
        return 2

    skeleton = template_path.read_text()

    # Materialize: parent dirs first, then content file atomically.
    campaign_dir.mkdir(parents=True, exist_ok=False)
    (campaign_dir / "topics").mkdir()
    (campaign_dir / "blog").mkdir()
    (campaign_dir / "assets").mkdir()
    _atomic_write(campaign_dir / "campaign.md", skeleton)

    print(f"created campaign skeleton at {campaign_dir}")
    print("next: populate the campaign.md fields (orchestrator step 4) and stop for user approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
