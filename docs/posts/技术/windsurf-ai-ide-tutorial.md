---
title: Windsurf 使用教程：Cascade 流式编辑与 AI IDE 入门
date: 2026-05-22
category: 技术
tags:
  - AI
  - Windsurf
  - 教程
excerpt: Codeium 出品的 AI IDE：Cascade 多步推理、Flows 工作流与和 Cursor 的差异选型。
---

<img src="/photos/thumb-05.jpg" alt="配图" class="article-banner" loading="lazy" />

# Windsurf 使用教程

[Windsurf](https://windsurf.com)（原 Codeium 编辑器路线）是与 Cursor 同类的 **AI-native IDE**，主打 **Cascade**——把「理解 → 规划 → 改文件 → 跑终端」串成连续流，减少你在 Chat 与编辑器之间来回粘贴。

## 安装

1. 官网下载对应系统安装包（注意 Apple Silicon / Intel）。  
2. 注册 Codeium / Windsurf 账号并选择套餐（Free 档通常有额度限制）。  
3. 可选导入 VS Code 配置，缩短上手时间。

## 核心概念

| 概念 | 说明 |
|------|------|
| **Cascade** | 多步 Agent，自动拆任务并连续执行，适合中等规模功能开发 |
| **Flows** | 可保存的重复流程（如「加 API + 测试 + 文档」） |
| **补全** | 行级预测，与 Cascade 互补 |
| **上下文** | 自动索引仓库，也可 `@` 指定文件 |

## 推荐使用方式

### 日常小改

用行级补全 + 局部 Chat，和 Copilot/Cursor 类似。

### 功能级开发

在 Cascade 面板输入**带验收标准**的任务，例如：

```text
在 lib/checkout/ 实现优惠券校验：
- 新增 CouponValidator
- 单元测试覆盖过期、叠加、非法码
- 不要修改 payment_gateway.dart
```

等待 Cascade 分步执行，**每步 diff 可中断或回滚**。

### 团队规范

在项目根添加说明文件（名称以 Windsurf 当前文档为准，常见为规则/记忆文件），写明：

- 目录结构与命名  
- 必须跑的 CI 命令  
- 禁止修改的路径  

## 与 Cursor 如何二选一

| 维度 | Windsurf | Cursor |
|------|----------|--------|
| 多步自动化 | Cascade 流式串联 | Composer / Agent |
| 生态 | 较新，扩展在追赶 | VS Code 迁移成熟 |
| 定价 | 以官网为准 | 以官网为准 |
| 手感 | 偏「一条龙」 | 偏「编辑器 + Agent 面板」 |

建议各试用一周，用**同一仓库同一任务**（如加一个 API 模块）对比 diff 质量与速度。

## 常见问题

**Q：Cascade 改太多怎么办？**  
A：Git 分支 + 限制提示词目录；要求「每步先列出将改的文件清单」。

**Q：公司仓库能用吗？**  
A：查看 Windsurf/Codeium 企业条款与隐私模式；涉密代码走私有化方案。

**Q：和 Claude Code 关系？**  
A：Windsurf 是 IDE；Claude Code 是终端 Agent，可互补而非替代。

---

*功能命名与订阅以 Windsurf 官网为准。*
