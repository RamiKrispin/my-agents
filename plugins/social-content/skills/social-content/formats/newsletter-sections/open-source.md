# Format: Open Source of the Week

Heading: `## Open Source of the Week`. The longest section. Usually one project
(occasionally two — repeat the structure under the single heading).

## Research

- Run `scripts/research.py github <url>` for metadata (license, language, topics,
  description, default branch, README raw URL), then read the README via the
  `readme_raw` URL.
- Identify: what it is, the problem it solves, how it works, key features, the
  license, and whether it has a documentation site.

## Structure (match the examples)

Optional lead-in: `This week's focus is on the {{name}} project.`

```markdown
**{{Project Name}}** is an open source project from {{org}} that {{what it does}}.
{{1 paragraph: the problem it solves and how it works — often framed "Rather than
{manual approach}, {project} {does X}." Close with the goal/aim.}}

Project repo: **[{{repo url}}]({{repo url}})**

### Key Features

- **{{capability}}** — {{short explanation}}
- **{{capability}}** — {{short explanation}}
- ... (typically 6–8 bullets; each opens with a bolded concept)

More details are available in the project [documentation]({{docs url}}).

License: {{SPDX id, e.g. MIT or Apache 2.0}}
```

## Length

The anchor section: ~150–220 words plus the feature bullets.

## Rules

- Concrete capabilities over adjectives; no hype.
- Bold key terms and product names.
- Always include the **repo link** and the **license**; add the docs link if one
  exists. Drop the "More details…" line if there's no docs site.
