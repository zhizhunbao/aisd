// ═══════════════════════════════════════════════════════════
// M3 文字叠层 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconType, IconFileText, IconPin, IconCode2, IconQuote } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#ffd700'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '结构文字',
    icon: <IconPin size={12} />,
    subModules: [
      { id: 'M3.1', label: '标题卡', leaves: [
        { id: 'scene_title', label: '场景标题' },
        { id: 'chapter_card', label: '章节卡' },
        { id: 'act_title', label: '分幕标题' },
      ]},
      { id: 'M3.2', label: '要点列表', leaves: [
        { id: 'core_points', label: '核心要点' },
        { id: 'compare_list', label: '对比列表' },
        { id: 'step_list', label: '步骤列表' },
      ]},
    ],
  },
  {
    label: '技术文字',
    icon: <IconCode2 size={12} />,
    subModules: [
      { id: 'M3.3', label: '公式渲染', leaves: [
        { id: 'inline_formula', label: '行内公式' },
        { id: 'block_formula', label: '块级公式' },
        { id: 'annotated_formula', label: '带注释公式' },
      ]},
      { id: 'M3.4', label: '代码块', leaves: [
        { id: 'single_line', label: '单行代码' },
        { id: 'multi_line', label: '多行代码' },
        { id: 'code_diff', label: '代码对比' },
      ]},
    ],
  },
  {
    label: '辅助文字',
    icon: <IconQuote size={12} />,
    subModules: [
      { id: 'M3.5', label: '字幕', leaves: [
        { id: 'narration_sub', label: '旁白字幕' },
        { id: 'hard_sub', label: '硬字幕' },
      ]},
      { id: 'M3.6', label: '标注/引用', leaves: [
        { id: 'arrow_ann', label: '箭头标注' },
        { id: 'box_ann', label: '框选标注' },
        { id: 'quote_gold', label: '引用金句' },
      ]},
    ],
  },
]

export function TextOverlaysPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconType size={16} />} title="M3 文字叠层" subtitle="Text Overlays · Mayer Redundancy" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconType size={64} />} title="文字叠层管理"
        lines={['标题卡 · 要点列表 · 公式渲染', '代码块 · 字幕 · 标注', 'Mayer Redundancy + Signaling 原则']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconFileText size={24} />} label="叠层预览" />}
    />
  )
}
