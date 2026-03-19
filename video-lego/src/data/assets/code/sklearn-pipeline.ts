import type { Asset } from '@/lib/asset-types'

export const asset: Asset = {
  id: 'code-pipeline',
  name: 'sklearn Pipeline',
  category: 'code',
  subCategory: 'python',
  atomType: 'code_snippet',
  tags: ['sklearn', 'Pipeline', 'Python'],
  knowledgeDimensions: ['code'],
  sources: [{ type: 'documentation', title: 'sklearn Pipeline', cite: 'sklearn docs' }],
  createdAt: '2026-03-10',
  compatibleBlocks: ['CodeBlock'],
  content: {
    category: 'text_overlay',
    data: {
      overlayType: 'code',
      text: 'from sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\n\npipe = Pipeline([\n  ("scaler", StandardScaler()),\n  ("model", clf)\n])\npipe.fit(X_train, y_train)',
      language: 'python',
    },
  },
}
