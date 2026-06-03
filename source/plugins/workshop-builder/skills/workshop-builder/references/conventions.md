# Naming & title conventions

These are the defaults the tool generates. A workshop repo may already document
its own in a `spec/naming-convention.md` — that file wins for that repo.

## Folders

- Topics: `NN_topic_name` — two-digit order prefix + snake_case label
  (`01_intro`, `02_environment_setup`, `03_first_app`). Renumber with no gaps if
  the agenda reorders.

## Files

| File | Pattern | Example |
|---|---|---|
| Combined deck (default) | `slides/workshop_slides.html` | `slides/workshop_slides.html` |
| Per-topic deck (opt-in) | `slides/NN_topic_name.html` | `slides/02_environment_setup.html` |
| Topic README (opt-in) | `NN_topic_name/README.md` | `02_environment_setup/README.md` |

- Always create `slides/` if it doesn't exist; never put deck files inside topic
  folders.
- Supporting code/docs keep their natural names, inside the topic folder.

## Titles

One canonical title per topic, used everywhere it appears:

- Topic README (when emitted) H1: `# {NN} — {Topic Title}`
- Slide section divider for the topic: `{NN} — {Topic Title}`
- Title Case; render commands as plain text in titles (`docker build`),
  backticks are fine in body copy.

## Hard rules

- **No** `script/` tree or `script_*.md` files. Workshops have no scripts.
- Topic README is **opt-in** in `spec/workshop-spec.md`. Don't emit one unless
  the spec says so.
- Slide-split preference is recorded in `spec/workshop-spec.md`. Pick exactly
  one of: combined `slides/workshop_slides.html`, or per-topic
  `slides/NN_topic_name.html`. Don't mix.
