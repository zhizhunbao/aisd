// ═══════════════════════════════════════════════════════════
// 素材详情页 — 拆为两栏: 中栏(预览) + 右栏(编辑)
// AssetDetailView — split: center(preview) + right(edit)
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { ASSET_CATEGORIES, getCategoryMeta } from '@/lib/asset-types'
import { AssetCatIcon, SourceIcon } from '@/components/AssetIcons'
import { AssetPreview } from '@/components/AssetPreview'
import {
  IconArrowLeft, IconCheck, IconPlus, IconX, IconTrash,
  IconCopy, IconBlocks, IconEdit,
} from '@/components/Icons'
import type { Asset } from '@/lib/asset-types'
import { EditInput, FieldLabel, MiniBtn, getPreviewText } from './shared'

// ═══════════════════════════════════════════════════════════
// 中栏: 大预览 + 顶部返回栏
// ═══════════════════════════════════════════════════════════

export function AssetPreviewPanel({ asset, draft, onBack }: {
  asset: Asset; draft: Partial<Asset>; onBack: () => void
}) {
  const catMeta = getCategoryMeta(draft.category || asset.category)
  const accent = catMeta?.color || MGMT.gold

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* 顶部: 返回 + 标题 */}
      <div style={{
        padding: '8px 14px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 8,
        background: `${accent}04`,
      }}>
        <span onClick={onBack} style={{
          padding: '4px 8px', borderRadius: 4, cursor: 'pointer',
          color: MGMT.dimWhite, display: 'flex', alignItems: 'center', gap: 4,
          fontSize: 11, fontWeight: 500, background: `${MGMT.white}06`,
        }}
          onMouseEnter={e => e.currentTarget.style.background = `${MGMT.white}12`}
          onMouseLeave={e => e.currentTarget.style.background = `${MGMT.white}06`}
        >
          <IconArrowLeft size={12} /> 返回列表
        </span>

        <AssetCatIcon catId={asset.category} size={14} style={{ color: accent }} />
        <span style={{ fontSize: 14, fontWeight: 700, color: MGMT.white }}>
          {draft.name || asset.name}
        </span>
        <span style={{ fontSize: 10, color: MGMT.grayLight }}>{catMeta?.name}</span>
      </div>

      {/* 大预览区域 */}
      <div style={{
        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: `linear-gradient(135deg, ${accent}06, ${accent}02)`,
        position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0, height: 3,
          background: `linear-gradient(90deg, ${accent}, ${accent}40)`,
        }} />
        <div style={{ transform: 'scale(1.5)', padding: 30 }}>
          <AssetPreview asset={{ ...asset, ...draft } as Asset} isStatic={false} />
        </div>
      </div>

      {/* 底部元数据条 */}
      <div style={{
        padding: '6px 14px', borderTop: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 14,
        fontSize: 9, color: MGMT.grayLight,
      }}>
        <span>ID: <span style={{ fontFamily: MGMT.codeFontFamily, color: MGMT.dimWhite }}>{asset.id}</span></span>
        <span>创建: {asset.createdAt}</span>
        {asset.updatedAt && <span>更新: {asset.updatedAt}</span>}
        <span>类型: <span style={{ fontFamily: MGMT.codeFontFamily, color: MGMT.dimWhite }}>{asset.atomType}</span></span>
        <div style={{ flex: 1 }} />
        {asset.tags.map(t => (
          <span key={t} style={{
            fontSize: 8, padding: '1px 5px', borderRadius: 3,
            background: `${accent}12`, color: accent,
          }}>{t}</span>
        ))}
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// 右栏: 编辑面板
// ═══════════════════════════════════════════════════════════

export function AssetEditSidebar({ asset, draft, isDirty,
  onUpdate, onSave, onDelete, onDuplicate }: {
  asset: Asset; draft: Partial<Asset>; isDirty: boolean
  onUpdate: (field: string, value: any) => void
  onSave: () => void; onDelete: () => void; onDuplicate: () => void
}) {
  const catMeta = getCategoryMeta(draft.category || asset.category)
  const accent = catMeta?.color || MGMT.gold
  const [newTag, setNewTag] = useState('')

  function addTag() {
    if (!newTag.trim()) return
    onUpdate('tags', [...(draft.tags || []), newTag.trim()])
    setNewTag('')
  }

  function removeTag(t: string) {
    onUpdate('tags', (draft.tags || []).filter((x: string) => x !== t))
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* 头部 */}
      <div style={{
        padding: '8px 12px', borderBottom: `1px solid ${MGMT.border}`,
        display: 'flex', alignItems: 'center', gap: 6,
      }}>
        <IconEdit size={12} style={{ color: accent }} />
        <span style={{ fontSize: 12, color: MGMT.dimWhite, fontWeight: 600, flex: 1 }}>属性编辑</span>
        {isDirty && (
          <span onClick={onSave} style={{
            fontSize: 10, padding: '3px 10px', borderRadius: 4,
            background: `${accent}20`, color: accent,
            cursor: 'pointer', fontWeight: 700,
            display: 'flex', alignItems: 'center', gap: 3,
            border: `1px solid ${accent}40`,
          }}>
            <IconCheck size={10} /> 保存
          </span>
        )}
      </div>

      {/* 字段 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 12, display: 'flex', flexDirection: 'column', gap: 12 }}>
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
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 5 }}>
            {(draft.tags || []).map((t: string) => (
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
          {asset.sources.length > 0 ? asset.sources.map((s, i) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 5, fontSize: 10,
              color: MGMT.dimWhite, marginBottom: 3,
              padding: '3px 6px', borderRadius: 3, background: `${MGMT.white}04`,
            }}>
              <SourceIcon type={s.type} size={10} style={{ color: MGMT.grayLight }} />
              <span style={{ flex: 1 }}>{s.cite}</span>
            </div>
          )) : (
            <div style={{ fontSize: 10, color: MGMT.grayLight, fontStyle: 'italic' }}>无来源</div>
          )}
        </div>

        {/* 兼容积木 */}
        {asset.compatibleBlocks && asset.compatibleBlocks.length > 0 && (
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

        {/* 操作 */}
        <div style={{ display: 'flex', gap: 6, marginTop: 6 }}>
          <MiniBtn label="复制" icon={<IconCopy size={9} />} onClick={onDuplicate} color={accent} />
          <MiniBtn label="删除" icon={<IconTrash size={9} />} onClick={onDelete} color="#e74c3c" />
        </div>
      </div>
    </div>
  )
}
