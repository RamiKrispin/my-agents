---
description: "Summarize the changes between the current branch and a base branch."
argument-hint: [base-branch]
model: sonnet
---

Summarize the changes on the current branch compared to a base branch.

The base branch is `$ARGUMENTS` (default to `main` if no argument was provided).

Steps:

1. Run `git diff <base>...HEAD --stat` to see which files changed.
2. Run `git log <base>..HEAD --oneline` to see the commits.
3. Read the diff for the most significant files.

Then produce:

- A one-paragraph **summary** of what the branch does.
- A bulleted **list of notable changes**, grouped by area.
- Any **risks or follow-ups** a reviewer should pay attention to.

Keep it concise and skimmable.
