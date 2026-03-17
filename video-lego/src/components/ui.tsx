// ═══════════════════════════════════════════════════════════
// 共享 UI 组件 — 管理系统通用原子组件
// Shared UI Components — Reusable atoms for the management UI
// ═══════════════════════════════════════════════════════════

import { useState, type ReactNode, type CSSProperties, type FC } from 'react'
import { MGMT } from '@/theme'

// ─────────── 卡片 Card ───────────

export const Card: FC<{
  children: ReactNode
  onClick?: () => void
  accentColor?: string
  style?: CSSProperties
}> = ({ children, onClick, accentColor, style }) => {
  const [hovered, setHovered] = useState(false)

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: hovered ? MGMT.bgCardHover : MGMT.bgCard,
        borderRadius: MGMT.radius.lg,
        border: `1px solid ${hovered ? MGMT.borderHover : MGMT.border}`,
        overflow: 'hidden',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all 0.2s',
        transform: hovered && onClick ? 'translateY(-2px)' : 'none',
        boxShadow: hovered && onClick ? '0 8px 24px rgba(0,0,0,0.2)' : 'none',
        ...(accentColor ? { borderTop: `3px solid ${accentColor}` } : {}),
        ...style,
      }}
    >
      {children}
    </div>
  )
}

// ─────────── 状态徽章 Badge ───────────

export const Badge: FC<{
  status: string
  size?: 'sm' | 'md'
}> = ({ status, size = 'md' }) => {
  const color = MGMT.statusColors[status] || MGMT.gray
  const labels: Record<string, string> = {
    ready: '✅ READY',
    todo: '⬜ TODO',
    in_progress: '🔄 进行中',
    review: '🔍 评审',
    rework: '⚠️ 重做',
    completed: '✅ 完成',
    pending: '⬜ 待定',
    skipped: '⏭ 跳过',
  }

  return (
    <span
      style={{
        fontSize: size === 'sm' ? MGMT.fontSize.tiny : MGMT.fontSize.small,
        fontWeight: 700,
        padding: size === 'sm' ? '2px 6px' : '3px 10px',
        borderRadius: 5,
        background: `${color}18`,
        color,
        letterSpacing: 0.5,
        whiteSpace: 'nowrap',
      }}
    >
      {labels[status] || status}
    </span>
  )
}

// ─────────── 搜索框 SearchBar ───────────

export const SearchBar: FC<{
  value: string
  onChange: (val: string) => void
  placeholder?: string
}> = ({ value, onChange, placeholder = '🔍 搜索...' }) => {
  const [focused, setFocused] = useState(false)

  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      placeholder={placeholder}
      style={{
        width: 240,
        background: MGMT.bgInput,
        border: `1px solid ${focused ? MGMT.gold : MGMT.border}`,
        borderRadius: MGMT.radius.md,
        padding: '9px 14px',
        color: MGMT.white,
        fontSize: MGMT.fontSize.body,
        fontFamily: MGMT.fontFamily,
        outline: 'none',
        transition: 'border-color 0.2s',
      }}
    />
  )
}

// ─────────── 筛选胶囊 FilterPills ───────────

export const FilterPills: FC<{
  options: { key: string; label: string }[]
  active: string
  onChange: (key: string) => void
}> = ({ options, active, onChange }) => (
  <div style={{ display: 'flex', gap: 4 }}>
    {options.map((opt) => {
      const isActive = opt.key === active
      return (
        <button
          key={opt.key}
          onClick={() => onChange(opt.key)}
          style={{
            background: isActive ? `${MGMT.gold}0F` : MGMT.bgInput,
            border: `1px solid ${isActive ? MGMT.gold : MGMT.border}`,
            borderRadius: MGMT.radius.sm,
            padding: '7px 14px',
            color: isActive ? MGMT.gold : MGMT.dimWhite,
            fontSize: MGMT.fontSize.small,
            fontFamily: MGMT.fontFamily,
            cursor: 'pointer',
            transition: 'all 0.15s',
            whiteSpace: 'nowrap',
          }}
        >
          {opt.label}
        </button>
      )
    })}
  </div>
)

// ─────────── 进度条 ProgressBar ───────────

export const ProgressBar: FC<{
  value: number
  color?: string
  height?: number
}> = ({ value, color = MGMT.green, height = 6 }) => (
  <div style={{ width: '100%', height, background: MGMT.border, borderRadius: height / 2, overflow: 'hidden' }}>
    <div
      style={{
        width: `${Math.min(100, Math.max(0, value))}%`,
        height: '100%',
        background: color,
        borderRadius: height / 2,
        transition: 'width 0.3s ease',
      }}
    />
  </div>
)

// ─────────── 流水线状态节点 StatusNode ───────────

export const StatusNode: FC<{
  label: string
  status: string
  onClick?: () => void
  isActive?: boolean
}> = ({ label, status, onClick, isActive }) => {
  const color = MGMT.statusColors[status] || MGMT.gray
  const [hovered, setHovered] = useState(false)

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, cursor: onClick ? 'pointer' : 'default' }}
    >
      <div
        style={{
          width: 48, height: 48, borderRadius: 12,
          background: `${color}20`,
          border: `2px solid ${isActive ? color : `${color}60`}`,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 20, transition: 'all 0.2s',
          transform: hovered ? 'scale(1.1)' : 'scale(1)',
        }}
      >
        {status === 'completed' ? '✅' : status === 'in_progress' ? '🔄' : status === 'skipped' ? '⏭' : '⬜'}
      </div>
      <span style={{ fontSize: MGMT.fontSize.tiny, color: isActive ? MGMT.white : MGMT.dimWhite, fontWeight: isActive ? 600 : 400, textAlign: 'center', maxWidth: 72 }}>
        {label}
      </span>
    </div>
  )
}

// ─────────── 星级评分 StarRating ───────────

export const StarRating: FC<{
  label: string
  value: number
  max?: number
}> = ({ label, value, max = 2 }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
    <span style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, width: 72 }}>{label}</span>
    <div style={{ flex: 1, height: 6, background: MGMT.border, borderRadius: 3 }}>
      <div style={{ width: `${(value / max) * 100}%`, height: '100%', background: value >= max * 0.7 ? MGMT.green : value >= max * 0.4 ? MGMT.orange : MGMT.red, borderRadius: 3 }} />
    </div>
    <span style={{ fontSize: MGMT.fontSize.small, fontWeight: 700, color: MGMT.white, fontFamily: MGMT.codeFontFamily, width: 24, textAlign: 'right' }}>{value}</span>
  </div>
)
