---
title: Kotlin 属性委托：lazy、observable 与 map 存储
date: 2025-04-01
category: 技术
tags:
  - Kotlin
excerpt: 拆解 Delegates.notNull 在 Fragment 视图绑定里的典型写法与生命周期。
---
<img src="/photos/thumb-05.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-14.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">留白处，读者可以补上自己的判断。</p>
</div>

# 属性委托

```kotlin
val name: String by lazy { expensive() }
var title: String by observable("") { _, old, new ->
    println("$old -> $new")
}
```

`by viewBinding()`（Android）把样板代码收敛到委托。

自定义委托需实现 `getValue`/`setValue` 操作符，可嵌入校验、缓存、加密读写的横切逻辑。

委托是 Kotlin **语法糖背后的语义压缩**，读懂它可读遍半本 Android 开源库。
