---
title: Swift 并发：async/await 与 Task 取消协作
date: 2025-01-28
category: 技术
tags:
  - Swift
  - 并发
excerpt: 讨论 TaskGroup、优先级反转与在 View 生命周期中绑定任务。
---
<img src="/photos/thumb-12.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-05.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">记录本身，就是一种立场。</p>
</div>

# Swift async/await

```swift
func loadFeed() async throws -> [Post] {
    try await withThrowingTaskGroup(of: Post.self) { group in
        for id in ids {
            group.addTask { try await api.post(id) }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}
```

`Task.checkCancellation()` 应在长循环中周期性调用。

## UI 绑定

`.task { await vm.load() }` 在 SwiftUI 视图消失时自动取消，优于裸 `Task {}` 泄漏风险。
