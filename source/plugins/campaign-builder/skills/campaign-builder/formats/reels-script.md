# Format: Reels / TikTok script

Short-form vertical video script. Designed for the user (or a video editor) to
shoot/edit from. The script is **literal** — the spoken VO line by line, with
on-screen text cues, B-roll suggestions, and timing.

## Length

- **Target: 30-60 seconds** for most posts. 90s max for a list with many items.
- Spoken VO at a natural pace ≈ **140-160 words per minute**, so:
  - 30s ≈ 70-80 words
  - 60s ≈ 140-160 words
  - 90s ≈ 210-240 words

Cut ruthlessly. Tight scripts perform.

## Script structure (3 acts)

```
[0:00-0:03]  HOOK         — make them stay past 3 seconds
[0:03-0:??]  PAYLOAD      — 1 idea, 3-5 beats max
[last 5s]    PAYOFF + CTA — takeaway + (optional) follow / link in bio
```

### HOOK (0-3s)

- **Concrete claim or question.** "I cut my Docker image from 8GB to 900MB."
- Pair with on-screen text that mirrors the claim (most viewers watch muted).
- No "Hey guys" / "What's up". Cut straight to the claim.

### PAYLOAD (3s → end-5s)

- **One idea.** Same rule as LinkedIn: a viewer should be able to summarize the
  video in one sentence.
- 3-5 beats. Each beat = one short spoken line + one on-screen text cue.
- Show the **before/after** when possible (text overlay, code on screen, or a
  diagram).

### PAYOFF + CTA (last 5s)

- One-line takeaway.
- Optional CTA — "Follow for more on Production AI" / "Link in bio for the full
  course". Use sparingly; respect 70/20/10.

## Output structure (the script file)

A single Markdown file. Every beat has: timestamp, VO, on-screen text, and
optional B-roll/visual note. The file is **literal** — no commentary, no
"here's what we'll do", just the script.

```markdown
# {Working title}

**Length:** ~45s · **Hook style:** specific outcome · **Pillar:** Docker

---

## [0:00-0:03] HOOK
**VO:** I cut my AI app's Docker image from 8GB to 900MB.
**On-screen:** "8GB → 900MB"
**Visual:** title card, then cut to terminal showing `docker images` output.

## [0:03-0:10] BEAT 1 — the problem
**VO:** The first build pulled the entire CUDA toolkit, plus dev dependencies.
**On-screen:** "CUDA + dev deps = bloat"
**Visual:** Dockerfile on screen, highlight `FROM nvidia/cuda` line.

## [0:10-0:25] BEAT 2 — the fix
**VO:** Three changes did most of the work — multi-stage build, slim base
image, .dockerignore.
**On-screen:** numbered list "1. Multi-stage  2. Slim base  3. .dockerignore"
**Visual:** scroll through Dockerfile diff.

## [0:25-0:40] BEAT 3 — the result
**VO:** Image dropped to 900MB. Cold start went from 90 seconds to 12.
**On-screen:** "8GB → 900MB · 90s → 12s"
**Visual:** side-by-side terminal panes, before vs after.

## [0:40-0:45] PAYOFF
**VO:** Smaller images aren't just disk savings — they're faster cold starts
in production.
**On-screen:** "Smaller image = faster cold start"
**Visual:** title card with takeaway.

---

## Caption (for the post itself)

{1-3 sentence caption mirroring the hook + payoff. This is what shows under
the video.}

## On-screen text inventory (for the editor)

- "8GB → 900MB"
- "CUDA + dev deps = bloat"
- "1. Multi-stage  2. Slim base  3. .dockerignore"
- "8GB → 900MB · 90s → 12s"
- "Smaller image = faster cold start"

## Hashtags / tags (3-5)

#Docker #MachineLearning #DataScience #ProductionAI
```

## Reels-specific rules

- **Vertical 9:16.** Don't write visual cues that assume horizontal framing.
- **Captions on by default.** Most viewers watch muted; on-screen text is not
  optional.
- **Cuts every 2-4 seconds.** No long static shots. The script's beats map to
  cuts.
- **First frame matters.** The thumbnail is the first frame — design the hook
  visual for that.
- **One idea.** Same as LinkedIn. A reel that teaches two things teaches
  neither.

## What does NOT go in a Reels script

- No "Hey guys, today we're going to talk about..."
- No multi-paragraph VO blocks. One short line per beat.
- No fabricated numbers/results. If the claim isn't grounded, drop it.
