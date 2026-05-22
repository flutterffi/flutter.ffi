---
title: SwiftUI 深度：AttributeGraph、@State 存哪儿、更新怎么传播
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - AttributeGraph
excerpt: 从 @State 的真实存储位置、依赖边到脏标记与 body 重算，建立可验证的 SwiftUI 运行时心智模型。
---

<img src="/photos/thumb-11.jpg" alt="配图" class="article-banner" loading="lazy" />

# AttributeGraph、@State 与更新传播

社区里 objc.io [Swift Talk 的 Attribute Graph 系列](https://talk.objc.io/episodes/S01E429-attribute-graph-part-1)、SwiftyPlace 对 [AttributeGraph 引擎](https://www.swiftyplace.com/blog/the-attributegraph-the-engine-behind-every-swiftui-view) 的梳理，以及 Michael Tsai 对 [@State 与图节点](https://mjtsai.com/blog/2026/05/14/swiftui-state-and-the-attribute-graph/) 的摘要，都指向同一件事：**SwiftUI 的「状态」不在 View 结构体里**。

本文是本站原创整理，用于把碎片知识串成可调试的心智模型。

## View 是描述，不是控件实例

```swift
struct CounterView: View {
    @State private var count = 0
    var body: some View {
        Button("+\(count)") { count += 1 }
    }
}
```

每次 `count` 变化，`CounterView` 作为 **值类型** 会被重新求值 `body`，但：

- 旧 struct 被丢弃，新 struct 被创建  
- **`count` 的整数值不跟着 struct 搬家**  
- struct 里只有指向运行时图的 **token / 引用**

因此「我在 View 里改了 @State，为什么下次 body 还能读到」——因为读写的是 **图上的节点**，不是 struct 字段。

## AttributeGraph 在干什么

可粗浅理解为：

1. **节点**：状态（@State、@Binding、Environment 值）、布局属性、部分派生数据  
2. **边（依赖）**：某个 `Text` 的 `body` 读取了 `count` → 建立依赖  
3. **脏标记**：`count` 写入 → 标记下游节点 dirty  
4. **拉取求值**：渲染阶段按需重新计算 dirty 子图，而非全树重绘  

这与「输入变化就全量重算」的增量库不同，更接近 **lazy pull**（objc.io 在复现 AttributeGraph 时的表述）。

WWDC21 *Demystify SwiftUI* 用「transactions → 依赖边 → 受影响 View」解释 Instrument，与 Xcode 里 SwiftUI Instrument 的蓝色依赖边一致。

## @State 的生命周期绑在「身份」上

**谁声明 @State，图节点就挂在谁的 View 身份上。**

| 操作 | @State 是否保留 |
|------|----------------|
| 同一身份下 body 重算 | 保留 |
| 改 `.id()` 或切换 `if/else` 分支导致身份变化 | 通常 **重置** |
| `NavigationLink` push 新实例 | 新身份 → 新状态 |

典型踩坑：

```swift
if flag {
    EditorView()
        .id(sessionA)
} else {
    EditorView()
        .id(sessionB)
}
```

两个分支是 **不同身份**，各自 `@State` 互不相干——这是特性，不是 bug。

## 一次点击背后发生了什么（简化时序）

1. `Button` action 写 `@State count`  
2. AttributeGraph 标记依赖 `count` 的节点为 dirty  
3. SwiftUI runtime 合并为 frame 内的 **transaction**（避免一帧内多次布局抖动）  
4. 对 dirty 子图重新求值 `body`、布局、合成  
5. 底层通过 `UIHostingController` 等桥接到 UIKit/AppKit 更新具体控件  

UIKit 仍画像素；SwiftUI 决定 **哪些描述需要重新翻译**。

## 和 @Observable（iOS 17+）的关系

`@Observable` 把依赖跟踪下沉到 **访问属性** 时注册，细粒度 invalidation，减少 `objectWillChange` 的全局刷新。

但 **图模型仍在**：只是「依赖边」从「整个 ObservableObject」收缩到「用到的字段」。

迁移时仍要注意：

- 在 `init` 里读 `@Observable` 属性 **不会** 建立观察（应在 `body` 或 `.onAppear` 读）  
- 与 `@State` 混用时，身份规则不变  

## 可操作的调试手段

1. **SwiftUI Instrument**（Xcode）：看 transaction、依赖边、重算的 View 类型  
2. **`Self._printChanges()`**（调试构建）：打印 body 重算原因（API 随版本变化，查当前 SDK）  
3. **故意加 `.id()`**：验证状态丢失是否身份问题  
4. **最小复现**：单个 `@State` + 单个 `Text`，排除 List/Navigation 副作用  

## 实践结论

- 把 `@State` 当成 **图上的外部存储**，不是 struct 字段  
- 任何「状态丢了」优先查 **身份**，再查绑定链  
- 性能优化应减少 **无效依赖边**（少在 body 里读大对象、拆子 View）  

## 延伸阅读

- [SwiftUI 视图身份与生命周期](/posts/技术/swiftui-view-identity-and-lifetime)  
- [@Observable 宏与依赖跟踪](/posts/技术/swiftui-observable-macro-deep-dive)  
- Apple：*Demystify SwiftUI*（WWDC21）、*Data Essentials in SwiftUI*（WWDC20）

---

*私有框架细节随系统版本演进，以 Apple 文档与 Instrument 为准。*
