---
name: newsletter
description: Draft this week's data science newsletter from a set of links.
argument-hint: [open-source / learning / book links]
---

Build this week's data science newsletter using the **newsletter-builder** skill.

Inputs provided:

$ARGUMENTS

Expected input shape (ask me for anything missing, once and concisely):

```
open-source: <github or project url>   # one or more
learning:    <course / tutorial / video / docs url>   # one or more
book:        <book url>                 # one
```

A short note after any link (why it's interesting) is welcome — use it.

Then follow the newsletter-builder skill end to end: research each link, draft
the three sections in the fixed order, write in my voice (the skill's `style/`),
run the QA checklist and `scripts/research.py validate`, then save the draft to
the configured output directory (default `drafts/issue-YYYY-MM-DD.md` in the
current working directory — see the skill's **Output location** section; never
inside the plugin) and show me the result.
