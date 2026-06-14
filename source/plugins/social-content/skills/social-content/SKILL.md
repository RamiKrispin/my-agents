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
source:    course | workshop | newsletter | topic | url
           # course/workshop: path to the built output dir
           # newsletter: path to a drafts/issue-*.md file
           # topic:   a one-line topic + 3-7 bullet points the user provides
           # url:     a public link (YouTube, podcast, article, docs page) —
           #          researched in step 2 to build the fact sheet
format:    linkedin | reels | newsletter-section   # default: linkedin
           # newsletter-section drafts a section body shaped to drop into a
           # newsletter-builder issue (Open Source / Learning / Book slots).
template:  list | lesson | contrarian | comparison | learning-resource | opinion | <other>
           # must match a subfolder in profiles/default/examples/
           # if omitted, recommend one based on the source material
           # IGNORED for format: newsletter-section (template axis doesn't apply).
newsletter-type: open-source | learning | book   # only for format: newsletter-section
                                                # if omitted, classify from source (see below)
newsletter-draft: skip | new | <path>             # only for format: newsletter-section
                                                  # if omitted, prompt at the end of the run
infographic: yes | no              # default: no (on request only)
diagram:   none | drawio           # default: none (on request only)
slug:      <short-kebab-case>      # used in metadata + sidecar filenames
group:     template | <filename.md>
           # default: template — writes to posts/<template>-post.md (linkedin)
           #                     or  posts/<template>-reels.md (reels)
           #                     or  posts/<slug>-newsletter.md (newsletter-section)
           # custom: any filename — writes to posts/<filename>
           #         (e.g. group: 2026-q2-launch.md → posts/2026-q2-launch.md)
```

If the user gives a URL ("make a LinkedIn post about
https://youtube.com/..."), that's a `url` source — see
`sources/from-url.md`. If they describe a topic without a URL, that's a
`topic` source — ask for 3-7 bullets and a template.

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
   - `sources/from-url.md` — research a URL (video, article, blog post,
     podcast). Try WebFetch first; for fetch-hostile pages (YouTube,
     Coursera, Udemy, Medium, JS apps) fall back to
     `python3 scripts/research.py render <url>`.
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

   **Skip this step entirely for `format: newsletter-section`** — that
   format has its own three sub-shapes keyed by content type, not by the
   social-template axis. Instead, classify the content type: use
   `newsletter-type` if it was passed; otherwise classify from the source
   per the rules in `formats/newsletter-section.md` (canonical home). If the
   source is ambiguous, ask the user once — don't guess.

4. **Load voice + template exemplars** — read in this order:
   - `profiles/default/voice-guide.md` (high-level voice)
   - `profiles/default/best-practices.md` (LinkedIn course distilled — 4 posting strategies + 4 post elements + cadence + anti-patterns)
   - `profiles/default/pillars.md` (4 content pillars + 70/20/10)
   - **Every post under `profiles/default/examples/<template>/`**
   The example posts are the source of truth for the template's hook, structure,
   length, white space, and ending. Match them.

   **For `format: newsletter-section`**, skip the LinkedIn template
   exemplars (they don't apply) and instead read:
   - `profiles/default/voice-guide.md`, `best-practices.md`, `pillars.md`
     as above (voice still rules).
   - `formats/newsletter-section.md` (this skill's scaffold for the three
     sub-shapes — covers classification, voice register, output file).
   - `formats/newsletter-sections/<newsletter-type>.md` (the canonical
     section format spec — owned by the `newsletter` plugin and imported
     here at build time). Follow it exactly.

5. **Draft** — follow the format scaffold:
   - LinkedIn → `formats/linkedin-post.md`
   - Reels / TikTok → `formats/reels-script.md`
   - Newsletter section → `formats/newsletter-section.md` plus the
     type-specific spec at `formats/newsletter-sections/<newsletter-type>.md`
   The draft must obey both the format scaffold and the patterns observed in the
   chosen example folder. The template wins on hook + structure; the format
   scaffold wins on platform-specific shape (line breaks, on-screen text cues,
   etc.). Newsletter-section drafts have no template axis — the type-specific
   spec wins on shape; the voice files win on register.

6. **Add-ons** (only if requested):
   - **Infographic spec** → write a sidecar to `posts/assets/<slug>.infographic.md`
     following `formats/infographic-spec.md`. Reference it from the post entry
     with a relative link (`Infographic: [./assets/<slug>.infographic.md]`).
   - **drawio diagram** → write a flat node spec, then run
     `python3 scripts/build_drawio.py <spec.json> posts/assets/<slug>.drawio`
     to emit XML. Reference it from the post entry the same way. Use drawio
     when the post benefits from an architecture/flow diagram — see
     `formats/drawio-diagram.md`.

7. **QA** — write the post body to a temporary file, then run the validator
   for the chosen format:
   - `linkedin` / `reels` → `python3 scripts/validate.py <body.md>`
   - `newsletter-section` → `python3 scripts/validate_newsletter_section.py <newsletter-type> <body.md>`
   Iterate on the body until the validator prints `PASS` and the QA
   checklist below passes. **Do not append to the aggregated file (linkedin
   / reels) or write the final draft (newsletter-section) until QA passes.**

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

   **For `format: newsletter-section`**, the save shape is different —
   each draft is a self-contained section body intended to be inlined into
   a newsletter issue, not aggregated:
   - **Default file:** `posts/<slug>-newsletter.md` (no H1, no metadata
     wrapper — the literal section body that would be inlined under the
     newsletter's `## Open Source of the Week` / `## New Learning
     Resources` / `## Book of the Week` heading).
   - **Override:** if the user passed `group: <filename.md>`, write to
     `posts/<filename>` literally.
   - **No `append_post.py`** — write the file directly with `Write`, since
     there's no aggregated wrapper to maintain.
   - **No sidecars** by default — newsletter sections don't ship with
     infographics or drawio attachments. If the user explicitly requested
     one, place it under `posts/assets/<slug>.<ext>` as usual.

   Print the file path written and a one-line summary of what was added.

