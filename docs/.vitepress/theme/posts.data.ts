import { createContentLoader } from 'vitepress'

export interface Post {
  title: string
  url: string
  date: string
  excerpt?: string
  tags?: string[]
}

declare const data: Post[]
export { data }

export default createContentLoader('posts/*.md', {
  excerpt: true,
  transform(raw): Post[] {
    return raw
      .map(({ url, frontmatter, excerpt }) => ({
        title: frontmatter.title as string,
        url,
        date: formatDate(frontmatter.date as string),
        excerpt: (excerpt || frontmatter.excerpt) as string | undefined,
        tags: frontmatter.tags as string[] | undefined,
      }))
      .sort((a, b) => +new Date(b.date) - +new Date(a.date))
  },
})

function formatDate(raw: string): string {
  return new Date(raw).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
