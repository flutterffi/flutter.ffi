---
title: Trae 使用教程：字节 AI IDE 安装与 Builder 工作流
date: 2026-05-23
category: 技术
tags:
  - AI
  - Trae
  - 教程
excerpt: 字节跳动 AI 编程 IDE Trae：安装、Builder/Chat、模型选择与和 Cursor 的差异。
---

<img src="/photos/thumb-09.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-09.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">新 IDE 的价值，在于你是否愿意为它改一条工作流。</p>
</div>

# Trae 使用教程

[Trae](https://www.trae.ai) 是字节跳动推出的 **AI-native 编程 IDE**（海外版与国内版策略可能不同），整体形态接近 Cursor / Windsurf：内置对话、多文件生成、终端集成，并强调 **Builder** 模式——用自然语言驱动从需求到可运行项目的迭代。

本文是本站原创入门笔记；功能名称与配额以 Trae 官网为准。

## 适合谁

- 希望**一站式 IDE + Agent**，不想自己拼 VS Code 扩展  
- 需要同时试用 **GPT / Claude / DeepSeek** 等模型（以 Trae 当前支持列表为准）  
- 国内网络环境下寻找 Cursor 的替代或补充

## 安装

1. 打开 Trae 官网，下载 **macOS / Windows** 安装包（注意芯片架构）。  
2. 注册并登录账号。  
3. 首次启动可选择导入 VS Code 主题/快捷键（若有该选项）。  
4. 在设置中选择默认模型与语言偏好。

## 界面与模式

| 能力 | 说明 |
|------|------|
| **Chat** | 针对当前文件或选区问答、解释、小改 |
| **Builder / Agent** | 多文件、多步骤实现功能（名称随版本可能为 Builder、Agent 等） |
| **补全** | 行级预测，写注释可提升建议质量 |
| **终端** | 内置终端跑测试、装依赖，Agent 可提议执行命令 |

## 推荐工作流

### 1. 小需求：Chat

「解释这段 Riverpod 为何 rebuild」「给这个 Widget 加 Semantics」——改前看清 diff。

### 2. 功能需求：Builder

输入结构化任务，例如：

```text
在 lib/features/todo/ 实现：
- TodoListPage（Riverpod）
- 本地 Hive 存储
- 单元测试覆盖增删改
不要修改 lib/main.dart 的路由注册方式
```

让 Builder 分步产出，**每步跑 `flutter test`** 再进入下一步。

### 3. 团队规范

在项目中维护说明文件（若 Trae 支持项目级 Rules / Instructions，将团队约定写入），包括：

- 目录与命名  
- 禁止修改 `generated/`  
- 必须跑的 CI 命令  

## 与 Cursor / Windsurf 选型

| 维度 | Trae | Cursor | Windsurf |
|------|------|--------|----------|
| 出品 | 字节 | Anysphere | Codeium |
| 国内可用性 | 通常更友好 | 视网络而定 | 视网络而定 |
| 多模型 | 支持列表以官网为准 | 多模型 | 多模型 |
| 生态 | 较新 | VS Code 迁移成熟 | Cascade 特色 |

建议用**同一仓库、同一 issue** 各试一天，比较 diff 质量与测试通过率，再定主力 IDE。

## 与终端 Agent 配合

Trae 负责日常编码；**Claude Code / Gemini CLI / Codex** 负责：

- 大批量迁移、脚本生成  
- CI 里 Headless 任务（若产品支持）  

避免两套 Agent **同时改同一分支**。

## 常见问题

**Q：Trae 和豆包 / 其他字节产品关系？**  
A：同属字节 AI 产品线，账号与计费可能打通，以官方说明为准。

**Q：公司代码能用吗？**  
A：查阅 Trae 隐私政策、是否支持私有化/企业版；涉密项目走合规审批。

**Q：已有 Cursor 还要装吗？**  
A：不必。Trae 适合作为备选或国内环境主 IDE；工具贵精不贵多。

## 延伸阅读

- [Cursor 使用教程](/posts/技术/cursor-ai-coding-tutorial)  
- [AI 编程工具教程索引](/posts/技术/ai-coding-tools-index)

---

*Trae 功能与区域可用性以官网为准。*
