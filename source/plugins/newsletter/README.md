# newsletter

Draft a weekly data science newsletter from a set of links — in the author's
voice, in the fixed three-section format, with real web research and a QA pass.

Install: `/plugin install newsletter@my-agents` · Run: `/newsletter`

## What's inside

| Component | Type | Role |
| --- | --- | --- |
| `newsletter-builder` | skill | The pipeline: parse → research → draft → voice → assemble → QA → save. |
| `/newsletter` | command | Entry point — paste the links (open-source / learning / book). |

## The fixed format

**Open Source of the Week** → **New Learning Resources** → **Book of the Week**,
wrapped in the standard intro ("This week's agenda…" + cross-post line) and
sign-off ("See you next Saturday!"). Section order is fixed.

## How it works

1. Sort the links into the three sections.
2. **Research each link** — never fabricated:
   - GitHub repos: metadata + README via `scripts/research.py github`.
   - Fetch-hostile pages (O'Reilly, YouTube, many course/book pages): a
     JS-rendering reader via `scripts/research.py render`.
   - Books: `scripts/research.py book <url-or-isbn>` (Google Books → render fallback).
   - If a page can't be read, it asks you to paste details.
3. Draft each section per its spec (`sections/*.md`).
4. **Voice pass** against `style/voice-guide.md` + real past issues in
   `style/examples/`.
5. Assemble in the fixed order; run the QA checklist + `research.py validate`.
6. Save `drafts/issue-YYYY-MM-DD.md`.

## Voice

Derived from real issues in `skills/newsletter-builder/style/examples/`. Refresh
the corpus anytime: `python3 scripts/fetch-examples.py` (from the skill dir).

## Research helper — `scripts/research.py`

`render <url>` · `book <url-or-isbn>` · `github <url>` · `check <url…>` ·
`validate <draft.md>` (offline structural check).

## Conventions

Follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on changes. See the repo `README.md`.
