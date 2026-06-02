# Naming & Structure Convention

> Source of truth for how this course is organized. Follow it whenever adding or
> renaming a lesson.

## Folder layout

```
chapter_{N}/l{M}/   README.md · slides_c{N}_l{M}.html · <assets>
script/ch{N}/       script_c{N}_l{M}.md
spec/               development docs
```

- Chapters: `chapter_{N}` (no padding unless > 9).
- Lessons: `l{M}` — lowercase `l`, no padding, teaching order, no gaps.
- Scripts live in `script/ch{N}/`, not the lesson folder.

## File names

| File | Pattern | Example |
| ---- | ------- | ------- |
| Lesson notes | `README.md` | `README.md` |
| Script | `script_c{N}_l{M}.md` | `script_c2_l3.md` |
| Slides | `slides_c{N}_l{M}.html` | `slides_c2_l3.html` |

Use `c{N}_l{M}` exactly; numbers must match the folder. No bare `slides.html`.
Supporting assets keep their natural names.

## Title format (one canonical title per lesson)

- README & script H1: `# Chapter {N} — Lesson {M}: {Title}`
- Slides `<title>` / title slide: `Chapter {N} · Lesson {M} — {Title}`
- Title Case; commands as plain text in titles.

## Checklist for adding a lesson

1. Create `chapter_{N}/l{M}/` and `script/ch{N}/` if needed.
2. Add `README.md` + `slides_c{N}_l{M}.html` + `script_c{N}_l{M}.md`.
3. One canonical title across all three.
4. Verify `c{N}_l{M}` matches the folder.
5. Renumber with no gaps if order changes.
6. Update `learning-goals.md` and `continuity.md`.
