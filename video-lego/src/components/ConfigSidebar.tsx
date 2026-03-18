// ═══════════════════════════════════════════════════════════
// 可配置侧栏 — 递归树渲染 + 动态增删
// ConfigSidebar — recursive tree + add/delete
//
// 支持任意层级：
//   L1: 分类标题 (children 不为空的顶层节点)
//   L2: 子模块   (MX.Y 编号，可点击)
//   L3+: 可选更深层级
//
// 特性：
//   ✅ 递归渲染任意深度
//   ✅ 每个节点可删除 (hover 显示 ×)
//   ✅ 每个分类可添加子节点 (+ 按钮)
//   ✅ 可添加顶层分类
//   ✅ 选中状态高亮
// ═══════════════════════════════════════════════════════════

import { useState, useCallback, type ReactNode } from 'react'
import { MGMT } from '@/theme'
import type { SidebarNode } from '@/data/module-registry'
import { IconPlus, IconX, IconSearch } from '@/components/Icons'

// ─── 图标映射 ───

const ICON_MAP: Record<string, (props: { size: number; style?: React.CSSProperties }) => ReactNode> = {}

// 动态导入在使用时填充（避免循环依赖）
export function registerIcon(key: string, component: typeof ICON_MAP[string]) {
  ICON_MAP[key] = component
}

// ─── 主组件 ───

interface ConfigSidebarProps {
  nodes: SidebarNode[]
  color: string
  moduleId: string
  selectedId: string | null
  onSelect: (id: string) => void
  onNodesChange?: (nodes: SidebarNode[]) => void
  /** 是否显示编辑按钮（增删） */
  editable?: boolean
}

export function ConfigSidebar({
  nodes, color, moduleId, selectedId, onSelect,
  onNodesChange, editable = true,
}: ConfigSidebarProps) {
  const [search, setSearch] = useState('')
  const [editMode, setEditMode] = useState(false)

  // ─── 增删操作 ───

  const addChild = useCallback((parentId: string | null) => {
    const label = prompt('输入名称:')
    if (!label) return

    if (!parentId) {
      // 添加顶层分类
      const newNode: SidebarNode = {
        id: `cat-${Date.now()}`,
        label,
        children: [],
      }
      onNodesChange?.([...nodes, newNode])
    } else {
      // 添加到指定父节点下
      const addTo = (list: SidebarNode[]): SidebarNode[] =>
        list.map(n => {
          if (n.id === parentId) {
            const nextIdx = (n.children?.length || 0) + 1
            const newId = `${moduleId}.${nextIdx}`
            return {
              ...n,
              children: [...(n.children || []), { id: newId, label }],
            }
          }
          if (n.children) return { ...n, children: addTo(n.children) }
          return n
        })
      onNodesChange?.(addTo(nodes))
    }
  }, [nodes, moduleId, onNodesChange])

  const deleteNode = useCallback((targetId: string) => {
    const remove = (list: SidebarNode[]): SidebarNode[] =>
      list
        .filter(n => n.id !== targetId)
        .map(n => n.children ? { ...n, children: remove(n.children) } : n)
    onNodesChange?.(remove(nodes))
  }, [nodes, onNodesChange])

  // ─── 搜索过滤 ───

  const filterNodes = useCallback((list: SidebarNode[], q: string): SidebarNode[] => {
    if (!q) return list
    return list
      .map(n => {
        if (n.label.toLowerCase().includes(q)) return n
        if (n.children) {
          const filtered = filterNodes(n.children, q)
          if (filtered.length > 0) return { ...n, children: filtered }
        }
        return null
      })
      .filter(Boolean) as SidebarNode[]
  }, [])

  const displayed = search ? filterNodes(nodes, search.toLowerCase()) : nodes

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* 搜索 + 编辑切换 */}
      <div style={{
        padding: '6px 10px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', gap: 4, alignItems: 'center',
      }}>
        <div style={{
          flex: 1, display: 'flex', alignItems: 'center', gap: 6,
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 5, padding: '5px 8px',
        }}>
          <IconSearch size={12} style={{ color: MGMT.grayLight, flexShrink: 0 }} />
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="搜索..."
            style={{
              background: 'transparent', border: 'none', color: MGMT.white,
              fontFamily: MGMT.fontFamily, fontSize: 11, outline: 'none', width: '100%',
            }}
          />
        </div>
        {editable && (
          <button
            onClick={() => setEditMode(!editMode)}
            style={{
              background: editMode ? `${color}20` : 'transparent',
              border: `1px solid ${editMode ? `${color}40` : 'transparent'}`,
              color: editMode ? color : MGMT.grayLight,
              borderRadius: 4, padding: '4px 6px', cursor: 'pointer',
              fontSize: 10, fontFamily: MGMT.fontFamily, fontWeight: 600,
              transition: 'all 0.15s',
            }}
          >
            {editMode ? '完成' : '编辑'}
          </button>
        )}
      </div>

      {/* 递归树 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 6 }}>
        {displayed.map(node => (
          <TreeNode
            key={node.id}
            node={node}
            depth={0}
            color={color}
            selectedId={selectedId}
            onSelect={onSelect}
            editMode={editMode}
            onAdd={addChild}
            onDelete={deleteNode}
          />
        ))}

        {/* 添加顶层分类 */}
        {editMode && (
          <button
            onClick={() => addChild(null)}
            style={{
              width: '100%', padding: '6px 10px', marginTop: 4,
              background: `${MGMT.white}04`, border: `1px dashed ${MGMT.border}`,
              borderRadius: 5, color: MGMT.grayLight, fontSize: 11,
              cursor: 'pointer', fontFamily: MGMT.fontFamily,
              display: 'flex', alignItems: 'center', gap: 4, justifyContent: 'center',
              transition: 'all 0.15s',
            }}
          >
            <IconPlus size={10} /> 添加分类
          </button>
        )}
      </div>
    </div>
  )
}

