// ═══════════════════════════════════════════════════════════
// 素材管理器 — 共享组件 + 工具函数
// Asset Manager — Shared components & utilities
// ═══════════════════════════════════════════════════════════

import React, { useState } from 'react'
import { MGMT } from '@/theme'
import { AssetCatIcon } from '@/components/AssetIcons'
import {
  IconArrowUp, IconArrowDown,
  IconCopy, IconTrash,
} from '@/components/Icons'
import type { Asset } from '@/lib/asset-types'

// ─── 类型 ───

export type ViewMode = 'grid' | 'list'
export type SortField = 'name' | 'createdAt' | 'none'
export type SortDir = 'asc' | 'desc'

// ─── localStorage 持久化 ───

export const LS_KEY = 'video-lego-assets'
const LS_VER_KEY = 'video-lego-assets-ver'

export function loadAssets(defaults: Asset[], version?: number): Asset[] {
  try {
    // 版本检测: 数据更新后自动清旧缓存
    if (version) {
      const savedVer = Number(localStorage.getItem(LS_VER_KEY) || '0')
      if (savedVer < version) {
        localStorage.removeItem(LS_KEY)
        localStorage.setItem(LS_VER_KEY, String(version))
        return [...defaults]
      }
    }
    const raw = localStorage.getItem(LS_KEY)
    return raw ? JSON.parse(raw) : [...defaults]
  } catch { return [...defaults] }
}

export function saveAssets(assets: Asset[]) {
  localStorage.setItem(LS_KEY, JSON.stringify(assets))
}

// ─── 素材预览文本 ───

export function getPreviewText(asset: Asset): string {
  const d = asset.content?.data as any
  if (!d) return ''
  if (d.latex) return d.latex
  if (d.overlayType === 'code' && d.text) return d.text.split('\n').slice(0, 3).join('\n')
  if (d.audioType) return `${d.audioType.toUpperCase()} · ${d.durationSec || '?'}s`
  if (d.events) return d.events.map((e: any) => `${e.year} ${e.text}`).slice(0, 3).join(' → ')
  if (d.rows) return d.rows.map((r: any) => `${r.key}: ${r.value}`).slice(0, 2).join(', ')
  if (d.citation) return d.citation
  if (d.description) return d.description
  if (d.title) return d.title
  return ''
}

// ─── SidebarItem ───

export function SidebarItem({ label, count, icon, color, isActive, onClick }: {
  label: string; count: number; icon: React.ReactNode; color: string
  isActive: boolean; onClick: () => void
}) {
  return (
    <div onClick={onClick}
      style={{
        padding: '8px 10px', borderRadius: 6, marginBottom: 2,
        background: isActive ? `${color}12` : 'transparent',
        border: `1px solid ${isActive ? `${color}35` : 'transparent'}`,
        cursor: 'pointer', transition: 'all 0.15s',
        display: 'flex', alignItems: 'center', gap: 8,
      }}
      onMouseEnter={e => { if (!isActive) e.currentTarget.style.background = `${MGMT.white}04` }}
      onMouseLeave={e => { if (!isActive) e.currentTarget.style.background = isActive ? `${color}12` : 'transparent' }}
    >
      {icon}
      <span style={{
        fontSize: 12, fontWeight: isActive ? 700 : 500,
        color: isActive ? MGMT.white : MGMT.dimWhite, flex: 1,
      }}>{label}</span>
      <span style={{
        fontSize: 9, color: isActive ? color : MGMT.grayLight,
        fontWeight: isActive ? 600 : 400,
      }}>{count}</span>
    </div>
  )
}

// ─── 排序按钮 ───

export function SortBtn({ label, field, current, dir, onClick }: {
  label: string; field: SortField; current: SortField; dir: SortDir; onClick: (f: SortField) => void
}) {
  const isActive = current === field
  return (
    <span onClick={() => onClick(field)} style={{
      fontSize: 10, padding: '3px 6px', borderRadius: 3, cursor: 'pointer',
      background: isActive ? `${MGMT.white}10` : 'transparent',
      color: isActive ? MGMT.white : MGMT.grayLight,
      display: 'flex', alignItems: 'center', gap: 2,
    }}>
      {label}
      {isActive && (dir === 'asc' ? <IconArrowUp size={8} /> : <IconArrowDown size={8} />)}
    </span>
  )
}

// ─── 视图切换按钮 ───

export function ViewBtn({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <span onClick={onClick} style={{
      fontSize: 11, padding: '3px 6px', cursor: 'pointer',
      background: active ? `${MGMT.white}10` : 'transparent',
      color: active ? MGMT.white : MGMT.grayLight,
    }}>{label}</span>
  )
}

// ─── 卡片操作按钮 ───

export function CardAction({ icon, onClick, danger }: {
  icon: React.ReactNode; onClick: (e: React.MouseEvent) => void; danger?: boolean
}) {
  return (
    <span onClick={onClick} style={{
      padding: 3, borderRadius: 3, cursor: 'pointer',
      background: danger ? 'rgba(231,76,60,0.2)' : `${MGMT.white}10`,
      color: danger ? '#e74c3c' : MGMT.dimWhite,
      display: 'flex', alignItems: 'center',
    }}>{icon}</span>
  )
}

// ─── 编辑面板辅助组件 ───

export function EditInput({ label, value, accent, onChange, style }: {
  label: string; value: string; accent?: string
  onChange: (v: string) => void; style?: React.CSSProperties
}) {
  return (
    <div style={style}>
      <FieldLabel>{label}</FieldLabel>
      <input value={value} onChange={e => onChange(e.target.value)}
        style={{
          width: '100%', padding: '6px 8px', borderRadius: 4,
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          color: MGMT.white, fontSize: 11, fontFamily: MGMT.fontFamily,
          outline: 'none', transition: 'border-color 0.15s',
          boxSizing: 'border-box',
        }}
        onFocus={e => e.currentTarget.style.borderColor = accent || MGMT.borderHover}
        onBlur={e => e.currentTarget.style.borderColor = MGMT.border}
      />
    </div>
  )
}

export function FieldLabel({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      fontSize: 9, color: MGMT.grayLight, marginBottom: 3,
      textTransform: 'uppercase', letterSpacing: 0.5, fontWeight: 600,
    }}>{children}</div>
  )
}

export function MiniBtn({ label, icon, onClick, color }: {
  label: string; icon?: React.ReactNode; onClick: () => void; color: string
}) {
  return (
    <span onClick={onClick} style={{
      fontSize: 10, padding: '4px 8px', borderRadius: 4,
      background: `${color}15`, color, cursor: 'pointer',
      display: 'flex', alignItems: 'center', gap: 3,
      border: `1px solid ${color}25`, transition: 'all 0.15s',
    }}
      onMouseEnter={e => e.currentTarget.style.background = `${color}25`}
      onMouseLeave={e => e.currentTarget.style.background = `${color}15`}
    >
      {icon} {label}
    </span>
  )
}
