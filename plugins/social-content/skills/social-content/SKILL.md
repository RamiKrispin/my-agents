---
name: social-content
description: Draft LinkedIn posts and short-form video (Reels / TikTok) scripts in Rami Krispin's voice from a course-builder run, a workshop-builder run, a newsletter issue, or a free-form topic. Templates are user-curated example posts under profiles/default/examples/. Use when building, drafting, or repurposing technical content for social platforms — including supporting video scripts, optional infographic specs, and optional drawio diagrams. Produces a Markdown draft per platform.
---

# Social Content

Draft a single piece of social content — a **LinkedIn post** or a **short-form
video script** (Reels / TikTok) — in Rami's voice, grounded in real source
material. **Never fabricate.** Every concrete claim, number, library name, or
feature must trace to a researched source (a built course/workshop output, a
newsletter draft, or a fact the user provided). If something can't be verified,
say so and ask.

## Inputs

The user will pick a **source**, a **format**, and (optionally) a **template**.
Ask once and concisely for anything missing — don't proceed on guesses.

```
source:    course | workshop | newsletter | topic
           # course/workshop: path to the built output dir
           # newsletter: path to a drafts/issue-*.md file
           # topic: a one-line topic + 3-7 bullet points the user provides
format:    linkedin | reels        # default: linkedin
template:  list | lesson | contrarian | comparison | learning-resource | opinion | <other>
           # must match a subfolder in profiles/default/examples/
           # if omitted, recommend one based on the source material
infographic: yes | no              # default: no (on request only)
diagram:   none | drawio           # default: none (on request only)
slug:      <short-kebab-case>      # used in metadata + sidecar filenames
group:     template | <filename.md>
           # default: template — writes to posts/<template>-post.md (linkedin)
           #                     or  posts/<template>-reels.md (reels)
           # custom: any filename — writes to posts/<filename>
           #         (e.g. group: 2026-q2-launch.md → posts/2026-q2-launch.md)
```

If the user just says "make a LinkedIn post about X", that's a `topic` source —
ask for 3-7 bullets they want covered, plus pick a template.

## Output location

Drafts (`posts/<template>-post.md`, `posts/<template>-reels.md`, custom
`posts/<filename>`, and sidecars under `posts/assets/`) are written to the
**user's current working directory** — **never inside this skill's / plugin's
folder**. The files under this skill (`profiles/`, `formats/`, `sources/`,
`scripts/`) are read-only resources at runtime; only ever read them, never
write next to them.

Resolve the output base directory at the start of every run, before drafting:

1. **Read** the cwd's `CLAUDE.md` (if present). If it has a
   `## Skill output paths` section with a `social-content: <path>` bullet, use
   that path as the parent of `posts/` (relative to cwd, or absolute). Skip to
   "Save".
2. **Otherwise** (no `CLAUDE.md`, or no `social-content` line in it), ask the
   user **once**, concisely:
   - Confirm the cwd is the right place (print it).
   - Propose `.` (so drafts land at `<cwd>/posts/...`) as the default. Let
     them pick another path if they prefer.
   - Ask whether to **remember** the choice for future runs by adding a line to
     the cwd's `CLAUDE.md`. If yes:
     - Create `CLAUDE.md` if it doesn't exist.
     - If a `## Skill output paths` section already exists, append a bullet to
       it. Otherwise append the section at the end:
       ```markdown
       ## Skill output paths

       - social-content: <chosen-path>
       ```
     - Do **not** rewrite or reorder the rest of `CLAUDE.md`.
   - Create the chosen folder + its `posts/` subfolder if they don't exist,
     then proceed.
3. **Safety net:** if the cwd looks like a clone of the my-agents marketplace
   repo (contains `source/plugins/` or `.claude-plugin/marketplace.json`),
   refuse to write there by default — ask the user for an explicit output
   directory outside the marketplace before continuing.

All `posts/...` paths in the rest of this skill are interpreted relative to
that resolved output base.

## Workflow

Run these in order. Load voice + the chosen template's example posts **before**
drafting, so the first draft is already in voice and shape.

1. **Parse the request** — identify source type, format, template, and any
   add-ons (infographic, diagram). Confirm a one-line slug for filenames.

2. **Ingest the source** — follow the matching guide:
   - `sources/from-course.md` — read a course-builder output dir
   - `sources/from-workshop.md` — read a workshop-builder output dir
   - `sources/from-newsletter.md` — repurpose a newsletter draft
   - `sources/from-topic.md` — free-form topic + bullets
   Build a fact sheet: 5-15 concrete claims with citations (file path or URL).
   Anything you can't ground stays out of the draft.

