---
title: 跨平台移动开发 2025：Flutter、KMP 与原生三角
date: 2025-05-25
category: 技术
tags:
  - Flutter
  - Kotlin
  - Swift
excerpt: 从团队技能、包体、生态与 FFI 四个维度做技术选型矩阵。
---
# 跨平台选型矩阵

| 维度 | Flutter | KMP | 双原生 |
|------|---------|-----|--------|
| UI 一致性 | 高 | 中 | 低 |
| 原生能力 | FFI/Platform Channel | 直接 | 最好 |
| 包体 | 中偏大 | 中 | 基准 |
| 热更新 | 受限 | 受限 | 商店策略 |

没有银弹：金融强监管可能偏原生；内容型产品 Flutter 效率高；已有大量 Kotlin 业务逻辑可 KMP 下沉。

用**团队主语言 + 发布节奏**倒推技术，而不是倒过来。
