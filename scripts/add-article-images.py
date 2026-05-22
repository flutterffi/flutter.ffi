#!/usr/bin/env python3
"""Insert local banner + figure images into posts that lack /photos/ references."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "docs" / "posts"
THUMBS = [f"/photos/thumb-{i:02d}.jpg" for i in range(1, 17)]
PHOTOS = [f"/photos/photo-{i:02d}.jpg" for i in range(1, 17)]

CAPTIONS = [
    "街角的光，像新闻标题一样突然又平常。",
    "镜头里留住的片刻，给观点一点落地的重量。",
    "画面不必解释一切，它只是让叙述慢下来。",
    "日常场景往往比热搜更长命。",
    "一张随拍，像评论里的脚注。",
    "光影把抽象话题拽回可触摸的现实。",
    "记录本身，就是一种立场。",
    "留白处，读者可以补上自己的判断。",
]

BLOCK = """<img src="{thumb}" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="{photo}" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">{caption}</p>
</div>

"""


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
    pi = stable_index(key + "/photo", len(PHOTOS))
    ci = stable_index(key + "/cap", len(CAPTIONS))
    insert = BLOCK.format(
        thumb=THUMBS[ti],
        photo=PHOTOS[pi],
        caption=CAPTIONS[ci],
    )
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
