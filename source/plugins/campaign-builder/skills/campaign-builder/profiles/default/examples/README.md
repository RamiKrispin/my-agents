# Examples — User-Populated Per-Platform Library

This folder is the source of truth for each platform's voice. Each subfolder
matches one platform name from the skill's `platforms` input. When the skill
drafts a topic for `<platform>`, it reads **every post in
`examples/<platform>/`** as exemplars before drafting — voice, structure,
length, rhythm.

In v1 these folders ship empty. The skill falls back to format scaffolds
(`formats/<platform>.md`) and the voice guide when a folder is empty, and
warns the user. Drop real posts into the matching folder to sharpen the
template — the next campaign run picks them up automatically.

## Layout

```
examples/
  linkedin/             # long-form LinkedIn posts
  reels/                # Reels / TikTok script transcripts
  x-thread/             # X / Twitter threads (one file per thread)
  bluesky/              # Bluesky posts (single or short threads)
  threads/              # Instagram Threads posts
  instagram-carousel/   # carousel briefs (one file per carousel)
  blog/                 # full blog posts (Substack / Medium Markdown)
  video-script/         # combined video scripts (the campaign-builder format)
  README.md             # this file
```

## File format (per exemplar)

A single Markdown file containing **only the post text** — exactly as it
ran on the platform. No frontmatter, no commentary, no metadata. The first
line is the post's first line (the hook). Filenames are short and
descriptive, e.g. `2026-06-docker-image-size.md`.

For multi-post artifacts (X threads, Bluesky threads, carousel slide briefs):
follow the format scaffold in `../../formats/<platform>.md` — `## 1/`,
`## 2/`, etc. headings for thread posts; `### Slide N` headings for
carousel slides.

## Tips

- **Pick posts that performed well** — saves, comments, reshares. Those
  encode what the audience valued.
- **3-7 exemplars per platform** is the sweet spot. One overfits; ten
  becomes noise.
- **Keep platforms separate.** Don't put a LinkedIn post in `x-thread/`
  even if it's "thread-shaped" — the cross-platform compression patterns
  are different.
- **Cross-reference with social-content's `examples/<template>/`** — if
  you've already populated learning-resource / opinion / lesson folders
  there, the LinkedIn-specific shape is well-covered. campaign-builder's
  `examples/linkedin/` is for **campaign-style** LinkedIn posts (lead
  magnet voice, course CTA), which may differ.
