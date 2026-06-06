---
name: campaign-builder
description: Build a multi-platform promotion campaign from a course-builder run, workshop-builder run, or LinkedIn-Learning-style course folder. Produces a per-topic, per-platform draft tree with a checkpoint between proposal and fan-out. Drafts are written one at a time. Use when promoting a course, workshop, or themed body of work across LinkedIn, X, Bluesky, Threads, Instagram (carousel / Reels), TikTok, blog, and video.
---

# Campaign Builder

Build a multi-post, multi-platform promotion campaign from a body of course or
workshop materials. The campaign uses the course as a lead magnet — each post
talks about a topic the course teaches and points readers back to the full
course. **Never fabricate.** Every concrete claim must trace to a file in the
source materials (file path + line where useful). If something can't be
grounded, flag it in `campaign.md` open items rather than inventing.

> Drafting a single post for one platform? Use the sibling
> [social-content](../../../social-content/) plugin. campaign-builder is for
> coordinated multi-post sequences sourced from a course / workshop.

## Inputs

The user provides a source path, a scope, and a platform list. Ask once,
concisely, for anything missing — **never guess defaults for `platforms`**.

```
source:       <path>                     # course / workshop / LinkedIn-Learning root
scope:        chapter <N> | lessons <list> | theme <description>
platforms:    <comma-separated>          # REQUIRED. options: linkedin, reels,
                                         #   x-thread, bluesky, threads,
                                         #   instagram-carousel, video-script, blog
blog_count:   0 | 1 | 2 | 3              # default 0 (only if `blog` in platforms)
blog_length:  800 | 1500 | 2000          # words; default 1500
video_length: 30s | 60s | 90s            # default 60s
pace:         per-topic | continuous     # default per-topic
slug:         <kebab-case>               # optional; AI proposes if absent
```

If `platforms` is absent, ask the user with this exact menu:

> Which platforms should the campaign cover? Pick from:
> `linkedin`, `reels`, `x-thread`, `bluesky`, `threads`,
> `instagram-carousel`, `video-script`, `blog`. Comma-separate.

Don't proceed on guesses.

## Workflow

The skill is a sequential orchestrator. **No subagents.** Drafts are written
**one at a time**. Per-topic checkpoint by default.

### 1. Parse the request

Identify source path, scope, platforms (REQUIRED), and any add-on knobs
(blog_count, blog_length, video_length, pace, slug). If platforms missing —
ask. If slug missing, propose a short kebab-case name based on the scope (e.g.
`docker-workflow-fundamentals` for "chapter 2" of a Docker course); the user
can override at the checkpoint.

### 2. Detect the source layout

Probe the source path. Check **all three** signals before settling on one
— if more than one is present, warn the user and ask which layout to use.

- `<source>/spec/course-spec.md` → **course-builder layout**, follow
  `sources/from-course-builder.md`.
- `<source>/spec/workshop-spec.md` → **workshop-builder layout**, follow
  `sources/from-workshop-builder.md`.
- `<source>/chapter_0/learning_goals.md` (no `spec/`) →
  **LinkedIn-Learning-style course folder**, follow
  `sources/from-course-folder.md`.

If exactly one signal matches, proceed with that layout. If multiple match
(e.g. a course-builder course was reorganized into a `chapter_0/` layout
without removing `spec/`), ask the user which is authoritative and warn
that the secondary signals will be ignored. If none match, ask the user
where the course structure lives — don't guess.

### 3. Ingest source scoped to the user's scope

Read the source files identified by the layout's ingestion guide, scoped to
the chapter / lesson list / theme the user gave. Build a **master fact sheet**:
20-40 grounded claims with file-path citations covering the scope. Mark each
claim with which kind of post it best supports (LinkedIn hook, blog deep-dive,
video demo, etc.). This fact sheet is the single source of truth for the
campaign — every draft pulls from it.

### 4. Propose campaign structure

From the fact sheet, propose:

- 3-9 **topics** (one per logical sub-area of the scope; the user can add /
  drop / merge at the checkpoint).
- Per topic: a working title, source grounding (which lesson files / line
  ranges anchor it), the recommended pillar (see `profiles/default/pillars.md`),
  and a short angle per chosen platform.
- Per blog (if `blog` in platforms and `blog_count > 0`): which topic(s) it
  spans, target length, target tone (Substack-friendly Markdown).
- A suggested posting order with rationale (lead with the strongest hook;
  bookend with course CTAs).

Run `python3 scripts/init_campaign.py <campaigns-dir> <slug>` to atomically
materialize the campaign skeleton:

```
campaigns/<slug>/
  campaign.md                  # the proposal — Status: PROPOSED
  topics/                      # empty; populated at fan-out
  blog/                        # empty; populated at fan-out
  assets/                      # empty; sidecars (drawio / infographic) land here
```

