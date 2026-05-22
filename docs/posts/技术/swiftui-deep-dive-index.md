---
title: SwiftUI 深度教程索引
date: 2026-05-23
category: 技术
tags:
  - Swift
  - SwiftUI
  - 索引
excerpt: 本站 SwiftUI 深度系列：AttributeGraph、身份、布局、导航、Observation、生命周期与 UIKit 互操作。
---

<img src="/photos/thumb-02.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-03.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">先建立运行时模型，再谈组件 API。</p>
</div>

# SwiftUI 深度教程索引

本系列为**原创技术长文**，写作时参考了社区高质量来源的思路（非转载），便于对照深入学习：

- [objc.io Swift Talk · Attribute Graph](https://talk.objc.io/episodes/S01E429-attribute-graph-part-1)  
- [SwiftyPlace · AttributeGraph / Lifecycle](https://www.swiftyplace.com/blog/the-attributegraph-the-engine-behind-every-swiftui-view)  
- [Donny Wals · NavigationPath](https://www.donnywals.com/programmatic-navigation-in-swiftui-with-navigationpath-and-navigationdestination/)  
- [Michael Tsai · @State 摘要](https://mjtsai.com/blog/2026/05/14/swiftui-state-and-the-attribute-graph/)  
- [Rafal Sroka · SwiftUI 架构](https://rafalsroka.com/posts/swiftui-architecture/)  

## 运行时与状态

| 主题 | 文章 |
|------|------|
| AttributeGraph、@State 存储与更新 | [AttributeGraph 与 @State](/posts/技术/swiftui-attribute-graph-and-state) |
| 视图身份与状态生死 | [视图身份与生命周期](/posts/技术/swiftui-view-identity-and-lifetime) |
| @Observable 宏与迁移 | [@Observable 深度](/posts/技术/swiftui-observable-macro-deep-dive) |
| 短文：Observation 入门 | [SwiftUI 状态观察](/posts/技术/swiftui-state-observation) |

## 布局与导航

| 主题 | 文章 |
|------|------|
| 布局提案与 Layout 协议 | [布局提案引擎](/posts/技术/swiftui-layout-proposal-engine) |
| NavigationPath 与持久化 | [NavigationStack 深度](/posts/技术/swiftui-navigation-path-deep-dive) |

## 生命周期与互操作

| 主题 | 文章 |
|------|------|
| onAppear / task / 容器 | [生命周期与容器](/posts/技术/swiftui-lifecycle-onappear-containers) |
| UIHostingController、Representable | [UIKit 互操作](/posts/技术/swiftui-uikit-interop-hosting) |

## 相关 Swift 基础（本站）

- [Swift 并发与 Task](/posts/技术/swift-async-await-task)  
- [Actor 隔离](/posts/技术/swift-actor-isolation)  
- [协议导向设计](/posts/技术/swift-protocol-oriented-design)  

## 建议阅读顺序

1. AttributeGraph 与 @State  
2. 视图身份  
3. @Observable 深度  
4. 布局提案  
5. NavigationPath  
6. 生命周期  
7. UIKit 互操作  

---

*系列会随 iOS SDK 更新；请以真机与 Instrument 验证为准。*
