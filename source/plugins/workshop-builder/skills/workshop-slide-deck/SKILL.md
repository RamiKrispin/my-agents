---
name: workshop-slide-deck
description: Build HTML slide decks for workshops. Presentation-scale typography, viewport-locked slides with cross-fade transitions, top-anchored content, and a clean unadorned canvas (only a slim progress bar). Single combined deck by default; per-topic split on request. Theme comes from the active profile's slide-style.
---

# Workshop slide-deck skill

A portable engine + visual language for consistent HTML slide decks for
workshops. Used by the workshop-builder content step. Keep the typography,
layout, and nav script identical across decks; vary the per-slide infographics
to match the content.

This skill is **profile-themed**: the active profile's `slide-style.md` chooses
the tokens and the title-slide branding. Don't hardcode a workshop name.

## When to use

- A workshop's **single combined deck** `slides/workshop_slides.html` (default)
  with one section per topic.
- A workshop's **per-topic deck** `slides/NN_topic_name.html` (opt-in via the
  spec) for one topic.
- Any slides that must match the workshop visual format.

Don't use it for non-workshop decks. Workshops have **no scripts** — the slides
plus topic notes are the artifacts.

## Inputs

- The topic block in `spec/agenda.md` (and any topic README, if the spec emits
  them) for what each section/deck should cover.
- The active **profile** `slide-style.md` (theme + branding) and the references
  below.

## Authoring workflow

1. **Read the source** (agenda + the topic content the orchestrator passes in)
   and the profile's `slide-style.md`.
2. **Plan slide types.** A combined deck has 1 title + per-topic: a section
   divider + content slides, and a final takeaway. A per-topic deck has 1 title
   + several content slides + 1 takeaway.
3. **Start from `templates/base-deck.html`.** Set the title-slide
   `{{COURSE_BRANDING}}` from the workshop title. Add per-slide CSS only for
   visuals the boilerplate doesn't already cover.
4. **Test in a browser** — keyboard nav (`←`/`→`/`space`) and the progress bar.
5. **Check the tallest slide fits `100vh`** (slides are hard-capped, `overflow:hidden`).
   Trim or split rather than letting content scroll.
6. **Always write into `slides/`.** Create the folder if it doesn't exist.

## Visual system

Full tokens in `references/style-tokens.md`. Key rules:

- **Unadorned canvas** — only a slim top progress bar. No brand strip, page
  counter, or keyboard hint.
- **Eyebrow** above each h2 (uppercase, `--blue-700`, letter-spacing .18em).
- **Title slide** uses an abstract SVG `title-art` motif matching the topic.
- **Takeaway slide** ends with a `takeaway-card` one-liner + a "next" foot line.
- **Max content width** `--maxw: 1280px`; **top-anchored** content; **viewport-
  locked** (`100vh`, no scroll); **opacity cross-fade** transitions (no
  `display:none`, no spatial motion).

## Slide patterns

`references/slide-patterns.md` catalogs the layouts (title, where-we-are,
fourstep, detail sidebar+vis, annotated code, terminal mock, before/after,
object grid, lifecycle, big quote, pipeline, takeaway, …). Match a pattern to
what the slide teaches; copy its skeleton and add only the CSS it needs.

## Tone & copy

- H1/H2 lines short and declarative; accent the topic's key noun in `.accent`.
- Slides are quiet beside the spoken delivery — keep them sparse.
- Code in slides is for shape: 3–8 lines per block; long examples go in the
  topic folder's supporting code.

## Anti-patterns (hard rules)

- No new fonts (Inter + ui-monospace only). No emojis unless asked (use SVG).
- No reveal-on-click animations; no `display:none` on slides; no spatial transforms
  on top of the fade.
- No brand strip / page counter / keyboard hint — the progress bar is the only chrome.
- No slide over `100vh`. Don't hardcode topic numbers in JS (it reads the DOM).
- Don't hardcode a workshop name — use `{{COURSE_BRANDING}}` from the spec/profile.
- Decks live in `slides/`. **Never** place a deck file inside an `NN_topic_name/`
  folder.

## Files in this skill

- `templates/base-deck.html` — the boilerplate deck (title, where-we-are,
  takeaway) with all styling + the nav script. Branding is `{{COURSE_BRANDING}}`.
- `references/style-tokens.md` — full color + typography reference.
- `references/slide-patterns.md` — each pattern's HTML skeleton.
