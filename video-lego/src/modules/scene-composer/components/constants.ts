// ═══════════════════════════════════════════════════════════
// 场景编排器 — 常量与工具函数
// Scene Composer — Constants & Utilities
// ═══════════════════════════════════════════════════════════

import React from 'react'
import { MGMT } from '@/theme'
import { getBlockMeta } from '@blocks/catalog'
import { IconFullscreen, IconSplit } from '@/components/Icons'
import type { LayoutType, SceneData } from '@/lib/types'

export const LAYOUT_OPTIONS: { value: LayoutType; label: string; icon: React.ReactNode }[] = [
  { value: 'landscape', label: '横屏 16:9', icon: React.createElement(IconFullscreen, { size: 14 }) },
  { value: 'portrait', label: '竖屏 9:16', icon: React.createElement(IconSplit, { size: 14 }) },
]

export const ACT_COLORS: Record<string, string> = {
  '第一幕': '#4ea8de', '第二幕': '#e67e22', '第三幕': '#2ecc71',
  '第四幕': '#e74c3c', '第五幕': '#9b59b6', '第六幕': '#1abc9c',
}

export function getActColor(act: string): string {
  for (const [key, color] of Object.entries(ACT_COLORS)) {
    if (act.includes(key)) return color
  }
  return MGMT.grayLight
}

export function blockLabel(name: string): string {
  const meta = getBlockMeta(name)
  if (!meta) return name
  const d = meta.description
  return d.includes('，') ? d.split('，')[0] : d
}

export function catLabel(name: string): string {
  return name.replace(/\s+[A-Za-z]+$/, '')
}

export function emptyScene(lastAct = ''): SceneData {
  return { layout: 'landscape', act: lastAct, title: '新场景', visuals: [], points: [] }
}
