# Slide Style — `design-principles`

This profile uses the **workshop-slide-deck** skill's default theme — the clean,
presentation-scale look from the reference Docker course. The slide skill is the
engine; this file records the theme choices for this profile.

## Theme

- **Tokens:** the `:root` set in `workshop-slide-deck/references/style-tokens.md`
  (surfaces, ink, blue→teal accent gradient, semantic green/amber/red). Don't
  invent colors — pick from the palette.
- **Engine:** `workshop-slide-deck/templates/base-deck.html` (viewport-locked
  slides, opacity cross-fade, top-anchored content, slim progress bar only).
- **Typography:** Inter + ui-monospace, presentation scale (h1 ~92px).

## Conventions for this profile

- **Branding line** on the title slide (`{{COURSE_BRANDING}}`): set from the
  workshop title, e.g. `"{Workshop Title} · {tagline}"`.
- **Title-art motif:** pick an abstract SVG that matches the topic (layers for
  Dockerfiles, grid for management, arrows for workflows).
- **Color semantics are locked:** green = good/running, amber = warning/build-time,
  red = bad/anti-pattern, violet/pink = secondary highlights.
- **Single combined deck (default):** one file with a title + a section per
  topic, written into `slides/workshop_slides.html`.
- **Per-topic decks (opt-in):** each starts from `base-deck.html`, written into
  `slides/NN_topic_name.html`.

See `workshop-slide-deck/references/slide-patterns.md` for the layout catalog and
the skill's anti-patterns list.
