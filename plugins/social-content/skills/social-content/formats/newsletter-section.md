# Format: newsletter section

A draft of one section of the weekly newsletter, shaped to drop straight into
a `newsletter-builder` issue. Three sub-shapes — one per content type:

- **open-source** → `formats/newsletter-sections/open-source.md`
- **learning** → `formats/newsletter-sections/learning.md`
- **book** → `formats/newsletter-sections/book.md`

Those three files are the **canonical contract** and are owned by the
`newsletter` plugin (`newsletter/skills/newsletter-builder/sections/`). They
land here at build time via the `imports:` field in this plugin's
`plugin.yaml`. Read the type-specific spec for the chosen content type and
follow it exactly — it specifies the heading, paragraph framing, bullet
shape, link policy, and length.

## Choosing the type

When the user passes `newsletter-type: open-source | learning | book`, use
that. Otherwise classify from the source URL (skill step 3):

- **open-source** — `github.com`, `gitlab.com`, `codeberg.org`, package
  registries (`pypi.org`, `crates.io`), Hugging Face spaces.
- **book** — `oreilly.com`, `manning.com`, `packtpub.com`, `nostarch.com`,
  `amazon.com/.../dp/`, `books.google.com`, `goodreads.com`, or any URL with
  an ISBN-10 / ISBN-13 in the path.
- **learning** — anything else that fits a course / video / tutorial / talk
  / docs page (YouTube, Coursera, Udemy, freeCodeCamp, deeplearning.ai,
  Hugging Face Learn, fast.ai, kaggle.com/learn, official docs).

If the source is ambiguous (e.g. a GitHub repo for a course, a book whose
official site is `github.io`), **ask the user once** which slot it belongs
in — don't guess. If the user-supplied `newsletter-type:` disagrees with the
heuristic, trust the user and surface the mismatch as a one-line note.

## What goes in the body

The output file is the **literal section body** that would be inlined into a
newsletter issue under the matching heading — no metadata wrapper, no
`<details>` block, no slug bullets. The newsletter template (`## Open
Source of the Week`, `## New Learning Resources`, `## Book of the Week`)
supplies the H2; do **not** repeat it inside the body.

Read the matching imported spec for the exact Markdown shape. In short:

- **open-source** — bold project name lead, one-paragraph summary, "Project
  repo: **[<url>](<url>)**" line, `### Key Features` with 6–8 bolded
  capability bullets, optional docs line, `License: <SPDX>` line.
- **learning** — opener line, then 1–6 entries; each entry is `### Title`
  + 1–2 sentence summary + bare URL on its own line. No bullet lists inside
  entries.
- **book** — `*Title* by Author` lead, one-paragraph summary, `### Topics
  Covered` with 8–10 bolded topic bullets, "ideal for ..." audience line,
  publisher + Amazon links.

## Voice

Same source-of-truth as the rest of social-content:

1. `profiles/default/voice-guide.md`
2. `profiles/default/best-practices.md`
3. `profiles/default/pillars.md`

The newsletter is its own register (curator voice, third-person pivot, no
LinkedIn-style hook). The voice guide still rules — banned hype phrases
apply; functional emoji whitelist applies; substance over adjectives
applies. **Don't** open with a LinkedIn hook ("I spent 3 hours …"). **Do**
follow the section spec's framings (e.g. "Rather than {manual approach},
{project} {does X}").

## Output file

A single Markdown file per draft (these don't aggregate — each section is a
self-contained block intended to be inlined into a newsletter issue or kept
on disk for one). The skill's step 8 writes:

```
posts/<slug>-newsletter.md
```

where `<slug>` is the kebab-case slug from the request. Override the
filename via `group: <filename.md>` exactly as `linkedin` / `reels` do.

## QA

`scripts/validate_newsletter_section.py <type> <draft>` runs the structural
check for the chosen sub-shape. The full LinkedIn `validate.py` does **not**
apply — its rules (hook on line 1, 200–3000 char body, no headings) would
mis-fire on a newsletter section.

## Optional: inject into a newsletter pre-draft

After QA, the skill can drop the draft directly into a newsletter pre-draft.
The orchestration (when to prompt, which target to pick, which helper
invocation to make) is owned by `SKILL.md` step 9 — refer to it. The format
file deliberately doesn't repeat the workflow so the two can't drift.
