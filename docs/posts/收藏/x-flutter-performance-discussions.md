---
title: 收藏｜X 上关于 Flutter 性能的高赞讨论精华
date: 2026-05-20
category: 收藏
tags:
  - Flutter
  - 收藏
  - X
excerpt: 整理开发者社区关于 Impeller、重建优化与真机 Profiling 的共识与争议，附可执行检查清单。
---
<img src="/photos/thumb-15.jpg" alt="配图" class="article-banner" loading="lazy" />

# X 上关于 Flutter 性能的讨论精华

> 本文为**编辑整理**，归纳公开技术社区（含 X/Twitter、Mastodon 技术圈）常见观点，非单条推文转载。具体作者与链接因时效未逐一列出，建议结合官方文档验证。

## 1. 「卡顿」先分三类

社区高频提醒：先区分 **构建（build）**、**布局（layout）**、**绘制（paint）** 三类成本。DevTools 里看 `build` 次数飙升，优先 `const` 与状态下沉；GPU 线程热，查 `RepaintBoundary` 与图片解码尺寸。

## 2. Impeller 不是万能药

2024–2025 年讨论里，Impeller 被寄予「消灭着色器编译 jank」的期望，但复杂矢量与模糊仍可能吃 GPU。整理帖共识：**在目标机型 profile**，不要只看发布会帧率。

## 3. 列表与图片是移动端真凶

多条高互动帖指向同一结论：

- `ListView.builder` + 固定 `itemExtent` 当可行时
- 网络图必须限制解码宽高（`cacheWidth` / `cacheHeight`）
- 避免在滚动回调里同步 IO

## 4. 可执行的每周 Profiling 仪式

| 步骤 | 动作 |
|------|------|
| 周一 | `flutter run --profile` 走核心路径 |
| 合并前 | 对比 `build` 热点是否新增 |
| 发布前 | 低端 Android 实机 10 分钟 monkey |

## 5. 社区争议：要不要「极致」优化

一派认为应像原生一样抠每帧；另一派认为业务迭代优先，**只在用户可感知处优化**。整理建议是：为关键转化路径设性能预算（例如首屏 < 1.2s），其余遵循 lint 即可。

---

若你只收藏一篇 Flutter 性能相关讨论，建议把**可复现的 Profiling 流程**写在团队 Wiki，比收藏推文链接更耐用。
