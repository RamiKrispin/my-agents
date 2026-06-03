# Slide Style — `design-principles`

This profile uses the **course-slide-deck** skill's default theme — the clean,
presentation-scale look from the reference Docker course. The slide skill is the
engine; this file records the theme choices for this profile.

## Theme

- **Tokens:** the `:root` set in `course-slide-deck/references/style-tokens.md`
  (surfaces, ink, blue→teal accent gradient, semantic green/amber/red). Don't
  invent colors — pick from the palette.
- **Engine:** `course-slide-deck/templates/base-deck.html` (viewport-locked
  slides, opacity cross-fade, top-anchored content, slim progress bar only).
- **Typography:** Inter + ui-monospace, presentation scale (h1 ~92px).

## Conventions for this profile

- **Branding line** on the title slide (`{{COURSE_BRANDING}}`): set from the
  course title, e.g. `"{Course Title} · {tagline}"`.
- **Title-art motif:** pick an abstract SVG that matches the lesson topic
  (layers for Dockerfiles, grid for management, arrows for workflows).
- **Color semantics are locked:** green = good/running, amber = warning/build-time,
  red = bad/anti-pattern, violet/pink = secondary highlights.
- Per-lesson decks start from `base-deck.html`.

See `course-slide-deck/references/slide-patterns.md` for the layout catalog and
the skill's anti-patterns list.
