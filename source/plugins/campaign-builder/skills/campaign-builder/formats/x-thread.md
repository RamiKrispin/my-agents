# Format: X (Twitter) thread

**This is an ADAPTATION format.** The orchestrator has already drafted
the canonical LinkedIn version of this post. Your job: **split the
LinkedIn body into a numbered X thread.** Same voice, same hook, same
content, same close. Only the LENGTH and the line-break shape change.

Don't rewrite. Don't introduce a new angle. Don't make it "punchier" or
"more Twitter-y" — Rami's voice is the same on every platform.

## Hard cap

**280 chars per tweet** — non-negotiable. X enforces this at the protocol
level.

## Adaptation strategy: condense or split

For each "beat" of the LinkedIn body (hook, supporting paragraph, list
item, takeaway), decide:

- **Fits in ≤ 280 chars after light tightening?** → make it one tweet.
- **Doesn't fit?** → split it across two tweets, OR cut a phrase that's
  scaffolding rather than substance (filler clauses, soft hedges, repeated
  context).

Most LinkedIn posts (1,200-1,800 chars) become a 5-7 tweet thread.

## Thread shape (mirrors the LinkedIn body)

- **Tweet 1 (the hook):** ≤ 280 chars. The same hook line that opens the
  LinkedIn post. Stands alone — earns the click on "Show more". No "🧵 a
  thread:" suffix; no decoration.
- **Tweets 2 through N-1 (the body):** one beat per tweet. Number them
  `2/`, `3/`, etc. Each tweet is one idea — typically one paragraph or
  one bullet from the LinkedIn version, tightened to ≤ 280 chars.
- **Tweet N (the close):** the same takeaway + optional course link
  that closes the LinkedIn post. ≤ 280 chars. Move the link here — never
  in tweet 1.

## Output structure

```markdown
# X thread — <topic title>

## 1/ Hook
{≤ 280 chars; mirror the LinkedIn hook line}

## 2/
{≤ 280 chars; one beat from the LinkedIn body}

## 3/
{≤ 280 chars}

## 4/
{≤ 280 chars}

## 5/ Takeaway
{≤ 280 chars; same close as LinkedIn; course link here on CTA topics}
```

The `## N/` headings are for human navigation; only the body text under
each heading goes into X.

## Anti-patterns

- **Don't reframe the post for "X tone".** Same Rami voice as LinkedIn.
- **Don't pad to look thready.** If 3 tweets is enough, ship 3.
- **Don't put the link in tweet 1.** Move it to the closing tweet.
- **No threadboi tropes** — "🧵👇", "Bookmark this", "Read this twice".

## Validation

`scripts/validate.py` does NOT cover X threads. QA inline: every tweet
≤ 280 chars (count each), link only in the closing tweet, no banned hype
phrases, voice matches the LinkedIn version.

```python
for tweet in thread.split("## "):
    assert len(tweet.body) <= 280
```

