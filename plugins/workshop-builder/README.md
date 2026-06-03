# workshop-builder

Build a **workshop** from idea to finished materials, stage by stage — with a
`spec/` folder as the source of truth, continuity tracking across topics, named
style **profiles**, and an independent QA pass.

A sibling of [course-builder](../course-builder/README.md) focused on workshops:
**no scripts**, **a single combined slide deck by default**, slides under
`slides/`, and topic READMEs **only when you ask for them**.

Install: `/plugin install workshop-builder@my-agents` · Start: `/workshop`

## What's in this plugin

| Component | Type | Role |
| --- | --- | --- |
| `workshop-builder` | skill | **Orchestrator.** Runs discovery → writes the spec → builds topic-by-topic with your checkpoints. Holds the templates, profiles, and conventions. |
| `workshop-content-creator` | subagent | Builds **one topic** from the approved spec — supporting code/assets, the topic's slides (contributed to the combined deck or a per-topic file), and an optional README when requested. |
| `workshop-qa` | subagent | **Independent** reviewer of each topic: scope, technical accuracy, pedagogy, naming, terminology, voice, and cross-topic continuity. |
| `workshop-slide-deck` | skill | Renders the HTML deck(s). Single combined deck by default; per-topic split on request. |
| `/workshop` | command | Entry point to start or continue a build. |

## Defaults that differ from course-builder

| | **course-builder** | **workshop-builder** |
| --- | --- | --- |
| Unit | chapter → lessons | agenda topics |
| Scripts | yes | **none** |
| Slides | one deck per lesson | **one combined deck** (default) — split per topic on request |
| Slides location | inside the lesson folder | always under `slides/` (created if absent) |
| Topic README | always emitted | **only when the user asks** |

## The `spec/` folder (source of truth)

All development docs live in `spec/` inside your **workshop repo** (not the
marketplace):

- `workshop-spec.md` — overview, requirements, profile, structure, build mode,
  implementation plan + status, README + slide-split preferences.
- `agenda.md` — the ordered topic list.
- `continuity.md` — the **continuity ledger + promise tracker**.
- `open-items.md` — blockers / deferrals / follow-ups.

Because the spec — not the chat — is authoritative, builds are **resumable**: stop
after Topic 02, build Topic 03 next week, and the thread holds.

## Continuity across topics

Even within a single combined deck, building one topic at a time risks losing the
thread. `spec/continuity.md` prevents that:

- **Ledger** — what each completed topic introduced (concepts, terms, the running
  example's state).
- **Promise tracker** — each topic's forward promise ("next we move to deploying
  the model"); the next topic must fulfill it, and QA verifies it.
- Every build step reads it first; transition rules (recap opener +
  forward-bridge close) live in the profile voice guide.

## Profiles (voice + slide style, coupled)

A **profile** sets the workshop's identity. Selected at the spec stage; default
`design-principles`.

- **`design-principles`** — principle/workflow teaching voice, distilled from a
  real course (includes example scripts).
- **`default`** — neutral instructional voice.

Add your own under `skills/workshop-builder/profiles/<label>/`, or override per
repo with a `spec/style/` folder. See `skills/workshop-builder/profiles/README.md`.

## Build modes

- **Step-by-step** (default) — one topic at a time, with a review checkpoint
  between each.
- **All-at-once** — build every topic in sequence, then one final review (QA +
  continuity still run per topic).

## Workflow

1. **Discovery** → scope, audience, objectives, profile, materials, build mode,
   slide-split preference, README preference.
2. **Architect** the agenda (it challenges weak ordering).
3. **Write the spec** → **Checkpoint 1** (you approve).
4. **Per topic**: content-creator → slides → QA → update continuity →
   **Checkpoint** (step-by-step).
5. **Wrap** — summary, open items, next steps.

## Conventions

This plugin follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on changes. See the repo `README.md` and
`docs/adding-a-plugin.md`.

## Reference

- `skills/workshop-builder/SKILL.md` — the orchestrator's full instructions.
- `skills/workshop-builder/references/{structure,conventions}.md` — layout + naming.
- `skills/workshop-slide-deck/SKILL.md` — the slide engine and visual rules.
