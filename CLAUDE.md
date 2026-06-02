# CLAUDE.md

Guidance for Claude when working in this repo.

## What this repo is

`my-agents` is a tool-neutral plugin **marketplace**. You author content **once**
under `source/`, and `scripts/build.py` compiles it into each tool's native
layout: a Claude Code marketplace (`.claude-plugin/marketplace.json` + `plugins/`)
and opencode (`.opencode/` + `opencode.json`).

## Golden rules (do not break these)

1. **Only edit under `source/`.** Never hand-edit generated output —
   `.claude-plugin/`, `plugins/`, `.opencode/`, `opencode.json`. `build.py`
   overwrites them wholesale, so manual edits are lost.
2. **After editing `source/`, run `python3 scripts/build.py`.** Then
   `python3 scripts/build.py --check` must pass (exit 0) before committing.
3. **Bump the plugin `version`** in `source/plugins/<name>/plugin.yaml` on *every*
   change to that plugin. Claude Code only re-installs when the version changes —
   same version means users never get the update. Use semver patch bumps for small
   edits (e.g. `0.1.2` → `0.1.3`).
4. **Keep `README.md` in sync.** When you add, remove, or rename a plugin (or
   change its description/version), update the **Available plugins** table in
   `README.md`. It is hand-maintained, not generated.
5. **Commit `source/` and generated files together** — Claude Code reads the
   generated files from the repo when adding the marketplace.

## Source format constraints

`plugin.yaml`, `marketplace.yaml`, and markdown frontmatter use a **flat YAML
subset** parsed by `build.py` (zero dependencies):

- One `key: value` per line; `#` comments allowed.
- Values are scalars (optionally quoted) or inline lists `[a, b, c]`.
- **No** nested maps or `- ` block lists. Nested objects use flat keys
  (`author_name`, `author_url`) and are rebuilt by the generator.

## Layout

```
source/plugins/<name>/
  plugin.yaml              manifest (flat keys)
  agents/*.md              neutral agent (frontmatter superset + prompt)
  commands/*.md            neutral command ($ARGUMENTS is portable)
  skills/<name>/SKILL.md   skill (Claude Code only; whole folder copied verbatim)
scripts/build.py           generator + `--check`
```

Cross-tool remapping (tool names, `mode`, skills-are-Claude-only, etc.) is
documented in `README.md`; the full authoring walkthrough is in
`docs/adding-a-plugin.md`. Follow those when adding or changing plugins.

## Conventions

- Skills are Claude-Code-only. Bundle a skill's reference files (sections,
  templates, style, scripts) **inside** `skills/<name>/` so they're copied with it.
- Prefer zero-dependency, stdlib-only Python for any scripts.
- When a skill researches the web, never fabricate: if a page can't be read, fall
  back (e.g. a rendering reader) or ask the user. See the `newsletter` plugin's
  `newsletter-builder` skill for the established pattern.
