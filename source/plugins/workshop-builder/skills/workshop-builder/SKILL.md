---
name: workshop-builder
description: Build a workshop from idea to finished materials, stage by stage. Use when creating workshop content — running discovery, writing a spec as the source of truth, then generating per-topic code/assets and slides, plus an independent QA pass. Single combined slide deck by default (per-topic split on request), slides under `slides/`, topic READMEs only when asked.
---

# Workshop Builder

Produce a workshop the way a small production team would: a **spec is the source
of truth** (not the chat), work proceeds **one topic at a time**, and every
topic is built by a content creator and checked by an **independent** QA
reviewer. Continuity across topics is tracked in `spec/continuity.md` so later
topics correctly reference earlier ones — even when they all share one combined
deck.

**Never fabricate.** Technical content must trace to the referenced
repo/materials; if something can't be verified, ask or flag it.

## What this skill produces

| | **Workshop** |
|---|---|
| Unit | agenda topics |
| Scripts | **no** |
| Slides | **one combined deck** (default) — split per topic on request |
| Slides location | always under `slides/` (created if absent) |
| Folders | `NN_topic_name/` (e.g. `01_intro`) |
| Topic README | **only when the user asks** (off by default) |
| Assets | in the topic folder |

See `references/structure.md` for the exact output layout and
`references/conventions.md` for naming/title rules.

## The `spec/` folder (source of truth)

All development docs live in `spec/` in the target repo (create it if absent):

- `workshop-spec.md` — overview, requirements, profile, structure, build mode,
  the implementation plan + status, and the **README preference** and
  **slide-split preference**.
- `agenda.md` — the ordered topic list.
- `continuity.md` — the continuity ledger + promise tracker (see below).
- `open-items.md` — blockers, deferrals, follow-ups.

Templates for all of these are in `templates/`.

## Profiles (voice + slide style, coupled)

A **profile** sets the workshop identity: writing voice + slide theme + examples.
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
- **Build mode:** *step-by-step* (one topic at a time, checkpoint between each —
  default) or *all-at-once* (build every topic in sequence, one final review;
  QA + continuity still run per topic).
- **Slide split:** **single combined deck** (default) or **one deck per topic**.
- **Topic READMEs:** off by default; ask whether to emit a `README.md` in each
  `NN_topic_name/` folder.

Ask anything missing as concise clarifying questions. Don't proceed on guesses.

### 2. Architect the agenda
Propose the agenda topics. **Challenge weak structures** — flag a concept used
before it's introduced, mis-ordered dependencies, or a topic that's out of
scope, and recommend a fix. The user can approve, revise, or redirect.

### 3. Write the spec  →  **CHECKPOINT 1**
Fill the templates into `spec/`. Record the **slide-split preference** and
**README preference** in `workshop-spec.md`. Initialize `continuity.md` (empty
ledger; record the planned per-topic forward promises from the agenda) and set
the status table (all topics `pending`). **Stop for the user to approve the
spec.**

### 4. Build, per topic  (respect the build mode)
For each topic, in agenda order:

  a. **Content** — dispatch the **workshop-content-creator** subagent for this
     topic (it reads the spec, agenda, continuity, profile, and the prior topic,
     then produces supporting code/assets, the topic's slides via the
     **workshop-slide-deck** skill, and a `README.md` only if the spec opts in).
  b. **QA** — dispatch the **workshop-qa** subagent (independent review incl.
     continuity, README compliance, and "no scripts"). If FAIL, hand findings
     back to a content pass and re-QA.
  c. **Update `spec/`** — append to `continuity.md` (what this topic established
     + its forward promise), update `open-items.md`, set the topic `complete`
     in the status table.
  d. **CHECKPOINT 2** (step-by-step only): user reviews the topic before the next.

In *all-at-once* mode, run a–c for every topic without stopping, then present
the whole build for one final review.

### 5. Wrap
Summarize what was built, open items, and suggested next steps.

## Continuity (`spec/continuity.md`)

The mechanism that makes staged building safe and resumable — and keeps a single
combined deck reading as one story:

- **Ledger** — per completed topic: concepts/terms introduced, the running
  example's state.
- **Promise tracker** — each topic's forward promise ("next topic we move from
  X to Y"); the next topic must fulfill it.
- Every build step reads this file first. Transition rules (recap opener +
  forward-bridge close) live in the profile voice guide; QA verifies them.

## Checkpoints (human-in-the-loop)

1. **Spec approved** before any building.
2. **Topic reviewed** before the next (step-by-step).

Honor these unless the user chose all-at-once (then only the final review).

## Files in this skill

- `templates/` — all spec + content templates.
- `profiles/<name>/` — voice guide, examples, slide style (the workshop identity).
- `references/structure.md`, `references/conventions.md` — layouts and naming.
- The companion **workshop-slide-deck** skill renders the slides.
