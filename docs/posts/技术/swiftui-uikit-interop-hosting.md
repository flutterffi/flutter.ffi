---
title: SwiftUI 深度：UIHostingController 与 UIViewRepresentable 互操作
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - UIKit
excerpt: 从 UIHostingController 桥接、表示式更新频率到 Coordinator 模式与尺寸协商。
---

<img src="/photos/thumb-01.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-02.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">SwiftUI 画意图，UIKit 仍画像素。</p>
</div>

# UIKit 互操作与 Hosting

多篇文章（如 [SwiftUI Under the Hood](https://rafalsroka.com/posts/swiftui-architecture/)）共同结论：**iOS 上 SwiftUI 最终仍通过 UIKit 渲染**。`Text` → `UILabel` 类实现；`List` →  UITableView 风格基础设施。桥梁核心是 `UIHostingController<Content>`。

## UIHostingController 放在哪

### 纯 SwiftUI App

`@main struct App` → `WindowGroup` 内部已是 hosting 树，无需手写。

### UIKit 宿主（渐进迁移）

```swift
let root = UIHostingController(rootView: MainTabView())
root.view.backgroundColor = .systemBackground
window.rootViewController = root
```

注意：

- 安全区、方向、状态栏由 hosting VC 传递  
- 嵌入 `UINavigationController` 时，SwiftUI 内再用 `NavigationStack` 可能 **双导航栏** — 通常二选一  

### 局部 SwiftUI

```swift
final class LegacyVC: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        let host = UIHostingController(rootView: SettingsPanel())
        addChild(host)
        view.addSubview(host.view)
        host.view.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            host.view.topAnchor.constraint(equalTo: view.topAnchor),
            host.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            host.view.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            host.view.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ])
        host.didMove(toParent: self)
    }
}
```

`host.view` 参与 Auto Layout；SwiftUI 内部布局仍走提案模型。

## UIViewRepresentable 模板

```swift
struct MapTile: UIViewRepresentable {
    var coordinate: CLLocationCoordinate2D

    func makeUIView(context: Context) -> MKMapView {
        let map = MKMapView()
        map.delegate = context.coordinator
        return map
    }

    func updateUIView(_ map: MKMapView, context: Context) {
        // 轻量同步；避免每次 body 都开新 region 动画
        let region = MKCoordinateRegion(center: coordinate, span: .init(latitudeDelta: 0.05, longitudeDelta: 0.05))
        if map.region.center.latitude != coordinate.latitude {
            map.setRegion(region, animated: context.transaction.animation != nil)
        }
    }

    func makeCoordinator() -> Coordinator { Coordinator() }

    final class Coordinator: NSObject, MKMapViewDelegate {}
}
```

原则：

| 方法 | 应做 |
|------|------|
| `makeUIView` | 一次性创建、设 delegate |
| `updateUIView` | 把 **SwiftUI 状态 → UIKit 属性**，要幂等 |
| `makeCoordinator` | 委托、target-action、KVO |

**反模式**：在 `updateUIView` 里 `addSubview` 重复叠加。

## 更新频率陷阱

`body` 每帧重算 → `updateUIView` 狂调。  
用 `Equatable` 包装减少 diff：

```swift
struct MapTile: UIViewRepresentable, Equatable {
    var coordinate: CLLocationCoordinate2D
    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.coordinate.latitude == rhs.coordinate.latitude &&
        lhs.coordinate.longitude == rhs.coordinate.longitude
    }
    // ...
}

// 使用处
MapTile(coordinate: coord).equatable()
```

或使用 `UIViewControllerRepresentable` 处理复杂 VC 生命周期。

## 尺寸：iOS 16+ sizeThatFits

```swift
func sizeThatFits(_ proposal: ProposedViewSize, uiView: MKMapView, context: Context) -> CGSize? {
    CGSize(width: proposal.width ?? 320, height: proposal.height ?? 240)
}
```

否则 SwiftUI 可能给 UIKit 视图 **零高度** 或撑满错误轴向。

## 事件与 Focus

- UIKit → SwiftUI：Coordinator 里 `Binding` 或 `@Observable` Store  
- SwiftUI → UIKit：`updateUIView` 传参  
- 键盘：注意 `UIViewRepresentable` 与 `ScrollView` 抢 responder  

## SwiftUI in Cell

`List` 中嵌 heavy `UIViewRepresentable` 仍贵。可选：

1. 纯 SwiftUI 重写  
2. `UICollectionView` + hosting configuration（iOS 16 `UIHostingConfiguration`）  
3. 预渲染静态图 + 点击再加载地图  

## 延伸阅读

- [布局提案引擎](/posts/技术/swiftui-layout-proposal-engine)  
- [视图生命周期](/posts/技术/swiftui-lifecycle-onappear-containers)  
- Apple：*Working with UIKit in SwiftUI*

---

*visionOS / macOS 桥接类型名不同，以平台文档为准。*
