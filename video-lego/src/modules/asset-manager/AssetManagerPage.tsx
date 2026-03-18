// ═══════════════════════════════════════════════════════════
// M0 素材管理器 — 主入口（重构后）
// Asset Manager — Main entry (refactored)
//
// 浏览模式: 左栏 + 中栏（概览/列表），2 栏
// 详情模式: 左栏 + 中栏（大预览）+ 右栏（编辑），3 栏
// ═══════════════════════════════════════════════════════════

import { useState, useMemo, useCallback, useEffect } from 'react'
import { MGMT } from '@/theme'
import { ModuleLayout, ModuleHeader } from '@/components/ModuleLayout'
import { ASSET_CATEGORIES, getCategoryMeta } from '@/lib/asset-types'
import { DEMO_ASSETS } from '@/data/demo-assets'
import { DATA_VERSION } from '@/data/assets'
import { AssetCatIcon } from '@/components/AssetIcons'
import { IconSearch, IconPackage } from '@/components/Icons'
import type { Asset } from '@/lib/asset-types'

import {
  type ViewMode, type SortField, type SortDir,
  LS_KEY, loadAssets, saveAssets,
  SidebarItem, MiniBtn,
} from './shared'
import { CategoryOverview } from './CategoryOverview'
import { AssetListView } from './AssetListView'
import { AssetPreviewPanel, AssetEditSidebar } from './AssetDetailView'

const COLOR = '#6c7a89'

// ═══════════════════════════════════════════════════════════
// 主组件
// ═══════════════════════════════════════════════════════════

