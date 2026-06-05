---
name: social-post
description: Draft a LinkedIn post or Reels script from a course/workshop/newsletter/topic source.
argument-hint: [source: course|workshop|newsletter|topic] [format: linkedin|reels] [template: list|lesson|contrarian|comparison] ...
---

Draft a social post using the **social-content** skill.

Inputs provided:

$ARGUMENTS

Expected input shape (ask me for anything missing, once and concisely):

```
source:      course | workshop | newsletter | topic
             # course/workshop: path to the built output dir
             # newsletter: path to a drafts/issue-*.md file
             # topic: a one-line topic + 3-7 bullets I'll provide
format:      linkedin | reels        # default: linkedin
template:    list | lesson | contrarian | comparison | learning-resource | opinion | <other>
             # must match a subfolder in profiles/default/examples/
infographic: yes | no                # default: no
diagram:     none | drawio           # default: none
slug:        <short-kebab-case>      # used in metadata + sidecar filenames
group:       template | <filename.md>
             # default: template → posts/<template>-post.md (or -reels.md)
             # custom: any filename → posts/<filename>
```

Then follow the social-content skill end to end: ingest the source, recommend
a template if I didn't pick one, load voice + the template's example folder,
draft in my voice, run the QA checklist and `scripts/validate.py` on the
body, then call `scripts/append_post.py` to insert the entry at the top of
the chosen `posts/...md` file (creating it on first use). Place sidecars
(drawio / infographic) in `posts/assets/<slug>.<ext>` and reference them from
the post entry. Show me the file path written and a one-line summary.
