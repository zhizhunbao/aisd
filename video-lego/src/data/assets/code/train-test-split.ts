import type { Asset } from '@/lib/asset-types'

export const asset: Asset = {
  id: 'code-split',
  name: 'train_test_split',
  category: 'code',
  subCategory: 'python',
  atomType: 'code_snippet',
  tags: ['sklearn', 'split', 'Python'],
  knowledgeDimensions: ['code'],
  sources: [{ type: 'documentation', title: 'sklearn', cite: 'sklearn docs' }],
  createdAt: '2026-03-10',
  compatibleBlocks: ['CodeBlock'],
  content: {
    category: 'text_overlay',
    data: {
      overlayType: 'code',
      text: 'from sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = \\\n    train_test_split(X, y, test_size=0.2,\n                     random_state=42, stratify=y)',
      language: 'python',
    },
  },
}
