# Format: Blog post (Substack / Medium-friendly Markdown)

A long-form article suitable for Substack, Medium, dev.to, or a personal
blog. The blog post **goes deeper** than any individual social post —
typically synthesizes multiple topics from the campaign and goes 800-2,500
words depending on configuration.

## Length

- **Configurable per blog** via `blog_length` in `campaign.md`.
- **Recommended targets:**
  - **800-1,200 words** — focused single-topic deep dive.
  - **1,500-2,000 words** — chapter-spanning synthesis (most common).
  - **2,000-2,500 words** — comprehensive reference (use sparingly; long blogs
    get skimmed).

## Shape

A blog post follows a standard 5-section arc:

1. **Title + subtitle** — concrete, searchable, optimized for click-through
   from a Substack / Medium feed. The title is NOT a clickbait hook; it's a
   descriptive label. The subtitle does the hook work.
2. **Lede (first 2-3 paragraphs)** — sets up the problem with a concrete
   scenario, names what the post will deliver, and previews the takeaway.
   This is what a reader sees in the email preview.
3. **Body (the bulk)** — H2 sections, each covering one idea. Code blocks,
   diagrams (linked from `assets/`), comparisons, references. This is where
   the depth lives that the social posts couldn't carry.
4. **Concrete example / walkthrough** — at least one section that does the
   thing end-to-end with code. Readers came for substance.
5. **Conclusion + CTA** — the takeaway in 2-3 sentences. Then a soft course
   CTA pointing readers to the full chapter / course.

## Voice

- **More instructional** than social posts. You can use sub-headings, bulleted
  lists, code blocks, and tables freely.
- **Same voice rules** — concrete, no hype, no banned phrases, no AI-flat
  prose. First-person where the lesson came from real work.
- **Code blocks** — fenced, language-tagged, runnable when possible. Don't
  inline pseudocode without saying "(pseudocode)".
- **Citations** — when referencing the course or external sources, link
  inline. Substack and Medium both render Markdown links.

## Output structure

```markdown
---
title: <Title — descriptive, searchable, ≤ 80 chars>
subtitle: <One-line hook — what this post delivers>
date: 2026-MM-DD
tags: [tag1, tag2, tag3]
---

# <Title>

<Subtitle / first hook line>

<Lede — 2-3 paragraphs. Concrete scenario, problem, what this post delivers.>

## <H2 Section 1 — first idea>

<Prose. Possibly a bulleted list.>

```python
# code block when relevant
```

## <H2 Section 2 — next idea>

...

## <H2 — concrete walkthrough>

<End-to-end example with code.>

## Takeaway

<2-3 sentence wrap-up.>

---

*Want the full course? <Course title and link.> The full chapter on
{topic} covers everything above plus {what's deeper in the course}.*
```

The frontmatter is YAML (Substack tolerates it; Medium ignores it but
imports cleanly).

## Length-and-depth alignment

- For a `blog_length: 800` post: 1 H2 of context + 2-3 H2s of body + 1
  conclusion. No more.
- For `blog_length: 1500`: 1 lede paragraph + 4-5 H2s + 1 walkthrough + 1
  conclusion.
- For `blog_length: 2000+`: add a 6th body H2 or expand the walkthrough,
  not the lede.

The lede is fixed-length regardless. Long ledes lose readers.

## Anti-patterns

- **Don't open with "In this post, we'll explore..."** — that's a 1990s
  blog tic. Open with a concrete scenario or problem.
- **Don't pad** — 1,800 words of substance beats 2,500 words of filler.
- **Don't repeat the LinkedIn post verbatim** — readers who came from the
  LinkedIn promo expect new depth.
- **Don't bury the takeaway** — it goes in section 1 (preview) AND section
  N (conclusion).
- **No hashtag block at the end** — those are for social posts, not blogs.
  The `tags:` frontmatter is for the platform; that's enough.
- **No "Hope this helps! 👋"** sign-offs — the takeaway IS the sign-off.

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
- Title ≤ 80 chars, descriptive (not clickbait).
- Lede has a concrete problem in paragraph 1.
- Word count within 10% of `blog_length`.
- At least one walkthrough section with code or a worked example.
- One soft course CTA at the end. No mid-body promo blocks.
- No banned phrases (same list as `voice-guide.md`).
