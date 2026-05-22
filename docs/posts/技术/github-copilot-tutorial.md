---
title: GitHub Copilot 使用教程：补全、Chat 与 Agent 模式入门
date: 2026-05-22
category: 技术
tags:
  - AI
  - GitHub Copilot
  - 教程
excerpt: 从 Copilot 补全到 Copilot Chat、Copilot CLI/Agent：在 VS Code 与 GitHub 工作流中的定位。
---

<img src="/photos/thumb-03.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-03.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">轻量补全往往最适合高频、小步的编码节奏。</p>
</div>

# GitHub Copilot 使用教程

[GitHub Copilot](https://github.com/features/copilot) 是最早大规模普及的 AI 编程助手之一，深度绑定 GitHub 生态。优势是**低摩擦补全**与团队企业管控，而非替代完整 IDE Agent。

## 订阅与开通

- 个人：Copilot Individual（GitHub 账户订阅）  
- 团队：Copilot Business / Enterprise（组织管理员开通）  
- 学生/开源维护者：可查官方免费资格政策

开通后在 GitHub 设置中确认 Copilot 已启用。

## 安装（VS Code 示例）

1. 扩展市场搜索 **GitHub Copilot** 与 **GitHub Copilot Chat**，安装并登录。  
2. 状态栏出现 Copilot 图标即表示补全已就绪。  
3. JetBrains、Neovim、Visual Studio 等亦有官方插件。

## 三层能力

### 1. Inline 补全（最常用）

输入注释或函数签名，等待灰色建议 → `Tab` 接受，逐段采纳。

技巧：

- 函数名与类型写清楚，建议质量更高  
- 对生成代码仍要做 Review，尤其鉴权与 SQL  

### 2. Copilot Chat

侧边栏对话，支持：

- `/explain` 解释选中代码  
- `/fix` 针对诊断修复  
- `/tests` 生成测试骨架  

适合**局部问题**，不适合无边界地改全仓库。

### 3. Copilot CLI / Agent（演进中）

在终端用自然语言执行 Git、PR、Issue 等操作（功能随版本更新）。适合已把代码托管在 GitHub 的团队，与 Actions、PR Review 联动。

## 企业场景注意点

- **策略**：组织可限制模型、日志与敏感仓库  
- **许可**：确认代码建议是否满足公司 IP 政策  
- **秘密**：勿在注释里粘贴 API Key，避免进入训练/日志策略争议区

## 与 Cursor / Claude Code 对比（怎么选）

| 场景 | 更推荐 |
|------|--------|
| 日常写业务代码、要最便宜上手 | Copilot 补全 |
| 多文件 Agent、强编辑体验 | Cursor |
| 终端自动化、脚本化工程任务 | Claude Code / Codilot CLI |

三者可并存，但**同一文件只开一套补全**，避免快捷键冲突。

## 常见问题

**Q：建议不符合项目风格？**  
A：在仓库加 `copilot-instructions.md`（或 `.github/copilot-instructions.md`）描述规范。

**Q：Kotlin / Dart 支持如何？**  
A：语言支持广泛，但深度仍取决于上下文是否完整；大文件可配合「选中再 Chat」。

## 延伸阅读

- 收藏区：[AI 辅助编程工作流](/posts/收藏/x-ai-assisted-coding-workflows)

---

*产品名称与功能以 GitHub 官方为准。*
