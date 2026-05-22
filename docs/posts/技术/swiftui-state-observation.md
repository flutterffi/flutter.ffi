---
title: SwiftUI 状态：@Observable 与 Observation 框架迁移
date: 2025-03-25
category: 技术
tags:
  - Swift
  - SwiftUI
excerpt: 从 ObservableObject 到 @Observable 宏，减少 objectWillChange 样板。
---
<img src="/photos/thumb-03.jpg" alt="配图" class="article-banner" loading="lazy" />

# SwiftUI 状态观察

iOS 17+ `@Observable` 取代部分 `ObservableObject`：

```swift
@Observable
final class BookStore {
    var books: [Book] = []
    func refresh() async { books = await api.fetch() }
}
```

View 对属性的读取被跟踪，细粒度刷新，减轻无效 `body` 重算。

迁移时留意与 `EnvironmentObject` 混用期的边界；UIKit 桥接仍可用 `UIHostingController`。
