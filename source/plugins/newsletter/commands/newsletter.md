---
name: newsletter
description: Draft this week's data science newsletter from a set of links or prepared section files.
argument-hint: [open-source / learning / book values — URLs or .md paths]
---

Build this week's data science newsletter using the **newsletter-builder** skill.

Inputs provided:

$ARGUMENTS

Expected input shape (ask me for anything missing, once and concisely):

```
open-source: <github or project url> | <path-to-prepared-section.md>   # one or more
learning:    <course / tutorial / video / docs url> | <path-to-prepared-section.md>   # one or more
book:        <book url> | <path-to-prepared-section.md>                # one
```

A short note after any link (why it's interesting) is welcome — use it.

A value that ends with `.md` and resolves to an existing local file is
treated as a **prepared section** (typically produced by the `social-content`
plugin's `format: newsletter-section` mode). The skill skips research +
draft for that slot and inlines the file's content under the matching
heading. Voice pass and structural validate still run.

Then follow the newsletter-builder skill end to end: research each URL link,
draft the three sections in the fixed order (skipping any slot supplied as a
prepared file), write in my voice (the skill's `style/`), run the QA
checklist and `scripts/research.py validate`, then save the draft to the
configured output directory (default `drafts/issue-YYYY-MM-DD.md` in the
current working directory — see the skill's **Output location** section;
never inside the plugin) and show me the result.
