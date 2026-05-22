---
title: Riverpod 2.x：依赖注入与 UI 解耦架构笔记
date: 2025-03-18
category: 技术
tags:
  - Flutter
  - Riverpod
  - 架构
excerpt: 用 Provider 组合替代 InheritedWidget 泥球，讨论 AsyncNotifier 与 family 参数化。
---
<img src="/photos/thumb-15.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-08.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">镜头里留住的片刻，给观点一点落地的重量。</p>
</div>

# Riverpod 架构笔记

`flutter_riverpod` 把状态提升为可测试的图结构，而不是散落在 Widget 树里。

## 核心概念

```dart
@riverpod
Future<User> user(UserRef ref, String id) async {
  return ref.watch(apiProvider).fetchUser(id);
}
```

`ref.watch` 建立依赖；`ref.listen` 处理副作用；`ref.read` 仅用于一次性动作（如按钮 onPressed）。

## 与 Repository 分层

- **Presentation**: ConsumerWidget
- **Application**: Notifier / AsyncNotifier
- **Data**: Repository + DataSource

测试时用 `ProviderContainer(overrides: [...])` 注入假实现，无需 pump 整棵 Widget 树。

## 反模式

全局 `read` 触发刷新却不 `watch`，导致 UI 不更新；在 `build` 里 `read` 网络请求。

Riverpod 强迫你把数据流画清楚——这正是中大型 Flutter 项目需要的纪律。
