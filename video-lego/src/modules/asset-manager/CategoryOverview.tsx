// ═══════════════════════════════════════════════════════════
// 分类概览（首页）— 所有分类卡片网格
// CategoryOverview — All category cards in a grid
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import { ASSET_CATEGORIES } from '@/lib/asset-types'
import { AssetCatIcon } from '@/components/AssetIcons'
import { IconPlus } from '@/components/Icons'

type CatWithCount = typeof ASSET_CATEGORIES[0] & { count: number }

export function CategoryOverview({ categories, onSelectCat, onAddAsset, totalAssets }: {
  categories: CatWithCount[]
  onSelectCat: (id: string) => void
  onAddAsset: (catId: string) => void
  totalAssets: number
}) {
  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: 20 }}>
      {/* 标题 */}
      <div style={{ marginBottom: 20 }}>
        <div style={{ fontSize: 20, fontWeight: 700, color: MGMT.white, marginBottom: 4 }}>
          素材库
        </div>
        <div style={{ fontSize: 12, color: MGMT.grayLight }}>
          {totalAssets} 个素材 · {categories.length} 个分类 · 点击分类查看详情
        </div>
      </div>

      {/* 分类卡片网格 */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: 12,
      }}>
        {categories.map(cat => (
          <div key={cat.id}
            onClick={() => onSelectCat(cat.id)}
            style={{
              padding: 16, borderRadius: 12, cursor: 'pointer',
              background: `${cat.color}08`,
              border: `1px solid ${cat.color}25`,
              transition: 'all 0.2s',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.background = `${cat.color}15`
              e.currentTarget.style.borderColor = `${cat.color}50`
              e.currentTarget.style.transform = 'translateY(-2px)'
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = `${cat.color}08`
              e.currentTarget.style.borderColor = `${cat.color}25`
              e.currentTarget.style.transform = 'translateY(0)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
              <div style={{
                width: 40, height: 40, borderRadius: 10,
                background: `${cat.color}15`, display: 'flex',
                alignItems: 'center', justifyContent: 'center',
              }}>
                <AssetCatIcon catId={cat.id} size={20} style={{ color: cat.color }} />
              </div>
              <div>
                <div style={{ fontSize: 14, fontWeight: 700, color: MGMT.white }}>{cat.name}</div>
                <div style={{ fontSize: 10, color: MGMT.grayLight }}>{cat.count} 个素材</div>
              </div>
            </div>
            <div style={{ fontSize: 11, color: MGMT.dimWhite, lineHeight: 1.4 }}>
              {cat.description}
            </div>
            {/* 快速新增 */}
            <div style={{ marginTop: 10, display: 'flex', gap: 6 }}>
              <span onClick={e => { e.stopPropagation(); onAddAsset(cat.id) }}
                style={{
                  fontSize: 9, padding: '2px 6px', borderRadius: 3,
                  background: `${cat.color}15`, color: cat.color,
                  cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 2,
                }}>
                <IconPlus size={8} /> 新增
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
