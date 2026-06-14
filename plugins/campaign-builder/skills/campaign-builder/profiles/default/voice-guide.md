# Voice Guide — Social

The voice for LinkedIn posts and short-form video scripts. Re-read this every
run, plus the chosen template's example folder. The example posts under
`examples/<template>/` are the source of truth for shape and rhythm; this guide
is the source of truth for tone.

## Audience

Data scientists, ML engineers, AI practitioners, engineering leaders. Mostly
read on mobile. They are technical — concrete examples beat abstract claims.

## Voice

- **Concrete over abstract.** "Cut Docker image from 8GB to 900MB" beats "Docker
  is important." Specific numbers, file names, library names — when they're
  real.
- **Substance, not hype.** Let the result carry the post. No "powerful",
  "cutting-edge", "revolutionary", "game-changing", "seamless".
- **Teaching, not telling.** Show the before/after, the failed attempt, the fix
  — don't assert that something matters. Code blocks and short tables are
  welcome.
- **Personal where it earns the post.** First person when the lesson came from
  real work ("I rebuilt this environment 30 times while recording the course").
  Third person for product descriptions.
- **One idea per post.** A reader should be able to summarize it in one
  sentence. If two ideas are competing, split into two posts.
- **Mobile-friendly white space.** Short paragraphs. Blank lines between ideas.
  Lists when items are parallel.
- **Functional emojis only.** Rami uses a small set of emojis with specific
  jobs — never as decoration. The list:
  - `🚀` — "new resource" signal in the hook line of a `learning-resource`
    post (and only there).
  - `👇🏼` — "look below" — used in a hook to flag a CTA / link that follows
    further down, or in the newsletter CTA.
  - `✅` — bullet marker for topic / capability lists inside a
    `learning-resource` post. One per line.
  - `📽️` — video / playlist / course link marker (often `📽️: <link>`).
  - `♻️` — share-CTA marker (`♻️ Please share if you find it useful`).
  - `🔔` — notification CTA. Use sparingly (once every several posts).
  - `📌` — promo / pinned marker, mostly for the newsletter CTA.
  No other emojis. No `🎉`, `🔥`, `💡`, `🎯`, `🤖`, `✨`, no flag emojis, no
  reaction-style emojis. If unsure: leave it out.

## Recurring framings (use naturally; don't over-use a single one)

- "I spent {time} debugging {thing}. The root cause was {one line}."
- "Most {category} failures aren't about {assumed cause}. They're about
  {real cause}."
- "Without {practice}: {bad outcome}. With {practice}: {good outcome}."
- "I reduced {metric} from {X} to {Y}." (then explain how)
- "{N} {things} I see in {category}:" (then a numbered list)
- "The lesson: {one sentence}."

## Hooks (line 1)

The hook decides whether someone reads line 2. Aim for one of:

- **Specific outcome** — "I reduced startup time from 4 minutes to 20 seconds."
- **Curiosity** — "I spent 3 hours debugging an AI agent. The root cause was a
  single line in the prompt."
- **Contrarian** — "Most AI agent failures have nothing to do with prompts."
- **Lesson learned** — "One mistake almost doubled the cost of our RAG
  pipeline."

The hook works on its own — LinkedIn truncates around line 3 in the feed.

## Endings

Pick one — pick deliberately:

- **Takeaway** — "The lesson: treat AI agents as software systems, not prompt
  engineering projects."
- **Question** — a real, specific question the audience can answer concretely.
  ("What's the biggest challenge you've faced moving an AI app to production?")
- **Discussion prompt** — "I'm curious how others handle LLM observability
  today."

## Avoid

- Hype adjectives — "powerful", "cutting-edge", "revolutionary", "game-changing",
  "seamless", "next-gen" (the colloquial abbreviation; the full word
  "next-generation" is fine in research / academic contexts), "AI-powered"
  (when redundant).
- Marketing / back-cover language.
- Inventing features, numbers, or facts not found in the source.
- "Agree?" / "Thoughts?" / "What do you think?" — overused, rarely generate
  meaningful discussion.
- Two competing ideas in one post.
- Long opening paragraphs that bury the hook.
- Reusing the exact opening of a previous post.
- Keyword stuffing (LinkedIn SEO matters, but stuff naturally — see
  `best-practices.md`).

## Refreshing the voice corpus

The example posts in `examples/<template>/` are the source. Drop new posts into
the matching subfolder (or create a new template subfolder for a new shape) and
re-run the skill — the voice and template patterns update automatically.
