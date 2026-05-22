---
title: Kotlin Multiplatform Mobile：共享逻辑与原生 UI 边界
date: 2025-03-12
category: 技术
tags:
  - Kotlin
  - KMP
excerpt: 评估 expect/actual、网络层下沉与 Compose Multiplatform 的现状与坑。
---
<img src="/photos/thumb-04.jpg" alt="配图" class="article-banner" loading="lazy" />

# KMM 边界

KMP 擅长共享：**序列化模型、仓库、业务规则**；UI 仍多平台原生或 Compose Multiplatform。

```kotlin
// commonMain
expect class PlatformLogger {
    fun log(msg: String)
}
```

## 与 Flutter 对比

Flutter 共享 UI + 逻辑；KMP 共享逻辑 + 原生 UI——组织技能栈不同。

## 工程化

用 `commonTest` 跑纯 Kotlin 测试；版本对齐 Kotlin、Gradle、SKIE（Swift 互操作）需锁定 BOM。

选型没有绝对赢家，只有团队现有产能曲线。