3. **Recommend a template** (if the user didn't pick one) — match the material
   to a subfolder of `profiles/default/examples/`. List → "5 X for Y";
   Lesson → personal experience; Contrarian → one bold against-the-grain
   claim defended in tight structure; Comparison → X vs Y; Learning-resource
   → short curation post for a single course / tutorial / playlist (the
   **Curate** bucket); Opinion → first-person commentary on industry trends
   / news with reasoning and a forecast (the **Industry trends and
   commentary** strategy in `best-practices.md`). If no folder fits, ask the
   user which template to use.

4. **Load voice + template exemplars** — read in this order:
   - `profiles/default/voice-guide.md` (high-level voice)
   - `profiles/default/best-practices.md` (LinkedIn course distilled — 4 posting strategies + 4 post elements + cadence + anti-patterns)
   - `profiles/default/pillars.md` (4 content pillars + 70/20/10)
   - **Every post under `profiles/default/examples/<template>/`**
   The example posts are the source of truth for the template's hook, structure,
   length, white space, and ending. Match them.

5. **Draft** — follow the format scaffold:
   - LinkedIn → `formats/linkedin-post.md`
   - Reels / TikTok → `formats/reels-script.md`
   The draft must obey both the format scaffold and the patterns observed in the
   chosen example folder. The template wins on hook + structure; the format
   scaffold wins on platform-specific shape (line breaks, on-screen text cues,
   etc.).

6. **Add-ons** (only if requested):
   - **Infographic spec** → write a sidecar to `posts/assets/<slug>.infographic.md`
     following `formats/infographic-spec.md`. Reference it from the post entry
     with a relative link (`Infographic: [./assets/<slug>.infographic.md]`).
   - **drawio diagram** → write a flat node spec, then run
     `python3 scripts/build_drawio.py <spec.json> posts/assets/<slug>.drawio`
     to emit XML. Reference it from the post entry the same way. Use drawio
     when the post benefits from an architecture/flow diagram — see
     `formats/drawio-diagram.md`.

7. **QA** — write the post body to a temporary file, then run
   `python3 scripts/validate.py <body.md>` (offline structural check). Iterate
   on the body until validate.py prints `PASS` and the QA checklist below
   passes. **Do not append to the aggregated file until QA passes.**

8. **Save** — append the entry to a per-template aggregated file in the
   **user's working directory** (NOT inside the plugin):
   - **Default file:** `posts/<template>-post.md` for `format: linkedin`,
     `posts/<template>-reels.md` for `format: reels`. Created on first use
     for that template/format combo, with a default H1 + intro.
   - **Override:** if the user passed `group: <filename.md>`, write to
     `posts/<filename>` literally (e.g. `posts/2026-q2-launch.md`).
   - **Append-to-top:** new entries are inserted directly below the H1 +
     intro; existing entries shift down. Newest is always on top.
   - **Slug conflict:** if the same slug already exists in the file, the
     helper exits with an error — ask the user whether to overwrite, skip,
     or rename, and act on their answer.
   - **How to write:** prepare a small `meta.json` (title, slug, date, source,
     pillar, format, status, optional notes) plus a `body.md` (literal post
     text), then run:
     ```
     python3 scripts/append_post.py <posts-file> <meta.json> <body.md>
     ```
     The helper handles file creation, header, slug-conflict detection, and
     the entry wrapper (H2 date heading + metadata bullets + collapsible
     `<details>Source notes</details>` block + body).
   - **Notes:** put the source-grounding notes (fact sheet citations,
     pre-post checks) in `meta.notes` — the helper embeds them in a
     collapsible `<details>` block, hidden by default in rendered Markdown.
   - **Sidecars:** drawio / infographic files live in `posts/assets/<slug>.<ext>`,
     referenced from the post entry via relative links.
   - Print the file path written and a one-line summary of what was added.

## QA checklist

- **Source-grounded**: every concrete claim (number, library, feature, stat,
  quote) traces to the fact sheet from step 2. No invented features. No vague
  "research shows" without a source.
- **Hook on line 1**: the first line creates curiosity, surprise, a contrarian
  take, or a specific outcome. It works as a standalone (LinkedIn truncates).
- **One idea**: a reader can summarize the post in one sentence. If you find
  yourself teaching two unrelated things, split it.
- **Structure matches the chosen template's example posts** — sections, lengths,
  use of bullets/lists, white space pattern.
- **Voice**: matches `voice-guide.md` and the example posts. No banned phrases
  from the "Avoid" list (no hype adjectives, no marketing language, no "Agree?",
  no "Thoughts?").
- **Mobile-readable**: short paragraphs (mostly 1-3 lines). White space between
  ideas. Lists where appropriate.
- **Ending**: takeaway, question, or discussion prompt — not a generic "Agree?".
- **CTA / promo discipline**: respects the 70/20/10 rule (mostly teach; promote
  rarely).
- **Reels-only**: hook within the first 3 seconds; on-screen text cues present;
  one clear takeaway; under target length (typically 30-90s).

Output `PASS`, or a bulleted `FAIL` list, and fix before saving.

## Files in this skill

- `profiles/default/voice-guide.md` — high-level voice rules.
- `profiles/default/best-practices.md` — LinkedIn's own content guidance distilled: 4 posting strategies, 4 post elements, cadence, and anti-patterns the QA pass must block.
- `profiles/default/pillars.md` — 4 content pillars + 70/20/10 mix.
- `profiles/default/examples/<template>/` — **user-populated** real posts that
  define each template. The skill learns the template by reading these. New
  templates = new subfolder + a few example posts.
- `formats/linkedin-post.md` — generic LinkedIn structure scaffold.
- `formats/reels-script.md` — Reels / TikTok script scaffold (hook, beats,
  on-screen text, captions, CTA).
- `formats/infographic-spec.md` — designer-facing infographic brief format.
- `formats/drawio-diagram.md` — when to use drawio + the flat node spec format
  consumed by `scripts/build_drawio.py`.
- `sources/from-{course,workshop,newsletter,topic}.md` — source-specific
  ingestion guides.
- `scripts/build_drawio.py` — zero-dep stdlib: emit a `.drawio` XML file from
  a flat JSON node spec.
- `scripts/validate.py` — offline checklist for a saved draft. Auto-detects
  aggregated posts files and validates only the topmost entry's body.
- `scripts/append_post.py` — insert a new post entry at the top of an
  aggregated `posts/<template>-post.md` file. Handles file creation,
  slug-conflict detection, and the entry wrapper.

## Notes

- The example posts are the source of truth for each template — re-read the
  chosen folder every run. When you (the user) add new posts, the template
  evolves automatically.
- If a template folder is empty, fall back to `best-practices.md` and
  `voice-guide.md` only, and warn the user that voice will be weaker without
  exemplars.
- Keep it concrete and concise. Substance over adjectives. Don't write what
  anyone could write — write what only Rami can write.
