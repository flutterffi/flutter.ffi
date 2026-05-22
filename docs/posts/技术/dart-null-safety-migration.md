---
title: Dart 空安全迁移：Sound null safety 语义深潜
date: 2025-05-10
category: 技术
tags:
  - Dart
  - Flutter
excerpt: 解释 promoted flow analysis、late 与可空泛型的边界行为。
---
<img src="/photos/thumb-04.jpg" alt="配图" class="article-banner" loading="lazy" />

# Dart 空安全

Sound null safety 在编译期消灭大量 NPE。

```dart
String? name;
void greet() {
  if (name == null) return;
  print(name.length); // promoted to String
}
```

## late 与 ! 运算符

`late final` 适合延迟注入；`!` 是断言非空，滥用等于回归 NPE 赌运气。

## 迁移策略

1. `dart migrate` 生成草案
2. 先升 SDK 约束
3. 从叶子 package 向上游推进

空安全让 API **被迫表达可空性**——这是类型系统送给移动开发者最实在的礼物之一。
