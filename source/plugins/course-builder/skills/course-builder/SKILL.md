---
name: course-builder
description: Build a course from idea to finished materials, stage by stage. Use when creating course content — running discovery, writing a spec as the source of truth, then generating chapters/lessons with scripts, slides, and code, plus an independent QA pass.
---

# Course Builder

Produce a course the way a small production team would: a **spec is the source
of truth** (not the chat), work proceeds **one stage at a time**, and every
stage is built by a content creator and checked by an **independent** QA
reviewer. Continuity across stages is tracked in `spec/continuity.md` so later
stages correctly reference earlier ones.

**Never fabricate.** Technical content must trace to the referenced repo/materials;
if something can't be verified, ask or flag it.

> Building a workshop instead? Use the sibling
> [workshop-builder](../../../workshop-builder/) plugin (single combined deck
> by default, slides under `slides/`, no scripts, opt-in topic READMEs).

## Output location

Course outputs (`spec/`, `chapter_{N}/`, `script/`, slides, supporting files)
are written to the **user's current working directory** — the target course
repo — **never inside this skill's / plugin's folder**. The files under this
skill (`templates/`, `profiles/`, `references/`) are read-only resources at
runtime; only ever read them, never write next to them.

Resolve the output base directory at the start of every run, before scoping or
building:

1. **Read** the cwd's `CLAUDE.md` (if present). If it has a
   `## Skill output paths` section with a `course-builder: <path>` bullet, use
   that path as the course root (relative to cwd, or absolute). Skip to "build".
2. **Otherwise** (no `CLAUDE.md`, or no `course-builder` line in it), ask the
   user **once**, concisely:
   - Confirm the cwd is the right course repo (print it).
   - Offer a default of `.` (the cwd itself, since course outputs are top-level
     folders in the target repo). Let them pick a subdirectory if they prefer.
   - Ask whether to **remember** the choice for future runs by adding a line to
     the cwd's `CLAUDE.md`. If yes:
     - Create `CLAUDE.md` if it doesn't exist.
     - If a `## Skill output paths` section already exists, append a bullet to
       it. Otherwise append the section at the end:
       ```markdown
       ## Skill output paths

       - course-builder: <chosen-path>
       ```
     - Do **not** rewrite or reorder the rest of `CLAUDE.md`.
   - Create the chosen folder if it doesn't exist, then proceed.
3. **Safety net:** if the cwd looks like a clone of the my-agents marketplace
   repo (contains `source/plugins/` or `.claude-plugin/marketplace.json`),
   refuse to write there by default — ask the user for an explicit course
   directory outside the marketplace before continuing.

All paths in the rest of this skill (`spec/...`, `chapter_{N}/...`,
`script/...`) are interpreted relative to that resolved output base.

## What this skill produces

| | **Course** |
|---|---|
| Unit | chapter → lessons |
| Scripts | yes (`script/ch{N}/script_c{N}_l{M}.md`) |
| Slides | one deck **per lesson** |
| Folders | `chapter_{N}/l{M}/` |
| Assets | in the lesson folder |

See `references/structure.md` for the exact output layout and
`references/conventions.md` for naming/title rules.

## The `spec/` folder (source of truth)

All development docs live in `spec/` in the target repo (create it if absent):

- `course-spec.md` — overview, requirements, profile, structure, build mode,
  and the implementation plan + status.
- `naming-convention.md` — folder/file/title rules.
- `learning-goals.md` — the syllabus.
- `continuity.md` — the continuity ledger + promise tracker (see below).
- `open-items.md` — blockers, deferrals, follow-ups.
- `scope-chapter-{N}.md` — per-chapter scope, written just before building.

Templates for all of these are in `templates/course/`.

## Profiles (voice + slide style, coupled)

A **profile** sets the course identity: writing voice + slide theme + examples.
Profiles live in `profiles/`; the default is **`design-principles`** (distilled
from a real Docker-for-AI course). Discovery picks one. A target repo may override
it with a `spec/style/` folder (wins if present). Voice and slide style are
coupled by default.

## Workflow

### 1. Discovery
Ask, then record the answers:
- Scope / topic, audience, prerequisites, objectives, duration/format.
- **Profile** (default `design-principles`).
- Materials: source repo, existing code, slide/style templates, anything to reuse.
- **Build mode:** *step-by-step* (one stage at a time, checkpoint between each —
  default) or *all-at-once* (build every stage in sequence, one final review;
  QA + continuity still run per stage).
Ask anything missing as concise clarifying questions. Don't proceed on guesses.

### 2. Architect the structure
Propose the chapter/lesson breakdown. **Challenge weak structures** — flag a
concept used before it's introduced, mis-ordered dependencies, or a lesson
that's out of scope, and recommend a fix. The user can approve, revise, or
redirect.

### 3. Write the spec  →  **CHECKPOINT 1**
Fill the templates into `spec/`. Initialize `continuity.md` (empty ledger;
record the planned per-stage forward promises from the structure) and set the
status table (all stages `pending`). **Stop for the user to approve the spec.**

### 4. Build, per stage  (respect the build mode)
For each chapter, in order:

  a. **Stage scope**: write `spec/scope-chapter-{N}.md`. In *step-by-step* mode
     this is a **CHECKPOINT 2** (approve the scope).
  b. **Content** — dispatch the **course-content-creator** subagent for this
     stage (it reads the spec, scope, continuity, profile, and the prior stage,
     then produces READMEs, scripts, assets, and slides via the
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

- `templates/course/` — all spec + content templates.
- `profiles/<name>/` — voice guide, examples, slide style (the course identity).
- `references/structure.md`, `references/conventions.md` — layouts and naming.
- The companion **course-slide-deck** skill renders the slides.
