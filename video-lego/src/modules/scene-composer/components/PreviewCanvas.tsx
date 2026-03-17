// ═══════════════════════════════════════════════════════════
// 场景编排器 — 中间画布预览
// Scene Composer — Center Panel: Preview Canvas
// ═══════════════════════════════════════════════════════════

import React, { useState, useCallback } from 'react'
import { MGMT } from '@/theme'
import type { SceneData } from '@/lib/types'
import { IconPlus, IconGrip, IconPin } from '@/components/Icons'
import { BlockPreview } from '../BlockPreview'
import { ContextMenu, type ContextMenuState } from './ContextMenu'
import { BlockPickerModal } from './BlockPickerModal'
import { LAYOUT_OPTIONS, blockLabel, getActColor } from './constants'

export function PreviewCanvas({ scene, selBlock, onSelectBlock, onChangeScene }: {
  scene: SceneData; selBlock: number; onSelectBlock: (i: number) => void
  onChangeScene: (s: SceneData) => void
}) {
  const [ctxMenu, setCtxMenu] = useState<ContextMenuState | null>(null)
  const [showPicker, setShowPicker] = useState(false)
  const [pickerTarget, setPickerTarget] = useState<{ mode: 'add' | 'replace'; slotIndex: number }>({ mode: 'add', slotIndex: 0 })
  const [dragBlockIdx, setDragBlockIdx] = useState<number | null>(null)
  const [dragOverIdx, setDragOverIdx] = useState<number | null>(null)
  const [zoom, setZoom] = useState(1)

  const isPortrait = scene.layout === 'portrait'
  const hasVisuals = scene.visuals.length > 0

  const handleWheel = useCallback((e: React.WheelEvent) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault()
      setZoom((z: number) => Math.min(2, Math.max(0.3, z - e.deltaY * 0.001)))
    }
  }, [])

  const handleContextAction = (action: string) => {
    const bi = ctxMenu!.slotIndex
    switch (action) {
      case 'add':
        setPickerTarget({ mode: 'add', slotIndex: bi }); setShowPicker(true); break
      case 'replace':
        setPickerTarget({ mode: 'replace', slotIndex: bi }); setShowPicker(true); break
      case 'duplicate':
        if (bi < scene.visuals.length) {
          const vs = [...scene.visuals]; vs.splice(bi + 1, 0, JSON.parse(JSON.stringify(scene.visuals[bi])))
          onChangeScene({ ...scene, visuals: vs })
        }
        break
      case 'move-up':
        if (bi > 0) {
          const vs = [...scene.visuals]; [vs[bi], vs[bi - 1]] = [vs[bi - 1], vs[bi]]
          onChangeScene({ ...scene, visuals: vs }); onSelectBlock(bi - 1)
        }
        break
      case 'move-down':
        if (bi < scene.visuals.length - 1) {
          const vs = [...scene.visuals]; [vs[bi], vs[bi + 1]] = [vs[bi + 1], vs[bi]]
          onChangeScene({ ...scene, visuals: vs }); onSelectBlock(bi + 1)
        }
        break
      case 'delete':
        onChangeScene({ ...scene, visuals: scene.visuals.filter((_, i) => i !== bi) }); break
    }
  }

  const handlePickBlock = (name: string) => {
    const { mode, slotIndex } = pickerTarget
    const vs = [...scene.visuals]
    if (mode === 'add') {
      vs.splice(slotIndex, 0, { block: name, data: {} } as SceneData['visuals'][number])
      onChangeScene({ ...scene, visuals: vs }); onSelectBlock(slotIndex)
    } else {
      vs[slotIndex] = { block: name, data: {} } as SceneData['visuals'][number]
      onChangeScene({ ...scene, visuals: vs })
    }
    setShowPicker(false)
  }

  const handleBlockDrop = (fromIdx: number, toIdx: number) => {
    if (fromIdx === toIdx) return
    const vs = [...scene.visuals]; const [moved] = vs.splice(fromIdx, 1); vs.splice(toIdx, 0, moved)
    onChangeScene({ ...scene, visuals: vs }); onSelectBlock(toIdx)
  }

  return (
    <div style={{ display: 'flex', flex: 1, flexDirection: 'column', background: '#070710' }}>
      {/* 顶部工具栏 */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 10,
        borderBottom: `1px solid ${MGMT.border}`,
        background: `${MGMT.white}02`, padding: '8px 16px',
      }}>
        <input
          value={scene.title}
          onChange={e => onChangeScene({ ...scene, title: e.target.value })}
          style={{
            background: 'transparent', border: 'none', fontSize: 14,
            fontWeight: 700, color: MGMT.white, fontFamily: MGMT.fontFamily,
            outline: 'none', width: 200,
          }}
          placeholder="场景标题"
        />
        <span style={{ color: `${MGMT.white}14`, fontSize: 16 }}>|</span>
        <input
          value={scene.act}
          onChange={e => onChangeScene({ ...scene, act: e.target.value })}
          style={{
            background: 'transparent', border: 'none', fontSize: 12,
            fontWeight: 600, color: getActColor(scene.act), fontFamily: MGMT.fontFamily,
            outline: 'none', width: 120,
          }}
          placeholder="所属幕"
        />
        <div style={{ flex: 1 }} />
        {/* 布局切换 */}
        <div style={{ display: 'flex', gap: 2, background: `${MGMT.white}06`, borderRadius: 6, padding: 2 }}>
          {LAYOUT_OPTIONS.map(opt => (
            <button
              key={opt.value}
              onClick={() => onChangeScene({ ...scene, layout: opt.value })}
              title={opt.label}
              style={{
                borderRadius: 4, padding: '4px 10px', fontSize: 14,
                background: scene.layout === opt.value ? `${MGMT.gold}20` : 'transparent',
                border: scene.layout === opt.value ? `1px solid ${MGMT.gold}40` : '1px solid transparent',
                color: scene.layout === opt.value ? MGMT.gold : MGMT.grayLight,
                cursor: 'pointer', transition: 'all 0.15s',
              }}
            >{opt.icon}</button>
          ))}
        </div>
        <span style={{ fontSize: 12, color: MGMT.grayLight }}>{scene.visuals.length} 积木</span>
      </div>

      {/* 画布 */}
      <div style={{
        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
        overflow: 'auto', padding: 16,
      }} onWheel={handleWheel}>
        <div
          data-canvas-root
          onContextMenu={e => {
            e.preventDefault()
            const slotIdx = (e.target as HTMLElement).closest('[data-block-slot]') ? -1 : scene.visuals.length
            if (slotIdx >= 0) setCtxMenu({ x: e.clientX, y: e.clientY, blockIndex: slotIdx, slotIndex: slotIdx, hasBlock: false })
          }}
          style={{
            width: 960 * zoom, aspectRatio: '16 / 9',
            borderRadius: 10, border: `1px solid ${MGMT.border}`,
            background: '#0d1117', overflow: 'hidden',
            display: 'flex', flexDirection: 'column',
            position: 'relative', flexShrink: 0,
            transition: 'width 0.2s',
          }}
        >
          {/* 标题 */}
          <div style={{
            flexShrink: 0, padding: `${16 * zoom}px ${24 * zoom}px ${8 * zoom}px`,
            background: 'linear-gradient(180deg, rgba(0,0,0,0.5) 0%, transparent 100%)',
          }}>
            <div style={{
              fontSize: 20 * zoom, fontWeight: 800,
              color: scene.titleColor || MGMT.white, fontFamily: MGMT.fontFamily,
            }}>{scene.title || '(无标题)'}</div>
            {scene.subtitle && (
              <div style={{ fontSize: 13 * zoom, color: MGMT.dimWhite, marginTop: 4 * zoom }}>{scene.subtitle}</div>
            )}
          </div>

          {/* 积木区域 */}
          <div style={{
            display: 'flex', flex: 1, minHeight: 0, padding: '0 8px',
            flexDirection: isPortrait ? 'column' : 'row',
          }}>
            {hasVisuals ? scene.visuals.map((v, si) => {
              const isSelected = selBlock === si
              const isDragTarget = dragOverIdx === si
              const isDragging = dragBlockIdx === si
              return (
                <div
                  key={si}
                  data-block-slot
                  draggable
                  onDragStart={e => { setDragBlockIdx(si); e.dataTransfer.effectAllowed = 'move' }}
                  onDragOver={e => { e.preventDefault(); setDragOverIdx(si) }}
                  onDragLeave={() => setDragOverIdx(null)}
                  onDrop={e => { e.preventDefault(); if (dragBlockIdx !== null) handleBlockDrop(dragBlockIdx, si); setDragBlockIdx(null); setDragOverIdx(null) }}
                  onDragEnd={() => { setDragBlockIdx(null); setDragOverIdx(null) }}
                  onClick={() => onSelectBlock(si)}
                  onContextMenu={e => {
                    e.preventDefault(); e.stopPropagation()
                    setCtxMenu({ x: e.clientX, y: e.clientY, blockIndex: si, slotIndex: si, hasBlock: true })
                  }}
                  style={{
                    flex: 1, cursor: 'grab', position: 'relative',
                    minHeight: 0, minWidth: 0, overflow: 'hidden',
                    borderRadius: 6, margin: 2,
                    outline: isSelected ? `2px solid ${MGMT.gold}` : isDragTarget ? `2px dashed ${MGMT.blue}` : 'none',
                    outlineOffset: -2, opacity: isDragging ? 0.5 : 1,
                    transition: 'all 0.15s',
                  }}
                >
                  <BlockPreview blockName={v.block} data={v.data} />
                  <div style={{
                    position: 'absolute', bottom: 4, left: 4,
                    fontSize: 10, padding: '2px 8px', borderRadius: 4,
                    fontWeight: 600, display: 'flex', alignItems: 'center', gap: 4,
                    background: isSelected ? MGMT.gold : 'rgba(0,0,0,0.7)',
                    color: isSelected ? '#0a0a14' : MGMT.grayLight,
                  }}>
                    <IconGrip size={10} style={{ opacity: 0.6 }} />
                    {blockLabel(v.block)}
                  </div>
                </div>
              )
            }) : (
              <div style={{
                flex: 1, display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center', gap: 8,
                color: MGMT.grayLight,
              }}>
                <IconPlus size={28} style={{ opacity: 0.3 }} />
                <span style={{ opacity: 0.5, fontSize: 12 }}>右键添加积木</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 底部工具栏 */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 8,
        borderTop: `1px solid ${MGMT.border}`,
        background: `${MGMT.white}02`, padding: '6px 16px',
        fontSize: 11, color: MGMT.grayLight,
      }}>
        <IconPin size={12} />
        <span>场景预览</span>
        <div style={{ flex: 1 }} />
        <button onClick={() => setZoom(z => Math.min(2, z + 0.1))} style={{
          color: MGMT.grayLight, fontSize: 14, padding: '2px 4px', cursor: 'pointer',
          background: 'none', border: 'none',
        }}>+</button>
        <span style={{ fontSize: 10, minWidth: 40, textAlign: 'center' as const }}>{Math.round(zoom * 100)}%</span>
        <button onClick={() => setZoom(z => Math.max(0.3, z - 0.1))} style={{
          color: MGMT.grayLight, fontSize: 14, padding: '2px 4px', cursor: 'pointer',
          background: 'none', border: 'none',
        }}>–</button>
        <button onClick={() => setZoom(1)} style={{
          fontSize: 10, color: MGMT.grayLight, border: `1px solid ${MGMT.border}`,
          borderRadius: 4, padding: '2px 8px', cursor: 'pointer', background: 'none',
        }}>重置</button>
      </div>

      {ctxMenu && <ContextMenu state={ctxMenu} onClose={() => setCtxMenu(null)} onAction={handleContextAction} />}
      {showPicker && <BlockPickerModal onSelect={handlePickBlock} onClose={() => setShowPicker(false)} />}
    </div>
  )
}
