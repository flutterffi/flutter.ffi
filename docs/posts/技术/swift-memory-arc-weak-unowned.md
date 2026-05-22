---
title: Swift ARC：strong、weak、unowned 与闭包捕获
date: 2025-05-15
category: 技术
tags:
  - Swift
  - 内存
excerpt: 用循环引用图解释 capture list 与 delegate 弱引用模式。
---
# ARC 内存管理

```swift
network.fetch { [weak self] result in
    guard let self else { return }
    self.render(result)
}
```

`weak` 用于可能为 nil 的 delegate；`unowned` 用于生命周期同步、非可选关系（误用会 UAF）。

Instruments Leaks + Memory Graph 是验证手段，别只靠 `[weak self]` 咒语。
