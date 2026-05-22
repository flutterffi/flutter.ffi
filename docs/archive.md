---
title: 所有文章
---

<script setup>
import { data as posts } from './posts.data'
import { CATEGORIES } from './categories'

const grouped = CATEGORIES.map((name) => ({
  name,
  posts: posts.filter((p) => p.category === name),
}))
</script>

# 所有文章

<section v-for="group in grouped" :key="group.name" class="category-block">
  <h2>{{ group.name }}</h2>
  <ul v-if="group.posts.length" class="post-list">
    <li v-for="post in group.posts" :key="post.url" class="post-list-item">
      <a :href="post.url">{{ post.title }}</a>
      <time :datetime="post.date">{{ post.date }}</time>
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

.post-excerpt {
  margin: 0.45rem 0 0;
  color: var(--vp-c-text-2);
}

.empty {
  color: var(--vp-c-text-3);
  font-size: 0.9375rem;
}
</style>
