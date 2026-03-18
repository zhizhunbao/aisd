// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 右侧参数编辑面板
// Block Editor — Right Panel: Props editor
//
// 根据 BlockFieldSchema 自动生成可编辑表单
// 支持: 简单字段 + 数组字段 + JSON 原始编辑
// ═══════════════════════════════════════════════════════════

import { useState, useCallback } from 'react'
import { MGMT } from '@/theme'
import { getBlockMeta } from '@blocks/catalog'
import { getBlockSchema } from '../defaults'
import {
  SectionLabel, InputField, TextAreaField, NumberField,
  ColorField, SelectField, BooleanField, SmallBtn,
} from './shared'
import { IconPlus, IconTrash, IconArrowUp, IconArrowDown, IconDownload, IconEdit, IconJson, IconWarning } from '@/components/Icons'
import type { FieldDescriptor, ArrayFieldDescriptor } from '../types'

interface PropsEditorProps {
  blockName: string
  data: Record<string, unknown>
  onChange: (data: Record<string, unknown>) => void
}

export function PropsEditor({ blockName, data, onChange }: PropsEditorProps) {
  const [tab, setTab] = useState<'form' | 'json'>('form')
  const meta = getBlockMeta(blockName)
  const schema = getBlockSchema(blockName)
  const hasSchema = schema.fields.length > 0 || schema.arrayFields.length > 0

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* 标题 + Tab */}
      <div style={{
        padding: '12px 16px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 8,
      }}>
        <span style={{
          width: 8, height: 8, borderRadius: '50%',
          background: meta?.category.color || MGMT.grayLight,
        }} />
        <span style={{
          fontSize: 14, fontWeight: 700, flex: 1,
          fontFamily: MGMT.codeFontFamily, color: MGMT.white,
        }}>
          {blockName}
        </span>
      </div>

      {/* Tab 切换 */}
      <div style={{ display: 'flex', borderBottom: `1px solid ${MGMT.border}` }}>
        {(['form', 'json'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            flex: 1, padding: 10, fontSize: 12, cursor: 'pointer',
            fontWeight: tab === t ? 700 : 400,
            color: tab === t ? MGMT.gold : MGMT.grayLight,
            background: tab === t ? `${MGMT.gold}08` : 'transparent',
            borderBottom: `2px solid ${tab === t ? MGMT.gold : 'transparent'}`,
            border: 'none', fontFamily: MGMT.fontFamily, transition: 'all 0.15s',
          }}>
            {t === 'form'
              ? <><IconEdit size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} /> 表单</>
              : <><IconJson size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} /> JSON</>}
          </button>
        ))}
      </div>

      {/* 编辑区 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {tab === 'form' ? (
          hasSchema
            ? <FormEditor schema={schema} data={data} onChange={onChange} />
            : <NoSchemaFallback blockName={blockName} data={data} onChange={onChange} />
        ) : (
          <JsonEditor data={data} onChange={onChange} />
        )}
      </div>

      {/* 底部操作栏 */}
      <div style={{
        padding: '10px 12px', borderTop: `1px solid ${MGMT.border}`,
        display: 'flex', gap: 8,
      }}>
        <SmallBtn color={MGMT.blue} onClick={() => {
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
          const a = document.createElement('a')
          a.href = URL.createObjectURL(blob)
          a.download = `${blockName}-data.json`
          a.click()
        }}>
          <IconDownload size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />
          导出 JSON
        </SmallBtn>
      </div>
    </div>
  )
}

// ═══════════════ 表单编辑器 ═══════════════

