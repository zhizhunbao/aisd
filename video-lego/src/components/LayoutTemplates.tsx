// ═══════════════════════════════════════════════════════════
// 布局模板组件 — 5 种通用内容区布局
// Layout Templates — 5 reusable content area layouts
//
// L1: 列表+详情      (list-detail)
// L2: 编辑器+预览    (editor-preview)
// L3: 画布+属性      (canvas-properties)
// L4: 卡片网格       (card-grid)
// L5: 横向时间线     (timeline)
//
// 所有模板统一接受:
//   nodeId, label, color, centerLabel, rightLabel
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import type { LayoutType } from '@/data/module-registry'
import {
  IconListChecks, IconEdit, IconPalette2, IconImage2, IconClock,
  IconChevronRight, IconSearch, IconPlus,
} from '@/components/Icons'

// ─── 统一接口 ───

export interface LayoutProps {
  nodeId: string
  label: string
  color: string
  centerLabel?: string
  rightLabel?: string
  description?: string
}

// ─── 布局图标 ───

const LAYOUT_ICONS: Record<LayoutType, typeof IconListChecks> = {
  L1: IconListChecks,
  L2: IconEdit,
  L3: IconPalette2,
  L4: IconImage2,
  L5: IconClock,
}

// ─── 返回类型 ───

export interface LayoutResult {
  center: React.ReactNode
  right: React.ReactNode
}

// ─── 渲染入口 ───

export function renderLayout(layout: LayoutType, props: LayoutProps): LayoutResult {
  switch (layout) {
    case 'L1': return LayoutL1(props)
    case 'L2': return LayoutL2(props)
    case 'L3': return LayoutL3(props)
    case 'L4': return LayoutL4(props)
    case 'L5': return LayoutL5(props)
  }
}

// ═══════════════════════════════════════════════════════════
// L1: 列表+详情
// ═══════════════════════════════════════════════════════════

function LayoutL1({ nodeId, label, color, centerLabel, rightLabel }: LayoutProps) {
  return { center: <L1Center nodeId={nodeId} label={label} color={color} centerLabel={centerLabel} />,
           right: <L1Right rightLabel={rightLabel} color={color} /> }
}

function L1Center({ nodeId, label, color, centerLabel }: { nodeId: string; label: string; color: string; centerLabel?: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      {/* 列表头 */}
      <div style={{
        padding: '10px 16px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 8,
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 6,
          flex: 1, background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 5, padding: '5px 8px',
        }}>
          <IconSearch size={12} style={{ color: MGMT.grayLight }} />
          <input placeholder={`搜索 ${label}...`}
            style={{ background: 'transparent', border: 'none', color: MGMT.white,
                     fontFamily: MGMT.fontFamily, fontSize: 11, outline: 'none', width: '100%' }} />
        </div>
        <button style={{
          background: `${color}15`, border: `1px solid ${color}30`, borderRadius: 4,
          color, padding: '5px 8px', fontSize: 11, cursor: 'pointer', fontFamily: MGMT.fontFamily,
          display: 'flex', alignItems: 'center', gap: 3,
        }}><IconPlus size={11} /> 新建</button>
      </div>
      {/* 列表区 (demo items) */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {[1,2,3,4,5].map(i => (
          <div key={i} style={{
            padding: '10px 16px', borderBottom: `1px solid ${MGMT.border}`,
            cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8,
            transition: 'background 0.1s',
          }}>
            <div style={{
              width: 6, height: 6, borderRadius: '50%',
              background: i === 1 ? color : MGMT.grayLight, opacity: i === 1 ? 1 : 0.3,
            }} />
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 12, color: i === 1 ? MGMT.white : MGMT.dimWhite, fontWeight: i === 1 ? 600 : 400 }}>
                {centerLabel || label} 项目 {i}
              </div>
              <div style={{ fontSize: 10, color: MGMT.grayLight, marginTop: 2 }}>
                {nodeId} · 示例数据
              </div>
            </div>
            <IconChevronRight size={12} style={{ color: MGMT.grayLight, opacity: i === 1 ? 1 : 0 }} />
          </div>
        ))}
      </div>
    </div>
  )
}

function L1Right({ rightLabel, color }: { rightLabel?: string; color: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 8, color: MGMT.grayLight }}>
      <IconListChecks size={32} style={{ opacity: 0.15 }} />
      <div style={{ fontSize: 12 }}>{rightLabel || '详情面板'}</div>
      <div style={{ fontSize: 10, opacity: 0.6 }}>选择左侧项目查看详情</div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// L2: 编辑器+预览
// ═══════════════════════════════════════════════════════════