9. **Newsletter pre-draft injection** — only for `format: newsletter-section`,
   only after QA + step 8 have written the local section file.

   Resolve the newsletter output directory from the cwd's `CLAUDE.md`
   `## Skill output paths` section (look for a `newsletter-builder: <path>`
   bullet). If absent, ask the user once for the directory; offer to add a
   bullet to `CLAUDE.md` for next time. The default folder is `drafts/`
   relative to cwd.

   Decide what to do based on `newsletter-draft`:
   - `skip` (or user declines when prompted) — done.
   - `new` — pick today's `issue-YYYY-MM-DD.md` under the newsletter
     output directory (refuse if it already exists; suggest `--append`
     instead). Run:
     ```
     python3 scripts/inject_section.py --new <newsletter-out>/issue-YYYY-MM-DD.md \
       --type <newsletter-type> <section-file>
     ```
     The helper builds a fresh pre-draft from the imported newsletter
     template, fills the chosen slot with the section content, and leaves
     the other two slots as TODO placeholders.
   - `<existing path>` — run:
     ```
     python3 scripts/inject_section.py --append <path> --type <newsletter-type> <section-file>
     ```
     The helper appends the new section content under the matching `## ...`
     heading. Any existing content in that section is preserved and
     separated from the new content by a horizontal rule.

   If `newsletter-draft` was not passed, prompt the user once at the end of
   the run with three choices: `skip` / `new` / `<existing-draft-path>` (offer
   a list of existing `issue-*.md` files in the resolved directory if any).

   Print the pre-draft path written / appended-to and a one-line summary.

## QA checklist

- **Source-grounded**: every concrete claim (number, library, feature, stat,
  quote) traces to the fact sheet from step 2. No invented features. No vague
  "research shows" without a source.
