Drop real posts here. One file per post. Each file is just the post text — no
frontmatter, no commentary. See `../README.md` for the full convention.

This folder defines the **learning resource** template — short curation posts
that surface a new course, tutorial, conference talks, or playlist, with a
one-line take and a topic list. This is the 20% **Curate** bucket of the
70/20/10 rule (see `../../pillars.md`).

## Shape (derived from the 5 seeded examples)

A learning-resource post is short (≈ 80-130 words) and almost always built from
these blocks, in this order:

1. **Hook line: `{Resource Name} 🚀`** (or `👇🏼` for conferences / talks).
   The 🚀 emoji is functional — it signals "new resource". Not optional in
   this template.
2. **One short paragraph** of context: who released it, when, why it matters.
   First-person framing is light — "This looks like a great resource…",
   "This includes discussion of…".
3. **Topic-list lead-in**: a single line such as
   `This {course / tutorial / one-hour course} by {author} covers the
   following topics:` or `The course covers the following topics:`
4. **Topic list** — `✅`-prefixed lines, one topic per line, **5-9 items**.
   Each item is short (2-6 words). No em-dash explanations — just the topic.
5. **Link line** with a functional emoji:
   - `📽️: <link>` for video / playlist / course (preferred for video).
   - `Playlist 📽️: <link>` is also fine.
   - For text resources, the link goes inline in the paragraph (see
     `2026-code-with-claude-talks.md`).
6. **Optional CTAs (use sparingly):**
   - `♻️ Please share if you find it useful` (engagement CTA — fine to include).
   - `🔔` notification nudge (use rarely — once every several posts).
   - `📌 Join 30k and subscribe to my newsletter to receive weekly updates 👇🏼`
     followed by the newsletter link — this is the 10% **Promo** slot and
     counts against that budget.
7. **Hashtags** — 2-3, on their own line at the end, lowercase, no punctuation
   in between, e.g. `#ai #llm #datascience`, `#mlops #machinelearning
   #datascience`.

## What this template is NOT

- Not a **lesson learned** (no first-person "I tried X and learned Y" arc).
- Not a **contrarian** (no strong opinion to defend).
- Not a **comparison** (single resource per post, not a vs).
- Not a deep **list / top-N** post (that template covers comparative lists
  like "5 Python libraries for time series forecasting"). A learning-resource
  post is **one** resource with its **topic list** — not multiple resources.

## When to recommend this template

- The user found a course / tutorial / conference talks / playlist they want
  to share with their network.
- The source is a single named resource by one or more named authors.
- They want a short, scannable post — not a long opinion piece.
- It maps to the **Curate (20%)** bucket of 70/20/10. Track the running mix
  if multiple posts in a week are this template.

## Anti-patterns specific to this template

- **Don't invent the topic list.** Pull topics from the resource's actual
  syllabus / chapter list / table of contents. If they aren't accessible, ask
  the user to paste them.
- **Don't add a topic just to round out to "an even number".** 5 real topics
  beat 8 padded ones.
- **Don't write more than 1-2 sentences of context** before the topic-list
  lead-in. The list IS the value of this post; long context buries it.
- **Don't drop the 🚀.** It's the visual signal of the template — every
  example uses it (or the `👇🏼` variant for conferences).
