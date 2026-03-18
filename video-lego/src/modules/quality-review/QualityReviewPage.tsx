// ═══════════════════════════════════════════════════════════
// M7 质量审查 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconListChecks, IconAlert, IconWarning, IconInfo } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#1abc9c'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '严重',
    color: '#e74c3c',
    icon: <IconAlert size={12} />,
    subModules: [
      { id: 'M7.1', label: '冗余检查', leaves: [
        { id: 'narr_vis_dup', label: '旁白+画面重复' },
        { id: 'text_vis_dup', label: '文字+画面重复' },
      ]},
      { id: 'M7.2', label: '时间同步', leaves: [
        { id: 'vis_early', label: '画面提前' },
        { id: 'vis_late', label: '画面滞后' },
      ]},
    ],
  },
  {
    label: '中等',
    color: '#f1c40f',
    icon: <IconWarning size={12} />,
    subModules: [
      { id: 'M7.3', label: '空间邻近', leaves: [
        { id: 'text_far', label: '文字离图太远' },
        { id: 'ann_offset', label: '标注位置偏移' },
      ]},
      { id: 'M7.4', label: '相干性', leaves: [
        { id: 'irrelevant_deco', label: '无关装饰' },
        { id: 'irrelevant_bgm', label: '无关 BGM' },
      ]},
      { id: 'M7.5', label: '分段检查', leaves: [
        { id: 'overtime_seg', label: '超时段落' },
        { id: 'no_interact', label: '无交互段落' },
      ]},
    ],
  },
  {
    label: '建议',
    color: '#2ecc71',
    icon: <IconInfo size={12} />,
    subModules: [
      { id: 'M7.6', label: '声音质量', leaves: [
        { id: 'robotic', label: '机器声明显' },
        { id: 'volume_uneven', label: '音量不均' },
      ]},
      { id: 'M7.7', label: '人格化', leaves: [
        { id: 'too_formal', label: '过于正式' },
        { id: 'no_interact_tone', label: '缺少互动' },
      ]},
    ],
  },
]

export function QualityReviewPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout defaultLeftWidth={280}
      left={<>
        <ModuleHeader icon={<IconListChecks size={16} />} title="M7 质量审查" subtitle="Quality Review · Clark & Mayer Ch.17" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconListChecks size={64} />} title="质量审查"
        lines={['Mayer 12 原则自动检查', '冗余 · 同步 · 邻近 · 相干', '输出 review_report.md']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconAlert size={24} />} label="审查报告" />}
    />
  )
}
