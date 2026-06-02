# my-agents

A personal **marketplace** of AI coding agents, slash commands, and skills —
authored once and compiled into the native format of multiple coding tools.

Today it targets **[Claude Code](https://docs.claude.com/en/docs/claude-code)**
and **[opencode](https://opencode.ai)**. Adding another tool is one emitter
function in the generator.

## Available plugins

| Plugin | Version | What's inside | Install (Claude Code) |
| --- | --- | --- | --- |
| **course-builder** | 0.1.1 | `course-builder` skill (orchestrator) + `course-content-creator` and `course-qa` subagents + a ported, theme-aware `course-slide-deck` skill, driven by `/course`. Builds a **course** (chapters/lessons with scripts + per-lesson slides) or a **workshop** (agenda topics + one combined deck, no scripts) stage-by-stage from a `spec/` source of truth, with a continuity ledger, named style profiles (default `design-principles`), step-by-step or all-at-once builds, and an independent QA pass. See [its README](plugins/course-builder/README.md). | `/plugin install course-builder@my-agents` |
| **newsletter** | 0.1.3 | `newsletter-builder` skill + `/newsletter` command. Drafts a weekly data science newsletter — the fixed *Open Source of the Week* → *New Learning Resources* → *Book of the Week* sections — from a set of links, in the author's voice. Researches each link (GitHub metadata, JS-rendering reader for fetch-hostile pages like O'Reilly/YouTube, ISBN→book lookup), runs a QA pass, and saves a Substack-ready draft. See [its README](plugins/newsletter/README.md). | `/plugin install newsletter@my-agents` |
| **example-toolkit** | 0.1.1 | `code-reviewer` agent, `/summarize-diff` command, and `changelog` skill — a minimal, working template to copy when starting a new plugin. See [its README](plugins/example-toolkit/README.md). | `/plugin install example-toolkit@my-agents` |

First add the marketplace (`/plugin marketplace add RamiKrispin/my-agents`, or a
local path — see [Connecting your tools](#connecting-your-tools)), then install.
Keep this table in sync when you add or remove a plugin under `source/plugins/`.

## How it works

You edit a single, tool-neutral copy of each agent/command/skill under
`source/`. Running the generator compiles that source into each tool's required
layout:

```
source/                         ← edit here (source of truth)
  marketplace.yaml              marketplace identity (name, owner, metadata)
  plugins/<plugin>/
    plugin.yaml                 plugin manifest
    agents/*.md                 neutral agent (frontmatter + prompt)
    commands/*.md               neutral command
    skills/<name>/SKILL.md      skill (Claude Code only)

scripts/build.py                generator: source/ → all tool outputs

── generated (do not hand-edit; commit them) ──
.claude-plugin/marketplace.json Claude Code marketplace manifest
plugins/<plugin>/...            Claude Code plugin (agents, commands, skills)
.opencode/agent/*.md            opencode agents (remapped frontmatter)
.opencode/command/*.md          opencode commands
opencode.json                   minimal opencode config
```

The generated files **are committed to the repo** — Claude Code clones this repo
and reads `.claude-plugin/marketplace.json` and `plugins/` directly. After
editing anything under `source/`, regenerate:

```bash
python3 scripts/build.py
```

No dependencies — plain Python 3, standard library only.

## Connecting your tools

### Claude Code

Add this repo as a marketplace, then install plugins from it:

```
/plugin marketplace add RamiKrispin/my-agents
/plugin install example-toolkit@my-agents
```

The `code-reviewer` agent, `/summarize-diff` command, and `changelog` skill from
that plugin become available. Manage with `/plugin` and
`/plugin marketplace list`.

### opencode

opencode auto-discovers agents and commands from a `.opencode/` directory.
Choose one:

- **Use this repo directly** — open it in opencode; `.opencode/` is already here.
- **Per project** — symlink or copy `.opencode/` into a project root:
  ```bash
  ln -s /path/to/my-agents/.opencode  /path/to/project/.opencode
  ```
- **Globally** — copy the contents into `~/.config/opencode/`:
  ```bash
  cp -r .opencode/agent   ~/.config/opencode/agent
  cp -r .opencode/command ~/.config/opencode/command
  ```

The `code-reviewer` agent and `summarize-diff` command then work in opencode.
(Skills are a Claude Code concept and are not emitted for opencode.)

## Adding your own content

See [docs/adding-a-plugin.md](docs/adding-a-plugin.md). In short: create a folder
under `source/plugins/`, add a `plugin.yaml`, an optional `README.md`, and your
`agents/`, `commands/`, and/or `skills/`, then run `python3 scripts/build.py`.
Each plugin should carry its own `README.md` documenting it (it ships with the
plugin).

## What gets remapped

| Neutral source                  | Claude Code                          | opencode                                       |
| ------------------------------- | ------------------------------------ | ---------------------------------------------- |
| `tools: [read, grep, bash]`     | `tools: Read, Grep, Bash`            | `tools: {read: true, …, write: false, …}`      |
| `model: sonnet`                 | `model: sonnet`                      | `model: sonnet`                                |
| `mode: subagent`                | *(ignored)*                          | `mode: subagent`                               |
| command `agent:` / `argument-hint:` | `argument-hint:` (agent ignored) | `agent:` (argument-hint ignored)               |
| `skills/`                       | copied as-is                         | *(skipped — no skill concept)*                 |

Prompt bodies are identical across tools (both use `$ARGUMENTS`), so they pass
through unchanged.

## CI

`python3 scripts/build.py --check` regenerates and fails if the committed
outputs are out of date — wire it into CI to keep `source/` and the generated
files in sync.
