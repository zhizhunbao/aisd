import type { Asset } from '@/lib/asset-types'

export const asset: Asset = {
  id: 'per-fix-hodges',
  name: 'Fix & Hodges (1951)',
  category: 'person',
  subCategory: 'portrait',
  atomType: 'person_card',
  tags: ['科学家', 'KNN', '1951'],
  sources: [{ type: 'paper', title: 'Discriminatory analysis', author: 'Fix & Hodges', year: 1951, cite: 'Fix & Hodges (1951)' }],
  createdAt: '2026-03-10',
  content: {
    category: 'person',
    data: { name: 'Fix & Hodges', title: '统计学家', bio: '1951年提出最初的非参数分类方法' },
  },
}
