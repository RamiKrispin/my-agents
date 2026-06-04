# social-content

Draft a **LinkedIn post** or a **Reels / TikTok script** in your voice — sourced
from a course-builder run, a workshop-builder run, a newsletter draft, or a
free-form topic. **Templates are user-curated example posts** under
`skills/social-content/profiles/default/examples/<template>/`: drop in your
real posts, the skill learns each template's hook and rhythm from them.
Drafts aggregate into per-template `posts/<template>-post.md` files in your
working directory, **newest at the top**, with QA / source-grounding notes
embedded in a collapsible `<details>` block per entry.

Install: `/plugin install social-content@my-agents` · Run: `/social-post`

## What's in this plugin

| Component | Type | Role |
| --- | --- | --- |
| `social-content` | skill | The pipeline: parse → ingest source → pick template → load voice + exemplars → draft → QA → append to `posts/<template>-post.md`. |
| `/social-post` | command | Entry point — pick source / format / template / optional add-ons. |

## What this plugin produces

A single Markdown file per template (and per format) in **your** working
directory:

```
<your repo>/
  posts/
    learning-resource-post.md      # LinkedIn, newest at top
    learning-resource-reels.md     # Reels / TikTok scripts (when you make video)
    opinion-post.md
    lesson-post.md
    contrarian-post.md
    list-post.md
    comparison-post.md
    assets/                        # sidecar files referenced from posts above
      <slug>.drawio
      <slug>.infographic.md
```

Each entry inside a `posts/<template>-post.md` file:

```markdown
## 2026-06-04 — Stanford CS25: Transformers

- **Source:** https://...
- **Slug:** stanford-cs25-transformers
- **Pillar:** Learning Radar
- **Status:** draft

<details><summary>Source notes</summary>
{citations, fact sheet, pre-post checks}
</details>

{post body — exactly what gets pasted to LinkedIn}
```

New entries are inserted directly below the file's H1 + intro; existing
entries shift down. If a slug already exists in the file, the helper exits
with an error so the skill can ask whether to overwrite, skip, or rename.

**Override the default file** with `group: <filename.md>` (e.g.
`group: 2026-q2-launch.md` writes to `posts/2026-q2-launch.md`).

## Templates (one folder per shape)

A **template** is a folder of your real posts. The skill reads every post in
the chosen folder and replicates the voice, structure, length, and rhythm
when drafting. Add new exemplars to evolve a template; add a new subfolder
to create a new template.

| Template | When to use |
| --- | --- |
| `list` | "5 X for Y", "Top N X" — multiple items compared |
| `lesson` | First-person experience: "I spent 3 hours debugging — here's what I learned" |
| `contrarian` | One bold against-the-grain claim, defended in tight structure |
| `comparison` | Side-by-side decision content: "RAG vs Fine-tuning" |
| `learning-resource` | Short curation post for a single course / tutorial / playlist (the **Curate** bucket) |
| `opinion` | First-person commentary on industry trends / news with reasoning + a forecast |

Each template's folder has a `README.md` documenting the derived shape
(hook patterns, length range, body structure, anti-patterns, boundary with
neighbouring templates). Open one — it's the source of truth for that
template.

## Sources

The skill ingests source material from one of four places and never invents
facts (every concrete claim must trace to the source):

- **`course`** — a built course-builder output dir (chapter / lesson scripts,
  READMEs, slides). See `skills/social-content/sources/from-course.md`.
- **`workshop`** — a built workshop-builder output dir (topic folders +
  combined deck). See `from-workshop.md`.
- **`newsletter`** — a `drafts/issue-YYYY-MM-DD.md` file from the
  `newsletter` plugin. See `from-newsletter.md`.
- **`topic`** — free-form: you provide a topic line + 3-7 bullets (and the
  skill verifies any named library / project via WebFetch). See
  `from-topic.md`.

## Voice (the source of truth)

Three layers, read in order on every run:

1. **`profiles/default/voice-guide.md`** — high-level tone rules. Functional
   emoji whitelist (`🚀 ✅ 📽️ ♻️ 🔔 📌 👇🏼`), banned hype phrases, recurring
   framings.
