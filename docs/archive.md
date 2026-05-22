---
title: 所有文章
---

<script setup>
import { data as posts } from './posts.data'
</script>

# 所有文章

<ul class="post-list">
  <li v-for="post in posts" :key="post.url" class="post-list-item">
    <a :href="post.url">{{ post.title }}</a>
    <time :datetime="post.date">{{ post.date }}</time>
    <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>
    <p v-if="post.tags?.length" class="post-tags">
      <span v-for="tag in post.tags" :key="tag">#{{ tag }}</span>
    </p>
  </li>
</ul>

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

.post-tags span {
  margin-right: 0.5rem;
  font-size: 0.8125rem;
  color: var(--vp-c-brand-1);
}
</style>
