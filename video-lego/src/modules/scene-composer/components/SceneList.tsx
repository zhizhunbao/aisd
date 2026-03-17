// ═══════════════════════════════════════════════════════════
// 场景编排器 — 左侧场景列表
// Scene Composer — Left Panel: Scene List with Act grouping
// ═══════════════════════════════════════════════════════════

import React, { useState, useMemo } from 'react'
import { MGMT } from '@/theme'
import type { SceneData } from '@/lib/types'
import { getActColor } from './constants'
import { SmallBtn } from './shared'

export function SceneList({ scenes, sel, onSelect, onMove, onDelete, onAdd }: {
  scenes: SceneData[]; sel: number
  onSelect: (i: number) => void; onMove: (i: number, d: -1 | 1) => void
  onDelete: (i: number) => void; onAdd: () => void
}) {
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({})
  const [dragIdx, setDragIdx] = useState<number | null>(null)
  const [dragOver, setDragOver] = useState<number | null>(null)

  const groups = useMemo(() => {
    const m = new Map<string, { act: string; color: string; scenes: { idx: number; scene: SceneData }[] }>()
    scenes.forEach((sc, idx) => {
      const act = sc.act || '未分组'
      if (!m.has(act)) m.set(act, { act, color: getActColor(act), scenes: [] })
      m.get(act)!.scenes.push({ idx, scene: sc })
    })
    return [...m.values()]
  }, [scenes])

  return (
    <>
      <div style={{ flex: 1, overflowY: 'auto', padding: 8 }}>
        {groups.map(group => {
          const isCollapsed = collapsed[group.act]
          return (
            <div key={group.act} style={{ marginBottom: 4 }}>
              {/* Act 标题 */}
              <div
                onClick={() => setCollapsed(p => ({ ...p, [group.act]: !p[group.act] }))}
                style={{
                  display: 'flex', alignItems: 'center', gap: 8,
                  padding: '8px 10px', borderRadius: 6, cursor: 'pointer',
                  transition: 'background 0.1s',
                }}
                onMouseEnter={e => (e.currentTarget.style.background = `${MGMT.white}05`)}
                onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
              >
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: group.color, flexShrink: 0 }} />
                <span style={{ fontSize: 11, fontWeight: 700, color: group.color, flex: 1, letterSpacing: 0.5, textTransform: 'uppercase' as const }}>
                  {group.act}
                </span>
                <span style={{ fontSize: 10, color: MGMT.grayLight }}>{group.scenes.length}</span>
                <span style={{
                  fontSize: 10, color: MGMT.grayLight,
                  display: 'inline-block', transition: 'transform 0.2s',
                  transform: isCollapsed ? 'rotate(-90deg)' : 'none',
                }}>▾</span>
              </div>

              {/* 场景列表 */}
              {!isCollapsed && group.scenes.map(({ idx, scene: sc }) => {
                const active = sel === idx
                const isDragging = dragIdx === idx
                const isDragTarget = dragOver === idx
                return (
                  <div
                    key={idx}
                    draggable
                    onDragStart={() => setDragIdx(idx)}
                    onDragOver={e => { e.preventDefault(); setDragOver(idx) }}
                    onDragLeave={() => setDragOver(null)}
                    onDrop={() => {
                      if (dragIdx !== null && dragIdx !== idx) onMove(dragIdx, idx > dragIdx ? 1 : -1)
                      setDragIdx(null); setDragOver(null)
                    }}
                    onDragEnd={() => { setDragIdx(null); setDragOver(null) }}
                    onClick={() => onSelect(idx)}
                    style={{
                      padding: '8px 10px 8px 26px', borderRadius: 6, cursor: 'grab',
                      marginBottom: 1, transition: 'all 0.15s',
                      borderLeft: `3px solid ${active ? MGMT.gold : isDragTarget ? `${MGMT.blue}50` : 'transparent'}`,
                      background: active ? `${MGMT.gold}0a` : isDragTarget ? `${MGMT.blue}08` : 'transparent',
                      opacity: isDragging ? 0.5 : 1,
                    }}
                    onMouseEnter={e => { if (!active && !isDragTarget) e.currentTarget.style.background = `${MGMT.white}04` }}
                    onMouseLeave={e => { if (!active && !isDragTarget) e.currentTarget.style.background = 'transparent' }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{
                        fontSize: 10, fontWeight: 800,
                        width: 22, height: 22, borderRadius: '50%',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
                        background: active ? MGMT.gold : `${MGMT.white}0f`,
                        color: active ? '#0a0a14' : MGMT.dimWhite,
                      }}>{idx + 1}</span>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{
                          fontSize: 13, fontWeight: active ? 700 : 500,
                          color: active ? MGMT.gold : MGMT.white,
                          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' as const,
                          lineHeight: 1.3,
                        }}>{sc.title || '(无标题)'}</div>
                        <div style={{
                          fontSize: 10, color: MGMT.grayLight, marginTop: 2,
                          display: 'flex', alignItems: 'center', gap: 6,
                        }}>
                          <span>{sc.visuals.length} 积木</span>
                          <span style={{ color: MGMT.border }}>·</span>
                          <span>{sc.layout}</span>
                        </div>
                      </div>
                    </div>
                    {active && (
                      <div style={{ display: 'flex', gap: 4, marginTop: 6, paddingLeft: 30 }}>
                        <SmallBtn color={MGMT.blue} disabled={idx === 0}
                          onClick={e => { e.stopPropagation(); onMove(idx, -1) }}>↑</SmallBtn>
                        <SmallBtn color={MGMT.blue} disabled={idx === scenes.length - 1}
                          onClick={e => { e.stopPropagation(); onMove(idx, 1) }}>↓</SmallBtn>
                        <SmallBtn color={MGMT.red}
                          onClick={e => { e.stopPropagation(); onDelete(idx) }}>删除</SmallBtn>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )
        })}
      </div>

      {/* 添加场景按钮 */}
      <div style={{ padding: 8, borderTop: `1px solid ${MGMT.border}` }}>
        <button onClick={onAdd} style={{
          width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
          background: `${MGMT.green}15`, border: `1px solid ${MGMT.green}30`,
          color: MGMT.green, borderRadius: 8, padding: '10px 14px',
          fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: MGMT.fontFamily,
          transition: 'all 0.15s',
        }}
        onMouseEnter={e => (e.currentTarget.style.background = `${MGMT.green}25`)}
        onMouseLeave={e => (e.currentTarget.style.background = `${MGMT.green}15`)}
        >+ 添加场景</button>
      </div>
    </>
  )
}
