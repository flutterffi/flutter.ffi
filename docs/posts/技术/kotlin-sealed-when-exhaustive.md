---
title: Kotlin 密封类：代数数据类型与穷尽 when
date: 2025-05-02
category: 技术
tags:
  - Kotlin
  - 类型系统
excerpt: 用 sealed interface 建模 UI 状态机，与 Swift enum associated value 对照。
---
# 密封类与穷尽 when

```kotlin
sealed interface Result<out T> {
    data class Ok<T>(val value: T) : Result<T>
    data class Err(val cause: Throwable) : Result<Nothing>
}

fun <T> Result<T>.fold(onOk: (T) -> Unit, onErr: (Throwable) -> Unit) = when (this) {
    is Result.Ok -> onOk(value)
    is Result.Err -> onErr(cause)
}
```

编译器保证分支穷尽，重构新增子类时编译器会逼你改全 `when`。

这与 Swift `enum`、Rust `enum` 同族，是**把状态机写进类型**的正道。