function FormEditor({ schema, data, onChange }: {
  schema: ReturnType<typeof getBlockSchema>
  data: Record<string, unknown>
  onChange: (data: Record<string, unknown>) => void
}) {
  // 按 group 分组字段
  const groups = new Map<string, FieldDescriptor[]>()
  for (const f of schema.fields) {
    const g = f.group || '基本属性'
    if (!groups.has(g)) groups.set(g, [])
    groups.get(g)!.push(f)
  }

  const updateField = useCallback((key: string, value: unknown) => {
    // 支持点号路径 e.g. 'left.icon'
    if (key.includes('.')) {
      const parts = key.split('.')
      const newData = { ...data }
      let obj = newData as Record<string, unknown>
      for (let i = 0; i < parts.length - 1; i++) {
        if (typeof obj[parts[i]] !== 'object' || obj[parts[i]] === null) {
          obj[parts[i]] = {}
        }
        obj[parts[i]] = { ...(obj[parts[i]] as Record<string, unknown>) }
        obj = obj[parts[i]] as Record<string, unknown>
      }
      obj[parts[parts.length - 1]] = value
      onChange(newData)
    } else {
      onChange({ ...data, [key]: value })
    }
  }, [data, onChange])

  const getFieldValue = useCallback((key: string): unknown => {
    if (key.includes('.')) {
      const parts = key.split('.')
      let obj: unknown = data
      for (const p of parts) {
        if (obj && typeof obj === 'object') obj = (obj as Record<string, unknown>)[p]
        else return undefined
      }
      return obj
    }
    return data[key]
  }, [data])

  return (
    <>
      {/* 简单字段 */}
      {Array.from(groups.entries()).map(([groupName, fields]) => (
        <div key={groupName}>
          <SectionLabel>{groupName}</SectionLabel>
          {fields.map(f => (
            <FieldControl
              key={f.key}
              field={f}
              value={getFieldValue(f.key)}
              onChange={v => updateField(f.key, v)}
            />
          ))}
        </div>
      ))}

      {/* 数组字段 */}
      {schema.arrayFields.map(af => (
        <ArrayFieldEditor
          key={af.key}
          field={af}
          items={getFieldValue(af.key) as unknown[] || []}
          onChange={items => updateField(af.key, items)}
        />
      ))}
    </>
  )
}

// ─── 单个字段控件 ───

function FieldControl({ field, value, onChange }: {
  field: FieldDescriptor; value: unknown; onChange: (v: unknown) => void
}) {
  switch (field.type) {
    case 'text':
    case 'latex':
      return <InputField
        label={field.label} value={String(value ?? '')}
        onChange={onChange} placeholder={field.placeholder}
        required={field.required} mono={field.type === 'latex'}
      />
    case 'textarea':
      return <TextAreaField
        label={field.label} value={String(value ?? '')}
        onChange={onChange} placeholder={field.placeholder}
      />
    case 'code':
      return <TextAreaField
        label={field.label} value={String(value ?? '')}
        onChange={onChange} rows={8} mono
      />
    case 'number':
      return <NumberField
        label={field.label} value={Number(value ?? 0)}
        onChange={onChange}
      />
    case 'color':
      return <ColorField
        label={field.label} value={String(value ?? '')}
        onChange={onChange}
      />
    case 'select':
      return <SelectField
        label={field.label} value={String(value ?? '')}
        onChange={onChange} options={field.options || []}
      />
    case 'boolean':
      return <BooleanField
        label={field.label} value={Boolean(value)}
        onChange={onChange}
      />
    default:
      return <InputField label={field.label} value={String(value ?? '')} onChange={onChange} />
  }
}

// ─── 数组字段编辑器 ───

