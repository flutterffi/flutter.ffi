<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import ArticleMeta from './components/ArticleMeta.vue'
import SiteStats from './components/SiteStats.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <template #doc-after>
      <ArticleMeta />
    </template>
    <template #layout-bottom>
      <SiteStats />
    </template>
  </DefaultTheme.Layout>
</template>
