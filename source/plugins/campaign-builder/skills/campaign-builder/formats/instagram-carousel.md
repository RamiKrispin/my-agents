# Format: Instagram carousel

**This is an ADAPTATION format.** The orchestrator has already drafted
the canonical LinkedIn version of this post. Your job: **adapt the
LinkedIn body into a slide-by-slide carousel brief.** Same voice, same
hook, same content, same close — the carousel is a visual layout of the
SAME LinkedIn post, not a reframing of it. Only the structure (slides
with short copy + visual cues) and the medium (Instagram + LinkedIn
document post) change.

Carousels are the most save-friendly format on Instagram. The skill
produces a **designer-facing brief** — what each slide says, what visual
it carries, what copy goes in the caption — not a finished image. You
(or a designer / Canva workflow) build the visuals from the brief.

## Length

- **6-10 slides.** Below 6 the post lacks substance; above 10 mobile readers
  drop off.
- **Per-slide copy ≤ 20 words.** Big readable text on mobile. If a slide
  needs more words, split it.
- **Caption (Instagram caption underneath the carousel): 200-400 chars.**
  Short, with one CTA at the end.

## Slide structure (the canonical 8-slide template)

```
Slide 1 — Hook        : the bold claim or specific outcome (largest text)
Slide 2 — Context     : 1-2 lines setting up why this matters
Slides 3-7 — Beats    : one idea each, with a number / library / before-after
                        on the slide. Most save-friendly slides.
Slide 8 — Takeaway+CTA: one-line lesson + "save this if useful" + course CTA
```

For a "5 X for Y" topic, the canonical is 7 slides (1 hook + 5 beats + 1
takeaway). For a "lesson learned" topic, 8 slides (1 hook + 1 context + 5
beats + 1 takeaway + course slide). Adapt to the topic; don't pad.

## Output structure (the file the skill writes)

```markdown
# Instagram carousel — <topic title>

**Companion topic:** topics/NN-<slug>/topic.md
**Format:** square (1080×1080) — portrait (1080×1350) is also supported by IG
**Pillar:** <Production AI | Docker | Learning Radar | Forecasting>
**Caption length:** <chars>

## Caption (the IG post text, under the carousel)

{caption, 200-400 chars; opens with the hook; ends with a soft course CTA
+ relevant hashtags}

## Slides

### Slide 1 — Hook

- **Copy (verbatim, large):** "{≤ 12 words; the claim or outcome}"
- **Visual:** {title-card style; bold text on background; optional accent}
- **Notes:** {anything the designer needs}

### Slide 2 — Context

- **Copy:** "{≤ 18 words; why this matters now}"
- **Visual:** {photo / icon / abstract; describe specifically}
- **Notes:** {if any}

### Slide 3 — Beat 1: <name>

- **Copy:** "{≤ 18 words; one idea}"
- **Visual:** {what the slide shows — code snippet, before/after, diagram cue}
- **Notes:**

### Slide 4 — Beat 2: <name>

- (same shape)

### ... (slides 5-7)

### Slide 8 — Takeaway + CTA

- **Copy:** "The lesson: {one line}.\n\nFull chapter in the course → @RamiKrispin"
- **Visual:** {summary card; possibly with a small course-cover thumbnail}
- **Notes:** Course URL goes in the caption + bio link, NOT on the slide.

## Color palette

- **Primary:** {hex} — for headlines
- **Accent:**  {hex} — for numbers / emphasis
- **Background:** {hex}
- **Text:** {hex}

## Typography

- **Headline:** sans-serif bold, ~80-100pt for slide 1, ~50-60pt for others
- **Body:**     sans-serif regular, ~30-40pt
- Max two type weights total

## Must-haves

- Every "beat" slide shows ONE specific fact / number / name. Not a paragraph.
- Slide 1 is readable as a thumbnail (the IG feed shows only slide 1 until
  swiped).
- Hashtags go in the **caption**, not on slides.

## Must-NOT-haves

- No emojis on slides (functional or otherwise — slides are typographic).
- No more than 10 slides total.
- No long paragraphs. If a slide needs explanation, that explanation goes in
  the caption.
- No hashtags on slides.
- No "Follow me for more" on slides — use the bio + caption.

## Caption pattern

```
{Hook line — same as slide 1, or a tighter version of it.}

{1-2 sentence context: what the carousel covers and why.}

Save this if it's useful — full chapter in the course: link in bio.

#docker #ai #ml #datascience #devops
```

3-5 hashtags, end of caption, on their own line.
```

## Anti-patterns

- **Don't write a 6-slide carousel of mostly text.** Save-friendly carousels
  pair every slide with a specific visual hook (a number, a code snippet, a
  before-after, an icon).
- **Don't repeat the LinkedIn post inside the slides.** Carousels are
  scannable visuals. Compress hard.
- **Don't bury the hook past slide 1.** The thumbnail = slide 1. If slide 1
  isn't the bold claim, the post doesn't get the swipe.
- **Don't put the course URL on a slide** — Instagram slides aren't tappable.
  URL goes in the caption + bio link.

## Validation

No automated validator. QA checklist: 6-10 slides; each slide copy ≤ 20
words; slide 1 readable as thumbnail; caption 200-400 chars; 3-5 hashtags.
