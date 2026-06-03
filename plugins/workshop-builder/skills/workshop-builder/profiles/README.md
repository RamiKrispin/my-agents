# Profiles

A **profile** is a workshop's identity: writing **voice** + slide **style** +
**examples**, coupled together. Pick one at the spec stage (default
`design-principles`).

```
<profile>/
  voice-guide.md     the writing voice + topic notes structure
  slide-style.md     the deck theme (which tokens / branding / motifs)
  examples/          (optional) real lessons/topics that anchor the voice
  conventions.md     (optional) per-profile structure tweaks
```

Available:

- **design-principles** — principle/workflow teaching voice, distilled from a real
  Docker-for-AI course; includes example scripts. Default.
- **default** — neutral instructional voice.

> Note: workshops have **no scripts**. The example scripts in
> `design-principles/examples/` are kept as voice references — read them to
> calibrate tone and structure, then write workshop slide content (and topic
> READMEs, when emitted) in the same voice.

## Add a profile

1. Copy `default/` to `profiles/<your-label>/`.
2. Rewrite `voice-guide.md` (drop 3–5 representative lessons/topics into
   `examples/` and derive the rules from them).
3. Adjust `slide-style.md` if the look differs (new tokens or a theme variant).
4. Reference it by label in discovery / the spec.

A target repo can override the chosen profile with a `spec/style/` folder, which
takes precedence for that repo.
