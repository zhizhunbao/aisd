// ═══════════════════════════════════════════════════════════
// 素材总索引 — 3 类核心素材
// ═══════════════════════════════════════════════════════════

import type { Asset } from '@/lib/asset-types'
import { formulas } from './formula/formulas'
import * as person from './person'
import * as code from './code'

// 把 named exports 收集为 Asset[]
const toArray = (mod: Record<string, unknown>) =>
  Object.values(mod).filter((v): v is Asset => typeof v === 'object' && v !== null && 'id' in v)

/** 所有素材 */
export const ALL_ASSETS: Asset[] = [
  ...formulas,
  ...toArray(person),
  ...toArray(code),
]

/** 数据版本 — 每次改公式/素材后自增，自动清旧缓存 */
export const DATA_VERSION = 5

/** 向后兼容 */
export const ASSET_GROUPS = { person, formula: { formulas }, code } as const
