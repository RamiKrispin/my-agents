---
name: course-builder
description: Build a course or workshop from idea to finished materials, stage by stage. Use when creating course/workshop content — running discovery, writing a spec as the source of truth, then generating chapters/lessons (or workshop topics) with scripts, slides, and code, plus an independent QA pass. Supports a course mode (chapters/lessons with scripts + per-lesson slides) and a workshop mode (agenda topics + one combined deck, no scripts).
---

# Course Builder

Produce a course or workshop the way a small production team would: a **spec is
the source of truth** (not the chat), work proceeds **one stage at a time**, and
every stage is built by a content creator and checked by an **independent** QA
reviewer. Continuity across stages is tracked in `spec/continuity.md` so later
stages correctly reference earlier ones.

**Never fabricate.** Technical content must trace to the referenced repo/materials;
if something can't be verified, ask or flag it.

## Two modes (decided in discovery)

| | **Course** | **Workshop** |
|---|---|---|
| Unit | chapter → lessons | agenda topics |
| Scripts | yes (`script/ch{N}/script_c{N}_l{M}.md`) | **no** |
| Slides | one deck **per lesson** | **one** deck for the whole workshop |
| Folders | `chapter_{N}/l{M}/` | `NN_topic_name/` (e.g. `01_intro`) |
| Assets | in the lesson folder | in the topic folder |

See `references/structure.md` for the exact output layout of each mode and
`references/conventions.md` for naming/title rules.

## The `spec/` folder (source of truth)

All development docs live in `spec/` in the target repo (create it if absent):

- `course-spec.md` **or** `workshop-spec.md` — overview, requirements, profile,
  structure, build mode, and the implementation plan + status.
- `naming-convention.md` (course) — folder/file/title rules.
- `learning-goals.md` (course) / `agenda.md` (workshop) — the syllabus / topic list.
- `continuity.md` — the continuity ledger + promise tracker (see below).
- `open-items.md` — blockers, deferrals, follow-ups.
- `scope-chapter-{N}.md` (course) — per-chapter scope, written just before building.

Templates for all of these are in `templates/course/` and `templates/workshop/`.

## Profiles (voice + slide style, coupled)

A **profile** sets the course identity: writing voice + slide theme + examples.
Profiles live in `profiles/`; the default is **`design-principles`** (distilled
from a real Docker-for-AI course). Discovery picks one. A target repo may override
it with a `spec/style/` folder (wins if present). Voice and slide style are
coupled by default.

## Workflow

### 1. Discovery
Ask, then record the answers:
- **Course or workshop?**
- Scope / topic, audience, prerequisites, objectives, duration/format.
- **Profile** (default `design-principles`).
- Materials: source repo, existing code, slide/style templates, anything to reuse.
- **Build mode:** *step-by-step* (one stage at a time, checkpoint between each —
  default) or *all-at-once* (build every stage in sequence, one final review;
  QA + continuity still run per stage).
Ask anything missing as concise clarifying questions. Don't proceed on guesses.

### 2. Architect the structure
Propose the chapter/lesson breakdown (course) or the agenda topics (workshop).
**Challenge weak structures** — flag a concept used before it's introduced,
mis-ordered dependencies, or a lesson that's out of scope, and recommend a fix.
The user can approve, revise, or redirect.

### 3. Write the spec  →  **CHECKPOINT 1**
Fill the mode's templates into `spec/`. Initialize `continuity.md` (empty ledger;
record the planned per-stage forward promises from the structure) and set the
status table (all stages `pending`). **Stop for the user to approve the spec.**

### 4. Build, per stage  (respect the build mode)
For each chapter/topic, in order:

  a. **Stage scope** (course): write `spec/scope-chapter-{N}.md`. In
     *step-by-step* mode this is a **CHECKPOINT 2** (approve the scope).
  b. **Content** — dispatch the **course-content-creator** subagent for this
     stage (it reads the spec, scope, continuity, profile, and the prior stage,
     then produces READMEs, scripts [course], assets, and slides via the
     **course-slide-deck** skill).
  c. **QA** — dispatch the **course-qa** subagent (independent review incl.
     continuity). If FAIL, hand findings back to a content pass and re-QA.
  d. **Update `spec/`** — append to `continuity.md` (what this stage established
     + its forward promise), update `open-items.md`, set the stage `complete` in
     the status table.
  e. **CHECKPOINT 3** (step-by-step only): user reviews the stage before the next.

In *all-at-once* mode, run a–d for every stage without stopping, then present the
whole build for one final review.

### 5. Wrap
Summarize what was built, open items, and suggested next steps.

## Continuity (`spec/continuity.md`)

The mechanism that makes staged building safe and resumable:

- **Ledger** — per completed stage: concepts/terms introduced, the running
  example's state.
- **Promise tracker** — each stage's forward promise ("next chapter we move from
  X to Y"); the next stage must fulfill it.
- Every build step reads this file first. Transition rules (recap opener +
  forward-bridge close) live in the profile voice guide; QA verifies them.

## Checkpoints (human-in-the-loop)

1. **Spec approved** before any building.
2. **Stage scope approved** (step-by-step).
3. **Stage reviewed** before the next (step-by-step).

Honor these unless the user chose all-at-once (then only the final review).

## Files in this skill

- `templates/course/`, `templates/workshop/` — all spec + content templates.
- `profiles/<name>/` — voice guide, examples, slide style (the course identity).
- `references/structure.md`, `references/conventions.md` — layouts and naming.
- The companion **course-slide-deck** skill renders the slides.
