# Format: Bluesky post

**This is an ADAPTATION format.** The orchestrator has already drafted
the canonical LinkedIn version of this post. Your job: **condense the
LinkedIn body into a single Bluesky post** (or a 2-3 post thread when
the content genuinely doesn't fit). Same voice, same hook, same content,
same close. Only the LENGTH changes.

Don't rewrite. Don't introduce a new angle. Same Rami voice.

## Hard cap

**300 chars per post** — protocol-enforced.

## Adaptation strategy: condense first, split second

For most topics, a 1,200-1,800 char LinkedIn post compresses to a single
300-char Bluesky post. The compression keeps:

- The hook line (the LinkedIn opener, tightened).
- The single most concrete fact / number / outcome.
- The takeaway / close (often paired with a link on CTA topics).

What gets cut: setup paragraphs, secondary supporting examples, hedges,
parallel restatements.

If the LinkedIn body has **two genuinely distinct sub-points** that can't
both be honored in 300 chars, split into a 2-3 post thread (each ≤ 300
chars). Don't fake-thread to look substantial — single-post is the default.

## Output structure

Single post (the common case):

```markdown
# Bluesky — <topic title>

{post text, ≤ 300 chars total including any link}
```

Thread (only when content demands it):

```markdown
# Bluesky thread — <topic title>

## 1/
{post text, ≤ 300 chars}

## 2/
{post text, ≤ 300 chars}

## 3/
{post text, ≤ 300 chars; course link here on CTA topics}
```

## Anti-patterns

- **Don't reframe for "Bluesky tone".** Same Rami voice as LinkedIn.
- **Don't fake-thread.** If 1 post fits, ship 1 post.
- **No engagement bait.** No "like if you agree", no "follow for more".
- **No hashtags.** Bluesky users don't lean on them; skip entirely.

## Validation

No structural validator for Bluesky in v1. QA inline: ≤ 300 chars per
post (count it), hook stands alone, no banned hype phrases, voice
matches the LinkedIn version.