export function AssetManagerPage() {
  const [assets, setAssets] = useState<Asset[]>(() => loadAssets(DEMO_ASSETS, DATA_VERSION))
  const [activeCatId, setActiveCatId] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [viewMode, setViewMode] = useState<ViewMode>('grid')
  const [sortField, setSortField] = useState<SortField>('none')
  const [sortDir, setSortDir] = useState<SortDir>('asc')

  // 详情页状态
  const [detailAsset, setDetailAsset] = useState<Asset | null>(null)
  const [editDraft, setEditDraft] = useState<Partial<Asset>>({})
  const [isDirty, setIsDirty] = useState(false)

  // 持久化
  useEffect(() => { saveAssets(assets) }, [assets])

  // ─── 分类统计 ───
  const catsWithAssets = useMemo(() =>
    ASSET_CATEGORIES.map(cat => ({
      ...cat,
      count: assets.filter(a => a.category === cat.id).length,
    })),
    [assets]
  )

  // ─── 筛选 + 排序 ───
  const filtered = useMemo(() => {
    let items = assets
    if (activeCatId) items = items.filter(a => a.category === activeCatId)
    if (search) {
      const q = search.toLowerCase()
      items = items.filter(a =>
        a.name.toLowerCase().includes(q) ||
        a.tags.some(t => t.toLowerCase().includes(q))
      )
    }
    if (sortField !== 'none') {
      items = [...items].sort((a, b) => {
        const va = a[sortField] || ''
        const vb = b[sortField] || ''
        const cmp = va < vb ? -1 : va > vb ? 1 : 0
        return sortDir === 'asc' ? cmp : -cmp
      })
    }
    return items
  }, [assets, activeCatId, search, sortField, sortDir])

  // ─── 进入详情 ───
  function openDetail(asset: Asset) {
    setDetailAsset(asset)
    setEditDraft({ ...asset, tags: [...asset.tags] })
    setIsDirty(false)
  }

  function closeDetail() {
    setDetailAsset(null)
    setEditDraft({})
    setIsDirty(false)
  }

  // ─── CRUD 操作 ───
  const updateDraft = useCallback((field: string, value: any) => {
    setEditDraft(prev => ({ ...prev, [field]: value }))
    setIsDirty(true)
  }, [])

  const saveDraft = useCallback(() => {
    if (!detailAsset || !editDraft.name) return
    const updated = { ...detailAsset, ...editDraft, updatedAt: new Date().toISOString().split('T')[0] } as Asset
    setAssets(prev => prev.map(a => a.id === updated.id ? updated : a))
    setDetailAsset(updated)
    setIsDirty(false)
  }, [detailAsset, editDraft])

  const deleteAsset = useCallback((id: string) => {
    if (!confirm('确定删除这个素材？')) return
    setAssets(prev => prev.filter(a => a.id !== id))
    if (detailAsset?.id === id) closeDetail()
  }, [detailAsset])

  const duplicateAsset = useCallback((asset: Asset) => {
    const newAsset: Asset = {
      ...asset,
      id: `${asset.id}-copy-${Date.now()}`,
      name: `${asset.name} (副本)`,
      createdAt: new Date().toISOString().split('T')[0],
    }
    setAssets(prev => [...prev, newAsset])
  }, [])

  const addNewAsset = useCallback((catId: string) => {
    const cat = getCategoryMeta(catId)
    const newAsset: Asset = {
      id: `new-${Date.now()}`,
      name: `新${cat?.name || '素材'}`,
      category: catId,
      tags: [],
      atomType: catId === 'person' ? 'person_card' : catId === 'code' ? 'code_snippet' : 'formula',
      sources: [],
      createdAt: new Date().toISOString().split('T')[0],
      content: catId === 'person'
        ? { category: 'person', data: { name: '新人物' } }
        : { category: 'text_overlay', data: { overlayType: catId === 'code' ? 'code' : 'formula', text: '' } } as any,
    }
    setAssets(prev => [...prev, newAsset])
    setActiveCatId(catId)
    openDetail(newAsset)
  }, [])

  const resetToDefaults = useCallback(() => {
    if (!confirm('重置为默认素材？你的修改将丢失。')) return
    localStorage.removeItem(LS_KEY)
    const defaults = [...DEMO_ASSETS]
    setAssets(defaults)
    closeDetail()
  }, [])

  // ═══════════════════════════════════════════════════════════
  // 左栏 — 分类导航（通用，两种模式下均显示）
  // ═══════════════════════════════════════════════════════════

  const leftPanel = (
    <>
      <ModuleHeader
        icon={<IconPackage size={16} />}
        title="M0 素材管理器"
        subtitle={`${assets.length} 个素材 · ${ASSET_CATEGORIES.length} 分类`}
        color={COLOR}
      />

      {/* 搜索 */}
      <div style={{ padding: '6px 10px', borderBottom: `1px solid ${MGMT.border}` }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 6,
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 5, padding: '5px 8px',
        }}>
          <IconSearch size={12} style={{ color: MGMT.grayLight, flexShrink: 0 }} />
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="搜索素材..."
            style={{
              background: 'transparent', border: 'none', color: MGMT.white,
              fontFamily: MGMT.fontFamily, fontSize: 11, outline: 'none', width: '100%',
            }}
          />
        </div>
      </div>

      {/* 分类列表 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '6px' }}>
        <SidebarItem
          label="全部素材" count={assets.length}
          icon={<IconPackage size={14} />}
          color={MGMT.gold}
          isActive={!activeCatId}
          onClick={() => { setActiveCatId(null); closeDetail() }}
        />

        {catsWithAssets.map(cat => {
          const isOpen = activeCatId === cat.id
          return (
            <div key={cat.id}>
              <SidebarItem
                label={cat.name} count={cat.count}
                icon={<AssetCatIcon catId={cat.id} size={14} style={{ color: cat.color }} />}
                color={cat.color}
                isActive={isOpen}
                onClick={() => {
                  setActiveCatId(isOpen ? null : cat.id)
                  closeDetail()
                }}
              />
              {/* 子分类展开 */}
              {isOpen && cat.subCategories && cat.subCategories.length > 0 && (
                <div style={{ paddingLeft: 14, marginBottom: 2 }}>
                  {cat.subCategories.map(sub => {
                    const subCount = assets.filter(a => a.category === cat.id && a.subCategory === sub.id).length
                    if (subCount === 0) return null
                    return (
                      <div key={sub.id}
                        style={{
                          fontSize: 11, padding: '4px 8px', borderRadius: 4,
                          cursor: 'pointer', marginBottom: 1,
                          color: MGMT.dimWhite,
                          background: 'transparent',
                          display: 'flex', alignItems: 'center', gap: 6,
                          transition: 'all 0.1s',
                        }}
                        onMouseEnter={e => e.currentTarget.style.background = `${MGMT.white}06`}
                        onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                      >
                        <span style={{ width: 4, height: 4, borderRadius: 2, background: `${cat.color}60`, flexShrink: 0 }} />
                        <span style={{ flex: 1 }}>{sub.name}</span>
                        <span style={{ fontSize: 9, color: MGMT.grayLight }}>{subCount}</span>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* 底部操作 */}
      <div style={{ padding: '6px 10px', borderTop: `1px solid ${MGMT.border}`, display: 'flex', gap: 4 }}>
        <MiniBtn label="重置" onClick={resetToDefaults} color={MGMT.grayLight} />
      </div>
    </>
  )

  // ═══════════════════════════════════════════════════════════
  // 渲染
  // ═══════════════════════════════════════════════════════════

  // 详情模式 → 三栏 (左 + 预览 + 编辑)
  if (detailAsset) {
    return (
      <ModuleLayout
        left={leftPanel}
        center={
          <AssetPreviewPanel
            asset={detailAsset}
            draft={editDraft}
            onBack={closeDetail}
          />
        }
        right={
          <AssetEditSidebar
            asset={detailAsset}
            draft={editDraft}
            isDirty={isDirty}
            onUpdate={updateDraft}
            onSave={saveDraft}
            onDelete={() => deleteAsset(detailAsset.id)}
            onDuplicate={() => duplicateAsset(detailAsset)}
          />
        }
        defaultLeftWidth={200}
        defaultRightWidth={280}
      />
    )
  }

  // 浏览模式 → 两栏 (左 + 概览/列表)
  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', overflow: 'hidden' }}>
      <div style={{
        width: 200, minWidth: 200, maxWidth: 200,
        borderRight: `1px solid ${MGMT.border}`,
        display: 'flex', flexDirection: 'column',
        background: MGMT.bgSidebar,
      }}>
        {leftPanel}
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {activeCatId ? (
          <AssetListView
            assets={filtered} activeCatId={activeCatId}
            selectedId={null}
            viewMode={viewMode} sortField={sortField} sortDir={sortDir}
            onSelect={openDetail}
            onDelete={deleteAsset}
            onDuplicate={duplicateAsset}
            onViewMode={setViewMode}
            onSort={(f) => {
              if (f === sortField) setSortDir(d => d === 'asc' ? 'desc' : 'asc')
              else { setSortField(f); setSortDir('asc') }
            }}
            onAdd={() => addNewAsset(activeCatId)}
          />
        ) : (
          <CategoryOverview
            categories={catsWithAssets}
            onSelectCat={setActiveCatId}
            onAddAsset={addNewAsset}
            totalAssets={assets.length}
          />
        )}
      </div>
    </div>
  )
}