function ArrayFieldEditor({ field, items, onChange }: {
  field: ArrayFieldDescriptor
  items: unknown[]
  onChange: (items: unknown[]) => void
}) {
  const addItem = () => {
    const newItem = typeof field.itemDefault === 'object' && field.itemDefault !== null
      ? { ...field.itemDefault }
      : field.itemDefault
    onChange([...items, newItem])
  }

  const removeItem = (i: number) => onChange(items.filter((_, idx) => idx !== i))
  const moveItem = (i: number, dir: -1 | 1) => {
    const j = i + dir
    if (j < 0 || j >= items.length) return
    const next = [...items];
    [next[i], next[j]] = [next[j], next[i]]
    onChange(next)
  }
  const updateItem = (i: number, value: unknown) => {
    const next = [...items]
    next[i] = value
    onChange(next)
  }

  return (
    <div style={{ marginBottom: 16 }}>
      <SectionLabel>
        {field.group ? `${field.group} · ` : ''}{field.label} ({items.length})
      </SectionLabel>

      {items.map((item, i) => (
        <div key={i} style={{
          background: `${MGMT.white}04`, borderRadius: 8,
          border: `1px solid ${MGMT.border}`, padding: 10, marginBottom: 6,
        }}>
          {/* 项头 */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 4, marginBottom: 8,
            paddingBottom: 6, borderBottom: `1px solid ${MGMT.border}`,
          }}>
            <span style={{ fontSize: 10, color: MGMT.grayLight, flex: 1, fontFamily: MGMT.codeFontFamily }}>
              [{i}]
            </span>
            <SmallBtn color={MGMT.grayLight} onClick={() => moveItem(i, -1)} disabled={i === 0}>
              <IconArrowUp size={10} />
            </SmallBtn>
            <SmallBtn color={MGMT.grayLight} onClick={() => moveItem(i, 1)} disabled={i === items.length - 1}>
              <IconArrowDown size={10} />
            </SmallBtn>
            <SmallBtn color={MGMT.red} onClick={() => removeItem(i)}>
              <IconTrash size={10} />
            </SmallBtn>
          </div>

          {/* 如果是简单值（string） */}
          {typeof item !== 'object' || item === null ? (
            <InputField
              label="值" value={String(item ?? '')}
              onChange={v => updateItem(i, v)}
            />
          ) : (
            /* 如果是对象 */
            field.itemFields.map(f => (
              <FieldControl
                key={f.key}
                field={f}
                value={(item as Record<string, unknown>)[f.key]}
                onChange={v => updateItem(i, { ...(item as Record<string, unknown>), [f.key]: v })}
              />
            ))
          )}
        </div>
      ))}

      <button onClick={addItem}
        style={{
          width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4,
          background: `${MGMT.green}08`, border: `1px dashed ${MGMT.green}30`,
          borderRadius: 6, padding: '8px 0', cursor: 'pointer',
          color: MGMT.green, fontSize: 11, fontWeight: 600, fontFamily: MGMT.fontFamily,
          transition: 'all 0.15s',
        }}
        onMouseEnter={e => { e.currentTarget.style.background = `${MGMT.green}14` }}
        onMouseLeave={e => { e.currentTarget.style.background = `${MGMT.green}08` }}
      >
        <IconPlus size={12} /> 添加 {field.label}
      </button>
    </div>
  )
}

// ═══════════════ JSON 编辑器 ═══════════════

function JsonEditor({ data, onChange }: {
  data: Record<string, unknown>; onChange: (data: Record<string, unknown>) => void
}) {
  const [text, setText] = useState(() => JSON.stringify(data, null, 2))
  const [error, setError] = useState<string | null>(null)

  const handleBlur = () => {
    try {
      const parsed = JSON.parse(text)
      onChange(parsed)
      setError(null)
    } catch (e) {
      setError((e as Error).message)
    }
  }

  return (
    <div>
      <SectionLabel>JSON 数据</SectionLabel>
      {error && (
        <div style={{
          fontSize: 11, color: MGMT.red, padding: '6px 8px',
          background: `${MGMT.red}10`, borderRadius: 4, marginBottom: 8,
        }}>
          <IconWarning size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />{error}
        </div>
      )}
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        onBlur={handleBlur}
        spellCheck={false}
        style={{
          width: '100%', minHeight: 400, boxSizing: 'border-box',
          background: `${MGMT.white}06`, border: `1px solid ${error ? MGMT.red : MGMT.border}`,
          borderRadius: 8, padding: 12, color: MGMT.white,
          fontFamily: MGMT.codeFontFamily, fontSize: 12, lineHeight: 1.6,
          outline: 'none', resize: 'vertical', transition: 'border 0.15s',
        }}
        onFocus={e => { if (!error) e.currentTarget.style.borderColor = `${MGMT.gold}40` }}
      />
      <div style={{ fontSize: 10, color: MGMT.grayLight, marginTop: 4 }}>
        编辑后点击其他区域应用更改
      </div>
    </div>
  )
}

// ─── 无 Schema 回退 ───

function NoSchemaFallback({ blockName, data, onChange }: {
  blockName: string; data: Record<string, unknown>; onChange: (data: Record<string, unknown>) => void
}) {
  return (
    <div>
      <div style={{
        fontSize: 12, color: MGMT.dimWhite, padding: '12px 0', lineHeight: 1.6,
      }}>
        <span style={{ color: MGMT.gold }}>「{blockName}」</span> 暂无表单 Schema，<br />
        请使用 JSON 模式编辑数据。
      </div>
      <JsonEditor data={data} onChange={onChange} />
    </div>
  )
}
