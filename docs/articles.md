---
title: 文章
---

<script setup>
import { data as posts } from './posts.data'
</script>

# 文章

按时间排列的全部文章。

<ul class="post-list">
  <li v-for="post in posts" :key="post.url" class="post-list-item">
    <span class="category">{{ post.category }}</span>
    <a :href="post.url">{{ post.title }}</a>
    <time :datetime="post.date">{{ post.date }}</time>
    <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>
  </li>
</ul>

<p v-if="!posts.length" class="empty">暂无文章</p>

<style scoped>
.post-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0;
}

.post-list-item {
  padding: 1rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
}

.category {
  display: inline-block;
  margin-right: 0.5rem;
  padding: 0.1rem 0.45rem;
  font-size: 0.75rem;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  border-radius: 4px;
}

.post-list-item a {
  font-size: 1.125rem;
  font-weight: 600;
}

.post-list-item time {
  display: block;
  margin-top: 0.25rem;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
}

.post-excerpt {
  margin: 0.5rem 0 0;
  color: var(--vp-c-text-2);
}

.empty {
  color: var(--vp-c-text-3);
}
</style>
