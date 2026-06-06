---
campaign: <slug>
status: PROPOSED
source: <path-to-course-or-workshop-root>
source_type: course-builder | workshop-builder | course-folder
scope: <chapter N | lessons X-Y | theme description>
platforms: <comma-separated list>
blog_count: <0..3>
blog_length: <words>
video_length: <seconds>
pace: per-topic | continuous
created: <YYYY-MM-DD>
---

# Campaign: <Title>

## Status legend

`PROPOSED` — awaiting user approval. The skill stops here.
`APPROVED` — user approved; the skill fans out.
`REVISE`   — user wants changes. Notes in the Revision notes section below.
             The skill reads notes, updates this file, sets back to PROPOSED.
`DRAFT`    — fan-out complete. All topic / blog files written.
`POSTED`   — manually flipped by the user when posting is done.

To approve: change `status: PROPOSED` to `status: APPROVED` in the frontmatter
above, then re-invoke the skill. To request revisions: change to `REVISE` and
add notes in the "Revision notes" section.

## Overview

<One paragraph: what this campaign is, who it's for, what the source course
covers, and what the campaign aims to achieve (e.g. "build awareness for the
Docker for Local AI course launch by sharing 7 lead-magnet posts on the
Docker workflow chapter, pointing readers to the full course").>

## Topics

| # | Slug | Title | Source grounding | Pillar | Status |
|---|------|-------|------------------|--------|--------|
| 01 | <kebab-slug> | <title> | <ch_X/lY/file refs> | <pillar> | PENDING |
| 02 | <kebab-slug> | <title> | <ch_X/lY/file refs> | <pillar> | PENDING |
| ...

Per-topic angle (one line per platform per topic — what the post actually says):

### 01 — <slug>

- **linkedin:** <hook angle>
- **x-thread:** <hook angle>
- **bluesky:** <hook angle>
- **threads:** <hook angle>
- **instagram-carousel:** <hook angle>
- **reels:** <hook angle>
- **video-script:** <hook angle>

### 02 — <slug>

(same pattern — only the platforms the user chose)

## Blog assignments (only if `blog` is in platforms)

| # | Slug | Spans topics | Target length | Status |
|---|------|--------------|---------------|--------|
| 01 | <kebab-slug> | 01, 02 | 1500 | PENDING |
| 02 | <kebab-slug> | 03, 05 | 1500 | PENDING |

## CTA / lead-magnet plan

- **Course landing page:** <URL>
- **Soft mentions:** which topic posts include a soft course reference at the
  close (typically the bookends — first and last topic).
- **Hard CTAs:** which topic posts (or blog posts) include an explicit
  "full chapter in the course" link. Default: 1 in 3 posts.

## Posting schedule (suggested; user-edits freely)

- 01: <day> — <platforms>
- 02: <day> — <platforms>
- ...

## Open items

(Populated by the skill at fan-out time. Examples: claims that couldn't be
grounded; topics where the user should clarify the angle; example folders
that are empty.)

## Revision notes

(Populated by the user when `status: REVISE`. The skill reads these on
re-entry, applies the changes, and sets status back to PROPOSED.)
