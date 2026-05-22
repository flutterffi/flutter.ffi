---
title: SwiftUI 深度：onAppear、task 与容器生命周期语义
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - 生命周期
excerpt: 区分节点销毁与仅不可见，理清 TabView、NavigationStack、LazyVStack 下数据加载应挂在哪。
---

<img src="/photos/thumb-16.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-16.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">出现不等于创建，消失不等于销毁。</p>
</div>

# onAppear、task 与容器语义

参考 SwiftyPlace 对 [View Lifecycle](https://www.swiftyplace.com/blog/swiftui-view-lifecycle-onappear) 的拆解：生产 bug 的根源常是把 **onAppear 当成 viewDidLoad**，而 SwiftUI 里二者不对等。

## 四条轨道（建议分开记）

| 轨道 | 问题 |
|------|------|
| **结构** | 节点是否在树里（if/else、pop） |
| **身份** | 是否是「同一个」逻辑实例（`.id`） |
| **可见性** | 用户是否看到（Tab 切换、cover） |
| **数据** | `@State` / Store 是否仍存活 |

`onAppear` 横跨 **结构 + 可见性**；`onDisappear` 同理。  
**@State 生死** 只跟 **结构 + 身份** 走。

## 应用级数据加载放哪

### 优先：`.task(id:)`

```swift
struct FeedView: View {
    let userId: String
    @State private var posts: [Post] = []

    var body: some View {
        List(posts) { ... }
            .task(id: userId) {
                posts = await api.feed(userId: userId)
            }
    }
}
```

- `userId` 变 → 取消旧任务、重新加载  
- View 从树移除 → 自动 cancel  
- 比 `onAppear` + 手动 `Task` 更少泄漏  

### 慎用：裸 `onAppear`

```swift
.onAppear {
    Task { await load() }  // 无自动 cancel；重复 appear 可能并发多次
}
```

若必须用，配合 `taskId` 标志或 `async let` 去重。

## 容器 cheat sheet（生产向）

| 容器 | onAppear 典型时机 | @State 何时没 |
|------|-------------------|---------------|
| `if` 真 | 进入分支 | 离开分支 |
| `sheet` 展示 | sheet 出现 | dismiss |
| `TabView` | 首次选中 tab（iOS 18+ 懒加载） | 极少因切换 tab 销毁 |
| `NavigationStack` push | 目标页入场 | pop |
| `List` / `LazyVStack` | cell 入屏 | 滚出回收可能丢 |

**TabView iOS 17**：未选中的 tab 也可能在启动时 `onAppear` → 后台 tab 里写 `fetch()` 会在启动就打 API。支持 17 要实测。

## Navigation 与 onAppear

push `DetailView`：

- `onAppear`：每次显示都会调（含从子页 pop 回来）  
- 若只要「首次加载」，用 `@State private var didLoad` 或把数据放在 **不因 pop 销毁** 的 Store  

```swift
.task(id: item.id) { detail = await api.detail(item.id) }
```

pop 再 push 同一 `item.id`：task 可能 **不重启**（身份相同）——要强制刷新用 `id: "\(item.id)-\(refreshToken)"`。

## List 预取 vs 重复请求

```swift
List(items) { item in
    Row(item: item)
        .task { await prefetch(item) }
}
```

快速滚动 → 多个 `.task` 并发 → 需要 **取消友好** 的 `prefetch`（检查 `Task.isCancelled`）。

## fullScreenCover 与 Alert

`fullScreenCover` 内容子树的 `onAppear` 与底层页 **并存**；底层 `onDisappear` **不一定** 调用。  
不要在 cover 打开时假设底层已「消失」。

## 与 UIKit 混用

`UIViewControllerRepresentable` 里：

- `updateUIViewController` 可能极频繁  
- 应用 `makeCoordinator` + `context.coordinator` 做一次性 setup  
- 数据加载仍建议放在 SwiftUI 层 `.task`，而非 `updateUIViewController`  

## 调试清单

1. 打 log：`onAppear` / `onDisappear` / `deinit`（class）  
2. 看 **是否缺 id 导致 List 复用错行**  
3. Instrument Time Profiler + SwiftUI 看重复 body  
4. 用 `.task(id:)` 替换散落的 `onAppear Task`  

## 延伸阅读

- [视图身份](/posts/技术/swiftui-view-identity-and-lifetime)  
- [NavigationPath](/posts/技术/swiftui-navigation-path-deep-dive)  
- [Swift 并发与 Task](/posts/技术/swift-async-await-task)

---

*容器行为以 Apple Release Notes 为准，跨版本务必回归。*
