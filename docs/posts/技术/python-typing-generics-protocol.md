---
title: Python 类型系统：Protocol、Generic 与静态检查
date: 2025-03-30
category: 技术
tags:
  - Python
  - typing
excerpt: 用 mypy 严格模式约束动态语言边界，Structlog + TypedDict 示例。
---
<img src="/photos/thumb-07.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-16.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">镜头里留住的片刻，给观点一点落地的重量。</p>
</div>

# Python typing

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: str) -> Post: ...

def render(repo: Repository, id: str) -> str:
    return repo.get(id).title
```

`Protocol` 实现结构化子类型；`Generic[T]` 表达容器不变性。

`mypy --strict` 在 CI 里渐进启用，比事后补类型便宜。
