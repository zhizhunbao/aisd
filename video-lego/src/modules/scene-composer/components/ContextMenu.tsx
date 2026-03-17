// ═══════════════════════════════════════════════════════════
// 场景编排器 — 右键菜单
// Scene Composer — Context Menu
// ═══════════════════════════════════════════════════════════

import React, { useRef, useEffect } from 'react'
import { MGMT } from '@/theme'
import {
  IconReplace, IconCopy, IconArrowUp, IconArrowDown, IconTrash, IconPlus,
} from '@/components/Icons'

export interface ContextMenuState {
  x: number
  y: number
  blockIndex: number
  slotIndex: number
  hasBlock: boolean
}

export function ContextMenu({ state, onClose, onAction }: {
  state: ContextMenuState
  onClose: () => void
  onAction: (action: string) => void
}) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handle = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose()
    }
    document.addEventListener('mousedown', handle)
    return () => document.removeEventListener('mousedown', handle)
  }, [onClose])

  const items: { id: string; label: string; color: string; icon?: React.ReactNode }[] = state.hasBlock
    ? [
        { id: 'add', label: '添加积木', color: MGMT.green, icon: <IconPlus size={14} /> },
        { id: 'replace', label: '替换积木', color: MGMT.blue, icon: <IconReplace size={14} /> },
        { id: 'duplicate', label: '复制积木', color: MGMT.green, icon: <IconCopy size={14} /> },
        { id: 'move-up', label: '上移', color: MGMT.dimWhite, icon: <IconArrowUp size={14} /> },
        { id: 'move-down', label: '下移', color: MGMT.dimWhite, icon: <IconArrowDown size={14} /> },
        { id: 'divider', label: '', color: '' },
        { id: 'delete', label: '删除积木', color: MGMT.red, icon: <IconTrash size={14} /> },
      ]
    : [
        { id: 'add', label: '添加积木到此位置', color: MGMT.green, icon: <IconPlus size={14} /> },
      ]

  return (
    <div ref={ref} style={{
      position: 'fixed', left: state.x, top: state.y, zIndex: 10000,
      background: '#1a1a35', border: `1px solid ${MGMT.border}`,
      borderRadius: 8, padding: 4, minWidth: 180,
      boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
      backdropFilter: 'blur(12px)',
    }}>
      {items.map((item, i) => {
        if (item.id === 'divider') {
          return <div key={i} style={{ height: 1, background: MGMT.border, margin: '4px 8px' }} />
        }
        return (
          <div key={item.id}
            onClick={() => { onAction(item.id); onClose() }}
            style={{
              padding: '8px 12px', borderRadius: 6, cursor: 'pointer',
              fontSize: 13, color: item.color,
              transition: 'background 0.1s',
            }}
            onMouseEnter={e => (e.currentTarget.style.background = `${MGMT.white}08`)}
            onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              {item.icon}
              {item.label}
            </span>
          </div>
        )
      })}
    </div>
  )
}
