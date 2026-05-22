#!/usr/bin/env python3
"""Update daily site pulse data and the auto section in docs/mine.md."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "docs" / "posts"
DATA = ROOT / "docs" / "data"
PULSE_PATH = DATA / "site-pulse.json"
QUOTES_PATH = DATA / "daily-quotes.json"
MINE_PATH = ROOT / "docs" / "mine.md"
ACTIVITY_PATH = ROOT / "docs" / "activity" / "latest.md"

MARKER_START = "<!-- site-pulse:auto:start -->"
MARKER_END = "<!-- site-pulse:auto:end -->"


def load_posts() -> list[dict[str, str]]:
    posts: list[dict[str, str]] = []
    for md in sorted(POSTS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        title = ""
        m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", text)
        if m:
            t = re.search(r"^title:\s*(.+)$", m.group(1), re.M)
            if t:
                title = t.group(1).strip().strip('"').strip("'")
        rel = md.relative_to(ROOT / "docs").with_suffix("").as_posix()
        posts.append({"title": title or md.stem, "path": f"/{rel}"})
    return posts


def pick_spotlight(posts: list[dict[str, str]], day: int) -> dict[str, str]:
    if not posts:
        return {"title": "暂无文章", "path": "/articles"}
    idx = day % len(posts)
    return posts[idx]


def build_pulse_block(pulse: dict) -> str:
    spot = pulse["spotlight"]
    return f"""{MARKER_START}
## 站点脉动（每日自动维护）

- **最近更新（UTC）**：{pulse["last_updated_utc"]}
- **本地日期**：{pulse["last_updated_local"]}
- **文章总数**：{pulse["posts_total"]} 篇
- **维护次数**：第 {pulse["pulse_count"]} 次自动脉动

> {pulse["daily_quote"]}

**今日随机推荐**：[{spot["title"]}]({spot["path"]})  

更完整的日志见 [每日脉动记录](/activity/latest)。
{MARKER_END}"""


def write_activity_page(pulse: dict) -> None:
    ACTIVITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    spot = pulse["spotlight"]
    body = f"""---
title: 每日脉动
---

# 每日脉动

本页由 GitHub Actions 每日自动更新，用于记录博客仓库的轻量维护节奏（非人工撰写正文）。

| 字段 | 值 |
|------|-----|
| UTC 时间 | {pulse["last_updated_utc"]} |
| 本地日期 | {pulse["last_updated_local"]} |
| 文章总数 | {pulse["posts_total"]} |
| 脉动序号 | {pulse["pulse_count"]} |

## 今日一句

> {pulse["daily_quote"]}

## 今日推荐文章

[{spot["title"]}]({spot["path"]})

---

[返回「我的」](/mine)
"""
    ACTIVITY_PATH.write_text(body, encoding="utf-8")


def update_mine(pulse: dict) -> None:
    text = MINE_PATH.read_text(encoding="utf-8")
    block = build_pulse_block(pulse)
    if MARKER_START in text and MARKER_END in text:
        text = re.sub(
            rf"{re.escape(MARKER_START)}[\s\S]*?{re.escape(MARKER_END)}",
            block,
            text,
            count=1,
        )
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    MINE_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc)
    local = datetime.now()
    day = local.timetuple().tm_yday

    quotes = json.loads(QUOTES_PATH.read_text(encoding="utf-8"))
    quote = quotes[day % len(quotes)]

    posts = load_posts()
    spotlight = pick_spotlight(posts, day)

    prev: dict = {}
    if PULSE_PATH.exists():
        prev = json.loads(PULSE_PATH.read_text(encoding="utf-8"))

    pulse = {
        "pulse_count": int(prev.get("pulse_count", 0)) + 1,
        "last_updated_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_updated_local": local.strftime("%Y-%m-%d"),
        "posts_total": len(posts),
        "day_of_year": day,
        "daily_quote": quote,
        "spotlight": spotlight,
    }

    PULSE_PATH.write_text(
        json.dumps(pulse, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_activity_page(pulse)
    update_mine(pulse)
    print(json.dumps(pulse, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
