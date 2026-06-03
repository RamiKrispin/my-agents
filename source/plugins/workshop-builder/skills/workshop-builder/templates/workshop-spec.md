# {{Workshop Title}} — Workshop Spec

> The single source of truth for this workshop. Keep it current; every build step
> reads it first.

## Overview

- **Title:** {{title}}
- **Audience:** {{who it's for}}
- **Prerequisites:** {{what they should already know / set up beforehand}}
- **Goal:** {{one paragraph — what attendees will have built/learned by the end}}
- **Duration / format:** {{half-day | full-day | 90 min}}, {{in-person | virtual}}
- **Profile:** {{design-principles}}
- **Build mode:** {{step-by-step | all-at-once}}
- **Slide split:** {{combined | per-topic}}   <!-- default: combined -->
- **Topic READMEs:** {{off | on}}              <!-- default: off -->

## Requirements

**Use / include**
- {{…}}

**Avoid / out of scope**
- {{…}}

## Materials & assets

- **Source repo:** {{path or url}}
- **Existing code / demos:** {{…}}
- **Templates / style:** profile `{{design-principles}}` (override in `spec/style/` if present)

## Agenda

Ordered topics (full detail in `agenda.md`):

| # | Topic | Folder |
| -- | ----- | ------ |
| 01 | {{…}} | `01_{{name}}` |
| 02 | {{…}} | `02_{{name}}` |

## Implementation plan & status

Build **one topic at a time** unless the build mode is all-at-once.

| Topic | Folder | Status |
| ----- | ------ | ------ |
| 01 | `01_{{name}}` | pending |
| 02 | `02_{{name}}` | pending |

- **Current target:** {{topic NN}}

## Slides

Pick one **slide split** in the Overview block above:

- **combined** (default): a single deck at `slides/workshop_slides.html` with
  one section per topic.
- **per-topic**: one deck per topic at `slides/NN_topic_name.html`.

The `slides/` folder is created if it doesn't exist.

## Topic READMEs

Off by default — topic folders only carry supporting code/assets. Set
**Topic READMEs: on** above to emit a `README.md` in each `NN_topic_name/`
following `templates/topic-README.md`.

## Conventions

Topic folders `NN_topic_name`; supporting code/docs inside each topic folder.
**No scripts** in workshop mode. Continuity: `spec/continuity.md`. Open items:
`spec/open-items.md`.
