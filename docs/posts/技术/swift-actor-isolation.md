---
title: Swift Actor：数据竞争与 MainActor 边界
date: 2025-02-20
category: 技术
tags:
  - Swift
  - Actor
excerpt: 解释 actor 串行化、nonisolated 与 @MainActor 标注 UI 代码的实践。
---
<img src="/photos/thumb-03.jpg" alt="配图" class="article-banner" loading="lazy" />

# Swift Actor

```swift
actor ImageCache {
    private var store: [URL: Data] = [:]
    func data(for url: URL) -> Data? { store[url] }
    func insert(_ data: Data, for url: URL) { store[url] = data }
}
```

Actor 把可变状态关进**串行邮箱**，编译器阻止外部直接并发读写。

`@MainActor` 标记 ViewModel/UI 层，跨 actor 调用需 `await`，语义比 GCD 队列清晰。

与 Kotlin 协程、Go channel 对照学习，可建立统一「隔离」词汇表。
