# Output structure

The course-builder writes into the **target repo** (where the course lives),
never into the marketplace. `spec/` holds the development docs; the rest is
learner-facing.

> Building a workshop? Use the sibling **workshop-builder** plugin instead.

```
spec/                              development docs (source of truth)
  course-spec.md
  naming-convention.md
  learning-goals.md
  continuity.md
  open-items.md
  scope-chapter-{N}.md             one per chapter, written just before building
  style/                           OPTIONAL per-repo profile override

chapter_{N}/                       one folder per chapter, N = 1..k
  l{M}/                            one folder per lesson, M = 1..k (no gaps)
    README.md                      lesson notes / reference
    slides_c{N}_l{M}.html          one deck per lesson
    <supporting files>             Dockerfile, *.py, *.sh, *.drawio, DEMO.md, …

script/                            narration scripts (separate tree)
  ch{N}/
    script_c{N}_l{M}.md
  script_opening.md                course-level scripts (optional)
  script_closing.md
```
