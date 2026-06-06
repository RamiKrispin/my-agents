# campaign-builder

Build a multi-platform promotion campaign from a course-builder run, a
workshop-builder run, or a LinkedIn-Learning-style course folder. Produces a
per-topic, per-platform draft tree with a checkpoint between proposal and
fan-out. **Drafts are written one at a time.**

The campaign uses the course as a lead magnet — each post talks about a
topic the course teaches and points readers back to the full course.

> Drafting a single post for one platform? Use the sibling
> [social-content](../social-content/README.md) plugin. campaign-builder is
> for coordinated multi-post sequences sourced from a course / workshop.

Install: `/plugin install campaign-builder@my-agents` · Run: `/campaign`

## What's in this plugin

| Component | Type | Role |
| --- | --- | --- |
| `campaign-builder` | skill | The orchestrator: detect layout → ingest source → propose → checkpoint → fan out one platform at a time → blog → wrap. |
| `/campaign` | command | Entry point — pass source path, scope, **platforms (required)**, optional knobs. |

## What this plugin produces

A topic-first directory tree under `campaigns/<ai-suggested-slug>/` in your
working directory:

```
campaigns/
  docker-workflow-fundamentals/        # AI-suggested slug
    campaign.md                        # ← proposal + checkpoint lives here
    topics/
      01-dockerfile-essentials/
        topic.md                       # source citations + fact sheet + per-platform angle
        linkedin.md                    # one platform per file (only the platforms you chose)
        x-thread.md
        bluesky.md
        threads.md
        instagram-carousel.md          # slide-by-slide brief
        reels.md
        video-script.md                # combined script with per-platform notes
      02-docker-build/
        ... (same shape, only chosen platforms)
    blog/
      01-from-zero-to-shipping-docker.md
      02-the-docker-workflow.md
    assets/                            # sidecar drawio / infographic files
```

The `campaign.md` proposal is the **checkpoint artifact** — its `Status`
field gates the fan-out. The skill writes everything as `Status: PROPOSED`,
then stops; you change to `APPROVED` (or `REVISE` with notes) to proceed.

## Locked behaviors

- **Platforms must be specified.** No silent defaults. If `platforms` is
  missing from the invocation, the skill asks once with the menu:
  `linkedin, reels, x-thread, bluesky, threads, instagram-carousel,
  video-script, blog`.
- **One platform at a time.** The orchestrator drafts each platform variant
  serially — no subagents, no parallel batches. After all of topic N's
  platforms are drafted, it stops and waits for "continue" before starting
  topic N+1 (override with `pace: continuous` to run straight through).
- **Never fabricate.** Every concrete claim traces to a file in the source
  course (path + line where useful). Anything that can't be grounded goes
  into `campaign.md`'s open items, not into a draft.

## Source layouts (auto-detected)

| Detection | Layout | Guide |
| --- | --- | --- |
| `<source>/spec/course-spec.md` exists | course-builder canonical | `sources/from-course-builder.md` |
| `<source>/spec/workshop-spec.md` exists | workshop-builder | `sources/from-workshop-builder.md` |
| `<source>/chapter_0/learning_goals.md` (no `spec/`) | LinkedIn-Learning-style | `sources/from-course-folder.md` |

## Platforms (one format scaffold per platform)

| Platform | Format scaffold | Length | Validator |
| --- | --- | --- | --- |
| `linkedin` | `formats/linkedin-post.md` | 1,200-1,800 chars | `validate.py` (PASS gate) |
| `reels` | `formats/reels-script.md` | 30-90s vertical script | `validate.py` |
| `x-thread` | `formats/x-thread.md` | 1 hook + 4-7 numbered tweets, ≤ 280 chars each | inline checklist |
| `bluesky` | `formats/bluesky-post.md` | 1 post (≤ 300 chars) or short thread | inline |
| `threads` | `formats/threads-post.md` | 1 post (≤ 500 chars) or 2-3 post thread | inline |
| `instagram-carousel` | `formats/instagram-carousel.md` | 6-10 slides, ≤ 20 words/slide | inline |
| `video-script` | `formats/video-script.md` | Configurable (30s / 60s / 90s) with per-platform notes (TikTok / IG Reel / LinkedIn) | inline |
| `blog` | `formats/blog-post.md` | 800-2,500 words; configurable `blog_length` | inline |

## Voice (canonical source: `social-content`)

`profiles/default/voice-guide.md`, `best-practices.md`, and `pillars.md` are
**deliberately copied** from the `social-content` plugin. social-content owns
the canonical copies; campaign-builder is downstream. When social-content's
voice files change, copy them over and bump campaign-builder's version. This
matches how `course-builder` and `workshop-builder` maintain their own
profile copies.

`profiles/default/examples/<platform>/` is **user-populated**. Drop real
posts into the matching folder; the next campaign run picks them up. v1
ships with empty folders + per-platform READMEs explaining the convention.

## Workflow (10 steps)

1. **Parse** the request. Confirm platforms, scope, slug; ask for missing
   inputs.
2. **Detect** the source layout (course-builder / workshop-builder /
   LinkedIn-Learning).
3. **Ingest** scoped source files; build the master fact sheet (20-40
   grounded claims).
4. **Propose** the topic list and write `campaigns/<slug>/campaign.md`
   with `Status: PROPOSED`. Run `init_campaign.py` to materialize the
   directory skeleton atomically.
5. **CHECKPOINT.** Stop. Tell the user to set `Status: APPROVED` (or
   `REVISE`) and re-invoke.
6. **Verify status** on re-entry via `verify_status.py`. Branch by status.
7. **Fan out per topic, one platform at a time.** Per-topic checkpoint by
   default — pause after each topic, summarize, wait for continue. After
   3+ topics, refresh source files before drafting to avoid context bloat.
8. **Blog phase** (after all topic drafts are done) — draft 0-3 blog posts
   spanning the campaign per `campaign.md`'s blog assignments.
9. **Update `campaign.md` Status** from `APPROVED` → `DRAFT`. Flag open
   items.
10. **Final summary** — print the file tree with one-line descriptions.

## Helper scripts (zero dependencies, stdlib only)

All under `skills/campaign-builder/scripts/`.

- `init_campaign.py <campaigns-root> <slug>` — atomically materializes
  `campaigns/<slug>/` with a skeleton `campaign.md` (Status: PROPOSED) and
  empty `topics/`, `blog/`, `assets/` dirs. Slug guard rejects path-traversal
  inputs; refuses to overwrite an existing campaign dir (exit 1 if the dir
  exists).
- `verify_status.py <campaign.md>` — reads the `Status` field; exit codes
  per status: 0 APPROVED, 1 PROPOSED, 2 REVISE, 3 DRAFT/POSTED, 4 unparsable.
- `validate.py <body.md>` — copy of social-content's structural validator
  (LinkedIn / Reels shape; auto-detects aggregated files; banned-phrase
  word-boundary match). Run on LinkedIn and Reels bodies; not used for
  other platforms in v1.

## Conventions

This plugin follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on every change. See the repo
`README.md` and `docs/adding-a-plugin.md`.

## Reference

- `skills/campaign-builder/SKILL.md` — full orchestrator instructions.
- `skills/campaign-builder/templates/{campaign,topic-spec}.md` — skeletons.
- `skills/campaign-builder/sources/from-{course-builder,workshop-builder,course-folder}.md` —
  per-layout ingestion guides.
- `skills/campaign-builder/formats/<platform>.md` — per-platform format
  scaffolds.
