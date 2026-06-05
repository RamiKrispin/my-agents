# Examples — User-Populated Template Library

This folder is the **source of truth for templates**. Each subfolder is one
template; each file in a subfolder is one real post (preferably one Rami already
posted) that demonstrates the template's hook, structure, length, and rhythm.

The skill, when invoked with `template: <name>`, reads **every post** in
`<name>/` and uses them as exemplars — voice, shape, white space, ending.
Adding a new post to a subfolder makes the template more accurate. Adding a new
subfolder creates a new template.

## Layout

```
examples/
  list/                # "5 Python libraries for time series forecasting"
  lesson/              # "I spent 3 hours debugging — here's what I learned"
  contrarian/          # "Most AI agent failures have nothing to do with prompts"
  comparison/          # "RAG vs Fine-tuning"
  learning-resource/   # short curation post for a single course / tutorial / playlist
  opinion/             # first-person commentary on industry trends / news, with reasoning + a forecast
  README.md            # this file
```

To add a new template (e.g. `behind-the-scenes`, `framework`, `checklist`):
just `mkdir behind-the-scenes/` and drop a few real posts inside.

## File format

Each file is a Markdown file containing **only the post text** — exactly as it
ran on LinkedIn. No frontmatter, no commentary, no metadata. The first line of
the file is the post's first line (the hook). Filenames are short and
descriptive, e.g. `2024-12-docker-image-size.md`.

```
{hook line}

{body, exactly as posted, including line breaks and white space}

{ending}
```

Optional: a sibling `<filename>.notes.md` with a one-line note explaining why
this post worked or what's representative about it. The skill ignores `.notes.md`
files when learning the template — they're for humans.

## Tips for picking exemplars

- Pick posts that **performed well** (saves, comments, reshares) — those encode
  what the audience valued.
- Pick **3-7 per template** when possible. One example overfits to one post; ten
  becomes noise.
- Keep templates **shape-pure**. If a post is "list-shaped but really a lesson",
  put it under `lesson/` — the skill learns hook + structure from the folder.
- It's fine to have **the same post in two folders** if it really fits both —
  but prefer to pick the dominant shape.

## What the skill does with these

When `template: list` is requested, the skill reads:

1. `voice-guide.md` (tone)
2. `best-practices.md` (rules)
3. `pillars.md` (mix)
4. **Every `*.md` file in `examples/list/` (excluding `*.notes.md`)** — the
   exemplars

Then drafts a new post that matches the exemplars' hook style, structure,
length, and rhythm — about new source material.

If a template folder is **empty**, the skill falls back to the format scaffold
under `formats/` and warns the user that voice will be weaker without
exemplars.
