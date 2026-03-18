// ═══════════════════════════════════════════════════════════
// M1 脚本工坊 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconMic, IconFileText, IconBookOpen } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#4ea8de'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '叙事结构',
    icon: <IconBookOpen size={12} />,
    subModules: [
      { id: 'M1.1', label: '故事结构', leaves: [
        { id: 'three_act', label: '三幕结构' },
        { id: 'five_act', label: '五幕结构' },
        { id: 'beat_sheet', label: 'Beat Sheet 15 拍' },
      ]},
      { id: 'M1.4', label: '冲突弧线', leaves: [
        { id: 'problem', label: '问题提出' },
        { id: 'tension', label: '紧张升级' },
        { id: 'resolution', label: '解决回落' },
      ]},
    ],
  },
  {
    label: '文稿编辑',
    icon: <IconMic size={12} />,
    subModules: [
      { id: 'M1.2', label: '旁白文稿', leaves: [
        { id: 'hook', label: '开场钩子' },
        { id: 'explain', label: '讲解旁白' },
        { id: 'transition_text', label: '过渡语' },
        { id: 'summary', label: '总结收尾' },
        { id: 'aside', label: '旁白补充' },
      ]},
      { id: 'M1.3', label: '节奏设计', leaves: [
        { id: 'duration_est', label: '时长预估' },
        { id: 'pause_mark', label: '停顿标记' },
        { id: 'speed_var', label: '语速变化' },
      ]},
    ],
  },
]

export function ScriptEditorPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconMic size={16} />} title="M1 脚本工坊" subtitle="Script Workshop · Snyder + McKee" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconMic size={64} />} title="脚本工坊"
        lines={['从知识地图生成旁白文稿', '分幕编辑 · 语气标注 · 关键词提取', 'Beat Sheet 故事节拍 · TTS 预览']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconFileText size={24} />} label="属性与预览" />}
    />
  )
}
