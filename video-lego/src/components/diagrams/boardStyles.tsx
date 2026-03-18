// ═══════════════════════════════════════════════════════════
// 三栏板书 — 共享布局样式 & SVG 小图标
// 所有 Diagram 组件复用此模块
// ═══════════════════════════════════════════════════════════

import React from 'react'

// ─── SVG 小图标 (替代 emoji) ───

/** 公式图标 ∫ */
export const IconFormula: React.FC<{ size?: number; color?: string }> = ({ size = 14, color = '#888' }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="none" style={{ verticalAlign: 'middle', marginRight: 4 }}>
    <path d="M5 2c1.5 0 2 1 2 2.5L6 9c-.3 1.5-1 2.5-2.5 2.5" stroke={color} strokeWidth="1.5" strokeLinecap="round" fill="none" />
    <line x1="3.5" y1="7" x2="8.5" y2="7" stroke={color} strokeWidth="1.2" />
    <circle cx="12" cy="5" r="1" fill={color} opacity={0.6} />
    <path d="M10 9l2-2 2 2" stroke={color} strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
  </svg>
)

/** 已知/设 图标 (列表) */
export const IconGiven: React.FC<{ size?: number; color?: string }> = ({ size = 14, color = '#888' }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="none" style={{ verticalAlign: 'middle', marginRight: 4 }}>
    <rect x="2" y="1" width="12" height="14" rx="2" stroke={color} strokeWidth="1.2" fill="none" />
    <line x1="5" y1="5" x2="11" y2="5" stroke={color} strokeWidth="1" opacity={0.7} />
    <line x1="5" y1="8" x2="11" y2="8" stroke={color} strokeWidth="1" opacity={0.7} />
    <line x1="5" y1="11" x2="9" y2="11" stroke={color} strokeWidth="1" opacity={0.7} />
  </svg>
)

/** 图解/求解 图标 (笔+尺) */
export const IconSolve: React.FC<{ size?: number; color?: string }> = ({ size = 14, color = '#888' }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="none" style={{ verticalAlign: 'middle', marginRight: 4 }}>
    <path d="M2 14L12 4l2 2L4 16" stroke={color} strokeWidth="1.2" fill="none" />
    <path d="M11 3l2-2 2 2-2 2" stroke={color} strokeWidth="1.2" fill="none" />
    <line x1="1" y1="15" x2="6" y2="15" stroke={color} strokeWidth="1.2" opacity={0.5} />
  </svg>
)

// ─── 共享布局样式 ───

export const colStyle = (flex: number): React.CSSProperties => ({
  flex, padding: '10px 12px', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start',
})

export const dividerStyle: React.CSSProperties = {
  width: 1, background: 'rgba(255,255,255,0.08)', alignSelf: 'stretch',
}

export const colLabelStyle: React.CSSProperties = {
  fontSize: 11, color: '#888', fontWeight: 700, marginBottom: 8,
  borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: 4,
  display: 'flex', alignItems: 'center',
}

export const givenLineStyle: React.CSSProperties = {
  fontSize: 12, color: '#ccc', lineHeight: 1.8, margin: 0,
}

/** 顶部公式标题栏样式 */
export const titleBarStyle: React.CSSProperties = {
  padding: '8px 14px',
  borderBottom: '1px solid rgba(255,255,255,0.06)',
  background: 'rgba(255,255,255,0.02)',
}

/** 三栏容器样式 */
export const boardStyle: React.CSSProperties = {
  display: 'flex', gap: 0,
  background: 'rgba(255,255,255,0.02)', borderRadius: 8,
  border: '1px solid rgba(255,255,255,0.06)',
  overflow: 'hidden',
}

/** 结论框样式 */
export const conclusionStyle: React.CSSProperties = {
  marginTop: 6, padding: '4px 8px',
  background: 'rgba(255,215,0,0.08)', borderRadius: 4,
  borderLeft: '3px solid #FFD700', fontSize: 12,
}
