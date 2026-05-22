import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Flutter FFI 技术博客',
  description: '专注 Flutter、FFI、iOS 开发的技术分享',
  lang: 'zh-CN',

  base: '/',
  cleanUrls: true,
  lastUpdated: true,

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/archive' },
      {
        text: 'GitHub',
        link: 'https://github.com/flutterffi/flutter.ffi',
      },
    ],
    sidebar: {
      '/posts/': [
        {
          text: '文章',
          items: [{ text: '欢迎来到博客', link: '/posts/hello-world' }],
        },
      ],
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/flutterffi/flutter.ffi' },
    ],
    footer: {
      message: '基于 VitePress 构建',
      copyright: 'Copyright © 2026 Flutter FFI',
    },
    search: {
      provider: 'local',
    },
    editLink: {
      pattern:
        'https://github.com/flutterffi/flutter.ffi/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页',
    },
  },
})
