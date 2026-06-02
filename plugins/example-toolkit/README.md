# example-toolkit

A minimal, working **template** plugin — copy it as the starting point for a new
plugin. It demonstrates one of each artifact type.

Install: `/plugin install example-toolkit@my-agents`

## What's inside

| Component | Type | Role |
| --- | --- | --- |
| `code-reviewer` | agent | Reviews a diff/branch/PR for correctness bugs, security issues, and quality. |
| `/summarize-diff` | command | Summarizes the changes on the current branch vs a base branch. |
| `changelog` | skill | Drafts a [Keep a Changelog](https://keepachangelog.com/) entry from git history. |

## Use it as a template

1. Copy `source/plugins/example-toolkit/` to `source/plugins/<your-plugin>/`.
2. Edit `plugin.yaml` (name, description, version).
3. Replace the agent / command / skill with your own.
4. Run `python3 scripts/build.py`.

See [docs/adding-a-plugin.md](../../../docs/adding-a-plugin.md) for the full walkthrough.

## Conventions

Follows the marketplace conventions: edit under `source/`, run
`scripts/build.py`, bump the version on changes.
