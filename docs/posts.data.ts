import { createContentLoader } from 'vitepress'

export interface Post {
  url: string
  title: string
  date: string
  excerpt?: string
  tags?: string[]
}

declare const data: Post[]
export { data }

export default createContentLoader('posts/*.md', {
  transform(raw): Post[] {
    return raw
      .map(({ url, frontmatter }) => ({
        url,
        title: frontmatter.title as string,
        date: frontmatter.date as string,
        excerpt: frontmatter.excerpt as string | undefined,
        tags: frontmatter.tags as string[] | undefined,
      }))
      .sort((a, b) => +new Date(b.date) - +new Date(a.date))
  },
})
