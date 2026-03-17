// ═══════════════════════════════════════════════════════════
// 场景编排器 — 右侧编辑面板
// Scene Composer — Right Panel: Edit Panel
// ═══════════════════════════════════════════════════════════

import React, { useState, useCallback } from 'react'
import { MGMT } from '@/theme'
import { BLOCK_CATEGORIES, getBlockMeta } from '@blocks/catalog'
import { IconProperties, IconPalette } from '@/components/Icons'
import type { SceneData } from '@/lib/types'
import { LAYOUT_OPTIONS, blockLabel, catLabel } from './constants'
import { SectionLabel, InputField } from './shared'

export function EditPanel({ scene, selBlock, onChange, onSelectBlock }: {
  scene: SceneData; selBlock: number
  onChange: (s: SceneData) => void; onSelectBlock: (i: number) => void
}) {
  const [tab, setTab] = useState<'props' | 'blocks'>('props')

  const addBlock = useCallback((name: string) => {
    onChange({ ...scene, visuals: [...scene.visuals, { block: name, data: {} } as SceneData['visuals'][number]] })
    onSelectBlock(scene.visuals.length)
  }, [scene, onChange, onSelectBlock])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Tab 切换 */}
      <div style={{ display: 'flex', borderBottom: `1px solid ${MGMT.border}` }}>
        {(['props', 'blocks'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            flex: 1, padding: 12, fontSize: 13, cursor: 'pointer',
            fontWeight: tab === t ? 700 : 400,
            color: tab === t ? MGMT.gold : MGMT.grayLight,
            background: tab === t ? `${MGMT.gold}08` : 'transparent',
            borderBottom: `2px solid ${tab === t ? MGMT.gold : 'transparent'}`,
            border: 'none', fontFamily: MGMT.fontFamily,
            transition: 'all 0.15s',
          }}>
            {t === 'props'
              ? <><IconProperties size={13} style={{ marginRight: 4, verticalAlign: 'middle' }} /> 属性</>
              : <><IconPalette size={13} style={{ marginRight: 4, verticalAlign: 'middle' }} /> 积木</>}
          </button>
        ))}
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {tab === 'props'
          ? <PropertiesTab scene={scene} selBlock={selBlock} onChange={onChange} onSelectBlock={onSelectBlock} />
          : <BlocksPaletteTab onAdd={addBlock} />}
      </div>
    </div>
  )
}

// ─── 属性 Tab ───

function PropertiesTab({ scene, selBlock, onChange, onSelectBlock }: {
  scene: SceneData; selBlock: number
  onChange: (s: SceneData) => void; onSelectBlock: (i: number) => void
}) {
  return (
    <>
      <SectionLabel>场景信息</SectionLabel>
      <InputField label="标题" value={scene.title} onChange={v => onChange({ ...scene, title: v })} />
      <InputField label="子标题" value={scene.subtitle || ''} onChange={v => onChange({ ...scene, subtitle: v || undefined })} placeholder="可选" />

      <SectionLabel>布局</SectionLabel>
      <div style={{ display: 'flex', gap: 6, marginBottom: 16 }}>
        {LAYOUT_OPTIONS.map(opt => (
          <button key={opt.value}
            onClick={() => onChange({ ...scene, layout: opt.value })}
            style={{
              flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4,
              borderRadius: 8, padding: '10px 8px', fontSize: 12, fontWeight: 600,
              background: scene.layout === opt.value ? `${MGMT.gold}14` : `${MGMT.white}05`,
              border: `1px solid ${scene.layout === opt.value ? `${MGMT.gold}40` : MGMT.border}`,
              color: scene.layout === opt.value ? MGMT.gold : MGMT.grayLight,
              cursor: 'pointer', fontFamily: MGMT.fontFamily, transition: 'all 0.15s',
            }}
          >
            <span style={{ fontSize: 18 }}>{opt.icon}</span>
            {opt.label}
          </button>
        ))}
      </div>

      {/* 已有积木列表 */}
      <SectionLabel>场景积木 ({scene.visuals.length})</SectionLabel>
      {scene.visuals.map((v, vi) => {
        const meta = getBlockMeta(v.block)
        const catColor = meta?.category?.color || '#888'
        const active = selBlock === vi
        return (
          <div key={vi}
            onClick={() => onSelectBlock(vi)}
            style={{
              display: 'flex', alignItems: 'center', gap: 8,
              padding: '8px 10px', borderRadius: 6, cursor: 'pointer', marginBottom: 2,
              borderLeft: `3px solid ${active ? MGMT.gold : `${catColor}30`}`,
              background: active ? `${MGMT.gold}08` : 'transparent',
              transition: 'all 0.1s',
            }}
            onMouseEnter={e => { if (!active) e.currentTarget.style.background = `${MGMT.white}04` }}
            onMouseLeave={e => { if (!active) e.currentTarget.style.background = 'transparent' }}
          >
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: catColor, flexShrink: 0 }} />
            <span style={{
              fontSize: 12, flex: 1,
              color: active ? MGMT.gold : MGMT.dimWhite,
              fontWeight: active ? 600 : 400,
            }}>{blockLabel(v.block)}</span>
            <button onClick={e => { e.stopPropagation(); onChange({ ...scene, visuals: scene.visuals.filter((_, i) => i !== vi) }) }}
              style={{
                background: 'none', border: 'none', color: `${MGMT.red}80`,
                cursor: 'pointer', fontSize: 14, padding: '0 2px',
              }}>×</button>
          </div>
        )
      })}
      {scene.visuals.length === 0 && (
        <div style={{
          fontSize: 12, color: MGMT.grayLight, textAlign: 'center',
          padding: 20, border: `1px dashed ${MGMT.border}`, borderRadius: 8,
        }}>
          右键画布添加积木<br />或切换到「积木」面板
        </div>
      )}

      {/* 要点 */}
      {scene.points.length > 0 && (
        <>
          <SectionLabel>要点 ({scene.points.length})</SectionLabel>
          {scene.points.map((pt, pi) => (
            <div key={pi} style={{
              fontSize: 12, color: MGMT.dimWhite, padding: '4px 8px',
              borderRadius: 4, marginBottom: 2, background: `${MGMT.white}03`,
            }}>
              {pt.icon && <span style={{ marginRight: 4 }}>{pt.icon}</span>}{pt.text}
            </div>
          ))}
        </>
      )}

      {/* 结论 */}
      {scene.conclusion && (
        <>
          <SectionLabel>结论</SectionLabel>
          <div style={{
            fontSize: 12, color: MGMT.gold, padding: '8px 10px',
            borderRadius: 6, background: `${MGMT.gold}08`, border: `1px solid ${MGMT.gold}20`,
          }}>
            {scene.conclusion.icon && <span style={{ marginRight: 4 }}>{scene.conclusion.icon}</span>}{scene.conclusion.text}
          </div>
        </>
      )}
    </>
  )
}

