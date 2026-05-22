---
title: SwiftUI 深度：NavigationStack、NavigationPath 与可恢复导航
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - Navigation
excerpt: 模型驱动导航、异构 Path、Codable 持久化与 Donny Wals 式程序化跳转的常见陷阱。
---

<img src="/photos/thumb-14.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-14.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">导航栈本质是数据，不是一串 View 指针。</p>
</div>

# NavigationStack 与 NavigationPath

Donny Wals 在 [NavigationPath 程序化导航](https://www.donnywals.com/programmatic-navigation-in-swiftui-with-navigationpath-and-navigationdestination/) 里强调：iOS 16+ 把栈写成 **数据**（`NavigationPath`），比纯 `NavigationLink` 堆视图更易测试、深链与恢复。Paul Hudson 的 [Codable 持久化示例](https://www.hackingwithswift.com/quick-start/swiftui/how-to-save-and-load-navigationstack-paths-using-codable) 则补齐了 **进程重启后续航** 的路径。

## 同质栈：数组即可

单一类型时用 `[Route]` 往往比 `NavigationPath` 更清晰：

```swift
enum Route: Hashable {
    case list
    case detail(UUID)
    case settings
}

struct RootView: View {
    @State private var path: [Route] = []

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .list: ListView()
                    case .detail(let id): DetailView(id: id)
                    case .settings: SettingsView()
                    }
                }
        }
    }
}
```

推送：`path.append(.detail(id))`  
回根：`path.removeAll()` 或 `path = []`

编译期类型安全，Codable 也简单。

## 异构栈：NavigationPath

同一栈里既有 `Int` 又有 `String`、自定义 struct 时：

```swift
@State private var path = NavigationPath()

NavigationStack(path: $path) {
    Root()
        .navigationDestination(for: Int.self) { DetailNumberView(n: $0) }
        .navigationDestination(for: String.self) { DetailStringView(s: $0) }
        .navigationDestination(for: Product.self) { ProductView($0) }
}
```

`path.append(42)` / `path.append("promo")` — **类型擦除**，运行时才检查是否注册了对应 `navigationDestination`。

陷阱：**忘记注册 destination** → 运行时静默无导航或断言。

## 绑定共享：谁拥有 path

```swift
struct Parent: View {
    @State private var path = NavigationPath()
    var body: some View {
        NavigationStack(path: $path) {
            ChildList(path: $path)
        }
    }
}

struct ChildList: View {
    @Binding var path: NavigationPath
    var body: some View {
        Button("Open") { path.append(Item(id: 1)) }
    }
}
```

**单一事实来源**：`path` 只在 ancestor 用 `@State`，子节点 `@Binding`。两处各 `@State` 各一份 path 是深链失败的头号原因。

## 持久化与深链

Apple 文档示例：`path.codable` → `NavigationPath.CodableRepresentation` → JSON。

```swift
@Observable
final class PathStore {
    var path = NavigationPath()
    private let url = URL.documentsDirectory.appending(path: "nav.json")

    func load() {
        guard let data = try? Data(contentsOf: url),
              let rep = try? JSONDecoder().decode(
                  NavigationPath.CodableRepresentation.self, from: data
              ) else { return }
        path = NavigationPath(rep)
    }

    func save() {
        guard let rep = path.codable,
              let data = try? JSONEncoder().encode(rep) else { return }
        try? data.write(to: url)
    }
}
```

注意：

- 写入 path 的类型必须 **稳定且 Codable**（改 enum case 要考虑迁移）  
- `path.codable` 为 `nil` 时表示当前栈内容无法序列化  
- 恢复应在 `ScenePhase.background` 或 `onDisappear` 保存，启动 `onAppear` 加载  

深链：`path = NavigationPath()` 后按 URL 解析 `append` 多级，与 Universal Link 处理器对接。

## 与 View 身份、状态

push 新 `DetailView` → **新身份** → 其 `@State` 新建。若需「返回保留滚动位置」，状态应放在 **path 之上的 Store** 或 `navigationDestination` 外层的 `@Observable`。

```swift
.navigationDestination(for: Item.self) { item in
    DetailView(item: item, store: store)  // store 生命周期长于 detail
}
```

## 常见 bug 表

| 现象 | 可能原因 |
|------|----------|
| append 无反应 | 未注册 `navigationDestination(for:)` |
| pop 后数据旧 | 详情页缓存未随 path 清空 |
| 恢复栈崩溃 | Codable 类型变更未迁移 |
| 双击 push 两层 | Button 与 NavigationLink 重复触发 |

## 延伸阅读

- [视图身份与生命周期](/posts/技术/swiftui-view-identity-and-lifetime)  
- Apple：`NavigationPath` 文档  
- [SwiftUI 教程索引](/posts/技术/swiftui-deep-dive-index)

---

*Navigation API 在 iOS 18+ 仍有小改动，以目标 SDK 为准。*
