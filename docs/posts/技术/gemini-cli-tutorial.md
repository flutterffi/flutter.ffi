---
title: Gemini CLI 使用教程：Google 终端 Agent 安装与项目实践
date: 2026-05-23
category: 技术
tags:
  - AI
  - Gemini CLI
  - Google
  - 教程
excerpt: Google 官方终端编程 Agent：安装、GEMINI.md 项目说明、工具调用与和 Claude Code 的分工。
---

<img src="/photos/thumb-08.jpg" alt="配图" class="article-banner" loading="lazy" />

# Gemini CLI 使用教程

**Gemini CLI** 是 Google 面向开发者的**终端 AI Agent**（与 Gemini 网页/APP 同源模型族），可在项目目录中读文件、执行命令、做多步推理。CC Switch 等工具已将其与 Claude Code、Codex 并列管理，说明它已是主流 Agent 之一。

> 包名与命令以 [Google Gemini CLI 文档](https://github.com/google-gemini/gemini-cli) 为准，下文为通用工作流说明。

## 适合谁

- 已使用 Google AI / Gemini API 或 Google 账号体系  
- 希望终端 Agent **与 Google 搜索、文档工具有联动**（以官方能力为准）  
- 想在同一台机器上并存 Claude Code / Codex，按任务换工具

## 安装

**方式一：npm（常见）**

```bash
npm install -g @google/gemini-cli
gemini --version
```

**方式二：官方脚本 / 其他渠道**  
见 GitHub Releases 与文档中的安装章节（macOS / Linux / Windows）。

首次进入项目目录：

```bash
cd your-repo
gemini
```

按提示登录 Google 账号或配置 `GEMINI_API_KEY`（视当前政策而定）。

## 项目说明：`GEMINI.md`

在仓库根目录创建 `GEMINI.md`（或文档规定的文件名），例如：

```markdown
# 项目约定
- Monorepo：apps/mobile 为 Flutter 主工程
- 测试：改动 lib/ 后运行 flutter test
- 禁止修改：*.g.dart、ios/Pods
- 提交信息使用英文，遵循 Conventional Commits
```

与 Claude Code 的 `CLAUDE.md` 同理：**规则写进文件，比每次 Chat 重复更稳**。

## 核心用法

| 场景 | 示例提示 |
|------|----------|
| 功能开发 | 「为 settings 页增加深色模式开关并补 widget 测试」 |
| 排错 | 「根据这段 flutter analyze 输出定位根因并修复」 |
| 重构 | 「将 data 层从 Provider 迁到 Riverpod，分步进行」 |
| 文档 | 「根据 lib/api/ 生成 README 中的 API 小节」 |

执行前 Agent 可能请求**运行 shell / 写文件**权限，生产仓库建议：

- 先 `git checkout -b gemini/task-name`  
- 对 `rm`、`curl | sh`、改 `.env` 保持人工确认  

## 与 CC Switch 配合

若使用 [CC Switch](/posts/收藏/appark-cc-switch-download-tutorial)：

1. 在 Gemini CLI 标签页添加 Provider（官方或兼容端点）。  
2. 启用本地代理路由（若文档要求）。  
3. 托盘热切换模型，适合「白天 Gemini、晚上 Claude」这类分工。

## 与 Claude Code / Codex 对比

| 维度 | Gemini CLI | Claude Code | Codex |
|------|------------|-------------|-------|
| 厂商 | Google | Anthropic | OpenAI |
| 终端体验 | 是 | 是 | 是（+ IDE 插件） |
| 项目记忆文件 | GEMINI.md | CLAUDE.md | 项目/IDE 配置 |
| 典型优势 | Google 生态整合 | 长上下文工程任务 | ChatGPT 订阅联动 |

不必只留一个；**按任务选工具**，统一用 Git 分支隔离改动。

## 常见问题

**Q：免费额度够用吗？**  
A：以 Google 当前 Gemini / AI Studio 政策为准；高频使用建议盯配额与计费面板。

**Q：能读整个大仓库吗？**  
A：大 monorepo 应用 `.gitignore` / 忽略规则缩小索引；任务描述里写清目录边界。

**Q：和 Gemini Code Assist（IDE 插件）区别？**  
A：CLI 偏**自动化与脚本化**；IDE 插件偏**边写边问**。可组合使用。

## 延伸阅读

- [AI 编程工具教程索引](/posts/技术/ai-coding-tools-index)  
- [Claude Code 使用教程](/posts/技术/claude-code-tutorial)

---

*命令与订阅政策以 Google 官方文档为准。*
