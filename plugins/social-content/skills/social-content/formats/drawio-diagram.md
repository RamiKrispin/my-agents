# Format: drawio diagram

Used **only on request** (`diagram: drawio`) and **only when a diagram earns
its place** in the post — typically:

- **System / architecture flow** (boxes + arrows showing data flow).
- **Decision tree** (branching choices).
- **Before / after** (two panels side by side).
- **Pipeline** (linear stages).

If the post doesn't benefit from a diagram, don't make one. A list of bullets
doesn't need a diagram.

## Workflow

1. Author a **flat node spec** as JSON (described below).
2. Run:
   ```
   python3 scripts/build_drawio.py <spec.json> <out.drawio>
   ```
3. The skill writes the JSON spec as a sidecar (`<stem>-diagram.spec.json`) and
   the resulting `.drawio` file (`<stem>.drawio`) next to the post draft.
4. The user opens the `.drawio` file in [drawio](https://app.diagrams.net) (or
   the desktop app) to fine-tune visuals before exporting.

## Spec format (flat JSON)

The spec is intentionally flat and simple — the script handles layout. The user
can post-edit in drawio for anything fancier.

```json
{
  "title": "RAG pipeline",
  "layout": "horizontal",
  "nodes": [
    {"id": "q",   "label": "User query",        "shape": "rounded"},
    {"id": "emb", "label": "Embed query",       "shape": "rect"},
    {"id": "vs",  "label": "Vector search",     "shape": "rect"},
    {"id": "rer", "label": "Rerank",            "shape": "rect"},
    {"id": "llm", "label": "LLM",               "shape": "rect"},
    {"id": "ans", "label": "Answer",            "shape": "rounded"}
  ],
  "edges": [
    {"from": "q",   "to": "emb"},
    {"from": "emb", "to": "vs"},
    {"from": "vs",  "to": "rer"},
    {"from": "rer", "to": "llm"},
    {"from": "llm", "to": "ans"}
  ]
}
```

### Field reference

| Field | Required | Values | Default |
| --- | --- | --- | --- |
| `title` | no | string | — |
| `layout` | no | `horizontal`, `vertical`, `grid` | `horizontal` |
| `nodes[].id` | yes | unique string | — |
| `nodes[].label` | yes | string (short — 1-3 words best) | — |
| `nodes[].shape` | no | `rect`, `rounded`, `ellipse`, `diamond`, `hexagon` | `rect` |
| `nodes[].group` | no | string — nodes with the same group are placed together | — |
| `edges[].from` | yes | a `nodes[].id` | — |
| `edges[].to` | yes | a `nodes[].id` | — |
| `edges[].label` | no | string | — |
| `edges[].style` | no | `solid`, `dashed` | `solid` |

The script keeps things simple: no nested groups, no swimlanes, no custom
positions. If you need those, post-edit in drawio.

## When to choose drawio over a mermaid block in the post body

- **Mermaid in post body** is fine for very simple flows (3-5 nodes, linear).
  But LinkedIn does not render mermaid — it would just be a code block.
- **drawio** is for the case where you want a real, editable diagram exported
  to PNG/SVG and uploaded to the post. It's the path that produces a shareable
  visual.

The user said: emit `.drawio` XML by default for diagrams. Mermaid is rarely
worth it on LinkedIn (rendering issues).

## Naming

- Spec sidecar (intermediate): a temp JSON file the skill creates and removes,
  or `posts/assets/<slug>.diagram.spec.json` if you want to keep it.
- Generated diagram: `posts/assets/<slug>.drawio`

The post entry references the diagram with a relative link, e.g.
`Diagram: [./assets/<slug>.drawio](./assets/<slug>.drawio)`.
