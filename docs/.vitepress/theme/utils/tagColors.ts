const TAG_PALETTE: Record<string, { bg: string; color: string }> = {
  Git: { bg: '#e3f2fd', color: '#1565c0' },
  工作流: { bg: '#e8eaf6', color: '#3949ab' },
  生活: { bg: '#fce4ec', color: '#c2185b' },
  阅读: { bg: '#e8f5e9', color: '#2e7d32' },
  技术: { bg: '#fff3e0', color: '#ef6c00' },
  Giffgaff: { bg: '#f3e5f5', color: '#7b1fa2' },
  英国: { bg: '#e1f5fe', color: '#0277bd' },
  旅行: { bg: '#fff8e1', color: '#f9a825' },
  随笔: { bg: '#efebe9', color: '#5d4037' },
  Book: { bg: '#f1f8e9', color: '#558b2f' },
}

const FALLBACKS = [
  { bg: '#e3f2fd', color: '#1565c0' },
  { bg: '#f3e5f5', color: '#6a1b9a' },
  { bg: '#e0f2f1', color: '#00695c' },
  { bg: '#fff3e0', color: '#e65100' },
  { bg: '#fce4ec', color: '#ad1457' },
]

export function getTagStyle(tag: string): Record<string, string> {
  const preset = TAG_PALETTE[tag]
  if (preset) {
    return {
      backgroundColor: preset.bg,
      color: preset.color,
      borderColor: preset.color + '33',
    }
  }
  const index =
    tag.split('').reduce((sum, ch) => sum + ch.charCodeAt(0), 0) %
    FALLBACKS.length
  const fb = FALLBACKS[index]
  return {
    backgroundColor: fb.bg,
    color: fb.color,
    borderColor: fb.color + '33',
  }
}
