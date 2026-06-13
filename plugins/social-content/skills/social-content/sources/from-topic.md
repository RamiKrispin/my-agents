# Source: free-form topic + bullets

When the user wants a post about a topic that **isn't** sourced from a course,
workshop, newsletter, or single URL. They provide:

- A one-line **topic** (e.g. "5 Python libraries for time series forecasting").
- **3-7 bullets** they want covered (the substance — not the post structure).
- Optional: a **template** preference. If absent, recommend one based on the
  topic shape.

This is the path for templated posts like "top N X for Y" — the example you
gave: *5 Python libraries for time series forecasting* and
*top 10 courses for deep learning*.

> If the topic is a single URL (a YouTube video, podcast episode, article,
> or blog post), see `from-url.md` instead — the skill will research the
> link to build the fact sheet rather than asking the user for bullets.

## What to ask if anything's missing

- **Topic line** — must be specific. "AI agents" isn't enough; "Why AI agents
  need validation layers" is.
- **3-7 bullets** — the actual content. Each bullet is a fact, library name,
  story, or claim the user wants in the post. If the user gives 1-2 bullets,
  ask for more — the post will be thin without them.
- **Template** — if not given, recommend one (`list` for top-N, `lesson` for
  personal stories, etc.).
- **Pillar tag** — which of the 4 pillars (see `pillars.md`)?

Ask **once and concisely.** Don't loop.

## Grounding without a source

The user-provided bullets *are* the fact sheet. The skill's job:

- **Trust** the bullets — they came from the user.
- **Don't invent** anything beyond the bullets. If the user said "5 libraries:
  prophet, statsforecast, neuralforecast, sktime, gluonts", that's the list.
  Don't add a sixth.
- **Light verification** for each library/tool/concept named — a quick web
  search to confirm spelling, current status, and one accurate descriptor per
  item. If a search returns nothing usable, ask the user for a one-line
  description per bullet.

## Web verification (when needed)

For a list-shaped post that names libraries, repos, or papers:

- Use **WebFetch** on the project / library homepage to confirm:
  - Exact name + correct casing.
  - One concrete fact (latest version, last commit, license, what it does).
- If WebFetch returns nothing usable, ask the user to paste a 1-line
  description per item.
- **Never invent** stars, version numbers, release dates, or features.

## Mapping topic → template

| Topic shape | Template |
| --- | --- |
| "5 X for Y", "Top N X" (multiple items compared) | `list` |
| "I learned X the hard way", "Why I switched to X" | `lesson` |
| One bold against-the-grain claim, tight defense | `contrarian` |
| Reaction to industry news / a trend, multi-paragraph reasoning, forecast | `opinion` |
| "X vs Y", "When to use X over Y" | `comparison` |
| Single named course / tutorial / playlist / talks to share | `learning-resource` |
| New tool / paper / repo (single subject, first-person experience) | `lesson` |
| New tool / paper / repo (single subject, curation only) | `learning-resource` |

If the topic doesn't fit any of these, **ask the user** which template to use,
listing the options. Don't invent a new template silently.

## Output expectations

Same as the other source guides — the skill produces a post draft following
the chosen template's example folder + the format scaffold. The fact sheet
in this case is just the user's bullets, optionally enriched with one verified
descriptor per named item.
