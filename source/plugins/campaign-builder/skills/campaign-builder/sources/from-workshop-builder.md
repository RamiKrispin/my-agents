# Source: workshop-builder output dir

How campaign-builder ingests a workshop produced by the `workshop-builder`
plugin, scoped to the user's topic list / theme.

For courses see `from-course-builder.md`. For LinkedIn-Learning-style course
folders see `from-course-folder.md`.

## Detection signal

```
<source>/spec/workshop-spec.md exists
```

## Layout (read-only)

```
spec/
  workshop-spec.md           # title, audience, goal, profile, agenda settings,
                             # slide-split + topic-README preferences
  agenda.md                  # ordered topic table with folder names + goals
  continuity.md              # ledger of concepts introduced; promise tracker
  open-items.md              # dev metadata — SKIP for campaign use

NN_topic_name/               # numbered (01_, 02_, …) per the agenda
  README.md                  # ONLY if `Topic READMEs: on` in workshop-spec.md
                             # otherwise this folder may contain only code
  <supporting files>         # *.py, Dockerfile, *.sh, DEMO.md

slides/
  workshop_slides.html       # default: ONE combined deck, one section per topic
  # OR per-topic split (when `Slide split: per-topic` in workshop-spec.md):
  NN_topic_name.html
```

## Critical workshop differences (vs course-builder)

- **No `script/` tree.** Workshops have no narration scripts. Slides + topic
  READMEs are the only narrative artifacts. This means the source signal is
  thinner — the campaign-builder must lean more on the slide deck content
  and any code in topic folders.
- **Topic READMEs are opt-in.** Many workshop runs don't have them. When
  absent, the only per-topic prose comes from the slide deck section for
  that topic.
- **The slide deck is HTML.** Plain `read_text()` works, but the ingestion
  must extract the relevant section (between `<section>` markers labeled by
  topic) and skip styling.

## Ingestion order

For a campaign-level run, read in this order:

1. **`spec/workshop-spec.md`** — title, audience, goal, AND the
   `Slide split` and `Topic READMEs` preference fields. These tell you
   which downstream files exist.
2. **`spec/agenda.md`** — the ordered topic list. This is your topic index
   for a workshop campaign — the goal column is the compact "what this
   topic teaches" signal.
3. **`spec/continuity.md` ledger body** (skip the promise-tracker table) —
   canonical concepts.

Then, scoped to the user's requested topics / theme:

4. For each topic in scope:
   - **`NN_topic_name/README.md`** if it exists — prose, goal statement,
     "Recap & next" section. Direct campaign source.
   - **Supporting code** in `NN_topic_name/` — `*.py`, `Dockerfile`,
     `*.sh`, `DEMO.md` — concrete commands and config.
5. **`slides/workshop_slides.html`** (combined deck) OR
   **`slides/NN_topic_name.html`** (per-topic split) — find the section for
   each in-scope topic, extract bullet points, code samples, and headings.
   When topic READMEs are absent, this is the primary prose signal.

## When topic READMEs are absent

If `spec/workshop-spec.md` says `Topic READMEs: off`, most topic folders
won't have a README. The fact-extraction strategy then is:

- Pull the topic's slide deck section (HTML parse — look for
  `<section data-topic="NN_topic_name">` or the H2 heading matching the
  topic title).
- Extract bullet points, code blocks (`<pre><code>`), and any inline
  text. These become the topic's facts.
- For very thin slide content, ASK the user to paste 5-7 bullet points
  describing what the topic teaches. Don't invent.

## Building the master fact sheet

Same shape as `from-course-builder.md`: 5-10 claims per topic, each with a
citation and a "what kind of post this supports" tag. Across the full
scope, 20-40 claims total.

Workshops typically yield **fewer claims per topic** than courses (no
narration scripts), so the campaign tends to be tighter — usually 5-7
topics rather than 8-9.

## What to skip

- **`spec/open-items.md`** — dev metadata.
- **`spec/workshop-spec.md` implementation plan & status table** — dev
  metadata.
- **`spec/continuity.md` promise-tracker** — dev metadata; ledger body
  is fine.
- **HTML styling and slide chrome** when extracting slide content — only
  the inner text and code blocks matter.

## Picking topic mappings

The user's scope can be:

- **A specific topic name or number** (e.g. "topic 03_dockerfile") — one
  campaign topic per workshop topic.
- **A topic range** (e.g. "topics 02 through 05") — one per workshop
  topic in the range.
- **A theme spanning the whole workshop** — propose 5-9 campaign topics
  by synthesizing across the agenda; topic boundaries may not align with
  workshop topic boundaries.

Write the proposed topic list into `campaign.md` and stop for approval
before any drafts.
