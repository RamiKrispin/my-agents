---
name: changelog
description: Generate or update a CHANGELOG.md entry from recent git commits, following the Keep a Changelog format. Use when the user wants to draft release notes or a changelog section.
---

# Changelog

Draft a clean changelog entry from git history, following the
[Keep a Changelog](https://keepachangelog.com/) conventions.

## When to use

Use this skill when the user asks to write release notes, draft a changelog
section, or summarize what changed since the last release/tag.

## Process

1. Find the range to summarize:
   - If a tag/version was given, use commits since that tag.
   - Otherwise, find the latest tag with `git describe --tags --abbrev=0` and
     summarize commits since then (`git log <tag>..HEAD --oneline`).
2. Read the commit messages (and diffs if a message is unclear).
3. Classify each meaningful change into one of the Keep a Changelog categories:
   `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
4. Write user-facing bullets — describe the impact, not the implementation.
   Skip noise (merge commits, formatting-only changes, version bumps).

## Output format

```markdown
## [Unreleased] - YYYY-MM-DD

### Added
- ...

### Fixed
- ...
```

If a `CHANGELOG.md` already exists, insert the new section at the top, below the
title, and preserve the existing entries.
