#!/usr/bin/env python3
"""Read a campaign.md and report its Status field via exit code.

Usage:
    python3 verify_status.py <campaign.md>

Exit codes:
    0   status is APPROVED       — orchestrator may proceed to fan-out
    1   status is PROPOSED       — user has not yet approved
    2   status is REVISE         — user wants changes; read inline notes
    3   status is DRAFT or POSTED — campaign is past approval
    4   file not found / unparseable / unknown status value

Stdout (on exit 0/1/2/3): the status value. Empty on exit 4.

The status field lives in the YAML frontmatter at the top of campaign.md
(`status: PROPOSED` etc.) OR on a top-level line `Status:` for compatibility.
We read the first match — frontmatter takes precedence if both are present.

This script is deliberately minimal: it reads only the status field, never the
topic-level Status entries deeper in the file. That keeps the gate
unambiguous.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# YAML frontmatter status: `status: APPROVED` (case-insensitive value)
_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n",
    re.DOTALL,
)
_STATUS_LINE_RE = re.compile(
    r"^\s*status\s*:\s*(\w+)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_EXIT_BY_STATUS = {
    "APPROVED": 0,
    "PROPOSED": 1,
    "REVISE":   2,
    "DRAFT":    3,
    "POSTED":   3,
}


def _extract_status(text: str) -> str | None:
    # Try frontmatter first.
    m = _FRONTMATTER_RE.search(text)
    if m:
        fm = m.group(1)
        sm = _STATUS_LINE_RE.search(fm)
        if sm:
            return sm.group(1).upper()
    # Fallback: any top-level `Status:` line (the templates also have a
    # legend block — match the first occurrence).
    sm = _STATUS_LINE_RE.search(text)
    if sm:
        return sm.group(1).upper()
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 4

    path = Path(argv[1])
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 4

    try:
        text = path.read_text()
    except OSError as exc:
        print(f"error: read failed: {exc}", file=sys.stderr)
        return 4

    status = _extract_status(text)
    if status is None:
        print("error: no status field found", file=sys.stderr)
        return 4

    if status not in _EXIT_BY_STATUS:
        print(f"error: unknown status value: {status}", file=sys.stderr)
        return 4

    print(status)
    return _EXIT_BY_STATUS[status]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
