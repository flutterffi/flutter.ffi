---
title: Swift 面向协议编程：扩展优于继承
date: 2025-04-12
category: 技术
tags:
  - Swift
  - 协议
excerpt: 用 protocol extension 提供默认实现，谈 PAT 与类型擦除容器。
---
<img src="/photos/thumb-11.jpg" alt="配图" class="article-banner" loading="lazy" />

# 面向协议编程

```swift
protocol Loggable {
    func log(_ message: String)
}
extension Loggable {
    func log(_ message: String) { print("[\(Self.self)] \(message)") }
}
```

默认实现让协议像「可组合能力模块」。

存在类型（PAT）需 `any Loggable` 或类型擦除包装 `AnyLogger`，是 Swift 泛型设计的代价。

与 Kotlin interface 默认方法、Go 小接口哲学相通。
