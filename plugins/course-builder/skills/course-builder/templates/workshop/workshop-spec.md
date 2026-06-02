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

A **single** deck for the whole workshop at `slides/workshop_slides.html`, with
one section per topic.

## Conventions

Topic folders `NN_topic_name`; supporting code/docs inside each topic folder.
**No scripts** in workshop mode. Continuity: `spec/continuity.md`. Open items:
`spec/open-items.md`.
