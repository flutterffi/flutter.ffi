import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const postsRoot = path.resolve(__dirname, '../../posts')

export const CATEGORIES = ['阅读', '生活', '技术', '收藏']

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  if (!match) return {}
  const yaml = match[1]
  const title = yaml.match(/^title:\s*(.+)$/m)?.[1]?.trim().replace(/^['"]|['"]$/g, '')
  const category = yaml.match(/^category:\s*(.+)$/m)?.[1]?.trim().replace(/^['"]|['"]$/g, '')
  return { title, category }
}

function collectPosts(dir, base = postsRoot) {
  const posts = []
  if (!fs.existsSync(dir)) return posts

  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name)
    const stat = fs.statSync(full)
    if (stat.isDirectory()) {
      posts.push(...collectPosts(full, base))
      continue
    }
    if (!name.endsWith('.md')) continue

    const content = fs.readFileSync(full, 'utf-8')
    const { title, category } = parseFrontmatter(content)
    const rel = path.relative(base, full).replace(/\.md$/, '').replace(/\\/g, '/')
    const folderCategory = path.dirname(rel).split('/')[0]
    const resolvedCategory = category || (CATEGORIES.includes(folderCategory) ? folderCategory : '生活')

    posts.push({
      text: title || name.replace(/\.md$/, ''),
      link: `/posts/${rel}`,
      category: resolvedCategory,
      mtime: stat.mtimeMs,
    })
  }
  return posts
}

export function buildCategorySidebar() {
  const posts = collectPosts(postsRoot).sort((a, b) => b.mtime - a.mtime)
  const grouped = Object.fromEntries(CATEGORIES.map((c) => [c, []]))

  for (const post of posts) {
    if (grouped[post.category]) grouped[post.category].push({ text: post.text, link: post.link })
  }

  return CATEGORIES.map((name) => ({
    text: name,
    collapsed: false,
    items: grouped[name],
  }))
}
