---
title: Go 接口：隐式实现与小接口哲学
date: 2025-04-18
category: 技术
tags:
  - Go
  - 接口
excerpt: 从 io.Reader 到仓储抽象，讨论接口应定义在消费方一侧。
---
<img src="/photos/thumb-09.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-02.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">日常场景往往比热搜更长命。</p>
</div>

# Go 接口

```go
type Store interface {
    Save(ctx context.Context, b Blog) error
}
```

接口越小，mock 越简单。Go 习惯**在用时定义接口**，而非先画巨大 UML。

空接口 `any` 与泛型（Go 1.18+）分工：能类型参数化就别滥用 `any`。
