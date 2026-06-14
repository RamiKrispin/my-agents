# Adding a plugin

Everything you author lives under `source/`. After any change, run the generator
to compile the tool-native outputs:

```bash
python3 scripts/build.py
```

## 1. Create the plugin folder

```
source/plugins/<your-plugin>/
  plugin.yaml
  README.md          # documents the plugin; shipped with it
  agents/
  commands/
  skills/
```

You only need the subfolders you actually use. A `README.md` at the plugin root
is optional but recommended — the generator copies it into the built plugin.

## 2. Write `plugin.yaml`

This is a **flat** key/value file (no nested maps or block lists; inline lists
use `[a, b, c]`). The generator turns it into the Claude Code `plugin.json` and
the marketplace entry.

```yaml
name: your-plugin            # kebab-case, unique within the marketplace
description: One line describing the plugin.
version: 0.1.0               # bump this on EVERY change — Claude Code only
                             # re-installs when the version changes
author_name: Rami Krispin    # optional
author_url: https://github.com/RamiKrispin   # optional (or author_email)
homepage: https://github.com/RamiKrispin/my-agents   # optional
license: MIT                 # optional
category: productivity       # optional (marketplace grouping)
keywords: [foo, bar]         # optional
```

## 3. Add agents — `agents/<name>.md`

Neutral frontmatter is a **superset**; each field maps to the right place per
tool (see the table in the README). Frontmatter values are flat scalars or
inline `[a, b]` lists.

```markdown
---
name: my-agent
description: What it does and when to use it. (Used by tools to auto-select it.)
model: sonnet            # optional: sonnet | opus | haiku
mode: subagent           # optional, opencode only: primary | subagent | all
tools: [read, grep, glob, bash]   # optional allow-list; omit to allow all
---

The system prompt body goes here. Write it tool-agnostically.
```

**Tool names** are neutral/lowercase and get remapped:
`read, write, edit, bash, grep, glob, list, webfetch, websearch, task, todowrite`.
A `tools:` allow-list restricts the agent to those tools in both Claude Code and
opencode. Omit `tools:` to allow everything.

## 4. Add commands — `commands/<name>.md`

```markdown
---
name: my-command
description: What the command does.
argument-hint: [some-arg]   # optional (Claude Code)
agent: my-agent             # optional (opencode: which agent runs it)
model: sonnet               # optional
tools: [read, bash]         # optional → Claude Code allowed-tools
---

The prompt template. Use `$ARGUMENTS` for the user's input (portable across
both tools).
```

## 5. Add skills — `skills/<name>/SKILL.md`

Skills are a **Claude Code** concept and are copied through unchanged (not
emitted for opencode).

```markdown
---
name: my-skill
description: When this skill applies and what it produces.
---

# My skill

Instructions / reference material the model loads when the skill triggers.
```

You can include supporting files alongside `SKILL.md` in the same folder; the
whole `skills/<name>/` directory is copied verbatim.

## 6. (Optional) Hooks and MCP servers — Claude Code only

If a plugin folder contains `hooks/` or a `.mcp.json`, they are copied verbatim
into the generated Claude Code plugin. These have no opencode equivalent here
and are not converted.

## 7. (Optional) Cross-plugin shared assets — `imports:`

When two plugins need to share a file or directory (a format spec, a
template, a style guide), keep one canonical copy and have the other import
it at build time. Add an `imports:` field to the importing plugin's
`plugin.yaml`:

```yaml
imports: [<src> > <dst>, <src2> > <dst2>]
```

Each entry has the form `<src-relative-to-source/plugins> > <dst-relative-to-built-plugin>`.
The build copies the source file (or directory tree) into the built plugin's
output. Source files are *not* duplicated in the importing plugin's
`source/` tree — they live with their canonical owner only.

Example: `social-content` imports the newsletter section format spec and the
newsletter assembly template from the `newsletter` plugin:

```yaml
imports: [newsletter/skills/newsletter-builder/sections > skills/social-content/formats/newsletter-sections, newsletter/skills/newsletter-builder/templates/newsletter-template.md > skills/social-content/formats/newsletter-template.md]
```

Notes:

- The build fails if a `<src>` path doesn't exist — typo-safe.
- Imports are Claude-Code-only (no opencode equivalent — opencode plugins
  don't ship skills).
- Bump the importing plugin's `version` whenever the imported source
  changes; otherwise installs of the importing plugin won't pick up the
  refresh.

## 8. Regenerate, sync docs, and commit

After any change to a plugin:

1. **Bump the plugin `version`** in its `plugin.yaml` (even for small edits).
   Claude Code only re-installs a plugin when the version changes. If you
   edited a file that another plugin `imports:` from, bump the **importing**
   plugin's version too — otherwise installs of that plugin won't pick up
   the refresh.
2. **Regenerate** the tool outputs:
   ```bash
   python3 scripts/build.py
   ```
3. **Update the README** — keep the *Available plugins* table in sync (add or
   remove the row; update the version and description).
4. **Verify** nothing is stale:
   ```bash
   python3 scripts/build.py --check
   ```
5. **Commit** source and generated files together:
   ```bash
   git add -A
   git commit -m "Add/update <your-plugin>"
   ```

The generated files **must** be committed — Claude Code reads them from the repo
when it adds the marketplace.

To pull the update into a running Claude Code session:
`/plugin marketplace update my-agents` then `/reload-skills` (or reinstall the
plugin with `/plugin uninstall` + `/plugin install`).

## Source format constraints

The zero-dependency parser intentionally supports only a small YAML subset:

- One `key: value` pair per line; `#` comments allowed.
- Values are scalars (optionally quoted) or inline lists `[a, b, c]`.
- **No** nested maps or `- ` block lists. Nested objects (like an author) are
  expressed as flat keys (`author_name`, `author_url`) and rebuilt by the
  generator.

This keeps the toolchain dependency-free and predictable.
