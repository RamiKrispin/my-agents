# Source: workshop-builder output dir

How the skill ingests a finished workshop-builder run as source material.
Workshops differ from courses (see `workshop-builder/references/structure.md`):
**no scripts**, **single combined deck by default**, topic READMEs are opt-in.

## Expected layout

```
spec/
  workshop-spec.md         overview, audience, objectives, profile
  agenda.md                topics in order
  continuity.md            ledger across topics
NN_topic_name/             numbered (01_, 02_, …)
  <supporting code/docs>   may or may not include README.md
slides/
  workshop_slides.html     ONE deck (default)
  # OR (per-topic variant):
  01_topic_name.html
  02_topic_name.html
  …
```

The user passes the **workshop root** (the dir that contains `spec/` and the
`NN_topic_name/` folders).

## What to read

1. **`spec/workshop-spec.md`** — audience, objectives, framing.
2. **`spec/agenda.md`** — full topic list with order and timing (timing matters
   for Reels: a 10-min topic is too dense for a 30s Reel).
3. **The topic the user names** (or ask). For each:
   - **`NN_topic_name/README.md`** if it exists (topic READMEs are opt-in in
     workshops — many runs won't have them).
   - **The topic's supporting files** — `*.py`, `Dockerfile`, `*.sh`, `*.md`,
     `*.drawio`. These carry the concrete content.
4. **`slides/workshop_slides.html`** (single combined deck) — find the section
   for the chosen topic. Workshop decks usually have section headers per topic.
   In per-topic variant, read `slides/NN_topic_name.html` directly.
5. **`spec/continuity.md`** — to know what the topic assumed.

## Building the fact sheet

Same as `from-course.md` — 5-15 grounded claims with file-path citations. The
only difference: workshop content is often **less narrative** (no scripts), so
slides + supporting code carry more of the load.

## Picking an angle

Workshops tend to be **practical and demo-driven**. Strong fits:

- **`list`** — top-N takeaways from the workshop or one topic.
- **`lesson`** — first-person story from running the workshop ("I ran this
  workshop with 80 engineers; here's what surprised me").
- **`comparison`** — when a topic explicitly compares approaches.

The `contrarian` template is harder to source from a workshop unless the
workshop itself takes a stance.

## What NOT to pull

- The workshop's spoken framing ("we'll now move to topic 3") — that's
  attendee-internal.
- Slide titles as post lines — they're often too terse to stand alone.
- Long code blocks — keep snippets under 5 lines for the post.
