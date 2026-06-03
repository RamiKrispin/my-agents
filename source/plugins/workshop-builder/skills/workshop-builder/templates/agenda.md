# Workshop Agenda

> The ordered list of topics. Folder names follow `NN_topic_name` in this order.
> If you reorder, renumber the folders with no gaps.

| # | Topic | Folder | Goal | Depends on |
| -- | ----- | ------ | ---- | ---------- |
| 01 | {{Topic title}} | `01_{{name}}` | {{what they'll do/learn}} | — |
| 02 | {{Topic title}} | `02_{{name}}` | {{…}} | 01 |
| 03 | {{…}} | `03_{{name}}` | {{…}} | 01, 02 |

## Notes

- Each topic gets a `NN_topic_name/` folder for supporting code/docs. A topic
  `README.md` is only emitted when `spec/workshop-spec.md` opts in.
- Slides live under `slides/`. By default it's a single combined deck
  (`slides/workshop_slides.html`); set the spec to `per-topic` to split into
  `slides/NN_topic_name.html`.
