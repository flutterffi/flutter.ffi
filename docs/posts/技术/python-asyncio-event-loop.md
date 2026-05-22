---
title: Python asyncio：事件循环、Task 与 aiohttp 实战
date: 2025-02-25
category: 技术
tags:
  - Python
  - asyncio
excerpt: 区分协程与线程池 offload，避免在 async 函数里阻塞调用。
---
<img src="/photos/thumb-12.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-05.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">记录本身，就是一种立场。</p>
</div>

# asyncio 实战

```python
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

asyncio.run(main())
```

`asyncio.to_thread` 把 CPU/阻塞 IO 踢进线程池，保持 loop 畅通。

勿在 async 路由里直接 `time.sleep`——那是性能静音器。
