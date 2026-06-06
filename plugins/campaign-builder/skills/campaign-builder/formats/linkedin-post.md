# Format: LinkedIn long-form post

**This is the CANONICAL format for a campaign topic.** When the orchestrator
fans out a topic across multiple platforms, **LinkedIn is drafted FIRST**;
every shorter platform (Bluesky, Threads, X-thread, Instagram carousel)
adapts this same body by LENGTH only — same voice, same hook, same content,
same close. Get this version right; the others derive from it.

Generic platform-shape rules for a LinkedIn post. The chosen template's example
folder (`profiles/default/examples/<template>/`) is the source of truth for
hook + structure + length; this file is the source of truth for
LinkedIn-specific shape (line breaks, character limits, link handling).

## Length

- Sweet spot: **1,200-1,800 characters** (≈ 200-300 words). Long enough for a
  framework or lesson; short enough to stay scrollable.
- Hard cap: 3,000 characters (LinkedIn's "see more" boundary affects engagement
  past it).
- Some templates (e.g. `list` with 8-10 items) can run longer — match the
  example folder.

## Line break discipline (this is what makes LinkedIn posts readable)

- **Line 1**: the hook. Single sentence. No preamble.
- **Empty line** between every paragraph or list block.
- **Paragraphs**: 1-3 short sentences. Never a wall of text.
- **Lists**: blank line before and after; one item per line.
- **Code-like content**: indented or bulleted, with a blank line around the
  block.

## Hook (first 3 lines)

The first 3 lines are visible in the feed before "see more". They have to:

1. Earn the click on "see more".
2. Contain the post's core keyword(s) for SEO.

Patterns (see `profiles/default/voice-guide.md` for examples):

- **Specific outcome** — "I reduced startup time from 4 minutes to 20 seconds."
- **Curiosity** — "I spent 3 hours debugging an AI agent. The root cause was a
  single line in the prompt."
- **Contrarian** — "Most AI agent failures have nothing to do with prompts."
- **Lesson learned** — "One mistake almost doubled the cost of our RAG
  pipeline."

## Body shape (template-driven)

Pick from the example folder. Common shapes the skill knows about:

- **list** — Hook → 1-line intro → numbered list (5-10 items, each one
  bolded concept + one-line explanation) → 1-line takeaway.
- **lesson** — Hook (problem) → 2-3 paragraph story → bulleted list of what
  changed → 1-line lesson.
- **contrarian** — Hook (claim) → 2-3 paragraphs of evidence → 1-line takeaway.
- **comparison** — Hook → mini-table or two parallel bulleted lists → 1-line
  recommendation.

## Ending

Pick **one** and pick deliberately:

- **Takeaway** — "The lesson: treat AI agents as software systems, not prompt
  engineering projects."
- **Question** — a real, specific question. Not "Agree?" / "Thoughts?".
- **Discussion prompt** — "I'm curious how others are handling LLM
  observability today."

## Links

- LinkedIn deprioritizes posts with external links in the body. If a link is
  essential (e.g. a course or repo), add it **after** the post body with a
  short prefix:
  - "Repo: <url>"
  - "Course: <url>"
- Or push the link to the **first comment** — note this for the user in the
  output (don't add a fake comment yourself; just say "post the link as a first
  comment").

## Hashtags

- Optional. **3-5 max**, end of post, on their own block.
- Use phrases people actually search for (see best-practices §11):
  `#AI`, `#MachineLearning`, `#Docker`, `#DataScience`, `#LLM`, etc.
- Don't keyword-stuff. Don't put hashtags inline.

## What does NOT go in a LinkedIn post draft

- **Decorative emojis.** Rami uses a small set of functional emojis only —
  `🚀 ✅ 📽️ ♻️ 🔔 📌 👇🏼` — each with a specific job (see
  `profiles/default/voice-guide.md`). Anything outside that set
  (`🎉 🔥 💡 🎯 🤖 ✨`, flag emojis, reaction-style emojis) is out.
- No engagement bait ("Like if you agree", "Share with your network" — the
  `♻️ Please share if you find it useful` line in the `learning-resource`
  template is the one acceptable exception).
- No long preamble before the hook.

## Output structure (the body that gets validated and saved)

The body that goes through `scripts/validate.py` and lands at
`campaigns/<slug>/topics/NN-<topic-slug>/linkedin.md` contains **only the
post text** — exactly what would be pasted into LinkedIn. No frontmatter,
no metadata, no commentary.

```
{hook line — line 1}

{body, in the shape called for by the topic-spec angle}

{ending — takeaway / question / discussion prompt}

{optional: "Repo: <url>" or "Course: <url>"}

{optional: 3-5 hashtags on a single line}
```

The QA / source-grounding metadata (citations, pre-post checks) does NOT
live in this body. It lives in the per-topic spec at
`campaigns/<slug>/topics/NN-<topic-slug>/topic.md`, which the orchestrator
writes once per topic and references when fanning out.
