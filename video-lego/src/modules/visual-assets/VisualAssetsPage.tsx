// ═══════════════════════════════════════════════════════════
// M2 视觉画面 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconPalette2, IconImage2, IconClapperboard } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#2ecc71'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '动态素材',
    icon: <IconClapperboard size={12} />,
    subModules: [
      { id: 'M2.1', label: '动画规格', leaves: [
        { id: 'manim', label: 'Manim 动画' },
        { id: 'motion_gfx', label: 'Motion Graphics' },
        { id: 'css_anim', label: 'CSS 动画' },
      ]},
      { id: 'M2.4', label: '屏幕录制', leaves: [
        { id: 'software_demo', label: '软件演示' },
        { id: 'code_writing', label: '代码编写' },
        { id: 'terminal_op', label: '终端操作' },
      ]},
    ],
  },
  {
    label: '静态素材',
    icon: <IconImage2 size={12} />,
    subModules: [
      { id: 'M2.2', label: '图表设计', leaves: [
        { id: 'bar', label: '柱状图' },
        { id: 'scatter', label: '散点图' },
        { id: 'heatmap', label: '热力图' },
        { id: 'u_curve', label: 'U 曲线' },
        { id: 'pie', label: '饼图' },
      ]},
      { id: 'M2.3', label: '示意图', leaves: [
        { id: 'concept_map', label: '概念图' },
        { id: 'flowchart', label: '流程图' },
        { id: 'tree_diagram', label: '树图' },
        { id: 'network', label: '网络图' },
      ]},
      { id: 'M2.5', label: '插画/照片', leaves: [
        { id: 'illustration', label: '插画' },
        { id: 'photo', label: '照片' },
        { id: 'screenshot', label: '截图' },
      ]},
    ],
  },
]

export function VisualAssetsPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconPalette2 size={16} />} title="M2 视觉画面" subtitle="Visual Assets · Mayer + Knaflic" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconPalette2 size={64} />} title="视觉画面管理"
        lines={['Manim 动画 · 图表设计 · 示意图', '屏幕录制 · 插画/照片', 'Mayer 多媒体 + Knaflic 数据叙事']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconImage2 size={24} />} label="视觉预览" />}
    />
  )
}
