// ═══════════════════════════════════════════════════════════
// 场景编排器 — 积木选择弹窗
// Scene Composer — Block Picker Modal
// ═══════════════════════════════════════════════════════════

import React from 'react'
import { MGMT } from '@/theme'
import { BLOCK_CATEGORIES } from '@blocks/catalog'
import { blockLabel, catLabel } from './constants'

export function BlockPickerModal({ onSelect, onClose }: {
  onSelect: (name: string) => void
  onClose: () => void
}) {
  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.5)', display: 'flex',
      alignItems: 'center', justifyContent: 'center', zIndex: 9999,
    }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{
        background: '#151528', borderRadius: 12, border: `1px solid ${MGMT.border}`,
        width: 520, maxHeight: '70vh', overflow: 'hidden',
        boxShadow: '0 20px 60px rgba(0,0,0,0.6)',
      }}>
        <div style={{
          padding: '16px 20px', borderBottom: `1px solid ${MGMT.border}`,
          fontSize: 15, fontWeight: 700, color: MGMT.gold,
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        }}>
          <span>选择积木</span>
          <button onClick={onClose} style={{
            background: 'none', border: 'none', color: MGMT.grayLight,
            fontSize: 18, cursor: 'pointer', padding: '0 4px',
          }}>✕</button>
        </div>
        <div style={{ padding: 16, overflowY: 'auto', maxHeight: 'calc(70vh - 60px)' }}>
          {BLOCK_CATEGORIES.map(cat => (
            <div key={cat.id} style={{ marginBottom: 16 }}>
              <div style={{
                fontSize: 12, fontWeight: 700, color: cat.color,
                marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6,
              }}>
                <span style={{ fontSize: 16 }}>{cat.icon}</span>
                {catLabel(cat.name)}
              </div>
              <div style={{
                display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8,
              }}>
                {cat.blocks.map(block => {
                  const ready = block.status === 'ready'
                  return (
                    <div key={block.name}
                      onClick={() => ready && onSelect(block.name)}
                      title={block.description}
                      style={{
                        padding: '10px 12px', borderRadius: 8, cursor: ready ? 'pointer' : 'default',
                        background: `${cat.color}08`, border: `1px solid ${cat.color}20`,
                        opacity: ready ? 1 : 0.4, transition: 'all 0.15s',
                      }}
                      onMouseEnter={e => {
                        if (ready) {
                          e.currentTarget.style.background = `${cat.color}18`
                          e.currentTarget.style.borderColor = `${cat.color}50`
                          e.currentTarget.style.transform = 'translateY(-1px)'
                        }
                      }}
                      onMouseLeave={e => {
                        e.currentTarget.style.background = `${cat.color}08`
                        e.currentTarget.style.borderColor = `${cat.color}20`
                        e.currentTarget.style.transform = 'none'
                      }}
                    >
                      <div style={{ fontSize: 12, fontWeight: 600, color: ready ? cat.color : MGMT.grayLight }}>
                        {blockLabel(block.name)}
                      </div>
                      <div style={{ fontSize: 10, color: MGMT.grayLight, marginTop: 3 }}>
                        {ready ? '✅ 就绪' : '⏳ 待实现'}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
