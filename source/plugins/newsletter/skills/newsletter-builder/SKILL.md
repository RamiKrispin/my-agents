---
name: newsletter-builder
description: Draft Rami Krispin's weekly data science newsletter from a set of links. Use when building, drafting, or assembling a newsletter issue with the fixed three sections — Open Source of the Week, New Learning Resources, and Book of the Week — researching each link and writing in the author's voice. Produces a Substack-ready Markdown draft.
---

# Newsletter Builder

Build one weekly issue of the data science newsletter from a handful of links,
in Rami's voice, following the fixed three-section format. **Never fabricate** —
every claim must trace to a researched source; if a source can't be read, say so
and ask.

## Inputs

Links grouped into three sections (a short note per link is welcome — use it):

```
open-source: <github or project url>   # one or more
learning:    <course / tutorial / video / docs url>   # one or more
book:        <book url>                 # one
issue:       <issue number>             # optional; for the "| Issue N" title
promo:       <optional course/promo link to feature after the intro>
```

If sections or links are missing, ask once, concisely. Don't proceed on guesses.
If the issue number is missing, ask for it (or infer the next number from the
most recent file in `style/examples/`).

## Output location

Drafts are written to the **user's current working directory** (where they
invoked the skill from), **never inside this skill's / plugin's folder**. The
files under this skill (`sections/`, `style/`, `templates/`, `scripts/`) are
read-only resources at runtime — only ever read them, never write next to them.

Resolve the output directory at the start of every run, before researching or
drafting:

1. **Read** the cwd's `CLAUDE.md` (if present). If it has a
   `## Skill output paths` section with a `newsletter-builder: <path>` bullet,
   use that path (relative to cwd). Skip to "Save".
2. **Otherwise** (no `CLAUDE.md`, or no `newsletter-builder` line in it), ask
   the user **once**, concisely:
   - Confirm the cwd is the right place (print it).
   - Propose `drafts/` as the default folder. Let them accept, pick another
     path, or save to the cwd directly.
   - Ask whether to **remember** the choice for future runs by adding a line to
     the cwd's `CLAUDE.md`. If yes:
     - Create `CLAUDE.md` if it doesn't exist.
     - If a `## Skill output paths` section already exists, append a bullet to
       it. Otherwise append the section at the end:
       ```markdown
       ## Skill output paths

       - newsletter-builder: <chosen-path>
       ```
     - Do **not** rewrite or reorder the rest of `CLAUDE.md`.
   - Create the chosen folder if it doesn't exist, then proceed.
3. **Safety net:** if the cwd looks like a clone of this marketplace repo (it
   contains `source/plugins/` or `.claude-plugin/marketplace.json`), refuse to
   write there by default — ask the user for an explicit output directory
   outside the marketplace before continuing.

## Workflow

Run these in order. Load the voice **before** drafting (step 4 reads `style/`),
so sections are written in voice from the first draft, not just polished at the end.

1. **Parse** — sort the provided links into the three sections; attach any note.

2. **Research each link** — gather facts; never invent them.
   - **GitHub repos**: run `python3 scripts/research.py github <url>` for metadata
     (stars, language, license, topics, description, default branch, README raw
     URL). Then read the README via WebFetch on the `readme_raw` URL it prints
     (raw.githubusercontent.com is fetchable even when the repo page isn't).
   - **Books**: run `python3 scripts/research.py book <url-or-isbn>` — it pulls
     clean metadata (title, authors, publisher, description) and renders the page
     when needed. Works for O'Reilly, publisher, and Amazon links.
   - **Other pages** (courses, tutorials, videos, docs): try WebFetch first.
   - **Fetch-hostile pages**: JavaScript apps and bot-protected sites (e.g.
     O'Reilly, Coursera, Udemy, many publisher pages) return a redirect, a 403,
     or an empty shell to a plain fetch. When WebFetch yields nothing usable, run
     `python3 scripts/research.py render <url>` — it renders the page (runs its
     JS) and returns clean Markdown, like a browser would. Read that output and
     extract the facts.
   - **If even rendering fails**: tell the user and ask them to paste the key
     details. Never guess.
   - **Many links (> 4 total)**: dispatch one research subagent per link in
     parallel (Task tool, general-purpose) to keep the main context clean; each
     returns a compact fact sheet. With few links, research inline.

3. **Draft each section** — read its format spec and follow it exactly:
   - `sections/open-source.md` (the fullest section)
   - `sections/learning.md` (intentionally shorter)
   - `sections/book.md` (medium)

4. **Voice pass** — read `style/voice-guide.md` and the issues in
   `style/examples/`, then revise every section to match that voice. Apply the
   guide's "Avoid" list (no hype adjectives, no marketing language).

5. **Assemble** — use `templates/newsletter-template.md`: intro, the three
   sections in the **fixed order** (Open Source → Learning → Book), sign-off.
   Never reorder sections.

6. **QA** — run the checklist below and fix issues. Then run
   `python3 scripts/research.py validate <draft>` (structural check) and
   `python3 scripts/research.py check <urls>` (confirm links resolve).

7. **Save** — write to `<output-dir>/issue-YYYY-MM-DD.md` where `<output-dir>`
   is the path resolved in **Output location** above (default `drafts/`,
   relative to cwd; date = today). Create the folder if it doesn't exist.
   **Never write inside the skill / plugin folder.** Print the absolute path
   and a short note of what QA changed.

## QA checklist

- **Structure**: all three sections present, correct order, correct headings;
  intro and sign-off present.
- **Content**: every claim traces to a researched source; no hallucinated
  features; each item has a working link; the book has title **and** author.
- **Style**: matches `style/voice-guide.md`; section lengths within their ranges
  (open-source fullest, learning shortest, book medium); no banned phrases; no
  repeated openers across sections.

Output `PASS`, or a bulleted `FAIL` list, and fix before saving.

## Research helper — `scripts/research.py` (zero-dependency, stdlib)

- `python3 scripts/research.py render <url>` — render a fetch-hostile page (JS
  apps / bot-blocked sites) and print clean Markdown.
- `python3 scripts/research.py book <url-or-isbn>` — clean book metadata
  (Google Books, with a render fallback).
- `python3 scripts/research.py github <repo-url>` — repo metadata as JSON.
- `python3 scripts/research.py check <url> [url ...]` — HTTP status per link.
- `python3 scripts/research.py validate <draft.md>` — offline structural check
  (exit 0 = PASS).

Network subcommands are **best-effort**; if they fail, try another or ask the
user. `render`/`book` route through the public r.jina.ai reader — fine for public
pages, not for anything private. `validate` is offline and deterministic.

## Notes

- The voice guide is the source of truth and is refined whenever new issues are
  added to `style/examples/` — re-read it each run.
- Keep it factual, concrete, and concise. Substance over adjectives.
