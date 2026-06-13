# Format: Blog post (Substack / Medium-friendly Markdown)

A long-form article suitable for Substack, Medium, dev.to, or a personal
blog. The blog post **goes deeper** than any individual social post —
typically synthesizes multiple topics from the campaign and goes 800-2,500
words depending on configuration.

## Source of truth

This file is the canonical structural + voice spec for blog drafts. It
overrides the social `voice-guide.md` for long-form work — `voice-guide.md`
is explicitly scoped to LinkedIn / Reels / Threads / Bluesky / X.

The example posts under `profiles/default/examples/blog/*.md` are the
**voice corpus** for blog drafts. **Re-read every `*.md` exemplar in that
folder before drafting.** When the corpus and this scaffold disagree, the
exemplar wins on tone and rhythm; this scaffold wins on structure (length
targets, section order, CTA shape).

## Length

- **Configurable per blog** via `blog_length` in `campaign.md`.
- **Recommended targets:**
  - **800-1,200 words** — focused single-topic deep dive.
  - **1,500-2,000 words** — chapter-spanning synthesis (most common).
  - **2,000-2,500 words** — comprehensive reference (use sparingly; long blogs
    get skimmed).

## Title and subtitle

- **Title pattern:** `<Topic>: <Descriptor>` (colon-separated).
  - Good: `Introduction to SQL AI Agents: The Four Components Behind Natural Language SQL`
  - Bad: `Introduction to SQL AI Agents` (no descriptor — title doesn't tell a feed reader what's inside).
  - Bad: `SQL AI Agents — A Deep Dive` (em-dash + vague descriptor).
- **Subtitle pattern:** for a series, `Part N of <Series Name>` (Title Case
  series name). Example: `Part 1 of the Foundations of SQL AI Agents series`.
- For one-off posts (not a series), the subtitle is one descriptive sentence
  — NOT a punchy fragment. `Question in. Answer out.` is a LinkedIn hook,
  not a Substack subtitle.
- Title ≤ 80 chars (Substack and Medium both truncate around there in feed
  cards).

## Header casing

- All H2 and H3 use **Title Case**. `What Is a SQL AI Agent?`, not
  `What is a SQL AI agent?`.
- Components / chapters take Title Case nouns: `The Prompt Handler`,
  `The Four-Component Architecture` — not `The prompt handler` /
  `four-block architecture`.
- Prefer `components` over `blocks` when describing software architecture
  parts.

## Shape

A blog post follows this 5-section arc:

1. **Title + subtitle** — see "Title and subtitle" above.
2. **Lede (one paragraph)** — sets up the problem with a concrete scenario,
   names what the post will deliver, previews the takeaway. See "Lede shape"
   below.
3. **Definition section** — a single H2 (e.g. `What Is a <Thing>?`) that
   answers "what is the topic of this post" in 3-5 paragraphs. Include at
   least one blockquote example.
4. **Core body** — H2 sections, each covering one idea. Code blocks,
   diagrams (linked from `assets/`), comparisons, references. For
   architectural posts, a single H2 contains numbered H3 sub-sections (one
   per component).
5. **Closing Thoughts** — H3 (or H2) titled exactly `Closing Thoughts`.
   3-4 paragraphs: synthesis → caveat → forward-look to the next post.
6. **CTA** — the dual-course (or N-course) bullet list. See "CTA template".

## Lede shape

The lede is one fuller paragraph (4-7 sentences). NOT a punchy 2-sentence
opener.

It must:

1. Name the **problem domain** in the first sentence (where the data /
   value lives).
2. Name **3 concrete stakeholder personas** by role — business stakeholders,
   support teams, product managers, analysts, engineers. Pick the 3 most
   relevant to the topic.
3. End on the **bottleneck / gap** — the human consequence of the problem.

Then a short 1-line bridge paragraph (`SQL AI agents emerged to bridge that
gap.`) followed by the rest of the intro.

**Course mention placement:** course is referenced **inline mid-lede**, not
as a byline tagline or separate sidebar:

> Many of these concepts are drawn from my LinkedIn Learning course,
> ***<Course Title>***, where <one-line outcome>.

The closing CTA still mentions the course(s) — see "CTA template".

## Component-section anatomy

For each component / chapter sub-section under a body H2:

```
### N. The <Component Name>

The <component> <one plain-prose sentence stating what it does>.

<1-2 detail paragraphs in full sentences. No bolded role tags at the start.>

<One short forward-looking closing sentence stating the consequence in
positive frame.>
```

Examples of the closing sentence (from the canonical exemplar):

- `Without it, the model is left to guess which tables and columns might exist.`
- `As models evolve, the architecture remains stable.`
- `It adds a small but important layer of reliability to the overall workflow.`
- `Without execution, generated SQL remains only a suggestion.`

