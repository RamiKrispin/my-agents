# Voice & Structure Guide — `design-principles`

Distilled from a real Docker-for-AI course (see `examples/`). Use this profile for
courses that teach **principles and workflows** — the "why before what" teaching
style. Read it (and skim an example) before drafting any script or lesson.

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

## Script structure (course mode)

```
# Chapter N — Lesson M: Title

[opener paragraph — recap + pivot; NO [CLICK] before it]

[CLICK]
[one concept or list — mirrors the slide bullets]

[CLICK]
[next concept]

---
> 🎬 LIVE WALKTHROUGH — pivot to {tool}.
> [italic camera/screen directions]
[spoken demo narration, with exact commands in fenced blocks]
[end with "Back to the slides."]
---

[CLICK]   ← resumes slides

[closing transition: "In the next lesson, we will…" / "In Chapter N, we…"]
```

- `[CLICK]` is the **only** section marker (≈ one slide advance). No "INTRO/BODY"
  labels, no timestamps.
- **Openers** recap: first lesson of a chapter → "Welcome to Chapter N… so far…";
  mid-chapter → "In the previous lesson, we…".
- **Closers** bridge forward, always. The final lesson of the whole course ends
  with "Thanks for following along."
- Numbered/best-practice lessons use bold labels: `**First: version your images.**`
- Code blocks in the script are the exact code shown on screen (script and screen
  stay in sync).
- Length: 350–900 words per lesson (median ~550–650).

## Lesson README

- H1 `# Chapter N — Lesson M: Title`; open with the learning goal
  ("With this content, you will be able to…").
- Prose with `##` sections; code blocks and Mermaid where they clarify; close with
  a short "What's next".

## Avoid

- Hype adjectives ("powerful", "cutting-edge", "seamless") unless precise.
- Reading the learning objective aloud as a formal statement in the script.
- Inconsistent terminology — reuse the canonical terms from `spec/continuity.md`.
- Inventing features/commands not in the referenced materials.

## Refining this profile

Add or swap `examples/` with the author's best lessons; re-derive these rules from
them. The slide look for this profile is in `slide-style.md`.