Populate `campaign.md` from `templates/campaign.md` with everything the AI
proposed. **Status starts at `PROPOSED`.**

### 5. CHECKPOINT — wait for approval

Stop. Tell the user:

> I've written the campaign proposal to `campaigns/<slug>/campaign.md`.
> Review it. To proceed, change `Status: PROPOSED` → `Status: APPROVED`.
> To request changes, change to `Status: REVISE` and write inline notes
> in the "Revision notes" section. Re-invoke the skill when ready.

**Do not write any drafts until the user signals approval.**

### 6. Re-entry — verify status

On re-invocation, run:

```
python3 scripts/verify_status.py campaigns/<slug>/campaign.md
```

Exit codes:

- `0` → APPROVED → proceed to step 7.
- `1` → PROPOSED → user hasn't approved yet; print path and stop.
- `2` → REVISE → read inline notes, revise the topic list / scope / platforms
  in `campaign.md`, set `Status: PROPOSED`, ask user to re-approve. Stop.
- `3` → DRAFT or POSTED (campaign already past approval) → ask user whether
  to resume drafting any PENDING topics, or stop.
- `4` → file missing / malformed.

### 7. Fan out — one platform at a time, per topic

For each topic in `campaign.md`, in order:

a. **Build the per-topic spec.** Write `campaigns/<slug>/topics/NN-<topic-slug>/topic.md`
   from `templates/topic-spec.md`: topic title, source citations (the subset
   of the fact sheet for this topic), 5-10 grounded claims, recommended pillar,
   per-platform angle.

b. **Load voice ONCE per topic.** Read in order:
   - `profiles/default/voice-guide.md`
   - `profiles/default/best-practices.md`
   - `profiles/default/pillars.md`
   - `profiles/default/examples/<platform>/*.md` for each chosen platform.
     **Filter `README.md` out of the listing first**, then check whether any
     `.md` exemplars remain. If none remain, the folder is effectively empty
     — fall back to the format scaffold + best-practices and warn the user.

c. **For each chosen platform, in this order, draft serially:**

   **Voice rule for all platforms: same tone, same hook, same content as
   the LinkedIn version. The only adaptation across platforms is LENGTH.**
   The LinkedIn post is the canonical version — written first, deepest in
   detail, and the source-of-truth for voice. Shorter platforms compress
   or split that same content; they do NOT introduce new angles, new hooks,
   or new framings.

   Platform character limits (hard caps; the orchestrator must respect them):

   | Platform | Limit | Default adaptation |
   | --- | --- | --- |
   | LinkedIn | 3,000 | canonical (target 1,200-1,800 chars per `voice-guide.md`) |
   | TikTok / Instagram caption | 2,200 | condense if needed; usually fits |
   | Threads | 500 per post | condense to 1 post; 2-3 post thread if the LinkedIn body has parallel beats |
   | Bluesky | 300 per post | condense to 1 post; 2-3 post thread for multi-beat content |
   | X | 280 per tweet | thread by default (4-7 numbered tweets); single only when the topic is genuinely one-line |

   1. **`linkedin` — DRAFT FIRST.** This is the canonical body all other
      platforms adapt from. Format scaffold: `formats/linkedin-post.md`.
      Write to `linkedin.md`. Run `python3 scripts/validate.py <body.md>`
      → iterate until PASS.
   2. `bluesky` → adapt the LinkedIn body to ≤ 300 chars.
      Format: `formats/bluesky-post.md`. Write to `bluesky.md`.
   3. `threads` → adapt the LinkedIn body to ≤ 500 chars.
      Format: `formats/threads-post.md`. Write to `threads.md`.
   4. `x-thread` → split the LinkedIn body into a numbered thread (each
      tweet ≤ 280 chars). Format: `formats/x-thread.md`. Write to
      `x-thread.md`.
   5. `instagram-carousel` → adapt the LinkedIn body into a slide-by-slide
      carousel brief — same voice, same content, visual layout. Format:
      `formats/instagram-carousel.md`. Write to `instagram-carousel.md`.
   6. `reels` → `formats/reels-script.md` → `reels.md`. **Do NOT run
      `validate.py` on `reels.md`.** The reels format scaffold mandates a
      `# {Working title}` H1 as the first line (metadata for the editor,
      not spoken VO), which validate.py would unconditionally reject as
      "first line looks like a heading". Use the reels-script.md inline
      QA rules instead (length budget, hook in first 3 seconds, on-screen
      text inventory, no fabricated numbers).
   7. `video-script` → `formats/video-script.md` → `video-script.md` (one
      combined script per topic with per-platform notes — TikTok cut pace,
      LinkedIn outcome-first opener, IG Reel framing).

   **One platform at a time.** Don't draft N platforms in parallel. Don't
   batch in subagents. Write each file, then move to the next platform.

