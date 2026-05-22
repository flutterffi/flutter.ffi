# Flutter FFI 技术博客

基于 [VitePress](https://vitepress.dev/) 的技术博客，双仓库 + GitHub Actions 自动部署到 GitHub Pages。

## 仓库说明

| 仓库 | 用途 |
|------|------|
| [flutterffi/flutter.ffi](https://github.com/flutterffi/flutter.ffi) | 源码：文章、配置、CI |
| [flutterffi/flutterffi.github.io](https://github.com/flutterffi/flutterffi.github.io) | 静态站点（Actions 自动推送） |

线上地址：https://flutterffi.github.io

## 快速开始

```bash
git clone https://github.com/flutterffi/flutter.ffi.git
cd flutter.ffi

npm install
npm run docs:dev
```

浏览器访问 http://localhost:5173

## 写文章

在 `docs/posts/` 下新建 Markdown，例如 `my-article.md`：

```md
---
title: 文章标题
date: 2026-05-22
tags:
  - Flutter
excerpt: 列表页显示的摘要（可选）
---

正文内容…
```

新文章若需出现在侧边栏，在 `docs/.vitepress/config.ts` 的 `sidebar` 中补充链接（或使用默认导航进入「所有文章」页）。

## 发布

```bash
git add .
git commit -m "添加新文章"
git push origin main
```

推送到 `main` 后，Actions 会执行 `npm run docs:build`，并将 `docs/.vitepress/dist` 部署到 `flutterffi.github.io` 的 `main` 分支。

## 目录结构

```
flutter.ffi/
├── docs/
│   ├── index.md              # 首页
│   ├── posts.data.ts         # 文章列表数据
│   ├── posts/                # 博客文章
│   └── .vitepress/
│       ├── config.ts         # 站点配置
│       └── theme/            # 主题扩展
├── .github/workflows/
│   └── pages.yml
└── package.json
```

## 配置

- 站点标题、导航：`docs/.vitepress/config.ts`
- 品牌色：`docs/.vitepress/theme/custom.css`

## 部署前置条件

1. 源码仓 Settings → Secrets → `PERSONAL_TOKEN`（对 `flutterffi.github.io` 有写权限）
2. `flutterffi.github.io` 仓库 Pages 源为 **main** 分支、根目录 `/`

## 许可证

MIT
