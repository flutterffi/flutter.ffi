---
title: 归档
---

<script setup>
import { data as posts } from './posts.data'
import { CATEGORIES } from './categories'
import { getTagStyle } from './.vitepress/theme/utils/tagColors'

const grouped = CATEGORIES.map((name) => ({
  name,
  posts: posts.filter((p) => p.category === name),
}))
</script>

# 归档

按分类浏览全部文章。

<section v-for="group in grouped" :key="group.name" class="category-block">
  <h2>{{ group.name }}</h2>
  <ul v-if="group.posts.length" class="post-list">
    <li v-for="post in group.posts" :key="post.url" class="post-list-item">
      <a :href="post.url">{{ post.title }}</a>
      <time :datetime="post.date">{{ post.date }}</time>
      <p v-if="post.tags?.length" class="post-tags">
      <span
        v-for="tag in post.tags"
        :key="tag"
        class="tag-pill"
        :style="getTagStyle(String(tag))"
      >{{ tag }}</span>
    </p>
    <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>
    </li>
  </ul>
  <p v-else class="empty">暂无文章</p>
</section>

<style scoped>
.category-block {
  margin-bottom: 2rem;
}

.category-block h2 {
  margin: 0 0 0.75rem;
  padding-bottom: 0.35rem;
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 1.25rem;
}

.post-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-list-item {
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
}

.post-list-item a {
  font-size: 1.0625rem;
  font-weight: 600;
}

.post-list-item time {
  display: block;
  margin-top: 0.2rem;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
}

.post-tags {
  margin: 0.35rem 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.post-tags .tag-pill {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 999px;
  border: 1px solid transparent;
}

.post-excerpt {
  margin: 0.45rem 0 0;
  color: var(--vp-c-text-2);
}

.empty {
  color: var(--vp-c-text-3);
  font-size: 0.9375rem;
}
</style>
