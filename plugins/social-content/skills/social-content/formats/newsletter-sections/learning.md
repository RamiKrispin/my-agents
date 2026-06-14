# Format: New Learning Resources

Heading: `## New Learning Resources`. Short, scannable — a list of quick pointers.

Open with this line (verbatim or very close):

> Here are some new learning resources that I came across this week.

Then one entry per resource (typically 3–6). Each entry is: a `###` title, a
short description, then the **raw link on its own line** below it.

## Research

- Determine the type: course | tutorial | talk | video | documentation | workshop.
- Identify the source/creator and the concrete topics it covers.
- **Videos (YouTube, etc.)** and other fetch-hostile pages: a plain fetch often
  fails, so run `python3 scripts/research.py render <url>` to read the title,
  channel/creator, and description before summarizing. Never guess the contents.

## Structure (match this exactly)

```markdown
### {{Resource Title}}

{{1–2 sentence summary: name the type and source/creator, then the concrete
topics or segments it covers.}}

{{url}}
```

- The link is a **bare URL on its own line** directly under the description
  (not `Link: …`, not bolded).
- Leave a blank line between the description and the URL.

## Example

```markdown
### Production RAG with LangChain & Vector Databases

This full course from freeCodeCamp walks through building, debugging, optimizing,
and scaling RAG systems for production, with hands-on segments on document
loaders, the indexing pipeline, and creating a vector database with Chroma.

https://www.youtube.com/watch?v=mHxLXzYjQRE
```

## Length & style

- 1–2 sentences per resource. **No** topic bullet lists — keep it to prose.
- Name the source/creator (e.g. "from freeCodeCamp", "by …").
- Vary the opener across items ("This full course from…", "The following talk
  by…", "This short tutorial provides a step-by-step guide for…").
- A signpost, not a review — save depth for the Open Source and Book sections.
