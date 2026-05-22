<script setup lang="ts">
import { computed } from 'vue'
import { useData, useRoute } from 'vitepress'
import { getTagStyle } from '../utils/tagColors'

const { frontmatter } = useData()
const route = useRoute()

const isPost = computed(() => route.path.includes('/posts/'))
const tags = computed(() => {
  const t = frontmatter.value.tags
  return Array.isArray(t) ? t : []
})
const date = computed(() => frontmatter.value.date as string | undefined)
</script>

<template>
  <div v-if="isPost" class="article-meta">
    <div v-if="tags.length" class="article-tags">
      <span
        v-for="tag in tags"
        :key="tag"
        class="tag-pill"
        :style="getTagStyle(String(tag))"
      >
        {{ tag }}
      </span>
    </div>
    <div class="article-stats">
      <span v-if="date" class="meta-date">{{ date }}</span>
      <span class="meta-views">
        <span class="meta-label">Views</span>
        <span id="busuanzi_value_page_pv" class="busuanzi-value">—</span>
      </span>
    </div>
  </div>
</template>