// ─── 积木面板 Tab ───

function BlocksPaletteTab({ onAdd }: { onAdd: (name: string) => void }) {
  return (
    <>
      {BLOCK_CATEGORIES.map(cat => (
        <div key={cat.id} style={{ marginBottom: 16 }}>
          <div style={{
            fontSize: 12, fontWeight: 700, color: cat.color, marginBottom: 8,
            display: 'flex', alignItems: 'center', gap: 6,
          }}>
            <span style={{ fontSize: 14 }}>{cat.icon}</span>
            {catLabel(cat.name)}
            <span style={{ fontSize: 10, color: MGMT.grayLight, fontWeight: 400 }}>
              {cat.blocks.filter(b => b.status === 'ready').length}/{cat.blocks.length}
            </span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 6 }}>
            {cat.blocks.map(block => {
              const ready = block.status === 'ready'
              return (
                <div key={block.name}
                  draggable={ready}
                  onDragStart={e => { e.dataTransfer.setData('block-name', block.name); e.dataTransfer.effectAllowed = 'copy' }}
                  onClick={() => ready && onAdd(block.name)}
                  title={block.description}
                  style={{
                    padding: '8px 10px', borderRadius: 6,
                    background: `${cat.color}08`, border: `1px solid ${cat.color}15`,
                    cursor: ready ? 'pointer' : 'default', opacity: ready ? 1 : 0.4,
                    transition: 'all 0.15s',
                  }}
                  onMouseEnter={e => { if (ready) { e.currentTarget.style.background = `${cat.color}18`; e.currentTarget.style.borderColor = `${cat.color}40` } }}
                  onMouseLeave={e => { e.currentTarget.style.background = `${cat.color}08`; e.currentTarget.style.borderColor = `${cat.color}15` }}
                >
                  <div style={{ fontSize: 11, fontWeight: 600, color: ready ? MGMT.white : MGMT.grayLight }}>
                    {blockLabel(block.name)}
                  </div>
                  <div style={{ fontSize: 9, color: MGMT.grayLight, marginTop: 3, display: 'flex', alignItems: 'center', gap: 4 }}>
                    {ready ? (
                      <>
                        <span style={{ color: MGMT.green }}>●</span> 就绪
                        {block.rating && <span style={{ marginLeft: 'auto', color: MGMT.gold }}>★{block.rating.total}</span>}
                      </>
                    ) : (<><span>○</span> 待实现</>)}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </>
  )
}
