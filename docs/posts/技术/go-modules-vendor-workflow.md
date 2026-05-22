---
title: Go Modules 与 vendor：依赖可复现构建
date: 2025-05-20
category: 技术
tags:
  - Go
  - 工程化
excerpt: go.work 多模块、replace 指令与私有 module proxy 配置要点。
---
<img src="/photos/thumb-16.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-09.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">画面不必解释一切，它只是让叙述慢下来。</p>
</div>

# Go Modules 工程化

```bash
go mod tidy
go test ./...
```

企业内网用 `GOPRIVATE` + Athens 代理；`go mod vendor` 在离线构建环境仍有价值。

`go.work` 适合 monorepo 本地联调多个 module，勿提交含绝对路径的 work 文件到公开仓库。
