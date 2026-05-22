---
title: Kotlin Flow 对比 RxJava：冷流、背压与操作符心智
date: 2025-02-08
category: 技术
tags:
  - Kotlin
  - Flow
excerpt: 说明 StateFlow、SharedFlow 与 Observable 在 UI 状态层的映射关系。
---
<img src="/photos/thumb-06.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-15.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">街角的光，像新闻标题一样突然又平常。</p>
</div>

# Flow vs RxJava

Flow 默认是**冷流**：收集才执行，利于资源节约。

```kotlin
fun ticker(): Flow<Int> = flow {
    var i = 0
    while (true) {
        emit(i++)
        delay(1000)
    }
}
```

`stateIn` / `shareIn` 把冷流热化，供多收集器订阅。

## 背压

`buffer`、`conflate` 处理生产快于消费；Android UI 常配合 `repeatOnLifecycle` 避免后台收集。

新项目优先 Flow；维护遗留 Rx 可用 `kotlinx-coroutines-rx2` 桥接。
