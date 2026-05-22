import { defineConfig } from 'vitepress'
import { buildCategorySidebar } from './utils/sidebar.mjs'

const categorySidebar = buildCategorySidebar()

export default defineConfig({
  title: '阅读与生活',
  description: '阅读和生活分享',
  lang: 'zh-CN',
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/articles' },
      { text: '归档', link: '/archive' },
      { text: '我的', link: '/mine' },
    ],
    sidebar: {
      '/': categorySidebar,
      '/posts/': categorySidebar,
      '/articles': categorySidebar,
      '/archive': categorySidebar,
      '/mine': categorySidebar,
      '/guide/': [
        { text: '文档', items: [{ text: '写作指南', link: '/guide/writing' }] },
      ],
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/flutterffi/flutter.ffi' },
    ],
  },
})
