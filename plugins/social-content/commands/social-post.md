---
description: "Draft a LinkedIn post, Reels script, or newsletter section from a course/workshop/newsletter/topic source."
argument-hint: [source: course|workshop|newsletter|topic] [format: linkedin|reels|newsletter-section] [template: list|lesson|contrarian|comparison] ...
---

Draft a social post using the **social-content** skill.

Inputs provided:

$ARGUMENTS

Expected input shape (ask me for anything missing, once and concisely):

```
source:           course | workshop | newsletter | topic
                  # course/workshop: path to the built output dir
                  # newsletter: path to a drafts/issue-*.md file
                  # topic: a one-line topic + 3-7 bullets I'll provide
format:           linkedin | reels | newsletter-section   # default: linkedin
                  # newsletter-section drafts a section body shaped to drop
                  # into a newsletter-builder issue (Open Source / Learning /
                  # Book slot).
template:         list | lesson | contrarian | comparison | learning-resource | opinion | <other>
                  # must match a subfolder in profiles/default/examples/
                  # IGNORED for format: newsletter-section.
newsletter-type:  open-source | learning | book   # only for format: newsletter-section
                  # if omitted, classify from the source URL
                  # (github → open-source; book publisher / Amazon /
                  # ISBN → book; everything else → learning).
newsletter-draft: skip | new | <path-to-existing>   # only for format: newsletter-section
                  # if omitted, the skill prompts at the end with these choices.
infographic:      yes | no                # default: no
diagram:          none | drawio           # default: none
slug:             <short-kebab-case>      # used in metadata + sidecar filenames
group:            template | <filename.md>
                  # default: template → posts/<template>-post.md (or -reels.md)
                  #          or  posts/<slug>-newsletter.md for newsletter-section
                  # custom: any filename → posts/<filename>
```

Then follow the social-content skill end to end: ingest the source, recommend
a template (or classify the newsletter-section content type) if I didn't pick
one, load voice + the template's example folder, draft in my voice, run the
QA checklist and the matching validator (`scripts/validate.py` for linkedin /
reels; `scripts/validate_newsletter_section.py` for newsletter-section), then
save the draft. For linkedin / reels, call `scripts/append_post.py` to insert
the entry at the top of the chosen `posts/...md` file (creating it on first
use). For newsletter-section, write the section body directly to
`posts/<slug>-newsletter.md`, then prompt me whether to inject it into a
newsletter pre-draft (`skip` / `new` / pick an existing issue) — the skill
runs `scripts/inject_section.py` with my answer. Place sidecars (drawio /
infographic) in `posts/assets/<slug>.<ext>` and reference them from the post
entry. Show me the file path written and a one-line summary.
