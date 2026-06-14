#!/usr/bin/env python3
"""Offline structural check for a newsletter-section social-content draft.

Usage:
    python3 validate_newsletter_section.py <type> <draft.md>

  <type> = open-source | learning | book

The draft is the literal section body that would be inlined into a newsletter
issue's matching slot — no metadata wrapper, no `## <heading>` line (the
heading is supplied by the newsletter template at assembly time).

Exit 0 means PASS. Non-zero with bulleted issues means FAIL.

Checks (all offline, deterministic):
  - File exists and is non-empty.
  - Length is within reasonable bounds for the section type.
  - Type-specific structural patterns are present (e.g. open-source needs a
    "Project repo:" link and a "License:" line; book needs "*Title* by
    Author" framing and a "Topics Covered" subheading).
  - No banned hype phrases (word-boundary match — "next-gen" is banned; the
    legitimate word "next-generation" is not).

The skill calls this in the QA step. Designed to catch obvious regressions,
not to grade prose. Voice / structure judgement is the model's job.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Shared with validate.py — kept in sync manually. Don't import across files
# (each script stays self-contained so they're easy to copy out of the repo).
BANNED_HYPE = [
    "powerful", "cutting-edge", "revolutionary", "game-changing",
    "game changing", "seamless", "next-gen", "next gen",
    "supercharge", "unleash", "unlock the power",
]

# Per-section length envelopes. Generous on the upper bound — the section
# specs allow lead-ins and feature lists; we only flag clearly-thin or
# clearly-bloated drafts.
LENGTH_BOUNDS = {
    "open-source": (300, 3500),
    "learning":    (150, 2000),
    "book":        (250, 2500),
}

REQUIREMENTS = {
    "open-source": [
        # Bold project name must appear in the first paragraph specifically —
        # not in a feature bullet later. The validator extracts the lead
        # paragraph before running this; see `_lead_paragraph` below.
        ("lead", re.compile(r"\*\*[^*\n]+\*\*"),
         "first paragraph must bold the project name (e.g. **ProjectName**)"),
        # Spec requires the bold form: `Project repo: **[<url>](<url>)**`.
        ("body", re.compile(r"Project repo:\s*\*\*\[", re.IGNORECASE),
         "missing 'Project repo: **[<url>](<url>)**' line (must use the bold form)"),
        ("body", re.compile(r"^###\s+Key Features", re.MULTILINE),
         "missing '### Key Features' heading"),
        ("body", re.compile(r"License:\s*\S", re.IGNORECASE),
         "missing 'License: <SPDX>' line"),
    ],
    "learning": [
        ("body", re.compile(r"^###\s+\S", re.MULTILINE),
         "must contain at least one '### Resource title' heading"),
        ("body", re.compile(r"^https?://\S+\s*$", re.MULTILINE),
         "must contain at least one bare URL on its own line"),
    ],
    "book": [
        # Italic `*Title* by Author` must appear in the first paragraph.
        ("lead", re.compile(r"\*[^*\n]+\*\s*by\s+\S", re.IGNORECASE),
         "first paragraph must include '*Title* by Author'"),
        ("body", re.compile(r"^###\s+Topics Covered", re.MULTILINE),
         "missing '### Topics Covered' heading"),
        ("body", re.compile(r"\bideal for\b", re.IGNORECASE),
         "missing 'ideal for ...' audience framing"),
    ],
}


def _lead_paragraph(body: str) -> str:
    """First paragraph block — everything before the first blank line."""
    return re.split(r"\n\s*\n", body, maxsplit=1)[0]


def validate(section_type: str, raw: str) -> list[str]:
    issues: list[str] = []

    body = raw.strip()
    if not body:
        return ["file is empty"]

    n = len(body)
    lo, hi = LENGTH_BOUNDS[section_type]
    if n < lo:
        issues.append(f"section is {n} chars (min {lo} for {section_type}); too thin")
    if n > hi:
        issues.append(f"section is {n} chars (max {hi} for {section_type}); consider trimming")

    lead = _lead_paragraph(body)
    for scope, pattern, message in REQUIREMENTS[section_type]:
        target = lead if scope == "lead" else body
        if not pattern.search(target):
            issues.append(message)

    lowered = body.lower()
    for phrase in BANNED_HYPE:
        if re.search(r"\b" + re.escape(phrase) + r"\b", lowered):
            issues.append(f'banned hype phrase: "{phrase}"')

    return issues


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    section_type = argv[1]
    if section_type not in REQUIREMENTS:
        print(
            f"error: type must be one of {sorted(REQUIREMENTS)}, got '{section_type}'",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[2])
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    issues = validate(section_type, path.read_text(encoding="utf-8"))
    if not issues:
        print("PASS")
        return 0

    print("FAIL")
    for issue in issues:
        print(f"  - {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
