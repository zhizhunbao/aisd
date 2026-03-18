// ═══════════════════════════════════════════════════════════
// 通用模块页面 — 数据驱动，从注册表渲染
// GenericModulePage — data-driven, renders from registry
//
// 使用 module-registry 的数据 + ConfigSidebar + LayoutTemplates:
//   选中 sidebar 节点 → 读取 layout 字段 → 渲染对应布局模板
// ═══════════════════════════════════════════════════════════

import { useState, useCallback } from 'react'
import { MGMT } from '@/theme'
import { ModuleLayout, ModuleHeader, CenterPlaceholder, RightPlaceholder } from '@/components/ModuleLayout'
import { ConfigSidebar } from '@/components/ConfigSidebar'
import { renderLayout, getLayoutIcon } from '@/components/LayoutTemplates'
import { findNode, LAYOUT_META, type ModuleDef, type SidebarNode, type LayoutType } from '@/data/module-registry'

// ─── 图标映射: string → React 组件 ───

import {
  IconPackage, IconMic, IconPalette2, IconType, IconDatabase,
  IconVolume, IconBlocks, IconSparkles, IconListChecks, IconBookOpen,
  IconFilm, IconClock,
} from '@/components/Icons'

const ICON_MAP: Record<string, React.ComponentType<{ size: number; style?: React.CSSProperties }>> = {
  package: IconPackage, mic: IconMic, palette: IconPalette2, type: IconType,
  database: IconDatabase, volume: IconVolume, blocks: IconBlocks, sparkles: IconSparkles,
  listChecks: IconListChecks, bookOpen: IconBookOpen, film: IconFilm, clock: IconClock,
}

function getModuleIcon(key: string, size: number, style?: React.CSSProperties) {
  const Icon = ICON_MAP[key] || IconPackage
  return <Icon size={size} style={style} />
}

// ─── 通用模块页面 ───

export function GenericModulePage({ moduleDef }: { moduleDef: ModuleDef }) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [sidebarNodes, setSidebarNodes] = useState<SidebarNode[]>(() => moduleDef.sidebar)

  const handleNodesChange = useCallback((nodes: SidebarNode[]) => {
    setSidebarNodes(nodes)
  }, [])

  // 找到选中节点
  const selectedNode = selectedId ? findNode(sidebarNodes, selectedId) : null
  const layout = selectedNode?.layout
  const layoutConfig = selectedNode?.layoutConfig

  // 根据 layout 渲染中栏和右栏
  let centerContent: React.ReactNode
  let rightContent: React.ReactNode

  if (selectedNode && layout) {
    const rendered = renderLayout(layout, {
      nodeId: selectedNode.id,
      label: selectedNode.label,
      color: moduleDef.color,
      centerLabel: layoutConfig?.centerLabel,
      rightLabel: layoutConfig?.rightLabel,
      description: layoutConfig?.description,
    })
    centerContent = rendered.center
    rightContent = rendered.right
  } else if (selectedNode && !layout) {
    // 选中了分类节点（没有 layout）
    centerContent = (
      <CenterPlaceholder
        icon={getModuleIcon(moduleDef.icon, 64)}
        title={selectedNode.label}
        lines={[
          `分类: ${selectedNode.label}`,
          `包含 ${selectedNode.children?.length || 0} 个子模块`,
          '选择子模块开始工作',
        ]}
        color={moduleDef.color}
      />
    )
    rightContent = <RightPlaceholder icon={getModuleIcon(moduleDef.icon, 24)} label="属性与预览" />
  } else {
    // 未选中任何节点
    centerContent = (
      <CenterPlaceholder
        icon={getModuleIcon(moduleDef.icon, 64)}
        title={moduleDef.label}
        lines={[
          `${moduleDef.labelEn} · ${moduleDef.subtitle}`,
          `${countLeafNodes(sidebarNodes)} 个子模块 · ${countLayouts(sidebarNodes)} 种布局`,
          '选择左侧子模块开始工作',
        ]}
        color={moduleDef.color}
      />
    )
    rightContent = (
      <div style={{ padding: 16 }}>
        <div style={{
          fontSize: 10, fontWeight: 700, color: moduleDef.color,
          textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12,
        }}>
          布局类型
        </div>
        {(['L1','L2','L3','L4','L5'] as LayoutType[]).map(l => {
          const meta = LAYOUT_META[l]
          const count = countLayoutType(sidebarNodes, l)
          if (count === 0) return null
          return (
            <div key={l} style={{
              padding: '8px 10px', marginBottom: 4, borderRadius: 5,
              background: `${MGMT.white}04`, border: `1px solid ${MGMT.border}`,
              display: 'flex', alignItems: 'center', gap: 8,
            }}>
              {getLayoutIcon(l, 14)}
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 11, color: MGMT.dimWhite }}>{meta.name}</div>
                <div style={{ fontSize: 9, color: MGMT.grayLight }}>{meta.desc}</div>
              </div>
              <span style={{
                fontSize: 9, color: moduleDef.color, fontWeight: 700,
                background: `${moduleDef.color}15`, padding: '2px 6px', borderRadius: 3,
              }}>{count}</span>
            </div>
          )
        })}
      </div>
    )
  }

  return (
    <ModuleLayout
      left={<>
        <ModuleHeader
          icon={getModuleIcon(moduleDef.icon, 16)}
          title={`${moduleDef.id} ${moduleDef.label}`}
          subtitle={`${moduleDef.labelEn} · ${moduleDef.subtitle}`}
          color={moduleDef.color}
        />
        <ConfigSidebar
          nodes={sidebarNodes}
          color={moduleDef.color}
          moduleId={moduleDef.id}
          selectedId={selectedId}
          onSelect={setSelectedId}
          onNodesChange={handleNodesChange}
        />
      </>}
      center={centerContent}
      right={rightContent}
    />
  )
}

// ─── 辅助 ───

function countLeafNodes(nodes: SidebarNode[]): number {
  let count = 0
  for (const n of nodes) {
    if (n.children && n.children.length > 0) count += countLeafNodes(n.children)
    else count++
  }
  return count
}

function countLayouts(nodes: SidebarNode[]): number {
  const set = new Set<string>()
  const collect = (list: SidebarNode[]) => {
    for (const n of list) {
      if (n.layout) set.add(n.layout)
      if (n.children) collect(n.children)
    }
  }
  collect(nodes)
  return set.size
}

function countLayoutType(nodes: SidebarNode[], layout: LayoutType): number {
  let count = 0
  const walk = (list: SidebarNode[]) => {
    for (const n of list) {
      if (n.layout === layout) count++
      if (n.children) walk(n.children)
    }
  }
  walk(nodes)
  return count
}
