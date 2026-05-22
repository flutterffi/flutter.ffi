---
title: "Claude Code最新使用教程: 安装方式、技巧与最佳实践"
date: 2026-05-22
category: 收藏
tags:
  - Appark
  - 教程
  - 转载
source: https://appark.ai/cn/blog/claude-code-user-guide-and-installation
excerpt: "终端 AI Agent 安装、套餐选择与 VS Code 接入。"
---
<img src="/photos/thumb-09.jpg" alt="配图" class="article-banner" loading="lazy" />

> **转载说明**：本文由 [Appark 博客](https://appark.ai/cn/blog/claude-code-user-guide-and-installation) 收录备份，版权归 Appark 及原作者所有。仅供个人学习收藏，如有侵权请联系删除。

Claude Code 最新使用教程：**安装方式、技巧与最佳实践** [](#claude-code-最新使用教程-安装方式、技巧与最佳实践)

我的电脑配置可以运行Claude Code 吗？ [](#我的电脑配置可以运行claude-code-吗)

先搞清楚：Claude Code 不是普通的 AI 编程插件

Claude Code 不是单纯的代码补全工具，也不是把对话框塞进 IDE。它更准确的定位，是 **Anthropic 推出的终端侧 AI 编程 Agent**。

你可以把它理解成这样：

- 普通聊天工具：你问一句，它答一句

- 普通编程插件：你在写代码，它在旁边辅助

- Claude Code：你给它一个任务，它会去读项目、改文件、跑命令、反馈结果

- **传统插件（如早期 Copilot）：** "我帮你写完这一行。"

**IDE AI（如 Cursor）：** "我帮你重构这几个文件。"

**Claude Code：** "去喝杯咖啡吧，这个 Feature 我写完了，测试过了，PR 也提了，你回来 Review 一下就行。"

对于习惯了 **"All in AI"** 工作流的开发者来说，Claude Code 实际上是把 IDE 降级为了"查看器"，而把终端升级为了"指挥部"。

很多新手会先担心一件事：自己电脑配置一般，能不能跑 Claude Code？

大多数情况下，答案是可以。

Claude Code 的核心智能在云端，本地机器主要负责三件事：

- 提供项目文件
- 提供命令执行环境
- 
负责和云端服务通讯第一步：先把 Claude Code 安装到本地 [](#第一步-先把-claude-code-安装到本地)

1. 安装 Node.js [](#_1-安装-node-js)

Claude Code 本质上是一个 Node.js 工具，所以本地必须先安装 Node.js。

先看这张图，确认自己打开的是 Node.js 官方下载页。第一次安装直接选择稳定版本即可，不用一开始就纠结版本管理工具或多环境切换。

![image-20260424163115402](https://appark.ai/_nuxt/blog/28/image-20260424163115402.png)

这一步做完后，不要急着继续装 Claude Code，先回到终端执行 `node -v`，确认版本号已经能正常返回。如果你只是第一次上手，直接安装稳定版本即可。装好之后先执行一次：

text

```
node -v
```

能正常返回版本号，说明运行环境已经就位。

2. 建议安装 Git [](#_2-建议安装-git)

如果你在 Windows 上使用 Claude Code，建议把 Git for Windows 一起装上。原因不是"为了 Git 本身"，而是它会带来 Git Bash 这套更顺手的命令行环境。

如果你是 Windows 用户，这张图对应的就是第二步：进入 Git for Windows 官方下载页，准备补齐 Git Bash 这套命令行环境。你重点只要确认自己进的是官方下载入口即可。

![截屏2026-04-24 16.35.22](https://appark.ai/_nuxt/blog/28/%E6%88%AA%E5%B1%8F2026-04-24_16.35.22.png)

装好之后，后面再执行 npm 安装和命令检查时，整体终端体验通常会顺很多。这一步不是绝对强制，但对 Windows 用户来说，后面很多操作会顺很多。

3. 安装 Claude Code [](#_3-安装-claude-code)

环境准备好之后，就可以正式安装 Claude Code 了：

text

```
npm install -g @anthropic-ai/claude-code
```

这张图对应的动作很直接：在本地终端里执行全局安装命令，等待安装过程完成。

![image-20260424163328747](https://appark.ai/_nuxt/blog/28/image-20260424163328747.png)

看到安装界面跑完，不代表已经万事大吉，下一步一定要继续查命令有没有真正生效。装完之后，再执行一次版本检查：

text

```
claude --version
```

这张图对应的是安装后的关键验证动作。

![img](https://appark.ai/_nuxt/blog/28/v2-ab39b770eda062733a140041a2ea1604_1440w.png)

只有这一步通过，才算本地安装真正完成。能看到版本号，本地安装这一步就算完成了。

第二步：账号准备 [](#第二步-账号准备)

很多人装好本地环境之后，会以为自己已经可以直接开用了。其实不一定。

因为 Claude Code 最终调用的是 Anthropic 的服务，所以在正式使用前，你还需要先确认几件事：

- 自己当前能否正常使用 Claude 官方服务
- 是否已经准备好可用邮箱
- 当前账号是否能完成登录或注册
- 
如果后续需要更高频使用，是否已经想清楚套餐选择1. 更推荐的接入方式：cc-switch（图形界面） [](#_1-更推荐的接入方式-cc-switch-图形界面)

cc-switch 是一款跨平台的开源桌面工具，专为 Claude Code 等 AI 命令行助手设计。它本质上是一个**协议转换层 + 智能路由器**，可以一键切换不同大模型服务商的 API 配置，完美解决国内访问问题。

1. 访问 cc-switch GitHub Releases 页面
1. 根据你的系统下载对应安装包： 
- Windows：下载 `.exe` 文件
- macOS：下载 `.dmg` 文件（注意区分 Intel 和 Apple Silicon 版本）
- 
Linux：下载 `.AppImage` 或 `.flatpak` 文件
1. 双击安装包，按照向导完成安装
1. 
安装完成后启动 cc-switch，它会在系统托盘运行2. 备选安装方式：npm 命令行版 [](#_2-备选安装方式-npm-命令行版)

如果你更喜欢命令行操作：

bash

```
npm install -g cc-switch
```

**验证安装**：

bash

```
cc-switch --version
```

3. 配置模型 [](#_3-配置模型)

打开 CC Switch，在 Claude 栏下点击右上角加号，新增模型配置（这里以 GLM-5 为例）：

1. 选择目标模型（如 GLM 国内版）
1. 填入你的 API Key
1. 确认模型配置（大部分会自动填充）
1. 
点击添加

![2592887e16211b6e8f36159386a7c755](https://appark.ai/_nuxt/blog/28/2592887e16211b6e8f36159386a7c755.png)

4. 启用配置 [](#_4-启用配置)

1. 回到 cc-switch 主界面
1. 在供应商列表中找到你刚刚添加的 GLM 条目
1. 点击「启用」按钮
1. 
cc-switch 会自动配置 Claude Code 的环境变量和代理设置5. 验证配置是否生效 [](#_5-验证配置是否生效)

打开一个新的终端窗口，运行：

bash

```
claude "你好，告诉我你现在使用的是什么模型"
```

如果 Claude 回复说它正在使用 GLM 模型，说明配置成功了！

类似 Kimi、DeepSeek等模型都可以在cc-switch中配置

第三步：如何选择套餐 [](#第三步-如何选择套餐)

Claude Code 本身不是单独售卖的软件，它依赖的是 Claude 的账户体系和模型访问能力。

你可以先粗略这样理解：

| 类型 | 更适合谁 |
| --- | --- |
| 免费版 | 轻度体验、新手熟悉界面 |
| Claude Pro | 个人高频使用 Claude |
| Claude Max | 更高频率使用、Claude Code 用量更重 |
| Claude Team | 团队统一协作 |
| API | 开发接入、自定义工作流 |

如果你只是第一次体验，免费版已经够你感受基础流程；如果你准备把 Claude Code 真正接进日常开发，再去看 Pro、Max 或 API 会更合理。

第四步：我怎么先生成一个小任务给 Claude Code？ [](#第四步-我怎么先生成一个小任务给-claude-code)

新手第一次用 Claude Code，最容易犯的错误，就是一上来就把一个很大的老项目丢给它。

问题不是它不能处理，而是第一次使用时，你自己还没建立起正确预期：

- 不知道任务该怎么描述
- 不知道上下文应该给到什么程度
- 
不知道结果该怎么验证你可以试着让它干这些"体力活"，比如：

- **整一个 Demo：** "帮我搞个简单的 Todo List 或者小游戏看下效果。"
- **加个小挂件：** 给现有的页面塞个无关痛痒的小功能
- **修个现成 Bug：** 找个那种"能稳定复现、一看就知道哪坏了"的小错让它改。
- **求带路：** "这块逻辑我看着头大，你给我翻译翻译。"
- 
**补课：** "给这段代码顺手写几个测试用例。"第二张图对应的动作，就是把任务明确交给 Claude Code。第一次试手时，像"帮我生成一个小游戏"这种目标清楚、结果直观的任务最容易建立感觉。

![截屏2026-04-24 17.19.18](https://appark.ai/_nuxt/blog/28/%E6%88%AA%E5%B1%8F2026-04-24_17.19.18.png)

第三张图要看的，是 Claude Code 已经把文件和项目结构实际生成出来了。也就是说，它不是只回答思路，而是真的把任务往前推进了一步。

![img](https://appark.ai/_nuxt/blog/28/v2-2a3132fefb5ef56ea05509710e024b3e_1440w.png)

最后这张图对应的是验收动作：把生成结果真正跑起来，看它是不是能工作。第一次使用时，这一步很关键，因为它能帮你建立"任务完成"和"结果可验证"之间的联系。

![v2-7a3d4aa48ecc3e4c4688f38108e5bf291440w](https://appark.ai/_nuxt/blog/28/v2-7a3d4aa48ecc3e4c4688f38108e5bf29_1440w.webp)

这类任务最大的价值，不是项目本身有多复杂，而是它能帮你快速建立一个感觉：Claude Code 最擅长的，不是补一小行，而是接住一个完整任务并往前推进。

第五步：终端运行不方便？也可以接进 VS Code [](#第五步-终端运行不方便-也可以接进-vs-code)

很多人对 Claude Code 有兴趣，但看到命令行就先退一步：能不能还是在 IDE 里用？

可以，而且这其实是很多开发者最后最稳定的工作流。

1. 先安装 VS Code [](#_1-先安装-vs-code)

这张图对应的是 IDE 准备步骤：先把 VS Code 装好。你不用在这一步想太多，重点只是把后面要承载 Claude Code 的工作界面准备出来。

![image-20260424162559189](https://appark.ai/_nuxt/blog/28/image-20260424162559189.png)

2. 安装 Claude Code 插件 [](#_2-安装-claude-code-插件)

打开扩展市场，搜索 Claude Code，安装对应插件。

这张图对应的是插件搜索动作。你只要在扩展市场里搜到 Claude Code，并确认安装的是对应插件即可。

![截屏2026-04-23 18.35.55](https://appark.ai/_nuxt/blog/28/%E6%88%AA%E5%B1%8F2026-04-23_18.35.55.png)

安装后，界面右上角会出现入口。

这张图对应的判断点很简单：安装完成后，VS Code 里已经出现 Claude Code 的打开入口，说明它已经被接进你的日常编辑界面了。

![截屏2026-04-24 17.33.48](https://appark.ai/_nuxt/blog/28/%E6%88%AA%E5%B1%8F2026-04-24_17.33.48.png)

这套组合很适合大多数人：

- VS Code 负责浏览项目和可视化编辑
- 
Claude Code 负责执行任务和推进链路两者并不冲突，反而是互补关系。

第六步：第一次真正跑通，记住这 3 个原则 [](#第六步-第一次真正跑通-记住这-3-个原则)

第一次上手时，你只要先记住下面三件事，体验通常不会差：

原则 1：任务越具体，结果越稳定 [](#原则-1-任务越具体-结果越稳定)

不要只说"帮我优化一下"，而要说清楚：

- 你想改哪个模块
- 目标是什么
- 
有没有边界约束原则 2：先做小任务，再做大任务 [](#原则-2-先做小任务-再做大任务)

第一次就拿大型遗留项目试手，往往不是最好的体验方式。先建立节奏感，再逐步放大范围，会更稳。

原则 3：让它做事，也要学会验证结果 [](#原则-3-让它做事-也要学会验证结果)

Claude Code 很强，但它不是不用检查。最好的用法不是全盘托管，而是让它推进任务，你负责判断方向和验收结果。

第七步：常见技巧与最佳实践 [](#第七步-常见技巧与最佳实践)

上下文管理 [](#上下文管理)

- **定期使用** **`/compact`**——压缩对话以节省 Token 同时保留关键上下文
- **开启聚焦会话**——一个任务一个会话，效果比马拉松式会话好
- **明确引用文件**——用 `@filename` 而非描述文件内容
- 
**切换话题时用** **`/clear`**——换任务时清空上下文避免混淆成本优化 [](#成本优化)

| 策略 | 影响 | 方法 |
| --- | --- | --- |
| **使用 Max 计划** | 高 | 无限使用消除 Token 焦虑 |
| **写具体提示词** | 中 | 减少来回交互 |
| **使用** **`/compact`** | 中 | 压缩上下文减少 Token |
| **批量处理相关任务** | 中 | 跨相关变更复用上下文 |
| **用** **`/cost`** **监控** | 低 | 了解消耗帮助调整行为 |

高级提示词模式 [](#高级提示词模式)

**"先分析再行动"模式：**

```
First, analyze the current authentication implementation in @src/auth/.
Then, identify any security vulnerabilities.
Finally, fix the issues you found, prioritizing by severity.
```

**"参考实现"模式：**

```
Look at how pagination is implemented in @src/routes/users.ts.
Now implement the same pagination pattern for @src/routes/products.ts
and @src/routes/orders.ts.
```

**"约束优先"模式：**

```
Refactor the payment service with these constraints:
- Must maintain backward compatibility with the existing API
- Must not change the database schema
- Must keep all existing tests passing
```

**"文档驱动开发"模式：**

```
1. Write the API documentation for a new /api/v2/notifications endpoint
2. Generate the implementation based on the documentation
3. Write tests that validate the implementation matches the docs
```

1. **不要不看就批准**——始终在接受前审查 Claude 的修改
1. **不要忽略测试失败**——如果 Claude 的变更破坏了测试，先修复再继续
1. **不要跳过 CLAUDE.md**——5 分钟的设置节省数小时的修正
1. **不要使用过于宽泛的提示词**——"Refactor everything"会产生不一致的结果
1. 
**不要忘记频繁提交**——小而频繁的提交使回滚更容易Claude Code vs 竞品对比 [](#claude-code-vs-竞品对比)

Claude Code vs 竞品对比

| 功能 | Claude Code | Cursor | GitHub Copilot | Windsurf | Aider |
| --- | --- | --- | --- | --- | --- |
| **运行环境** | 终端 + IDE + Web | IDE（VS Code 分支） | IDE 插件 | IDE（VS Code 分支） | 终端 |
| **Agentic 编辑** | 完整支持 | 完整支持 | 支持Agent 模式 | 完整支持 | 完整支持 |
| **多文件编辑** | 支持 | 支持 | 支持 | 支持 | 支持 |
| **Git 自动化** | 支持完整工作流 | 基础 | 基础 | 基础 | 支持良好 |
| **MCP 支持** | 支持 | 支持 | 不支持 | 支持 | 不支持 |
| **CI/CD 模式** | 支持Headless | 不支持 | 支持Copilot CLI | 不支持 | 支持 |
| **免费版** | 不支持 | 支持有限 | 支持有限 | 支持有限 | 支持（自带密钥） |
| **起步价** | $20/月 | $20/月 | $10/月 | $15/月 | 免费（API 费用） |

选择 Claude Code 的场景 [](#选择-claude-code-的场景)

- **你是终端优先开发者**——Claude Code 为 CLI 用户而生
- **你需要 Git 自动化**——没有其他工具能匹配从分支到 PR 的端到端流程
- **你需要多平台访问**——终端、VS Code、JetBrains、桌面应用、Web、Slack
- 
**你需要 CI/CD 集成**——Headless 模式专为自动化管道设计选择替代品的场景 [](#选择替代品的场景)

- **你想要可视化 IDE 体验**——Cursor 和 Windsurf 提供更丰富的可视化 diff 和 GUI 工作流
- **你预算有限**——GitHub Copilot 从 $10/月起
- 
**你更喜欢行内建议**——Copilot 和 Cursor 在输入时的自动补全更流畅Claude Code vs Cursor 深入对比 [](#claude-code-vs-cursor-深入对比)

| 方面 | Claude Code | Cursor |
| --- | --- | --- |
| **UX 范式** | 对话驱动 | 混合——行内建议 + 聊天 + Composer |
| **上下文窗口** | 按需读取，整个代码库可访问 | 索引代码库用于 @-mentions |
| **多文件编辑** | 原生——Claude 规划并一次性跨文件编辑 | Composer 模式——多文件编辑带可视化 diff |
| **学习曲线** | 较陡——需要终端操作和提示词技巧 | 较缓——熟悉的 VS Code 界面加 AI 层 |
| **最适合** | 复杂重构、Git 自动化、CI/CD | 实时编码辅助、可视化工作流 |

常见问题 [](#常见问题)

**Q1：Claude Code 和 Cursor，到底先用哪个？**

**A：** 这取决于你是想找个"副驾驶"**还是**"外包代工"。

- 如果你习惯边写边想，享受在 IDE 里那种实时交互的快感，选 **Cursor**，它的可视化界面能让你随时"查漏补缺"。
- 
但如果你有一个明确的项目目标（比如：重构整个 Auth 模块），想让 AI 像个资深开发一样自己进目录、改代码、跑测试，那 **Claude Code** 这种 Agent（智能体）模式才是真香。**Q2：Claude Code 本身需要单独掏钱买吗？**

**A：** 工具本身免费开源，但里面的"刀片"是要钱的。你真正要操心的是你的 **Claude API 额度**或者 **Claude Pro 订阅**。本质上，你是在为背后的"大脑"付费，而不是为了这个终端界面。

**Q3：我的老破小电脑配置一般，跑得动 Claude Code 吗？**

**A：** 放心，它不吃你电脑的 CPU，它吃的是云端算力。 Claude Code 的重活儿（思考和推理）全在云端跑，你本地只要能跑得起 Node.js、能连上网，它就能起飞。这就好比用低配电脑玩云游戏，**大脑在天上，你手里拿的只是个手柄。**

**Q4：第一次上手，最适合拿什么任务"调教"它？**

**A：** 别一上来就让它写个操作系统。 最推荐的是那种"边界清晰的脏活累活"。比如：

1. 写一个简单的 CRUD Demo；
1. 给一段屎山代码加注释；
1. 
修复一个已经定位清楚的逻辑 Bug。 让它在这些小任务里展现一下"自动读文件、自动跑命令"的闭环能力，你瞬间就能 get 到它的威力。**Q5：如果我只是想写代码，不想研究那些繁琐的接入细节怎么办？**

**A：** 术业有专攻，如果你不想在配置 API、网络环境上浪费半天时间，走"代购模式"最省心。 国内有很多集成服务，帮你打通了所有接入环节。你只需要关心如何给它下指令，剩下的脏活累活（比如环境适配、统一计费）交给它们就行。**毕竟，开发者的每一分钟，都应该花在创造上。**
