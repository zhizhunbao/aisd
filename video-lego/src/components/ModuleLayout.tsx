// ═══════════════════════════════════════════════════════════
// 模块通用三栏布局 — 可复用骨架
// Module Three-Panel Layout — reusable skeleton
//
// 所有模块页面统一使用此布局:
//   左栏: 列表/导航（可拖拽宽度）
//   中栏: 主画布/预览区
//   右栏: 编辑/属性面板（可拖拽宽度）
//
// 用法:
//   <ModuleLayout
//     left={<MyList />}
//     center={<MyCanvas />}
//     right={<MyPanel />}
//   />
// ═══════════════════════════════════════════════════════════

import { useState, useEffect, useRef, type ReactNode } from 'react'
import { MGMT } from '@/theme'

// ─── 分割条 DividerHandle ───

function DividerHandle({ side, draggingRef }: {
  side: 'left' | 'right'
  draggingRef: React.MutableRefObject<'left' | 'right' | null>
}) {
  return (
    <div
      onMouseDown={() => { draggingRef.current = side; document.body.style.cursor = 'col-resize' }}
      style={{
        width: 5, cursor: 'col-resize', background: 'transparent',
        flexShrink: 0, position: 'relative', zIndex: 10,
      }}
      onMouseEnter={e => (e.currentTarget.style.background = `${MGMT.gold}30`)}
      onMouseLeave={e => { if (!draggingRef.current) e.currentTarget.style.background = 'transparent' }}
    />
  )
}

// ─── 子模块项 ───

export interface SubModuleItem {
  id: string
  label: string
  desc: string
}

// ─── 模块标题栏 ───

export function ModuleHeader({ icon, title, subtitle, color }: {
  icon: ReactNode
  title: string
  subtitle: string
  color?: string
}) {
  return (
    <div style={{ padding: '14px 16px', borderBottom: `1px solid ${MGMT.border}` }}>
      <div style={{
        fontSize: 15, fontWeight: 800, color: MGMT.white,
        display: 'flex', alignItems: 'center', gap: 8,
      }}>
        <span style={{ color: color || MGMT.white, display: 'flex', alignItems: 'center' }}>{icon}</span>
        {title}
      </div>
      <div style={{ fontSize: 11, color: MGMT.grayLight, marginTop: 4 }}>{subtitle}</div>
    </div>
  )
}

// ─── 子模块列表（平铺） ───

export function SubModuleList({ items, color, selectedId, onSelect }: {
  items: SubModuleItem[]
  color: string
  selectedId: string | null
  onSelect: (id: string) => void
}) {
  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: 8 }}>
      {items.map(item => {
        const active = selectedId === item.id
        return (
          <div key={item.id}
            onClick={() => onSelect(item.id)}
            style={{
              padding: '10px 12px', borderRadius: 6, marginBottom: 4,
              background: active ? `${color}10` : `${MGMT.white}04`,
              border: `1px solid ${active ? `${color}30` : MGMT.border}`,
              cursor: 'pointer', transition: 'all 0.15s',
            }}
          >
            <div style={{
              fontSize: 12, fontWeight: active ? 700 : 600,
              color: active ? MGMT.white : MGMT.dimWhite,
              display: 'flex', alignItems: 'center', gap: 6,
            }}>
              <span style={{ color, fontSize: 10, fontFamily: MGMT.codeFontFamily }}>{item.id}</span>
              {item.label}
            </div>
            <div style={{ fontSize: 10, color: MGMT.grayLight, marginTop: 2, paddingLeft: 0 }}>{item.desc}</div>
          </div>
        )
      })}
    </div>
  )
}

// ─── 分组子模块列表（二级: 大分类 → 子分类） ───
// 保留旧组件兼容

export interface SubModuleGroup {
  label: string
  color?: string
  icon?: ReactNode
  items: SubModuleItem[]
}

