// ═══════════════════════════════════════════════════════════
// 场景编排器 — 共享原子组件 (inline style + MGMT theme)
// Scene Composer — Shared atomic UI components
// ═══════════════════════════════════════════════════════════

import React from 'react'
import { MGMT } from '@/theme'

export function SmallBtn({ color, disabled, onClick, children }: {
  color: string; disabled?: boolean; onClick: (e: React.MouseEvent) => void
  children: React.ReactNode
}) {
  return (
    <button disabled={disabled} onClick={onClick} style={{
      background: `${color}12`, border: `1px solid ${color}30`, color,
      borderRadius: 4, cursor: disabled ? 'default' : 'pointer',
      padding: '3px 8px', fontSize: 11, fontWeight: 600,
      opacity: disabled ? 0.3 : 1, fontFamily: MGMT.fontFamily,
      transition: 'all 0.15s',
    }}>{children}</button>
  )
}

export function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      fontSize: 11, color: MGMT.grayLight, fontWeight: 700,
      letterSpacing: 0.5, marginBottom: 8, marginTop: 16,
      textTransform: 'uppercase',
    }}>{children}</div>
  )
}

export function InputField({ label, value, onChange, placeholder }: {
  label: string; value: string; onChange: (v: string) => void; placeholder?: string
}) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 4 }}>{label}</div>
      <input value={value} onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 6, padding: '8px 10px', color: MGMT.white,
          fontFamily: MGMT.fontFamily, fontSize: 13, width: '100%',
          outline: 'none', boxSizing: 'border-box',
          transition: 'border 0.15s',
        }}
        onFocus={e => (e.currentTarget.style.borderColor = `${MGMT.gold}40`)}
        onBlur={e => (e.currentTarget.style.borderColor = MGMT.border)}
      />
    </div>
  )
}

export function DividerHandle({ side, draggingRef }: {
  side: 'left' | 'right'
  draggingRef: React.MutableRefObject<'left' | 'right' | null>
}) {
  return (
    <div
      onMouseDown={() => { draggingRef.current = side; document.body.style.cursor = 'col-resize' }}
      style={{
        width: 5, cursor: 'col-resize', background: 'transparent',
        flexShrink: 0, position: 'relative', zIndex: 10,
      }}
      onMouseEnter={e => (e.currentTarget.style.background = `${MGMT.gold}30`)}
      onMouseLeave={e => { if (!draggingRef.current) e.currentTarget.style.background = 'transparent' }}
    />
  )
}
