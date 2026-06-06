# Format: Video script (combined, with per-platform notes)

**One** combined `video-script.md` per topic that produces a beat-by-beat
script the user can shoot from. The script is platform-agnostic at its core
(hook → beats → payoff) with **per-platform notes** for the cuts that differ:
TikTok pace, LinkedIn opener, Instagram framing.

## Length (configurable per campaign)

- **Default:** 60 seconds → ~140-160 spoken words.
- **Short:** 30 seconds → ~70-80 words. Use for one-beat hooks or before-after
  reveals.
- **Long:** 90-120 seconds → ~210-280 words. Use for a 5-item list or a
  walkthrough.
- **Cap:** 120s. Anything longer becomes a different format (LinkedIn long
  video, YouTube short).

The user sets `video_length` in `campaign.md`. Match the word count to it.

## Script structure (3 acts)

```
[0:00 – 0:03]   HOOK         — earn the watch past 3 seconds
[0:03 – LAST 5]  PAYLOAD      — 1 idea, 3-5 beats max
[last 5 sec]    PAYOFF + CTA — takeaway + soft course mention
```

### HOOK (0-3s)

- **Concrete claim** spoken AND on-screen text. Most viewers watch muted.
- "I cut my Docker image from 8GB to 900MB" + on-screen `8GB → 900MB`.
- No "Hey guys" / "What's up". Cut to the claim immediately.

### PAYLOAD (3s → end-5s)

- **One idea.** Same rule as the LinkedIn / X variants. If the post teaches
  two things, split into two videos.
- **3-5 beats.** Each beat = one short spoken line + one on-screen text cue
  + a B-roll suggestion (terminal capture, before/after, hand demo).
- **Show, don't tell.** If the topic has a visible artifact (a Dockerfile,
  a `docker images` output, a code diff), show it.

### PAYOFF + CTA (last 5s)

- **One-line takeaway** spoken + on-screen.
- **Soft course CTA:** "Full chapter at <course URL>" or "Link in bio". Hard
  CTAs are reserved for 1-2 topics per campaign — see `campaign.md` CTA plan.

## Per-platform cut notes

The same script body adapts to three platforms with small tweaks. The skill
includes a notes block in the script file:

```markdown
## Per-platform notes

**TikTok:**
- Cut every 1-2 seconds for the first 5 seconds. TikTok rewards velocity.
- Vertical 9:16. Captions ON by default.
- Open with a hand or face on screen — pure title cards underperform.

**Instagram Reels:**
- Cut every 2-3 seconds. Slightly slower than TikTok.
- Vertical 9:16. Captions ON.
- The first frame becomes the thumbnail — design for that.

**LinkedIn video (native):**
- Open with the OUTCOME, not the setup. ("I cut my image from 8GB..." beats
  "I had a problem with my image size...")
- 16:9 or 9:16 both work; 9:16 reads better on mobile-dominant LinkedIn.
- Captions ON. Even more important than IG/TikTok — 80%+ of LinkedIn video
  is watched muted.
```

## Output structure (the literal file the skill writes)

```markdown
# Video script — <topic title>

**Length:** ~60s · **Hook style:** specific outcome · **Pillar:** Docker
**Companion topic:** topics/NN-<slug>/topic.md

---

## [0:00-0:03] HOOK

**VO:** "I cut my AI app's Docker image from 8GB to 900MB."
**On-screen:** "8GB → 900MB"
**Visual:** title card, then cut to terminal showing `docker images` output.

## [0:03-0:10] BEAT 1 — the problem

**VO:** "The first build pulled the entire CUDA toolkit, plus dev
dependencies."
**On-screen:** "CUDA + dev deps = bloat"
**Visual:** Dockerfile on screen, highlight `FROM nvidia/cuda` line.

## [0:10-0:25] BEAT 2 — the fix

**VO:** "Three changes did most of the work — multi-stage build, slim base
image, .dockerignore."
**On-screen:** numbered list "1. Multi-stage  2. Slim base  3. .dockerignore"
**Visual:** scroll through Dockerfile diff.

## [0:25-0:40] BEAT 3 — the result

**VO:** "Image dropped to 900MB. Cold start went from 90 seconds to 12."
**On-screen:** "8GB → 900MB · 90s → 12s"
**Visual:** side-by-side terminal panes, before vs after.

## [0:40-0:60] PAYOFF + CTA

**VO:** "Smaller images aren't just disk savings — they're faster cold starts
in production. Full chapter on Docker workflow at <course URL>."
**On-screen:** "Smaller image = faster cold start"
**Visual:** title card with takeaway + course URL on screen for the last 3s.

---

## Caption (for the post, under the video)

{1-3 sentence caption mirroring the hook + payoff. This is what shows under
the video on LinkedIn / IG / TikTok.}

## On-screen text inventory (for the editor)

- "8GB → 900MB"
- "CUDA + dev deps = bloat"
- "1. Multi-stage  2. Slim base  3. .dockerignore"
- "8GB → 900MB · 90s → 12s"
- "Smaller image = faster cold start"

## Per-platform notes

(see the per-platform notes block above)

## Hashtags / tags (3-5)

#Docker #MachineLearning #DataScience #ProductionAI
```

## Anti-patterns

- **No "Hey guys, today we're going to talk about..."** — cut straight to
  the claim.
- **No multi-paragraph VO blocks.** One short line per beat.
- **No fabricated numbers.** If the claim isn't grounded, drop it.
- **No long static shots.** Every 2-4 seconds, a cut.
- **Hook text on slide 1 must match the spoken VO.** Don't show one number
  and say a different one.
- **Don't write three separate scripts** for IG/TikTok/LinkedIn. The body
  is the same; the per-platform notes carry the differences.

## Anchor patterns observed

- **Hook patterns that work:**
  - "I cut my [thing] from [X] to [Y]."
  - "Most [category] failures aren't about [common cause]. They're about
    [real cause]."
  - "Three [things] every [audience] should know about [topic]."

- **Payoff patterns that work:**
  - "The lesson: {one line}."
  - "[Specific outcome] = [specific benefit]."

## Validation

The skill runs `scripts/validate.py` on the **VO text only** (concatenated)
to check for banned hype phrases and engagement bait. Other structural rules
(timestamp coverage, on-screen text inventory completeness) are checked
inline in SKILL.md's QA pass.
