#!/usr/bin/env python3
"""Insert local article banner into posts that lack /photos/ references."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "docs" / "posts"
THUMBS = [f"/photos/thumb-{i:02d}.jpg" for i in range(1, 17)]

BLOCK = '<img src="{thumb}" alt="配图" class="article-banner" loading="lazy" />\n\n'


def stable_index(key: str, modulo: int) -> int:
    return sum(ord(c) for c in key) % modulo


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "/photos/" in text:
        return False

    m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?", text)
    if not m:
        return False

    key = path.stem
    ti = stable_index(key, len(THUMBS))
    insert = BLOCK.format(thumb=THUMBS[ti])
    rest = text[m.end() :]
    path.write_text(text[: m.end()] + insert + rest, encoding="utf-8")
    return True


def main() -> None:
    updated = []
    for md in sorted(POSTS.rglob("*.md")):
        if process(md):
            updated.append(md.relative_to(ROOT))
    print(f"updated {len(updated)} files")
    for p in updated:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
