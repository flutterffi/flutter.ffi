---
title: Flutter FFI 与 C 互操作：从 dlopen 到内存所有权
date: 2025-02-14
category: 技术
tags:
  - Flutter
  - FFI
  - Dart
excerpt: 梳理 Dart FFI 调用 C 库时符号加载、结构体布局与指针生命周期的常见陷阱。
---
# Flutter FFI 与 C 互操作

移动与桌面场景常需复用既有 C/C++ 能力：编解码、传感器 SDK、游戏引擎碎片。Dart 2.12+ 的 `dart:ffi` 提供稳定 ABI，但**所有权**与**线程**仍是事故高发区。

## 最小可用示例

```dart
import 'dart:ffi';
import 'dart:io';

typedef NativeAdd = Int32 Function(Int32 a, Int32 b);
typedef DartAdd = int Function(int a, int b);

void main() {
  final lib = DynamicLibrary.open(Platform.isMacOS ? 'libadd.dylib' : 'libadd.so');
  final add = lib.lookupFunction<NativeAdd, DartAdd>('add');
  print(add(2, 40));
}
```

## 结构体与内存对齐

C 侧 `struct SensorFrame` 的 padding 必须与 Dart `@Packed` / 字段顺序一致。建议用 `ffigen` 从头文件生成绑定，避免手写偏移错误。

## 回调与 Isolate

C 回调若跨线程触发 Dart 代码，应通过 `NativePort` 或把结果投递回主 Isolate。切勿在回调里直接操作 Flutter Widget 树。

## 实践建议

1. 用 `Arena` 批量分配、统一 `release`。
2. 为每个 native 句柄建立 Dart 侧 `Finalizer`。
3. 在 CI 里对 Android/iOS/macOS 三端做 smoke test。

FFI 不是银弹，但用好它能让 Flutter 真正「全栈到原生边界」。
