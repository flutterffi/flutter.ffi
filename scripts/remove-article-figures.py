#!/usr/bin/env python3
"""Remove inline .figure.wide photo blocks; keep article-banner only."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "docs" / "posts"

FIGURE_WIDE = re.compile(
    r"\n?<div class=\"figure wide\">[\s\S]*?</div>\n?",
    re.MULTILINE,
)


def main() -> None:
    n = 0
    for md in sorted(POSTS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        new, count = FIGURE_WIDE.subn("\n", text)
        if count:
            new = re.sub(r"\n{3,}", "\n\n", new)
            md.write_text(new, encoding="utf-8")
            n += 1
            print(f"  {md.relative_to(ROOT)} ({count} block(s))")
    print(f"cleaned {n} files")


if __name__ == "__main__":
    main()
