# Source: URL (video, article, blog post, podcast)

When the user gives a URL as the source — e.g. *"make a LinkedIn post about
this video: https://youtube.com/..."*. The skill researches the page, builds
a fact sheet from the actual content (title, author, key topics), and uses
that to draft. **Never paraphrase the URL into invented claims.**

This is the path for posts curating a single piece of external content —
typically a YouTube video, podcast episode, conference talk, blog post,
documentation page, or paper. A URL source naturally maps to the
`learning-resource` template, but `lesson` (extract one personal takeaway)
and `opinion` (commentary on the trend the link represents) are also fits.

## What to ask if anything's missing

- **The URL** — must be a public link the skill can reach.
- **Format** — LinkedIn (default) or Reels.
- **Template** — if not given, recommend one (`learning-resource` for a
  curation/signpost; `lesson` for a personal-takeaway frame; `opinion` for
  first-person commentary on the trend the URL represents).
- **Output location** — handled by the skill's standard `CLAUDE.md` flow.

Ask **once and concisely**. Don't loop.

## Research the URL — try WebFetch first

The skill must read the page before drafting. Default approach: WebFetch
with a focused prompt, e.g. *"Extract title, author/channel, publication
date, full description, and the chapter/section list."*

WebFetch works for plain HTML pages, README files, most blog posts, and
docs sites. It does **not** work for JS-heavy or bot-protected pages —
typically:

- YouTube, Vimeo (video metadata is hydrated by JavaScript)
- Coursera, Udemy, edX (course pages)
- O'Reilly, publisher landing pages
- Medium (in some cases)
- Twitter / X status pages
- Anything that returns "Sign in" / "Confirm you're not a bot"

When WebFetch returns a redirect, a 403, an empty shell, or just nav
chrome, fall back to:

```bash
python3 scripts/research.py render <url>
```

This routes through the public **r.jina.ai** reader, which renders the
page's JavaScript server-side and returns clean Markdown. Works well for
YouTube (title, channel, description, chapter list, pinned comment),
course pages, and similar fetch-hostile sites.

If even rendering returns nothing usable, **tell the user and ask** for
the title, author, and 3-7 bullets of substance. Never guess.

## Fact-sheet shape from a URL

Build a fact sheet — the skill's invariant is that every concrete claim
traces to a source.

**For a video / podcast / talk**, capture:

- **Title** — exact, with capitalization
- **Channel / author / creator** — the entity producing it
- **Series** — if part of a podcast / show / playlist
- **Published date** — if visible
- **Duration** — if visible
- **Chapters / sections** — verbatim chapter titles + timestamps
- **Concrete concepts named** — tools, libraries, demos, metaphors that
  appear in chapters or in the channel's own pinned comment
- **Caveats** — vendor framing, hype to avoid amplifying, mixed reception
  in the comments worth signposting honestly

**For an article / blog post / paper**, capture:

- **Title**, **author**, **publication / blog name**, **date**
- **Section headings** — verbatim
- **Concrete claims, libraries, numbers, version IDs** explicitly named
  in the text
- **Conclusion / takeaway** in the author's own framing

YouTube tip: the rendered output usually contains a `## Chapters` block
with each chapter as an H4 + timestamp. Treat that as the canonical topic
list. Don't invent chapters that aren't there. If a long video's chapter
list truncates in the rendered output, use only what rendered and flag
the gap in your caveats.

## Voice when curating a URL

- **Signpost, don't sell.** Name the source (channel, author), name the
  guest if any, name the topics. Don't write "must-watch", "amazing", or
  recommendation language unless the user explicitly asks for that
  framing.
- **Substance first.** Lead with the most concrete useful concept — not
  the marquee branding. A bonsai metaphor for code review is more
  interesting than a product version number.
- **Honest framing.** If the source is vendor-promotional, acknowledge
  what's substantive without amplifying the hype. If the user wants a
  neutral "here's what's covered" signpost, deliver that.
- **One paragraph + a topic checklist** is the canonical shape for a
  learning-resource-template post built from a URL — see real exemplars
  in the user's `posts/` folder when present (the per-post
  `linkedin.md` files are the source of truth for hook + structure).

## Mapping URL → template

| URL shape | Suggested template |
| --- | --- |
| Single video / podcast / talk to share | `learning-resource` |
| Single article / blog post / paper to share | `learning-resource` |
| URL where the user has a strong personal take | `opinion` |
| URL where the user wants to extract one takeaway | `lesson` |
| Multiple URLs compared (e.g. "X vs Y") | `comparison` |

If the URL doesn't fit, **ask the user** which template they want.

## Output expectations

Same as the other source guides — the skill produces a post draft
following the chosen template's example folder + the format scaffold.
The fact sheet is the rendered metadata + chapters/sections, optionally
trimmed to the most substantive items (skip filler like "Intro" or
"Welcome to the show" unless the post benefits from naming them).
