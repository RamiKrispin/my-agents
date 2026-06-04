Drop real posts here. One file per post. Each file is just the post text — no
frontmatter, no commentary. See `../README.md` for the full convention.

This folder defines the **opinion** template — first-person commentary on
industry trends, news, or technical decisions. The post stakes a personal
POV up front and backs it with reasoning, often with numbers or a chain of
implications. Maps to the **Industry trends and commentary** posting strategy
in `../../best-practices.md`.

## Shape (derived from the 3 seeded examples)

Opinion posts vary widely in length but share a consistent voice and arc:

### 1. Hook (line 1) — three flavors observed

- **Bias-up-front, claim** — `Yes, I am super biased, but in my personal
  opinion, {claim} 👇🏼` (the long-argument hook).
- **Cross-link to your own content** — `From my weekly newsletter:
  {topic} 🚀👇🏼` (when the post recycles or extends an argument from your
  newsletter / a past post).
- **Reference to a past post** — `I shared a post a few days ago about
  {topic}. {what's new now}.` (when the post is a quick reaction with new
  evidence — e.g. a video that supports your earlier argument).

`👇🏼` is the recurring "argument follows" signal. `🚀` shows up when the post
is rooted in a specific named project / piece of content.

### 2. Body — multi-paragraph reasoning

The body is the distinguishing feature of this template:

- **Stakes the POV early** with first-person framing — "in my opinion", "in
  my biased opinion", "I expect to see…". Don't bury the take.
- **Backs the take with concrete reasoning** — math (the $20k/employee /
  $5-9k machine arbitrage), specific products (M5 with 128GB, Mac Studio with
  512GB), specific projects (exo, llama.cpp, quantization), specific events
  (macOS Tahoe RDMA, Uber's AI spending statement). Numbers and names are the
  fuel; vague claims are not.
- **Length is flexible — 70 to 450 words.**
  - Short variant (~70 words): one paragraph, one forecast, one link. Use
    when reacting to fresh news / a video that extends a past argument.
  - Medium variant (~200-250 words): one project / event explored across
    2-3 paragraphs. Hook → context → why it matters → repo / link.
  - Long variant (~400-450 words): full argument with math, a 2-3 bullet
    list of supporting changes, and a closing forecast / inevitability
    statement.

### 3. Honesty about bias

- "Yes, I am super biased…", "in my biased opinion".
- This is a feature, not a hedge. It signals you're sharing a take, not
  reporting consensus, and earns the right to a strong claim.

### 4. Reference to outside content (almost always)

- A linked past post, an external video, a news article, an open-source repo,
  or a newsletter cross-link. The opinion post anchors itself to something
  the reader can verify or follow up on.
- Inline links are fine in this template — bolded link patterns from the
  `learning-resource` template are NOT used here. Plain `https://lnkd.in/...`
  works.

### 5. Ending — a forecast, implication, or inevitability statement

- "we are going to move to a new equilibrium…"
- "I expect to see, as the cost of token usage rises, more companies pivot
  to local models…"
- "In the long term, open-source models will take over proprietary ones.
  This is inevitable."
- This forward-looking close is what makes the post commentary, not
  reporting. It puts your forecast on the line.

### 6. Hashtags — flexible

- 0 to 4. Lowercase, end of post.
- Short reaction posts may have **none** (the Mac Mini video post has zero
  hashtags). Long arguments tend to have 1-4.

## What this template is NOT

- **Not `contrarian`.** A contrarian post is structurally tight: one bold
  against-the-grain claim + 2-3 paragraphs defending it + a 1-line takeaway.
  An opinion post is broader — it can be long-form reasoning, doesn't have
  to be against the grain, and the body shape is fluid.
- **Not `learning-resource`.** Learning-resource posts use the
  `🚀 + ✅-bullet topic list + 📽️: link` shape. Opinion posts don't use
  ✅ topic bullets. They use prose paragraphs, sometimes with a 2-3 item
  bulleted aside.
- **Not `lesson`.** A lesson post is rooted in a specific personal
  experience ("I rebuilt this Docker environment 30 times…"). An opinion
  post forecasts or argues — it may reference experience, but the focus is
  the take on the trend, not the story of doing the work.

## When to recommend this template

- The user wants to **react to industry news** (a CTO statement, a hardware
  release, a model launch, a regulation).
- The user wants to **forecast** where a trend is heading.
- The user wants to **defend a take** with reasoning + numbers, not a
  personal-experience arc.
- The user is **extending an argument from a past post / newsletter** (the
  cross-link variant).

Maps to the **Industry trends and commentary** posting strategy in
`best-practices.md` (one of the four core strategies). Counts toward the
70% **Teach** bucket of 70/20/10 — these posts are authority-building.

## Anti-patterns specific to this template

- **Don't open with "Hot take:"** or other clichés. Use a real first-person
  stance: "in my opinion", "in my biased opinion", or a fact + your reaction.
- **Don't make the forecast vague.** "AI is changing everything" is not a
  forecast. "Companies will have to choose between spending $20k/year on
  tokens and a $5-9k Mac" is.
- **Don't pretend it's neutral reporting.** This template is explicitly
  opinion. Owning the bias is what makes it work.
- **Don't add ✅ bullets** to fake learning-resource shape. If the post
  is genuinely a curated list of resources, use `learning-resource` instead.
- **Don't bury the lede in 4 paragraphs of background** before stating your
  take. The take goes in line 1 or paragraph 1.