function LayoutL2({ nodeId, label, color, centerLabel, rightLabel }: LayoutProps) {
  return { center: <L2Center nodeId={nodeId} label={label} color={color} centerLabel={centerLabel} />,
           right: <L2Right rightLabel={rightLabel} color={color} /> }
}

function L2Center({ nodeId, label, color, centerLabel }: { nodeId: string; label: string; color: string; centerLabel?: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      {/* 编辑器头 */}
      <div style={{
        padding: '8px 16px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 6,
      }}>
        <IconEdit size={12} style={{ color }} />
        <span style={{ fontSize: 11, color: MGMT.grayLight }}>{centerLabel || '编辑器'}</span>
        <span style={{ fontSize: 8, color: MGMT.grayLight, fontFamily: MGMT.codeFontFamily, marginLeft: 'auto' }}>{nodeId}</span>
      </div>
      {/* 编辑区 */}
      <div style={{
        flex: 1, padding: 16, fontFamily: MGMT.codeFontFamily,
        fontSize: 13, lineHeight: 1.8, color: MGMT.dimWhite,
        background: `${MGMT.white}02`,
      }}>
        <div style={{ opacity: 0.4, marginBottom: 12 }}>// {label} 编辑器</div>
        <div style={{
          padding: 16, border: `1px dashed ${MGMT.border}`, borderRadius: 8,
          textAlign: 'center', color: MGMT.grayLight, fontSize: 12,
          fontFamily: MGMT.fontFamily,
        }}>
          点击这里开始编辑内容
        </div>
      </div>
    </div>
  )
}

function L2Right({ rightLabel, color }: { rightLabel?: string; color: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <div style={{
        padding: '8px 16px', borderBottom: `1px solid ${MGMT.border}`,
        fontSize: 11, color: MGMT.grayLight, display: 'flex', alignItems: 'center', gap: 6,
      }}>
        <div style={{ width: 6, height: 6, borderRadius: '50%', background: color }} />
        {rightLabel || '实时预览'}
      </div>
      <div style={{
        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: MGMT.grayLight, flexDirection: 'column', gap: 8,
      }}>
        <IconEdit size={28} style={{ opacity: 0.15 }} />
        <div style={{ fontSize: 11 }}>预览区域</div>
        <div style={{ fontSize: 10, opacity: 0.5 }}>编辑器内容将在此实时渲染</div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// L3: 画布+属性
// ═══════════════════════════════════════════════════════════

function LayoutL3({ nodeId, label, color, centerLabel, rightLabel, description }: LayoutProps) {
  return { center: <L3Center nodeId={nodeId} label={label} color={color} centerLabel={centerLabel} description={description} />,
           right: <L3Right rightLabel={rightLabel} color={color} /> }
}

function L3Center({ nodeId, label, color, centerLabel, description }: {
  nodeId: string; label: string; color: string; centerLabel?: string; description?: string
}) {
  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{
        width: '80%', maxWidth: 640, aspectRatio: '16/9',
        border: `2px dashed ${color}30`, borderRadius: 12,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexDirection: 'column', gap: 8, background: `${color}05`,
      }}>
        <IconPalette2 size={36} style={{ color, opacity: 0.2 }} />
        <div style={{ fontSize: 14, fontWeight: 600, color: MGMT.dimWhite }}>{centerLabel || label}</div>
        <div style={{ fontSize: 10, color: MGMT.grayLight, fontFamily: MGMT.codeFontFamily }}>{nodeId}</div>
        {description && <div style={{ fontSize: 11, color: MGMT.grayLight, maxWidth: 300, textAlign: 'center' }}>{description}</div>}
      </div>
    </div>
  )
}

function L3Right({ rightLabel, color }: { rightLabel?: string; color: string }) {
  return (
    <div style={{ padding: 16 }}>
      <div style={{
        fontSize: 10, fontWeight: 700, color,
        textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12,
      }}>
        {rightLabel || '属性面板'}
      </div>
      {/* Demo 属性字段 */}
      {['名称', '类型', '颜色', '动画'].map(field => (
        <div key={field} style={{ marginBottom: 10 }}>
          <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 3 }}>{field}</div>
          <div style={{
            padding: '6px 10px', borderRadius: 4,
            background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
            fontSize: 12, color: MGMT.dimWhite,
          }}>—</div>
        </div>
      ))}
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// L4: 卡片网格
// ═══════════════════════════════════════════════════════════

function LayoutL4({ nodeId, label, color, centerLabel, rightLabel }: LayoutProps) {
  return { center: <L4Center nodeId={nodeId} label={label} color={color} centerLabel={centerLabel} />,
           right: <L4Right rightLabel={rightLabel} color={color} /> }
}

