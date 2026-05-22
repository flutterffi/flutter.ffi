---
title: SwiftUI 深度：@Observable 宏、依赖跟踪与迁移陷阱
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - Observation
excerpt: Observation 框架如何把属性访问变成依赖边，以及 @ObservationIgnored、Environment 与性能边界。
---

<img src="/photos/thumb-15.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-15.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">少刷新不是魔法，是更细的依赖图。</p>
</div>

# @Observable 宏与依赖跟踪

本站已有短文 [SwiftUI 状态观察](/posts/技术/swiftui-state-observation)。本篇补足 **机制与迁移深水区**，思路与 Apple *Discover Observation in SwiftUI*（WWDC23）及社区对 AttributeGraph 细粒度边的讨论一致。

## 从 ObservableObject 到 Observation

旧模式：

```swift
final class Store: ObservableObject {
    @Published var items: [Item] = []
    func reload() { ... }  // 未 @Published → 改了 UI 可能不刷新
}
```

任何 `@Published` 变化 → `objectWillChange` → 所有观察该对象的 View **整棵重算**。

新模式：

```swift
@Observable
final class Store {
    var items: [Item] = []
    func reload() async { items = await api.fetch() }
}
```

View `body` 里 **读到** `store.items` 才登记依赖；只改未读字段时，不触发该 View。

## 宏背后在干什么（概念层）

`@Observable` 为类型合成：

- 访问跟踪（per-instance registrar）  
- 与 SwiftUI 集成的 `ObservationRegistrar`  
- 使类型满足 `Observable` 协议  

编译期改写属性访问器，在 get 时 `access(keyPath:)`，set 时 `withMutation(keyPath:)`。

你不需要手写 `objectWillChange`，但 **必须在观察周期内读取属性** 才能建立依赖。

## @ObservationIgnored

```swift
@Observable
final class Session {
    var token: String = ""
    @ObservationIgnored var lastHash: Int = 0  // 不触发 UI
}
```

适合：缓存、调试计数、非 UI 的派生字段。  
滥用会导致：**数据变了 UI 不更新**。

## 与 SwiftUI 集成的写法

### 推荐（iOS 17+）

```swift
struct LibraryView: View {
    @State private var store = Store()
    var body: some View {
        List(store.items) { ... }
            .task { await store.reload() }
    }
}
```

或注入 Environment：

```swift
extension EnvironmentValues {
    @Entry var store: Store = Store()
}

// 根视图
.environment(\.store, store)
```

子 View `@Environment(\.store) var store`。

### 避免

```swift
@ObservedObject var store: Store  // 旧包装，对 @Observable 非最优
```

若必须 iOS 16 兼容，保留 `ObservableObject` 分支或 `#available` 双实现。

## 性能边界：不是银弹

1. **body 里读太多属性** → 依赖边仍多，重算成本上升  
2. **大数组整体替换** → 依赖 `items` 的 View 全刷新；考虑 diff 或 section 化  
3. **在 body 做重计算** → 应 `@ObservationIgnored` + 手动缓存或移到 async  

```swift
// 反模式
var body: some View {
    let sorted = store.items.sorted(by: heavyCompare)  // 每次访问都排序
    return List(sorted) { ... }
}
```

改：

```swift
@Observable final class Store {
    private(set) var sorted: [Item] = []
    func reload() async {
        let raw = await api.fetch()
        sorted = raw.sorted(by: heavyCompare)
    }
}
```

## 与 @Bindable

对 `@Observable` 对象中的值类型字段双向绑定：

```swift
struct Editor: View {
    @Bindable var draft: Draft  // Draft 为 @Observable class 中的模型
    var body: some View {
        TextField("Title", text: $draft.title)
    }
}
```

`@Bindable` 替代部分 `@ObservedObject` + `@Published` 的表单场景。

## 迁移 checklist

| 步骤 | 动作 |
|------|------|
| 1 | 类标 `@Observable`，去掉 `ObservableObject` |
| 2 | 删除 `@Published`，普通 stored property |
| 3 | View 改 `@State` / `@Environment` 持有 |
| 4 | 检查 `onReceive(objectWillChange)` 改为显式逻辑 |
| 5 | 单元测试：未读属性变更不触发 view 更新（可用 ViewInspector 等） |

## 与 AttributeGraph 的关系

`@Observable` 让 **依赖边更细**；底层仍走 SwiftUI 更新事务。  
调试时仍用 SwiftUI Instrument，关注「哪条属性访问导致 Text 重绘」。

## 延伸阅读

- [AttributeGraph 与 @State](/posts/技术/swiftui-attribute-graph-and-state)  
- [SwiftUI 状态观察（短文）](/posts/技术/swiftui-state-observation)  
- Apple：Observation 框架文档、WWDC23 Observation session

---

*部署目标若含 iOS 16，请保留 ObservableObject 代码路径。*