- **Hook on line 1** *(LinkedIn / Reels only)*: the first line creates
  curiosity, surprise, a contrarian take, or a specific outcome. It works as
  a standalone (LinkedIn truncates). **Newsletter sections** open with the
  section spec's prescribed framing instead — not a hook.
- **One idea**: a reader can summarize the post in one sentence. If you find
  yourself teaching two unrelated things, split it.
- **Structure matches the chosen template's example posts** *(LinkedIn /
  Reels)* — sections, lengths, use of bullets/lists, white space pattern.
  **Newsletter sections** must match the imported type-specific spec at
  `formats/newsletter-sections/<newsletter-type>.md` exactly (heading levels,
  bullet shape, link policy, license / publisher lines).
- **Voice**: matches `voice-guide.md` and the example posts. No banned phrases
  from the "Avoid" list (no hype adjectives, no marketing language, no "Agree?",
  no "Thoughts?").
- **Mobile-readable** *(LinkedIn / Reels)*: short paragraphs (mostly 1-3
  lines). White space between ideas. Lists where appropriate.
- **Ending** *(LinkedIn / Reels)*: takeaway, question, or discussion prompt
  — not a generic "Agree?". Newsletter sections close per their spec
  (license line / "ideal for ..." / etc.), not with a CTA.
- **CTA / promo discipline** *(LinkedIn / Reels)*: respects the 70/20/10
  rule (mostly teach; promote rarely).
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
- `formats/newsletter-section.md` — scaffold for a body shaped to drop into
  a newsletter-builder issue (Open Source / Learning / Book sub-shapes).
- `formats/newsletter-sections/{open-source,learning,book}.md` — canonical
  type-specific section format specs. **Owned by the `newsletter` plugin**
  (`newsletter/skills/newsletter-builder/sections/`) and copied here at
  build time via `imports:` in `plugin.yaml`. Edit them in the newsletter
  source tree, not here.
- `formats/newsletter-template.md` — canonical assembly template, also
  imported from the newsletter plugin. Used by `inject_section.py --new`
  to scaffold a fresh pre-draft.
- `formats/infographic-spec.md` — designer-facing infographic brief format.
- `formats/drawio-diagram.md` — when to use drawio + the flat node spec format
  consumed by `scripts/build_drawio.py`.
- `sources/from-{course,workshop,newsletter,topic,url}.md` — source-specific
  ingestion guides.
- `scripts/research.py` — zero-dep stdlib: render a fetch-hostile page (JS
  apps / bot-blocked sites like YouTube, Coursera, Medium) via the public
  r.jina.ai reader and print clean Markdown. Mirrors newsletter-builder's
  `render` subcommand.
- `scripts/build_drawio.py` — zero-dep stdlib: emit a `.drawio` XML file from
  a flat JSON node spec.
- `scripts/validate.py` — offline checklist for a saved LinkedIn / Reels
  draft. Auto-detects aggregated posts files and validates only the topmost
  entry's body.
- `scripts/validate_newsletter_section.py` — offline structural check for a
  newsletter-section draft, keyed by content type (open-source / learning /
  book). Different rules from `validate.py` (no LinkedIn hook, longer body,
  type-specific required patterns).
- `scripts/append_post.py` — insert a new post entry at the top of an
  aggregated `posts/<template>-post.md` file. Handles file creation,
  slug-conflict detection, and the entry wrapper. Used for `linkedin` /
  `reels` only — newsletter-section drafts are written directly.
- `scripts/inject_section.py` — drop a prepared newsletter section into a
  newsletter pre-draft (`--new` from template, or `--append` into an
  existing issue file under the matching `## ...` heading).

## Notes

- The example posts are the source of truth for each template — re-read the
  chosen folder every run. When you (the user) add new posts, the template
  evolves automatically.
- If a template folder is empty, fall back to `best-practices.md` and
  `voice-guide.md` only, and warn the user that voice will be weaker without
  exemplars.
- Keep it concrete and concise. Substance over adjectives. Don't write what
  anyone could write — write what only Rami can write.
