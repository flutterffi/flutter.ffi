export const CATEGORIES = ['阅读', '生活', '技术', '收藏'] as const

export type Category = (typeof CATEGORIES)[number]
