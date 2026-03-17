// ═══════════════════════════════════════════════════════════
// 积木目录页 — 分类导航 + 搜索筛选 + 可视化预览卡片
// BlockCatalog — Category nav + search + visual preview cards
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { Card, Badge, SearchBar, FilterPills } from '@/components/ui'
import { BlockPreview } from '@/components/BlockPreview'
import { useNav } from '@/App'
import { BLOCK_CATEGORIES, type BlockMeta } from '@blocks/catalog'

export function BlockCatalog() {
  const { navigate } = useNav()
  const [activeCat, setActiveCat] = useState('all')
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  // 展平所有积木
  const allBlocks: (BlockMeta & { _cat: typeof BLOCK_CATEGORIES[number] })[] = BLOCK_CATEGORIES.flatMap(
    (cat) => cat.blocks.map((b) => ({ ...b, _cat: cat })),
  )

  // 筛选
  let filtered = activeCat === 'all' ? allBlocks : allBlocks.filter((b) => b._cat.id === activeCat)
  if (statusFilter !== 'all') filtered = filtered.filter((b) => b.status === statusFilter)
  if (search) {
    const q = search.toLowerCase()
    filtered = filtered.filter(
      (b) => b.name.toLowerCase().includes(q) || b.description.toLowerCase().includes(q),
    )
  }

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      {/* 分类侧栏 */}
      <div style={{ width: 200, minWidth: 200, borderRight: `1px solid ${MGMT.border}`, padding: `${MGMT.sp.md}px ${MGMT.sp.sm}px`, overflowY: 'auto' }}>
        <div style={{ fontSize: MGMT.fontSize.tiny, textTransform: 'uppercase', letterSpacing: 2, color: MGMT.gray, padding: '8px 12px', fontWeight: 600 }}>
          分类
        </div>

        <NavItem icon="🧱" name="全部" count={`${allBlocks.filter((b) => b.status === 'ready').length}/${allBlocks.length}`}
          color={MGMT.gold} isActive={activeCat === 'all'} onClick={() => setActiveCat('all')} />

        {BLOCK_CATEGORIES.map((cat) => {
          const ready = cat.blocks.filter((b) => b.status === 'ready').length
          return (
            <NavItem key={cat.id} icon={cat.icon} name={cat.name.split(' ')[0]}
              count={`${ready}/${cat.blocks.length}`} color={cat.color}
              isActive={activeCat === cat.id} onClick={() => setActiveCat(cat.id)} />
          )
        })}
      </div>

      {/* 主区域 */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* 工具栏 */}
        <div style={{ padding: `${MGMT.sp.md}px ${MGMT.sp.lg}px`, borderBottom: `1px solid ${MGMT.border}`, display: 'flex', alignItems: 'center', gap: MGMT.sp.md }}>
          <h2 style={{ fontSize: MGMT.fontSize.h2, fontWeight: 700, flex: 1 }}>
            {activeCat === 'all'
              ? '🧱 全部积木'
              : `${BLOCK_CATEGORIES.find((c) => c.id === activeCat)?.icon} ${BLOCK_CATEGORIES.find((c) => c.id === activeCat)?.name}`}
          </h2>
          <SearchBar value={search} onChange={setSearch} placeholder="🔍 搜索积木..." />
          <FilterPills
            options={[
              { key: 'all', label: '全部' },
              { key: 'ready', label: '✅ 完成' },
              { key: 'todo', label: '⬜ TODO' },
            ]}
            active={statusFilter}
            onChange={setStatusFilter}
          />
        </div>

        {/* 卡片网格 */}
        <div style={{ flex: 1, overflowY: 'auto', padding: MGMT.sp.lg }}>
          {filtered.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 80, color: MGMT.grayLight }}>
              <div style={{ fontSize: 48, marginBottom: 12 }}>🔍</div>
              <div style={{ fontSize: MGMT.fontSize.body }}>没有匹配的积木</div>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: MGMT.sp.md }}>
              {filtered.map((block) => (
                <Card key={block.name} accentColor={block._cat.color}
                  onClick={() => navigate({ page: 'block-detail', blockName: block.name })}
                  style={{ opacity: block.status === 'todo' ? 0.55 : 1 }}>

                  {/* ═══ 可视化预览区域 Visual Preview ═══ */}
                  <div style={{
                    height: 200, overflow: 'hidden',
                    background: block.status === 'ready'
                      ? 'linear-gradient(180deg, rgba(26,26,46,0.9), rgba(15,15,30,0.95))'
                      : `${MGMT.bgCard}`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    borderBottom: `1px solid ${MGMT.border}`,
                    position: 'relative',
                  }}>
                    {block.status === 'ready' ? (
                      <div style={{ transform: 'scale(0.75)', transformOrigin: 'center center', width: '100%', display: 'flex', justifyContent: 'center' }}>
                        <BlockPreview blockName={block.name} />
                      </div>
                    ) : (
                      <div style={{ color: MGMT.gray, textAlign: 'center' }}>
                        <div style={{ fontSize: 36, marginBottom: 6, opacity: 0.4 }}>⬜</div>
                        <div style={{ fontSize: MGMT.fontSize.tiny }}>待实现</div>
                      </div>
                    )}
                    {/* 分类角标 */}
                    <span style={{
                      position: 'absolute', top: 8, right: 8,
                      fontSize: MGMT.fontSize.tiny, padding: '2px 8px', borderRadius: 4, fontWeight: 600,
                      background: `${block._cat.color}15`, color: block._cat.color,
                      backdropFilter: 'blur(4px)',
                    }}>
                      {block._cat.icon} {block._cat.name.split(' ')[0]}
                    </span>
                  </div>

                  {/* ═══ 信息区 Info ═══ */}
                  <div style={{ padding: `${MGMT.sp.md}px ${MGMT.sp.lg}px` }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: MGMT.sp.xs }}>
                      <span style={{ fontFamily: MGMT.codeFontFamily, fontSize: 16, fontWeight: 600 }}>{block.name}</span>
                      <Badge status={block.status} size="sm" />
                    </div>
                    <div style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, lineHeight: 1.5, marginBottom: MGMT.sp.sm }}>
                      {block.description}
                    </div>
                    {/* 评分 + 文件路径 */}
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      {block.rating ? (
                        <span style={{ fontSize: MGMT.fontSize.small, color: MGMT.gold, fontWeight: 700 }}>
                          ⭐ {block.rating.total}/10
                        </span>
                      ) : (
                        <span />
                      )}
                      <span style={{ fontFamily: MGMT.codeFontFamily, fontSize: 11, color: MGMT.gray }}>{block.file}</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─────────── 分类导航项 NavItem ───────────

function NavItem({ icon, name, count, color, isActive, onClick }: {
  icon: string; name: string; count: string; color: string; isActive: boolean; onClick: () => void
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
      <span style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.grayLight }}>{count}</span>
    </div>
  )
}
