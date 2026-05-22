---
title: Go context.Context：超时、取消与请求作用域
date: 2025-02-02
category: 技术
tags:
  - Go
  - context
excerpt: 贯穿 HTTP handler、gRPC 与 worker 池的取消传播惯例。
---
# context.Context

```go
ctx, cancel := context.WithTimeout(parent, 3*time.Second)
defer cancel()
req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
```

**不要把 Context 存在 struct 字段里**——Go 文档明确反对；应作为函数首参 `ctx context.Context` 传递。

`context.WithCancelCause`（Go 1.20+）让取消原因可观测，利于分布式追踪。
