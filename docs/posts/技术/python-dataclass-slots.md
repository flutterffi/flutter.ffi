---
title: Python dataclass：slots、frozen 与性能取舍
date: 2025-04-28
category: 技术
tags:
  - Python
excerpt: 对比 attrs/pydantic，谈配置模型与 API DTO 分层。
---
<img src="/photos/thumb-02.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-11.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">一张随拍，像评论里的脚注。</p>
</div>

# dataclass 进阶

```python
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
```

`frozen` 可哈希；`slots` 降内存、禁动态属性。

API 边界用 Pydantic 校验；内部领域用轻量 dataclass，避免全家桶 ORM 化。