2. **`profiles/default/best-practices.md`** — distilled from LinkedIn's own
   content-creation course: 4 posting strategies (career insights, industry
   trends, BTS, milestones), 4 post elements (hook, value, visual, invite to
   converse), cadence rules, and anti-patterns the QA pass must block.
3. **`profiles/default/pillars.md`** — your 4 content pillars (Production AI
   35% / Docker 25% / Learning Radar 25% / Forecasting 15%) and the 70/20/10
   Teach / Curate / Promote rule.
4. **`profiles/default/examples/<template>/`** — your real posts, the
   authoritative pattern for the chosen template's hook + structure +
   length + rhythm.

## Add-ons

- **Infographic spec** (`infographic: yes`) → designer-facing brief written
  to `posts/assets/<slug>.infographic.md`.
- **drawio diagram** (`diagram: drawio`) → flat JSON node spec → emit
  `posts/assets/<slug>.drawio` via the bundled emitter. Open in
  [drawio](https://app.diagrams.net) to fine-tune visuals before exporting
  to PNG/SVG.

Both are **on request only** — defaults skip them.

## Workflow

1. **Parse** the request (source / format / template / add-ons / slug / group).
2. **Ingest the source** — build a fact sheet (5-15 grounded claims with
   citations). Anything that can't be verified stays out of the draft.
3. **Recommend a template** if you didn't pick one (skip if you did).
4. **Load voice** — voice-guide → best-practices → pillars → every post in
   `examples/<template>/`.
5. **Draft** following the chosen template's example folder + the
   format scaffold (`formats/linkedin-post.md` or `formats/reels-script.md`).
6. **Add-ons** (if requested) — write infographic spec / drawio sidecar to
   `posts/assets/`.
7. **QA** — run the checklist in `SKILL.md`; run
   `python3 scripts/validate.py <body.md>` (offline structural check).
   Iterate until `PASS`.
8. **Save** — `python3 scripts/append_post.py <posts-file> <meta.json> <body.md>`
   inserts the entry at the top of the chosen `posts/...md` file (creating
   it on first use). The helper builds the entry wrapper (H2 date heading +
   metadata bullets + collapsible source-notes block + body). Slug conflicts
   exit with an error.

## Helper scripts (zero dependencies, stdlib only)

All under `skills/social-content/scripts/`.

- `validate.py <file>` — offline structural check. Auto-detects aggregated
  posts files (H2 date headings) and validates **only the topmost entry's
  body**; single-post files validate as-is. Word-boundary banned-phrase
  match (`next-gen` flagged, `next-generation` not). Bullet-list paragraphs
  exempt from the line-cap.
- `append_post.py <posts-file> <meta.json> <body.md>` — inserts a new entry
  at the top. Creates the file with a default header on first run; detects
  slug conflicts; embeds optional `meta.notes` in a collapsible `<details>`
  block.
- `build_drawio.py <spec.json> <out.drawio>` — emits a `.drawio` XML file
  from a flat JSON node spec (nodes, edges, optional shapes / styles /
  layout = horizontal | vertical | grid).

## Adding new templates / new exemplars

- **New exemplar for an existing template:** drop a Markdown file in
  `profiles/default/examples/<template>/`. One file per post. The file is
  just the post text — no frontmatter, no commentary. Filenames are short
  and descriptive (e.g. `mlops-with-databricks.md`).
- **New template:** `mkdir profiles/default/examples/<new-template>/`,
  drop 3-7 real posts inside, write a `README.md` documenting the derived
  shape (look at `examples/learning-resource/README.md` or
  `examples/opinion/README.md` as references). Then add the template name
  to the lists in `SKILL.md`, `profiles/default/examples/README.md`,
  `sources/from-topic.md`, and `commands/social-post.md`. Bump the plugin
  version, run `python3 scripts/build.py`.

## Conventions

This plugin follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on every change. See the repo
`README.md` and `docs/adding-a-plugin.md`.

## Reference

- `skills/social-content/SKILL.md` — full skill instructions.
- `skills/social-content/profiles/default/examples/<template>/README.md` —
  per-template shape documentation.
- `skills/social-content/formats/{linkedin-post,reels-script,infographic-spec,drawio-diagram}.md` —
  format-specific scaffolds.
- `skills/social-content/sources/from-{course,workshop,newsletter,topic}.md` —
  source-specific ingestion guides.