// ─── 递归树节点 ───

function TreeNode({ node, depth, color, selectedId, onSelect, editMode, onAdd, onDelete }: {
  node: SidebarNode
  depth: number
  color: string
  selectedId: string | null
  onSelect: (id: string) => void
  editMode: boolean
  onAdd: (parentId: string | null) => void
  onDelete: (id: string) => void
}) {
  const [hovered, setHovered] = useState(false)
  const hasChildren = node.children && node.children.length > 0
  const isCategory = depth === 0 && hasChildren
  const isSelected = selectedId === node.id
  const isMCode = /^M\d/.test(node.id)

  if (isCategory) {
    // ── L1: 分类标题 ──
    return (
      <div style={{ marginBottom: 6 }}>
        <div
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
          style={{
            fontSize: 10, fontWeight: 700, color,
            textTransform: 'uppercase', letterSpacing: 1,
            padding: '8px 8px 3px',
            display: 'flex', alignItems: 'center', gap: 4,
          }}
        >
          <span style={{ flex: 1 }}>{node.label}</span>
          {editMode && hovered && (
            <span style={{ display: 'flex', gap: 2 }}>
              <ActionBtn icon={<IconPlus size={9} />} color={color}
                onClick={() => onAdd(node.id)} title="添加子项" />
              <ActionBtn icon={<IconX size={9} />} color="#e74c3c"
                onClick={() => onDelete(node.id)} title="删除分类" />
            </span>
          )}
        </div>
        {node.children!.map(child => (
          <TreeNode key={child.id} node={child} depth={depth + 1}
            color={color} selectedId={selectedId} onSelect={onSelect}
            editMode={editMode} onAdd={onAdd} onDelete={onDelete} />
        ))}
      </div>
    )
  }

  // ── L2+: 子模块 / 叶子 ──
  const indent = depth * 8

  return (
    <div>
      <div
        onClick={() => onSelect(node.id)}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        style={{
          padding: `5px ${8}px 5px ${8 + indent}px`,
          borderRadius: 5, marginBottom: 1,
          background: isSelected ? `${color}10` : 'transparent',
          border: `1px solid ${isSelected ? `${color}30` : 'transparent'}`,
          cursor: 'pointer', transition: 'all 0.15s',
          display: 'flex', alignItems: 'center', gap: 6,
        }}
      >
        {/* M-code 编号 */}
        {isMCode && (
          <span style={{
            color, fontSize: 8, fontWeight: 700,
            fontFamily: MGMT.codeFontFamily, opacity: 0.7,
            width: 30, flexShrink: 0, textAlign: 'right',
          }}>
            {node.id}
          </span>
        )}
        <span style={{
          fontSize: depth <= 1 ? 12 : 11,
          fontWeight: isSelected ? 700 : 500,
          color: isSelected ? MGMT.white : MGMT.dimWhite,
          flex: 1,
        }}>
          {node.label}
        </span>
        {editMode && hovered && (
          <span style={{ display: 'flex', gap: 2 }}>
            {hasChildren && (
              <ActionBtn icon={<IconPlus size={9} />} color={color}
                onClick={() => onAdd(node.id)} title="添加子项" />
            )}
            <ActionBtn icon={<IconX size={9} />} color="#e74c3c"
              onClick={() => onDelete(node.id)} title="删除" />
          </span>
        )}
      </div>
      {/* 递归渲染子节点 */}
      {hasChildren && node.children!.map(child => (
        <TreeNode key={child.id} node={child} depth={depth + 1}
          color={color} selectedId={selectedId} onSelect={onSelect}
          editMode={editMode} onAdd={onAdd} onDelete={onDelete} />
      ))}
    </div>
  )
}

// ─── 操作按钮 ───

function ActionBtn({ icon, color, onClick, title }: {
  icon: ReactNode; color: string; onClick: () => void; title: string
}) {
  return (
    <button
      onClick={e => { e.stopPropagation(); onClick() }}
      title={title}
      style={{
        background: `${color}15`, border: `1px solid ${color}30`,
        borderRadius: 3, padding: 2, cursor: 'pointer',
        color, display: 'flex', alignItems: 'center',
        transition: 'all 0.12s',
      }}
    >
      {icon}
    </button>
  )
}
