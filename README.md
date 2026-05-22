# Flutter FFI 技术博客

基于 Hexo + Fluid 主题的个人技术博客，使用 GitHub Actions 自动部署。

## 🚀 快速开始

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/flutterffi/flutter.ffi.git
cd flutter.ffi

# 安装依赖
npm install

# 初始化主题
git submodule update --init --recursive

# 启动本地服务器
npm run server
```

访问 http://localhost:4000 查看博客。

### 创建文章

```bash
# 创建新文章
hexo new "文章标题"

# 或指定分类和标签
hexo new "Flutter FFI 深入解析" --layout post
```

文章会自动创建在 `source/_posts/` 目录。

### 部署

推送到 `main` 分支，GitHub Actions 会自动构建并部署到 GitHub Pages。

```bash
git add .
git commit -m "更新内容"
git push origin main
```

## 📁 目录结构

```
blog-source/
├── source/
│   └── _posts/          # 博客文章 (Markdown)
├── scaffolds/           # 文章模板
├── themes/              # 主题 (submodule)
├── .github/
│   └── workflows/       # GitHub Actions 配置
├── _config.yml          # Hexo 配置
└── package.json        # 项目依赖
```

## ⚙️ 配置

### 博客信息 (_config.yml)

```yaml
title: 博客标题
subtitle: 博客副标题
description: 博客描述
author: 作者名称
language: zh-CN
```

### 部署目标

部署目标仓库：`https://github.com/flutterffi/flutterffi.github.io`

## 🎨 主题

使用 [Fluid](https://github.com/fluid-dev/hexo-theme-fluid) 主题，配置文档：https://fluid-dev.github.io/hexo-fluid-docs/

## 📝 写作规范

1. 使用 Markdown 编写
2. 添加适当的 categories 和 tags
3. 图片放在 `source/images/` 目录

## 🔧 故障排除

### 主题不显示
```bash
git submodule update --init --recursive
```

### 构建后没有 public 目录
确认 `_config.yml` 中 `theme: fluid` 与 CI 中安装的 Fluid 主题一致。若主题为 `landscape` 但未安装 `hexo-theme-landscape`，`hexo generate` 会失败且不会生成 `public/`。

### 部署失败
1. 在源码仓库 `flutter.ffi` 的 Settings → Secrets 中配置 `PERSONAL_TOKEN`（需对 `flutterffi.github.io` 有写权限的 PAT）。
2. 用户站点 `flutterffi.github.io` 应使用 **main** 分支作为 Pages 源，不是 `gh-pages`。
3. 确保 `flutterffi.github.io` 仓库存在且为 Public。

## 📄 许可证

MIT
