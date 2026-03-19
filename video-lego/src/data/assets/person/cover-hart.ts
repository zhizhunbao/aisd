import type { Asset } from '@/lib/asset-types'

export const asset: Asset = {
  id: 'per-cover-hart',
  name: 'Cover & Hart (1967)',
  category: 'person',
  subCategory: 'portrait',
  atomType: 'person_card',
  tags: ['科学家', 'KNN', '1967'],
  sources: [{ type: 'paper', title: 'Nearest neighbor pattern classification', author: 'Cover & Hart', year: 1967, cite: 'Cover & Hart (1967)' }],
  createdAt: '2026-03-10',
  content: {
    category: 'person',
    data: { name: 'Cover & Hart', title: '统计学家', bio: '1967年提出最近邻分类算法的理论基础' },
  },
}
