// ═══════════════════════════════════════════════════════════
// 素材列表视图 — 网格 + 表格 + 子分类分组
// AssetListView — Grid & table with sub-category grouping
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { getCategoryMeta, getSubCategoryName } from '@/lib/asset-types'
import { AssetCatIcon } from '@/components/AssetIcons'
import { AssetPreview } from '@/components/AssetPreview'
import { IconSearch, IconPlus, IconCopy, IconTrash } from '@/components/Icons'
import type { Asset } from '@/lib/asset-types'
import {
  type ViewMode, type SortField, type SortDir,
  SortBtn, ViewBtn, CardAction, getPreviewText,
} from './shared'

// ═══════════════════════════════════════════════════════════
// 主列表视图
// ═══════════════════════════════════════════════════════════

export function AssetListView({ assets, activeCatId, selectedId, viewMode, sortField, sortDir,
  onSelect, onDelete, onDuplicate, onViewMode, onSort, onAdd }: {
  assets: Asset[]; activeCatId: string; selectedId: string | null
  viewMode: ViewMode; sortField: SortField; sortDir: SortDir
  onSelect: (a: Asset) => void; onDelete: (id: string) => void; onDuplicate: (a: Asset) => void
  onViewMode: (m: ViewMode) => void; onSort: (f: SortField) => void; onAdd: () => void
}) {
  const catMeta = getCategoryMeta(activeCatId)
  const accent = catMeta?.color || MGMT.gold

  // 按 subCategory 分组，按 ASSET_CATEGORIES 定义顺序排列
  function groupBySubCat() {
    // 获取该分类的子分类定义顺序
    const subOrder = catMeta?.subCategories.map(s => s.id) || []

    const subGroups: { subId: string; subName: string; items: Asset[] }[] = []
    const seen = new Set<string>()
    for (const a of assets) {
      const sid = a.subCategory || '_none'
      if (!seen.has(sid)) {
        seen.add(sid)
        subGroups.push({
          subId: sid,
          subName: sid === '_none' ? '未分类' : getSubCategoryName(activeCatId, sid),
          items: assets.filter(x => (x.subCategory || '_none') === sid),
        })
      }
    }
    // 按定义顺序排序
    subGroups.sort((a, b) => {
      const ia = subOrder.indexOf(a.subId)
      const ib = subOrder.indexOf(b.subId)
      return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib)
    })
    return subGroups
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* 工具栏 */}
      <div style={{
        padding: '8px 14px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 8,
      }}>
        <AssetCatIcon catId={activeCatId} size={14} style={{ color: accent }} />
        <span style={{ fontSize: 13, fontWeight: 700, color: accent }}>{catMeta?.name}</span>
        <span style={{ fontSize: 10, color: MGMT.grayLight }}>{assets.length} 项</span>

        <div style={{ flex: 1 }} />

        {/* 排序 */}
        <SortBtn label="名称" field="name" current={sortField} dir={sortDir} onClick={onSort} />
        <SortBtn label="日期" field="createdAt" current={sortField} dir={sortDir} onClick={onSort} />

        {/* 视图切换 */}
        <div style={{ display: 'flex', border: `1px solid ${MGMT.border}`, borderRadius: 4, overflow: 'hidden' }}>
          <ViewBtn label="▦" active={viewMode === 'grid'} onClick={() => onViewMode('grid')} />
          <ViewBtn label="☰" active={viewMode === 'list'} onClick={() => onViewMode('list')} />
        </div>

        {/* 新增 */}
        <span onClick={onAdd}
          style={{
            fontSize: 10, padding: '4px 8px', borderRadius: 4,
            background: `${accent}15`, color: accent,
            cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 3,
            fontWeight: 600,
          }}>
          <IconPlus size={10} /> 新增
        </span>
      </div>

      {/* 内容区 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {assets.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 40, color: MGMT.grayLight }}>
            <IconSearch size={28} style={{ opacity: 0.3, marginBottom: 8 }} />
            <div style={{ fontSize: 12 }}>暂无素材</div>
            <span onClick={onAdd}
              style={{
                fontSize: 11, padding: '4px 12px', borderRadius: 4,
                background: `${accent}15`, color: accent,
                cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 3,
                marginTop: 8,
              }}>
              <IconPlus size={10} /> 添加第一个
            </span>
          </div>
        ) : viewMode === 'grid' ? (
          /* 按子分类分组的网格 */
          groupBySubCat().map(g => (
            <div key={g.subId} style={{ marginBottom: 16 }}>
              <div style={{
                display: 'flex', alignItems: 'center', gap: 6,
                padding: '4px 2px', marginBottom: 8,
                borderBottom: `1px solid ${accent}15`,
              }}>
                <span style={{ fontSize: 11, fontWeight: 600, color: accent }}>{g.subName}</span>
                <span style={{ fontSize: 9, color: MGMT.grayLight }}>{g.items.length}</span>
              </div>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
                gap: 10,
              }}>
                {g.items.map(a => (
                  <AssetCard key={a.id} asset={a} isSelected={selectedId === a.id}
                    onClick={() => onSelect(a)}
                    onDelete={() => onDelete(a.id)}
                    onDuplicate={() => onDuplicate(a)}
                  />
                ))}
              </div>
            </div>
          ))
        ) : (
          /* 表格视图 */
          <div>
            {/* 表头 */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 180px 120px 70px 50px',
              gap: 6, padding: '6px 10px', marginBottom: 4,
              borderBottom: `1px solid ${MGMT.border}`,
              fontSize: 9, color: MGMT.grayLight, fontWeight: 600,
              textTransform: 'uppercase', letterSpacing: 0.5,
            }}>
              <span>名称</span>
              <span>预览</span>
              <span>标签</span>
              <span>日期</span>
              <span></span>
            </div>
            {groupBySubCat().map(g => (
              <div key={g.subId} style={{ marginBottom: 12 }}>
                <div style={{
                  fontSize: 10, fontWeight: 600, color: accent,
                  padding: '4px 10px', marginBottom: 2,
                }}>
                  {g.subName} <span style={{ color: MGMT.grayLight, fontWeight: 400 }}>({g.items.length})</span>
                </div>
                {g.items.map(a => (
                  <AssetTableRow key={a.id} asset={a} isSelected={selectedId === a.id}
                    onClick={() => onSelect(a)}
                    onDelete={() => onDelete(a.id)}
                    onDuplicate={() => onDuplicate(a)}
                  />
                ))}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// 素材卡片（网格视图）— 使用 AssetPreview 富预览
// ═══════════════════════════════════════════════════════════

function AssetCard({ asset, isSelected, onClick, onDelete, onDuplicate }: {
  asset: Asset; isSelected: boolean; onClick: () => void
  onDelete: () => void; onDuplicate: () => void
}) {
  const [hovered, setHovered] = useState(false)
  const catMeta = getCategoryMeta(asset.category)
  const accent = catMeta?.color || MGMT.gold

  return (
    <div onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        borderRadius: 10, overflow: 'hidden', cursor: 'pointer',
        background: isSelected ? `${accent}08` : `${MGMT.white}03`,
        border: `1.5px solid ${isSelected ? `${accent}50` : MGMT.border}`,
        transition: 'all 0.15s',
      }}
    >
      {/* 预览区 — 使用 AssetPreview 组件 */}
      <div style={{
        height: 120, overflow: 'hidden',
        background: `linear-gradient(135deg, ${accent}06, ${accent}02)`,
        position: 'relative',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 2, background: accent, opacity: isSelected ? 1 : 0.3 }} />
        <AssetPreview asset={asset} isStatic />
        {/* 操作按钮 */}
        {hovered && (
          <div style={{ position: 'absolute', top: 6, right: 6, display: 'flex', gap: 3 }}>
            <CardAction icon={<IconCopy size={10} />} onClick={e => { e.stopPropagation(); onDuplicate() }} />
            <CardAction icon={<IconTrash size={10} />} onClick={e => { e.stopPropagation(); onDelete() }} danger />
          </div>
        )}
      </div>
      {/* 信息 */}
      <div style={{ padding: '8px 10px' }}>
        <div style={{
          fontSize: 11, fontWeight: isSelected ? 700 : 500,
          color: isSelected ? MGMT.white : MGMT.dimWhite,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          marginBottom: 3,
        }}>{asset.name}</div>
        <div style={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
          {asset.tags.slice(0, 2).map(t => (
            <span key={t} style={{ fontSize: 8, padding: '1px 4px', borderRadius: 2, background: `${MGMT.white}06`, color: MGMT.grayLight }}>{t}</span>
          ))}
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// 表格行（表格视图）
// ═══════════════════════════════════════════════════════════

function AssetTableRow({ asset, isSelected, onClick, onDelete, onDuplicate }: {
  asset: Asset; isSelected: boolean; onClick: () => void
  onDelete: () => void; onDuplicate: () => void
}) {
  const [hovered, setHovered] = useState(false)
  const catMeta = getCategoryMeta(asset.category)
  const accent = catMeta?.color || MGMT.gold
  const preview = getPreviewText(asset)

  return (
    <div onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 180px 120px 70px 50px',
        gap: 6, padding: '7px 10px', borderRadius: 5, marginBottom: 1,
        borderLeft: `3px solid ${isSelected ? accent : 'transparent'}`,
        background: isSelected ? `${accent}08` : hovered ? `${MGMT.white}03` : 'transparent',
        cursor: 'pointer', transition: 'all 0.1s',
        alignItems: 'center',
      }}
    >
      {/* 名称 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, overflow: 'hidden' }}>
        <AssetCatIcon catId={asset.category} size={13} style={{ color: accent, flexShrink: 0 }} />
        <span style={{
          fontSize: 11, fontWeight: isSelected ? 600 : 400,
          color: isSelected ? MGMT.white : MGMT.dimWhite,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{asset.name}</span>
      </div>
      {/* 预览 */}
      <span style={{
        fontSize: 9, color: MGMT.grayLight, fontFamily: MGMT.codeFontFamily,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        opacity: 0.7,
      }}>{preview.slice(0, 40)}</span>
      {/* 标签 */}
      <div style={{ display: 'flex', gap: 2, overflow: 'hidden' }}>
        {asset.tags.slice(0, 2).map(t => (
          <span key={t} style={{ fontSize: 8, padding: '1px 4px', borderRadius: 2, background: `${MGMT.white}06`, color: MGMT.grayLight, whiteSpace: 'nowrap' }}>{t}</span>
        ))}
      </div>
      {/* 日期 */}
      <span style={{ fontSize: 9, color: MGMT.grayLight }}>{asset.createdAt?.slice(5)}</span>
      {/* 操作 */}
      <div style={{ display: 'flex', gap: 2, opacity: hovered ? 1 : 0, transition: 'opacity 0.1s' }}>
        <CardAction icon={<IconCopy size={9} />} onClick={e => { e.stopPropagation(); onDuplicate() }} />
        <CardAction icon={<IconTrash size={9} />} onClick={e => { e.stopPropagation(); onDelete() }} danger />
      </div>
    </div>
  )
}
