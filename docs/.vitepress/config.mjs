import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Flutter FFI 技术博客',
  description: '专注 Flutter、FFI、iOS 开发的技术分享',
  lang: 'zh-CN',
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/posts/hello-world' },
      { text: '归档', link: '/archive' },
      { text: 'GitHub', link: 'https://github.com/flutterffi/flutter.ffi' },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/flutterffi/flutter.ffi' },
    ],
  },
})
