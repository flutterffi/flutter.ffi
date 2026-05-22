---
title: Cursor 使用教程：从安装到 Agent 与 Composer 实战
date: 2026-05-22
category: 技术
tags:
  - AI
  - Cursor
  - 教程
excerpt: 基于 VS Code 的 AI IDE：Tab 补全、Chat、Composer/Agent 多文件编辑与项目级上下文配置。
---

<img src="/photos/thumb-01.jpg" alt="配图" class="article-banner" loading="lazy" />

# Cursor 使用教程

[Cursor](https://cursor.com) 是在 VS Code 基础上深度集成 AI 的独立 IDE，适合「边写边问、多文件一起改」的日常开发。本文是本站原创入门笔记，侧重可复现的工作流。

## 适合谁

- 已习惯 VS Code 快捷键与扩展生态
- 需要**可视化 diff**、多文件 Agent 编辑
- 希望在一个窗口里完成 Chat + 改代码 + 跑终端

不太适合：只想在纯终端里跑 Agent、且不想换编辑器的人（可转向 Claude Code / Codex CLI）。

## 安装与迁移

1. 从官网下载 macOS / Windows / Linux 安装包。  
2. 首次启动可**导入 VS Code 设置与扩展**，降低迁移成本。  
3. 登录 Cursor 账号并选择订阅档（Free / Pro / Business，以官网为准）。

## 核心能力一览

| 能力 | 作用 | 典型快捷键/入口 |
|------|------|-----------------|
| **Tab 补全** | 行级/块级预测补全 | 输入时自动触发 |
| **Chat** | 单文件或选区问答 | 侧边栏 Chat |
| **Composer / Agent** | 跨文件规划与修改 | `Cmd+I` / Composer 面板 |
| **@ 上下文** | 精确引用文件、文档、Git | 输入 `@Files` `@Codebase` 等 |

## 推荐工作流

### 1. 小改：Chat + 选区

选中函数或报错栈 → Chat 里描述目标 → 应用补丁前**逐段看 diff**。

### 2. 大改：Composer + 明确约束

在 Composer 里写清：

- 要改的目录范围（如 `lib/features/auth/`）
- 必须通过的测试（`flutter test test/auth/`）
- 禁止动到的模块（如 `generated/`）

### 3. 项目规则：`.cursor/rules` 或 Rules

把团队约定写进规则文件，例如：

- 状态管理用 Riverpod，不用 setState 泥球  
- 新 API 必须带 dartdoc  
- 禁止提交 `print` 调试

规则越具体，Agent 越少「自作主张」。

## 上下文技巧

- **`@Codebase`**：适合「这段逻辑在哪被调用」类问题，注意大仓库会消耗额度。  
- **`@Docs`**：可挂官方文档 URL，减少模型胡编 API。  
- **`.cursorignore`**：排除 `build/`、`node_modules/`，提速并减少噪声。

## 常见问题

**Q：和 GitHub Copilot 能一起开吗？**  
A：通常二选一，避免两套补全打架。以 Cursor 自带模型为主即可。

**Q：Agent 改坏了怎么办？**  
A：用 Git 分支 + 小步提交；Composer 前先 `git checkout -b ai/cursor-task`。

**Q：公司代码能上传吗？**  
A：查阅 Cursor 隐私与 **Privacy Mode** 说明；涉密项目用企业策略或本地模型方案。

## 与其他工具的分工

- **Cursor**：日常编码主 IDE，可视化改多文件。  
- **Claude Code / Codex**：终端 Agent、CI Headless、重度自动化。  
- **Copilot**：在原生 VS Code 里轻量补全。

---

*版本与定价以 Cursor 官网为准。*
