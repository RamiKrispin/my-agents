#!/usr/bin/env python3
"""Offline structural check for a saved social-content draft.

Usage:
    python3 validate.py <draft.md>

Exit 0 means PASS. Non-zero with a bulleted list of issues means FAIL.

Accepts two file shapes:
  - **Single-post file** — the whole file is one post body (validate as-is).
  - **Aggregated posts file** — produced by `append_post.py`. Detected by an
    H1 line followed by `## YYYY-MM-DD —` H2 entry headings. Validates only
    the **topmost entry's body**: skips the H1 + intro, the metadata bullets,
    and any `<details>...</details>` source-notes block before the post text.

Checks (all offline, deterministic):
  - File exists and is non-empty.
  - Has a hook on the first non-blank line of the post body.
  - For LinkedIn drafts: total length is within reasonable bounds (200-3000
    characters of body text, excluding hashtags / link footer).
  - No banned hype phrases (word-boundary match — "next-gen" is banned but
    the legitimate word "next-generation" is not).
  - No banned engagement-bait endings ("Agree?", "Thoughts?", "What do you
    think?").
  - Reasonable white space — no paragraph longer than 6 lines, except
    bullet-list paragraphs (≥3 contiguous bullet lines) which are exempt.

The skill calls this in the QA step. Designed to catch obvious regressions, not
to grade prose. Voice/structure judgement is the model's job.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BANNED_HYPE = [
    "powerful", "cutting-edge", "revolutionary", "game-changing",
    "game changing", "seamless", "next-gen", "next gen",
    "supercharge", "unleash", "unlock the power",
]

BANNED_ENDINGS = [
    "agree?",
    "thoughts?",
    "what do you think?",
    "what are your thoughts?",
]

MAX_PARAGRAPH_LINES = 6
MIN_BODY_CHARS = 200
MAX_BODY_CHARS = 3000


def _strip_link_and_hashtag_footer(text: str) -> str:
    """Trim trailing 'Repo: ...', 'Course: ...' lines and a hashtag block."""
    lines = text.rstrip().splitlines()
    while lines:
        last = lines[-1].strip()
        if not last:
            lines.pop()
            continue
        is_hashtag_block = last.startswith("#") and " " not in last.lstrip("#").split("#", 1)[0]
        is_hashtag_line = bool(re.match(r"^(#\w+\s*)+$", last))
        is_link_footer = bool(re.match(r"^(Repo|Course|Link|Newsletter):\s+http", last, re.I))
        if is_hashtag_block or is_hashtag_line or is_link_footer:
            lines.pop()
            continue
        break
    return "\n".join(lines)


_AGGREGATED_ENTRY_RE = re.compile(r"^## \d{4}-\d{2}-\d{2} —", re.MULTILINE)


def _extract_top_entry_body(raw: str) -> str:
    """For an aggregated posts file, return only the topmost entry's post body.

    Skips the H1 + intro, the H2 date heading, the metadata bullets, and any
    `<details>...</details>` source-notes block before the post body.
    Returns empty string if no entry is found.
    """
    matches = list(_AGGREGATED_ENTRY_RE.finditer(raw))
    if not matches:
        return ""
    first = matches[0]
    second = matches[1].start() if len(matches) > 1 else len(raw)
    entry = raw[first.start():second]
    # entry starts with "## YYYY-MM-DD — Title"; drop that line.
    after_h2 = entry.split("\n", 1)[1] if "\n" in entry else ""
    # Drop an optional `\n---\n` separator at the end of the entry.
    after_h2 = re.sub(r"\n---\s*$", "", after_h2)
    # Drop leading metadata bullets (lines starting with "- **").
    lines = after_h2.splitlines()
    i = 0
    # skip blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1
    # skip metadata bullets
    while i < len(lines) and lines[i].startswith("- **"):
        i += 1
    # skip optional <details>...</details> source-notes block
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("<details"):
        while i < len(lines) and "</details>" not in lines[i]:
            i += 1
        i += 1  # consume the </details> line itself
    # skip trailing blanks before body
    while i < len(lines) and not lines[i].strip():
        i += 1
    return "\n".join(lines[i:]).strip()


def _is_aggregated(raw: str) -> bool:
    return bool(_AGGREGATED_ENTRY_RE.search(raw))


def validate(path: Path) -> list[str]:
    issues: list[str] = []

    if not path.exists():
        return [f"file not found: {path}"]

    raw = path.read_text()
    if not raw.strip():
        return ["file is empty"]

    if _is_aggregated(raw):
        post_text = _extract_top_entry_body(raw)
        if not post_text:
            return ["aggregated file has no extractable top entry"]
    else:
        post_text = raw

    body = _strip_link_and_hashtag_footer(post_text)
    body_chars = len(body)

    # Hook check.
    first_nonblank = next(
        (ln for ln in post_text.splitlines() if ln.strip()), ""
    )
    if not first_nonblank:
        issues.append("no hook on first non-blank line")
    elif first_nonblank.startswith("#"):
        issues.append("first line looks like a heading, not a LinkedIn hook")

    # Length check.
    if body_chars < MIN_BODY_CHARS:
        issues.append(
            f"body is {body_chars} chars (min {MIN_BODY_CHARS}); "
            "post is too thin"
        )
    if body_chars > MAX_BODY_CHARS:
        issues.append(
            f"body is {body_chars} chars (max {MAX_BODY_CHARS}); "
            "consider splitting into two posts"
        )

    # Banned hype phrases. Word-boundary match — substring match would
    # over-fire ("next-gen" inside the legitimate word "next-generation").
    lowered = body.lower()
    for phrase in BANNED_HYPE:
        if re.search(r"\b" + re.escape(phrase) + r"\b", lowered):
            issues.append(f"banned hype phrase: \"{phrase}\"")

    # Banned engagement bait at the end.
    last_nonblank = ""
    for line in reversed(body.splitlines()):
        if line.strip():
            last_nonblank = line.strip().lower()
            break
    for phrase in BANNED_ENDINGS:
        if last_nonblank == phrase or last_nonblank.endswith(" " + phrase):
            issues.append(f"banned engagement bait ending: \"{phrase}\"")

    # White space discipline.
    # Exempt list-like paragraphs from the line cap: a paragraph with a
    # contiguous run of >=3 bullet lines is a topic list (often with a 1-2
    # line lead-in), not a wall of text.
    bullet_re = re.compile(r"^\s*(?:[-*•✓✅▪●]|\d+\.)\s+")
    paragraphs = re.split(r"\n\s*\n", body.strip())
    for i, para in enumerate(paragraphs, 1):
        lines = [ln for ln in para.strip().splitlines() if ln.strip()]
        line_count = len(lines)
        if line_count <= MAX_PARAGRAPH_LINES:
            continue
        max_run = run = 0
        for ln in lines:
            run = run + 1 if bullet_re.match(ln) else 0
            max_run = max(max_run, run)
        if max_run >= 3:
            continue
        issues.append(
            f"paragraph {i} is {line_count} lines "
            f"(max {MAX_PARAGRAPH_LINES}); break it up for mobile"
        )

    return issues


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    path = Path(argv[1])
    issues = validate(path)
    if not issues:
        print("PASS")
        return 0

    print("FAIL")
    for issue in issues:
        print(f"  - {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
