---
title: Kotlin 协程：结构化并发与作用域取消
date: 2025-01-20
category: 技术
tags:
  - Kotlin
  - 协程
excerpt: 从 CoroutineScope、Job 层次与 supervisorScope 谈取消传播与异常聚合。
---
# Kotlin 结构化并发

协程不是「轻量线程」口号，而是一套**带生命周期**的并发抽象。

```kotlin
class DetailViewModel : ViewModel() {
    private val scope = viewModelScope
    fun load() = scope.launch {
        val user = async { repo.user() }
        val posts = async { repo.posts() }
        _ui.value = Ui(user.await(), posts.await())
    }
}
```

`viewModelScope` 在 `onCleared` 自动 `cancel`，避免泄漏。

## supervisorScope

子任务失败不拖垮兄弟任务，适合「多源聚合」仪表盘。

## 与 Flutter 对照

Dart Isolate 无共享状态；Kotlin 协程共享内存但用挂起函数串起异步——选型取决于平台与团队栈。
