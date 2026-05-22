---
title: Go channel 与 select：并发模式集锦
date: 2025-03-08
category: 技术
tags:
  - Go
  - 并发
excerpt: fan-in、超时 select、done channel 关闭语义与 nil channel 陷阱。
---
<img src="/photos/thumb-11.jpg" alt="配图" class="article-banner" loading="lazy" />

# channel 模式

```go
select {
case v := <-ch:
    handle(v)
case <-time.After(time.Second):
    return errors.New("timeout")
case <-ctx.Done():
    return ctx.Err()
}
```

关闭 channel 表示「不再有值」；接收方用 `v, ok := <-ch` 判断。

用 `errgroup` 管理一组 goroutine 生命周期，比裸 channel 更不易泄漏。
