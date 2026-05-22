---
title: Flutter Isolate：并发模型与消息传递实战
date: 2025-03-02
category: 技术
tags:
  - Flutter
  - Dart
  - 并发
excerpt: 对比 Isolate 与线程池思维，说明 compute、ReceivePort 与后台解析大 JSON 的模式。
---
<img src="/photos/thumb-16.jpg" alt="配图" class="article-banner" loading="lazy" />

# Flutter Isolate 实战

Dart 单线程事件循环保证 UI 顺滑，CPU 密集任务必须 offload。

## compute 与 Isolate.run

```dart
final parsed = await Isolate.run(() => heavyParse(bytes));
```

Flutter 3.7+ 推荐 `Isolate.run` 替代部分 `compute` 场景，语义更清晰。

## 双向通信

```dart
final port = ReceivePort();
await Isolate.spawn(worker, port.sendPort);
port.listen((msg) => print(msg));
```

复杂流水线可引入 `IsolateNameServer` 做注册发现。

## 常见误区

- 试图在 Isolate 间共享可变对象（应序列化消息）。
- 在 UI Isolate 做图像解码（用 `decodeImageFromList` 仍可能卡帧，应后台化）。

Isolate 是「无共享内存的 actor」——理解这一点，并发设计会简单很多。
