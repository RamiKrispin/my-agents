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

1. Sort the values into the three sections. Each value is either a **URL**
   (researched in step 2) or a **prepared section file** — a local `.md`
   path produced by the `social-content` plugin's `format:
   newsletter-section` mode. Prepared files skip research + draft and are
   inlined verbatim into the matching slot.
2. **Research each URL link** — never fabricated:
   - GitHub repos: metadata + README via `scripts/research.py github`.
   - Fetch-hostile pages (O'Reilly, YouTube, many course/book pages): a
     JS-rendering reader via `scripts/research.py render`.
   - Books: `scripts/research.py book <url-or-isbn>` (Google Books → render fallback).
   - If a page can't be read, it asks you to paste details.
3. Draft each section per its spec (`sections/*.md`). Skip slots that came
   in as prepared files.
4. **Voice pass** against `style/voice-guide.md` + real past issues in
   `style/examples/`. Lighter editing on prepared sections — fix any drift,
   don't rewrite content the social-content skill already grounded.
5. Assemble in the fixed order; run the QA checklist + `research.py validate`.
6. Save `drafts/issue-YYYY-MM-DD.md`.

## Working with the social-content plugin

The `social-content` plugin can produce a section body shaped to drop
straight into a newsletter issue (`format: newsletter-section`). Two
integration paths:

- **Independent files:** `social-content` writes to
  `posts/<slug>-newsletter.md`. Pass that path to `/newsletter`:
  ```
  open-source: posts/exo-cluster-newsletter.md
  learning:    https://www.youtube.com/watch?v=...
  book:        https://www.oreilly.com/...
  ```
- **Direct injection:** `social-content` can also drop the section straight
  into a newsletter pre-draft (`drafts/issue-YYYY-MM-DD.md`), filling the
  matching slot and leaving the others as TODO placeholders. Run
  `/newsletter` on that pre-draft — the skill flesh-fills the missing
  sections from any URLs you add and leaves the prepared section alone.

The two plugins share the section format spec (`sections/*.md`) and the
assembly template (`templates/newsletter-template.md`) via the build's
`imports:` mechanism — single source of truth, both plugins always in sync.

## Voice

Derived from real issues in `skills/newsletter-builder/style/examples/`. Refresh
the corpus anytime: `python3 scripts/fetch-examples.py` (from the skill dir).

## Research helper — `scripts/research.py`

`render <url>` · `book <url-or-isbn>` · `github <url>` · `check <url…>` ·
`validate <draft.md>` (offline structural check).

## Conventions

Follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on changes. See the repo `README.md`.
