// ═══════════════════════════════════════════════════════════
// M8 来源引用 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconBookOpen, IconBookmark, IconListChecks } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#888888'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '索引管理',
    icon: <IconBookOpen size={12} />,
    subModules: [
      { id: 'M8.1', label: '教科书库', leaves: [
        { id: 'indexed_books', label: '已索引书目' },
        { id: 'chapter_struct', label: '章节结构' },
        { id: 'book_search', label: '搜索' },
      ]},
      { id: 'M8.2', label: '引用管理', leaves: [
        { id: 'asset_binding', label: '素材绑定' },
        { id: 'batch_cite', label: '批量标注' },
      ]},
    ],
  },
  {
    label: '检查输出',
    icon: <IconListChecks size={12} />,
    subModules: [
      { id: 'M8.3', label: '版权检查', leaves: [
        { id: 'img_license', label: '图片 License' },
        { id: 'code_license', label: '代码 License' },
        { id: 'cite_format', label: '引用格式' },
      ]},
      { id: 'M8.4', label: '片尾字幕', leaves: [
        { id: 'bibliography', label: '参考文献' },
        { id: 'acknowledgment', label: '致谢' },
        { id: 'disclaimer', label: '声明' },
      ]},
    ],
  },
]

export function ReferencesPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconBookOpen size={16} />} title="M8 来源引用" subtitle="References · 学术规范" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconBookOpen size={64} />} title="来源引用管理"
        lines={['教科书索引 · 引用绑定', '版权检查 · 片尾字幕生成', '确保每个素材有据可查']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconBookmark size={24} />} label="引用详情" />}
    />
  )
}
