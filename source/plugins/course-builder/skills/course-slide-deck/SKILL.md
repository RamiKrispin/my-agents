---
name: course-slide-deck
description: Build HTML slide decks for course lessons and workshops. Presentation-scale typography, viewport-locked slides with cross-fade transitions, top-anchored content, and a clean unadorned canvas (only a slim progress bar). Use whenever creating a lesson's slides.html (course) or the combined workshop deck. Theme comes from the active profile's slide-style.
---

# Course slide-deck skill

A portable engine + visual language for consistent HTML slide decks. Used by the
course-builder content step. Keep the typography, layout, and nav script
identical across decks; vary the per-slide infographics to match the content.

This skill is **profile-themed**: the active profile's `slide-style.md` chooses
the tokens and the title-slide branding. Don't hardcode a course name.

## When to use

- A course lesson `slides_c{N}_l{M}.html` (one deck per lesson).
- A workshop's single combined deck `slides/workshop_slides.html` (one section per topic).
- Any slides that must match the course visual format.

Don't use it for the lesson script or README (separate artifacts), or for
non-course decks.

## Inputs

- **Course:** the lesson script `script_c{N}_l{M}.md` — each `[CLICK]` marker is
  roughly one slide boundary. Plan ~8–12 slides per lesson.
- **Workshop:** the topic READMEs + agenda — one section of the combined deck per
  topic (title divider + that topic's content slides).
- The active **profile** `slide-style.md` (theme + branding) and the references
  below.

## Authoring workflow

1. **Read the source** (script for a lesson; topic READMEs for a workshop) and
   the profile's `slide-style.md`.
2. **Plan slide types.** Every lesson deck has: 1 title + 1 "where we are" +
   several content slides + 1 takeaway. A workshop deck has 1 title + per-topic:
   a section divider + content slides, and a final takeaway.
3. **Start from `templates/base-deck.html`.** Set the title-slide
   `{{COURSE_BRANDING}}` from the course/workshop title. Add per-slide CSS only
   for visuals the boilerplate doesn't already cover.
4. **Test in a browser** — keyboard nav (`←`/`→`/`space`) and the progress bar.
5. **Check the tallest slide fits `100vh`** (slides are hard-capped, `overflow:hidden`).
   Trim or split rather than letting content scroll.

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

- H1/H2 lines short and declarative; accent the lesson's key noun in `.accent`.
- Slides are a quiet voice beside the script — let the script tell the story.
- Code in slides is for shape: 3–8 lines per block; long examples go in the README.

## Anti-patterns (hard rules)

- No new fonts (Inter + ui-monospace only). No emojis unless asked (use SVG).
- No reveal-on-click animations; no `display:none` on slides; no spatial transforms
  on top of the fade.
- No brand strip / page counter / keyboard hint — the progress bar is the only chrome.
- No slide over `100vh`. Don't hardcode chapter/lesson numbers in JS (it reads the DOM).
- Don't hardcode a course name — use `{{COURSE_BRANDING}}` from the spec/profile.

## Files in this skill

- `templates/base-deck.html` — the boilerplate deck (title, where-we-are,
  takeaway) with all styling + the nav script. Branding is `{{COURSE_BRANDING}}`.
- `references/style-tokens.md` — full color + typography reference.
- `references/slide-patterns.md` — each pattern's HTML skeleton.
