---
title: Claude Code 使用教程：终端 Agent 安装与工程化实践
date: 2026-05-22
category: 技术
tags:
  - AI
  - Claude Code
  - 教程
excerpt: Anthropic 终端编程 Agent：安装、CLAUDE.md 项目记忆、权限模式与 VS Code 插件协同。
---

<img src="/photos/thumb-02.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-02.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">终端是指挥部，仓库是战场。</p>
</div>

# Claude Code 使用教程

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) 是 Anthropic 推出的**终端优先** AI 编程 Agent：能读仓库、改文件、跑命令、提 PR。适合把「一整个任务」交给 AI，而不是只补一行代码。

## 环境准备

- **Node.js** 18+（`node -v` 可验证）  
- **Git**（Windows 建议装 Git Bash）  
- **Claude 账号**：Pro / Max / Team 等（以 Anthropic 当前政策为准）  
- 可访问 Claude 服务的网络环境

## 安装

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

首次运行：

```bash
cd your-project
claude
```

按提示完成浏览器 OAuth 登录。

## 项目记忆：`CLAUDE.md`

在仓库根目录（或 `~/.claude/`）放置 `CLAUDE.md`，写清：

```markdown
# 项目约定
- Flutter 3.x，空安全
- 状态：flutter_riverpod
- 测试：修改 lib/ 必须跑 flutter test
- 不要改 ios/Pods、android/.gradle
```

Agent 每次启动会读取，**比临时 Chat 更稳定**。

## 常用命令与模式

| 命令/操作 | 说明 |
|-----------|------|
| 自然语言任务 | 「为 UserRepository 加缓存并写测试」 |
| `/compact` | 压缩对话上下文，省额度 |
| `/clear` | 换任务时清空上下文 |
| `@path/to/file` | 精确引用文件 |
| 权限确认 | 执行 shell/写文件前会询问，生产环境建议谨慎开启 auto-approve |

## 推荐任务粒度

适合：

- 按 issue 实现功能 + 测试  
- 重构模块并更新 import  
- 解释遗留代码并补文档  

不适合一次性：

- 「重写整个 App」且无测试护栏  
- 无 Git 分支的大范围自动合并  

## VS Code 协同

安装 **Claude Code** 扩展后，可在 IDE 里看 diff，在终端里跑 Agent，形成「可视化 Review + 终端执行」组合。

## 国内接入提示

若官方直连不稳定，可用 [CC Switch](https://github.com/farion1231/cc-switch) 等工具切换兼容端点（见收藏区 Appark 转载教程）。务必确认**数据合规**与密钥仅存本地。

## 常见问题

**Q：和 Cursor 冲突吗？**  
A：不冲突。Cursor 写代码，Claude Code 跑批量任务；注意两边不要同时改同一分支。

**Q：如何控制成本？**  
A：小任务单会话；大任务用 `/compact`；复杂重构拆成多个可验证子任务。

## 延伸阅读

- 收藏区：[Appark 转载 · Claude Code 安装与最佳实践](/posts/收藏/appark-claude-code-user-guide-and-installation)

---

*功能与订阅政策以 Anthropic 文档为准。*
