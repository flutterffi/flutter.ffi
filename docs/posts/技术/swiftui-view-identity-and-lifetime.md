---
title: SwiftUI 深度：视图身份（Identity）如何决定状态生死
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - 架构
excerpt: 结构身份 vs 显式 id、ForEach 稳定性、TabView 懒加载与 onAppear 为何「对不上号」。
---

<img src="/photos/thumb-12.jpg" alt="配图" class="article-banner" loading="lazy" />

# 视图身份与生命周期

SwiftyPlace 关于 [onAppear 何时触发](https://www.swiftyplace.com/blog/swiftui-view-lifecycle-onappear) 的文章把问题拆成两条轨：**节点生命周期**（图里有没有这个 View）与 **可见性**（用户看不看得到）。很多「onAppear 乱了」其实是 **身份** 和 **容器策略** 叠在一起。

## 两种身份来源

### 1. 结构身份（Structural Identity）

由 View 树 **位置** 决定：

```swift
VStack {
    Header()
    if showDetail { Detail() }  // 分支切换 → 不同身份
    Footer()
}
```

`if` 从 false→true，`Detail` **首次插入** 图；false 时节点被移除，其 `@State` 随之销毁（除非用别的容器保留）。

### 2. 显式身份（Explicit Identity）

```swift
ChildView()
    .id(user.id)
```

`user.id` 变化 → SwiftUI 认为是 **另一个 ChildView** → `@State` 重置。

ForEach 同理：

```swift
ForEach(items) { item in
    Row(item: item)
}
// 依赖 item.id（Identifiable）稳定；用 indices 且无稳定 id 会整行闪烁重置
```

**反模式**：`ForEach(items.indices, id: \.self)` 在删除中间元素时 id 错位，状态串台。

## 状态「还在」但 onDisappear  fired？

常见场景：`TabView` 切走、 `NavigationStack` pop、`List` 滚出屏幕。

| 容器 | 节点是否销毁 | onDisappear 含义 |
|------|----------------|------------------|
| `if/else` 假分支 | 销毁 | 真消失 |
| `TabView`（iOS 18+ 懒加载） | 未访问的 tab 可能未创建 | 首次选中才 onAppear |
| `NavigationStack` pop | 销毁（除非用 `.navigationDestination` 特殊保留） | pop 时触发 |
| `List` / `LazyVStack` | 滚出可能销毁 cell | 可见性 + 回收 |

**iOS 17 vs 18**：TabView 是否在启动时 **eager** 构建所有 tab，会影响「后台 tab 的 onAppear 是否在启动时就跑」。支持 iOS 17 时要按 **最低版本** 测一遍。

## 设计模式：何时用 `.id()` 重置

**合理用法**：

- 登录用户切换，表单必须清空  
- 选中列表项变化，详情页完全重载  

```swift
DetailView(item: item)
    .id(item.id)
```

**滥用**：每次 body 里 `UUID()` 当 id → 每帧新身份 → 动画闪、输入框丢字、网络请求死循环。

## 与 @StateObject / @Observable 的边界

```swift
struct Screen: View {
    @StateObject private var vm = ViewModel()
    var body: some View { ... }
}
```

`@StateObject` 的 **首次创建** 绑在 View 身份上。身份被 `.id()` 换掉 → **新 ViewModel**，旧订阅若未 cancel 会泄漏。

`@Observable` + `@State` 持有：

```swift
@State private var vm = ViewModel()
```

同样受身份影响；换用户时应 **显式** `vm = ViewModel()` 或 `.id(userId)`。

## 工程 checklist

1. 列表用 **稳定业务 id**，不用纯 index  
2. 条件分支切换前问：要不要保留子树状态？要则换 `opacity`/`hidden` 或上层 `@State`  
3. 数据加载放 `.task(id:)` 而非裸 `onAppear`，与身份解耦  
4. 深链进 NavigationStack 时，path 与 View 身份 **一起设计**（见 [NavigationPath 深度](/posts/技术/swiftui-navigation-path-deep-dive)）  

## 最小实验

```swift
struct IdentityLab: View {
    @State private var flag = true
    @State private var counter = 0
    var body: some View {
        VStack {
            if flag {
                Child(counter: $counter).id("a")
            } else {
                Child(counter: $counter).id("b")
            }
            Button("Toggle branch") { flag.toggle() }
        }
    }
}
```

观察切换分支时 counter 是否归零；再去掉 `.id` 对比。

## 延伸阅读

- [AttributeGraph 与 @State](/posts/技术/swiftui-attribute-graph-and-state)  
- [onAppear 与容器语义](/posts/技术/swiftui-lifecycle-onappear-containers)  
- objc.io：Swift Talk Attribute Graph 系列

---

*容器行为随 iOS 版本变化，请在目标 deployment target 上实测。*
