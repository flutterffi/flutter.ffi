---
title: SwiftUI 深度：布局提案（Layout Proposal）与子视图尺寸协商
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - Layout
excerpt: 从 proposedSize、idealSize 到 Layout 协议与 alignmentGuide，理解 SwiftUI 不是 Auto Layout 字符串。
---

<img src="/photos/thumb-13.jpg" alt="配图" class="article-banner" loading="lazy" />

# 布局提案引擎

UIKit 用约束求解；SwiftUI 用 **提案—响应** 协商。Rafal Sroka 等作者在 [SwiftUI 架构与 UIKit 关系](https://rafalsroka.com/posts/swiftui-architecture/) 里强调：布局仍落到 `sizeThatFits` / `layoutSubviews`，但上层语义是 **父向子提议尺寸，子返回实际占用**。

## 三档 proposed size

父容器传给子 `proposedSize` 常是：

| 提议 | 含义（直觉） |
|------|----------------|
| `width: nil, height: nil` | 子自己决定（类似 intrinsic） |
| 具体数值 | 上限/目标，子可更小 |
| `infinity` | 尽量占满（在 safe 范围内） |

子 View 的 `body` 返回后，布局引擎汇总 **理想尺寸** 与 **最小/最大** 约束，再决定分配。

常见困惑：

```swift
Text("Hi")
    .frame(maxWidth: .infinity)
```

`Text` 本想 wrap intrinsic width，父级 `HStack` 给了 **水平 infinity 提案** → Text 被拉满。解决：`.fixedSize(horizontal: true, vertical: false)` 或外层不用无限提案。

## 读尺寸：GeometryReader 的代价

```swift
GeometryReader { geo in
    Color.red.frame(width: geo.size.width * 0.5)
}
```

`GeometryReader` **总是占满父级给的最大提案**，再把孩子尺寸告诉内部。滥用会导致：

- 列表 cell 高度异常  
- 滚动冲突（与 ScrollView 抢提案）  

优先：`VisualEffect`、`containerRelativeFrame`（iOS 17+）、`onGeometryChange`（iOS 17+）等更窄的 API。

## alignmentGuide：在协商后微调

```swift
HStack(alignment: .firstTextBaseline) {
    Text("Ag")
    Image(systemName: "star")
        .alignmentGuide(.firstTextBaseline) { d in d[.bottom] * 0.8 }
}
```

`alignmentGuide` 改的是 **对齐锚点**，不是布局提案本身；适合图标与文字基线对齐。

## Layout 协议（iOS 16+）

自定义 `Layout` 实现 **measure + place**，等价于「我掌控所有子节点的提案与最终 frame」：

```swift
struct FlowLayout: Layout {
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let maxWidth = proposal.width ?? .infinity
        var x: CGFloat = 0, y: CGFloat = 0, rowHeight: CGFloat = 0
        var totalHeight: CGFloat = 0
        for sub in subviews {
            let size = sub.sizeThatFits(.unspecified)
            if x + size.width > maxWidth, x > 0 {
                x = 0; y += rowHeight; rowHeight = 0
            }
            rowHeight = max(rowHeight, size.height)
            x += size.width + 8
            totalHeight = max(totalHeight, y + rowHeight)
        }
        return CGSize(width: maxWidth, height: totalHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x = bounds.minX, y = bounds.minY, rowHeight: CGFloat = 0
        let maxWidth = bounds.width
        for sub in subviews {
            let size = sub.sizeThatFits(.unspecified)
            if x + size.width > bounds.minX + maxWidth, x > bounds.minX {
                x = bounds.minX; y += rowHeight; rowHeight = 0
            }
            sub.place(at: CGPoint(x: x, y: y), proposal: .unspecified)
            x += size.width + 8
            rowHeight = max(rowHeight, size.height)
        }
    }
}
```

要点：

- `sizeThatFits` 必须 **纯函数式**，不依赖副作用  
- `place` 里对每个子应使用与其测量时 **一致的 proposal**  
- 可用 `cache` 存测量结果，避免 O(n²)  

## 与 UIKit 互操作的尺寸

`UIViewRepresentable` 默认提案常导致 **intrinsicContentSize 与 SwiftUI 提案冲突**：

```swift
func sizeThatFits(_ proposal: ProposedViewSize, uiView: UIView, context: Context) -> CGSize? {
    let target = CGSize(width: proposal.width ?? UIView.noIntrinsicMetric,
                        height: proposal.height ?? UIView.noIntrinsicMetric)
    let fitted = uiView.systemLayoutSizeFitting(target)
    return fitted
}
```

iOS 16+ 实现 `sizeThatFits` 可减少「SwiftUI 里 UIView 高度为 0」类问题。

## 调试布局

1. 给可疑层加 `.border(Color.red)` 看实际 frame  
2. 逐层去掉 `frame(maxWidth: .infinity)`  
3. Instrument **SwiftUI** 类别查看布局重复计算  
4. 复杂列表优先 **固定行高** 或 `LazyVStack` + 明确 proposal  

## 延伸阅读

- [UIKit 桥接与 UIHostingController](/posts/技术/swiftui-uikit-interop-hosting)  
- Apple：*Compose custom layouts with SwiftUI*（WWDC22）  
- Donny Wals：布局相关短文（偏好、safeArea 等）

---

*API 以当前 SDK 为准。*
