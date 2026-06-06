# Source: course folder (LinkedIn Learning / chapter_0 layout)

How campaign-builder ingests a course folder that doesn't follow the
course-builder convention — typically a LinkedIn Learning course or a
hand-organized course tree where metadata lives in `chapter_0/` instead of
`spec/`. The reference example is the user's Docker for Local AI course at
`/Users/ramikrispin/Personal/courses/docker-local-ai-11189001`.

For canonical course-builder output see `from-course-builder.md`. For
workshops see `from-workshop-builder.md`.

## Detection signal

```
<source>/chapter_0/learning_goals.md exists  (and no spec/course-spec.md)
```

## Layout (observed in the reference course)

```
chapter_0/
  learning_goals.md          # canonical course outline: chapter+lesson table
                             # with title and learning goal per lesson
  naming_convention.md       # internal — SKIP
  open_items.md              # dev metadata — SKIP

chapter_{N}/                 # N >= 1; one folder per chapter
  l{M}/
    README.md                # lesson notes (well-structured prose)
    slides_c{N}_l{M}.html    # one HTML deck per lesson
    <supporting files>       # Dockerfile, *.py, *.sh, DEMO.md, .dockerignore

script/
  ch{N}/
    script_c{N}_l{M}.md      # narration script — densest source of voice + facts

# (Optional) at the course root:
README.md                    # course overview, LinkedIn Learning URL, run instructions
docs/                        # architectural docs (overview, requirements)
pm/                          # project state, phase-by-phase architecture
<application code roots>     # the running example app the course builds — e.g.
                             # `rag/`, `clients/`, `notebooks/`, `tests/`,
                             # `docker/`, `config/`, `docker-compose.yaml`
```

The application code at the course root (the running example the course
builds) is **rich source material** — concrete files, real commands, real
configs. The campaign-builder should pull from these freely when a topic
is anchored to the running example.

## Ingestion order

For a campaign-level run:

1. **`chapter_0/learning_goals.md`** — the canonical syllabus. Read first
   to enumerate every chapter and lesson with its title and learning goal.
   This is the topic index.
2. **`chapter_0/open_items.md`** — read briefly to know which chapters or
   lessons are incomplete; skip those for the campaign or warn the user.
3. **`README.md`** at the course root if present — course title, audience,
   the official course URL (use as the lead-magnet target), and any
   "running the project" instructions (real commands worth quoting).

Then, scoped to the user's chapter / lesson / theme:

4. **`chapter_{N}/l{M}/README.md`** for each lesson in scope — prose,
   code blocks, real examples.
5. **`script/ch{N}/script_c{N}_l{M}.md`** for each lesson in scope — the
   densest source of voice and facts. Strip `[CLICK]` markers and live
   demo direction blocks.
6. **Supporting code** in the lesson folder — `*.py`, `Dockerfile*`,
   `*.sh`, `*.dockerignore`, `DEMO.md`. Concrete commands and config.
7. **Application code at the course root** — when a topic references the
   running example, read the actual source files (`rag/<module>/<file>.py`,
   `docker/Dockerfile_*`, `docker-compose.yaml`, etc.) for grounded
   commands and code snippets.

## What's different from course-builder layout

- **No `spec/` folder.** The course-spec equivalent is synthesized from
  `chapter_0/learning_goals.md` + the course-root `README.md`.
- **No `spec/scope-chapter-{N}.md` files.** The "chapter arc" must be
  inferred from the lesson titles in `learning_goals.md` and from each
  lesson's README opening paragraph (which is usually a goal-statement
  blockquote in this layout).
- **No `spec/continuity.md`.** Concept-introduction sequence must be
  inferred from lesson order. The campaign-builder should be careful not
  to reference concepts in early-campaign posts that the course only
  introduces later.

## Building the master fact sheet

Same shape as `from-course-builder.md`: 5-10 claims per topic with
citations + post-type tags. The reference Docker course is unusually
fact-dense — most lessons yield 8-10 grounded claims (numbers, exact
commands, file paths, quotable sentences from scripts).

## What to skip

- **`chapter_0/naming_convention.md`** — internal.
- **`chapter_0/open_items.md`** content beyond "is this lesson complete?".
- **`pm/` folder** at the course root — project-state docs, dev metadata.
- **`tests/` folder** — unless a campaign topic specifically covers
  testing, the test code is too technical for social posts.
- **Live-demo direction blocks** in scripts (`🎬 LIVE DEMO`, `[CLICK]`
  markers) — strip these.

## Edge cases

- **Lesson is empty / placeholder** — `chapter_0/open_items.md` will say
  so; warn the user and skip that lesson.
- **Course root has multiple application directories** (e.g. both `rag/`
  and `clients/`) — pull from whichever one a given lesson references.
- **A `DEMO.md` exists alongside the README** — both are fact sources;
  DEMO.md often has the exact command sequence to reproduce.
- **The course is in progress** — `chapter_0/open_items.md` says some
  chapters aren't done. Build the campaign from completed chapters only.

## Picking topic mappings

Same as `from-course-builder.md`: chapter scope → one topic per lesson;
lesson list → one topic per listed lesson; theme → propose 5-9 topics by
synthesizing across lessons.

Write the proposed topic list into `campaign.md` and stop for approval
before any drafts are written.
