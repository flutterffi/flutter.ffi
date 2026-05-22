---
title: Cline 使用教程：VS Code 开源 Agent 与 API 配置
date: 2026-05-22
category: 技术
tags:
  - AI
  - Cline
  - VS Code
  - 教程
excerpt: 开源 VS Code 扩展 Cline：接 Anthropic/OpenAI/国产模型 API，Plan/Act 模式与 MCP 扩展。
---

<img src="/photos/thumb-06.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-06.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">留在熟悉的 VS Code，也能接上不同的模型后端。</p>
</div>

# Cline 使用教程

[Cline](https://github.com/cline/cline)（前身 Clawd / Claude Dev）是 VS Code 上的**开源 AI 编程 Agent** 扩展：保留你现有编辑器与插件，通过配置 **API Key** 或兼容端点调用 Claude、GPT、Gemini、DeepSeek、GLM 等模型。

适合：不想换 Cursor/Windsurf，但想要**可插拔模型**与**透明开源**的开发者。

## 安装

1. VS Code 扩展市场搜索 **Cline**，安装。  
2. 侧边栏出现 Cline 图标，打开设置（Settings）。  
3. 选择 **API Provider**（Anthropic / OpenAI / OpenRouter / 自定义 Base URL 等）。  
4. 填入 API Key 或 OAuth（视提供商而定）。  
5. 选择模型 ID（如 `claude-sonnet-4`、`gpt-4o` 等，以账户可用为准）。

## Plan 与 Act 模式

| 模式 | 行为 |
|------|------|
| **Plan** | 先出步骤与将改的文件，等你确认再动手 |
| **Act** | 直接读文件、编辑、跑终端命令 |

建议默认 **Plan**，熟悉仓库后再对简单任务用 Act。

## 典型工作流

1. 在 Cline 输入任务，附带 `@` 文件（如 `@src/main.dart`）。  
2. 审阅 Plan 里的文件列表与风险点。  
3. 批准执行，观察终端输出与 diff。  
4. 本地跑测试，失败则把日志贴回 Cline 继续迭代。  
5. 提交前自己 Review 安全相关改动（网络、鉴权、路径遍历）。

## MCP（Model Context Protocol）

Cline 支持挂载 MCP Server，例如：

- 文件系统、GitHub、数据库只读查询  
- 团队内部文档检索  

在设置里添加 MCP 配置 JSON，可让 Agent 拉取**实时上下文**，减少胡编。

## 与 Roo Code、Kilo Code 的关系

同属 VS Code Agent 生态，UI 与配置不同。若已用 Roo Code，迁移到 Cline 主要是**习惯与预设**差异，核心仍是「API + 工具调用」。

## 成本与国产模型

- 自带 Key：按各平台 API 单价计费，适合控制用量。  
- 智谱 GLM Coding Plan 等套餐声明支持 Cline / Claude Code 协议兼容，见收藏区 GLM 教程。  
- 可用 CC Switch 统一管理多端点（可选）。

## 常见问题

**Q：和 GitHub Copilot 一起装？**  
A：可以，但避免同时开两套 Agent 自动改同一文件；Copilot 做补全，Cline 做任务。

**Q：命令执行安全吗？**  
A：生产仓库关闭危险命令自动批准；对 `rm -rf`、`curl | sh` 保持警惕。

**Q：Roo Code 还要学吗？**  
A：二选一即可，原理相通；团队统一工具链更重要。

## 延伸阅读

- 收藏区：[CC Switch 配置多 Agent](/posts/收藏/appark-cc-switch-download-tutorial)

---

*扩展版本与 Provider 列表以 Cline GitHub 为准。*