## Closing Thoughts section

Three-part shape, in order:

1. **Synthesis** (1-2 paragraphs) — restate each component individually,
   then `Together, however, they enable …` to describe the emergent capability.
2. **Caveat / nuance** (1 paragraph) — `<X> alone is not enough` framing.
   The pattern: structure provides the form, but something else (context,
   data quality, governance, …) decides the outcome.
3. **Forward look** (1 paragraph) — name the **next post's topic** and the
   pivot, using an em-dash bridge:

   > In the next article, we'll explore that missing ingredient—context—
   > and why it is often the deciding factor between an impressive
   > demonstration and a genuinely useful SQL AI agent.

A standalone short paragraph (`That simplicity can be deceptive.`) is a
useful pivot device between parts 1 and 2.

## CTA template (verbatim — at the end of every post)

```markdown
---

**Interested in learning more about <topic>?**

If you'd like to dive deeper into <topic>, I've put together <N> LinkedIn Learning courses that cover the topic from beginner to advanced levels.

- **<Course 1 Title>** – an introductory course that <one-line outcome>.

- **<Course 2 Title>** – a more advanced course focused on <one-line outcome>.

Whether you're just getting started or thinking about production use cases, I hope you'll find them helpful.
```

Notes:

- The horizontal rule (`---`) separates the closing-thoughts forward-look
  from the CTA.
- The CTA has **no emojis** (no 📌, 🚀, 🎓 — none).
- Course titles are bolded with the en-dash `–` (not em-dash) before the
  description.
- For single-course campaigns, drop the second bullet and adjust the
  intro line (`I've put together a LinkedIn Learning course that …`).
- For 3+ course campaigns, expand the bullet list and adjust the count.

## Voice (long-form)

These rules override the social `voice-guide.md` for blog drafts.

### Sentence rhythm

- **Complete sentences predominate.** Fragments allowed but **rare** —
  if you find more than 3 fragment-only sentences in a 1,200-word body,
  rewrite. Save the staccato fragment rhythm for LinkedIn / social posts.
- **Em-dashes are sparing**, not the dominant rhythm device. Commas and
  full stops carry most of the cadence. One em-dash per ~3 paragraphs is
  the right density.
- **No bolded role one-liners** at the start of a section
  (`**assembles the prompt the model sees**`). The opener is plain prose.

### Word choice

- **Components**, not blocks (when describing software architecture).
- **Lightweight application**, not "thin program".
- **Remarkably simple / remarkably effective** is fine; **revolutionary /
  game-changing / next-gen** are not (same banned-word list as social).

### Use cases

Use **abstract industry-grade categories**, NOT specific deployment
patterns:

- Good: `internal analytics assistants`, `natural-language reporting`,
  `conversational analytics in products`, `accelerate analysts' work`.
- Bad: `Slack bot for the data team`, `SaaS NL-query feature`,
  `support engineers querying operational data`.

### Example questions

Each on its **own line as a blockquote**, italic optional:

```markdown
People naturally express questions in business language:

> *How many retail orders did we receive last quarter?*

Databases, on the other hand, require precise instructions...
```

NOT inline as a comma-separated list of three italicized questions.

### Decoration & inline formatting

- **No body emojis.** Not in headers, not in CTAs, not in pull-quotes.
- **No styled callout boxes.** If a sentence is important enough to
  pull-quote, work it into flow prose. (HTML-rendered drafts must not use
  `.callout` divs either.)
- **Minimal inline code** in the body. Prefer **bold** for emphasis (e.g.
  `**right SQL for your data**`) and *italics* for example phrasing or
  quoted questions. Inline `<code>` is fine for the rare technical literal
  (a function name, a CLI flag) but not the default emphasis tool.
- Section transitions can use **bridge sentences** as their own short
  paragraph:
  - `That distinction is important.`
  - `That simplicity can be deceptive.`
  - `Despite the excitement surrounding AI agents, …`

### Banned patterns (block in QA)

- `Skip this step and …` failure-frame closers. **Removed in editing every
  time.** Use forward-frame positive closers instead (see
  "Component-section anatomy").
- `It is not a framework. It is not a product.` style negation chains.
- Multiple inline italicized examples in a single sentence
  (`*example 1*, *example 2*, *example 3*` — break into blockquotes).
- Body emojis (the social emoji whitelist does NOT carry over to long-form).
- Styled callouts (`.callout`, `> [!INFO]`, etc.).

## Output structure

