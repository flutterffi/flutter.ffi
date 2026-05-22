---
title: Widget 重建优化：从 RepaintBoundary 到 ListView 懒加载
date: 2025-04-22
category: 技术
tags:
  - Flutter
  - 性能
excerpt: 用 Profile 模式定位 rebuild 热点，总结 const、Key 与 itemExtent 策略。
---
# Widget 重建优化

## 诊断流程

1. `flutter run --profile`
2. DevTools → Performance → 「Track rebuilds」
3. 观察 `build` 次数是否随父节点频繁刷新而飙升

## 手段清单

| 手段 | 场景 |
|------|------|
| `const` 构造 | 静态子树 |
| `RepaintBoundary` | 动画隔离重绘 |
| `ListView.builder` | 长列表 |
| `AutomaticKeepAliveClientMixin` | Tab 保活 |

## ListView 陷阱

给 `itemExtent` 可让滚动跳变计算更便宜；图片列表配合 `cacheWidth/Height` 降采样。

性能优化不是提前崇拜微优化，而是**用数据证明 rebuild 值得被消灭**。
