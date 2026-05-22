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
      { text: '归档', link: '/archive' },
      { text: '写作指南', link: '/guide/writing' },
      { text: 'GitHub', link: 'https://github.com/flutterffi/flutter.ffi' },
    ],
    sidebar: {
      '/': categorySidebar,
      '/posts/': categorySidebar,
      '/archive': categorySidebar,
      '/guide/': [
        { text: '文档', items: [{ text: '写作指南', link: '/guide/writing' }] },
      ],
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/flutterffi/flutter.ffi' },
    ],
  },
})