d. **Per-topic checkpoint.** After all chosen platforms for the topic are
   drafted, **stop**. Print:
   - The list of files written.
   - One-line summary per platform (e.g. "linkedin.md — 1,520 chars; PASS;
     hook = 'I cut the demo image from 8GB to 900MB'").
   - Any open items (claims that couldn't be grounded; example folders that
     were empty).

   Wait for the user to say "continue" before starting the next topic.

   **Override:** if `pace: continuous` was set, skip the checkpoint and run
   straight through all topics.

e. **Context refresh.** If 3 or more topics have been drafted in the same
   session, before drafting the next topic re-read its source files
   (per `topic.md` citations) to refresh grounding. This is the mitigation
   for context bloat in long fan-out runs.

### 8. Blog phase (after all topic drafts are done)

If `blog` is in platforms and `blog_count > 0`:

For each blog assignment in `campaign.md`:
- Read the **full lesson source files** for the topics the blog spans
  (deeper than the per-topic fact sheet).
- Load `formats/blog-post.md`.
- Draft to `campaigns/<slug>/blog/NN-<blog-slug>.md` at the configured length.

### 9. Update campaign.md status

After all platforms and blogs are drafted, update each topic's `Status: PENDING`
→ `Status: DRAFT` in `campaign.md`. Update top-level `Status: APPROVED` →
`Status: DRAFT`. Add an `## Open items` summary if anything was flagged.

### 10. Final summary

Print the full `campaigns/<slug>/` file tree, one line per file, with a
one-sentence description of each draft. Tell the user:
- Which platforms had empty example folders (will improve as exemplars are
  populated under `profiles/default/examples/<platform>/`).
- Which validate.py runs failed and were iterated.
- Suggested posting order from `campaign.md`.

## QA checklist (per draft, before writing the file)

- **Source-grounded** — every concrete claim (number, library, file path,
  command) traces to a fact-sheet entry. No fabrications.
- **One idea** — a reader can summarize the post in one sentence.
- **Hook on line 1** — first line earns the read (LinkedIn / X / Threads /
  blog title); first 3 seconds for video.
- **Voice** — matches `voice-guide.md` and the chosen platform's example
  folder. No banned hype phrases. Functional emoji whitelist only.
- **CTA / lead-magnet discipline** — soft course mention on 1-2 of the topic
  posts (the bookends, plus any topic where the course connection is most
  natural). Not every post.
- **Format-specific** — see each format scaffold for platform rules
  (length caps, line-break discipline, hashtag norms).

For LinkedIn and Reels: the offline structural validator
(`python3 scripts/validate.py`) is authoritative on the structural rules
(hook present, length bounds, banned phrases, paragraph discipline). Run it
on every body before writing the file.

## Files in this skill

- `formats/{linkedin-post,reels-script,x-thread,bluesky-post,threads-post,instagram-carousel,blog-post,video-script}.md` —
  per-platform format scaffolds.
- `sources/{from-course-builder,from-workshop-builder,from-course-folder}.md` —
  source-layout-specific ingestion guides.
- `profiles/default/{voice-guide,best-practices,pillars}.md` — voice corpus
  (canonical source: `social-content`; this is a maintained copy — re-sync and
  bump campaign-builder's version when social-content's profile evolves).
- `profiles/default/examples/<platform>/` — user-populated exemplars per
  platform. Empty in v1; the skill warns when a folder is empty and falls
  back to the format scaffold.
- `templates/{campaign,topic-spec}.md` — skeletons used by `init_campaign.py`
  and step 7a respectively.
- `scripts/init_campaign.py` — atomically creates the campaign directory and
  a skeleton `campaign.md`.
- `scripts/verify_status.py` — reads `campaign.md` Status field; exit codes
  per status.
- `scripts/validate.py` — local copy of social-content's validator
  (canonical source: `social-content/skills/social-content/scripts/`).

## Notes

- The example posts under `profiles/default/examples/<platform>/` are the
  ultimate source of truth for each platform's voice. When you (the user)
  populate them, the skill's drafts get sharper. v1 ships with empty folders
  — the skill warns when it falls back to scaffolds only.
- Voice files (voice-guide / best-practices / pillars) are deliberately
  duplicated from `social-content`. Discipline rule: social-content owns the
  canonical copy; when those files change, copy them over and bump
  campaign-builder's version.
- Keep it concrete and concise. Substance over adjectives. Don't write what
  anyone could write — write what only Rami can write.
