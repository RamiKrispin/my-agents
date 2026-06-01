#!/usr/bin/env python3
"""Research + validation helper for the newsletter-builder skill.

Subcommands:
  render <url>             Fetch a page through a JS-rendering reader (r.jina.ai)
                           and print clean Markdown. Use for fetch-hostile pages
                           (JavaScript apps / bot-protected sites) where a plain
                           fetch returns a redirect, 403, or empty shell.
  book <url-or-isbn>       Print clean book metadata. Extracts the ISBN, queries
                           Google Books, and falls back to `render` if needed.
  github <repo-url>        Print GitHub repo metadata as JSON.
  check  <url> [url ...]   Print HTTP status for each URL.
  validate <draft.md>      Offline structural check of a newsletter draft.

Network subcommands are best-effort; on failure, fall back to another subcommand
or ask the user. `validate` is fully offline (exit code 0 = PASS, 1 = FAIL).

Notes:
- `render` sends the target URL to the public r.jina.ai reader service, which
  fetches and renders it. Fine for public pages; don't use it for anything
  private. Allowlist `r.jina.ai` if your environment sandboxes outbound network.
- TLS verification is disabled (public GETs only) to avoid macOS missing-CA errors.
"""

from __future__ import annotations

import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
TIMEOUT = 40
CTX = ssl._create_unverified_context()

# Section headings expected in the final newsletter, in their required order.
REQUIRED_SECTIONS = [
    "Open Source of the Week",
    "New Learning Resources",
    "Book of the Week",
]


def _get(url: str, headers: dict | None = None):
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, **(headers or {})}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
        return resp.status, resp.read()


def _extract_isbn(text: str) -> str | None:
    digits = re.sub(r"[-\s]", "", text)
    m = re.search(r"97[89]\d{10}", digits) or re.search(r"\b\d{9}[\dXx]\b", digits)
    return m.group(0) if m else None


def cmd_render(url: str) -> int:
    target = url if url.startswith("http") else "https://" + url
    try:
        _, body = _get(f"https://r.jina.ai/{target}", {"Accept": "text/plain"})
    except Exception as exc:  # noqa: BLE001 — best-effort.
        print(f"render failed: {exc}\nfall back to WebFetch or ask the user.")
        return 1
    sys.stdout.write(body.decode("utf-8", "replace"))
    return 0


def cmd_book(arg: str) -> int:
    isbn = _extract_isbn(arg)
    if isbn:
        for attempt in range(3):
            try:
                _, body = _get(
                    f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
                )
                items = json.loads(body).get("items") or []
                if items:
                    v = items[0].get("volumeInfo", {})
                    print(json.dumps({
                        "source": "google_books",
                        "isbn": isbn,
                        "title": v.get("title"),
                        "subtitle": v.get("subtitle"),
                        "authors": v.get("authors"),
                        "publisher": v.get("publisher"),
                        "publishedDate": v.get("publishedDate"),
                        "pageCount": v.get("pageCount"),
                        "categories": v.get("categories"),
                        "description": v.get("description"),
                    }, indent=2))
                    return 0
                break  # 200 but no items — go to render fallback.
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                break
            except Exception:  # noqa: BLE001
                break
    # Fallback: render the page (works for O'Reilly, publisher, Amazon, etc.).
    print(f"# google books unavailable (isbn={isbn}); rendering the page instead\n")
    return cmd_render(arg)


def cmd_github(url: str) -> int:
    match = re.search(r"github\.com/([^/]+)/([^/#?]+)", url)
    if not match:
        print(json.dumps({"error": f"not a github repo url: {url}"}))
        return 1
    owner, repo = match.group(1), match.group(2).removesuffix(".git")
    try:
        _, body = _get(
            f"https://api.github.com/repos/{owner}/{repo}",
            {"Accept": "application/vnd.github+json"},
        )
        data = json.loads(body)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({
            "error": str(exc),
            "repo": f"{owner}/{repo}",
            "hint": "fall back to WebFetch on the README raw url",
        }))
        return 1
    branch = data.get("default_branch", "main")
    print(json.dumps({
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "html_url": data.get("html_url"),
        "homepage": data.get("homepage"),
        "stars": data.get("stargazers_count"),
        "language": data.get("language"),
        "license": (data.get("license") or {}).get("spdx_id"),
        "topics": data.get("topics", []),
        "pushed_at": data.get("pushed_at"),
        "default_branch": branch,
        "readme_raw": f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md",
    }, indent=2))
    return 0


def cmd_check(urls: list[str]) -> int:
    results = []
    for url in urls:
        try:
            status, _ = _get(url)
            results.append({"url": url, "status": status, "ok": 200 <= status < 400})
        except urllib.error.HTTPError as exc:
            results.append({"url": url, "status": exc.code, "ok": False})
        except Exception as exc:  # noqa: BLE001
            results.append({"url": url, "status": None, "ok": False, "error": str(exc)})
    print(json.dumps(results, indent=2))
    return 0 if all(r["ok"] for r in results) else 1


def cmd_validate(path: str) -> int:
    headings = re.findall(
        r"^#{1,3}\s+(.*)$",
        Path(path).read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    problems: list[str] = []
    found: list[int] = []
    for name in REQUIRED_SECTIONS:
        idx = next((i for i, h in enumerate(headings) if name.lower() in h.lower()), None)
        if idx is None:
            problems.append(f"missing section: {name}")
        else:
            found.append(idx)
    if found != sorted(found):
        problems.append("sections out of order; expected: " + " -> ".join(REQUIRED_SECTIONS))

    if problems:
        print("FAIL:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("PASS: all three sections present and in order")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    if cmd == "render" and rest:
        return cmd_render(rest[0])
    if cmd == "book" and rest:
        return cmd_book(rest[0])
    if cmd == "github" and rest:
        return cmd_github(rest[0])
    if cmd == "check" and rest:
        return cmd_check(rest)
    if cmd == "validate" and rest:
        return cmd_validate(rest[0])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
