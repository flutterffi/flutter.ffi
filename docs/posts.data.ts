import { createContentLoader } from 'vitepress'
import { CATEGORIES, type Category } from './categories'

export interface Post {
  title: string
  url: string
  date: string
  category: Category
  excerpt?: string
  tags?: string[]
}

declare const data: Post[]
export { data }

export default createContentLoader('posts/**/*.md', {
  excerpt: true,
  transform(raw): Post[] {
    return raw
      .map(({ url, frontmatter, excerpt }) => {
        const category = resolveCategory(url, frontmatter.category as string | undefined)
        return {
          title: frontmatter.title as string,
          url,
          date: formatDate(frontmatter.date as string),
          category,
          excerpt: (excerpt || frontmatter.excerpt) as string | undefined,
          tags: frontmatter.tags as string[] | undefined,
        }
      })
      .sort((a, b) => +new Date(b.date) - +new Date(a.date))
  },
})

function resolveCategory(url: string, category?: string): Category {
  if (category && CATEGORIES.includes(category as Category)) return category as Category
  const segment = url.split('/').filter(Boolean)[1]
  if (segment && CATEGORIES.includes(segment as Category)) return segment as Category
  return '生活'
}

function formatDate(raw: string): string {
  return new Date(raw).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