function L4Center({ nodeId, label, color, centerLabel }: { nodeId: string; label: string; color: string; centerLabel?: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <div style={{
        padding: '8px 16px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 6,
      }}>
        <IconImage2 size={12} style={{ color }} />
        <span style={{ fontSize: 11, color: MGMT.grayLight }}>{centerLabel || label}</span>
        <span style={{ fontSize: 9, color: MGMT.grayLight, marginLeft: 'auto' }}>8 项</span>
      </div>
      <div style={{
        flex: 1, overflowY: 'auto', padding: 12,
        display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
        gap: 8, alignContent: 'start',
      }}>
        {Array.from({length: 8}, (_, i) => (
          <div key={i} style={{
            aspectRatio: '4/3', borderRadius: 8,
            background: i === 0 ? `${color}15` : `${MGMT.white}04`,
            border: `1px solid ${i === 0 ? `${color}40` : MGMT.border}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexDirection: 'column', gap: 4, cursor: 'pointer',
            transition: 'all 0.15s',
          }}>
            <IconImage2 size={20} style={{ color: i === 0 ? color : MGMT.grayLight, opacity: 0.3 }} />
            <span style={{ fontSize: 9, color: MGMT.grayLight }}>{nodeId}.{i+1}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function L4Right({ rightLabel, color }: { rightLabel?: string; color: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 8, color: MGMT.grayLight }}>
      <IconImage2 size={32} style={{ opacity: 0.15 }} />
      <div style={{ fontSize: 12 }}>{rightLabel || '详情'}</div>
      <div style={{ fontSize: 10, opacity: 0.6 }}>选择卡片查看详情</div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// L5: 横向时间线
// ═══════════════════════════════════════════════════════════

function LayoutL5({ nodeId, label, color, centerLabel, rightLabel }: LayoutProps) {
  return { center: <L5Center nodeId={nodeId} label={label} color={color} centerLabel={centerLabel} />,
           right: <L5Right rightLabel={rightLabel} color={color} /> }
}

function L5Center({ nodeId, label, color, centerLabel }: { nodeId: string; label: string; color: string; centerLabel?: string }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      {/* 上部：内容区 */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', color: MGMT.grayLight }}>
          <IconClock size={36} style={{ opacity: 0.15, marginBottom: 8 }} />
          <div style={{ fontSize: 13, color: MGMT.dimWhite }}>{centerLabel || label}</div>
          <div style={{ fontSize: 10, fontFamily: MGMT.codeFontFamily, marginTop: 4 }}>{nodeId}</div>
        </div>
      </div>
      {/* 下部：横向轨道 */}
      <div style={{
        height: 100, borderTop: `1px solid ${MGMT.border}`,
        background: `${MGMT.white}02`, padding: '10px 16px',
      }}>
        <div style={{ fontSize: 9, color: MGMT.grayLight, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6 }}>
          轨道 TRACK
        </div>
        <div style={{ display: 'flex', gap: 4, height: 36 }}>
          {[0.2, 0.35, 0.15, 0.3].map((w, i) => (
            <div key={i} style={{
              flex: w, height: '100%', borderRadius: 4,
              background: `${color}${i === 1 ? '30' : '15'}`,
              border: `1px solid ${color}${i === 1 ? '50' : '25'}`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <span style={{ fontSize: 8, color, fontFamily: MGMT.codeFontFamily }}>
                {(w * 30).toFixed(0)}s
              </span>
            </div>
          ))}
        </div>
        {/* 时间刻度 */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4 }}>
          {['0:00', '0:10', '0:20', '0:30'].map(t => (
            <span key={t} style={{ fontSize: 8, color: MGMT.grayLight, fontFamily: MGMT.codeFontFamily }}>{t}</span>
          ))}
        </div>
      </div>
    </div>
  )
}

function L5Right({ rightLabel, color }: { rightLabel?: string; color: string }) {
  return (
    <div style={{ padding: 16 }}>
      <div style={{
        fontSize: 10, fontWeight: 700, color,
        textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12,
      }}>
        {rightLabel || '时间属性'}
      </div>
      {['起始时间', '结束时间', '时长', '偏移量'].map(field => (
        <div key={field} style={{ marginBottom: 10 }}>
          <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 3 }}>{field}</div>
          <div style={{
            padding: '6px 10px', borderRadius: 4,
            background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
            fontSize: 12, color: MGMT.dimWhite, fontFamily: MGMT.codeFontFamily,
          }}>0:00.000</div>
        </div>
      ))}
    </div>
  )
}

// ─── 获取布局图标 ───

export function getLayoutIcon(layout: LayoutType, size: number) {
  const Icon = LAYOUT_ICONS[layout]
  return <Icon size={size} />
}
