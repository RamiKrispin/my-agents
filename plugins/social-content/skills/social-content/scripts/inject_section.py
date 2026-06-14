#!/usr/bin/env python3
"""Insert a prepared newsletter section into a newsletter pre-draft.

Usage:
    python3 inject_section.py --new <draft-path> --type <type> <section-file>
    python3 inject_section.py --append <draft-path> --type <type> <section-file>

  --new      Create a new pre-draft from the imported newsletter template,
             filling the chosen slot with <section-file> and leaving the
             other two slots as TODO placeholders. Fails if <draft-path>
             already exists.
  --append   Append <section-file> content into the existing section under
             ## <heading> in <draft-path>. If the section currently holds a
             template placeholder or a TODO marker, it is replaced; otherwise
             the new content is appended after a horizontal-rule separator
             so prior items stay visible. Fails if <draft-path> doesn't
             exist or the heading isn't found.

  <type>             open-source | learning | book — picks which slot to fill.
  <section-file>     The prepared section markdown (no metadata wrapper).

The newsletter template (`formats/newsletter-template.md`) is imported into
this skill from the `newsletter` plugin at build time; this helper resolves
it relative to its own location, so it works from the built plugin tree
without any further setup.

Exit codes:
  0 — wrote successfully
  2 — usage error, validation failure, or missing target / template
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "formats" / "newsletter-template.md"

TYPE_TO_SLOT = {
    "open-source": "{{open_source_section}}",
    "learning":    "{{learning_section}}",
    "book":        "{{book_section}}",
}

TYPE_TO_HEADING = {
    "open-source": "## Open Source of the Week",
    "learning":    "## New Learning Resources",
    "book":        "## Book of the Week",
}

TODO_PLACEHOLDER = {
    "open-source": "_TODO: research and draft the Open Source of the Week section._",
    "learning":    "_TODO: research and draft the New Learning Resources section._",
    "book":        "_TODO: research and draft the Book of the Week section._",
}

# The template's title and agenda lines carry placeholders we want to surface
# as TODO markers so the user can see what's still owed before publishing.
TITLE_LINE_OLD = "{{highlight}}, {{highlight}} | Issue {{N}}"
TITLE_LINE_NEW = "_TODO: highlight_, _TODO: highlight_ | Issue _TODO_"

AGENDA_REPLACEMENTS = {
    "open-source": ("Open Source of the Week - {{project name}}",
                    "Open Source of the Week - "),
    "learning":    ("New learning resources - {{resource}}, {{resource}}, {{resource}}",
                    "New learning resources - "),
    "book":        ("Book of the week - {{title}} by {{author}}",
                    "Book of the week - "),
}


def _agenda_hint(section_type: str, section_content: str) -> str:
    """Best-effort short label for the agenda bullet, derived from the section.

    Returns "_TODO_" if no signal is found — the user can fill it in by hand.
    """
    if section_type == "open-source":
        match = re.search(r"\*\*([^*\n]+)\*\*", section_content)
        if match:
            return match.group(1).strip()
    elif section_type == "book":
        match = re.search(r"\*([^*\n]+)\*\s*by\s+([^.\n]+)", section_content)
        if match:
            return f"{match.group(1).strip()} by {match.group(2).strip()}"
    elif section_type == "learning":
        titles = re.findall(r"^###\s+(.+?)\s*$", section_content, re.MULTILINE)
        if titles:
            return ", ".join(t.strip() for t in titles[:3])
    return "_TODO_"


def _atomic_write(path: Path, content: str) -> None:
    """Sibling .tmp file then os.replace — same discipline as append_post.py."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def cmd_new(draft_path: Path, section_type: str, section_content: str) -> int:
    if draft_path.exists():
        print(
            f"error: {draft_path} already exists; use --append or pick a new path",
            file=sys.stderr,
        )
        return 2
    if not TEMPLATE_PATH.exists():
        print(
            f"error: imported newsletter template not found at {TEMPLATE_PATH}; "
            "rebuild the marketplace (python3 scripts/build.py) so 'imports:' "
            "copies it into this plugin",
            file=sys.stderr,
        )
        return 2

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    out = template

    # Fill slot for the chosen section type; replace others with TODOs.
    for type_key, slot in TYPE_TO_SLOT.items():
        replacement = (
            section_content.strip() if type_key == section_type
            else TODO_PLACEHOLDER[type_key]
        )
        out = out.replace(slot, replacement)

    # Title line — leave a TODO so the user fills the issue title and number.
    out = out.replace(TITLE_LINE_OLD, TITLE_LINE_NEW)

    # Agenda bullets — fill the chosen one from the section content; others stay TODO.
    for type_key, (placeholder, prefix) in AGENDA_REPLACEMENTS.items():
        if type_key == section_type:
            label = _agenda_hint(type_key, section_content)
        else:
            label = "_TODO_"
        out = out.replace(placeholder, prefix + label)

    draft_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write(draft_path, out)
    print(f"created new pre-draft at {draft_path} (slot: {section_type})")
    return 0


