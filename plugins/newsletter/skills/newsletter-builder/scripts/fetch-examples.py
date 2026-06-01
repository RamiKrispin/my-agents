#!/usr/bin/env python3
"""Refresh the voice corpus: pull recent issues of Rami's Data Newsletter into
this skill's `style/examples/` as clean Markdown.

Usage:
    python3 scripts/fetch-examples.py [count]      # default count = 8

How it works: reads Substack's public archive API, then fetches each post's
`body_html` and converts it to Markdown with a stdlib HTML parser (zero
third-party dependencies). One-off promotional posts (very short) are skipped.

Requirements:
- Network access to ramikrispin.substack.com (allowlist it if your environment
  sandboxes outbound network).
- TLS verification is disabled to avoid macOS missing-CA issues; this only fetches
  public content.
"""

import json
import re
import ssl
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

PUB = "https://ramikrispin.substack.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
CTX = ssl._create_unverified_context()
# Skip posts shorter than this many characters of body text — they're usually
# one-off course promos / workshop announcements, not standard 3-section issues.
MIN_CHARS = 4000

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "style" / "examples"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30, context=CTX) as resp:
        return resp.read()


class Md(HTMLParser):
    BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "figure"}
    SKIP = {"script", "style", "figure", "figcaption", "svg", "button"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.buf = [], []
        self.prefix = ""
        self.skip_depth = 0
        self.list_stack = []
        self.link_start = None
        self.href = None

    def flush(self):
        text = "".join(self.buf).strip()
        self.buf = []
        if not text:
            return
        if self.prefix:
            text = "\n".join(self.prefix + ln if ln else ln for ln in text.split("\n"))
        self.blocks.append(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in ("ul", "ol"):
            self.flush()
            self.list_stack.append([tag, 0])
        elif tag == "li":
            self.flush()
            depth = max(0, len(self.list_stack) - 1)
            marker = "- "
            if self.list_stack and self.list_stack[-1][0] == "ol":
                self.list_stack[-1][1] += 1
                marker = f"{self.list_stack[-1][1]}. "
            self.prefix = "  " * depth + marker
        elif tag in self.BLOCK:
            self.flush()
            if tag[0] == "h" and tag[1:].isdigit():
                self.prefix = "#" * int(tag[1:]) + " "
            elif tag == "blockquote":
                self.prefix = "> "
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag == "code":
            self.buf.append("`")
        elif tag == "br":
            self.buf.append("\n")
        elif tag == "hr":
            self.flush()
            self.blocks.append("---")
        elif tag == "a":
            self.link_start = len(self.buf)
            self.href = a.get("href")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag in ("ul", "ol"):
            self.flush()
            if self.list_stack:
                self.list_stack.pop()
            self.prefix = ""
        elif tag in ("li",) or tag in self.BLOCK:
            self.flush()
            self.prefix = ""
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag == "code":
            self.buf.append("`")
        elif tag == "a" and self.link_start is not None:
            text = "".join(self.buf[self.link_start:]).strip()
            del self.buf[self.link_start:]
            self.buf.append(f"[{text}]({self.href})" if (self.href and text) else text)
            self.link_start, self.href = None, None

    def handle_data(self, data):
        if not self.skip_depth:
            self.buf.append(data)

    def markdown(self):
        self.flush()
        return re.sub(r"\n{3,}", "\n\n", "\n\n".join(self.blocks)).strip()


def main(count):
    archive = json.loads(get(f"{PUB}/api/v1/archive?sort=new&search=&offset=0&limit=40").decode())
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    written, skipped = 0, 0
    for p in archive:
        if written >= count:
            break
        if p.get("type") != "newsletter":
            continue
        slug, date = p["slug"], p.get("post_date", "")[:10]
        post = json.loads(get(f"{PUB}/api/v1/posts/{slug}").decode())
        md = Md()
        md.feed(post.get("body_html") or "")
        body = md.markdown()
        if len(body) < MIN_CHARS:
            skipped += 1
            print(f"  skip {date} (short / promo): {post.get('title')}")
            continue
        header = f"# {post.get('title', '').strip()}\n"
        if post.get("subtitle"):
            header += f"\n_{post['subtitle'].strip()}_\n"
        header += f"\n<!-- source: {p['canonical_url']} | {date} -->\n\n"
        (EXAMPLES_DIR / f"issue-{date}.md").write_text(header + body + "\n", encoding="utf-8")
        written += 1
        print(f"  wrote issue-{date}.md ({len(body)} chars): {post.get('title')}")
        time.sleep(1)
    print(f"\nDone: {written} issues -> {EXAMPLES_DIR} ({skipped} skipped)")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
