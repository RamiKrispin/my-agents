# Source: existing newsletter issue

Repurpose a newsletter draft (`drafts/issue-YYYY-MM-DD.md` produced by the
`newsletter` plugin) into a LinkedIn post or a Reels script. The newsletter
already does the research and citation work — your job is to repackage one
section, not all three.

## Expected input

A path to a Markdown file from the newsletter plugin's output:
`drafts/issue-YYYY-MM-DD.md`. Structure (see `newsletter/skills/newsletter-builder/`):

```markdown
# {Highlights} | Issue {N}
_A weekly curated update on data science and engineering topics and resources._

This week's agenda:
- ...

## Open Source of the Week
{the longest section — a single project, deeply described}

## New Learning Resources
{shorter — one or more learning items}

## Book of the Week
{medium — one book}
```

## What to read

1. The whole file (it's short — ~600-1,000 words). Don't sub-read.
2. Identify the user's intent — usually one of:
   - Promote one specific item (the open-source project, a book, a course).
   - Build a list-shaped post pulling all three items.
   - Take a stance on something the newsletter mentioned.

## Picking an angle

The newsletter format maps cleanly to social templates:

- **Open Source of the Week → `learning-resource` or `lesson`** — for the
  open-source project. If it's pure curation (sharing the project, with a
  one-line take and the project's feature list), use `learning-resource`. If
  there's a personal angle ("I used this in my Docker course last week"),
  reframe as a `lesson`.
- **All three sections → `list`** — "3 things I'm reading this week:
  {project}, {course}, {book}". Curation post — counts toward the 20% Curate
  bucket in 70/20/10.
- **New Learning Resources → `learning-resource`** — the most direct fit. One
  course / tutorial / playlist per post with its topic list.
- **Book of the Week → `lesson` or `learning-resource`** — pull one specific
  idea from the book and frame with personal experience, OR keep it as a
  short curation post.

## Repurposing rules

- **Don't copy the section verbatim.** LinkedIn isn't the newsletter — the hook
  needs to be sharper, paragraphs shorter, white space heavier.
- **Keep the citations.** Every grounded claim from the newsletter is already a
  fact sheet entry. Carry the URLs into the post (or first comment if
  LinkedIn's link-deprioritization matters).
- **Compress.** A 200-word newsletter section becomes a 100-word post +
  takeaway.
- **Add the personal layer.** The newsletter is a curator voice; LinkedIn
  benefits from a first-person hook ("I came across this project this week and
  it changed how I think about X").
- **Disclose.** If the newsletter promo'd a course / book / repo, the post can
  do the same — but the post counts toward 70/20/10 promotion budget.

## What NOT to pull

- The newsletter's intro/sign-off — they're newsletter-specific.
- The "This week's agenda:" bullets — they reference newsletter structure.
- The cross-post lines ("Also on LinkedIn / Medium") — circular.
