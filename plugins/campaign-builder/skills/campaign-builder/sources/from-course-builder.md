# Source: course-builder output dir

How campaign-builder ingests a course produced by the `course-builder`
plugin, scoped to the user's chapter / lesson list / theme.

This guide is for the **course-builder canonical layout** — directories that
contain `spec/course-spec.md`. For LinkedIn-Learning-style course folders
that have no `spec/` and use `chapter_0/` instead, see
`from-course-folder.md`. For workshops, see `from-workshop-builder.md`.

## Detection signal

```
<source>/spec/course-spec.md exists
```

## Layout (read-only — do not modify the course)

```
spec/
  course-spec.md             # title, audience, goal, profile, chapter table
  learning-goals.md          # syllabus: chapter → lesson → "you will be able to…"
  continuity.md              # ledger of concepts introduced; promise tracker
  scope-chapter-{N}.md       # per-chapter scope, the why-before-what framing
  open-items.md              # dev metadata — SKIP for campaign use
  naming-convention.md       # internal — SKIP for campaign use

chapter_{N}/
  l{M}/
    README.md                # lesson notes; H1 starts "Chapter N — Lesson M: Title"
    slides_c{N}_l{M}.html    # one HTML deck per lesson
    <supporting files>       # Dockerfile, *.py, *.sh, DEMO.md — high-signal source

script/
  ch{N}/
    script_c{N}_l{M}.md      # narration script — the densest source of facts + voice
```

## Ingestion order

For a campaign-level run, **read in this order** to build the master fact
sheet:

1. **`spec/course-spec.md`** — title, audience, objectives, profile, the
   chapter table. Establishes the campaign's framing.
2. **`spec/learning-goals.md`** — the compact syllabus. This is the topic
   index — read this first to enumerate every lesson and its "you will be
   able to…" goal.
3. **`spec/continuity.md`** (ledger body only — SKIP the promise-tracker
   table; it's dev metadata) — canonical vocabulary and concept sequence
   to use correctly in campaign copy.

Then, scoped to the user's requested chapter / lessons / theme:

4. **`spec/scope-chapter-{N}.md`** for each chapter in scope — chapter arc
   and per-lesson scope summaries. Has why-before-what framing already
   written, which translates well to campaign hooks.
5. **`chapter_{N}/l{M}/README.md`** for each lesson in scope — prose, code
   blocks, Mermaid, the "What's next" bridge.
6. **`script/ch{N}/script_c{N}_l{M}.md`** for each lesson in scope — the
   densest source of facts and voice. Strip `[CLICK]` markers and `🎬 LIVE
   DEMO` direction blocks before quoting; treat demo blocks as separate
   "hands-on signal" content.
7. **Supporting code** in `chapter_{N}/l{M}/` (`*.py`, `Dockerfile*`,
   `*.sh`, `DEMO.md`) — concrete commands, file paths, and config that
   anchor posts.

## Building the master fact sheet

For each campaign topic (chapter or lesson, depending on the user's scope),
extract 5-10 grounded claims. Each claim has:

- **The claim itself** — concrete, specific (a number, a library name, a
  command, a file path, a quotable sentence from the script).
- **Citation** — `<source>/<file>:<line-range>` if useful, otherwise just
  the file path.
- **Tag** — which kinds of posts this claim best supports
  (`linkedin-hook`, `blog-deep`, `video-demo`, `comparison-data`).

Across the full scope, the master fact sheet typically has 20-40 claims
total — enough to source 5-9 topics with 5-10 claims each, with overlap.

## What to skip

- **`spec/open-items.md`** — dev metadata, blockers, deferrals. Not learner-
  or campaign-relevant.
- **`spec/naming-convention.md`** — internal file-naming rules.
- **The `## Implementation plan & status` table** in `course-spec.md` — dev
  status tracking.
- **`spec/continuity.md` promise-tracker table** — the "fulfilled by /
  status" column is dev metadata; the ledger body is useful but the
  tracker table itself is noise.
- **`[CLICK]` markers and `🎬 LIVE DEMO` direction blocks** inside scripts —
  strip these before using script text as campaign source. They're
  presentation cues, not content.
- **Course-internal narrative** ("we'll now move to chapter 3", "as we saw
  in lesson 2") — that's reader-internal framing for the course, not
  campaign-friendly copy.

## Picking topic mappings

The user's scope can be a chapter (e.g. "chapter 2"), a list of lessons
(e.g. "2.1, 2.3, 4.1"), or a theme that spans chapters (e.g. "Docker
multi-stage builds across chapter 2 and 5").

- **Chapter scope** — propose one topic per lesson (5-9 topics for most
  chapters). The chapter arc from `scope-chapter-{N}.md` becomes the
  posting order.
- **Lesson list scope** — one topic per listed lesson; user controls
  ordering at the checkpoint.
- **Theme scope** — propose 5-9 topics by reading `learning-goals.md` for
  every lesson that touches the theme, then synthesizing them into
  campaign-ready angles. Topic boundaries may not align with lesson
  boundaries.

In all cases: write the proposed topic list into `campaign.md` and **stop
for the user's approval** before any drafts are written.

## What this guide does NOT cover

- **Workshops** — `spec/workshop-spec.md` instead of `course-spec.md`. See
  `from-workshop-builder.md`.
- **Courses without `spec/`** (LinkedIn Learning style with `chapter_0/`
  metadata) — see `from-course-folder.md`.
- **Free-form topic** (no source course) — campaign-builder requires a
  source. For ad-hoc single posts use the `social-content` plugin's
  `from-topic.md` flow.
