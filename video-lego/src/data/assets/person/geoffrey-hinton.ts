import type { Asset } from '@/lib/asset-types'

export const asset: Asset = {
  id: 'per-geoffrey-hinton',
  name: 'Geoffrey Hinton',
  category: 'person',
  subCategory: 'portrait',
  atomType: 'person_card',
  tags: ['科学家', 'DL', '反向传播'],
  sources: [{ type: 'wikipedia', title: 'Geoffrey Hinton', cite: 'Wikipedia' }],
  createdAt: '2026-03-10',
  content: {
    category: 'person',
    data: { name: 'Geoffrey Hinton', title: '深度学习先驱', bio: '2024年诺贝尔物理学奖得主，反向传播算法重要贡献者' },
  },
}
