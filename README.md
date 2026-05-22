# 阅读与生活

基于 [VitePress](https://vitepress.dev/) 的个人博客：阅读和生活分享。双仓库 + GitHub Actions 自动部署。

- 线上站点：https://flutterffi.github.io
- 站点内写作指南：https://flutterffi.github.io/guide/writing

## 仓库说明

| 仓库 | 用途 |
|------|------|
| [flutterffi/flutter.ffi](https://github.com/flutterffi/flutter.ffi) | 源码：文章、配置、CI |
| [flutterffi/flutterffi.github.io](https://github.com/flutterffi/flutterffi.github.io) | 静态站点（Actions 自动推送） |

## 快速开始

```bash
git clone https://github.com/flutterffi/flutter.ffi.git
cd flutter.ffi

npm install
npm run docs:dev
```

浏览器访问 http://localhost:5173

## 文章分类

| 分类 | 目录 |
|------|------|
| 阅读 | `docs/posts/阅读/` |
| 生活 | `docs/posts/生活/` |
| 技术 | `docs/posts/技术/` |
| 收藏 | `docs/posts/收藏/` |

左侧**侧边栏**按上述四类展示文章；**归档页**（`/archive`）按分类分组列出全部文章。

## 写文章

在 `docs/posts/<分类>/` 下新建 Markdown，例如 `docs/posts/阅读/my-note.md`：

```md
---
title: 文章标题
date: 2026-05-22
category: 阅读
tags:
  - 随笔
excerpt: 归档页显示的摘要（可选）
---

正文内容…
```

- `category` 与文件夹名一致时，侧边栏与归档**自动更新**，无需改配置
- 文件名建议用英文/拼音 slug，避免空格和 `..`
- 详细说明见 [docs/guide/writing.md](docs/guide/writing.md)（同步发布到站点 `/guide/writing`）

## 发布

```bash
git add .
git commit -m "添加新文章"
git push origin main
```

Actions 构建 `docs/.vitepress/dist` 并推送到 `flutterffi.github.io` 的 `main` 分支。

## 每日自动脉动（仓库活跃度）

工作流 [`.github/workflows/daily-activity.yml`](.github/workflows/daily-activity.yml) 每天 UTC 01:15 运行（也可在 Actions 页手动 **Run workflow**）：

1. 执行 `scripts/update-site-pulse.py`
2. 更新 `docs/data/site-pulse.json`、`docs/activity/latest.md`、`docs/mine.md` 中的自动区块
3. 提交并 push 到 `main`，随后触发 `pages.yml` 重新部署站点

每日变化包括：一句轮换文案、随机推荐一篇文章、文章总数与维护序号。

**若希望 commit 计入你的 GitHub 个人贡献图**（而不是 `github-actions[bot]`），在仓库 **Settings → Secrets and variables → Actions → Variables** 添加：

| 变量名 | 示例 |
|--------|------|
| `ACTIVITY_COMMIT_NAME` | `flutterffi` |
| `ACTIVITY_COMMIT_EMAIL` | `12345678+flutterffi@users.noreply.github.com`（见 GitHub 邮箱设置里的 noreply 地址） |

本地试跑：

```bash
python3 scripts/update-site-pulse.py
```

## 目录结构

```
flutter.ffi/
├── docs/
│   ├── index.md                 # 首页
│   ├── archive.md               # 归档（按分类）
│   ├── categories.ts            # 分类常量
│   ├── posts.data.ts            # 文章列表加载
│   ├── guide/writing.md         # 写作指南（站内文档）
│   ├── posts/
│   │   ├── 阅读/
│   │   ├── 生活/
│   │   ├── 技术/
│   │   └── 收藏/
│   └── .vitepress/
│       ├── config.mjs           # 站点配置
│       ├── utils/sidebar.mjs    # 侧边栏生成
│       └── theme/
├── .github/workflows/pages.yml
├── .github/workflows/daily-activity.yml
├── scripts/update-site-pulse.py
├── docs/data/site-pulse.json
└── package.json
```

## 配置

| 内容 | 文件 |
|------|------|
| 标题、导航、侧边栏 | `docs/.vitepress/config.mjs` |
| 首页文案 | `docs/index.md` |
| 增删分类 | `docs/categories.ts`、`docs/.vitepress/utils/sidebar.mjs` |

## 部署前置条件

1. 源码仓 Settings → Secrets → `PERSONAL_TOKEN`（对 `flutterffi.github.io` 有写权限）
2. Pages 仓库源为 **main** 分支、根目录 `/`

## 常用命令

```bash
npm run docs:dev      # 本地预览
npm run docs:build    # 构建到 docs/.vitepress/dist
npm run docs:preview  # 预览构建结果
```

不要使用 `npx vitepress --version`（会误启动 dev 服务器）。

## 许可证

MIT
