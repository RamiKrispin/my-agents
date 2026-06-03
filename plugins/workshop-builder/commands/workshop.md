---
description: "Start or continue building a workshop."
argument-hint: [continue | a request]
---

Use the **workshop-builder** skill to build a workshop.

Request:

$ARGUMENTS

How to proceed:

- **If `spec/` does not exist yet** (fresh start): run discovery — collect
  scope, audience, objectives, the **profile** (default `design-principles`),
  materials (repo, templates, style), the **build mode** (step-by-step or
  all-at-once), the **slide-split preference** (single combined deck by default;
  ask if they want per-topic decks), and the **README preference** (no per-topic
  READMEs by default; ask whether to emit them). Propose the agenda and, after
  approval, write the spec into `spec/`. Stop at the spec checkpoint.
- **If `spec/` exists**: read `spec/` (including `spec/continuity.md`) and
  continue from the recorded status — honoring the chosen build mode and the
  human checkpoints.

Always follow the workshop-builder skill end to end: spec → per-topic build
(content-creator → slides → QA) → update continuity → checkpoint.
