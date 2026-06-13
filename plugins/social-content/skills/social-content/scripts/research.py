#!/usr/bin/env python3
"""Research helper for the social-content skill.

Subcommands:
  render <url>    Fetch a page through a JS-rendering reader (r.jina.ai)
                  and print clean Markdown. Use for fetch-hostile pages
                  (YouTube, Coursera, Udemy, Medium, JS apps, bot-blocked
                  sites) where a plain WebFetch returns a redirect, 403,
                  or empty shell.

This mirrors the `render` subcommand in newsletter-builder's research.py
so a fact pulled by one skill is reproducible by the other.

Network call is best-effort; on failure, fall back to WebFetch or ask
the user. TLS verification is disabled (public GETs only) to avoid
macOS missing-CA errors.

Notes:
- `render` sends the target URL to the public r.jina.ai reader service,
  which fetches and renders it server-side. Fine for public pages; do
  NOT use for anything private or behind a login.
- Allowlist `r.jina.ai` if your environment sandboxes outbound network.
"""
from __future__ import annotations

import ssl
import sys
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 Chrome/120 Safari/537.36"
)
TIMEOUT = 40
CTX = ssl._create_unverified_context()


def _get(url: str, headers: dict | None = None):
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, **(headers or {})}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
        return resp.status, resp.read()


def cmd_render(url: str) -> int:
    target = url if url.startswith("http") else "https://" + url
    try:
        _, body = _get(
            f"https://r.jina.ai/{target}", {"Accept": "text/plain"}
        )
    except Exception as exc:  # noqa: BLE001 — best-effort.
        print(
            f"render failed: {exc}\n"
            "fall back to WebFetch or ask the user."
        )
        return 1
    sys.stdout.write(body.decode("utf-8", "replace"))
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    if cmd == "render" and rest:
        return cmd_render(rest[0])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
