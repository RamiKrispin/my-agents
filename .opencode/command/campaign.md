---
description: "Build a multi-platform promotion campaign from a course / workshop / topic. Per-topic, per-platform drafts written one at a time."
---

Build a promotion campaign using the **campaign-builder** skill.

Inputs provided:

$ARGUMENTS

Expected input shape (ask me for anything missing, once and concisely — never
guess defaults for `platforms`):

```
source:      <path-to-course-or-workshop-root>
             # course-builder: dir with spec/course-spec.md
             # workshop-builder: dir with spec/workshop-spec.md
             # LinkedIn-Learning-style: dir with chapter_0/learning_goals.md
scope:       chapter <N> | lessons <list> | theme <description>
             # e.g. "chapter 2", "lessons 2.1, 2.3, 5.4", "theme: Docker security across chapters 2 and 5"
platforms:   <comma-separated list>
             # REQUIRED — must be specified. Available options:
             #   linkedin, reels, x-thread, bluesky, threads,
             #   instagram-carousel, video-script, blog
             # if missing, the skill asks once with the full menu — no silent defaults
blog_count:  0 | 1 | 2 | 3              # default 0 (only if `blog` in platforms)
blog_length: 800 | 1500 | 2000 ...      # words; default 1500
video_length: 30s | 60s | 90s ...       # seconds; default 60s
pace:        per-topic | continuous     # default per-topic — checkpoint after each topic
slug:        <kebab-case>               # optional; AI proposes one if absent
```

Then follow the campaign-builder skill end to end:

1. **Detect** the source layout (course-builder / workshop-builder / LinkedIn-Learning).
2. **Ingest** the course materials scoped to my requested chapter / lessons / theme.
3. **Propose** a topic list and write `campaigns/<slug>/campaign.md` with `Status: PROPOSED`.
4. **Stop** and wait for me to set `Status: APPROVED` (or `Status: REVISE` with notes).
5. On approval, **fan out per topic, one platform at a time.** After each topic,
   stop, summarize what was written, and wait for me to say continue (unless
   `pace: continuous`).
6. **Save** every draft under `campaigns/<slug>/topics/NN-<topic-slug>/<platform>.md`,
   blogs under `campaigns/<slug>/blog/`, sidecars under `campaigns/<slug>/assets/`.
7. **Print** the file tree at the end.

Never fabricate. Every concrete claim traces to a course file (path + line
where useful). If a fact can't be grounded, flag it in `campaign.md` open
items rather than inventing.
