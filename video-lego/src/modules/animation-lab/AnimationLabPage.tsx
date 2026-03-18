// ═══════════════════════════════════════════════════════════
// M6a 动画实验室 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconSparkles, IconSettings, IconClapperboard } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#9b59b6'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '动画类型',
    icon: <IconClapperboard size={12} />,
    subModules: [
      { id: 'M6.A', label: '入场动画', leaves: [
        { id: 'fadeIn', label: 'fadeIn' },
        { id: 'slideUp', label: 'slideUp' },
        { id: 'springScale', label: 'springScale' },
        { id: 'zoomIn', label: 'zoomIn' },
      ]},
      { id: 'M6.B', label: '强调动画', leaves: [
        { id: 'pulse', label: 'pulse' },
        { id: 'glow', label: 'glow' },
        { id: 'shake', label: 'shake' },
        { id: 'bounce', label: 'bounce' },
      ]},
      { id: 'M6.C', label: '退场动画', leaves: [
        { id: 'fadeOut', label: 'fadeOut' },
        { id: 'slideDown', label: 'slideDown' },
        { id: 'shrink', label: 'shrink' },
        { id: 'zoomOut', label: 'zoomOut' },
      ]},
    ],
  },
  {
    label: '动画工具',
    icon: <IconSettings size={12} />,
    subModules: [
      { id: 'M6.D', label: '缓动曲线', leaves: [
        { id: 'easeIn', label: 'easeIn' },
        { id: 'easeOut', label: 'easeOut' },
        { id: 'spring', label: 'spring' },
        { id: 'bounce_ease', label: 'bounce' },
      ]},
      { id: 'M6.E', label: '序列组合', leaves: [
        { id: 'serial', label: '串行' },
        { id: 'parallel', label: '并行' },
        { id: 'stagger', label: '错峰' },
      ]},
    ],
  },
]

export function AnimationLabPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconSparkles size={16} />} title="M6a 动画实验室" subtitle="Animation Lab · Williams 动画原理" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconSparkles size={64} />} title="动画实验室"
        lines={['浏览 · 编辑 · 预览动画原子', '缓动曲线编辑器', '动画序列组合 · 积木绑定']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconSparkles size={24} />} label="参数与缓动曲线" />}
    />
  )
}
