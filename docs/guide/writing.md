---
title: 写作指南
---

# 写作指南

本站基于 [VitePress](https://vitepress.dev/) 构建，采用**双仓库**部署：源码在 `flutter.ffi`，静态站点发布到 `flutterffi.github.io`。

## 文章分类

博客文章分为四个大分类，会显示在**左侧侧边栏**和**归档页**：

| 分类 | 目录 | 说明 |
|------|------|------|
| 阅读 | `docs/posts/阅读/` | 读书笔记、译文、长文阅读感受 |
| 生活 | `docs/posts/生活/` | 日常、旅行、随笔 |
| 技术 | `docs/posts/技术/` | 技术笔记、开发记录 |
| 收藏 | `docs/posts/收藏/` | 摘录、链接合集、值得收藏的内容 |

某分类下还没有文章时，侧边栏仍会显示该分类名称，但下面没有链接。

## 新建一篇文章

### 1. 选择分类目录

在对应分类文件夹下创建 `.md` 文件，文件名建议用英文或拼音（避免空格和特殊符号），例如：

```
docs/posts/阅读/my-book-notes.md
docs/posts/生活/weekend-walk.md
```

### 2. 填写 frontmatter

每篇文章开头需要 YAML 元数据：

```md
---
title: 文章标题（显示在页面和列表里）
date: 2026-05-22
category: 阅读
tags:
  - 标签一
  - 标签二
excerpt: 在归档页显示的简短摘要（可选）
---

# 正文一级标题

正文用 Markdown 编写……
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 文章标题 |
| `date` | 是 | 发布日期，格式 `YYYY-MM-DD` |
| `category` | 建议 | 填 `阅读` / `生活` / `技术` / `收藏` 之一，与文件夹一致 |
| `tags` | 否 | 标签列表 |
| `excerpt` | 否 | 归档列表中的摘要；不写则用正文前一段 |

**注意：** `category` 应与文件所在目录一致（如放在 `posts/生活/` 则写 `category: 生活`）。一致时**无需改任何配置文件**，侧边栏和归档会自动出现新文章。

### 3. 本地预览

```bash
npm install
npm run docs:dev
```

浏览器打开终端提示的地址（一般为 http://localhost:5173），修改 Markdown 后会热更新。

### 4. 发布上线

```bash
git add .
git commit -m "添加文章：xxx"
git push origin main
```

推送到 `main` 后，GitHub Actions 会自动构建并部署到 https://flutterffi.github.io 。

## 站点结构说明

```
docs/
├── index.md                 # 首页（Hero、简介）
├── archive.md               # 归档页（按分类列出全部文章）
├── categories.ts            # 四个分类常量
├── posts.data.ts            # 构建时加载文章列表
├── guide/
│   └── writing.md           # 本页：写作指南
├── posts/
│   ├── 阅读/
│   ├── 生活/
│   ├── 技术/
│   └── 收藏/
└── .vitepress/
    ├── config.mjs           # 站点标题、导航、侧边栏
    ├── utils/sidebar.mjs    # 扫描 posts 生成侧边栏
    └── theme/               # 主题扩展
```

## 侧边栏如何生成

构建时脚本会扫描 `docs/posts/` 下所有 `.md` 文件，按 `category`（或所在文件夹名）归入四个分类，并生成侧边栏链接。

- 修改文章、新增文章：**只要 push 源码**，侧边栏会自动更新
- **不要**在 `config.mjs` 里手工维护每篇文章的链接

## 修改站点信息

| 内容 | 文件 |
|------|------|
| 站点标题、导航菜单 | `docs/.vitepress/config.mjs` |
| 首页主标题、副标题 | `docs/index.md` 的 `hero` 区域 |
| 分类列表（增删分类名） | `docs/categories.ts` 与 `docs/.vitepress/utils/sidebar.mjs` 中的 `CATEGORIES` |

增删分类需同时改上述两处，并保持 `posts/` 下文件夹名称一致。

## 部署说明

| 仓库 | 用途 |
|------|------|
| [flutterffi/flutter.ffi](https://github.com/flutterffi/flutter.ffi) | 源码与 CI |
| [flutterffi/flutterffi.github.io](https://github.com/flutterffi/flutterffi.github.io) | 仅存放构建后的静态 HTML |

前置条件：

1. 源码仓 Settings → Secrets 配置 `PERSONAL_TOKEN`（对 `flutterffi.github.io` 有写权限）
2. Pages 仓库的 GitHub Pages 源为 **main** 分支、目录 `/`

## 常见问题

### 写了两篇文章，归档只显示一篇？

归档页从 `docs/posts/` **自动扫描**全部文章。若只显示一篇，请检查：

- 另一篇是否在 `docs/posts/<分类>/` 目录下
- 是否有正确的 `title`、`date` frontmatter
- 文件名是否含空格或 `..` 等特殊字符（建议改为 `my-post.md` 这类 slug）

### `npx vitepress --version` 卡住？

VitePress 没有 `--version` 子命令，该写法会**启动开发服务器**。请使用：

```bash
npm run docs:dev    # 本地预览
npm run docs:build  # 构建
```

### 构建报错 dead link？

文章里不要写 `http://localhost:5173` 这类仅本地有效的链接；或在 `config.mjs` 中已设置 `ignoreDeadLinks: true`。

---

更多问题可查看项目根目录 [README](https://github.com/flutterffi/flutter.ffi/blob/main/README.md)。
