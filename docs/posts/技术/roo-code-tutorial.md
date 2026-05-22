---
title: Roo Code 使用教程：VS Code Agent 模式与 Cline 生态对比
date: 2026-05-23
category: 技术
tags:
  - AI
  - Roo Code
  - VS Code
  - 教程
excerpt: Roo Code（原 Roo Cline）VS Code 扩展：Code/Architect/Debug 模式、API 配置与和 Cline 的选型。
---

<img src="/photos/thumb-10.jpg" alt="配图" class="article-banner" loading="lazy" />

# Roo Code 使用教程

[Roo Code](https://github.com/RooCodeInc/Roo-Code)（前身为 **Roo Cline**，由 Cline 生态分支发展）是 VS Code 上的 **AI 编程 Agent** 扩展。与 [Cline](/posts/技术/cline-vscode-agent-tutorial) 类似，通过自有 API Key 调用多厂商模型；差异在于 Roo Code 强调**多角色模式**（写代码 / 做架构 / 调试）与更细的自定义配置。

适合：留在 VS Code、希望**比单一 Chat 更有分工**、且愿意折腾 Provider 与模式的开发者。

## 安装

1. VS Code 扩展市场搜索 **Roo Code**（或 **Roo Cline**，以市场显示名为准）。  
2. 安装后侧边栏出现 Roo 图标，打开 **Settings**。  
3. 配置 **API Provider**（Anthropic、OpenAI、OpenRouter、Ollama 本地等）。  
4. 填入 API Key，选择默认模型。  
5. （可选）安装推荐主题/图标仅为美观，非必须。

## 模式一览

Roo Code 的核心是**按任务切换模式**（名称以当前版本 UI 为准）：

| 模式 | 典型用途 |
|------|----------|
| **Code** | 实现功能、改 bug、写测试 |
| **Architect** | 方案设计、模块划分、ADR 草稿，少直接改代码 |
| **Debug** | 根据日志/堆栈推理根因，提出最小修复 |
| **Ask** | 只问不改，适合读代码 |

实践建议：

- 新功能先 **Architect** 出步骤与文件清单 → 再 **Code** 落地  
- 线上问题用 **Debug**，避免 Agent 大范围重写  

## 基本工作流

1. 在 Roo 面板选择模式（如 Code）。  
2. 用 `@` 引用文件或文件夹（如 `@src/services/`）。  
3. 描述任务与验收标准（测试命令、边界）。  
4. 审阅 diff，在终端执行 `npm test` / `flutter test`。  
5. 失败则切换 **Debug** 模式，粘贴完整报错继续迭代。

## 自定义与 `.roo` 配置

Roo Code 支持较丰富的自定义（具体文件名见官方文档），常见包括：

- **Custom Modes**：为团队定义「只做 Review」「只写文档」等模式  
- **Rules / Instructions**：编码规范、禁止路径  
- **MCP**：挂载外部工具（文档检索、Issue 系统等）

将「必须跑哪些检查」写进规则，比每次口头提醒更可靠。

## 与 Cline 如何二选一

| 维度 | Roo Code | Cline |
|------|----------|-------|
| 来源 | Cline 分支演进 | 主流开源主线 |
| 模式 | 多角色（Code/Architect/Debug） | Plan / Act |
| 社区 | 活跃，功能迭代快 | 用户基数大 |
| 配置复杂度 | 偏高 | 相对直接 |

**团队统一选一个即可**，避免同一仓库两套 Agent 配置分叉。个人可先各试用一个下午，看哪个 diff 更贴项目风格。

## 成本与模型

- 自带 API Key：按提供商计费，适合控成本。  
- 本地 **Ollama**：适合离线试验，复杂任务需选对模型体积。  
- 国产模型：通过 OpenRouter 或兼容 `base_url` 接入（注意合规）。

## 常见问题

**Q：和 Cline 配置能迁移吗？**  
A：部分 Provider 设置类似，但规则文件格式不一定兼容，需按 Roo 文档迁移。

**Q：Roo 会自动跑终端命令吗？**  
A：会提议执行；生产环境关闭盲目 auto-approve，对删除与网络命令人工确认。

**Q：还值得学 Cline 吗？**  
A：原理相通；会 Roo 再学 Cline 很快。招聘/协作看团队标准工具即可。

## 延伸阅读

- [Cline 使用教程](/posts/技术/cline-vscode-agent-tutorial)  
- [AI 编程工具教程索引](/posts/技术/ai-coding-tools-index)  
- [CC Switch 多 Agent 配置](/posts/收藏/appark-cc-switch-download-tutorial)

---

*模式名称与配置项以 Roo Code GitHub 文档为准。*
