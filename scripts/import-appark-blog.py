#!/usr/bin/env python3
"""Import Appark cn/blog tutorials into docs/posts/收藏/."""
from __future__ import annotations

import re
import ssl
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "posts" / "收藏"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
BASE = "https://appark.ai/cn/blog"

SLUGS = [
    "address-generator-us-tax-free-turkey-appleid",
    "chatgpt-turkey-discount-subscription-guide",
    "claude-pro-discount-subscription-tutorial",
    "cc-switch-download-tutorial",
    "how-to-create-gmail-account",
    "glm-coding-plan-discount-purchase",
    "app-store-connect-submission-guide",
    "openai-codex-guide-gpt55-vs-deepseekv4",
    "gpt-image-2-advanced-prompt-and-templates",
    "claude-code-user-guide-and-installation",
    "gpt-image-2-complete-guide-and-prompt-tips",
    "app-store-change-region",
]

META = {
    "address-generator-us-tax-free-turkey-appleid": (
        "2026 免费地址生成器推荐（美区/土耳其 Apple ID）",
        "美区、免税州与土耳其地址一键生成，Apple ID 资料填写必备。",
    ),
    "chatgpt-turkey-discount-subscription-guide": (
        "2026 ChatGPT 土耳其区折扣订阅指南",
        "土耳其礼品卡低价订阅 ChatGPT Plus 的流程、风控与续费说明。",
    ),
    "claude-pro-discount-subscription-tutorial": (
        "2026 Claude Pro 折扣订阅（尼日利亚区）",
        "尼区 Apple ID、礼品卡与 Claude 注册接码的完整教程。",
    ),
    "cc-switch-download-tutorial": (
        "CC Switch 下载安装与进阶使用教程",
        "跨平台管理 Claude Code/Codex 等 AI 终端配置的开源工具指南。",
    ),
    "how-to-create-gmail-account": (
        "2026 谷歌邮箱 Gmail 注册全指南",
        "PC/移动端注册、跳过手机验证与安全设置。",
    ),
    "glm-coding-plan-discount-purchase": (
        "GLM Coding Plan 九折优惠购买指南",
        "智谱 GLM 编程套餐、优惠码与国际版订阅说明。",
    ),
    "app-store-connect-submission-guide": (
        "App Store Connect 上架教程",
        "从零发布第一款 iOS App 的证书、元数据与审核避坑。",
    ),
    "openai-codex-guide-gpt55-vs-deepseekv4": (
        "OpenAI Codex 使用教程（对比 DeepSeek V4）",
        "Codex 安装、GPT-5.5 实战与 DeepSeek V4 对比。",
    ),
    "gpt-image-2-advanced-prompt-and-templates": (
        "GPT Image 2 提示词高阶模板合集",
        "推特爆款 Prompt 模板与结构化生图技巧。",
    ),
    "claude-code-user-guide-and-installation": (
        "Claude Code 安装与最佳实践",
        "终端 AI Agent 安装、套餐选择与 VS Code 接入。",
    ),
    "gpt-image-2-complete-guide-and-prompt-tips": (
        "GPT Image 2 免费使用教程",
        "ChatGPT/API/第三方站点使用与触发判断技巧。",
    ),
    "app-store-change-region": (
        "App Store 切换地区终极指南（2026）",
        "itms-apps 一键跳转美/日/韩/土等热门区域。",
    ),
}

ATTRIBUTION = """> **转载说明**：本文由 [Appark 博客]({url}) 收录备份，版权归 Appark 及原作者所有。仅供个人学习收藏，如有侵权请联系删除。

"""


class DocParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_doc = False
        self.depth = 0
        self.parts: list[str] = []
        self._buf = ""
        self._stack: list[str] = []
        self._pre = False
        self._in_table = False
        self._row: list[str] = []
        self._rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = dict(attrs)
        cls = ad.get("class") or ""
        if tag == "div" and "vp-doc" in cls and not self.in_doc:
            self.in_doc = True
            self.depth = 1
            return
        if not self.in_doc:
            return
        if tag == "div":
            self.depth += 1
        if tag in ("h1", "h2", "h3", "h4"):
            self._flush_inline()
            level = int(tag[1])
            self._stack.append(f"{'#' * level} ")
        elif tag == "p":
            self._flush_inline()
            self._stack.append("")
        elif tag in ("ul", "ol"):
            self._flush_inline()
            self._stack.append(tag)
        elif tag == "li":
            self._flush_inline()
            parent = self._stack[-1] if self._stack else "ul"
            bullet = "1." if parent == "ol" else "-"
            self.parts.append(f"\n{bullet} ")
        elif tag == "strong":
            self._buf += "**"
        elif tag == "code" and not self._pre:
            self._buf += "`"
        elif tag == "pre":
            self._flush_inline()
            self._pre = True
            self.parts.append("\n\n```\n")
        elif tag == "a":
            href = ad.get("href") or ""
            self._buf += "["
            self._link_href = href
        elif tag == "img":
            src = ad.get("src") or ""
            alt = ad.get("alt") or "配图"
            self.parts.append(f"\n\n![{alt}]({src})\n\n")
        elif tag == "table":
            self._in_table = True
            self._rows = []
        elif tag == "tr" and self._in_table:
            self._row = []
        elif tag in ("th", "td") and self._in_table:
            self._flush_inline()
            self._stack.append("cell")

    def handle_endtag(self, tag: str) -> None:
        if not self.in_doc:
            return
        if tag == "div":
            self.depth -= 1
            if self.depth <= 0:
                self.in_doc = False
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self._flush_inline()
            if self._stack:
                self._stack.pop()
            self.parts.append("\n\n")
        elif tag == "p":
            self._flush_inline()
            self.parts.append("\n\n")
        elif tag in ("ul", "ol"):
            if self._stack and self._stack[-1] in ("ul", "ol"):
                self._stack.pop()
            self.parts.append("\n")
        elif tag == "strong":
            self._buf += "**"
        elif tag == "code" and not self._pre:
            self._buf += "`"
        elif tag == "pre":
            self.parts.append("\n```\n\n")
            self._pre = False
        elif tag == "a":
            href = getattr(self, "_link_href", "")
            self._buf += f"]({href})"
        elif tag in ("th", "td") and self._in_table:
            self._row.append(self._buf.strip())
            self._buf = ""
            if self._stack and self._stack[-1] == "cell":
                self._stack.pop()
        elif tag == "tr" and self._in_table:
            if self._row:
                self._rows.append(self._row)
        elif tag == "table" and self._in_table:
            self._emit_table()
            self._in_table = False

    def handle_data(self, data: str) -> None:
        if not self.in_doc or self._in_table:
            if self._in_table:
                self._buf += data
            return
        if self._pre:
            self.parts.append(data)
        else:
            self._buf += data

    def _flush_inline(self) -> None:
        if self._buf:
            self.parts.append(self._buf)
            self._buf = ""

    def _emit_table(self) -> None:
        if not self._rows:
            return
        lines = []
        header = self._rows[0]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for row in self._rows[1:]:
            while len(row) < len(header):
                row.append("")
            lines.append("| " + " | ".join(row[: len(header)]) + " |")
        self.parts.append("\n\n" + "\n".join(lines) + "\n\n")


def fetch_html(slug: str) -> str:
    url = f"{BASE}/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def html_to_markdown(html: str) -> tuple[str, str]:
    parser = DocParser()
    parser.feed(html)
    body = "".join(parser.parts)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"​", "", body)
    body = re.sub(r"\s+Permalink to.*?\n", "\n", body)
    m = re.search(r"<title>([^<]+)</title>", html, re.I)
    title = m.group(1).strip() if m else ""
    title = re.sub(r"\s*\|.*$", "", title)
    if not title:
        hm = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
        if hm:
            title = re.sub(r"<.*?>", "", hm.group(1))
            title = re.sub(r"​", "", title).strip()
    return title, body.strip()


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def write_post(slug: str, title: str, excerpt: str, body: str) -> None:
    url = f"{BASE}/{slug}"
    fname = f"appark-{slug}.md"
    front = f"""---
title: {yaml_quote(title)}
date: 2026-05-22
category: 收藏
tags:
  - Appark
  - 教程
  - 转载
source: {url}
excerpt: {yaml_quote(excerpt)}
---

{ATTRIBUTION.format(url=url)}

"""
    (OUT / fname).write_text(front + body + "\n", encoding="utf-8")


def write_index() -> None:
    lines = [
        "---",
        'title: "Appark 教程收藏索引"',
        "date: 2026-05-22",
        "category: 收藏",
        "tags:",
        "  - Appark",
        "  - 索引",
        'excerpt: "从 Appark 博客收录的应用增长、ASO 与工具教程目录。"',
        "---",
        "",
        ATTRIBUTION.format(url="https://appark.ai/cn/blog/"),
        "",
        "# Appark 教程收藏",
        "",
        "以下文章整理自 [Appark 博客](https://appark.ai/cn/blog/)，便于离线阅读与检索。",
        "",
    ]
    for slug in SLUGS:
        title, excerpt = META[slug]
        lines.append(f"- [{title}](/posts/收藏/appark-{slug}) — {excerpt}")
    lines.append("")
    (OUT / "appark-tutorial-index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for slug in SLUGS:
        print(f"fetch {slug}...")
        html = fetch_html(slug)
        scraped_title, body = html_to_markdown(html)
        title, excerpt = META[slug]
        if scraped_title and len(scraped_title) < 120:
            title = scraped_title.split("|")[0].strip() or title
        write_post(slug, title, excerpt, body)
        print(f"  -> appark-{slug}.md ({len(body)} chars)")
    write_index()
    print("done:", len(SLUGS), "posts + index")


if __name__ == "__main__":
    main()
