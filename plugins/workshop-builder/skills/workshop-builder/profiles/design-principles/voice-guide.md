# Voice & Structure Guide — `design-principles`

Distilled from a real Docker-for-AI course (see `examples/`). Use this profile
for workshops that teach **principles and workflows** — the "why before what"
teaching style. Read it (and skim an example) before drafting any topic.

> The example scripts in `examples/` come from the course version of this
> profile. Workshops have **no scripts**; read the examples for **voice and
> structure** only — apply that voice to the slide section and (when emitted)
> the topic README.

## Voice

- **First-person plural** ("we", "our") — instructor and learner move through the
  material together. Second person ("you") only for direct address or an action
  to take.
- **Conversational but precise.** Contractions are fine. Define every technical
  term on first use, immediately.
- **Short sentences**, one idea each — rarely over 25 words. Break complex ideas
  into consecutive short sentences, not stacked clauses.
- **Why before what**, at every scale: state the problem/gap, then name the
  solution, then show how it works.
- Never call hard things "easy"; "simple" is reserved for genuinely small points.

Representative phrases (each < 25 words):
- "We can think of a Dockerfile as a recipe, and the image as the cake."
- "Running is not the same as working."
- "This step is often skipped, but it is the most important one."
- "Let's make this concrete." (into a demo)
- "That's {X}: {one-line summary}." (closing a concept)

## Slide section structure (per topic)

- A section divider with the canonical topic title `{NN} — {Topic Title}`.
- Open the topic with a brief recap of the previous one ("In the previous topic,
  we…"); for the first topic, frame the workshop as a whole.
- Close with a forward bridge to the next topic; the final topic closes with
  "Thanks for following along."
- Numbered/best-practice topics use bold labels in slides: `**First: version
  your images.**`.
- Code in slides is for shape: 3–8 lines per block. Long examples go in the
  topic folder.

## Topic README (only when the spec opts in)

- H1 `# {NN} — {Topic Title}`; open with the topic goal.
- Prose with `##` sections; code blocks and Mermaid where they clarify; close
  with a short "Recap & next".

## Avoid

- Hype adjectives ("powerful", "cutting-edge", "seamless") unless precise.
- Inconsistent terminology — reuse the canonical terms from `spec/continuity.md`.
- Inventing features/commands not in the referenced materials.
- Producing scripts. Workshops have no scripts.

## Refining this profile

Add or swap `examples/` with the author's best lessons/topics; re-derive these
rules from them. The slide look for this profile is in `slide-style.md`.