def cmd_append(draft_path: Path, section_type: str, section_content: str) -> int:
    if not draft_path.exists():
        print(f"error: {draft_path} does not exist; use --new", file=sys.stderr)
        return 2

    raw = draft_path.read_text(encoding="utf-8")
    heading = TYPE_TO_HEADING[section_type]
    lines = raw.splitlines(keepends=True)

    start = next(
        (i for i, line in enumerate(lines) if line.rstrip() == heading),
        None,
    )
    if start is None:
        print(
            f"error: heading '{heading}' not found in {draft_path}",
            file=sys.stderr,
        )
        return 2

    # Section ends at the next H2 heading or the next horizontal-rule separator.
    end = len(lines)
    for j in range(start + 1, len(lines)):
        rstripped = lines[j].rstrip()
        if rstripped.startswith("## ") or rstripped == "---":
            end = j
            break

    body = "".join(lines[start + 1:end]).strip()
    slot = TYPE_TO_SLOT[section_type]
    placeholder = TODO_PLACEHOLDER[section_type]
    new_content = section_content.strip()

    # Dedupe guard: if the exact same content is already in this section,
    # treat the call as a no-op rather than stacking duplicates. Catches
    # retried runs where the model calls --append twice for the same input.
    if new_content and new_content in body:
        print(
            f"note: '{heading}' in {draft_path} already contains this section "
            "content; no changes made",
        )
        return 0

    is_empty_or_placeholder = (
        not body
        or body == placeholder
        or slot in body
    )

    new_block = "\n" + new_content + "\n\n"
    if not is_empty_or_placeholder:
        # Preserve prior content; place a horizontal rule between the old
        # section body and the appended content so both stay readable.
        new_block = "\n" + body + "\n\n---\n\n" + new_content + "\n\n"

    out = "".join(lines[:start + 1]) + new_block + "".join(lines[end:])
    if not out.endswith("\n"):
        out += "\n"

    _atomic_write(draft_path, out)
    print(f"appended to '{heading}' in {draft_path}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Inject a prepared section into a newsletter pre-draft.",
        add_help=True,
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--new", dest="new_path", metavar="PATH",
                        help="create a new pre-draft from the newsletter template")
    target.add_argument("--append", dest="append_path", metavar="PATH",
                        help="append into an existing pre-draft")
    parser.add_argument("--type", required=True, choices=sorted(TYPE_TO_SLOT.keys()),
                        help="which newsletter slot to fill")
    parser.add_argument("section_file", metavar="SECTION-FILE",
                        help="prepared section markdown (no metadata wrapper)")
    args = parser.parse_args(argv[1:])

    section_path = Path(args.section_file)
    if not section_path.exists():
        print(f"error: section file not found: {section_path}", file=sys.stderr)
        return 2
    section_content = section_path.read_text(encoding="utf-8")
    if not section_content.strip():
        print(f"error: section file is empty: {section_path}", file=sys.stderr)
        return 2

    if args.new_path:
        return cmd_new(Path(args.new_path), args.type, section_content)
    return cmd_append(Path(args.append_path), args.type, section_content)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
