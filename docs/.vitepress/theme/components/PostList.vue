<script setup lang="ts">
import { data as posts } from '../../../posts.data'
</script>

<ul class="post-list">
  <li v-for="post in posts.slice(0, 5)" :key="post.url" class="post-list-item">
    <a :href="post.url">{{ post.title }}</a>
    <time :datetime="post.date">{{ post.date }}</time>
    <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>
  </li>
</ul>
<p class="more">
  <a href="/archive">查看全部文章 →</a>
</p>

<style scoped>
.post-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  max-width: 42rem;
  margin-inline: auto;
}

.post-list-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
}

.post-list-item a {
  font-weight: 600;
}

.post-list-item time {
  display: block;
  margin-top: 0.2rem;
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.post-excerpt {
  margin: 0.35rem 0 0;
  font-size: 0.9375rem;
  color: var(--vp-c-text-2);
}

.more {
  margin-top: 1rem;
  text-align: center;
}
</style>
