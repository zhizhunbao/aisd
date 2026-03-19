import type { Asset } from '@/lib/asset-types'

export const asset: Asset = {
  id: 'code-pytorch',
  name: 'PyTorch nn.Module',
  category: 'code',
  subCategory: 'python',
  atomType: 'code_snippet',
  tags: ['PyTorch', 'nn.Module', 'DL'],
  knowledgeDimensions: ['code'],
  sources: [{ type: 'documentation', title: 'PyTorch', cite: 'PyTorch docs' }],
  createdAt: '2026-03-12',
  compatibleBlocks: ['CodeBlock'],
  content: {
    category: 'text_overlay',
    data: {
      overlayType: 'code',
      text: 'import torch.nn as nn\n\nclass Model(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.layers = nn.Sequential(\n            nn.Linear(784, 128),\n            nn.ReLU(),\n            nn.Linear(128, 10)\n        )\n\n    def forward(self, x):\n        return self.layers(x)',
      language: 'python',
    },
  },
}
