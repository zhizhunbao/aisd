// 公式素材 — 从 TS 文件加载（使用 String.raw 避免反斜杠转义问题）
// Formula assets — loaded from TS with String.raw to avoid backslash issues

import { formulas } from './formulas'

// 导出全部公式数组（供 ALL_ASSETS 使用）
export { formulas }

// 也导出各个公式的快捷引用
export const euclidean    = formulas.find(f => f.id === 'fml-euclidean')!
export const manhattan    = formulas.find(f => f.id === 'fml-manhattan')!
export const cosine       = formulas.find(f => f.id === 'fml-cosine')!
export const minkowski    = formulas.find(f => f.id === 'fml-minkowski')!
export const softmax      = formulas.find(f => f.id === 'fml-softmax')!
export const sigmoid      = formulas.find(f => f.id === 'fml-sigmoid')!
export const relu         = formulas.find(f => f.id === 'fml-relu')!
export const tanh         = formulas.find(f => f.id === 'fml-tanh')!
export const crossEntropy = formulas.find(f => f.id === 'fml-cross-entropy')!
export const mse          = formulas.find(f => f.id === 'fml-mse')!
export const mae          = formulas.find(f => f.id === 'fml-mae')!
export const klDivergence = formulas.find(f => f.id === 'fml-kl-divergence')!
export const bayes        = formulas.find(f => f.id === 'fml-bayes')!
export const gaussian     = formulas.find(f => f.id === 'fml-gaussian')!
export const entropy      = formulas.find(f => f.id === 'fml-entropy')!
export const dotProduct   = formulas.find(f => f.id === 'fml-dot-product')!
export const matMul       = formulas.find(f => f.id === 'fml-matrix-multiply')!
export const transpose    = formulas.find(f => f.id === 'fml-transpose')!
export const sgd          = formulas.find(f => f.id === 'fml-sgd')!
export const momentum     = formulas.find(f => f.id === 'fml-momentum')!
export const lrDecay      = formulas.find(f => f.id === 'fml-learning-rate')!
