// ═══════════════════════════════════════════════════════════
// 右栏 — 可编辑的属性面板
// AssetEditPanel — Right sidebar property editor
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { ASSET_CATEGORIES, getCategoryMeta } from '@/lib/asset-types'
import { SourceIcon } from '@/components/AssetIcons'
import {
  IconEdit, IconPlus, IconX, IconTrash, IconCopy,
  IconCheck, IconBlocks,
} from '@/components/Icons'
import type { Asset } from '@/lib/asset-types'
import { EditInput, FieldLabel, MiniBtn } from './shared'

export function AssetEditPanel({ asset, draft, isDirty, onUpdate, onSave, onDelete, onDuplicate }: {
  asset: Asset; draft: Partial<Asset>; isDirty: boolean
  onUpdate: (field: string, value: any) => void
  onSave: () => void; onDelete: () => void; onDuplicate: () => void
}) {
  const catMeta = getCategoryMeta(asset.category)
  const accent = catMeta?.color || MGMT.gold
  const [newTag, setNewTag] = useState('')

  function addTag() {
    if (!newTag.trim()) return
    const tags = [...(draft.tags || asset.tags), newTag.trim()]
    onUpdate('tags', tags)
    setNewTag('')
  }

  function removeTag(t: string) {
    onUpdate('tags', (draft.tags || asset.tags).filter((x: string) => x !== t))
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* 头部 + 保存按钮 */}
      <div style={{
        padding: '8px 12px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 6,
      }}>
        <IconEdit size={12} style={{ color: accent }} />
        <span style={{ fontSize: 11, color: MGMT.dimWhite, fontWeight: 600, flex: 1 }}>编辑</span>
        {isDirty && (
          <span onClick={onSave} style={{
            fontSize: 10, padding: '3px 10px', borderRadius: 4,
            background: `${accent}20`, color: accent,
            cursor: 'pointer', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 3,
            border: `1px solid ${accent}40`,
          }}>
            <IconCheck size={10} /> 保存
          </span>
        )}
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: 12, display: 'flex', flexDirection: 'column', gap: 10 }}>
        {/* 名称 */}
        <EditInput label="名称" value={draft.name || ''} accent={accent}
          onChange={v => onUpdate('name', v)} />

        {/* 分类 */}
        <div>
          <FieldLabel>分类</FieldLabel>
          <select
            value={draft.category || asset.category}
            onChange={e => onUpdate('category', e.target.value)}
            style={{
              width: '100%', padding: '6px 8px', borderRadius: 4,
              background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
              color: MGMT.white, fontSize: 11, fontFamily: MGMT.fontFamily,
              outline: 'none', cursor: 'pointer',
            }}
          >
            {ASSET_CATEGORIES.map(c => (
              <option key={c.id} value={c.id} style={{ background: '#1a1a2e', color: '#fff' }}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        {/* 课程 + 主题 */}
        <div style={{ display: 'flex', gap: 6 }}>
          <EditInput label="课程" value={draft.course || ''} accent={accent}
            onChange={v => onUpdate('course', v)} style={{ flex: 1 }} />
          <EditInput label="主题" value={draft.topic || ''} accent={accent}
            onChange={v => onUpdate('topic', v)} style={{ flex: 1 }} />
        </div>

        {/* 标签 */}
        <div>
          <FieldLabel>标签</FieldLabel>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 4 }}>
            {(draft.tags || asset.tags).map((t: string) => (
              <span key={t} style={{
                fontSize: 10, padding: '3px 6px', borderRadius: 4,
                background: `${MGMT.white}08`, color: MGMT.dimWhite,
                display: 'flex', alignItems: 'center', gap: 3,
              }}>
                {t}
                <IconX size={8} onClick={() => removeTag(t)}
                  style={{ color: MGMT.grayLight, cursor: 'pointer' }} />
              </span>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 4 }}>
            <input value={newTag} onChange={e => setNewTag(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && addTag()}
              placeholder="添加标签..."
              style={{
                flex: 1, padding: '4px 8px', borderRadius: 4,
                background: `${MGMT.white}06`, border: `1px solid ${MGMT.border}`,
                color: MGMT.white, fontSize: 10, fontFamily: MGMT.fontFamily, outline: 'none',
              }}
            />
            <span onClick={addTag} style={{
              padding: '4px 8px', borderRadius: 4,
              background: `${accent}15`, color: accent,
              cursor: 'pointer', display: 'flex', alignItems: 'center',
              fontSize: 10,
            }}>
              <IconPlus size={8} />
            </span>
          </div>
        </div>

        {/* 来源 */}
        <div>
          <FieldLabel>来源</FieldLabel>
          {asset.sources.map((s, i) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 5, fontSize: 10,
              color: MGMT.dimWhite, marginBottom: 3,
              padding: '3px 6px', borderRadius: 3, background: `${MGMT.white}04`,
            }}>
              <SourceIcon type={s.type} size={10} style={{ color: MGMT.grayLight }} />
              <span style={{ flex: 1 }}>{s.cite}</span>
            </div>
          ))}
        </div>

        {/* 兼容积木 */}
        {asset.compatibleBlocks && (
          <div>
            <FieldLabel>兼容积木</FieldLabel>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {asset.compatibleBlocks.map(b => (
                <span key={b} style={{
                  fontSize: 9, padding: '2px 6px', borderRadius: 3,
                  background: `${MGMT.gold}10`, color: MGMT.gold, fontFamily: MGMT.codeFontFamily,
                  display: 'flex', alignItems: 'center', gap: 2,
                }}>
                  <IconBlocks size={8} /> {b}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* 元数据 */}
        <div style={{
          padding: '8px 10px', borderRadius: 5,
          background: `${MGMT.white}04`, fontSize: 9, color: MGMT.grayLight,
          display: 'flex', flexDirection: 'column', gap: 2,
        }}>
          <div>ID: <span style={{ fontFamily: MGMT.codeFontFamily, color: MGMT.dimWhite }}>{asset.id}</span></div>
          <div>创建: {asset.createdAt}</div>
          {asset.updatedAt && <div>更新: {asset.updatedAt}</div>}
        </div>

        {/* 危险操作 */}
        <div style={{ display: 'flex', gap: 6, marginTop: 4 }}>
          <MiniBtn label="复制" icon={<IconCopy size={9} />} onClick={onDuplicate} color={accent} />
          <MiniBtn label="删除" icon={<IconTrash size={9} />} onClick={onDelete} color="#e74c3c" />
        </div>
      </div>
    </div>
  )
}
