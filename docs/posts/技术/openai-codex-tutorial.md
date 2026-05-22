---
title: OpenAI Codex 使用教程：IDE 插件与 CLI 工程 Agent
date: 2026-05-22
category: 技术
tags:
  - AI
  - OpenAI Codex
  - 教程
excerpt: 面向软件工程任务的 Codex：在 Cursor/VS Code 中安装、ChatGPT 登录、模型选择与任务拆分。
---

<img src="/photos/thumb-04.jpg" alt="配图" class="article-banner" loading="lazy" />

# OpenAI Codex 使用教程

OpenAI **Codex**（2025–2026 产品线中的工程 Agent）定位是参与真实开发流程：读仓库、改多文件、跑命令、协助 Code Review。与早期「只补全 API」不同，当前形态更接近**可授权执行的编程代理**。

## 前置条件

- **ChatGPT Plus / Pro / Business** 或团队授权（政策以 OpenAI 为准）  
- 稳定访问 OpenAI 服务  
- 推荐宿主：**Cursor**、VS Code，或支持 Codex 扩展的 IDE

## 在 Cursor 中安装（常见路径）

1. 打开扩展市场，搜索 **Codex** 官方插件并安装。  
2. 打开任意文件，从侧边栏或命令面板进入 Codex 面板。  
3. 选择 **Sign in with ChatGPT**，浏览器完成 OAuth。  
4. 在设置中将默认模型切到 **GPT-5.x-Codex**（名称随版本更新）。  
5. 按需开启 **Full Access**（文件与终端权限）；企业项目建议先在分支上试用。

## 适合交给 Codex 的任务

| 类型 | 示例 |
|------|------|
| 实现 | 「按 `docs/spec.md` 实现导出 CSV 接口」 |
| 重构 | 「把 `legacy/` 下回调改为 async/await」 |
| 审查 | 「检查 PR 中鉴权遗漏」 |
| 运维脚本 | 「写 GitHub Actions 缓存 Flutter 依赖」 |

每条任务应包含：**完成定义**（测试命令、截图、接口契约）。

## 工作流建议

1. **开分支**：`git checkout -b codex/feature-x`  
2. **缩小范围**：一次只改一个模块，避免整仓重写  
3. **让它跑测试**：在提示里写 `flutter test` / `pytest` 必须通过  
4. **人工 Review diff**：重点看安全、并发、边界条件  
5. **合并前 squash 或整理提交信息**

## 与 API 开发的关系

Plus 用户往往**无需单独 API Key** 即可在 IDE 使用 Codex；若要做 CI Headless、自定义流水线，再查阅 OpenAI 是否提供 CLI/API 形态及计费。

## 与 DeepSeek 等开源模型

开源模型适合自建推理、成本可控；Codex 优势通常在**复杂工程调度与工具链整合**。可按任务类型分工具，而非只留一个。

## 常见问题

**Q：登录失败？**  
A：确认订阅档、系统时间、代理；清理浏览器 Cookie 后重试 OAuth。

**Q：和 Cursor 自带 Agent 重复吗？**  
A：可并存，但避免对同一任务开两套 Agent 同时改文件。

## 延伸阅读

- 收藏区：[Appark 转载 · Codex 实战与 DeepSeek 对比](/posts/收藏/appark-openai-codex-guide-gpt55-vs-deepseekv4)

---

*模型名称与权限以 OpenAI 官方文档为准。*
