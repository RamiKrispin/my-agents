# Naming & title conventions

These are the defaults the tool generates. A course repo may already document its
own in `spec/naming-convention.md` — that file wins for that repo.

> Building a workshop? Use the sibling **workshop-builder** plugin instead.

## Folders

- Chapters: `chapter_{N}` (no zero-padding unless > 9).
- Lessons: `l{M}` — lowercase `l`, no padding (`l1`, `l2`, … `l10`), numbered in
  teaching order with no gaps. If order changes, renumber so there are no gaps.
- Scripts live in `script/ch{N}/`, **not** in the lesson folder.

## File names (chapter/lesson numbers embedded so files are unambiguous)

| File | Pattern | Example |
|---|---|---|
| Lesson notes | `README.md` | `README.md` |
| Script | `script_c{N}_l{M}.md` | `script_c2_l3.md` |
| Slides | `slides_c{N}_l{M}.html` | `slides_c2_l3.html` |

- Use `c{N}_l{M}` exactly (lowercase `c`/`l`, underscore). The numbers must match
  the folder. No bare `slides.html`.
- Supporting assets keep their natural, tool-expected names.

## Titles — one canonical title per lesson across README, script, and slides

- README & script H1: `# Chapter {N} — Lesson {M}: {Title}` (em dash, colon).
- Slides `<title>` / title slide: `Chapter {N} · Lesson {M} — {Title}` (middle dot, em dash).
- Title Case; render commands as plain text in titles (`docker build`), backticks
  are fine in body copy.

## Learning goals

Every lesson opens with a goal completing: **"With this content, you will be able
to…"** — reproduced at the top of the lesson README and indexed in
`spec/learning-goals.md`. Keep them in sync when a lesson changes.