```markdown
---
title: <Topic>: <Descriptor>
subtitle: Part N of <Series Name>
date: 2026-MM-DD
tags: [tag1, tag2, tag3]
---

# <Topic>: <Descriptor>

*Part N of <Series Name>*

<Lede paragraph — 4-7 sentences, 3 stakeholder personas, lands on the bottleneck.>

![<Alt text>](assets/<slug>-<n>.png)

<1-line bridge paragraph.>

<Definition / setup paragraphs — include at least one blockquote example.>

> *<Example question or quote>*

<More setup, ending with the inline course mention paragraph.>

## What Is a <Topic>?

<3-5 paragraphs defining the thing. At least one blockquote example.>

## The <N>-Component Architecture of a <Topic>

<Intro paragraph.>

![<Architecture diagram alt text>](assets/<slug>-architecture.png)

<Bridge paragraph: simplicity is the strength, etc.>

Let's examine each of these components in turn.

### 1. The <Component Name>

<Opening sentence — plain prose, no bold tag.>

<1-2 detail paragraphs.>

<Forward-frame closing sentence.>

### 2. The <Component Name>

<...>

### 3. The <Component Name>

<...>

### 4. The <Component Name>

<...>

### Closing Thoughts

<Synthesis paragraph 1.>

<Bridge — a short standalone paragraph like "That simplicity can be deceptive.">

<Caveat / nuance paragraph.>

<Forward-look paragraph teasing the next post.>

---

**Interested in learning more about <topic>?**

If you'd like to dive deeper into <topic>, I've put together two LinkedIn Learning courses that cover the topic from beginner to advanced levels.

- **<Course 1 Title>** – an introductory course that <one-line outcome>.

- **<Course 2 Title>** – a more advanced course focused on <one-line outcome>.

Whether you're just getting started or thinking about production use cases, I hope you'll find them helpful.
```

The frontmatter is YAML (Substack tolerates it; Medium ignores it but
imports cleanly).

## Length-and-depth alignment

- For a `blog_length: 800` post: 1 lede paragraph + 1 definition H2 + 2-3
  body H2/H3s + Closing Thoughts + CTA. No more.
- For `blog_length: 1500`: 1 lede paragraph + 1 definition H2 + 1
  architecture H2 with 4 H3 sub-sections + Closing Thoughts + CTA. (This is
  the canonical exemplar's shape.)
- For `blog_length: 2000+`: add a worked-example H2 between architecture
  and Closing Thoughts, OR add a 5th component, OR add a "Common Pitfalls"
  H2. Don't expand the lede.

The lede is fixed-length regardless. Long ledes lose readers.

## Anti-patterns

- **Don't open with a punchy fragment hook** ("Question in. Answer out.")
  — those are LinkedIn hooks, not Substack ledes.
- **Don't open with "In this post, we'll explore…"** — open with the
  problem.
- **Don't pad** — 1,800 words of substance beats 2,500 words of filler.
- **Don't repeat the LinkedIn post verbatim** — readers who came from the
  LinkedIn promo expect new depth.
- **Don't bury the takeaway** — it goes in the lede AND in Closing Thoughts.
- **Don't use "Skip this step and …" closers.** They get edited out every
  time. Use forward-frame closers.
- **No hashtag block at the end** — those are for social posts, not blogs.
  The `tags:` frontmatter is for the platform; that's enough.
- **No "Hope this helps! 👋"** sign-offs — Closing Thoughts IS the sign-off.
- **No emojis in body, headers, or CTAs.**
- **No styled callout boxes.**
- **No inline-italics-list-of-3 example questions** — break into
  blockquotes.

## Substack / Medium compatibility checklist

- Frontmatter is YAML between `---` (Substack: ignored on import; Medium:
  ignored). Either platform handles the body's standard Markdown.
- Code blocks fenced with backticks + language tag (Substack and Medium
  both render syntax highlighting).
- Inline links use `[text](url)` (universal).
- Images: link from `assets/<slug>-<n>.png`; the user uploads them when
  publishing. Reference in Markdown as `![alt](assets/...)`.

## Validation

No automated validator. QA checklist:

- Title ≤ 80 chars, follows `<Topic>: <Descriptor>` colon pattern.
- Subtitle is `Part N of <Series>` for a series, or one descriptive
  sentence for a one-off — never a fragment hook.
- All H2 / H3 in Title Case.
- Lede is one paragraph, names ≥3 stakeholder personas, ends on the
  bottleneck.
- Inline course mention exists in the lede block.
- Each component sub-section follows opener → detail → forward-frame
  closer.
- Zero `Skip this step and …` closers.
- Closing Thoughts present, named exactly that, with synthesis + caveat +
  forward-look.
- CTA matches the verbatim template above (heading, intro line, bullet
  list, closing line).
- No body emojis.
- No styled callouts.
- Word count within 10% of `blog_length`.
- All concrete claims trace to the campaign's master fact sheet (no
  fabrications).
