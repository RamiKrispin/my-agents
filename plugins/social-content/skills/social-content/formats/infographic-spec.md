# Format: Infographic spec (designer-facing brief)

A Markdown brief that a designer (or you in Canva / Figma / Keynote) can build a
single infographic from. Produced **only when the user requests one**
(`infographic: yes`). The skill writes it to
`posts/assets/<slug>.infographic.md` and the post entry references it with a
relative link.

The spec doesn't generate the image — it tells the designer exactly what to
build. Be concrete: text strings, panel layout, color palette, must-haves.

## Output structure

```markdown
# Infographic: {title}

**Companion post:** {filename of the LinkedIn / Reels draft}
**Format:** square (1080×1080) | portrait (1080×1350) | landscape (1200×627)
**Pillar:** {Production AI | Docker | Learning Radar | Forecasting}

## Title block

- **Headline (large):** {one short, scannable headline — usually the post hook}
- **Subhead (small):** {one supporting line, optional}

## Panels

A numbered list of panels. Each panel = one piece of the infographic. List
panels in reading order (top→bottom, left→right).

### Panel 1 — {short label, e.g. "The problem"}

- **Layout position:** top-left | top-band | center | etc.
- **Copy (verbatim):**
  > {the exact text that goes in the panel — keep it short, ~12 words max}
- **Visual cue:** {icon / mini-diagram / chart / before-after / quote, etc.}
- **Notes:** {anything the designer needs to know}

### Panel 2 — {label}

(same structure)

(...repeat for every panel — typical: 3-6 panels)

## Color palette

- **Primary:** {hex} — used for {what}
- **Accent:**  {hex} — used for {what}
- **Background:** {hex}
- **Text:**       {hex}

If there's no brand palette to follow, default to a neutral two-color scheme
(dark text on light background + one accent for key numbers).

## Typography

- **Headline:** {sans-serif, bold, ~60-80pt}
- **Body:**     {sans-serif, regular, ~24-32pt}
- Avoid more than two type weights.

## Must-haves

- {non-negotiables — e.g. "every panel shows a number", "credit
  '@RamiKrispin'", "include the repo URL"}

## Must-NOT-haves

- {anti-patterns — e.g. no emojis, no clipart icons, no stock photos, no more
  than 6 panels}

## Footer

- **Attribution:** "@RamiKrispin" (or whatever the user uses)
- **Optional:** repo URL / course URL
```

## Rules of thumb (for the spec author = the skill)

- **Mirror the post's structure.** If the post is a 5-item list, the
  infographic is 5 panels. If it's a comparison, it's two parallel columns.
- **Concrete copy.** Don't write "describe X here" — write the literal text the
  panel will show.
- **Numbers > adjectives.** Panels with a number ("8GB → 900MB") perform; panels
  with vague text don't.
- **Six panels max** (excluding title + footer). Beyond that the image gets
  noisy on mobile.
- **Saveable on its own.** The infographic should make sense without the
  caption — it's what people screenshot and save.
