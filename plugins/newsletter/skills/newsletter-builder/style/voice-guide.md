# Voice & Style Guide

Derived from real issues of **Rami's Data Newsletter** (see `examples/`). This is
the source of truth for voice and structure — re-read it (and skim a couple of
examples) before drafting. When new issues are added to `examples/`, update this
file to match.

## Publication facts

- Name: **Rami's Data Newsletter**. Cadence: weekly, published **Saturday**.
- Tagline (italic subtitle under the title):
  _A weekly curated update on data science and engineering topics and resources._
- Also cross-posted on LinkedIn and Medium (linked in the intro — see template).
- Audience: data scientists, ML and data engineers, AI practitioners.

## Voice

- Informative and descriptive; positive but **not** hype-y. Let substance carry it.
- Explain **what a thing is and the problem it solves**, then how it works.
- Recurring framings (use naturally, don't overuse a single one):
  - "This week's focus is on the **{name}** project."
  - "Rather than {painful manual approach}, {project} {does X}."
  - "Instead of {assumption}, it demonstrates {better approach}."
  - "The goal is to {aim}."
  - Learning items: "The following {course/talk/video/tutorial} by {author} focuses on {topic}."
- Third-person product descriptions; light first person in framing ("I came across",
  "This week's focus").

## Formatting conventions

- **Title**: `{Highlight}, {Highlight} | Issue {N}` — a comma-separated teaser of the
  items, then the issue number. Always include `| Issue {N}`.
- **Section headings** (exact, in this fixed order):
  `## Open Source of the Week` → `## New Learning Resources` → `## Book of the Week`.
- **Sub-headings** within sections: `### Key Features`, `### Topics Covered`, and
  `### {Resource Name}` per learning item.
- **No emojis.**
- **Links are inline and usually bolded**, e.g. `Project repo: **[url](url)**`.
- Horizontal rules (`---`) separate the intro, each section, and the sign-off.
- Bullets in Key Features / Topics Covered open with a **bolded concept** then an
  em-dash and a short explanation: `- **Local deployment** — running models on…`.

## Fixed scaffolding (always present)

- **Intro**: `This week's agenda:` + three bullets (one per section), then the
  LinkedIn/Medium cross-post line. (See template for exact links.)
- Optional **promo block(s)** after the intro (e.g. a current LinkedIn Learning
  course) — include only if the user provides one; otherwise omit.
- **Sign-off** (verbatim):
  ```
  **Have any questions? Please comment below!**

  See you next Saturday!

  Thanks,

  Rami

  Thanks for reading Rami's Data Newsletter! Subscribe for free to receive new posts and support my work.
  ```

## Avoid

- Hype adjectives ("powerful", "cutting-edge", "revolutionary", "game-changing",
  "seamless") unless precise and earned.
- Marketing / back-cover language.
- Inventing features, topics, or facts not found in the source.
- Reusing the exact same opening sentence across the three sections.

## Refreshing the voice corpus

Run `python3 scripts/fetch-examples.py` (see its header) to re-pull recent issues
into `examples/`. Requires network access to `ramikrispin.substack.com`.
