// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 左侧积木列表面板
// Block Editor — Left Panel: Block List with categories
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { BLOCK_CATEGORIES, type BlockMeta } from '@blocks/catalog'
import { IconSearch, IconChevronDown, IconChevronRight, IconPlus } from '@/components/Icons'

interface BlockListProps {
  selectedBlock: string | null
  onSelect: (name: string) => void
  onCreate: () => void
}

export function BlockList({ selectedBlock, onSelect, onCreate }: BlockListProps) {
  const [search, setSearch] = useState('')
  const [expandedCats, setExpandedCats] = useState<Set<string>>(
    new Set(BLOCK_CATEGORIES.map(c => c.id)),
  )

  const toggleCat = (id: string) => {
    setExpandedCats(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id); else next.add(id)
      return next
    })
  }

  const q = search.toLowerCase()

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* 搜索 + 新建 */}
      <div style={{ padding: 12, borderBottom: `1px solid ${MGMT.border}` }}>
        <div style={{ display: 'flex', gap: 6, marginBottom: 8 }}>
          <div style={{
            flex: 1, display: 'flex', alignItems: 'center', gap: 6,
            background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
            borderRadius: 6, padding: '6px 10px',
          }}>
            <IconSearch size={13} style={{ color: MGMT.grayLight, flexShrink: 0 }} />
            <input value={search} onChange={e => setSearch(e.target.value)}
              placeholder="搜索积木..."
              style={{
                background: 'transparent', border: 'none', color: MGMT.white,
                fontFamily: MGMT.fontFamily, fontSize: 12, outline: 'none', width: '100%',
              }}
            />
          </div>
        </div>
        <button onClick={onCreate}
          style={{
            width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
            background: `${MGMT.gold}12`, border: `1px solid ${MGMT.gold}30`,
            borderRadius: 6, padding: '8px 12px', cursor: 'pointer',
            color: MGMT.gold, fontSize: 12, fontWeight: 600, fontFamily: MGMT.fontFamily,
            transition: 'all 0.15s',
          }}
          onMouseEnter={e => { e.currentTarget.style.background = `${MGMT.gold}20` }}
          onMouseLeave={e => { e.currentTarget.style.background = `${MGMT.gold}12` }}
        >
          <IconPlus size={14} /> 新建积木
        </button>
      </div>

      {/* 分类列表 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '8px 0' }}>
        {BLOCK_CATEGORIES.map(cat => {
          const expanded = expandedCats.has(cat.id)
          const blocks = q
            ? cat.blocks.filter(b => b.name.toLowerCase().includes(q) || b.description.toLowerCase().includes(q))
            : cat.blocks
          if (q && blocks.length === 0) return null

          return (
            <div key={cat.id} style={{ marginBottom: 4 }}>
              {/* 分类标题 */}
              <div onClick={() => toggleCat(cat.id)} style={{
                display: 'flex', alignItems: 'center', gap: 6,
                padding: '8px 12px', cursor: 'pointer',
                transition: 'background 0.1s',
              }}
                onMouseEnter={e => (e.currentTarget.style.background = `${MGMT.white}04`)}
                onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
              >
                {expanded
                  ? <IconChevronDown size={13} style={{ color: MGMT.grayLight }} />
                  : <IconChevronRight size={13} style={{ color: MGMT.grayLight }} />}
                <span style={{ fontSize: 14 }}>{cat.icon}</span>
                <span style={{ fontSize: 12, fontWeight: 600, color: cat.color, flex: 1 }}>
                  {cat.name}
                </span>
                <span style={{ fontSize: 10, color: MGMT.grayLight }}>
                  {cat.blocks.filter(b => b.status === 'ready').length}/{cat.blocks.length}
                </span>
              </div>

              {/* 积木项 */}
              {expanded && blocks.map(block => (
                <BlockItem
                  key={block.name}
                  block={block}
                  catColor={cat.color}
                  isSelected={selectedBlock === block.name}
                  onSelect={() => onSelect(block.name)}
                />
              ))}
            </div>
          )
        })}
      </div>

      {/* 底部统计 */}
      <div style={{
        padding: '10px 12px', borderTop: `1px solid ${MGMT.border}`,
        fontSize: 10, color: MGMT.grayLight, display: 'flex', justifyContent: 'space-between',
      }}>
        <span>
          {BLOCK_CATEGORIES.flatMap(c => c.blocks).filter(b => b.status === 'ready').length} 已实现
        </span>
        <span>
          {BLOCK_CATEGORIES.flatMap(c => c.blocks).length} 总计
        </span>
      </div>
    </div>
  )
}

// ─── 积木列表项 ───

function BlockItem({ block, catColor, isSelected, onSelect }: {
  block: BlockMeta; catColor: string; isSelected: boolean; onSelect: () => void
}) {
  const isReady = block.status === 'ready'
  return (
    <div onClick={onSelect}
      style={{
        display: 'flex', alignItems: 'center', gap: 8,
        padding: '7px 12px 7px 32px', cursor: 'pointer',
        borderLeft: `3px solid ${isSelected ? MGMT.gold : 'transparent'}`,
        background: isSelected ? `${MGMT.gold}08` : 'transparent',
        opacity: isReady ? 1 : 0.5,
        transition: 'all 0.1s',
      }}
      onMouseEnter={e => { if (!isSelected) e.currentTarget.style.background = `${MGMT.white}04` }}
      onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = 'transparent' }}
    >
      <span style={{
        width: 7, height: 7, borderRadius: '50%',
        background: isReady ? catColor : `${catColor}40`, flexShrink: 0,
      }} />
      <span style={{
        fontSize: 12, flex: 1, fontWeight: isSelected ? 600 : 400,
        color: isSelected ? MGMT.gold : (isReady ? MGMT.white : MGMT.grayLight),
        fontFamily: MGMT.codeFontFamily,
      }}>
        {block.name}
      </span>
      {block.rating && (
        <span style={{ fontSize: 10, color: MGMT.gold, fontWeight: 600 }}>
          ★{block.rating.total}
        </span>
      )}
      {!isReady && (
        <span style={{
          fontSize: 9, color: MGMT.grayLight, padding: '1px 5px',
          borderRadius: 3, background: `${MGMT.white}06`,
        }}>TODO</span>
      )}
    </div>
  )
}
