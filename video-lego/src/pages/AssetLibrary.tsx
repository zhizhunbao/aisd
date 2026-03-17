// ═══════════════════════════════════════════════════════════
// 素材库页面 — 分类侧栏 + 子分类 + 来源展示
// AssetLibrary — Category sidebar + sub-categories + sources
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { Card, SearchBar, FilterPills } from '@/components/ui'
import { useNav } from '@/App'
import { ASSET_CATEGORIES, type AssetCategory, getCategoryMeta, getSubCategoryName } from '@/lib/asset-types'
import { DEMO_ASSETS } from '@/data/demo-assets'
import { AssetPreview } from '@/components/AssetPreview'

// ─────────── 来源类型图标 ───────────

const SOURCE_ICONS: Record<string, string> = {
  textbook: '📕', paper: '📄', wikipedia: '🌐',
  documentation: '📋', course: '🎓', original: '✍️',
}

export function AssetLibrary() {
  const { navigate } = useNav()
  const [activeCat, setActiveCat] = useState<'all' | AssetCategory>('all')
  const [activeSubCat, setActiveSubCat] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [courseFilter, setCourseFilter] = useState('all')

  // 筛选
  let filtered = activeCat === 'all' ? DEMO_ASSETS : DEMO_ASSETS.filter(a => a.category === activeCat)
  if (activeSubCat) filtered = filtered.filter(a => a.subCategory === activeSubCat)
  if (courseFilter !== 'all') filtered = filtered.filter(a => a.course === courseFilter)
  if (search) {
    const q = search.toLowerCase()
    filtered = filtered.filter(a =>
      a.name.toLowerCase().includes(q) ||
      a.tags.some(t => t.toLowerCase().includes(q)) ||
      a.sources.some(s => s.cite.toLowerCase().includes(q) || s.title.toLowerCase().includes(q))
    )
  }

  const allCourses = [...new Set(DEMO_ASSETS.map(a => a.course).filter(Boolean))] as string[]
  const activeCatMeta = activeCat !== 'all' ? getCategoryMeta(activeCat) : null

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      {/* ── 分类侧栏 ── */}
      <div style={{ width: 210, minWidth: 210, borderRight: `1px solid ${MGMT.border}`, padding: `${MGMT.sp.md}px ${MGMT.sp.sm}px`, overflowY: 'auto' }}>
        <div style={{ fontSize: MGMT.fontSize.tiny, textTransform: 'uppercase', letterSpacing: 2, color: MGMT.gray, padding: '8px 12px', fontWeight: 600 }}>
          素材分类
        </div>

        <CatNavItem icon="📦" name="全部" count={DEMO_ASSETS.length}
          color={MGMT.gold} isActive={activeCat === 'all'}
          onClick={() => { setActiveCat('all'); setActiveSubCat(null) }} />

        {ASSET_CATEGORIES.map(cat => {
          const count = DEMO_ASSETS.filter(a => a.category === cat.id).length
          const isOpen = activeCat === cat.id
          return (
            <div key={cat.id}>
              <CatNavItem icon={cat.icon} name={cat.name}
                count={count} color={cat.color}
                isActive={isOpen}
                onClick={() => { setActiveCat(cat.id); setActiveSubCat(null) }} />
              {/* 子分类展开 */}
              {isOpen && cat.subCategories.length > 0 && (
                <div style={{ paddingLeft: 18, marginBottom: 4 }}>
                  {cat.subCategories.map(sub => {
                    const subCount = DEMO_ASSETS.filter(a => a.category === cat.id && a.subCategory === sub.id).length
                    if (subCount === 0) return null
                    return (
                      <div key={sub.id}
                        onClick={() => setActiveSubCat(activeSubCat === sub.id ? null : sub.id)}
                        style={{
                          fontSize: MGMT.fontSize.tiny, padding: '5px 10px',
                          borderRadius: MGMT.radius.sm, cursor: 'pointer', marginBottom: 1,
                          color: activeSubCat === sub.id ? cat.color : MGMT.dimWhite,
                          background: activeSubCat === sub.id ? `${cat.color}0A` : 'transparent',
                          fontWeight: activeSubCat === sub.id ? 600 : 400,
                          transition: 'all 0.15s',
                        }}>
                        {sub.name} <span style={{ color: MGMT.grayLight, marginLeft: 4 }}>{subCount}</span>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* ── 主区域 ── */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* 工具栏 */}
        <div style={{ padding: `${MGMT.sp.md}px ${MGMT.sp.lg}px`, borderBottom: `1px solid ${MGMT.border}`, display: 'flex', alignItems: 'center', gap: MGMT.sp.md }}>
          <h2 style={{ fontSize: MGMT.fontSize.h2, fontWeight: 700, flex: 1 }}>
            {activeCat === 'all' ? '📦 素材库' : `${activeCatMeta?.icon} ${activeCatMeta?.name}素材`}
            {activeSubCat && activeCatMeta && (
              <span style={{ fontSize: MGMT.fontSize.small, color: activeCatMeta.color, fontWeight: 500, marginLeft: 8 }}>
                · {getSubCategoryName(activeCat, activeSubCat)}
              </span>
            )}
            <span style={{ fontSize: MGMT.fontSize.small, color: MGMT.grayLight, fontWeight: 400, marginLeft: 12 }}>
              {filtered.length} 项
            </span>
          </h2>
          <SearchBar value={search} onChange={setSearch} placeholder="🔍 搜索素材 / 来源..." />
          <FilterPills
            options={[{ key: 'all', label: '全部' }, ...allCourses.map(c => ({ key: c, label: c }))]}
            active={courseFilter}
            onChange={setCourseFilter}
          />
        </div>

        {/* 卡片网格 */}
        <div style={{ flex: 1, overflowY: 'auto', padding: MGMT.sp.lg }}>
          {filtered.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 80, color: MGMT.grayLight }}>
              <div style={{ fontSize: 48, marginBottom: 12 }}>🔍</div>
              <div style={{ fontSize: MGMT.fontSize.body }}>没有匹配的素材</div>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: MGMT.sp.md }}>
              {filtered.map(asset => {
                const catMeta = getCategoryMeta(asset.category)
                return (
                  <Card key={asset.id} accentColor={catMeta?.color}
                    onClick={() => navigate({ page: 'asset-detail', assetId: asset.id })}>

                    {/* 预览区 */}
                    <div style={{
                      height: 180, overflow: 'hidden',
                      background: 'linear-gradient(180deg, rgba(26,26,46,0.9), rgba(15,15,30,0.95))',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      borderBottom: `1px solid ${MGMT.border}`, position: 'relative',
                    }}>
                      <AssetPreview asset={asset} />
                      {/* 分类 + 子分类角标 */}
                      <div style={{ position: 'absolute', top: 8, right: 8, display: 'flex', gap: 4 }}>
                        {asset.subCategory && catMeta && (
                          <span style={{
                            fontSize: 10, padding: '2px 6px', borderRadius: 3,
                            background: `${catMeta.color}10`, color: catMeta.color, fontWeight: 500,
                          }}>
                            {getSubCategoryName(asset.category, asset.subCategory)}
                          </span>
                        )}
                        <span style={{
                          fontSize: MGMT.fontSize.tiny, padding: '2px 8px', borderRadius: 4, fontWeight: 600,
                          background: `${catMeta?.color || MGMT.gray}15`, color: catMeta?.color || MGMT.gray,
                        }}>
                          {catMeta?.icon} {catMeta?.name}
                        </span>
                      </div>
                    </div>

                    {/* 信息区 */}
                    <div style={{ padding: `${MGMT.sp.md}px ${MGMT.sp.lg}px` }}>
                      <div style={{ fontSize: 16, fontWeight: 600, marginBottom: MGMT.sp.xs }}>{asset.name}</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: MGMT.sp.sm }}>
                        {asset.tags.slice(0, 4).map(tag => (
                          <span key={tag} style={{
                            fontSize: 11, padding: '1px 6px', borderRadius: 3,
                            background: `${MGMT.white}08`, color: MGMT.dimWhite,
                          }}>
                            {tag}
                          </span>
                        ))}
                      </div>
                      {/* 来源引用 */}
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: MGMT.fontSize.tiny, color: MGMT.gray }}>
                        <span style={{ display: 'flex', gap: 4, flexWrap: 'wrap', flex: 1 }}>
                          {asset.sources.slice(0, 2).map((s, i) => (
                            <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              {SOURCE_ICONS[s.type] || '📎'} {s.cite}
                            </span>
                          ))}
                          {asset.sources.length > 2 && <span>+{asset.sources.length - 2}</span>}
                        </span>
                        {asset.compatibleBlocks && (
                          <span style={{ color: MGMT.dimWhite, whiteSpace: 'nowrap' }}>
                            🧱 {asset.compatibleBlocks.length}
                          </span>
                        )}
                      </div>
                    </div>
                  </Card>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─────────── 分类导航项 ───────────

function CatNavItem({ icon, name, count, color, isActive, onClick }: {
  icon: string; name: string; count: number; color: string; isActive: boolean; onClick: () => void
}) {
  return (
    <div onClick={onClick} style={{
      display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px',
      borderRadius: MGMT.radius.sm, cursor: 'pointer', marginBottom: 2,
      background: isActive ? `${color}0A` : 'transparent',
      border: `1px solid ${isActive ? `${color}22` : 'transparent'}`,
      transition: 'all 0.15s',
    }}>
      <span style={{ fontSize: 18 }}>{icon}</span>
      <span style={{ fontSize: MGMT.fontSize.small, fontWeight: isActive ? 600 : 400, color: isActive ? color : MGMT.white, flex: 1 }}>{name}</span>
      <span style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.grayLight, background: `${MGMT.white}08`, padding: '1px 6px', borderRadius: 8 }}>{count}</span>
    </div>
  )
}
