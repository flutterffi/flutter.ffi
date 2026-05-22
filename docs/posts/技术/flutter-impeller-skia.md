---
title: Impeller 渲染管线：Flutter 图形栈的一次重构
date: 2025-04-05
category: 技术
tags:
  - Flutter
  - 渲染
  - Impeller
excerpt: 简述 Impeller 相对 Skia 在着色器预编译、光栅化与 jank 上的取舍。
---
# Impeller 与 Skia

Impeller 是 Flutter 为降低**首帧着色器编译卡顿**而引入的渲染后端，尤其针对 Vulkan/Metal。

## 设计动机

Skia 运行时 JIT 着色器在移动端可能造成「神秘掉帧」。Impeller 倾向**离线生成**管线状态对象（PSO），把不确定性前移。

## 对开发者的影响

- 自定义 `FragmentProgram` 仍可用，但需关注后端差异。
- 复杂 Path 与模糊效果在旧设备上应做性能 profiling。

## 调试手段

`flutter run --enable-impeller`（平台默认策略随版本变）配合 DevTools Performance 观察 GPU 线程。

渲染栈变迁说明：Flutter 不只是在写 Widget，而是在经营一条跨平台的 GPU 流水线。