export function GroupedSubModuleList({ groups, color, selectedId, onSelect }: {
  groups: SubModuleGroup[]
  color: string
  selectedId: string | null
  onSelect: (id: string) => void
}) {
  // 转换为三级结构（叶子为空）
  const tree: SidebarCategory[] = groups.map(g => ({
    label: g.label, color: g.color, icon: g.icon,
    subModules: g.items.map(item => ({
      id: item.id, label: item.label, desc: item.desc, leaves: [],
    })),
  }))
  return <ModuleSidebar categories={tree} color={color} selectedId={selectedId} onSelect={onSelect} />
}

// ─── 三级侧栏（大分类 → 子模块 → 原子叶子项） ───
//
// L1: 大分类标题 (section header, colored, uppercase)
// L2: 子模块 (M-code tag + label, clickable)
// L3: 原子叶子项 (indented, smallest text, clickable)
//
// 所有层级平铺展示，不折叠。

export interface LeafItem {
  id: string
  label: string
}

export interface SubModuleNode {
  id: string
  label: string
  desc?: string
  leaves: LeafItem[]
}

export interface SidebarCategory {
  label: string
  color?: string
  icon?: ReactNode
  subModules: SubModuleNode[]
}

export function ModuleSidebar({ categories, color, selectedId, onSelect }: {
  categories: SidebarCategory[]
  color: string
  selectedId: string | null
  onSelect: (id: string) => void
}) {
  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: 8 }}>
      {categories.map(cat => {
        const catColor = cat.color || color
        return (
          <div key={cat.label} style={{ marginBottom: 10 }}>
            {/* ── L1: 大分类标题 ── */}
            <div style={{
              fontSize: 10, fontWeight: 700, color: catColor,
              textTransform: 'uppercase', letterSpacing: 1,
              padding: '8px 10px 4px',
              display: 'flex', alignItems: 'center', gap: 5,
            }}>
              {cat.icon && <span style={{ display: 'flex', alignItems: 'center' }}>{cat.icon}</span>}
              {cat.label}
            </div>

            {cat.subModules.map(sub => (
              <div key={sub.id}>
                {/* ── L2: 子模块 ── */}
                <div
                  onClick={() => onSelect(sub.id)}
                  style={{
                    padding: '6px 10px', borderRadius: 5, marginBottom: 1,
                    background: selectedId === sub.id ? `${catColor}10` : 'transparent',
                    border: `1px solid ${selectedId === sub.id ? `${catColor}30` : 'transparent'}`,
                    cursor: 'pointer', transition: 'all 0.15s',
                    display: 'flex', alignItems: 'center', gap: 6,
                  }}
                >
                  <span style={{
                    color: catColor, fontSize: 8, fontWeight: 700,
                    fontFamily: MGMT.codeFontFamily, opacity: 0.7,
                    width: 30, flexShrink: 0, textAlign: 'right',
                  }}>
                    {sub.id}
                  </span>
                  <span style={{
                    fontSize: 12, fontWeight: selectedId === sub.id ? 700 : 500,
                    color: selectedId === sub.id ? MGMT.white : MGMT.dimWhite,
                  }}>
                    {sub.label}
                  </span>
                </div>

                {/* ── L3: 原子叶子项 ── */}
                {sub.leaves.length > 0 && (
                  <div style={{ paddingLeft: 42, marginBottom: 4 }}>
                    {sub.leaves.map(leaf => {
                      const leafActive = selectedId === leaf.id
                      return (
                        <div key={leaf.id}
                          onClick={() => onSelect(leaf.id)}
                          style={{
                            fontSize: 11, padding: '3px 8px', borderRadius: 4, marginBottom: 1,
                            color: leafActive ? MGMT.white : MGMT.grayLight,
                            background: leafActive ? `${catColor}10` : 'transparent',
                            cursor: 'pointer', transition: 'all 0.12s',
                            fontWeight: leafActive ? 600 : 400,
                          }}
                        >
                          {leaf.label}
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>
            ))}
          </div>
        )
      })}
    </div>
  )
}

// ─── 占位中心区域（模块开发中） ───

export function CenterPlaceholder({ icon, title, lines, color }: {
  icon: ReactNode
  title: string
  lines: string[]
  color: string
}) {
  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ textAlign: 'center', color: MGMT.grayLight, maxWidth: 440 }}>
        <div style={{ opacity: 0.15, marginBottom: 16, display: 'flex', justifyContent: 'center' }}>
          {icon}
        </div>
        <div style={{ fontSize: 18, fontWeight: 600, color: MGMT.dimWhite, marginBottom: 8 }}>
          {title}
        </div>
        <div style={{ fontSize: 13, lineHeight: 1.8 }}>
          {lines.map((l, i) => <span key={i}>{l}{i < lines.length - 1 && <br />}</span>)}
        </div>
        <div style={{
          marginTop: 20, padding: '8px 16px', borderRadius: 6,
          background: `${color}10`, border: `1px solid ${color}20`,
          color, fontSize: 12, display: 'inline-flex', alignItems: 'center', gap: 6,
        }}>
          ⚡ 模块开发中
        </div>
      </div>
    </div>
  )
}

// ─── 占位右侧面板 ───

export function RightPlaceholder({ icon, label }: {
  icon: ReactNode
  label: string
}) {
  return (
    <div style={{
      flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
      color: MGMT.grayLight,
    }}>
      <div style={{ textAlign: 'center', fontSize: 11 }}>
        <div style={{ opacity: 0.2, marginBottom: 6, display: 'flex', justifyContent: 'center' }}>{icon}</div>
        <div>{label}</div>
      </div>
    </div>
  )
}

// ─── 主布局组件 ───

interface ModuleLayoutProps {
  left: ReactNode
  center: ReactNode
  right: ReactNode
  defaultLeftWidth?: number
  defaultRightWidth?: number
  minLeft?: number
  maxLeft?: number
  minRight?: number
  maxRight?: number
}

export function ModuleLayout({
  left, center, right,
  defaultLeftWidth = 260,
  defaultRightWidth = 300,
  minLeft = 200, maxLeft = 400,
  minRight = 240, maxRight = 460,
}: ModuleLayoutProps) {
  const [leftW, setLeftW] = useState(defaultLeftWidth)
  const [rightW, setRightW] = useState(defaultRightWidth)
  const draggingRef = useRef<'left' | 'right' | null>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!draggingRef.current) return
      e.preventDefault()
      if (draggingRef.current === 'left') {
        setLeftW(Math.max(minLeft, Math.min(maxLeft, e.clientX - MGMT.sidebar.width)))
      } else {
        setRightW(Math.max(minRight, Math.min(maxRight, window.innerWidth - e.clientX)))
      }
    }
    const onUp = () => { draggingRef.current = null; document.body.style.cursor = '' }
    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup', onUp)
    return () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp) }
  }, [minLeft, maxLeft, minRight, maxRight])

  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', overflow: 'hidden' }}>
      {/* ═══ 左栏 ═══ */}
      <div style={{
        width: leftW, minWidth: leftW, maxWidth: leftW,
        borderRight: `1px solid ${MGMT.border}`,
        display: 'flex', flexDirection: 'column',
        background: MGMT.bgSidebar,
      }}>
        {left}
      </div>

      <DividerHandle side="left" draggingRef={draggingRef} />

      {/* ═══ 中栏 ═══ */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {center}
      </div>

      <DividerHandle side="right" draggingRef={draggingRef} />

      {/* ═══ 右栏 ═══ */}
      <div style={{
        width: rightW, minWidth: rightW, maxWidth: rightW,
        borderLeft: `1px solid ${MGMT.border}`,
        display: 'flex', flexDirection: 'column',
        background: MGMT.bgSidebar,
      }}>
        {right}
      </div>
    </div>
  )
}
