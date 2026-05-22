---
title: 欢迎来到博客
date: 2026-05-21
category: 生活
tags:
  - 生活
excerpt: 这是博客的第一篇文章。
---

<img src="/photos/photo-01.jpg" alt="生活随拍" class="article-banner" />

<div class="figure svg-inline">
  <img src="/svg/book.svg" alt="阅读" width="80" />
</div>

# 欢迎 👋

这是博客的第一篇文章！

## 博客特点

- **自动化部署** — 推送到 GitHub 自动构建部署
- **Markdown 写作** — 在 `docs/posts/` 下新增 `.md` 即可
- **VitePress** — 默认主题简洁、构建稳定
- **全文搜索** — 内置本地搜索

## 本地开发

```bash
npm install
npm run docs:dev
```

浏览器打开本地开发地址（默认端口 5173）预览。

## 发布文章

```bash
# 在 docs/posts/ 新建文章，例如 my-post.md
git add .
git commit -m "添加新文章"
git push origin main
```

GitHub Actions 会将站点构建到 `flutterffi.github.io` 仓库的 `main` 分支。

## 下一步

1. 阅读 [写作指南](/guide/writing) 了解分类与发布流程
2. 在 `docs/posts/<分类>/` 下添加文章（阅读 / 生活 / 技术 / 收藏）
3. 推送到 GitHub，查看自动部署效果

祝你写作愉快！
