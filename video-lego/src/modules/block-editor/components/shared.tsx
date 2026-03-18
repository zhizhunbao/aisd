// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 共享原子组件
// Block Editor — Shared atomic UI components
// ═══════════════════════════════════════════════════════════

import React from 'react'
import { MGMT } from '@/theme'

/** 分组标签 */
export function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      fontSize: 11, color: MGMT.grayLight, fontWeight: 700,
      letterSpacing: 0.5, marginBottom: 8, marginTop: 16,
      textTransform: 'uppercase',
    }}>{children}</div>
  )
}

/** 文本输入 */
export function InputField({ label, value, onChange, placeholder, required, mono }: {
  label: string; value: string; onChange: (v: string) => void
  placeholder?: string; required?: boolean; mono?: boolean
}) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 4 }}>
        {label}{required && <span style={{ color: MGMT.red, marginLeft: 2 }}>*</span>}
      </div>
      <input value={value} onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 6, padding: '8px 10px', color: MGMT.white,
          fontFamily: mono ? MGMT.codeFontFamily : MGMT.fontFamily,
          fontSize: 13, width: '100%', outline: 'none', boxSizing: 'border-box',
          transition: 'border 0.15s',
        }}
        onFocus={e => (e.currentTarget.style.borderColor = `${MGMT.gold}40`)}
        onBlur={e => (e.currentTarget.style.borderColor = MGMT.border)}
      />
    </div>
  )
}

/** 多行文本输入 */
export function TextAreaField({ label, value, onChange, placeholder, rows, mono }: {
  label: string; value: string; onChange: (v: string) => void
  placeholder?: string; rows?: number; mono?: boolean
}) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 4 }}>{label}</div>
      <textarea value={value} onChange={e => onChange(e.target.value)}
        placeholder={placeholder} rows={rows ?? 4}
        style={{
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 6, padding: '8px 10px', color: MGMT.white,
          fontFamily: mono ? MGMT.codeFontFamily : MGMT.fontFamily,
          fontSize: 13, width: '100%', outline: 'none', boxSizing: 'border-box',
          resize: 'vertical', transition: 'border 0.15s', lineHeight: 1.5,
        }}
        onFocus={e => (e.currentTarget.style.borderColor = `${MGMT.gold}40`)}
        onBlur={e => (e.currentTarget.style.borderColor = MGMT.border)}
      />
    </div>
  )
}

/** 数字输入 */
export function NumberField({ label, value, onChange, min, max, step }: {
  label: string; value: number; onChange: (v: number) => void
  min?: number; max?: number; step?: number
}) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 4 }}>{label}</div>
      <input type="number" value={value} min={min} max={max} step={step}
        onChange={e => onChange(Number(e.target.value))}
        style={{
          background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
          borderRadius: 6, padding: '8px 10px', color: MGMT.white,
          fontFamily: MGMT.codeFontFamily, fontSize: 13, width: '100%',
          outline: 'none', boxSizing: 'border-box', transition: 'border 0.15s',
        }}
        onFocus={e => (e.currentTarget.style.borderColor = `${MGMT.gold}40`)}
        onBlur={e => (e.currentTarget.style.borderColor = MGMT.border)}
      />
    </div>
  )
}

/** 颜色选择器 */
export function ColorField({ label, value, onChange }: {
  label: string; value: string; onChange: (v: string) => void
}) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 4 }}>{label}</div>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <input type="color" value={value || '#ffffff'}
          onChange={e => onChange(e.target.value)}
          style={{
            width: 32, height: 32, border: `1px solid ${MGMT.border}`,
            borderRadius: 6, cursor: 'pointer', background: 'transparent', padding: 0,
          }}
        />
        <input value={value || ''} onChange={e => onChange(e.target.value)}
          placeholder="#ffffff"
          style={{
            background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
            borderRadius: 6, padding: '6px 8px', color: MGMT.white,
            fontFamily: MGMT.codeFontFamily, fontSize: 12, flex: 1,
            outline: 'none', boxSizing: 'border-box',
          }}
        />
      </div>
    </div>
  )
}

/** 下拉选择 */
export function SelectField({ label, value, onChange, options }: {
  label: string; value: string; onChange: (v: string) => void
  options: { value: string; label: string }[]
}) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginBottom: 4 }}>{label}</div>
      <select value={value} onChange={e => onChange(e.target.value)}
        style={{
          background: MGMT.bgInput, border: `1px solid ${MGMT.border}`,
          borderRadius: 6, padding: '8px 10px', color: MGMT.white,
          fontFamily: MGMT.fontFamily, fontSize: 13, width: '100%',
          outline: 'none', boxSizing: 'border-box', cursor: 'pointer',
        }}>
        {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  )
}

/** 布尔开关 */
export function BooleanField({ label, value, onChange }: {
  label: string; value: boolean; onChange: (v: boolean) => void
}) {
  return (
    <div style={{
      marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8,
      cursor: 'pointer',
    }} onClick={() => onChange(!value)}>
      <div style={{
        width: 36, height: 20, borderRadius: 10,
        background: value ? `${MGMT.green}60` : `${MGMT.white}12`,
        border: `1px solid ${value ? MGMT.green : MGMT.border}`,
        position: 'relative', transition: 'all 0.2s',
      }}>
        <div style={{
          width: 14, height: 14, borderRadius: '50%',
          background: value ? MGMT.green : MGMT.grayLight,
          position: 'absolute', top: 2, left: value ? 19 : 2,
          transition: 'all 0.2s', boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
        }} />
      </div>
      <span style={{ fontSize: 12, color: MGMT.dimWhite }}>{label}</span>
    </div>
  )
}

/** 小按钮 */
export function SmallBtn({ color, disabled, onClick, children, style }: {
  color: string; disabled?: boolean; onClick: (e: React.MouseEvent) => void
  children: React.ReactNode; style?: React.CSSProperties
}) {
  return (
    <button disabled={disabled} onClick={onClick} style={{
      background: `${color}12`, border: `1px solid ${color}30`, color,
      borderRadius: 4, cursor: disabled ? 'default' : 'pointer',
      padding: '3px 8px', fontSize: 11, fontWeight: 600,
      opacity: disabled ? 0.3 : 1, fontFamily: MGMT.fontFamily,
      transition: 'all 0.15s', ...style,
    }}>{children}</button>
  )
}

/** 可拖拽分隔条 */
export function DividerHandle({ side, draggingRef }: {
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
