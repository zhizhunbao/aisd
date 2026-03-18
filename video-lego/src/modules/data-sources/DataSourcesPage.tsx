// ═══════════════════════════════════════════════════════════
// M4 数据源 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconDatabase, IconTable, IconChart, IconFileCode } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#e67e22'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '结构数据',
    icon: <IconChart size={12} />,
    subModules: [
      { id: 'M4.1', label: '时间线数据', leaves: [
        { id: 'year_event', label: '年份事件' },
        { id: 'milestone', label: '里程碑' },
        { id: 'evolution', label: '演进路线' },
      ]},
      { id: 'M4.2', label: '对比结构', leaves: [
        { id: 'binary_cmp', label: '二元对比' },
        { id: 'multi_cmp', label: '多维对比' },
      ]},
      { id: 'M4.5', label: '参数表', leaves: [
        { id: 'kv_props', label: 'KV 属性' },
        { id: 'config_table', label: '配置表' },
      ]},
    ],
  },
  {
    label: '内容数据',
    icon: <IconFileCode size={12} />,
    subModules: [
      { id: 'M4.3', label: '数值数据集', leaves: [
        { id: 'json_data', label: 'JSON' },
        { id: 'csv_data', label: 'CSV' },
        { id: 'inline_array', label: '内联数组' },
      ]},
      { id: 'M4.4', label: '代码示例', leaves: [
        { id: 'python', label: 'Python' },
        { id: 'javascript', label: 'JavaScript' },
        { id: 'sql', label: 'SQL' },
        { id: 'shell', label: 'Shell' },
      ]},
    ],
  },
]

export function DataSourcesPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconDatabase size={16} />} title="M4 数据源" subtitle="Data Sources · Knaflic + Mayer" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconDatabase size={64} />} title="数据源管理"
        lines={['时间线 · 对比结构 · 数值数据集', '代码示例 · 参数表', '驱动积木组件的结构化数据']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconTable size={24} />} label="数据预览" />}
    />
  )
}
