---
description: "Start or continue building a course or workshop."
argument-hint: [course | workshop | continue | a request]
---

Use the **course-builder** skill to build a course or workshop.

Request:

$ARGUMENTS

How to proceed:

- **If `spec/` does not exist yet** (fresh start): run discovery — ask whether
  this is a **course** or a **workshop**, then collect scope, audience,
  objectives, the **profile** (default `design-principles`), materials (repo,
  templates, style), and the **build mode** (step-by-step or all-at-once).
  Propose the structure, and after approval write the spec into `spec/`. Stop at
  the spec checkpoint.
- **If `spec/` exists**: read `spec/` (including `spec/continuity.md`) and
  continue from the recorded status — honoring the chosen build mode and the
  human checkpoints.

Always follow the course-builder skill end to end: spec → per-stage build
(content-creator → slides → QA) → update continuity → checkpoint.
