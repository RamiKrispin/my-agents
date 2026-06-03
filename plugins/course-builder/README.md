# course-builder

Build a **course** from idea to finished materials, stage by stage — with a
`spec/` folder as the source of truth, continuity tracking across stages,
named style **profiles**, and an independent QA pass.

> Building a workshop instead? Use the sibling
> [workshop-builder](../workshop-builder/README.md) plugin (single combined
> deck by default, slides under `slides/`, no scripts, opt-in topic READMEs).

Install: `/plugin install course-builder@my-agents` · Start: `/course`

## What's in this plugin

| Component | Type | Role |
| --- | --- | --- |
| `course-builder` | skill | **Orchestrator.** Runs discovery → writes the spec → builds stage-by-stage with your checkpoints. Holds the templates, profiles, and conventions. |
| `course-content-creator` | subagent | Builds **one stage** (a chapter) from the approved spec — READMEs, scripts, code/assets, and slides. |
| `course-qa` | subagent | **Independent** reviewer of each stage: scope, technical accuracy, pedagogy, naming, terminology, voice, and cross-stage continuity. |
| `course-slide-deck` | skill | Renders the HTML decks (ported, theme-aware; one deck per lesson). |
| `/course` | command | Entry point to start or continue a build. |

## What this plugin produces

| | **Course** |
| --- | --- |
| Unit | chapter → lessons |
| Scripts | yes (`script/ch{N}/script_c{N}_l{M}.md`) |
| Slides | one deck **per lesson** |
| Folders | `chapter_{N}/l{M}/` |

## The `spec/` folder (source of truth)

All development docs live in `spec/` inside your **course repo** (not the
marketplace):

- `course-spec.md` — overview, requirements, profile, structure, build mode,
  implementation plan + status.
- `naming-convention.md` — folder/file/title rules.
- `learning-goals.md` — syllabus.
- `continuity.md` — the **continuity ledger + promise tracker** (below).
- `open-items.md` — blockers / deferrals / follow-ups.
- `scope-chapter-{N}.md` — per-chapter scope, written just before building.

Because the spec — not the chat — is authoritative, builds are **resumable**: stop
after Chapter 2, build Chapter 3 next week, and the thread holds.

## Continuity across stages

Building one stage at a time risks losing the thread. `spec/continuity.md` prevents
that:

- **Ledger** — what each completed stage introduced (concepts, terms, the running
  example's state).
- **Promise tracker** — each stage's forward promise ("next chapter we move to
  testing"); the next stage must fulfill it, and QA verifies it.
- Every build step reads it first; transition rules (recap opener + forward-bridge
  close) live in the profile voice guide.

## Profiles (voice + slide style, coupled)

A **profile** sets the course identity. Selected at the spec stage; default
`design-principles`.

- **`design-principles`** — principle/workflow teaching voice, distilled from a
  real Docker-for-AI course (includes example scripts).
- **`default`** — neutral instructional voice.

Add your own under `skills/course-builder/profiles/<label>/`, or override per repo
with a `spec/style/` folder. See `skills/course-builder/profiles/README.md`.

## Build modes

- **Step-by-step** (default) — one stage at a time, with a review checkpoint
  between each.
- **All-at-once** — build every stage in sequence, then one final review (QA +
  continuity still run per stage).

## Workflow

1. **Discovery** → scope, audience, objectives, profile, materials, build mode.
2. **Architect** the structure (chapters/lessons); it challenges weak ordering.
3. **Write the spec** → **Checkpoint 1** (you approve).
4. **Per stage**: scope → content-creator → slides → QA → update continuity →
   **Checkpoint** (step-by-step).
5. **Wrap** — summary, open items, next steps.

## Conventions

This plugin follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on changes. See the repo `README.md` and
`docs/adding-a-plugin.md`.

## Reference

- `skills/course-builder/SKILL.md` — the orchestrator's full instructions.
- `skills/course-builder/references/{structure,conventions}.md` — layouts + naming.
- `skills/course-slide-deck/SKILL.md` — the slide engine and visual rules.
