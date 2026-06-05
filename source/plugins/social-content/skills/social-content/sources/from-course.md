# Source: course-builder output dir

How the skill ingests a finished (or in-progress) course-builder run as source
material for a social post. Goal: build a fact sheet of grounded claims with
file-path citations, then pick the most post-worthy angle.

## Expected layout

A course-builder run produces (see `course-builder/references/structure.md`):

```
spec/
  course-spec.md           overview, audience, objectives, profile
  learning-goals.md        the syllabus
  continuity.md            ledger across chapters
  scope-chapter-{N}.md     per-chapter scope
chapter_{N}/
  l{M}/
    README.md              lesson notes
    slides_c{N}_l{M}.html  one deck per lesson
    <supporting files>     Dockerfile, *.py, *.sh, *.drawio, DEMO.md, …
script/
  ch{N}/
    script_c{N}_l{M}.md    narration script
```

The user passes the **course root** (the dir that contains `spec/` and
`chapter_N/`).

## What to read

In order, with grep/glob — don't dump the whole tree:

1. **`spec/course-spec.md`** — establishes audience, objectives, framing, and
   the course's voice/profile. Read fully.
2. **`spec/learning-goals.md`** — the syllabus, gives the chapter→lesson
   structure.
3. **The chapter or lesson the user names** — usually they want a post about
   one specific concept covered. If they didn't say which, ask.
4. **The lesson's `README.md` and `script_c{N}_l{M}.md`** — the actual taught
   material, in their voice. The script is closest to spoken voice; the README
   is closest to reference material.
5. **Any `*.py`, `Dockerfile`, `*.sh`, `DEMO.md`** in the lesson folder — the
   concrete code/commands the lesson teaches. These are gold for "show, don't
   tell" posts.
6. **`spec/continuity.md`** — to learn what the lesson assumed (and what came
   before / after) so the post doesn't reference unintroduced concepts.

Keep what's **specific and concrete**: numbers, library names, filenames,
config values, before/after states. Drop the framing/transitions — those are
course-internal.

## Building the fact sheet

Produce 5-15 claims. Each claim has the exact text + a citation:

```
- Multi-stage Docker build cuts the image from 8GB to 900MB.
  → chapter_3/l2/Dockerfile, chapter_3/l2/script_c3_l2.md:42
- The slim base image used is `python:3.11-slim`.
  → chapter_3/l2/Dockerfile:1
- Cold start dropped from 90s to 12s after slimming.
  → chapter_3/l2/README.md:78
```

If a claim isn't in the source, drop it. If the user wants to make a claim that
isn't grounded, ask.

## Picking an angle

The same lesson can become several posts. Map the material to a template:

- **`list`** — "5 Dockerfile mistakes I see in AI projects" (when the lesson
  covers multiple parallel pitfalls or items).
- **`lesson`** — "I rebuilt the same environment 30 times to record this
  course. Docker Compose saved hours." (when the lesson has a behind-the-scenes
  story).
- **`contrarian`** — "Most Docker tutorials are wrong about layer caching."
  (when the lesson takes a stance against common practice).
- **`comparison`** — "Multi-stage vs single-stage Docker builds for ML"
  (when the lesson explicitly compares two approaches).

If the lesson cleanly fits one template, use it. If multiple fit, ask the user
which angle they want.

## What NOT to pull from the course

- The **course's own narrative voice** — that's optimized for a learner reading
  a chapter, not a scroller on LinkedIn. Keep the **facts**, drop the framing.
- Long code blocks — at most a 3-5 line snippet in the post.
- Anything from `spec/` that isn't a stable, learner-facing fact (e.g. status
  tables, open-items.md) — those are dev metadata.
