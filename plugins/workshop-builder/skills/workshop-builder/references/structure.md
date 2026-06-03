# Output structure

The workshop-builder writes into the **target repo** (where the workshop lives),
never into the marketplace. `spec/` holds the development docs; the rest is
attendee-facing.

## Layout (default — single combined deck, no per-topic READMEs)

```
spec/                              development docs (source of truth)
  workshop-spec.md
  agenda.md
  continuity.md
  open-items.md
  style/                           OPTIONAL per-repo profile override

NN_topic_name/                     numbered by agenda order: 01_intro, 02_setup, …
  <supporting code / docs>         in the topic folder
                                   (no README.md unless the spec opts in)

slides/
  workshop_slides.html             ONE deck for the whole workshop (a section per topic)
```

## Variants

**Per-topic decks (opt-in).** When the spec's slide-split preference is
"per-topic", each topic gets its own deck file under the same `slides/` folder:

```
slides/
  01_topic_name.html
  02_topic_name.html
  …
```

The combined `slides/workshop_slides.html` is **not** produced in this variant.

**Topic READMEs (opt-in).** When the spec opts in, each topic folder gets:

```
NN_topic_name/
  README.md                        topic notes + steps (H1: # NN — Topic Title)
  <supporting code / docs>
```

Otherwise topic folders contain only the supporting code/assets.

## Hard rules

- Always create `slides/` if it doesn't exist; never put deck files inside topic
  folders.
- **No** `script/` tree. Workshops have no scripts.
- Topic folders are `NN_topic_name` with two-digit zero-padded numbering and
  no gaps. Renumber if the agenda reorders.
